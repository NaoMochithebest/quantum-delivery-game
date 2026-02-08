from http.server import BaseHTTPRequestHandler
import json
import numpy as np

# tytan_lite: TYTANと同じAPIを提供する軽量版（pandas/networkx不要）
from .tytan_lite import symbols_list, Compile, sampler, Auto_array


class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(content_length))
            houses = body.get('houses', [])

            N = len(houses)
            if N < 3:
                self._send_json(400, {'error': '3軒以上の家が必要です'})
                return

            # 1. 距離行列の計算
            dist_matrix = np.zeros((N, N))
            for i in range(N):
                for j in range(N):
                    if i != j:
                        dx = houses[i]['x'] - houses[j]['x']
                        dy = houses[i]['y'] - houses[j]['y']
                        dist_matrix[i][j] = np.sqrt(dx * dx + dy * dy)

            # 正規化
            max_dist = np.max(dist_matrix)
            if max_dist > 0:
                norm_dist = dist_matrix / max_dist
            else:
                norm_dist = dist_matrix

            # 2. 量子ビットの用意 (TYTAN互換API)
            q = symbols_list([N, N], 'q{}_{}')

            # 3. QUBO定式化
            H = 0

            # 制約A: 各ステップで訪れる都市は1つだけ
            for t in range(N):
                row_sum = sum(q[t][i] for i in range(N))
                H += (row_sum - 1) ** 2

            # 制約B: 各都市は必ず1回だけ訪れる
            for i in range(N):
                col_sum = sum(q[t][i] for t in range(N))
                H += (col_sum - 1) ** 2

            # コスト項
            Hcost = 0
            for t in range(N):
                next_t = (t + 1) % N
                for i in range(N):
                    for j in range(N):
                        if i != j:
                            d = norm_dist[i][j]
                            Hcost += d * q[t][i] * q[next_t][j]

            H_total = H + 0.5 * Hcost

            # 4. コンパイル (TYTAN互換API)
            qubo, offset = Compile(H_total).get_qubo()

            # 5. サンプリング (TYTAN互換 SASampler)
            solver = sampler.SASampler()
            result = solver.run(qubo, shots=100)

            # 6. 結果の解析 (TYTAN互換 Auto_array)
            best_result = result[0]
            arr, subs = Auto_array(best_result[0]).get_ndarray('q{}_{}')

            ai_path = []
            for t in range(N):
                for i in range(N):
                    if arr[t][i] == 1:
                        ai_path.append(i)
                        break

            if len(ai_path) != N or len(set(ai_path)) != N:
                ai_path = list(range(N))

            self._send_json(200, {'path': ai_path})

        except Exception as e:
            self._send_json(500, {'error': str(e)})

    def _send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def _send_json(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

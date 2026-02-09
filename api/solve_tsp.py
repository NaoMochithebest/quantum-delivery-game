from http.server import BaseHTTPRequestHandler
import json
import numpy as np
from .tytan_lite import symbols_list, Compile, sampler, Auto_array


class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def do_POST(self):
        try:
            body = json.loads(self.rfile.read(int(self.headers.get('Content-Length', 0))))
            houses = body.get('houses', [])
            shots = body.get('shots', 100)
            T_num = body.get('T_num', None)

            N = len(houses)
            if N < 3:
                return self._json(400, {'error': '3軒以上必要'})

            # 1. 距離行列
            dist = np.zeros((N, N))
            for i in range(N):
                for j in range(N):
                    if i != j:
                        dx = houses[i]['x'] - houses[j]['x']
                        dy = houses[i]['y'] - houses[j]['y']
                        dist[i][j] = np.sqrt(dx * dx + dy * dy)

            # 正規化
            mx = np.max(dist)
            nd = dist / mx if mx > 0 else dist

            # 2. 量子ビット: q[t][i] = ステップtで都市iを訪問
            q = symbols_list([N, N], 'q{}_{}')

            # 3. 制約項
            H = 0
            # 制約A: 各ステップで訪れる都市は1つだけ
            for t in range(N):
                H += (sum(q[t][i] for i in range(N)) - 1) ** 2
            # 制約B: 各都市は必ず1回だけ訪れる
            for i in range(N):
                H += (sum(q[t][i] for t in range(N)) - 1) ** 2

            # 4. コスト項: 巡回問題（最後の街→最初の街に帰る）
            #    t=0→1, 1→2, ..., N-2→N-1, N-1→0 の N本の辺
            Hcost = 0
            for t in range(N):
                next_t = (t + 1) % N    # ← 最後のステップは最初に戻る
                for i in range(N):
                    for j in range(N):
                        if i != j:
                            Hcost += nd[i][j] * q[t][i] * q[next_t][j]

            # 重み: 制約の重み1.0に対し、コスト項は0.5
            # 正規化済みなのでこのバランスで制約を優先しつつコストも反映
            qubo, offset = Compile(H + 0.5 * Hcost).get_qubo()

            # 5. サンプリング
            solver = sampler.SASampler()
            result = solver.run(qubo, shots=shots, T_num=T_num)

            # 6. 結果デコード
            arr, _ = Auto_array(result[0][0]).get_ndarray('q{}_{}')
            path = []
            for t in range(N):
                for i in range(N):
                    if arr[t][i] == 1:
                        path.append(i)
                        break
            if len(path) != N or len(set(path)) != N:
                path = list(range(N))

            self._json(200, {'path': path})
        except Exception as e:
            self._json(500, {'error': str(e)})

    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def _json(self, code, data):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self._cors()
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

# 量子あめ配達員 (Quantum Candy Deliverer)

TSP × 量子アニーリング対戦ゲーム — Vercel + tytan_lite

## アーキテクチャ

```
public/              → Vercel Static (CDN配信)
  index.html, style.css, script.js

api/                 → Vercel Python Serverless Function
  solve_tsp.py       → TSP求解エンドポイント
  tytan_lite/        → TYTAN SDK互換の軽量モジュール
    __init__.py
    symbols.py       → symbols_list (sympy)
    compile.py       → Compile (sympy → QUBO)
    sampler.py       → SASampler (numpy SA)
    auto_array.py    → Auto_array (結果デコード)

requirements.txt     → numpy + sympy のみ (< 250MB)
vercel.json          → CORS設定
```

## 250MB制限の解決

TYTAN SDKのフルインストール（numpy + sympy + pandas + networkx + tytan本体）は250MBを超過します。
本プロジェクトでは、TYTANの **API互換** な軽量版 `tytan_lite` を同梱し、
依存を `numpy` + `sympy` の2つだけに削減しました。

`solve_tsp.py` のコードは元のTYTAN版とほぼ同一です:
- `symbols_list([N, N], 'q{}_{}')` → 同じ
- `Compile(H).get_qubo()` → 同じ
- `sampler.SASampler().run(qubo, shots=100)` → 同じ
- `Auto_array(result[0][0]).get_ndarray('q{}_{}')` → 同じ

## デプロイ

```bash
git add . && git commit -m "tytan_lite版" && git push
```

Vercelが自動デプロイします。

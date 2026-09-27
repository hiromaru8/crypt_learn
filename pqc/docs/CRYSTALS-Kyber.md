
 **「CRYSTALS-Kyberを“実装できる理解”まで持っていく」**ことを目的に、**初学者向けの学習ルート＋最小Python実装 → C実装への対応関係**という形で説明します。

結論から言うと：

> 🔑 **概念理解とアルゴリズム追跡は Python が圧倒的にわかりやすい**
> 🔧 **最終的な実装・実務は C（NIST参照実装）**

です。
あなたの技術レベル（C/C++・暗号・実装志向）を考えると、この順番が一番早く「腑に落ちる」構成になります。

---

# 1. CRYSTALS-Kyber とは何をしている暗号か

Kyber は **公開鍵暗号ではなく KEM** です。

```
目的：安全に「共有秘密鍵」を作る
```

流れは必ずこの3つ：

1. **KeyGen**

   * 公開鍵 pk
   * 秘密鍵 sk
2. **Encapsulate(pk)**

   * 共有鍵 K
   * 暗号文 c
3. **Decapsulate(sk, c)**

   * 同じ共有鍵 K を復元

RSAの「暗号化/復号」ではなく
👉 **「鍵を包んで渡す」**のがポイントです。

---

# 2. Kyberの中身を一言で言うと

> **「多項式（ベクトル） × 行列演算 ＋ ノイズ」**

これだけです。

ただし：

* 係数は **整数 mod q**
* 高速化のため **NTT（数論変換）**
* 秘密を隠すため **誤差（ノイズ）**

が入ります。

---

# 3. まず理解すべき最小数学セット

Kyber理解に必要なのは、これだけ👇

## (1) 多項式環

Kyberはこの世界で計算します：

```
R_q = Z_q[x] / (x^256 + 1)
```

意味：

* 256次までの多項式
* 係数は mod q（q=3329）
* x^256 = -1 として計算

Pythonでは「長さ256の配列」でOKです。

---

## (2) 行列 × ベクトル

公開鍵は本質的に：

```
A * s + e
```

* A：公開行列（乱数）
* s：秘密ベクトル
* e：ノイズ

これ、**線形代数そのもの**です。

---

# 4. 超簡略版 Kyber（Python）

まずは **暗号強度を完全に無視した「学習用Kyber」** を書きます。

## (A) 基本定数

```python
import random

N = 8        # 本物は256（まずは小さく）
Q = 3329
```

---

## (B) 多項式演算

```python
def poly_add(a, b):
    return [(x + y) % Q for x, y in zip(a, b)]

def poly_mul(a, b):
    res = [0]*N
    for i in range(N):
        for j in range(N):
            k = (i + j) % N
            sign = -1 if (i + j) >= N else 1
            res[k] = (res[k] + sign * a[i] * b[j]) % Q
    return res
```

👉 これが
`Z_q[x] / (x^N + 1)` の乗算です。

---

## (C) KeyGen（超簡略）

```python
def keygen():
    A = [[random.randint(0, Q-1) for _ in range(N)] for _ in range(N)]
    s = [random.randint(0, 1) for _ in range(N)]
    e = [random.randint(0, 1) for _ in range(N)]

    b = poly_add(
        [sum(A[i][j] * s[j] for j in range(N)) % Q for i in range(N)],
        e
    )
    return (A, b), s
```

* `(A, b)` が公開鍵
* `s` が秘密鍵

---

## (D) Encapsulate / Decapsulate（概念版）

```python
def encapsulate(pk):
    A, b = pk
    r = [random.randint(0, 1) for _ in range(N)]
    e1 = [random.randint(0, 1) for _ in range(N)]
    e2 = random.randint(0, 1)

    u = poly_add(
        [sum(A[i][j] * r[j] for j in range(N)) % Q for i in range(N)],
        e1
    )

    v = (sum(b[i] * r[i] for i in range(N)) + e2) % Q

    K = v % 2   # 本物は KDF
    return (u, v), K


def decapsulate(sk, ct):
    u, v = ct
    s = sk
    v2 = (v - sum(u[i] * s[i] for i in range(N))) % Q
    return v2 % 2
```

---

## (E) 動作確認

```python
pk, sk = keygen()
ct, K1 = encapsulate(pk)
K2 = decapsulate(sk, ct)

print(K1, K2)
```

👉 一致すれば成功。

---

# 5. このPythonコードと「本物Kyber」の対応表

| 本物Kyber  | このPython     |
| -------- | ------------ |
| 多項式次数256 | N=8（簡略）      |
| NTT      | 省略           |
| CBDノイズ   | randint(0,1) |
| SHAKE    | random       |
| KDF      | `% 2`        |

**構造は完全に同じ**です。

---

# 6. C実装に進むときの道筋（重要）

次はこれをやります👇

## ステップ1

👉 **NIST公式C実装を読む**

* `poly.c`
* `polyvec.c`
* `indcpa.c`
* `kem.c`

構成は：

```
KeyGen      → indcpa_keypair
Encapsulate → crypto_kem_enc
Decapsulate → crypto_kem_dec
```

---

## ステップ2

👉 Pythonで理解した処理をCコードで「対応づけ」

例：

```c
poly_mul()
↓
poly_basemul_montgomery()
```

---

## ステップ3

👉 自作ミニKyberをCで書く（NTTなし）

あなたのレベルなら、
**「NTTなし・N=16のKyber」**をCで書くと理解が完成します。

---

# 7. おすすめ次アクション

次に進むなら、どれがいいですか？

1. **Python版をもう少し本物に近づける（CBDノイズ・KDF）**
2. **NIST公式Cコードを一緒に読み解く**
3. **ミニKyberをCで一から実装**
4. **NTTだけを独立して解説＆実装**

👉 番号で指定してください。

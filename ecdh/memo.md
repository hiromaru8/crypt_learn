今のNISTベクタでは、

```text
dIUT      ← 自装置秘密鍵
QCAVS     ← 相手公開鍵
ZIUT      ← 期待共有秘密
```

しか与えられていません。

つまり、

```python
shared = dIUT × QCAVS
```

の検証だけができます。

---

## 相手側(CAVS)の共有秘密は計算できるか

ECDHでは本来、

自装置(IUT)

[
Q_{IUT}=d_{IUT}G
]

[
Z=d_{IUT}Q_{CAVS}
]

相手(CAVS)

[
Q_{CAVS}=d_{CAVS}G
]

[
Z=d_{CAVS}Q_{IUT}
]

です。

---

## しかし dCAVS がない

NISTベクタには

```text
QCAVSx
QCAVSy
```

しかありません。

つまり

```text
Q_CAVS = d_CAVS × G
```

の

```text
d_CAVS
```

が非公開です。

ECDLP（楕円曲線離散対数問題）が安全性の根拠なので、

```python
dCAVS = ?
```

を求めることは実質不可能です。

---

## だから相手側計算はできない

相手側は本来

```python
shared = scalar_mult(
    dCAVS,
    QIUT,
    a,
    p
)
```

を実行します。

しかし

```python
dCAVS
```

が無いので再現できません。

---

## NISTベクタで検証できること

### 公開鍵生成

NISTは

```text
dIUT
QIUTx
QIUTy
```

も提供しています。

したがって

```python
QIUT = scalar_mult(
    dIUT,
    G,
    a,
    p
)

assert QIUT[0] == QIUTx
assert QIUT[1] == QIUTy
```

ができます。

---

### ECDH

```python
shared = scalar_mult(
    dIUT,
    QCAVS,
    a,
    p
)

assert shared[0] == ZIUT
```

ができます。

---

## 両側を確認したいなら

テスト用に自分で秘密鍵を作ります。

例えば

```python
alice_private = 12345
bob_private = 67890
```

---

公開鍵生成

```python
alice_public = scalar_mult(
    alice_private,
    G,
    a,
    p
)

bob_public = scalar_mult(
    bob_private,
    G,
    a,
    p
)
```

---

Alice

```python
alice_secret = scalar_mult(
    alice_private,
    bob_public,
    a,
    p
)
```

---

Bob

```python
bob_secret = scalar_mult(
    bob_private,
    alice_public,
    a,
    p
)
```

---

確認

```python
assert alice_secret == bob_secret
```

---

関係式は

[
alice_secret
============

# d_A(d_BG)

d_Ad_BG
]

[
bob_secret
==========

# d_B(d_AG)

d_Bd_AG
]

なので同じになります。

---

### NISTベクタの目的

NISTの ECCCDH Primitive テストは

```text
相手秘密鍵が正しいか
```

を確認するためのものではなく、

```text
与えられた公開鍵に対して
正しい共有秘密を計算できるか
```

を確認するためのものです。

そのため

```text
dIUT      : 公開
QIUT      : 公開
QCAVS     : 公開
ZIUT      : 公開
dCAVS     : 非公開
```

という構成になっています。これであなたの ECDH 実装が正しいか十分に検証できます。

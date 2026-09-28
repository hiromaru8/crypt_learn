# 格子と基底

## グラム-シュミット直交化（関数`GS0`）

階層`n`の格子の基底 ${b_0, b_1, \ldots, b_{n-1}}$ に対する
グラム-シュミットの直交化ベクトル 

```math
b_0^* , b_1^* , \ldots , b_{n-1}^*
```

 は、
まず 

```math
b_0^* = b_0
```

と定め、

```math
i \geq 1 
```

に対しては
次のように逐次的に定められる。

```math
b_i^*=
b_i-
\sum_{j=0}^{i-1}
\mu_{ij} b_j^*
```

```math
\mu_{ij}=\frac{\langle b_i, b_j^* \rangle}
{\|b_j^*\|^2}
```

```math
(0 \leq j < i \leq n-1)
```

このとき ${\langle b_i^*,b_j^*\rangle}=0 (i \neq j)$ が成り立つ。




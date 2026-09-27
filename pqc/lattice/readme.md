\usepackage { mathtools }

# 格子と基底

## グラム-シュミット直交化（関数`GS0`）と直交射影

階層`n`の格子の基底
\(
{b_1, b_2, \ldots, b_n}
|)
に対するグラム-シュミットの直交化ベクトル
$$
b_1^*, b_2^*, \ldots, b_n^*
$$
は、まず
$$
b_1^* = b_1
$$
と定め、
$$
i \geq 2
$$
に対しては次のように逐次的に定められる。
$$
b_i^*=
b_i-
\sum_{j=1}^{i-1}
\mu_{ij} b_j^*
$$

$$
\mu_{ij}=\frac{\langle b_i, b_j^* \rangle}
{\|b_j^*\|^2}
$$
$$
(1 \leq j < i \leq n)
$$
このとき
$$
{\langle b_i^*,b_j^*\rangle}=0 (i \neq j)
$$
が成り立つ。

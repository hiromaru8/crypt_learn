# 格子と基底

## グラム-シュミット直交化（関数`GS0`）と直交射影

階層`n`の格子の基底
$$ {b_1, b_2, \ldots, b_n} $$
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




* As we learned previously, the equation $Ax=b$ does not have a solution if b does not lie in column space $C(A)$. In this case, one can instead ask for the least squares (LS) solution: the choice of x that minimizes
```math
\|Ax-b\|^2 = \sum_i [(Ax)_i - b_i]^2
```
* This means $v=Ax$ should be precisely the projection of $x$ onto $C(A)$, so from what we previously learned, we see that $v = A(A^t A)^{-1}A^t b$, and consequently $x=(A^t A)^{-1}A^t b$.
* Application: given a data set $(a_i,b_i)$ for $1\le i \le 1000$, we covered how to find:
  * The straight line with no intercept that achieves the least squares fit: $b=xa$ where $x$ is the slope;
  * The straight line with intercept that achieves the least squares fit: $b = x_0 + x_1 a$ where $x_0$ is the intercept and $x_1$ is the slope;
  * The cubic function that achieves the least squares fit: $b = x_0 + x_1 a + x_2 a^2 + x_3 a^3$.
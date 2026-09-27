


def GS0(B, n):

    GS = Matrix(QQ,n)
    mu = Matrix(QQ,n)
    
    for i in range(n):
        GS[i] = B[i]
        mu[i,i] = 1
        for j in range(i):
            mu[i,j] = B[i].inner_product(GS[j]) / GS[j].norm()^2
            GS[i]   -= mu[i,j]*GS[j]
            
    return GS, mu
    
    
def LLL(B, n, delta):
    
    GS, mu = GS0(B, n)
    BB = vector(QQ,n)
    k = 1
    
    for i in range(n):
        BB[i] = GS[i].norm()^2
    
    while k <= n-1:
        for j in range(k)[::-1]:
            if abs(mu[k,j]) > 1/2:
                q=round(mu[k,j])
                B[k] -= q*B[j]
                
                for l in range(j+1):
                    mu[k,l] -= q*mu[j,l]
        
        if BB[k] >= (delta - mu[k,k-1]^2)*BB[k-1]:
            k += 1
        else:
            v = B[k-1]
            B[k-1] = B[k]
            B[k] = v
            GS, mu = GS0(B, n)
            for i in range(n):
                BB[i] = GS[i].norm()^2
            k = max(k-1, 1)
            
n=20
bound = 2^n
B = Matrix(ZZ,n)
B[0,0] = bound
for i in range(1,n):
    B[i,i] = 1
    B[i,0] = randint(0,bound)

print(B)
LLL(B, n, 0.99)
print(B)
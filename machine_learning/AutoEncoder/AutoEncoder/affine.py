def affine(x, W, b):
    #　W * x +b -> output
    y = inner(x, W)
    y = plus (y, b)
    return y

def inner(y,x):
    # x・y -> output
    n = len(x)
    m = len(y)
    l = len(y[0])
    if len(x[0]) != m:
        print("Error: inner size")
        exit
    else:
        #xのサイズが n*m になっていると想定
        #yのサイズは　m*l
        z = [[0 for _ in range(l)] for _ in range(n)]
        #アクセス順を意識して高速化
        for i in range(n):
            for j in range(m):
                for k in range(l):
                    z[i][k] += x[i][j]* y[j][k]
    return z

def plus(x,y):
    rowx = len(x)
    rowy = len(y)
    colx = len(x[0])
    coly = len(y[0])
    if rowx != rowy:
        print("Error: not match matrix row")
    elif colx != coly:
        print("Error: not match matrix column")
    else:
        for i in range(rowx):
            for j in range(colx):
                x[i][j] += y[i][j]
    
    return x

if __name__ == "__main__":
    import numpy as np
    a = [[(i+1)*(j+1) for i in range(5)] for j in range(3)]
    W = [[i*2 for i in range(3)] for j in range(4) ]
    b = [[3-i for i in range(5)] for j in range(4)]
    print(a,W)
    print(b)
    y = affine(a,W,b)
    nx = np.array(a)
    nW = np.array(W)
    nb = np.array(b)
    ny = np.dot(nW, nx) + b
    print(ny == y)
def outer(x,y):
    #外積にはouterとcross productの二種類ある
    #cross productをクロス積と呼ぶことも
    # n list * m list -> n,m list
    n=len(x)
    m=len(y)
    out=[[0 for i in range(m)] for i in range(n)]
    for i in range(n):
        for j in range(m):
            out[i][j]+=x[i]*y[j]
    return out

if __name__=="__main__":
    x=[1,2,3]
    y=[1,2,3,4,5]
    out=outer(x,y)
    print(out)

import numpy as np

class Aggregate(object): #継承をしたいのでobject追加
    def __init__(self, n, W, d=8):
        #特徴ベクトル、重み
        self.x = np.r_[np.ones((1,n)),np.zeros((d-1,n))]
        self.W = W
    def Relu(self, x):
        y = np.maximum(0,x)
        return y
    def aggregate(self, W, adjacency_matrix, aggregate_step=2):
        x=self.x #xが初期値に戻るようにする
        for i in range(aggregate_step):
            a    = np.dot(x, adjacency_matrix)
            tmp  = np.dot(W,a)
            x = self.Relu(tmp) #xの更新
        h_output = np.sum(x,axis=1)
        return h_output

class GNN(Aggregate):
    def __init__(self,vertex,W,a,b,y=0):
        super().__init__(vertex,W)
        #パラメータa,b 正解ラベル
        self.a,self.b,self.y= a,b,y
        self.omega=[0, 0, 0]
    def sigmoid(self, x, threshold= 34.538776394910684):
        if x>=threshold:
            y=1.0-1e-15
        elif x<=-1*threshold:
            y=1e-15
        else:
            y=1/(1+np.exp(-x))
        return y
    def loss_function(self,s,threshold=10):
        if s>threshold:
            loss = self.y*np.log(1+np.exp(-s))+(1-self.y)*s
        else:
            loss = self.y*np.log(1+np.exp(-s))+(1-self.y)*np.log(1+np.exp(s))
        return loss
    def forward(self,matrix,W,a,b):
        h         = self.aggregate(W, matrix)
        s         = np.dot(a, h)+b
        p         = self.sigmoid(s)
        predict_y = np.where(p<1/2, 0, 1)
        L         = self.loss_function(s)
        return predict_y,L
    def gradient(self,matrix,epsilon=0.001):
        gradient_W=np.zeros_like(self.W)
        for i in range(np.shape(self.W)[0]):
            for j in range(np.shape(self.W)[1]):
                tmp       = self.W.copy()
                tmp[i][j] += 1*epsilon
                _, deltaL = self.forward(matrix, tmp   , self.a, self.b)
                _, L      = self.forward(matrix, self.W, self.a, self.b)
                gradient_W[i][j] = (deltaL-L)/epsilon
        #print(gradient_W)
        gradient_a=np.zeros_like(self.a)
        for i in range(np.shape(self.a)[0]):
            for j in range(np.shape(self.a)[1]):
                tmp=np.zeros_like(self.a)
                tmp[i][j]=1
                _, deltaL = self.forward(matrix, self.W, self.a+epsilon*tmp, self.b)
                _, L      = self.forward(matrix, self.W, self.a, self.b)
                gradient_a[i][j]=(deltaL-L)/epsilon
        _, deltaL = self.forward(matrix, self.W, self.a, self.b+epsilon)
        _, L      = self.forward(matrix, self.W, self.a, self.b)
        gradient_b = (deltaL-L)/epsilon
        return gradient_W,gradient_a,gradient_b
    def update(self, dW, dA, dB, updata_way="SGD", alpha=1e-4, eta=0.9):
        if updata_way=="SGD":
            self.W-= alpha* dW
            self.a-= alpha* dA
            self.b-= alpha* dB
        elif updata_way=="M-SGD":
            self.W-=alpha* dW- eta* self.omega[0]
            self.a-=alpha* dA- eta* self.omega[1]
            self.b-=alpha* dB- eta* self.omega[2]
            self.omega[0]=-alpha* dW+ eta*self.omega[0]
            self.omega[1]=-alpha* dA+ eta*self.omega[1]
            self.omega[2]=-alpha* dB+ eta*self.omega[2]
        else:
            print("No such a update way")
        return self.W, self.a, self.b
if __name__=="__main__":
    np.random.seed(21)
    n=10
    d=8
    #隣接行列の生成
    r=np.zeros((n,n))
    for i in range(n):
        for j in range(i+1,n):
            possibly=np.random.rand(1)
            if possibly>0.5:
                r[i][j]=1
                r[j][i]=1
    #parameterの生成
    W=np.random.normal(0,0.4,(d,d))
    a=np.random.normal(0,0.4,(1,d))
    b=0
    y=1
    for trial in range(1001):
        gnn = GNN(n,W,a,b,y)
        predict, L = gnn.forward(r,W,a,b)
        dw,da,db = gnn.gradient(r)
        W, a, b = gnn.update(dw, da, db)
        if trial%200==0:
            print(L)
            print(dw,da,db)
            #print(W, a, b)

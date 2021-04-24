import numpy as np
from kadai1 import Aggregate

def sigmoid(x):
    y=1/(1+np.exp(-x))
    return y

def loss_function(s,y,threshold=10):
    if s>threshold:
        loss=y*np.log(1+np.exp(-s))+(1-y)*s
    else:
        loss=y*np.log(1+np.exp(-s))+(1-y)*np.log(1+np.exp(s))
    return loss


class Predict:
    def __init__(self,A,b):
        self.a=A
        self.b=b
    def predict(self,h):
        s=np.dot(self.a,h)+self.b
        p=sigmoid(s)
        predict_y=np.where(p<1/2,0,1)
        self.p=p
        return predict_y,s
    def loss(self,s,y):
        L=loss_function(s,y)
        return L

class GNN:
    def __init__(self,r,t=2):
        #x: 初期ベクトル
        #t: 集約の試行回数
        self.R=r
        self.t=t
    def forward(self,W,a,b,x,y):
        #R: 隣接行列
        #W,a,b: パラメータ
        #y: ラベル
        self.x=x
        self.y=y
        for i in range(self.t):
            shokika=Aggregate(self.x)
            tmp1=shokika.aggregate1(self.R)
            #print("tmp: "+str(tmp1))
            new_x=shokika.aggregate2(tmp1,W)
            self.x=new_x
        h=shokika.output()
        param_shokika=Predict(a,b)
        y_hat,s=param_shokika.predict(h)
        L=param_shokika.loss(s,y)
        return L
    def yosokuti(self,W,a,b,x):
        self.x=x
        for i in range(self.t):
            shokika=Aggregate(self.x)
            tmp1=shokika.aggregate1(self.R)
            new_x=shokika.aggregate2(tmp1,W)
            self.x=new_x
        h=shokika.output()
        param_shokika=Predict(a,b)
        y_hat,_=param_shokika.predict(h)
        return y_hat
    def gradient(self,W,a,b,epsillon=0.001):
        self.W=W
        self.a=a
        self.b=b
        gradient_W=np.zeros_like(W)
        for i in range(np.shape(W)[0]):
            for j in range(np.shape(W)[1]):
                tmp=np.zeros_like(W)
                tmp[i][j]=1
                dif=(self.forward(W+tmp*epsillon,a,b,x,y)-self.forward(W,a,b,x,y))/epsillon
                gradient_W[i][j]=dif
                #print(dif)
        print(W,gradient_W)
        #aのパラメータ更新
        gradient_a=np.zeros_like(a)
        for i in range(np.shape(a)[0]):
            for j in range(np.shape(a)[1]):
                tmp=np.zeros_like(a)
                tmp[i][j]=1
                dif=(self.forward(W,a+tmp*epsillon,b,self.x,self.y)-self.forward(W,a,b,self.x,self.y))/epsillon
                gradient_a[i][j]=dif
        #bの勾配計算
        gradient_b=(self.forward(W,a,b+epsillon,self.x,self.y)-self.forward(W,a,b,self.x,self.y))/epsillon
        #print(gradient_b)
        '''W-=alpha*gradient_W
        a-=alpha*gradient_a
        b-=alpha*gradient_b'''
        #print(gradient_a,gradient_b,gradient_W)
        return gradient_W,gradient_a,gradient_b
    def update(self,delta_W,delta_a,delta_b,alpha=0.0001):
        W=self.W-alpha*delta_W
        a=self.a-alpha*delta_a
        b=self.b-alpha*delta_b
        return W,a,b
    #def update2(self)



np.random.seed(21)
n=10
d=8
x=np.r_[np.ones((1,n)),np.zeros((d-1,n))]
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
for trial in range(1):
    shoki=GNN(r)
    L=shoki.forward(W,a,b,x,y)
    delta_W,delta_a,delta_b=shoki.gradient(W,a,b)
    W,a,b=shoki.update(delta_W,delta_a,delta_b)
    if trial%200==0:
        print(L)

import numpy as np


#グラフGがinputで与えられる(隣接行列形式)
#Gの頂点数も

def ReLU(x):
    y= np.maximum(0,x)
    return y


class Aggregate: 
    #Dは特徴ベクトルの次元
    #Vは頂点数
    def __init__(self,X):
        self.x= X
    def aggregate1(self,R):
        #a_v=SUM(隣接?x_w;0)
        #(D,V)*(V,V) -> (D,V)
        a= np.dot(self.x,R)
        #self.a=a
        return a
    def aggregate2(self,a,W):
        #(D,D)*(D,V)-> (D,V)-> (D,V)
        tmp= np.dot(W,a)
        new_x= ReLU(tmp)
        self.new_x= new_x
        return new_x
    def output(self):
        #(D,V) -> (D,1)
        h= np.sum(self.new_x,axis=1)
        self.h=h
        return h



#特徴ベクトルのx_vの初期化
#パラメータWの初期化

import os
import numpy as np
from kadai2 import GNN

def read_file(path):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    with open(path) as f:
        n=int(f.readline())
        adjust_matrix=np.zeros((n,n))
        for i in range(n):
            l=list(map(int,f.readline().split()))
            for j in range(n):
                adjust_matrix[i][j]=l[j]
    return n,adjust_matrix

def get_data(batch,idx):
    tmp = os.getcwd()
    path="../datasets/train/"+str(batch[idx])+"_graph.txt"
    n,r=read_file(path)
    path="../datasets/train/"+str(batch[idx])+"_label.txt"
    with open(path) as f:
        y=int(f.readline())
    os.chdir(tmp)
    return n,r,y



#学習データ2000個（学習用: 1600, 検証用: 400）

class Train:
    def __init__(self,W,a,b,minibatch=50):
        self.minibatch=minibatch
        self.W=W
        self.a=a
        self.b=b
    def batch(self, all_data_number=2000, train=1600):
        self.all_data_number=all_data_number
        self.train=train
        l=list(range(all_data_number))
        np.random.shuffle(l)
        return l
    def SGD(self, batch_list, d=8, update_way="SGD"):
        SUM_delta_W=0
        SUM_delta_a=0
        SUM_delta_b=0
        for i in range(self.train):
            n,r,y=get_data(batch_list,i)
            self.x=np.r_[np.ones((1,n)),np.zeros((d-1,n))]
            shoki=GNN(r)
            L=shoki.forward(self.W,self.a,self.b,self.x,y)
            delta_W,delta_a,delta_b=shoki.gradient(self.W,self.a,self.b)
            SUM_delta_W+=delta_W
            SUM_delta_a+=delta_a
            SUM_delta_b+=delta_b
            if i!=0 and i%(self.minibatch-1)==0:
                SUM_delta_W/=self.minibatch
                SUM_delta_a/=self.minibatch
                SUM_delta_b/=self.minibatch
                if update_way=="SGD":
                    self.W,self.a,self.b=shoki.update(SUM_delta_W,SUM_delta_a,SUM_delta_b)
                elif update_way=="M-SGD":
                    self.W,self.a,self.b=shoki.update2(SUM_delta_W,SUM_delta_a,SUM_delta_b)
                else:
                    print("None such a update way")
                SUM_delta_W=0
                SUM_delta_a=0
                SUM_delta_b=0
    def accuracy(self,epoch):
        l=[]
        cnt=0
        for i in range(self.train):
            n,r,y=get_data(i)
            shoki=GNN(r)
            y_hat=shoki.yosokuti(self.W,self.a,self.b,self.x)
            if y_hat==y:
                cnt+=1
        l.append(cnt/self.train)
        cnt=0
        for i in range(self.train,self.all_data_number):
            n,r,y=get_data(i)
            shoki=GNN(r)
            y_hat=shoki.yosokuti(self.W,self.a,self.b,self.x)
            if y_hat==y:
                cnt+=1
        l.append(cnt/(self.all_data_number-self.train))
        return (epoch,":",l)

epoch=100
np.random.seed(42)
d=8
W=np.random.normal(0,0.4,(d,d))
a=np.random.normal(0,0.4,(1,d))
b=0
t=Train(W,a,b)
batch_list=t.batch()
#print(batch_list)
for i in range(epoch):
    t.SGD(batch_list)
    if i==10:
        result=t.accuracy
        print(result)

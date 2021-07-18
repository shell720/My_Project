import numpy as np
import os
from kadai2 import GNN

#入力データを読み込む(ランダムに)
#その各データに対してGNNの学習を行う(値の算出と分類部分、勾配算出部分)
#バッチ数に到達したら、勾配の平均をとる
#あるバッチ数ごとにパラメータの更新を行う
#訓練データと検証データのそれぞれに対して学習結果を表示

class Input_data:
    def __init__(self,idx, dirName="train"):
        self.idx=idx
        self.dir=dirName
    def input_AdjacencyMatrix(self):
        #i番目の隣接行列情報を読み込む
        tmp=os.getcwd()
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        path="../datasets/"+self.dir+"/"+str(self.idx)+"_graph.txt"
        with open(path) as f:
            n                = int(f.readline())
            adjacency_matrix = np.zeros((n,n))
            for i in range(n):
                l=list(map(int,f.readline().split()))
                for j in range(n):
                    adjacency_matrix[i][j]=l[j]
        os.chdir(tmp)
        return n,adjacency_matrix
    def input_label(self):
        tmp=os.getcwd()
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        path="../datasets/"+self.dir+"/"+str(self.idx)+"_label.txt"
        with open(path) as f:
            y=int(f.readline())
        os.chdir(tmp)
        return y

class Batch:
    def __init__(self,all_train_data_kazu,train_ratio):
        self.all_data = all_train_data_kazu
        self.train    = all_train_data_kazu*train_ratio
        self.kenshou  = all_train_data_kazu*(1-train_ratio)
    def sampling(self):
        l   = list(range(self.all_data))
        arr = np.array(l) #型変換
        shuffle_arr=np.random.permutation(arr)
        return shuffle_arr

if __name__=="__main__": #importされただけで動かないように
    """
    for i in range(10):
        input_data=Input_data(i)
        vertex, matrix= input_data.input_AdjacencyMatrix()
        label         = input_data.input_label()
        print("index:"+str(i))
        print(vertex)
        print(matrix)
        print(label)"""
    epoch=101 
    minibatch=1
    d = 8 #特徴ベクトルの次元
    np.random.seed(42)
    W = np.random.normal(0, 0.4, (d,d))
    a = np.random.normal(0, 0.4, (1,d))
    b = 0
    #print(W,a,b)
    for i in range(epoch):
        all_data_number  = 2000
        train_hiritu     = 0.8
        data_split = Batch(all_data_number,train_hiritu)
        l          = data_split.sampling()
        dw, da, db = 0, 0, 0
        mean_L=0
        TP, TN, FP, FN= 0, 0, 0, 0
        for idx in range(1600): #
            data_idx=l[idx]
            input_data=Input_data(data_idx)
            vertex,matrix    = input_data.input_AdjacencyMatrix()
            label_y          = input_data.input_label()
            #print(data_idx,vertex,matrix,label_y)
            gnn = GNN(vertex, W, a, b, label_y)
            predict, L = gnn.forward(matrix, W , a, b)
            grad_w, grad_a, grad_b = gnn.gradient(matrix)
            dw+=grad_w
            da+=grad_a
            db+=grad_b
            mean_L+=L
            #print("data_idx:"+str(data_idx))
            #print(db,grad_b)
            if predict==0 and label_y==0:
                TN+=1
            if predict==1 and label_y==0:
                FP+=1
            if predict==1 and label_y==1:
                TP+=1
            if predict==0 and label_y==1:
                FN+=1
            if idx%minibatch==minibatch-1:
                W, a, b = gnn.update(dw/minibatch, da/minibatch, db/minibatch, updata_way="SGD")
                dw=0
                da=0
                db=0
        if i%10==0:
            accuracy=0 #今回は結局使わない方向で
            TP_k, TN_k, FP_k, FN_k= 0, 0, 0, 0
            for j in range(1600,2000):
                kenshou_idx=l[j]
                input_data_kenshou=Input_data(kenshou_idx)
                vertex_k, matrix_k = input_data_kenshou.input_AdjacencyMatrix()
                label_y_k          = input_data_kenshou.input_label()
                gnn_k = GNN(vertex_k, W, a, b, label_y_k)
                predict_k, L_k = gnn_k.forward(matrix_k, W , a, b)
                #print("data_idx:"+str(data_idx),"label:"+str(label_y),"predict"+str(predict))
                if predict_k==label_y_k:
                    accuracy+=1
                if predict_k==0 and label_y_k==0:
                    TN_k+=1
                if predict_k==1 and label_y_k==0:
                    FP_k+=1
                if predict_k==1 and label_y_k==1:
                    TP_k+=1
                if predict_k==0 and label_y_k==1:
                    FN_k+=1
            print(mean_L/1600)#/(all_data_number*train_hiritu))
            #print(W,a,b)
            #print("precision:"+str(TP/(TP+FP)))
            #print("recall:"+str(TP/(TP+FN)))
            print("TP:",TP,"FP:",FP,"FN:",FN,"TN:",TN)
            #print(TP+FP+FN+TN)
            print((TN+TP)/1600,(TN_k+TP_k)/400)
            print("TP:",TP_k,"FP:",FP_k,"FN:",FN_k,"TN:",TN_k)
import numpy as np
import os
from kadai3 import Input_data, Batch
from kadai2 import GNN

#結果をファイルに書き込む

class Write_output:
    def __init__(self):
        tmp= os.getcwd()
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        path= "../result.txt"
        S= "test\n"
        with open(path, mode='w') as f:
            f.write(S)
    def write(self,result):
        tmp= os.getcwd()
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        path= "../result.txt"
        S= str(result)+"\n"
        with open(path, mode='a') as f:
            f.write(S)

if __name__=="__main__":
    epoch= 101 
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
        for idx in range(1600): 
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
            if idx%minibatch==minibatch-1:
                W, a, b = gnn.update(dw/minibatch, da/minibatch, db/minibatch, updata_way="SGD")
                dw=0
                da=0
                db=0
    #testデータで結果を出力し、ファイルに書き込む
    output= Write_output()
    for idx in range(500): 
        input_data=Input_data(idx, dirName="test")
        vertex,matrix    = input_data.input_AdjacencyMatrix()
        gnn = GNN(vertex, W, a, b)
        predict, _ = gnn.forward(matrix, W , a, b)
        #print(predict)
        output.write(predict[0])
    #output.write(6)

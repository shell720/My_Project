import unittest
import numpy as np
from kadai1 import Aggregate

class TestKadai1(unittest.TestCase):
    def test_aggregate(self):
        np.random.seed(42)
        n=4
        d=3
        r=np.array([[0,1,0,0],[1,0,1,1],[0,1,0,1],[0,1,1,0]])
        W=np.random.randint(1,10,(d,d))
        x=np.r_[np.ones((1,n)),np.zeros((d-1,n))]
        expected=np.array([[7,21,14,14],[5,15,10,10],[7,21,14,14]])
        a=Aggregate(x)
        tmp=a.aggregate1(r)
        actual=a.aggregate2(tmp,W)
        print(actual==expected)
        expected2=np.array([56,40,56])
        actual2=a.output()
        print(actual2==expected2)
        #self.assertEqual(expected, actual)
    def test2_aggregate(self):
        np.random.seed(42)
        n=10
        d=8
        x=np.random.randint(0,2,(d,n))
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
        a=Aggregate(x)
        tmp=a.aggregate1(r)
        print(tmp)
        actual=a.aggregate2(tmp,W)
        #print(actual)



if __name__=="__main__":
    unittest.main()
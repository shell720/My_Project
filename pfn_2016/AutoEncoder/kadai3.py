from outer import outer
from affine import affine, inner

class iter:
    def __init__(self, x, W1, W2, b1, b2):
        self.x = x    #入力次元　n*1
        self.W1 = W1  # (5*n)ベクトル
        self.W2 = W2  # (n*5)ベクトル
        self.b1 = b1  # (5*1)ベクトル
        self.b2 = b2  # (n*1)

    def foward_propagation(self, loss_culc = False):
        #h: 5*1ベクトル
        #y: n*1ベクトル
        h = affine(self.x, self.W1, self.b1)
        y = affine(self.h, self.W2, self.b2)
        self.h = h
        ret = y
        if loss_culc = True:
            loss = 0
            for i in range(len(y)):
                loss += (x[i]-y[i])* (x[i]-y[i])
            loss /=2
            ret = loss

        return ret

    def back_propagation(self, y):
        n = len(self.W2)
        m = len(self.W2[0])
        W2t = [[self.W2[i][j] for i in range(n)] for j in range(m)]
        self.gy  = self.y - self.x
        self.gW2 = outer(self.gy, self.h)
        self.gb2 = self.gy
        self.gh =  inner(self.gy, W2t)
        self.gW1 = outer(self.gh, self.x)
        self.gb1 = self.gh

    def update(self, mu):
        self.W2 -= mu* self.gW2
        self.W1 -= mu* self.gW1
        self.b2 -= mu* self.gb2
        self.b1 -= mu* self.gb1
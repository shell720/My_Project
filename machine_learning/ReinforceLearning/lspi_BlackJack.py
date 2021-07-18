import numpy as np

np.random.seed(1)

sample= []
koudou = []
houshuu = []
#draw=[0 for i in range(13)]
pi = [1 if i<160 else 0 for i in range(9*10*2)] #s = (y-12)*20+(x-1)*2+z
test_sample=[]

def calc_xyz2s(x, y, z):
    return (x-1)*2+(y-12)*20+z

def calc_state_and_action(x, y, z, action):
    return calc_xyz2s(x, y, z)+action*180

def calc_learning_degree():
    cumulative_reward = 0
    cnt = 0
    for j in range(10000):
        state = test_sample[j]
        test_case = BlackJack(state)
        while test_case.y<21:
            test_case.set_action(pi[calc_xyz2s(state[0], state[1], state[2])])
            test_case.action_palyer()
            r = test_case.get_reward()
            if r==1:
                cnt+=1
            cumulative_reward += r
            if test_case.a == 0:
                break
    return cumulative_reward, cnt/10000

class BlackJack():
    def __init__(self, state=None):
        if state == None:
            self.x = np.random.randint(1,10+1)
            self.y = np.random.randint(12,20+1)
            self.z = np.random.randint(0,1+1) #0:無し　1:有り
        else:
            self.x = state[0]
            self.y = state[1]
            self.z = state[2]
    
    def set_action(self, a=None):
        if a == None:
            self.a = np.random.randint(0,1+1) #0:貰わない　1:貰う
        else:
            self.a = a

    def action_palyer(self):
        if self.a==1:
            draw_card = np.random.randint(1,13+1)
            self.y += min(draw_card, 10)
            #draw[min(draw_card, 10)-1] +=1
        else:
            pass
    
    def win_or_lose(self):
        if 22 <= self.y:
            r = -1
        else:
            while self.x<17:
                card = np.random.randint(1,13+1)
                self.x += min(card, 10)
            
            if 22 <= self.x or self.x < self.y:
                r = 1
            elif self.y == self.x:
                r = 0
            elif self.y < self.x:
                r = -1
        return r
    
    def get_reward(self):
        if self.a == 0 or 21<=self.y:
            reward = self.win_or_lose()
        else:
            reward = 0
        return reward



if __name__ == '__main__':

    #モンテカルロシミュレーション
    for i in range(10010):
        bj = BlackJack()
        test_sample.append([bj.x, bj.y, bj.z])
        while True:
            bj.set_action()
            #koudou.append(bj.a)
            sample.append([bj.x, bj.y, bj.z, bj.a])
            #tmp = bj.x
            bj.action_palyer()
            r = bj.get_reward()
            #houshuu.append(r)
            sample[-1].append(r)
            if bj.a==0 or 21<=bj.y:
                sample.append([bj.x, 21, bj.z])
                break
    #学習
    A = np.zeros((360,360))
    b = np.zeros((360,1))
    lamb = 0.000001

    for i in range(len(sample)-1):
        monte = sample[i]
#        print("sample is ", monte)
        if len(monte) == 3:
            continue
        phi_now = np.zeros((360,1))
        phi_next = np.zeros((360,1))
#        print("s,a: ", calc_state_and_action(*monte[0:3], monte[3]), "s: ", calc_xyz2s(*sample[i][0:3]))
        phi_now[calc_state_and_action(*monte[0:3], monte[3])][0] = 1
        if len(sample[i+1]) != 3:
            s = calc_xyz2s(*sample[i+1][0:3])
            phi_next[calc_state_and_action(*sample[i+1][0:3], pi[s])][0] = 1
        A += np.dot(phi_now, (phi_now-phi_next).T)
        b += monte[4]*phi_now
        if i%10000 == 0:
            omega = np.dot(np.linalg.inv(A+lamb*np.identity(360)), b)
            check = False
            while check==False:
                check=True
                for idx in range(180):
                    new_aciton = pi[idx]
                    if omega[idx][0] < omega[180+idx][0]:
                        #print(omega[idx][0], omega[180+idx])
                        new_aciton = 1
                    elif omega[idx+180][0] < omega[idx][0]:
                        #print(omega[idx], omega[180+idx])
                        new_aciton = 0
                
                    if new_aciton != pi[idx]:
                        check = False
                        pi[idx] = new_aciton
            res, shouritu = calc_learning_degree()
            print(pi)
            print(res, shouritu)
            #print(omega)

    print()
    print(len(sample), len(koudou), len(houshuu), len(test_sample))
    print(sample[0:10])
    print(koudou[0:10], houshuu[0:10])
    #print(draw, sum(draw), sum(draw)/13)
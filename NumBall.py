import random

class NumBall:
    def __init__(self, digit, diff):
        self.digit = digit
        self.diff = diff
        self.winner = None
        self.state = 'start'
        
    def setPlayerNum(self, num):
        self.playerNum = num
        
    def getWinner(self):
        return self.winner
        
    def Attack(self, attackNum):
        strike, ball = self.Compare(attackNum, self.computerNum)
        if strike == self.digit:
            self.winner = 'Player'
        return attackNum, strike, ball
        
    def Compare(self, str_a, str_b):
        strike = 0
        ball = 0
        for i in range(len(str_a)):
            if str_a[i] == str_b[i]: strike += 1
            elif str_a[i] in str_b: ball += 1
        return strike, ball

    def isRight(self, num):
        if len(num) != self.digit: return False
        for i in range(self.digit):
            if num[i] in num[i+1:]: return False
        return True
    
    def getState(self):
        return self.state
        
    def setState(self, state):
        self.state = state
            
class Computer(NumBall):
    def __init__(self, digit, diff):
        super().__init__(digit, diff)
        
    def setComputerNum(self):
        self.computerNum = str()
        D = [i for i in range(1, 10)]
        for i in range(self.digit):
            ran = random.randint(0, len(D) - 1)
            self.computerNum += str(D[ran])
            del D[ran]

        self.tracking = str()
        self.comCase = list()
        self.DFS(0)
    
    def getComputerNum(self):
        return self.computerNum
        
    def DFS(self, count):
        if count == self.digit:
            self.comCase.append(self.tracking)
            return
        for i in range(1, 10):
            if str(i) in self.tracking: continue
            self.tracking += str(i)
            self.DFS(count + 1)
            self.tracking = self.tracking[:-1]
    
    def Defend(self):
        ran = random.randint(0, len(self.comCase) - 1)
        attackNum = self.comCase[ran]
        
        strike, ball = self.Compare(attackNum, self.playerNum)
        if strike == self.digit:
            self.winner = 'Computer'
          
          #플레이어의 숫자를 맞추기 위해서 comCase중 가능성이 없는 것들을 모두 제거함   
        D = {0: 2, 1: 1, 2: 0}
        i = 0
    
        while i < len(self.comCase):
            s, b = self.Compare(attackNum, self.comCase[i])
            if not (strike == s and ball == b):
                ran = random.randint(1, 5)
                delete = ran > D[self.diff]
                if delete:
                    del self.comCase[i]
                    i -= 1
            i += 1
            
        return attackNum, strike, ball
    

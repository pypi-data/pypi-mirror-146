class StringInteger:
    def __init__(self, n):
        self.n = n
        self.a = 0
    def Product(self, m):
        self.a = str(eval(str(self.n))*eval(str(m)))
        return self.a
    def Suvtract(self, m):
        self.a = str(eval(str(self.n))-eval(str(m)))
        return self.a
    def Plus(self, m):
        self.a = str(eval(str(self.n))+eval(str(m)))
        return self.a
    def Division(self, m):
        self.a = str(eval(str(self.n))/eval(str(m)))
        return self.a
    

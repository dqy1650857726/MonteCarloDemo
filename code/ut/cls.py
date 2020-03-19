class People:
    def __init__(self,tp,state):
        self.point=tp
        self.state=state
    
    def __str__(self):
        return "(%d,%d)=%d"%(self.point[0],self.point[1],self.state)

    #感染
    def infected():
        self.state=False

class Result:
    def __init__(self,x,y,sorce):
        self.x = x
        self.y=y
        self.sorce=sorce

    def __str__(self):
        return "(%d,%d)=%d"%(self.x,self.y,self.sorce)

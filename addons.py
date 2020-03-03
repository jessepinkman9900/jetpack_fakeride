# COIN = 'C'
# COINRATE = 100
class Generate:

    def __init__(self):
        pass
    
    def create(self,x,xlim):
        import configs
        import random
        ''' get a random (x,y) in current frame
            render as set of 4,6 like the madolorian '''
        cy = random.randint(5,configs.HEIGHT-3)
        cx = random.randint(x,xlim)
        return (cy,cx)

    def select(self,rate):
        import random as rd
        return (rd.randrange(0,rate,1)%(rate-1)==0)
    
class Coins(Generate):
    def __init__(self):
        super().__init__()
        self.COINCHAR = 'C'
        # self.COIN = '$'
        self.__COINRATE = 100

    def getcoinrate(self):
        return self.__COINRATE
        
class Speedboost(Generate):
    def __init__(self):
        super().__init__()
        self.SPEED='>'
        self.__SPEEDRATE = 150
        self.__framespeed = 4

    def getspeedrate(self):
        return self.__SPEEDRATE
    
    def getframrate(self):
        return self.__framespeed

class Shield(Generate):
    def __init__(self):
        super().__init__()
        self.SHIELD='S'
        self.__SHIELDRATE = 200
    
    def getshieldtrate(self):
        return self.__SHIELDRATE
    
class Beam(Generate):
    def __init__(self):
        ORIENTATIONS = ['v','h','u','d']
        import random
        super().__init__()
        self.__life = random.randint(1,4)
        self.__orientation = random.choice(ORIENTATIONS)
        self.BEAMRATE = 1000
        self.__BEAMLEN = 5
        self.BEAMCHAR='*'
        self.beamlen = random.randint(1,self.__BEAMLEN)
    
    def getlife(self):
        return self.__life

    def getbeamrate(self):
        return self.BEAMRATE   

    def getorientation(self):
        return self.__orientation 
    
    def getbeamlen(self):
        return self.__BEAMLEN

class Magnet(Generate):
    def __init__(self):
        super().__init__()
        self.__MAGRATE = 1000
        self.MAGCHAR = 'M'
        pass
    def getmagrate(self):
        return self.__MAGRATE

class Bossenemy(Generate):

    def __init__(self):
        super().__init__()
        self.__SHOOTRATE = 50
        self.__x=0
        self.__y=0
        self.__timetoatack=0
        self.__lives=10

    def getx(self):
        return self.__x
    def getlives(self):
        return self.__lives
    def gety(self):
        return self.__y

    def getshootrate(self):
        return self.__SHOOTRATE

    def settime(self):
        self.__timetoatack=1

    def timetoattack(self):
        return self.__timetoatack
    
    def shootselect(self):
        rate = self.__SHOOTRATE
        import random as rd
        return (rd.randrange(0,rate,1)%(rate-1)==0)
    
    def lucky(self):
        return self.shootselect()
    
    def setx(self,x):
        self.__x=x

    def sety(self,y):
        self.__y=y

    def loselife(self):
        self.__lives-=1
    
    
        
        
    
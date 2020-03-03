# class Person
# to make to have inheritence
import configs
import signal
import getch
import alarm
class Player:

    def __init__(self):
        import configs
        self.__lives = 5
        self.__y = configs.HEIGHT-2 #bottom
        self.__x = 5 #left
        self.__score = 0
        self.__shield = 0
        self.__inc=1
        self.__time = 0 

    def getx(self):
        return self.__x
    def gety(self):
        return self.__y
    
    def setx(self,a):
        self.__x=a

    def loselife(self,game):
        import time
        self.__lives-=1
        print("\033[2J")
        # print("\033[0;0H")
        print("\t\t\t\t\t<<\033[31m DEAD \033[0m>>\n\t\t\t\t<< PRESS ANY KEY TO START >>")
        
        time.sleep(1)
        if getch._getChUnix()() is not '': #press key to start
            self.__x = game.getx() + 5
            pass
            
        print("\033[2J")
        
    
    def getscore(self):
        return self.__score
    
    def getlives(self):
        return self.__lives

    def valid(self,move,game):
        #if we can move u,d,l or r;
        f=0
        x = game.getx()
        if x%3==0 and self.__y  <= configs.HEIGHT-2:
            self.__time+=1
        if move=='w' and self.__y>3:
                self.__y-=3
                # if x%3:
                #     self.__inc+=1
                return 1
        if move=='a':
            if self.__x>x:
                self.__x-=2
            else:
                self.loselife(game)
            return 1
        if move=='d':
            if self.__x < x+configs.WIDTH-2:
                self.__x+=2
            elif self.__x==x+configs.WIDTH-2:
                self.__x-=3
            return 1
        # if move=

        if move=='e':
            game.shoot(self.__y,self.__x)
            # return 1

        if self.__y<configs.HEIGHT-2:
            
            # self.__y+=self.__time
            self.__y+=1
            if self.__y >= configs.HEIGHT-1:
                self.__y = configs.HEIGHT-2
                self.__inc=1
                self.__time=1
            
        return f
    

    def coincollected(self):
        self.scoreup(100)
        pass
    def beamkilled(self):
        self.scoreup(400)
    def enemykilled(self):
        self.scoreup(5000) 
        
    def scoreup(self,amount):
        self.__score+=amount
    
    def move(self,game):
        def alarmhandler(signum,frame):
            raise alarm.AlarmException


        def user_input(timeout=0.1):
            '''input method'''
            signal.signal(signal.SIGALRM, alarmhandler )
            signal.setitimer(signal.ITIMER_REAL, timeout)
            try:
                move = getch._getChUnix()()
                signal.alarm(0)
                return move
            except alarm.AlarmException:
                pass
            signal.signal(signal.SIGALRM, signal.SIG_IGN)
            return ''

        move = user_input()
        if move=='q':
            quit()
        if(self.valid(move,game)):
            pass
    
    def shielded(self):
        return self.__shield

    def setshield(self,a):
        self.__shield = a
        



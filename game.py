import numpy as np
import player
import getch
class Game:

    def __init__(self,player,enemy):
        import configs
        self.__h,self.__w=configs.HEIGHT,configs.WIDTH
        self.__x=0
        self.__cnt = 0
        self.__framespeed=15
        self.__timeforshield = 60
        self.__gametimeforboss = 20
        self.empty=' '
        self.fresh()
        # maps
        self.coinmap = []
        self.speedmap = []
        self.shieldmap = []
        self.bulletmap = []
        self.enemybulletmap = []
        self.beammap = []
        self.magmap = []
        self.playery = []
        for _ in range(6):
            self.playery.append(self.__h-2)
        self.invbeammap = np.full((self.geth(0),self.getw()*100),0)
        # flags
        self.__timeforboss=0
        self.__bosstimeanou=0
        self.__status=1
        self.__win = 0
        self.__speedstart = 0
        self.__increasedframe = 0
        self.__shieldstart = 0
        # game print
        self.render(player,enemy)

    def getx(self):
        return self.__x
    def geth(self,a=0):
        return self.__h + a
    def fresh(self):
        ''' empty grid '''
        self.board = np.full((self.geth(0),self.getw()*100),' ')

    def buildskynroof(self):
        ''' ^ roof when no color'''
        for i in range(self.getw()):
            self.board[0][self.getx()+i],self.board[self.geth(-1)][self.getx()+i] = '^ ','^ '

    def shoot(self,y,x):
        ''' add bullets to bulletmap'''
        self.bulletmap.append([y,x])

    def cooedinateofbullet(self,player):
        ''' place bullet on game from map ''' 
        import configs
        for i in range(len(self.bulletmap)):
            self.bulletmap[i][1]+=configs.BULLETVELOCITY
        self.placebullet(player)

    def beamloselife(self,y,x,player):
        ''' in contact with beam in game so lose life '''
        coord = self.invbeammap[y][x]
        if coord < len(self.beammap):
            self.beammap[coord][4]-=1
            if(self.beammap[coord][4]==0):
                self.beammap.pop(coord)
                player.beamkilled()
        pass

    def placebullet(self,player):
        ''' place bullet onto game grid '''
        import addons
        beam = addons.Beam()
        bmc = beam.BEAMCHAR
        for i in self.bulletmap:
            f=1
            now = self.board[i[0]][i[1]]
            if now==bmc or self.board[i[0]-1][i[1]]==bmc or self.board[i[0]+1][i[1]]==bmc:
                f=0
                self.beamloselife(i[0],i[1],player)
                if [i[0],i[1]] in self.bulletmap:
                    self.bulletmap.remove([i[0],i[1]])
            if f:
                self.board[i[0]][i[1]]='='
            

    def collectcoin(self,player):
        ''' if player in contact with coins collect and increase core '''
        import addons
        x,y = player.getx(),player.gety()
        coin = addons.Coins()
        if self.board[y-1][x+1]==coin.COINCHAR:
            self.board[y-1][x+1] = self.empty
            self.coinremove(y-1,x+1)
            player.coincollected()
        if self.board[y-1][x]==coin.COINCHAR:
            self.board[y-1][x] = self.empty
            self.coinremove(y-1,x)
            player.coincollected()
        if self.board[y][x]==coin.COINCHAR:
            self.board[y][x] = self.empty
            self.coinremove(y,x)
            player.coincollected()
        if self.board[y][x+1]==coin.COINCHAR:
            self.board[y][x+1] = self.empty
            self.coinremove(y,x+1)
            player.coincollected()    

    def gettimeforboss(self):
        return self.__timeforboss

    def buildplayer(self,player):
        ''' add player onto game grid ''' 
        import addons
        beam = addons.Beam()
        beamchar = beam.BEAMCHAR
        x,y = player.getx(),player.gety()
        if y<self.geth(-2):
            y+=1
        if self.gettimeforboss():
            self.playery.append(y)
        if self.getx()>x:
            player.loselife(self)
        
        incontactwithsnowball = (self.board[y-1][x+1]=='O' 
        or self.board[y-1][x]=='O' or self.board[y][x]=='O' 
        or self.board[y][x+1]=='O')

        incontactwithbeam = (self.board[y-1][x+1]==beamchar 
        or self.board[y-1][x]==beamchar or self.board[y][x]==beamchar 
        or self.board[y][x+1]==beamchar)

        ''' collect coins and other powerups while building player '''
        self.collectcoin(player)
        self.collectspeed(player)
        self.collectshield(player)
        if incontactwithbeam or incontactwithsnowball:
            if player.shielded():
                player.setshield(0)
            else:
                player.loselife(self)
        self.board[y-1][x+1],self.board[y-1][x] = '\\','-'
        self.board[y][x],self.board[y][x+1] = '-','/'
        if player.shielded():
            self.board[y-1][x+1],self.board[y-1][x] = '\\','/'
            self.board[y][x],self.board[y][x+1] = '\\','/'

    def clean(self):
        ''' empty grid before rendering '''
        for i in range(self.getx(),self.getx()+self.getw()):
            for j in range(self.geth(0)):
                self.board[j][i]=self.empty

    def printlives(self,player):
        lives = player.getlives()
        out = "LIFE : "
        while lives>0:
            out+="\033[41m\033[33m<3\033[0m "
            lives-=1
        print(out,end='\t\t')

    def collectshield(self,player):
        import addons
        shield = addons.Shield()
        x,y = player.getx(),player.gety()
        if not player.shielded():
            if self.board[y-1][x+1]==shield.SHIELD:
                self.board[y-1][x+1]=self.empty
                self.shieldremove(y-1,x+1)
                self.shieldup(player)
            if self.board[y-1][x]==shield.SHIELD:
                self.board[y-1][x]=self.empty
                self.shieldremove(y-1,x)
                self.shieldup(player)
            if self.board[y][x]==shield.SHIELD:
                self.board[y][x]=self.empty
                self.shieldremove(y,x)
                self.shieldup(player)
            if self.board[y][x+1]==shield.SHIELD:
                self.board[y][x+1]=self.empty
                self.shieldremove(y,x+1)
                self.shieldup(player)
        pass

    def shieldremove(self,y,x):
        if (y,x) in self.shieldmap:
            self.shieldmap.remove((y,x))
        pass
    def setshieldstart(self,a):
        self.shieldstart=a
    def getshieldstart(self):
        return self.__shieldstart
    def shieldup(self,player):
        player.setshield(1)
        self.setshieldstart(self.getx())
        pass

    def shielddown(self,player):
        if self.getx()-self.getshieldstart()>=10:
            player.setshield(0)
            self.setshieldstart(self.getx())

    def coinremove(self,x,y):
        self.coinmap.remove((x,y))

    def placecoin(self):
        import addons
        coin = addons.Coins()
        for i in self.coinmap:
            y,x = i[0],i[1]
            coinshape = coin.COINCHAR
            self.board[y][x]=coinshape

    def coinvalid(self,x0,y,x):
        import configs
        hm,hma = 4, configs.HEIGHT
        xm,xma = x0,self.getx()+configs.WIDTH
        return (y<hma and y>hm) and (x<xma and x>xm)

    def getw(self):
        return self.__w

    def generatenplacecoin(self,x):
        import random, addons
        coin = addons.Coins()
        if coin.select(coin.getcoinrate()):
            cy,cx = coin.create(self.getw()+self.getx()-2,self.getx()+self.getw())
            if self.coinvalid(x,cy,cx):
                self.coinmap.append((cy,cx))
            if self.coinvalid(x,cy-1,cx+1):
                self.coinmap.append((cy-1,cx+1))
            if self.coinvalid(x,cy-1,cx):
                self.coinmap.append((cy-1,cx))
            if self.coinvalid(x,cy,cx+1):
                self.coinmap.append((cy,cx+1))
        del coin
        self.placecoin()
        pass

    def setincreasedframe(self,a):
        self.__increasedframe = a

    def getincreasedframe(self):
        return self.__increasedframe

    def getframespeed(self):
        return self.__framespeed

    def setframespeed(self,amount):
        self.__framespeed=amount

    def moveframe(self):
        self.__cnt+=1
        if(self.__cnt==self.getframespeed()):
            self.__x+=1
            self.__cnt=0        

    def validx(self,x):
        xm,xma = self.getx(),self.getx()+self.getw()
        return (x<xma and x>xm)

    def validy(self,y):
        import configs
        ym,yma=2,configs.HEIGHT - 3
        return (y>ym and y<yma)

    def placebeam(self):
        import addons
        beam = addons.Beam()
        for i in range(len(self.beammap)):
            bm = self.beammap[i]
            by,bx,orientation,beamlen,life=bm[0],bm[1],bm[2],bm[3],bm[4]
            if life>0:
                for _ in range(beamlen):
                    if not self.validx(bx) and not self.validy(by):
                        break
                    self.board[by%self.geth(0)][bx]=beam.BEAMCHAR
                    self.invbeammap[by][bx]=i
                    self
                    if orientation=='v':
                        by-=1
                    if orientation=='h':
                        bx+=1
                    if orientation=='u':
                        by-=1
                        bx+=1
                    if orientation=='d':
                        bx+=1
                        by+=1
        del beam



    def generatenplacebeam(self,x):
        import random, addons
        beam = addons.Beam()
        if beam.select(beam.getbeamrate()):
            cy,cx = beam.create(self.getx()+self.getw()-2,self.getx()+self.getw())
            orientation = beam.getorientation()
            self.beammap.append([cy,cx,orientation,beam.getbeamlen(),beam.getlife()])
        self.placebeam()
        del beam

    def placemag(self):
        import addons
        magn = addons.Magnet()
        for mag in self.magmap:
            y,x=mag[0],mag[1] 
            self.board[y][x]=magn.MAGCHAR
            self.board[y+1][x-2],self.board[y+1][x+2]=magn.MAGCHAR,magn.MAGCHAR
            self.board[y+2][x-2],self.board[y+2][x+2]=magn.MAGCHAR,magn.MAGCHAR
        del magn
        pass

    def generatenplacemag(self,player):
        import addons
        mag = addons.Magnet()
        my,mx = 2,self.getw()+self.getx()-2
        if mag.select(mag.getmagrate()):
            self.magmap.append((my,mx))
        for i in self.magmap:
            my,mx = i[0],i[1]
            if player.getx() >= mx-7 and player.getx() < mx:
                player.setx(player.getx()+1)
                player.valid('w',self)
            if player.getx() >= mx and player.getx() <= mx+7:
                player.setx(player.getx()-1)
                player.valid('w',self)
        self.placemag()
        pass

    def bulletinvicinity(self,enemy):
        x,y = enemy.getx(),enemy.gety()
        # check for bullet
        for i in range(x-2,x+2):
            if self.board[y][i]=='=':
                return 1
        pass

    def setgamewon(self):
        self.__win=1

    def getwin(self):
        return self.__win

    def setstatus(self,a):
        self.__status=a

    def buildenemy(self,player,enemy):
        x = self.getx() + self.getw() - 5
        enemy.setx(x)
        y=0
        for i in range(4):
            y += self.playery[i]
        y = int(y/4)
        self.playery.pop(0)
        enemy.sety(y)
        if self.getx()%2 and self.bulletinvicinity(enemy):
            y-=2
        incontactwithbullet = (self.board[y-2][x]=='=' or self.board[y-1][x+1]=='=' or self.board[y-1][x-1]=='=' or self.board[y][x+1]=='=' or self.board[y][x-1]=='=')
        #  character
        self.board[y-2][x]='|'
        self.board[y-1][x+1],self.board[y-1][x-1]='{','}'
        self.board[y][x+1],self.board[y][x-1]='{','}'

        if incontactwithbullet:
            enemy.loselife()
        if enemy.getlives()<=0:
            self.setstatus(0)
            player.enemykilled()
            self.setgamewon()

        if enemy.shootselect() and enemy.timetoattack():
            self.enemyshoot(y,x)

    def gamestatus(self):
        return self.__status
        
    def gameover(self,player):
        import time, formaters
        blink = 7
        while blink>0:
            time.sleep(0.14)
            if self.getwin():
                formaters.printwin()
            else:
                formaters.printloss()
            blink-=1
        formaters.printfinalscore(player)

    def enemyshoot(self,y,x):
        self.enemybulletmap.append([y,x])
        pass

    def placeenemybullet(self):
        for i in self.enemybulletmap:
            f=1
            for j  in range(-1,2):
                if self.board[i[0]][i[1]+j]=='=':
                    f=0
                    self.board[i[0]][i[1]]=' '
                    if [i[0],i[1]+j] in self.bulletmap:
                        self.bulletmap.remove([i[0],i[1]+j])
                    if i in self.enemybulletmap:
                        self.enemybulletmap.remove(i)
                    break
            if f:
                self.board[i[0]][i[1]]='O'

    def cooedinateofenemybullet(self):
        enemybulletvelocity = 2
        for i in range(len(self.enemybulletmap)):
            self.enemybulletmap[i][1]-=enemybulletvelocity
        self.placeenemybullet()

    def set__(self,a):
        self.__timeforboss=a

    def getbosstimeanou(self):
        return self.__bosstimeanou

    def setbosstimeanou(self,a):
        self.__bosstimeanou=a

    def bosstime(self):
        self.set__(1)
        import time
        if self.getbosstimeanou() == 0:
            time.sleep(1.5)
            # print("\033[2J")
            print("\033[0;0H")
            print("\n\n\n\n\n\n\t\t\t\t\t\t\033[33m"+"<< \033[32mBOSS TIME!! \033[33m>>\033[0m\n")
            if getch._getChUnix()() is not '': #press key to start
                pass
            self.setbosstimeanou(1)

    def placespeed(self):
        import addons
        speed = addons.Speedboost()
        if not self.getincreasedframe():
            for i in self.speedmap:
                y,x = i[0],i[1]
                speedshape = speed.SPEED
                self.board[y][x]=speedshape
        del speed

    def speedremove(self,y,x):
        if (y,x) in self.speedmap:  
            self.speedmap.remove((y,x))


    def collectspeed(self,player):
        import addons
        speed = addons.Speedboost()
        x,y = player.getx(),player.gety()
        if not self.getincreasedframe():
            if self.board[y-1][x+1]==speed.SPEED:
                self.board[y-1][x+1]=self.empty
                self.speedremove(y-1,x+1)
                self.speedup()
            if self.board[y-1][x]==speed.SPEED:
                self.board[y-1][x]=self.empty
                self.speedremove(y-1,x)
                self.speedup()
            if self.board[y][x]==speed.SPEED:
                self.board[y][x]=self.empty
                self.speedremove(y,x)
                self.speedup()
            if self.board[y][x+1]==speed.SPEED:
                self.board[y][x+1]=self.empty
                self.speedremove(y,x+1)
                self.speedup()
    
    def setspeedstart(self,a):
        self.__speedstart=a
    def speedup(self):
        import addons
        speed = addons.Speedboost()
        if not self.getincreasedframe():
            self.setincreasedframe(1)
            self.setframespeed(speed.getframrate())
            self.setspeedstart(self.getx())
            while len(self.speedmap)>0:
                self.speedmap.pop()

    def getspeedstart(self):
        return self.__speedstart
    def speeddown(self):
        if self.getx()-self.getspeedstart()>=30:
            self.setframespeed(15)
            # self.setincreasedframe(0)
        

    def generatenplacespeed(self,x):
        import addons
        speed = addons.Speedboost()
        if speed.select(speed.getspeedrate()) and not self.getincreasedframe():
            sy,sx = speed.create(self.getw()+self.getx()-2,self.getx()+self.getw())
            self.speedmap.append((sy,sx))
        del speed
        self.placespeed()
        pass

    def generatenplaceshield(self,player):
        import addons
        shield = addons.Shield()
        if shield.select(shield.getshieldtrate()):
            sy,sx = shield.create(self.getw()+self.getx()-2,self.getx()+self.getw())
            self.shieldmap.append((sy,sx))
        del shield
        self.placeshield(player)
    
    def placeshield(self,player):
        import addons 
        if not player.shielded():
            shield = addons.Shield()
            for i in self.shieldmap:
                y,x = i[0],i[1]
                self.board[y][x]=shield.SHIELD
    def gettimeforshield(self):
        return self.__timeforshield
    def getgametimeforboss(self):
        return self.__gametimeforboss
    def render(self,player,enemy): #have to add player postion as an argument
        import addons
        import formaters
        coin = addons.Coins()
        beam = addons.Beam()
        mag = addons.Magnet()
        self.clean()
        self.generatenplacecoin(player.getx())
        self.generatenplacespeed(player.getx())


        if self.getx()-self.getshieldstart() >= self.gettimeforshield() or self.getshieldstart()==0:
            self.generatenplaceshield(player)

        self.generatenplacebeam(player.getx())
        self.generatenplacemag(player)
        self.cooedinateofbullet(player)
        self.buildskynroof()
        if self.getx()>=self.getgametimeforboss():
            enemy.settime()
            self.bosstime()
        if enemy.timetoattack():
            self.buildenemy(player,enemy)
        self.cooedinateofenemybullet()
        self.buildplayer(player)
        
        # 
        bkg ='\033[46m'
        if enemy.timetoattack():
            bkg = '\033[40m'
        # print('\033[2J')
        print("\033[0;0H")
        formaters.printtitle()
        formaters.printscore(player)
        self.printlives(player)
        formaters.printtime(self)
        if enemy.timetoattack():
            formaters.printenemylife(enemy)
        # begin generating string to render
        char = '\n'
        for row in range(1,self.geth(-1)):
            for col in range(self.getx(),self.getx()+self.getw()):
                now = self.board[row][col]
                if now==mag.MAGCHAR:
                    char+=(bkg+"\033[2;31m"+now)
                    continue                    
                if now==beam.BEAMCHAR:
                    char+=(bkg+"\033[31m"+now)
                    continue
                if now==coin.COINCHAR:
                    char+=(bkg+"\033[33m"+now)
                    continue
                if now in ['|','{','}'] and bkg=='\033[40m':
                    char+=(bkg+"\033[35m"+now)
                    continue
                if now in ['\\','/'] and bkg=='\033[40m':
                    char+=(bkg+"\033[32m"+now)
                    continue
                if now in ['>']:
                    char+=(bkg+"\033[34m"+now)
                    continue
                char+=(bkg+now+"\033[0m")
            char+='\n'
        for _ in range(2):
            for row in range(self.geth(-1),self.geth(0)):
                for col in range(self.getx(),self.getx()+self.getw()):
                    char+=("\033[42m" + ' ' + "\033[0m")
                char+='\n'
        print(char)

        # ready for next
        self.moveframe()
        if self.getincreasedframe():
            self.speeddown()
        # 
        return self.gamestatus()


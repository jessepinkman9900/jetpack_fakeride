def printscore(player):
        print("\t\tSCORE: "+ "\033[43m\033[31m"+str(player.getscore())+"\033[0m",end='\t')

def printtitle():
    print("\t\t\t\t\t\t\033[0m\033[45m\033[36mJETPACK FAKE-RIDE \033[0m\n")   

def printtime(game):
        print("TIME : "+str(300 - game.getx()),end='\t')

def printwin():
        import os
        print("\033[2J\033[32m")
        os.system('cat yoda')
        print("\t\t \033[35m//   SUCESSFULLY   \\\\")
        print("\t\t \033[35m\\\\ SAVED BABY YODA //")
        print("\t\t \033[33m"+"  << \033[32mGAME  OVER!! \033[33m>>\033[0m\n")
        print("\t\t \033[33m"+"   << \033[32mYOU  WIN!! \033[33m>>\033[0m\n")

def printloss():
        print("\033[2J\033[32m")
        print("\t\t \033[35m<< DID NOT SAVE BABY YODA >>")
        print("\t\t \033[33m"+"     << \033[32mGAME  OVER!! \033[33m>>\033[0m\n")
        print("\t\t \033[33m"+"      << \033[31mYOU  LOSE! \033[33m>>\033[0m\n")

def printenemylife(enemy):
        print("ENEMY: "+str(enemy.getlives()))

def printfinalscore(player):
        print("\t\t \033[33m"+"<< \033[36mFINAL SCORE: "+str(player.getscore())+" \033[33m>>\033[0m\n")
        
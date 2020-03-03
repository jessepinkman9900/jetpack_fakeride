import colorama as cm  
import player
import game
import addons

if __name__ == "__main__":
    #init colorama
    print("\033[2J")
    cm.init()
    plyr = player.Player()
    enemy = addons.Bossenemy()
    gameBoard = game.Game(plyr,enemy)
    gameplay=1
    while(plyr.getlives() > 0 and gameplay):
        gameplay = gameBoard.render(plyr,enemy)
        plyr.move(gameBoard)
    gameBoard.gameover(plyr)

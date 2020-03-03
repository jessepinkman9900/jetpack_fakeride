# ABOUT
This is an ASCII game, heavily inspired from the popular game Jetpack Joyride, created for the Design and Analysis of Software Systems assignment

## DEPENDENCIES
- numpy==1.18.1
- colorama==0.4.3

## USAGE 
```
chmod +x run
./run
```
```
Q to quit 
```

## CODE ORGANISATION
- main.py
    - has the game loop
    - initialise game and player
    - render screen at constant frame rate as long as game is not over

- getch.py
    - user input class

- alarm.py
    - contains AlarmException class for user input 

- configs.py
    - some game dimenion details
    - dimension of game
    - bullet velocity

- addons.py
    - contains code for coins, magnet, fire beam, shield, and bossenemy
    - Coins
        - getcoinrate - to decide how frequnetly we suspend coins in the air
        - COINCHAR - char that will be printed as money in the game

    - Speedboost
        - getspeedrate - rate at which we suspend speed boost in the air
        - getframerate - the increased speed to implement
    
    - Shield
        - getshieldrate - rate at which we suspend shield coins in the air during the game
    
    - Beam
        - getlife - life remaining of the beam suspended in air
        - getbeamrate - rate at which we suspend beams in the air
        - getorientaton - orientation of beam in air
        - getbeamlen - length of the beam in air
    
    - Magnet
        - getmagrate - rate at which we suspend magents in the air
    
    - Bossenemy
        - getx,getyy - return x,y of enemy respectively
        - getlives - lives of enemy
        - getshootrate - rate at which enemy shoots the player
        - settime - set if time to attack or not
        - timetoattack - return if timetoattack
        - shootselect - if we shoot or not
        - setx,sety - assign value to x,y of enemy respectively
        - loselife - player hit by players bullet 

- player.py 
    - all player functionality 
    - getx, gety - return x,y of player respectively
    - setx, sety - assign x,y values to player respectively
    - loselife - player hit by enemy snowball
    - getscore, getlives - return score,lives remaining of player respectively
    - valid - if move is within board
    - coincollected - increase score because coins collected
    - beamkilled - beam hit by player bullet
    - enemykilled - enemy killed, score added
    - scoreup - score incremented by given argument
    - move - take user input and implement it if it is valid
    - shielded - if the player is shielded
    - setshielded - set the shielded variable value, when shield coin collected


- game.py
    - the state of game and updation of game with time is done here
    - once all oblects placed on the board, we check if any are overlapping using vaious functions and then use the given logic to act or score appropriately
    - render 
        - generatenplacecoin, generatenplacespeed, generatenplaceshield, generatenplacemag, generatenplacebeam
            - generate coin, beam, magnet, speed coin, shieldcoin randomly
            - place the coin, beam, magnet, speed coin, shieldcoin on the board
        - then generate the screen string and print it after formatting and coloring
        - then move the frame ahead
        

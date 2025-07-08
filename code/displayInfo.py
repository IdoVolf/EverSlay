import pygame
from menu import displayText


myFont = pygame.font.Font(None, 24)
def displayPlayerInfo(window,player):
        displayText(window, f"Your health : {player.hp}/{player.maxHp} hp", (350, 300), myFont, (0, 0, 0))
        displayText(window, f"Your weapon : {player.weapon} - {player.getDmg()} dmg", (350, 320), myFont, (0, 0, 0))
        displayText(window, f"Your armor : {player.armor} - {player.getDefense() *100:.0f}% def", (350, 340), myFont, (0, 0, 0))
        displayText(window, f"Monsters killed : {player.monsterKilled}", (350, 360), myFont, (0, 0, 0))

def displayMonsterInfo(window,mns):
    displayText(window, f"health - {mns.hp}", (mns.pos[0] , 120), myFont, (0, 0, 0))
    displayText(window, f"defense - {mns.defense*100:.0f}%", (mns.pos[0], mns.pos[1] - 50), myFont, (0, 0, 0))
    displayText(window, f"attack - {mns.attack}", (mns.pos[0], mns.pos[1] - 70), myFont, (0, 0, 0))
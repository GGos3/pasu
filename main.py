from pygame.transform import scale
from note import Note
from osureader.reader import BeatmapParser
from osureader.beatmap import Beatmap
import pygame as pg
import os, sys

reader = BeatmapParser()
beatmap = Beatmap(reader.parse("D:/osu/Songs/481786 Levaslater - NNRT/Levaslater - NNRT (ZZHBOY) [CS' Another].osu"))
notes = list()
#objects = beatmap.hit_objects
#for i in objects:
#    notes.append(Note().setNote(i))
#print(len(notes))
#GG 
gametime = 0
running = True
notepos = 0
notepng1 = pg.image.load('mania-note1.png')
notepng2 = pg.image.load('mania-note2.png')
notepng3 = pg.image.load('mania-note2.png')
notepng4 = pg.image.load('mania-note1.png')
stageright = pg.image.load('mania-stage-right.png')
stagehint = pg.image.load('mania-stage-hint.png')

noteobject1 = pg.transform.scale(notepng1, (150, 50))
noteobject2 = pg.transform.scale(notepng2, (150, 50))
noteobject3 = pg.transform.scale(notepng3, (150, 50))
noteobject4 = pg.transform.scale(notepng4, (150, 50))
stageright = pg.transform.scale(stageright, (400, 2300))
stagehint = pg.transform.scale(stagehint, (600, 100))
screen = pg.display.set_mode((630, 1000))

pg.display.set_caption("PYMAX")
pg.init()
clock = pg.time.Clock()

# 메인
while running:
    clock.tick(144)
    gametime += clock.get_time() / 1000          #0부터 지금까지의 시간을 저장
    if gametime <= 2:
        notepos = 0 + 1050 * (gametime / 2)      #시간으로 노트 움직이기
        
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            print(event)
        elif event.type == pg.MOUSEBUTTONUP:
            print(event)
    screen.fill((0, 0, 0))
    screen.blit(noteobject1, (0, notepos))
    screen.blit(noteobject2, (150, notepos))
    screen.blit(noteobject3, (300, notepos))
    screen.blit(noteobject4, (450, notepos))
    screen.blit(stageright, (600, 0))
    screen.blit(stagehint, (0, 800))
    pg.display.update()

pg.quit()
sys.exit()
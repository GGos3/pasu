from note import Note
from osureader.reader import BeatmapParser
from osureader.beatmap import Beatmap
import os, pygame, sys

reader = BeatmapParser()
beatmap = Beatmap(reader.parse("D:/osu/Songs/481786 Levaslater - NNRT/Levaslater - NNRT (ZZHBOY) [CS' Another].osu"))
objects = beatmap.hit_objects
notes = list()
for i in objects:
    notes.append(Note().setNote(i))
print(len(notes))
#GG 
notepng1 = pygame.image.load('mania-note1.png')
noteobject = pygame.transform.scale(notepng1, (128, 100))
screen = pygame.display.set_mode((600, 900))
pygame.display.set_caption("Test")
pygame.init()
gametime = 0
clock = pygame.time.Clock()
running = True
notepos = 0
screen.fill((0, 0, 0))

# 메인
while running:
    clock.tick(144)
    gametime += clock.get_time() / 1000            #0부터 지금까지의 시간을 저장
    if gametime <= 2:
        notepos = 0 + 900 * (gametime / 2)      #시간으로 노트 움직이기
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            print(event)
    screen.fill((0, 0, 0))
    screen.blit(noteobject, (300, notepos))
    pygame.display.update()

pygame.quit()
sys.exit()
from osureader.reader import BeatmapParser
from osureader.beatmap import Beatmap
from note import Note
import maploader
import pygame as pg
import os
import sys

directory = 'D:/osu/Songs/324288 xi - ANiMA/'
fileName = 'xi - ANiMA (Kuo Kyoka) [4K Lv.4].osu'

keypositions = maploader.Maploader().load_keyposition(directory+fileName)
notelist = maploader.Maploader().load_notes(directory+fileName, keypositions)

k1list = []  # 생성된 노트 리스트
k2list = []  # 생성된 노트 리스트
k3list = []  # 생성된 노트 리스트
k4list = []  # 생성된 노트 리스트

gametime = 0 # 게임 플레이 시간
running = True
notepng1 = pg.image.load('mania-note1.png') # 노트 리소스
notepng2 = pg.image.load('mania-note2.png') # 노트 리소스
notepng3 = pg.image.load('mania-note2.png') # 노트 리소스
notepng4 = pg.image.load('mania-note1.png') # 노트 리소스
stageright = pg.image.load('mania-stage-right.png') # UI 리소스
stagehint = pg.image.load('mania-stage-hint.png') # 판정선 리소스

noteobject1 = pg.transform.scale(notepng1, (150, 50)) # 노트 오브젝트 생성
noteobject2 = pg.transform.scale(notepng2, (150, 50)) # 노트 오브젝트 생성
noteobject3 = pg.transform.scale(notepng3, (150, 50)) # 노트 오브젝트 생성
noteobject4 = pg.transform.scale(notepng4, (150, 50)) # 노트 오브젝트 생성
stageright = pg.transform.scale(stageright, (400, 2300)) # UI 오브젝트 생성
stagehint = pg.transform.scale(stagehint, (600, 100)) # 판정선 생성
screen = pg.display.set_mode((630, 1000)) # 해상도 설정

pg.display.set_caption("pasu!") # 타이틀
pg.init() # 파이게임 초기화
sound = pg.mixer.music.load(f"{directory}anima.ogg") # 음악 리소스 불러오기
pg.mixer.pre_init(44100, -16, 2, 0) # 파이게임 오디오 초기화
clock = pg.time.Clock()

isPlay = False # 게임 시작 체크

duration = 300 # 노트 이동속도 (*이동에 걸리는 시간)
pressedkey = [False, False, False, False] # 키 입력 체크 (추후 사용)

# 메인 루프
while running:
    clock.tick(1000) # 프레임 제한

    for event in pg.event.get(): # 파이게임 이벤트
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            isPlay = True
            pg.mixer.music.play()
        elif event.type == pg.MOUSEBUTTONUP:
            print(event)

        # 키보드 입력 부분
        elif event.type == pg.KEYDOWN and event.key == pg.K_d:  # 1번 키 (인덱스 0)
            pressedkey[0] = True
            if len(k1list) != 0:  # 16.5 ms 내
                if gametime >= k1list[0].starttime - 16.5: # gametime을 기준으로 (노트 퍼펙트 시간 +- 16.5 ms) 이내에 쳤을 경우 MAX 판정
                    print("MAX")
                    k1list.pop(0)   # 스폰된 노트 제거 (리스트에서 제거)
                elif gametime <= k1list[0].starttime + 16.5:
                    print("MAX")
                    k1list.pop(0)
        elif event.type == pg.KEYDOWN and event.key == pg.K_f:  # 2번 키 (인덱스 1)
            pressedkey[1] = True
            if len(k2list) != 0:  # 16.5 ms 내
                if gametime >= k2list[0].starttime - 16.5:
                    print("MAX")
                    k2list.pop(0)
                elif gametime <= k2list[0].starttime + 16.5:
                    print("MAX")
                    k2list.pop(0)
        elif event.type == pg.KEYDOWN and event.key == pg.K_j:  # 3번 키 (인덱스 2)
            pressedkey[2] = True
            if len(k3list) != 0:  # 16.5 ms 내
                if gametime >= k3list[0].starttime - 16.5:
                    print("MAX")
                    k3list.pop(0)
                elif gametime <= k3list[0].starttime + 16.5:
                    print("MAX")
                    k3list.pop(0)
        elif event.type == pg.KEYDOWN and event.key == pg.K_k:  # 4번 키 (인덱스 3)
            pressedkey[3] = True
            if len(k4list) != 0:  # 16.5 ms 내
                if gametime >= k4list[0].starttime - 16.5:
                    print("MAX")
                    k4list.pop(0)
                elif gametime <= k4list[0].starttime + 16.5:
                    print("MAX")
                    k4list.pop(0)

        # 키를 눌렀다 뗐을때 (추후 롱노트에 사용)
        elif event.type == pg.KEYUP and event.key == pg.K_d:  # 1번 키 (인덱스 0)
            pressedkey[0] = False
        elif event.type == pg.KEYUP and event.key == pg.K_f:  # 2번 키 (인덱스 1)
            pressedkey[1] = False
        elif event.type == pg.KEYUP and event.key == pg.K_j:  # 3번 키 (인덱스 2)
            pressedkey[2] = False
        elif event.type == pg.KEYUP and event.key == pg.K_k:  # 4번 키 (인덱스 3)
            pressedkey[3] = False

    if not isPlay: # 플레이중이 아닐 때 임시처리 (추후에 퍼즈 기능으로 사용) 
        a = 0 # 의미 없음
    else:
        gametime += clock.get_time()  # 0부터 지금까지의 시간을 저장

        # gametime 이 [생성전 대기중인 노트리스트] 0번의 스폰시간을 넘었으면
        if gametime >= notelist[0].starttime - duration:
            if notelist[0].key == 0:
                k1list.append(notelist.pop(0)) # 해당하는 키 리스트에 넣는다
            elif notelist[0].key == 1:
                k2list.append(notelist.pop(0))
            elif notelist[0].key == 2:
                k3list.append(notelist.pop(0))
            elif notelist[0].key == 3:
                k4list.append(notelist.pop(0))

        screen.fill((0, 0, 0)) # 화면 검은색으로 채우기
        screen.blit(stageright, (600, 0)) # UI 불러오기
        screen.blit(stagehint, (0, 800)) # 판정선 불러오기

        for i in k1list:
            # 노트 미스 처리
            if gametime > i.starttime + 127.5:
                k1list.remove(i)
            else:
                # 시간으로 노트 움직이기 (따로 설명)
                pos = 0 + 750 * \
                    ((gametime - i.starttime + duration) / duration)
                obj = pg.transform.scale(notepng1, (150, 50))
                screen.blit(obj, (0, pos))
        for i in k2list:
            if gametime > i.starttime + 127.5:
                k2list.remove(i)
            else:
                # 시간으로 노트 움직이기
                pos = 0 + 750 * \
                    ((gametime - i.starttime + duration) / duration)
                obj = pg.transform.scale(notepng1, (150, 50))
                screen.blit(obj, (150, pos))
        for i in k3list:
            if gametime > i.starttime + 127.5:
                k3list.remove(i)
            else:
                # 시간으로 노트 움직이기
                pos = 0 + 750 * \
                    ((gametime - i.starttime + duration) / duration)
                obj = pg.transform.scale(notepng1, (150, 50))
                screen.blit(obj, (300, pos))
        for i in k4list:
            if gametime > i.starttime + 127.5:
                k4list.remove(i)
            else:
                # 시간으로 노트 움직이기
                pos = 0 + 750 * \
                    ((gametime - i.starttime + duration) / duration)
                obj = pg.transform.scale(notepng1, (150, 50))
                screen.blit(obj, (450, pos))
        pg.display.update()

pg.quit()
sys.exit()

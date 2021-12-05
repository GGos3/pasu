from pygame.constants import KEYDOWN
from osureader.reader import BeatmapParser
from osureader.beatmap import Beatmap
from Note import Note
import Maploader
import pygame as pg
import os
import math
import sys

directory = 'songs/ANiMA/'
fileName = "xi - ANiMA [4K Lv.4].osu"

keypositions = Maploader.Maploader().load_keyposition(directory + fileName)
notelist = Maploader.Maploader().load_notes(directory + fileName, keypositions)

k1list = []  # 생성된 노트 리스트
k2list = []  # 생성된 노트 리스트
k3list = []  # 생성된 노트 리스트
k4list = []  # 생성된 노트 리스트

gametime = 0  # 게임 플레이 시간
exposure_time = 0  # 판정의 노출 시간
running = True
notepng1 = pg.image.load('skin/mania-note1.png')  # 노트 리소스
notepng2 = pg.image.load('skin/mania-note2.png')  # 노트 리소스
notepng3 = pg.image.load('skin/mania-note2.png')  # 노트 리소스
notepng4 = pg.image.load('skin/mania-note1.png')  # 노트 리소스
stageright = pg.image.load('skin/mania-stage-right.png')  # UI 리소스
stageleft = pg.image.load('skin/mania-stage-left.png')  # UI 리소스
stagehint = pg.image.load('skin/mania-stage-hint.png')  # 판정선 리소스
hit0 = pg.image.load('skin/mania-hit0.png')  # hit 0 리소스
hit50 = pg.image.load('skin/mania-hit50.png')  # hit 50 리소스
hit100 = pg.image.load('skin/mania-hit100.png')  # hit 100 리소스
hit200 = pg.image.load('skin/mania-hit200.png')  # hit 200 리소스
hit300 = pg.image.load('skin/mania-hit300.png')  # hit 300 리소스
hit300g = pg.image.load('skin/mania-hit300g-0.png')  # hit 300g 리소스

score0 = pg.image.load('skin/score0.png')  # 숫자 이미지
score1 = pg.image.load('skin/score1.png')  # 숫자 이미지
score2 = pg.image.load('skin/score2.png')  # 숫자 이미지
score3 = pg.image.load('skin/score3.png')  # 숫자 이미지
score4 = pg.image.load('skin/score4.png')  # 숫자 이미지
score5 = pg.image.load('skin/score5.png')  # 숫자 이미지
score6 = pg.image.load('skin/score6.png')  # 숫자 이미지
score7 = pg.image.load('skin/score7.png')  # 숫자 이미지
score8 = pg.image.load('skin/score8.png')  # 숫자 이미지
score9 = pg.image.load('skin/score9.png')  # 숫자 이미지
scores = [score0, score1, score2, score3, score4,
          score5, score6, score7, score8, score9]

noteobject1 = pg.transform.scale(notepng1, (150, 50))  # 노트 오브젝트 생성
noteobject2 = pg.transform.scale(notepng2, (150, 50))  # 노트 오브젝트 생성
noteobject3 = pg.transform.scale(notepng3, (150, 50))  # 노트 오브젝트 생성
noteobject4 = pg.transform.scale(notepng4, (150, 50))  # 노트 오브젝트 생성
stageright = pg.transform.scale(stageright, (8, 1000))  # UI 오브젝트 생성
stageleft = pg.transform.scale(stageleft, (8, 1000))  # UI 오브젝트 생성
stagehint = pg.transform.scale(stagehint, (600, 100))  # 판정선 생성

screen = pg.display.set_mode((608, 1000))  # 해상도 설정
pg.display.set_caption("pasu!")  # 타이틀
pg.init()  # 파이게임 초기화
sound = pg.mixer.music.load(f"{directory}audio.mp3")  # 음악 리소스 불러오기
pg.mixer.pre_init(44100, -16, 2, 0)  # 파이게임 오디오 초기화
pg.mixer.music.set_volume(0.25)
clock = pg.time.Clock()

isPlay = False  # 게임 시작 체크

restarted = False
TotalNotes = len(notelist)
score = 0  # 게임 점수
MaxScore = 1000000  # 최대 점수
last_hit = hit0  # 현재 판정
Bonus = 100
combo = 0
perfectpos = 800  # 판정 선
duration = 400  # 노트 이동속도 (*이동에 걸리는 시간)
pressedkey = [False, False, False, False]  # 키 입력 체크 (추후 사용)


def getHoldNoteSize(base_height, hold_length, duration):
    return base_height * hold_length / duration


def EXscore(MaxScore, TotalNotes, Judgement):
    global Bonus
    Hit = ()
    if Judgement == "MAX":
        Hit = ("MAX", 320, 32, 2, 0)
    elif Judgement == "300":
        Hit = ("300", 300, 32, 1, 0)
    elif Judgement == "200":
        Hit = ("200", 200, 16, 0, 8)
    elif Judgement == "100":
        Hit = ("100", 100, 8, 0, 24)
    elif Judgement == "50":
        Hit = ("50", 50, 4, 0, 44)
    BaseScore = (MaxScore * 0.5 / TotalNotes) * (Hit[1] / 320)
    Bonus = Bonus + Hit[3] - Hit[4]
    if Bonus > 100:
        Bonus = 100
    elif Bonus < 0:
        Bonus = 0
    BonusScore = (MaxScore * 0.5 / TotalNotes) * \
        (Hit[2] * math.sqrt(Bonus) / 320)
    Score = BaseScore + BonusScore
    return Score


def getmiddle_nums(target_digit, all_digit):
    return 608 / 2 - (score0.get_width() / 2) * all_digit + target_digit * score0.get_width()


def getmiddle_img(img):
    return 608 / 2 - (img.get_width() / 2)


# 메인 루프
while running:
    clock.tick(1000)  # 프레임 제한
    if restarted == True:
        restarted = False
        pg.mixer.music.play()
    for event in pg.event.get():  # 파이게임 이벤트
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            running = False
        elif event.type == pg.KEYDOWN and event.key == pg.K_PAGEUP:
            if duration - 100 > 0:
                duration -= 100
        elif event.type == pg.KEYDOWN and event.key == pg.K_PAGEDOWN:
            duration += 100
        elif event.type == pg.MOUSEBUTTONDOWN:
            if not isPlay:
                isPlay = True
                pg.mixer.music.play()
        elif event.type == pg.KEYDOWN and event.key == pg.K_r:
            if isPlay:
                pg.mixer.music.stop()
                notelist = Maploader.Maploader().load_notes(directory + fileName, keypositions)
                k1list = []
                k2list = []
                k3list = []
                k4list = []
                gametime = 0
                exposure_time = 0
                score = 0
                Bonus = 100
                combo = 0
                pressedkey = [False, False, False, False]
                restarted = True

        # 키보드 입력 부분
        elif event.type == pg.KEYDOWN and event.key == pg.K_z:  # 1번 키 (인덱스 0)
            pressedkey[0] = True
            if len(k1list) != 0:  # 16.5 ms 내
                inputtime = gametime - k1list[0].starttime
                if inputtime <= 16.5 and inputtime >= - 16.5:
                    print("MAX / ", inputtime)
                    last_hit = hit300g
                    exposure_time = 500
                    score += (EXscore(MaxScore, TotalNotes, "MAX"))
                    combo += 1
                    k1list.pop(0)
                elif inputtime <= 37.5 and inputtime >= - 37.5:
                    print("300 / ", inputtime)
                    last_hit = hit300
                    exposure_time = 500
                    score += (EXscore(MaxScore, TotalNotes, "300"))
                    combo += 1
                    k1list.pop(0)
                elif inputtime <= 70.5 and inputtime >= - 70.5:
                    print("200 / ", inputtime)
                    last_hit = hit200
                    exposure_time = 500
                    score += (EXscore(MaxScore, TotalNotes, "200"))
                    combo += 1
                    k1list.pop(0)
                elif inputtime <= 100.5 and inputtime >= - 100.5:
                    print("100 / ", inputtime)
                    last_hit = hit100
                    exposure_time = 500
                    score += (EXscore(MaxScore, TotalNotes, "100"))
                    combo += 1
                    k1list.pop(0)
                elif inputtime <= 124.5 and inputtime >= - 124.5:
                    print("50 / ", inputtime)
                    last_hit = hit50
                    exposure_time = 500
                    score += (EXscore(MaxScore, TotalNotes, "50"))
                    combo += 1
                    k1list.pop(0)
            print(score)
            print(combo)
        elif event.type == pg.KEYDOWN and event.key == pg.K_x:  # 2번 키 (인덱스 1)
            pressedkey[1] = True
            if len(k2list) != 0:  # 16.5 ms 내
                inputtime = gametime - k2list[0].starttime
                if inputtime <= 16.5 and inputtime >= - 16.5:
                    print("MAX / ", inputtime)
                    last_hit = hit300g
                    exposure_time = 500
                    score += EXscore(MaxScore, TotalNotes, "MAX")
                    combo += 1
                    k2list.pop(0)
                elif inputtime <= 37.5 and inputtime >= - 37.5:
                    print("300 / ", inputtime)
                    last_hit = hit300
                    exposure_time = 500
                    score += (EXscore(MaxScore, TotalNotes, "300"))
                    combo += 1
                    k2list.pop(0)
                elif inputtime <= 70.5 and inputtime >= - 70.5:
                    print("200 / ", inputtime)
                    last_hit = hit200
                    exposure_time = 500
                    score += (EXscore(MaxScore, TotalNotes, "200"))
                    combo += 1
                    k2list.pop(0)
                elif inputtime <= 100.5 and inputtime >= - 100.5:
                    print("100 / ", inputtime)
                    last_hit = hit100
                    exposure_time = 500
                    score += (EXscore(MaxScore, TotalNotes, "100"))
                    combo += 1
                    k2list.pop(0)
                elif inputtime <= 124.5 and inputtime >= - 124.5:
                    print("50 / ", inputtime)
                    last_hit = hit50
                    exposure_time = 500
                    score += (EXscore(MaxScore, TotalNotes, "50"))
                    combo += 1
                    k2list.pop(0)
            print(score)
            print(combo)
        # 3번 키 (인덱스 2)
        elif event.type == pg.KEYDOWN and event.key == pg.K_KP_2:
            pressedkey[2] = True
            if len(k3list) != 0:  # 16.5 ms 내
                inputtime = gametime - k3list[0].starttime
                if inputtime <= 16.5 and inputtime >= - 16.5:
                    print("MAX / ", inputtime)
                    last_hit = hit300g
                    exposure_time = 500
                    score += (EXscore(MaxScore, TotalNotes, "MAX"))
                    combo += 1
                    k3list.pop(0)
                elif inputtime <= 37.5 and inputtime >= - 37.5:
                    print("300 / ", inputtime)
                    last_hit = hit300
                    exposure_time = 500
                    score += (EXscore(MaxScore, TotalNotes, "300"))
                    combo += 1
                    k3list.pop(0)
                elif inputtime <= 70.5 and inputtime >= - 70.5:
                    print("200 / ", inputtime)
                    last_hit = hit200
                    exposure_time = 500
                    score += (EXscore(MaxScore, TotalNotes, "200"))
                    combo += 1
                    k3list.pop(0)
                elif inputtime <= 100.5 and inputtime >= - 100.5:
                    print("100 / ", inputtime)
                    last_hit = hit100
                    exposure_time = 500
                    score += (EXscore(MaxScore, TotalNotes, "100"))
                    combo += 1
                    k3list.pop(0)
                elif inputtime <= 124.5 and inputtime >= - 124.5:
                    print("50 / ", inputtime)
                    last_hit = hit50
                    exposure_time = 500
                    score += (EXscore(MaxScore, TotalNotes, "50"))
                    combo += 1
                    k3list.pop(0)
            print(score)
            print(combo)
        # 4번 키 (인덱스 3)
        elif event.type == pg.KEYDOWN and event.key == pg.K_KP_3:
            pressedkey[3] = True
            if len(k4list) != 0:  # 16.5 ms 내
                inputtime = gametime - k4list[0].starttime
                if inputtime <= 16.5 and inputtime >= - 16.5:
                    print("MAX / ", inputtime)
                    last_hit = hit300g
                    exposure_time = 500
                    score += (EXscore(MaxScore, TotalNotes, "MAX"))
                    combo += 1
                    k4list.pop(0)
                elif inputtime <= 37.5 and inputtime >= - 37.5:
                    print("300 / ", inputtime)
                    last_hit = hit300
                    exposure_time = 500
                    score += (EXscore(MaxScore, TotalNotes, "300"))
                    combo += 1
                    k4list.pop(0)
                elif inputtime <= 70.5 and inputtime >= - 70.5:
                    print("200 / ", inputtime)
                    last_hit = hit200
                    exposure_time = 500
                    score += (EXscore(MaxScore, TotalNotes, "200"))
                    combo += 1
                    k4list.pop(0)
                elif inputtime <= 100.5 and inputtime >= - 100.5:
                    print("100 / ", inputtime)
                    last_hit = hit100
                    exposure_time = 500
                    score += (EXscore(MaxScore, TotalNotes, "100"))
                    combo += 1
                    k4list.pop(0)
                elif inputtime <= 124.5 and inputtime >= - 124.5:
                    print("50 / ", inputtime)
                    last_hit = hit50
                    exposure_time = 500
                    score += (EXscore(MaxScore, TotalNotes, "50"))
                    combo += 1
                    k4list.pop(0)
            print(score)
            print(combo)
        # 키를 눌렀다 뗐을때 (추후 롱노트에 사용)
        elif event.type == pg.KEYUP and event.key == pg.K_z:  # 1번 키 (인덱스 0)
            pressedkey[0] = False
        elif event.type == pg.KEYUP and event.key == pg.K_x:  # 2번 키 (인덱스 1)
            pressedkey[1] = False
        elif event.type == pg.KEYUP and event.key == pg.K_KP_2:  # 3번 키 (인덱스 2)
            pressedkey[2] = False
        elif event.type == pg.KEYUP and event.key == pg.K_KP_3:  # 4번 키 (인덱스 3)
            pressedkey[3] = False

    if not isPlay:  # 플레이중이 아닐 때 임시처리 (추후에 퍼즈 기능으로 사용)
        a = 0  # 의미 없음
    else:
        gametime += clock.get_time()  # 0부터 지금까지의 시간을 저장

        # gametime 이 [생성전 대기중인 노트리스트] 0번의 스폰시간을 넘었으면
        if len(notelist) != 0:
            if gametime >= notelist[0].starttime - duration:
                if notelist[0].key == 0:
                    k1list.append(notelist.pop(0))  # 해당하는 키 리스트에 넣는다
                elif notelist[0].key == 1:
                    k2list.append(notelist.pop(0))
                elif notelist[0].key == 2:
                    k3list.append(notelist.pop(0))
                elif notelist[0].key == 3:
                    k4list.append(notelist.pop(0))

        screen.fill((0, 0, 0))  # 화면 검은색으로 채우기
        screen.blit(stagehint, (4, 800))  # 판정선 불러오기
        screen.blit(stageright, (600, 0))  # UI 불러오기
        screen.blit(stageleft, (0, 0))  # UI 불러오기

        if exposure_time > 0:
            exposure_time -= clock.get_time()
            if last_hit == hit300g:
                screen.blit(last_hit, (getmiddle_img(last_hit), 500))
            if last_hit == hit300:
                screen.blit(last_hit, (getmiddle_img(last_hit), 500))
            if last_hit == hit200:
                screen.blit(last_hit, (getmiddle_img(last_hit), 500))
            if last_hit == hit100:
                screen.blit(last_hit, (getmiddle_img(last_hit), 500))
            if last_hit == hit50:
                screen.blit(last_hit, (getmiddle_img(last_hit), 500))
            if last_hit == hit0:
                screen.blit(last_hit, (getmiddle_img(last_hit), 500))
        # 스코어의 위치 표시
        if combo > 0:
            for i in range(0, len(str(combo))):
                screen.blit(scores[int(str(combo)[i])],
                            (getmiddle_nums(i, len(str(combo))), 200))

        for i in k1list:
            # 노트 미스 처리
            if i.notetype == 1 and gametime > i.endtime + 124.5:
                print("MISS / ", gametime - i.starttime)
                last_hit = hit0
                exposure_time = 500
                combo = 0
                k1list.remove(i)
            elif i.notetype == 0 and gametime > i.starttime + 124.5:
                print("MISS / ", gametime - i.starttime)
                last_hit = hit0
                exposure_time = 500
                combo = 0
                k1list.remove(i)
            else:
                # 시간으로 노트 움직이기 (따로 설명)
                pos = 0 + perfectpos * \
                    ((gametime - i.starttime + duration) / duration)
                obj = pg.transform.scale(notepng1, (150, 50))
                screen.blit(obj, (0, pos))

                if i.notetype == 1:  # 롱노트이면
                    long_obj = pg.transform.scale(
                        notepng1, (150, getHoldNoteSize(50, i.holdlength, duration)))
                    screen.blit(long_obj, (0, pos - 50 - long_obj.get_width()))
        for i in k2list:
            if i.notetype == 1 and gametime > i.endtime + 124.5:
                print("MISS / ", gametime - i.starttime)
                last_hit = hit0
                exposure_time = 500
                combo = 0
                k2list.remove(i)
            elif i.notetype == 0 and gametime > i.starttime + 124.5:
                print("MISS / ", gametime - i.starttime)
                last_hit = hit0
                exposure_time = 500
                combo = 0
                k2list.remove(i)
            else:
                # 시간으로 노트 움직이기 (따로 설명)
                pos = 0 + perfectpos * \
                    ((gametime - i.starttime + duration) / duration)
                obj = pg.transform.scale(notepng2, (150, 50))
                screen.blit(obj, (150, pos))

                if i.notetype == 1:  # 롱노트이면
                    long_obj = pg.transform.scale(
                        notepng2, (150, getHoldNoteSize(50, i.holdlength, duration)))
                    screen.blit(long_obj, (0, pos - 50 - long_obj.get_width()))
        for i in k3list:
            if i.notetype == 1 and gametime > i.endtime + 124.5:
                print("MISS / ", gametime - i.starttime)
                last_hit = hit0
                exposure_time = 500
                combo = 0
                k3list.remove(i)
            elif i.notetype == 0 and gametime > i.starttime + 124.5:
                print("MISS / ", gametime - i.starttime)
                last_hit = hit0
                exposure_time = 500
                combo = 0
                k3list.remove(i)
            else:
                # 시간으로 노트 움직이기 (따로 설명)
                pos = 0 + perfectpos * \
                    ((gametime - i.starttime + duration) / duration)
                obj = pg.transform.scale(notepng2, (150, 50))
                screen.blit(obj, (300, pos))

                if i.notetype == 1:  # 롱노트이면
                    long_obj = pg.transform.scale(
                        notepng2, (150, getHoldNoteSize(50, i.holdlength, duration)))
                    screen.blit(long_obj, (0, pos - 50 - long_obj.get_width()))
        for i in k4list:
            if i.notetype == 1 and gametime > i.endtime + 124.5:
                print("MISS / ", gametime - i.starttime)
                last_hit = hit0
                exposure_time = 500
                combo = 0
                k4list.remove(i)
            elif i.notetype == 0 and gametime > i.starttime + 124.5:
                print("MISS / ", gametime - i.starttime)
                last_hit = hit0
                exposure_time = 500
                combo = 0
                k4list.remove(i)
            else:
                # 시간으로 노트 움직이기 (따로 설명)
                pos = 0 + perfectpos * \
                    ((gametime - i.starttime + duration) / duration)
                obj = pg.transform.scale(notepng1, (150, 50))
                screen.blit(obj, (450, pos))

                if i.notetype == 1:  # 롱노트이면
                    long_obj = pg.transform.scale(
                        notepng1, (150, getHoldNoteSize(50, i.holdlength, duration)))
                    screen.blit(long_obj, (0, pos - 50 - long_obj.get_width()))
        pg.display.update()

pg.quit()
sys.exit()

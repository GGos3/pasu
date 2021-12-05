import pygame as pg
from pygame.constants import KEYDOWN
from osureader.reader import BeatmapParser
from osureader.beatmap import Beatmap
from tkinter import filedialog
from tkinter import messagebox
from note import Note
import maploader
from enum import Enum
import os
import math
import sys
import Usersetting
import Notemanager
import Gamemanager

game_icon = pg.image.load('skin/osulogo.png')
note1 = pg.image.load('skin/mania-note1.png')  # 노트 리소스
note2 = pg.image.load('skin/mania-note2.png')  # 노트 리소스
note3 = pg.image.load('skin/mania-note2.png')  # 노트 리소스
note4 = pg.image.load('skin/mania-note1.png')  # 노트 리소스
stageright = pg.image.load('skin/mania-stage-right.png')  # UI 리소스
stageleft = pg.image.load('skin/mania-stage-left.png')  # UI 리소스
stagehint = pg.image.load('skin/mania-stage-hint.png')  # 판정선 리소스
hit0 = pg.image.load('skin/mania-hit0.png')  # hit 0 리소스
hit50 = pg.image.load('skin/mania-hit50.png')  # hit 50 리소스
hit100 = pg.image.load('skin/mania-hit100.png')  # hit 100 리소스
hit200 = pg.image.load('skin/mania-hit200.png')  # hit 200 리소스
hit300 = pg.image.load('skin/mania-hit300.png')  # hit 300 리소스
hit300g = pg.image.load('skin/mania-hit300g-0.png')  # hit 300g 리소스

rankSS = score0 = pg.image.load('skin/ranking-X.png')
rankS = score0 = pg.image.load('skin/ranking-S.png')
rankA = score0 = pg.image.load('skin/ranking-A.png')
rankB = score0 = pg.image.load('skin/ranking-B.png')
rankC = score0 = pg.image.load('skin/ranking-C.png')
rankD = score0 = pg.image.load('skin/ranking-D.png')

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

default0 = pg.image.load('skin/default-0.png')
default1 = pg.image.load('skin/default-1.png')
default2 = pg.image.load('skin/default-2.png')
default3 = pg.image.load('skin/default-3.png')
default4 = pg.image.load('skin/default-4.png')
default5 = pg.image.load('skin/default-5.png')
default6 = pg.image.load('skin/default-6.png')
default7 = pg.image.load('skin/default-7.png')
default8 = pg.image.load('skin/default-8.png')
default9 = pg.image.load('skin/default-9.png')
defaults = [default0, default1, default2, default3, default4,
            default5, default6, default7, default8, default9]

noteobject1 = pg.transform.scale(note1, (150, 50))  # 노트 오브젝트 생성
noteobject2 = pg.transform.scale(note2, (150, 50))  # 노트 오브젝트 생성
noteobject3 = pg.transform.scale(note3, (150, 50))  # 노트 오브젝트 생성
noteobject4 = pg.transform.scale(note4, (150, 50))  # 노트 오브젝트 생성
stageright = pg.transform.scale(stageright, (8, 1000))  # UI 오브젝트 생성
stageleft = pg.transform.scale(stageleft, (8, 1000))  # UI 오브젝트 생성
stagehint = pg.transform.scale(stagehint, (600, 100))  # 판정선 생성

screen = pg.display.set_mode((608, 1000))  # 해상도 설정
pg.display.set_caption("pasu!")  # 타이틀
pg.display.set_icon(game_icon)  # 아이콘
pg.init()  # 파이게임 초기화

user_setting = Usersetting.Usersetting()  # Usersetting 객체 생성
user_setting.songselect()   # 맵 선택
noteManager = Notemanager.Notemanager()
noteManager.Setup(user_setting.user_select)
gameManager = Gamemanager.manager()

beatmapSongFileName = maploader.Maploader().load_songFileName(
    user_setting.user_select)  # 음악 파일 이름 가져오기
beatmapDir = user_setting.user_select_dir  # 비트맵 폴더

sound = pg.mixer.music.load(beatmapDir+'/'+beatmapSongFileName)  # 음악 리소스 불러오기

pg.mixer.pre_init(44100, -16, 2, 0)  # 파이게임 오디오 초기화
pg.mixer.music.set_volume(0.25)
clock = pg.time.Clock()

isPlay = False
running = True
isPause = False
frameRate = 1000
isEnded = False
endDelayTime = 3000

# 인게임 시스템 변수
TotalNotes = len(noteManager.notelist)
score = 0  # 게임 점수
MaxScore = 1000000  # 최대 점수
Bonus = 100
perfectpos = 800  # 판정 선
last_accuracy = hit0
last_accuracy_exposure_time = 0  # 마지막 판정의 노출 시간
combo = 0
hitValues = [0, 0, 0, 0, 0, 0]  # MISS,50,100,200,300,MAX

pressedkey = [False, False, False, False]  # 키 입력 체크 (추후 사용)

# 화면 변수


class Screen(Enum):
    MainMenu = 0
    GamePlay = 1
    ResultScreen = 2


now_screen = Screen(1)

# 롱노트 오브젝트 길이


def getHoldNoteSize(base_height, hold_length, duration):
    return base_height * hold_length / duration

# 점수계산


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

def getAccuracy(hitValues):
    totalPointsOfHits = hitValues[1]*50 + hitValues[2] * \
        100 + hitValues[3]*200+hitValues[4]*300+hitValues[5]*300
    totalNumberofHits = hitValues[0]+hitValues[1] + \
        hitValues[2]+hitValues[3]+hitValues[4]+hitValues[5]
    result = totalPointsOfHits / (totalNumberofHits * 300)
    result = math.floor(result*10000) / 100
    return result

def getRank(accuracy):
    if accuracy <= 100:
        return 'SS'
    if accuracy <= 95:
        return 'S'
    if accuracy <= 90:
        return 'A'
    if accuracy <= 80:
        return 'B'
    if accuracy <= 70:
        return 'C'
    else:
        return 'D'

# 위치계산 함수들
# 콤보 띄우는 이미지


def getmiddle_nums(target_digit, all_digit):
    global score0  # 대표적인 숫자 콤보 이미지 변수
    return 608 / 2 - (score0.get_width() / 2) * all_digit + target_digit * score0.get_width()
# 스코어 띄우는 이미지


def getmiddle_nums_score(target_digit, all_digit):
    global default0  # 대표적인 숫자 스코어 이미지 변수
    return 608 / 2 - (default0.get_width() / 2) * all_digit + target_digit * default0.get_width()


def getmiddle_img(img):
    return 608 / 2 - (img.get_width() / 2)


def NoteRender(i):
    global gameManager, perfectpos, user_setting, note1
    gametime = gameManager.gametime
    duration = user_setting.duration

    if i.key == 0:
        pos = 0 + perfectpos * ((gametime - i.starttime + duration) / duration)
        # if i.notetype == 1:  # 롱노트이면
        #     long_obj = pg.transform.scale(
        #         note1, (150, getHoldNoteSize(50, i.holdlength, duration)))
        #     screen.blit(long_obj, (0, pos - 50 - long_obj.get_width()))
        obj = pg.transform.scale(note1, (150, 50))
        screen.blit(obj, (0, pos))
    elif i.key == 1:
        pos = 0 + perfectpos * ((gametime - i.starttime + duration) / duration)
        # if i.notetype == 1:  # 롱노트이면
        #     long_obj = pg.transform.scale(
        #         note2, (150, getHoldNoteSize(50, i.holdlength, duration)))
        #     screen.blit(long_obj, (150, pos - 50 - long_obj.get_width()))
        obj = pg.transform.scale(note2, (150, 50))
        screen.blit(obj, (150, pos))
    elif i.key == 2:
        pos = 0 + perfectpos * ((gametime - i.starttime + duration) / duration)
        # if i.notetype == 1:  # 롱노트이면
        #     long_obj = pg.transform.scale(
        #         note3, (150, getHoldNoteSize(50, i.holdlength, duration)))
        #     screen.blit(long_obj, (300, pos - 50 - long_obj.get_width()))
        obj = pg.transform.scale(note3, (150, 50))
        screen.blit(obj, (300, pos))
    elif i.key == 3:
        pos = 0 + perfectpos * ((gametime - i.starttime + duration) / duration)
        # if i.notetype == 1:  # 롱노트이면
        #     long_obj = pg.transform.scale(
        #         note4, (150, getHoldNoteSize(50, i.holdlength, duration)))
        #     screen.blit(long_obj, (450, pos - 50 - long_obj.get_width()))
        obj = pg.transform.scale(note4, (150, 50))
        screen.blit(obj, (450, pos))


def Update():
    global gameManager, noteManager, last_accuracy, last_accuracy_exposure_time, combo, isPlay

    if isPlay:
        gameManager.gametime += clock.get_time()  # 0부터 지금까지의 시간을 저장
        noteManager.SpawnNote(gameManager.gametime, user_setting.duration)
        for i in noteManager.k1list:
            if noteManager.CheckMiss(i, gameManager.gametime) == True:
                last_accuracy = hit0
                last_accuracy_exposure_time = 500
                combo = 0
                hitValues[0] += 1
                if i.islastNote:
                    isEnded = True
            else:
                NoteRender(i)
        for i in noteManager.k2list:
            if noteManager.CheckMiss(i, gameManager.gametime) == True:
                last_accuracy = hit0
                last_accuracy_exposure_time = 500
                combo = 0
                hitValues[0] += 1
                if i.islastNote:
                    isEnded = True
            else:
                NoteRender(i)
        for i in noteManager.k3list:
            if noteManager.CheckMiss(i, gameManager.gametime) == True:
                last_accuracy = hit0
                last_accuracy_exposure_time = 500
                combo = 0
                hitValues[0] += 1
                if i.islastNote:
                    isEnded = True
            else:
                NoteRender(i)
        for i in noteManager.k4list:
            if noteManager.CheckMiss(i, gameManager.gametime) == True:
                last_accuracy = hit0
                last_accuracy_exposure_time = 500
                combo = 0
                hitValues[0] += 1
                if i.islastNote:
                    isEnded = True
            else:
                NoteRender(i)


while running:
    clock.tick(frameRate)  # 프레임 제한
    gametime = gameManager.gametime

    for event in pg.event.get():  # 파이게임 이벤트
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            running = False
        elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            if isPlay == False:
                isPlay = gameManager.play()
                if isPause:
                    isPause = False
                    pg.mixer.music.unpause()
                else:
                    pg.mixer.music.play()
            else:
                pg.mixer.music.pause()
                isPlay = gameManager.pause()
                isPause = True
        elif event.type == pg.KEYDOWN and event.key == pg.K_r:
            if isPlay:
                pg.mixer.music.stop()
                noteManager.Setup(user_setting.user_select)
                gameManager.restart()
                exposure_time = 0
                score = 0
                Bonus = 100
                combo = 0
                pressedkey = [False, False, False, False]
                isPause = False
                isPlay = gameManager.play()
                pg.mixer.music.play()
                continue
        elif event.type == pg.KEYDOWN and event.key == pg.K_PAGEUP:
            if user_setting.duration - 100 > 0:
                user_setting.duration -= 100
        elif event.type == pg.KEYDOWN and event.key == pg.K_PAGEDOWN:
            user_setting.duration += 100

        elif event.type == pg.KEYDOWN and event.key == pg.K_z:  # 1번 키 (인덱스 0)
            pressedkey[0] = True
            if len(noteManager.k1list) != 0:  # 16.5 ms 내
                inputtime = gametime - noteManager.k1list[0].starttime
                if inputtime <= 16.5 and inputtime >= - 16.5:
                    print("MAX / ", inputtime)
                    last_accuracy = hit300g
                    exposure_time = 500
                    score += (EXscore(MaxScore, TotalNotes, "MAX"))
                    combo += 1
                    hitValues[5] += 1
                    if noteManager.k1list[0].islastNote:
                        isEnded = True
                    noteManager.k1list.pop(0)
                elif inputtime <= 37.5 and inputtime >= - 37.5:
                    print("300 / ", inputtime)
                    last_accuracy = hit300
                    exposure_time = 500
                    score += (EXscore(MaxScore, TotalNotes, "300"))
                    combo += 1
                    hitValues[4] += 1
                    if noteManager.k1list[0].islastNote:
                        isEnded = True
                    noteManager.k1list.pop(0)
                elif inputtime <= 70.5 and inputtime >= - 70.5:
                    print("200 / ", inputtime)
                    last_accuracy = hit200
                    exposure_time = 500
                    score += (EXscore(MaxScore, TotalNotes, "200"))
                    combo += 1
                    hitValues[3] += 1
                    if noteManager.k1list[0].islastNote:
                        isEnded = True
                    noteManager.k1list.pop(0)
                elif inputtime <= 100.5 and inputtime >= - 100.5:
                    print("100 / ", inputtime)
                    last_accuracy = hit100
                    exposure_time = 500
                    score += (EXscore(MaxScore, TotalNotes, "100"))
                    combo += 1
                    hitValues[2] += 1
                    if noteManager.k1list[0].islastNote:
                        isEnded = True
                    noteManager.k1list.pop(0)
                elif inputtime <= 124.5 and inputtime >= - 124.5:
                    print("50 / ", inputtime)
                    last_accuracy = hit50
                    exposure_time = 500
                    score += (EXscore(MaxScore, TotalNotes, "50"))
                    combo += 1
                    hitValues[1] += 1
                    if noteManager.k1list[0].islastNote:
                        isEnded = True
                    noteManager.k1list.pop(0)
        elif event.type == pg.KEYDOWN and event.key == pg.K_x:  # 2번 키 (인덱스 1)
            pressedkey[1] = True
            if len(noteManager.k2list) != 0:  # 16.5 ms 내
                inputtime = gametime - noteManager.k2list[0].starttime
                if inputtime <= 16.5 and inputtime >= - 16.5:
                    print("MAX / ", inputtime)
                    last_accuracy = hit300g
                    last_accuracy_exposure_time = 500
                    score += EXscore(MaxScore, TotalNotes, "MAX")
                    combo += 1
                    hitValues[5] += 1
                    if noteManager.k2list[0].islastNote:
                        isEnded = True
                    noteManager.k2list.pop(0)
                elif inputtime <= 37.5 and inputtime >= - 37.5:
                    print("300 / ", inputtime)
                    last_accuracy = hit300
                    last_accuracy_exposure_time = 500
                    score += (EXscore(MaxScore, TotalNotes, "300"))
                    combo += 1
                    hitValues[4] += 1
                    if noteManager.k2list[0].islastNote:
                        isEnded = True
                    noteManager.k2list.pop(0)
                elif inputtime <= 70.5 and inputtime >= - 70.5:
                    print("200 / ", inputtime)
                    last_accuracy = hit200
                    last_accuracy_exposure_time = 500
                    score += (EXscore(MaxScore, TotalNotes, "200"))
                    combo += 1
                    hitValues[3] += 1
                    if noteManager.k2list[0].islastNote:
                        isEnded = True
                    noteManager.k2list.pop(0)
                elif inputtime <= 100.5 and inputtime >= - 100.5:
                    print("100 / ", inputtime)
                    last_accuracy = hit100
                    last_accuracy_exposure_time = 500
                    score += (EXscore(MaxScore, TotalNotes, "100"))
                    combo += 1
                    hitValues[2] += 1
                    if noteManager.k2list[0].islastNote:
                        isEnded = True
                    noteManager.k2list.pop(0)
                elif inputtime <= 124.5 and inputtime >= - 124.5:
                    print("50 / ", inputtime)
                    last_accuracy = hit50
                    last_accuracy_exposure_time = 500
                    score += (EXscore(MaxScore, TotalNotes, "50"))
                    combo += 1
                    hitValues[1] += 1
                    if noteManager.k2list[0].islastNote:
                        isEnded = True
                    noteManager.k2list.pop(0)
        # 3번 키 (인덱스 2)
        elif event.type == pg.KEYDOWN and event.key == pg.K_KP_2:
            pressedkey[2] = True
            if len(noteManager.k3list) != 0:  # 16.5 ms 내
                inputtime = gametime - noteManager.k3list[0].starttime
                if inputtime <= 16.5 and inputtime >= - 16.5:
                    print("MAX / ", inputtime)
                    last_accuracy = hit300g
                    last_accuracy_exposure_time = 500
                    score += (EXscore(MaxScore, TotalNotes, "MAX"))
                    combo += 1
                    hitValues[5] += 1
                    if noteManager.k3list[0].islastNote:
                        isEnded = True
                    noteManager.k3list.pop(0)
                elif inputtime <= 37.5 and inputtime >= - 37.5:
                    print("300 / ", inputtime)
                    last_accuracy = hit300
                    last_accuracy_exposure_time = 500
                    score += (EXscore(MaxScore, TotalNotes, "300"))
                    combo += 1
                    hitValues[4] += 1
                    noteManager.k3list.pop(0)
                elif inputtime <= 70.5 and inputtime >= - 70.5:
                    print("200 / ", inputtime)
                    last_accuracy = hit200
                    last_accuracy_exposure_time = 500
                    score += (EXscore(MaxScore, TotalNotes, "200"))
                    combo += 1
                    hitValues[3] += 1
                    if noteManager.k3list[0].islastNote:
                        isEnded = True
                    noteManager.k3list.pop(0)
                elif inputtime <= 100.5 and inputtime >= - 100.5:
                    print("100 / ", inputtime)
                    last_accuracy = hit100
                    last_accuracy_exposure_time = 500
                    score += (EXscore(MaxScore, TotalNotes, "100"))
                    combo += 1
                    hitValues[2] += 1
                    if noteManager.k3list[0].islastNote:
                        isEnded = True
                    noteManager.k3list.pop(0)
                elif inputtime <= 124.5 and inputtime >= - 124.5:
                    print("50 / ", inputtime)
                    last_accuracy = hit50
                    last_accuracy_exposure_time = 500
                    score += (EXscore(MaxScore, TotalNotes, "50"))
                    combo += 1
                    hitValues[1] += 1
                    if noteManager.k3list[0].islastNote:
                        isEnded = True
                    noteManager.k3list.pop(0)
        # 4번 키 (인덱스 3)
        elif event.type == pg.KEYDOWN and event.key == pg.K_KP_3:
            pressedkey[3] = True
            if len(noteManager.k4list) != 0:  # 16.5 ms 내
                inputtime = gametime - noteManager.k4list[0].starttime
                if inputtime <= 16.5 and inputtime >= - 16.5:
                    print("MAX / ", inputtime)
                    last_accuracy = hit300g
                    last_accuracy_exposure_time = 500
                    score += (EXscore(MaxScore, TotalNotes, "MAX"))
                    combo += 1
                    hitValues[5] += 1
                    if noteManager.k4list[0].islastNote:
                        isEnded = True
                    noteManager.k4list.pop(0)
                elif inputtime <= 37.5 and inputtime >= - 37.5:
                    print("300 / ", inputtime)
                    last_accuracy = hit300
                    last_accuracy_exposure_time = 500
                    score += (EXscore(MaxScore, TotalNotes, "300"))
                    combo += 1
                    hitValues[4] += 1
                    if noteManager.k4list[0].islastNote:
                        isEnded = True
                    noteManager.k4list.pop(0)
                elif inputtime <= 70.5 and inputtime >= - 70.5:
                    print("200 / ", inputtime)
                    last_accuracy = hit200
                    last_accuracy_exposure_time = 500
                    score += (EXscore(MaxScore, TotalNotes, "200"))
                    combo += 1
                    hitValues[3] += 1
                    if noteManager.k4list[0].islastNote:
                        isEnded = True
                    noteManager.k4list.pop(0)
                elif inputtime <= 100.5 and inputtime >= - 100.5:
                    print("100 / ", inputtime)
                    last_accuracy = hit100
                    last_accuracy_exposure_time = 500
                    score += (EXscore(MaxScore, TotalNotes, "100"))
                    combo += 1
                    hitValues[2] += 1
                    if noteManager.k4list[0].islastNote:
                        isEnded = True
                    noteManager.k4list.pop(0)
                elif inputtime <= 124.5 and inputtime >= - 124.5:
                    print("50 / ", inputtime)
                    last_accuracy = hit50
                    last_accuracy_exposure_time = 500
                    score += (EXscore(MaxScore, TotalNotes, "50"))
                    combo += 1
                    hitValues[1] += 1
                    if noteManager.k4list[0].islastNote:
                        isEnded = True
                    noteManager.k4list.pop(0)
    if now_screen == Screen(0):  # 메인메뉴일때
        print('현재 메인메뉴 입니다.')
    elif now_screen == Screen(1):  # 인게임화면일때
        screen.fill((0, 0, 0))  # 화면 검은색으로 채우기
        screen.blit(stagehint, (4, 800))  # 판정선 불러오기
        screen.blit(stageright, (600, 0))  # UI 불러오기
        screen.blit(stageleft, (0, 0))  # UI 불러오기

        Update()  # 업데이트 함수

        if isEnded:
            if endDelayTime > 0:
                endDelayTime -= clock.get_time()
            else:
                now_screen = Screen(2)
                pg.mixer.music.fadeout(3000)
                print("결과창 구현")

        # 현재 콤보 표시
        if combo > 0:  # 콤보가 0보다 클때
            for i in range(0, len(str(combo))):  # 현재 콤보를 문자열로 변환 후 문자의 개수를 가져옴 -> for 반복문
                screen.blit(scores[int(str(combo)[i])],
                            (getmiddle_nums(i, len(str(combo))), 200))
                # 숫자 이미지를 리스트로 담은 scores에서 이미지를 가져옴
                # 현재콤보를 문자열로 만들어서 문자의 개수를 구한 뒤, 함수 사용 (i는 몇 번째에 있는 문자인가)

        if last_accuracy_exposure_time > 0:
            last_accuracy_exposure_time -= clock.get_time()
            if last_accuracy == hit300g:
                screen.blit(last_accuracy, (getmiddle_img(last_accuracy), 500))
            if last_accuracy == hit300:
                screen.blit(last_accuracy, (getmiddle_img(last_accuracy), 500))
            if last_accuracy == hit200:
                screen.blit(last_accuracy, (getmiddle_img(last_accuracy), 500))
            if last_accuracy == hit100:
                screen.blit(last_accuracy, (getmiddle_img(last_accuracy), 500))
            if last_accuracy == hit50:
                screen.blit(last_accuracy, (getmiddle_img(last_accuracy), 500))
            if last_accuracy == hit0:
                screen.blit(last_accuracy, (getmiddle_img(last_accuracy), 500))
    elif now_screen == Screen(2):  # 결과창일때
        screen.fill((0, 0, 0))
        accuracy = getAccuracy(hitValues)
        if score > 0:
            for i in range(0, len(str(math.floor(score)))):
                screen.blit(defaults[int(str(math.floor(score))[i])],
                            (getmiddle_nums_score(i, len(str(math.floor(score)))), 500))
        if getRank(accuracy) == 'SS':
            screen.blit(rankSS, (getmiddle_img(rankSS), 200))
        elif getRank(accuracy) == 'S':
            screen.blit(rankS, (getmiddle_img(rankS), 200))
        elif getRank(accuracy) == 'A':
            screen.blit(rankA, (getmiddle_img(rankA), 200))
        elif getRank(accuracy) == 'B':
            screen.blit(rankB, (getmiddle_img(rankB), 200))
        elif getRank(accuracy) == 'C':
            screen.blit(rankC, (getmiddle_img(rankC), 200))
        elif getRank(accuracy) == 'D':
            screen.blit(rankD, (getmiddle_img(rankD), 200))
        print('결과창일때')
        print('점수:', math.floor(score))
        print('정확도:', accuracy)
        print('랭크:', getRank(accuracy))
    pg.display.update()

pg.quit()
sys.exit()

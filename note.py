from osureader.objects import HitObject, SliderObject
from osureader.reader import BeatmapParser
from osureader.beatmap import Beatmap
import os 

class Note:
    startime = 0 #  퍼펙트 시간
    endtime = 0  #  롱노트의 종료 시간 
    notetype = 0 #  노트 타입
    key = 0      #  키 위치

    def setNote(self, note:SliderObject, position):
        self.starttime = note.time
        if note.type == SliderObject:
            self.endtime = note.time + note.length
        self.duration = 2
        self.key = position
        
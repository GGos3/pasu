from osureader.objects import HitObject, HitObjectType, SliderObject
from osureader.reader import BeatmapParser
from osureader.beatmap import Beatmap
import os 

class Note:
    startime = 0 #  퍼펙트 시간
    endtime = 0  #  롱노트의 종료 시간
    holdlength = 0
    notetype = 0 #  노트 타입
    key = 0      #  키 위치
    islastNote = False

    def setNote(self, note, position):
        self.starttime = note.time
        if note.type == int(HitObjectType.MANIA_HOLD):
            self.notetype = 1
            self.endtime = int(str(note.extras).split(':')[0])
            self.holdlength = self.endtime - note.time
        self.duration = 2
        self.key = position
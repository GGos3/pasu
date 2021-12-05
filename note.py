from osureader.objects import HitObject, HitObjectType, SliderObject
from osureader.reader import BeatmapParser
from osureader.beatmap import Beatmap
import os 

class Note:
    startTime = 0 #  퍼펙트 시간
    noteType = 0   #  노트 타입
    key = 0        #  키 위치
    islastNote = False

    def set_Note(self, note, position):
        self.startTime = note.time
        #   if note.type == int(HitObjectType.MANIA_HOLD):
        #       self.notetype = 1
        #       self.endtime = int(str(note.extras).split(':')[0])
        #       self.holdlength = self.endtime - note.time
        self.key = position
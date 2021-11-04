from osureader.objects import HitObject
from osureader.reader import BeatmapParser
from osureader.beatmap import Beatmap
import os 

class Note:
    startime = 0 #  퍼펙트 시간
    endtime = 0  #  롱노트의 종료 시간 
    notetype = 0 #  노트 타입
    duration = 0 #  이동속도
    def setNote(self, note:HitObject):
        self.starttime = note.time
        self.duration = 2
        
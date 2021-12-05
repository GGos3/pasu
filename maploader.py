from typing import List
from osureader.reader import BeatmapParser
from osureader.beatmap import Beatmap
from Note import Note


class Maploader:
    def load_songFileName(self, location):
        reader = BeatmapParser()
        beatmap = Beatmap(reader.parse(location))
        filename = beatmap.general_settings.audio_file_name
        return filename.lstrip()

    # 키 위치를 가져오는 함수
    # 오스에서 제작한 비트맵에는 노트 위치가 맵마다 뒤죽박죽임
    # 같은 4키인데 모두 다른 경우가 있음
    # 근데 오스는 이걸 정확하게 분리해 낸다.
    # 그래서 어떤 라인에 나오는지를 따로 정의해주어야함

    def load_keyposition(self, location):
        reader = BeatmapParser()                    # 비트맵 파싱 모듈 객체 가져오기
        beatmap = Beatmap(reader.parse(location))   # location의 파일 가져와서 읽기
        positions = []                              # 각 위치 저장할 리스트
        for i in beatmap.hit_objects:               # 노트 오브젝트를 돌면서
            if i.point.x not in positions:          # x 좌표가 positions 리스트에 없다면
                positions.append(i.point.x)         # 리스트에 추가해준다
        positions.sort()                            # 오름차순으로 정렬
        return positions

    # 노트 오브젝트를 가져오는 함수
    def load_notes(self, location, keypositons: List):
        reader = BeatmapParser()
        beatmap = Beatmap(reader.parse(location))
        notes = []
        objects = beatmap.hit_objects
        for i in objects:
            cache = Note()
            cache.set_Note(i, keypositons.index(i.point.x))
            notes.append(cache)
        return notes

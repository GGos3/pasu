from tkinter import filedialog
from tkinter import messagebox
import tkinter
import os
import sys


class Usersetting:
    duration = 500  # 스크롤 속도
    user_select = ''  # 선택한 비트맵
    user_select_dir = ''  # 선택한 비트맵 폴더

    def setSkin(args):
        print()

    def songSelect(self):
        root = tkinter.Tk()
        root.overrideredirect(True)
        root.attributes("-alpha", 0)
        # files 변수에 선택 파일 경로 넣기
        files = filedialog.askopenfilename(
            title='비트맵 파일을 선택해 주세요', filetypes=[('비트맵 파일', '*.osu')])
        root.destroy()
        # print(files)    # files 값 출력

        if files == '':
            # 파일 선택 안했을 때 메세지 출력
            messagebox.showwarning('경고', '.osu 파일을 선택해 주세요.')
            sys.exit()

        self.user_select = files
        self.user_select_dir = os.path.dirname(files)

import sys
import book
import configparser
import os

config = configparser.ConfigParser()

path = os.path.join(os.path.dirname(__file__), "setting.ini")  # BOMなしに注意
config.read(path, "UTF-8")
print(config.sections())

number = config["info"]["LOGIN_ID"]
password1 = config["info"]["LOGIN_PW"]
lesson = config["info"]["CLASS"]
shop = config["info"]["SHOP"]
start = config["info"]["DAY"]
ti = config["info"]["TIME"]

sys.path.append(
    "C:\\Users\\saku\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\site-packages"
)
import PySimpleGUI as sg
from datetime import datetime, timedelta

sg.theme("Black")

frame1 = (
    [
        [sg.Text("以下を入力してください。"), sg.Button("クリア", key="clear")],
        [sg.Text("会員番号"), sg.Input(number, key="number")],
        [sg.Text("パスワード"), sg.Input(password1, key="password")],
        [sg.Text("レッスン名"), sg.Input(lesson, key="lesson")],
        [sg.Text("施設名"), sg.Input(shop, key="club")],
        [sg.Text("レッスン日時")],
        [sg.Input(start, key="calender")],
        [
            sg.CalendarButton(
                "日付選択",
                close_when_date_chosen=False,
                key="day",
                target="calender",
                format="%#m/%#d",
            ),
        ],
        [sg.Text("開始時刻(例 1:23)"), sg.Input(ti, key="start_time")],
        [sg.Button("OK", key="ok")],
        [sg.Text("システムメッセージ")],
        [sg.Output(size=(50, 10), key="output")],
    ],
)

date_format = "%m/%d"

layouts = frame1

window = sg.Window("自動予約bot", layout=layouts, resizable=True, location=(100, 100))

while True:
    event, values = window.read()
    print(event, values)

    if event == sg.WIN_CLOSED:
        break

    elif event == "clear":  # クリアボタンを押したとき。
        window["lesson"].update("")
        window["day"].update("")
        window["start_time"].update("")

    elif event == "ok":  # okボタンを押したとき。
        day = values["calender"]
        date_obj = datetime.strptime(day, date_format)
        date_obj = date_obj.replace(year=datetime.now().year)
        week_ago = date_obj - timedelta(days=7)
        week_ago = week_ago.replace(hour=6, minute=59, second=55)
        print(week_ago.strftime("%Y-%m-%d %H:%M:%S"))
        current = datetime.now()
        number = values["number"]
        passcode = values["password"]
        lesson = values["lesson"]
        club = values["club"]
        print(day)
        print(number)
        print(passcode)
        print(lesson)
        print(club)
        if week_ago.strftime("%Y-%m-%d %H:%M:%S") == current.strftime(
            "%Y-%m-%d %H:%M:%S"
        ):
            try:
                book.book(number, passcode, day, lesson, club)

            except Exception:
                print("予約に失敗しました")
                print(Exception)
            else:
                print("予約に成功しました")

window.close()

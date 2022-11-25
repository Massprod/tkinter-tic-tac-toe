import tkinter
from tkinter import *
import random
import pyautogui
import os
import time

global PLAYER  # PLAYER = 3: X-win, PLAYER = 4: O-win.
global GAME_NUM, TURN_NUM


def start_game():
    global PLAYER, GAME_NUM, TURN_NUM
    try:
        GAME_NUM = int(list(os.listdir('history')[-1])[-1])
        GAME_NUM += 1
    except FileNotFoundError:
        os.mkdir(path="C:/Users/Pampam/PycharmProjects/StartProject2/history")
        GAME_NUM = 0
    TURN_NUM = 0
    PLAYER = random.randint(1, 2)
    for button in main_w.winfo_children()[:9]:
        button.grid()
    for button in main_w.winfo_children()[9:]:
        button.grid_remove()


def tile_clicked(event):
    global PLAYER
    if event:
        if PLAYER == 1 and event.widget["text"] == "-":
            event.widget["image"] = x_mark
            event.widget["text"] = "x"
            PLAYER += 1
            screenshot()
        elif PLAYER == 2 and event.widget["text"] == "-":
            event.widget["image"] = o_mark
            event.widget["text"] = "o"
            PLAYER -= 1
            screenshot()
    played_tiles = []
    for widget in main_w.winfo_children()[:9]:
        played_tiles.append(widget["text"])
    # 1 row 0 1 2 [:3] slice
    # 2 row 3 4 5 [3:6] slice
    # 3 row 6 7 8 [6:9] slice
    # 8 win conditions:
    # 0 1 2 , 3 4 5 , 6 7 8 , 6 4 2 , 8 4 0 , 2 5 8 , 0 3 6 , 1 4 7
    # [:3]  , [3:6] , [6:9] , [6]+[4]+[2] , [8]+[4]+[0] , [2] [5] [8] , [0] [3] [6] , [1] [4] [7]
    win_conditions = {"012": f"{played_tiles[0]}{played_tiles[1]}{played_tiles[2]}",
                      "345": f"{played_tiles[3]}{played_tiles[4]}{played_tiles[5]}",
                      "678": f"{played_tiles[6]}{played_tiles[7]}{played_tiles[8]}",
                      "642": f"{played_tiles[6]}{played_tiles[4]}{played_tiles[2]}",
                      "840": f"{played_tiles[8]}{played_tiles[4]}{played_tiles[0]}",
                      "258": f"{played_tiles[2]}{played_tiles[5]}{played_tiles[8]}",
                      "036": f"{played_tiles[0]}{played_tiles[3]}{played_tiles[6]}",
                      "147": f"{played_tiles[1]}{played_tiles[4]}{played_tiles[7]}",
                      }
    for key in win_conditions:
        if win_conditions[key].count("x") == 3:
            PLAYER = 3
            main_w.winfo_children()[-3].grid()
            for index in list(key):
                main_w.winfo_children()[:9][int(index)]["image"] = x_mark_won
                for x in range(0, 9):
                    if str(x) not in key:
                        if main_w.winfo_children()[:9][x]["text"] == "x":
                            main_w.winfo_children()[:9][x]["image"] = x_mark_lost
                        elif main_w.winfo_children()[:9][x]["text"] == "o":
                            main_w.winfo_children()[:9][x]["image"] = o_mark_lost
        elif win_conditions[key].count("o") == 3:
            PLAYER = 4
            main_w.winfo_children()[-3].grid()
            for index in list(key):
                main_w.winfo_children()[:9][int(index)]["image"] = o_mark_won
                for x in range(0, 9):
                    if str(x) not in key:
                        if main_w.winfo_children()[:9][x]["text"] == "x":
                            main_w.winfo_children()[:9][x]["image"] = x_mark_lost
                        elif main_w.winfo_children()[:9][x]["text"] == "o":
                            main_w.winfo_children()[:9][x]["image"] = o_mark_lost
    if "-" not in played_tiles:
        main_w.winfo_children()[-3].grid()
        for x in range(0, 9):
            if main_w.winfo_children()[:9][x]["text"] == "x":
                main_w.winfo_children()[:9][x]["image"] = x_mark_draw
            elif main_w.winfo_children()[:9][x]["text"] == "o":
                main_w.winfo_children()[:9][x]["image"] = o_mark_draw


def screenshot():
    global GAME_NUM, TURN_NUM
    try:
        os.mkdir(path=f"C:/Users/Pampam/PycharmProjects/StartProject2/history/Game{GAME_NUM}")
    except FileExistsError:
        pass

    TURN_NUM += 1
    pyautogui.screenshot(f"history/Game{GAME_NUM}/turn{TURN_NUM}.png",
                         region=(
                             main_w.winfo_rootx(),
                             main_w.winfo_rooty(),
                             main_w.winfo_width(),
                             main_w.winfo_height()
                         ))


def hide_tiles():
    for widget in main_w.winfo_children()[:9]:
        widget["image"] = tile
        widget["text"] = "-"
        widget.bind("<ButtonPress-1>", tile_clicked)
        widget.grid_remove()


main_w = Tk()
# media zone #
tile = tkinter.PhotoImage(file="media/tile_170x170.png.")
x_mark = tkinter.PhotoImage(file="media/x_mark_170x170.png")
x_mark_won = tkinter.PhotoImage(file="media/x_mark_170x170_win.png")
x_mark_lost = tkinter.PhotoImage(file="media/x_mark_170x170_lose.png")
x_mark_draw = tkinter.PhotoImage(file="media/x_mark_170x170_draw.png")
o_mark = tkinter.PhotoImage(file="media/o_mark_170x170.png")
o_mark_won = tkinter.PhotoImage(file="media/o_mark_170x170_win.png")
o_mark_lost = tkinter.PhotoImage(file="media/o_mark_170x170_lose.png")
o_mark_draw = tkinter.PhotoImage(file="media/o_mark_170x170_draw.png")
icon = tkinter.PhotoImage(file="media/ttt_icon.png")
start_icon = tkinter.PhotoImage(file="media/start_450x450.png")
history_icon = tkinter.PhotoImage(file="media/history_55x55.png")
versus_icon = tkinter.PhotoImage(file="media/vs_ai_155x96.png")
replay_icon = tkinter.PhotoImage(file="media/replay_130x130.png")
# main window - setup, size, centering experiments #
# Was trying to do somewhat, flexible resolution for main_window, to adapt padding and window size for
# different screen resolutions, but didn't work out as I wanted. Leaving fixed resolution and padding.
main_w.update_idletasks()
main_w_width = int(main_w.winfo_screenwidth() * 0.45)
main_w_height = int(main_w.winfo_screenheight() * 0.6)
main_w_start_x = int((main_w.winfo_screenwidth() / 2) - main_w_width / 2)
main_w_start_y = int((main_w.winfo_screenheight() / 2) - main_w_height / 2)
main_w.geometry(f"{800}x{600}+{main_w_start_x}+{main_w_start_y}")
main_w.resizable(False, False)
main_w.iconphoto(True, icon)
main_w.title("TicTacToe")
main_w.config(padx=145,
              pady=45, )
# tiles setup #
# I was thinking obviously making it by loop, but for this I would need coordinates and dictionary for them.
# While I was thinking how to place and align them, already have made all of them.
# Won't be needed dictionary with values for these buttons (for now), prefer leave it like this and hide with loop.
tile_11 = Button(main_w,
                 image=o_mark,
                 highlightthickness=0,
                 border=0,
                 relief=tkinter.RIDGE,
                 )
tile_11.grid(row=0,
             column=0,
             )
tile_12 = Button(main_w,
                 image=x_mark,
                 highlightthickness=0,
                 border=0,
                 relief=tkinter.RIDGE,
                 )
tile_12.grid(row=0,
             column=1,
             )
tile_13 = Button(main_w,
                 image=o_mark,
                 highlightthickness=0,
                 border=0,
                 relief=tkinter.RIDGE,
                 )
tile_13.grid(row=0,
             column=2,
             )
tile_21 = Button(main_w,
                 image=tile,
                 highlightthickness=0,
                 border=0,
                 relief=tkinter.RIDGE,
                 )
tile_21.grid(row=1,
             column=0,
             )
tile_22 = Button(main_w,
                 image=o_mark,
                 highlightthickness=0,
                 border=0,
                 relief=tkinter.RIDGE,
                 )
tile_22.grid(row=1,
             column=1,
             )
tile_23 = Button(main_w,
                 image=tile,
                 highlightthickness=0,
                 border=0,
                 relief=tkinter.RIDGE,
                 )
tile_23.grid(row=1,
             column=2,
             )
tile_31 = Button(main_w,
                 image=tile,
                 highlightthickness=0,
                 border=0,
                 relief=tkinter.RIDGE,
                 )
tile_31.grid(row=2,
             column=0,
             )
tile_32 = Button(main_w,
                 image=x_mark,
                 highlightthickness=0,
                 border=0,
                 relief=tkinter.RIDGE,
                 )
tile_32.grid(row=2,
             column=1,
             )
tile_33 = Button(main_w,
                 image=o_mark,
                 highlightthickness=0,
                 border=0,
                 relief=tkinter.RIDGE,
                 )
tile_33.grid(row=2,
             column=2,
             )
hide_tiles()
# start button #
start_button = Button(main_w,
                      image=start_icon,
                      highlightthickness=0,
                      border=0,
                      relief=tkinter.RIDGE,
                      command=start_game,
                      )
start_button.grid(row=0,
                  columnspan=2,
                  padx=(30, 30),
                  )
# replay button #
replay_button = Button(main_w,
                       image=replay_icon,
                       highlightthickness=0,
                       border=0,
                       relief=tkinter.RIDGE,
                       command=lambda: (hide_tiles(), screenshot(), start_game()),
                       )
replay_button.grid(
    row=1,
    column=3,
    padx=(15, 0)
)
replay_button.grid_remove()
# history button #
history_button = Button(main_w,
                        compound="right",
                        text="Played",
                        font=("Helvetica", 15, "bold"),
                        image=history_icon,
                        highlightthickness=0,
                        border=0,
                        relief=tkinter.RIDGE,
                        )
history_button.grid(row=1,
                    column=0,
                    sticky="w",
                    pady=25,
                    )
# versus button #
versus_button = Button(main_w,
                       image=versus_icon,
                       highlightthickness=0,
                       border=0,
                       relief=tkinter.RIDGE,
                       )
versus_button.grid(row=1,
                   column=1,
                   sticky="e",
                   pady=10,
                   )

main_w.mainloop()

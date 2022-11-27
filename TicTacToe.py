import tkinter
from tkinter import *
import random
import pyautogui
import os
from tkinter import ttk

global PLAYER, PLAYER_IMAGE, AI_IMAGE  # PLAYER = 4: X-win, PLAYER = 5: O-win.
global GAME_NUM, TURN_NUM
history_list = []


def start_game(ai=False):
    global PLAYER, GAME_NUM, TURN_NUM, PLAYER_IMAGE, AI_IMAGE
    try:
        played = [int(element.strip("Game")) for element in os.listdir('history')]
        played.sort()
        GAME_NUM = played[-1]
        GAME_NUM += 1
        PLAYER = 0
    except FileNotFoundError:
        GAME_NUM = 0
        os.mkdir(path="history")
        PLAYER = 0
    except IndexError:
        GAME_NUM = 0
        os.mkdir(path=f"history/Game{GAME_NUM}")
        PLAYER = 0
    if not ai:
        TURN_NUM = 0
        PLAYER = random.randint(1, 2)
        for button in main_w.winfo_children()[:9]:
            button.grid()
        for button in main_w.winfo_children()[9:]:
            button.grid_remove()
        go_back_button.grid()
        replay_button.config(command=lambda: (hide_tiles(), screenshot(), start_game()))
    else:
        TURN_NUM = 0
        PLAYER = 6
        for button in main_w.winfo_children()[:9]:
            button.grid()
        for button in main_w.winfo_children()[9:]:
            button.grid_remove()
        go_back_button.grid()
        marks = [x_mark, o_mark]
        random.shuffle(marks)
        PLAYER_IMAGE = random.choice(marks)
        marks.remove(PLAYER_IMAGE)
        AI_IMAGE = marks[0]
        replay_button.configure(command=lambda: (hide_tiles(), screenshot(), start_game(ai=True)))


def win_check():
    global PLAYER
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
            PLAYER = 4
            replay_button.grid()
            for index in list(key):
                main_w.winfo_children()[:9][int(index)]["image"] = x_mark_won
                for x in range(0, 9):
                    if str(x) not in key:
                        if main_w.winfo_children()[:9][x]["text"] == "x":
                            main_w.winfo_children()[:9][x]["image"] = x_mark_lost
                        elif main_w.winfo_children()[:9][x]["text"] == "o":
                            main_w.winfo_children()[:9][x]["image"] = o_mark_lost
        elif win_conditions[key].count("o") == 3:
            PLAYER = 5
            replay_button.grid()
            for index in list(key):
                main_w.winfo_children()[:9][int(index)]["image"] = o_mark_won
                for x in range(0, 9):
                    if str(x) not in key:
                        if main_w.winfo_children()[:9][x]["text"] == "x":
                            main_w.winfo_children()[:9][x]["image"] = x_mark_lost
                        elif main_w.winfo_children()[:9][x]["text"] == "o":
                            main_w.winfo_children()[:9][x]["image"] = o_mark_lost
    if "-" not in played_tiles:
        replay_button.grid()
        if PLAYER <= 3 or PLAYER == 6:  # was overwriting wins with draw, if the last move was a win_move
            for x in range(0, 9):
                if main_w.winfo_children()[:9][x]["text"] == "x":
                    main_w.winfo_children()[:9][x]["image"] = x_mark_draw
                elif main_w.winfo_children()[:9][x]["text"] == "o":
                    main_w.winfo_children()[:9][x]["image"] = o_mark_draw
    return win_conditions


def tile_clicked(event):
    global PLAYER, PLAYER_IMAGE
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
        elif PLAYER == 6 and event.widget["text"] == "-":
            event.widget["image"] = PLAYER_IMAGE
            if PLAYER_IMAGE == x_mark:
                event.widget["text"] = "x"
            else:
                event.widget["text"] = "o"
            screenshot()
            PLAYER = 3
    ai_brain(win_check())
    win_check()


def ai_brain(win_conditions):
    global PLAYER, TURN_NUM
    if PLAYER == 3:
        PLAYER = 6
        strength = [100, 50]
        strength = random.choice(strength)
        if TURN_NUM == 2:
            if AI_IMAGE == x_mark:
                for key in win_conditions:
                    if win_conditions[key].count("o") == 2:
                        for x in range(0, 3):
                            if win_conditions[key][x] == "-":
                                main_w.winfo_children()[int(list(key)[x])]["image"] = x_mark
                                main_w.winfo_children()[int(list(key)[x])]["text"] = "x"
                                return
                            elif win_conditions[key][x] == "x":
                                for y in range(0, 100):
                                    ai_tile = random.choice(main_w.winfo_children()[:9])
                                    if ai_tile["text"] == "-":
                                        if AI_IMAGE == x_mark:
                                            if ai_tile["text"] == "-":
                                                ai_tile["image"] = x_mark
                                                ai_tile["text"] = "x"
                                                return
                                        else:
                                            if ai_tile["text"] == "-":
                                                ai_tile["image"] = o_mark
                                                ai_tile["text"] = "o"
                                                return
                    elif win_conditions[key].count("o") == 1:
                        for _ in range(0, 100):
                            ai_tile = random.choice(main_w.winfo_children()[:9])
                            if ai_tile["text"] == "-":
                                if AI_IMAGE == x_mark:
                                    if ai_tile["text"] == "-":
                                        ai_tile["image"] = x_mark
                                        ai_tile["text"] = "x"
                                        return
                                else:
                                    if ai_tile["text"] == "-":
                                        ai_tile["image"] = o_mark
                                        ai_tile["text"] = "o"
                                        return
            else:
                for key in win_conditions:
                    if win_conditions[key].count("x") == 2:
                        for x in range(0, 3):
                            if win_conditions[key][x] == "-":
                                main_w.winfo_children()[int(list(key)[x])]["image"] = o_mark
                                main_w.winfo_children()[int(list(key)[x])]["text"] = "o"
                                return
                            elif win_conditions[key][x] == "o":
                                for y in range(0, 100):
                                    ai_tile = random.choice(main_w.winfo_children()[:9])
                                    if ai_tile["text"] == "-":
                                        if AI_IMAGE == x_mark:
                                            if ai_tile["text"] == "-":
                                                ai_tile["image"] = x_mark
                                                ai_tile["text"] = "x"
                                                return
                                        else:
                                            if ai_tile["text"] == "-":
                                                ai_tile["image"] = o_mark
                                                ai_tile["text"] = "o"
                                                return
        elif strength == 50 or TURN_NUM < 2:
            for _ in range(0, 100):
                ai_tile = random.choice(main_w.winfo_children()[:9])
                if ai_tile["text"] == "-":
                    if AI_IMAGE == x_mark:
                        if ai_tile["text"] == "-":
                            ai_tile["image"] = x_mark
                            ai_tile["text"] = "x"
                            return
                    else:
                        if ai_tile["text"] == "-":
                            ai_tile["image"] = o_mark
                            ai_tile["text"] = "o"
                            return
        if strength == 100:
            if AI_IMAGE == x_mark:
                for key in win_conditions:
                    if win_conditions[key].count("o") == 2:
                        for x in range(0, 3):
                            if win_conditions[key][x] == "-":
                                main_w.winfo_children()[int(list(key)[x])]["image"] = x_mark
                                main_w.winfo_children()[int(list(key)[x])]["text"] = "x"
                                return
                    elif win_conditions[key].count("o") == 1:
                        for _ in range(0, 100):
                            ai_tile = random.choice(main_w.winfo_children()[:9])
                            if ai_tile["text"] == "-":
                                if AI_IMAGE == x_mark:
                                    if ai_tile["text"] == "-":
                                        ai_tile["image"] = x_mark
                                        ai_tile["text"] = "x"
                                        return
                                else:
                                    if ai_tile["text"] == "-":
                                        ai_tile["image"] = o_mark
                                        ai_tile["text"] = "o"
                                        return
            else:
                for key in win_conditions:
                    if win_conditions[key].count("x") == 2:
                        for x in range(0, 3):
                            if win_conditions[key][x] == "-":
                                main_w.winfo_children()[int(list(key)[x])]["image"] = o_mark
                                main_w.winfo_children()[int(list(key)[x])]["text"] = "o"
                                return
                    elif win_conditions[key].count("o") == 1:
                        for _ in range(0, 100):
                            ai_tile = random.choice(main_w.winfo_children()[:9])
                            if ai_tile["text"] == "-":
                                if AI_IMAGE == x_mark:
                                    if ai_tile["text"] == "-":
                                        ai_tile["image"] = x_mark
                                        ai_tile["text"] = "x"
                                        return
                                else:
                                    if ai_tile["text"] == "-":
                                        ai_tile["image"] = o_mark
                                        ai_tile["text"] = "o"
                                        return


def screenshot():
    global GAME_NUM, TURN_NUM, PLAYER
    try:
        os.mkdir(path=f"history/Game{GAME_NUM}")
    except FileExistsError:
        pass

    TURN_NUM += 1
    pyautogui.screenshot(f"history/Game{GAME_NUM}/turn{TURN_NUM}.png",
                         region=(
                             main_w.winfo_rootx() + 136.5,
                             main_w.winfo_rooty() + 40,
                             525,
                             520,
                         ))


def hide_tiles():
    for widget in main_w.winfo_children()[:9]:
        widget["image"] = tile
        widget["text"] = "-"
        widget.bind("<ButtonPress-1>", tile_clicked)
        widget.grid_remove()
    for widget in main_w.winfo_children()[9:12]:
        widget.grid_remove()


def menu():
    for widget in main_w.winfo_children()[10:14]:
        widget.grid()


def history():
    main_w.config(padx=0)
    for widget in main_w.winfo_children()[10:14]:
        widget.grid_remove()
    played = [int(element.strip("Game")) for element in os.listdir('history')]  # all games
    played.sort()
    game_index = played[-1]
    all_turns = os.listdir(f"history/Game{game_index}")
    for index in all_turns:
        path = f"history/Game{played[0]}/{index}"
        history_list.append(tkinter.PhotoImage(file=path))
    print(history_list)
    history_label = Canvas(main_w,
                           width=525,
                           height=520)

    history_label.grid(row=0,
                       column=1)
    go_back_history = Button(main_w,
                             image=go_back_icon,
                             highlightthickness=0,
                             border=0,
                             relief=tkinter.RIDGE,
                             )
    go_back_history.grid(row=0,
                         column=2,
                         sticky="se")
    history_label.create_image(0, 0, image=history_list[0], anchor=NW)
    go_back_history.lower()
    style = ttk.Style()
    style.configure("TCombobox", fieldbackground="white", foreground="black",
                    background="white", highlightthickness=0, border=0, highlightcolor="white")
    choose_game = ttk.Combobox(main_w,
                               width=15,
                               values=["test", "test1", "test"],
                               justify="right",
                               state="readonly",
                               )
    choose_game.bind("<<ComboboxSelected>>", lambda e: main_w.focus())
    choose_game.current(0)
    choose_game.grid(row=0,
                     column=2,
                     sticky="n",
                     )
    back_scroll_button = Button(main_w,
                             image=go_back_icon,
                             highlightthickness=0,
                             border=0,
                             relief=tkinter.RIDGE,
                             )
    back_scroll_button.grid(row=0,
                            column=0,
                            sticky="w")


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
go_back_icon = tkinter.PhotoImage(file="media/go_back_130x130.png")
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
# replay button #
replay_button = Button(main_w,
                       image=replay_icon,
                       highlightthickness=0,
                       border=0,
                       relief=tkinter.RIDGE,
                       command=lambda: (hide_tiles(), screenshot()),
                       )
replay_button.grid(
    row=1,
    column=3,
    padx=(15, 0)
)
replay_button.grid_remove()
# go back button #
go_back_button = Button(main_w,
                        image=go_back_icon,
                        highlightthickness=0,
                        border=0,
                        relief=tkinter.RIDGE,
                        command=lambda: (hide_tiles(), screenshot(), menu())
                        )
go_back_button.grid(row=2,
                    column=3,
                    padx=(15, 0),
                    )
go_back_button.grid_remove()
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
# history button #
history_button = Button(main_w,
                        compound="right",
                        text="Played",
                        font=("Helvetica", 15, "bold"),
                        image=history_icon,
                        highlightthickness=0,
                        border=0,
                        relief=tkinter.RIDGE,
                        command=history,
                        )
history_button.grid(row=1,
                    column=0,
                    sticky="w",
                    pady=(10, 0),
                    )
# versus button #
versus_button = Button(main_w,
                       image=versus_icon,
                       highlightthickness=0,
                       border=0,
                       relief=tkinter.RIDGE,
                       command=lambda: start_game(ai=True),
                       )
versus_button.grid(row=1,
                   column=1,
                   sticky="e",
                   pady=(10, 0),
                   padx=(25, 0),
                   )
main_w.mainloop()

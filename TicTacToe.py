import os
import shutil
import random
import tkinter
import pyautogui
from tkinter import *
from tkinter import ttk


global PLAYER, PLAYER_IMAGE, AI_IMAGE  # PLAYER == 4: X-win, PLAYER == 5: O-win.
global GAME_NUM, TURN_NUM, HISTORY_TURN, HISTORY_INDEX
history_list: list[PhotoImage] = []
main_w_background: str = '#FFFFFF'


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
        if AI_IMAGE == x_mark:
            for key in win_conditions:
                if win_conditions[key].count("x") == 2:
                    for x in range(0, 3):
                        if win_conditions[key][x] == "-":
                            main_w.winfo_children()[int(list(key)[x])]["image"] = x_mark
                            main_w.winfo_children()[int(list(key)[x])]["text"] = "x"
                            return
                elif win_conditions[key].count("o") == 2:
                    for x in range(0, 3):
                        if win_conditions[key][x] == "-":
                            main_w.winfo_children()[int(list(key)[x])]["image"] = x_mark
                            main_w.winfo_children()[int(list(key)[x])]["text"] = "x"
                            return
            else:
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
                if win_conditions[key].count("o") == 2:
                    for x in range(0, 3):
                        if win_conditions[key][x] == "-":
                            main_w.winfo_children()[int(list(key)[x])]["image"] = o_mark
                            main_w.winfo_children()[int(list(key)[x])]["text"] = "o"
                            return
                elif win_conditions[key].count("x") == 2:
                    for x in range(0, 3):
                        if win_conditions[key][x] == "-":
                            main_w.winfo_children()[int(list(key)[x])]["image"] = o_mark
                            main_w.winfo_children()[int(list(key)[x])]["text"] = "o"
                            return
            else:
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
    main_w.config(padx=145,
                  pady=45,
                  )
    for widget in main_w.winfo_children():
        widget.grid_remove()
    for widget in main_w.winfo_children()[10:14]:
        widget.grid()
    history_list.clear()
    history_choose_game.configure(values=[])
    # If History exist, delete every game with less than 3 steps.
    # 1 screenshot is always empty board. So it's <= 3.
    try:
        for game in os.listdir(f'history'):
            if len(os.listdir(f'history/{game}')) <= 3:
                shutil.rmtree(f'history/{game}')
    except FileNotFoundError:
        pass


def history():
    global HISTORY_TURN, HISTORY_INDEX
    # change all widgets to list maybe #
    # if I don't want to make other window to show it, I need to create all widget's out of the function
    # otherwise it will change winfo_children() order!
    try:
        for widget in main_w.winfo_children():
            widget.grid_remove()
        main_w.config(padx=75)
        # (maybe) change it for lists, one list for every window option #
        history_go_back_button.grid()
        history_label.grid()
        history_choose_game.grid()
        history_prev_turn_button.grid()
        history_next_turn_button.grid()
        history_delete_button.grid()

        played = [int(element.strip("Game")) for element in os.listdir('history')]  # all games
        played.sort()
        HISTORY_INDEX = played[-1]  # last game played
        all_turns = os.listdir(f"history/Game{HISTORY_INDEX}")
        all_turns = [int(name.strip("turn.png")) for name in all_turns]
        all_turns.sort()
        HISTORY_TURN = 0
        # trash collector deletes created photos if they're not stored out of function
        for index in all_turns:
            path = f"history/Game{HISTORY_INDEX}/turn{index}.png"
            history_list.append(tkinter.PhotoImage(file=path))
        history_label.create_image(0, 0, image=history_list[HISTORY_TURN], anchor=NW)
        history_choose_game.configure(values=[str(f"Game: {value}") for value in played])
        history_choose_game.set(f"Game: {played[-1]}")
    except FileNotFoundError:
        menu()
    except IndexError:
        menu()


def history_next_turn(back=False):
    global HISTORY_TURN
    if not back:
        HISTORY_TURN += 1
        try:
            history_label.create_image(0, 0, image=history_list[HISTORY_TURN], anchor=NW)
        except IndexError:
            HISTORY_TURN -= 1
    else:
        if HISTORY_TURN > 0:
            HISTORY_TURN -= 1
            try:
                history_label.create_image(0, 0, image=history_list[HISTORY_TURN], anchor=NW)
            except IndexError:
                HISTORY_TURN += 1


def history_game_chosen():
    global HISTORY_INDEX, HISTORY_TURN
    HISTORY_INDEX = (history_choose_game.get()).strip("Game: ")
    all_turns = os.listdir(f"history/Game{HISTORY_INDEX}")
    all_turns = [int(name.strip("turn.png")) for name in all_turns]
    all_turns.sort()  # mb I could sort with strings, search it later
    HISTORY_TURN = 0
    history_list.clear()
    for index in all_turns:
        path = f"history/Game{HISTORY_INDEX}/turn{index}.png"
        history_list.append(tkinter.PhotoImage(file=path))
    # history_list is holding all created images.
    # So it will show them correct even if delete directory or images from directory.
    # But, if we will try to choose same Game again when directory empty or deleted,
    #  then it will corrupt HISTORY_TURN and raise directory not_found.
    # So if all_turns is empty then directory doesn't exist.
    if history_list:
        history_label.create_image(0, 0, image=history_list[HISTORY_TURN], anchor=NW)
    else:
        delete_history_game_chosen()


def delete_history_game_chosen():
    global HISTORY_INDEX, HISTORY_TURN
    # Needs to be sorted, otherwise we will get listdir with dict ordering.
    # And cases like 10 -> 9 will try to rename 10 to 9 when it's still not changed to 8.
    game_indexes = sorted([int(element.strip("Game")) for element in os.listdir(f"history")])
    if HISTORY_INDEX == game_indexes[-1]:
        shutil.rmtree(f"history/Game{HISTORY_INDEX}")
    else:
        shutil.rmtree(f"history/Game{HISTORY_INDEX}")
        for index in game_indexes:
            if index > int(HISTORY_INDEX):
                os.rename(f'history/Game{index}', f'history/Game{index - 1}')
    history_list.clear()  # clearing list of images, otherwise they will append another game history
    history()


# Main window.
main_w = Tk()
# Media zone
tile: PhotoImage = tkinter.PhotoImage(file="media/tile_170x170.png.")
x_mark: PhotoImage = tkinter.PhotoImage(file="media/x_mark_170x170.png")
x_mark_won: PhotoImage = tkinter.PhotoImage(file="media/x_mark_170x170_win.png")
x_mark_lost: PhotoImage = tkinter.PhotoImage(file="media/x_mark_170x170_lose.png")
x_mark_draw: PhotoImage = tkinter.PhotoImage(file="media/x_mark_170x170_draw.png")
o_mark: PhotoImage = tkinter.PhotoImage(file="media/o_mark_170x170.png")
o_mark_won: PhotoImage = tkinter.PhotoImage(file="media/o_mark_170x170_win.png")
o_mark_lost: PhotoImage = tkinter.PhotoImage(file="media/o_mark_170x170_lose.png")
o_mark_draw: PhotoImage = tkinter.PhotoImage(file="media/o_mark_170x170_draw.png")
icon: PhotoImage = tkinter.PhotoImage(file="media/ttt_icon.png")
start_icon: PhotoImage = tkinter.PhotoImage(file="media/start_450x450.png")
history_icon: PhotoImage = tkinter.PhotoImage(file="media/history_55x55.png")
versus_icon: PhotoImage = tkinter.PhotoImage(file="media/vs_ai_155x96.png")
replay_icon: PhotoImage = tkinter.PhotoImage(file="media/replay_130x130.png")
go_back_icon: PhotoImage = tkinter.PhotoImage(file="media/go_back_130x130.png")
prev_turn_icon: PhotoImage = tkinter.PhotoImage(file="media/prev_turn_100x100.png")
next_turn_icon: PhotoImage = tkinter.PhotoImage(file="media/next_turn_100x100.png")
delete_icon: PhotoImage = tkinter.PhotoImage(file="media/delete_icon_50x50.png")
# Main window - setup.
main_w.update_idletasks()
# Always position on center of the screen.
screen_width: int = main_w.winfo_screenwidth()
screen_height: int = main_w.winfo_screenheight()
main_w_width: int = 800
main_w_height: int = 600
main_w_start_x: int = screen_width // 2 - main_w_width // 2
main_w_start_y: int = screen_height // 2 - main_w_height // 2
# Working correctly with 800x600 as min for me to test with my Monitor.
main_w.geometry(f"{main_w_width}x{main_w_height}+{main_w_start_x}+{main_w_start_y}")
main_w.resizable(False, False)
main_w.iconphoto(True, icon)
main_w.title("TicTacToe")
main_w.config(
    padx=145,
    pady=45,
    background=main_w_background,
)
main_w.protocol("WM_DELETE_WINDOW", lambda: (menu(), main_w.destroy()))
# Tile buttons setup.
# Same 9 tiles, and using main window children widgets 0 -> 8 inclusive.
# First row.
tile_11: Button = Button(
    main_w,
    image=tile,
    highlightthickness=0,
    border=0,
    borderwidth=0,
    background=main_w_background,
    activebackground=main_w_background,
    relief=tkinter.RIDGE,
)
tile_11.grid(
    row=0,
    column=0,
)
tile_12: Button = Button(
    main_w,
    image=tile,
    highlightthickness=0,
    border=0,
    borderwidth=0,
    background=main_w_background,
    activebackground=main_w_background,
    relief=tkinter.RIDGE,
)
tile_12.grid(
    row=0,
    column=1,
)
tile_13: Button = Button(
    main_w,
    image=o_mark,
    highlightthickness=0,
    border=0,
    borderwidth=0,
    background=main_w_background,
    activebackground=main_w_background,
    relief=tkinter.RIDGE,
)
tile_13.grid(
    row=0,
    column=2,
)
# Second row.
tile_21: Button = Button(
    main_w,
    image=tile,
    highlightthickness=0,
    border=0,
    borderwidth=0,
    background=main_w_background,
    activebackground=main_w_background,
    relief=tkinter.RIDGE,
)
tile_21.grid(
    row=1,
    column=0,
)
tile_22: Button = Button(
    main_w,
    image=o_mark,
    highlightthickness=0,
    border=0,
    borderwidth=0,
    background=main_w_background,
    activebackground=main_w_background,
    relief=tkinter.RIDGE,
)
tile_22.grid(
    row=1,
    column=1,
)
tile_23: Button = Button(
    main_w,
    image=tile,
    highlightthickness=0,
    border=0,
    borderwidth=0,
    background=main_w_background,
    activebackground=main_w_background,
    relief=tkinter.RIDGE,
)
tile_23.grid(
    row=1,
    column=2,
)
# Third row.
tile_31: Button = Button(
    main_w,
    image=tile,
    highlightthickness=0,
    border=0,
    borderwidth=0,
    background=main_w_background,
    activebackground=main_w_background,
    relief=tkinter.RIDGE,
)
tile_31.grid(
    row=2,
    column=0,
)
tile_32: Button = Button(
    main_w,
    image=x_mark,
    highlightthickness=0,
    border=0,
    borderwidth=0,
    background=main_w_background,
    activebackground=main_w_background,
    relief=tkinter.RIDGE,
)
tile_32.grid(
    row=2,
    column=1,
)
tile_33: Button = Button(
    main_w,
    image=o_mark,
    highlightthickness=0,
    border=0,
    borderwidth=0,
    background=main_w_background,
    activebackground=main_w_background,
    relief=tkinter.RIDGE,
)
tile_33.grid(
    row=2,
    column=2,
)
# Not part of the start window. Hide.
hide_tiles()
# Replay button.
replay_button: Button = Button(
    main_w,
    image=replay_icon,
    highlightthickness=0,
    border=0,
    borderwidth=0,
    background=main_w_background,
    activebackground=main_w_background,
    relief=tkinter.RIDGE,
    command=lambda: (hide_tiles(), screenshot()),
)
replay_button.grid(
    row=1,
    column=3,
    padx=(15, 0)
)
# Not part of the start window. Hide.
replay_button.grid_remove()
# Go back to menu button.
go_back_button: Button = Button(
    main_w,
    image=go_back_icon,
    highlightthickness=0,
    border=0,
    borderwidth=0,
    background=main_w_background,
    activebackground=main_w_background,
    relief=tkinter.RIDGE,
    command=lambda: (hide_tiles(), screenshot(), menu())
)
go_back_button.grid(
    row=2,
    column=3,
    padx=(15, 0),
)
# Not part of the start window. Hide.
go_back_button.grid_remove()
# Start game with 2 players button.
start_button: Button = Button(
    main_w,
    image=start_icon,
    highlightthickness=0,
    border=0,
    borderwidth=0,
    background=main_w_background,
    activebackground=main_w_background,
    relief=tkinter.RIDGE,
    command=start_game,
)
start_button.grid(
    row=0,
    columnspan=2,
    padx=(30, 30),
)
# Start game vs computer button.
versus_button: Button = Button(
    main_w,
    image=versus_icon,
    highlightthickness=0,
    border=0,
    borderwidth=0,
    background=main_w_background,
    activebackground=main_w_background,
    relief=tkinter.RIDGE,
    command=lambda: start_game(ai=True),
)
versus_button.grid(
    row=1,
    column=1,
    sticky="e",
    pady=(10, 0),
    padx=(25, 0),
)
# History button.
history_button: Button = Button(
    main_w,
    compound="right",
    text="Played",
    font=("Helvetica", 15, "bold"),
    image=history_icon,
    highlightthickness=0,
    border=0,
    borderwidth=0,
    relief=tkinter.RIDGE,
    command=history,
    background=main_w_background,
    activebackground=main_w_background,
)
history_button.grid(
    row=1,
    column=0,
    sticky="w",
    pady=(10, 0),
)
# History window made as canvas on main_w.
history_label: Canvas = Canvas(
    main_w,
    width=525,
    height=520,
    background=main_w_background,
    border=0,
    borderwidth=0,
    highlightthickness=0,
)
history_label.grid(
    row=0,
    column=1,
    sticky="nsew",
)
history_label.grid_remove()
# History go back to menu button.
history_go_back_button: Button = Button(
    main_w,
    image=go_back_icon,
    highlightthickness=0,
    border=0,
    borderwidth=0,
    background=main_w_background,
    activebackground=main_w_background,
    relief=tkinter.RIDGE,
    command=menu,
)
history_go_back_button.grid(
    row=0,
    column=2,
    sticky="s",
)
# Not part of the start window. Hide.
history_go_back_button.grid_remove()
# History Combobox, dropbox with all games saved.
history_choose_game: ttk.Combobox = ttk.Combobox(
    main_w,
    width=12,
    justify="center",
    state="readonly",
    font=("Helvetica", 10, "bold"),
)
history_choose_game.option_add("*TCombobox*Listbox.Justify", "center")
history_choose_game.bind("<<ComboboxSelected>>", lambda event: (main_w.focus(), history_game_chosen()))
history_choose_game.grid(
    row=0,
    column=2,
    sticky="n",
)
# Not part of the start window. Hide.
history_choose_game.grid_remove()
# History: previous turn button.
history_prev_turn_button: Button = Button(
    main_w,
    image=prev_turn_icon,
    highlightthickness=0,
    border=0,
    borderwidth=0,
    background=main_w_background,
    activebackground=main_w_background,
    relief=tkinter.RIDGE,
    command=lambda: history_next_turn(back=True),
)
history_prev_turn_button.grid(
    row=0,
    column=0,
)
# Not part of the start window. Hide.
history_prev_turn_button.grid_remove()
# History: next turn button
history_next_turn_button: Button = Button(
    main_w,
    image=next_turn_icon,
    highlightthickness=0,
    border=0,
    borderwidth=0,
    background=main_w_background,
    activebackground=main_w_background,
    relief=tkinter.RIDGE,
    command=history_next_turn,
)
history_next_turn_button.grid(
    row=0,
    column=2,
    sticky="w",
)
# Not part of the start window. Hide.
history_next_turn_button.grid_remove()
# History: delete game button #
history_delete_button = Button(
    main_w,
    image=delete_icon,
    highlightthickness=0,
    border=0,
    borderwidth=0,
    background=main_w_background,
    activebackground=main_w_background,
    relief=tkinter.RIDGE,
    command=delete_history_game_chosen,
)
history_delete_button.grid(
    row=0,
    column=0,
    sticky="sw",
)
# Not part of the start window. Hide.
history_delete_button.grid_remove()

main_w.mainloop()

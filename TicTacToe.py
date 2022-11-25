import tkinter
from tkinter import *
import random
global PLAYER

def start_game():
    global PLAYER
    PLAYER = random.randint(1, 2)
    for button in main_w.winfo_children()[:9]:
        button.grid()
    for button in main_w.winfo_children()[9:]:
        button.grid_remove()


def tile_clicked(event):
    global PLAYER
    if event:
        if PLAYER == 1 and event.widget["text"] == "":
            event.widget["image"] = x_mark
            event.widget["text"] = "x"
            PLAYER += 1
        elif PLAYER == 2 and event.widget["text"] == "":
            event.widget["image"] = o_mark
            event.widget["text"] = "o"
            PLAYER -= 1








def hide_tiles():
    for widget in main_w.winfo_children()[:9]:
        widget["image"] = tile
        widget["text"] = ""
        widget.bind("<ButtonPress-1>", tile_clicked)
        widget.grid_remove()


main_w = Tk()
# media zone #
tile = tkinter.PhotoImage(file="media/tile_170x170.png.")
x_mark = tkinter.PhotoImage(file="media/x_mark_170x170.png")
o_mark = tkinter.PhotoImage(file="media/o_mark_170x170.png")
icon = tkinter.PhotoImage(file="media/ttt_icon.png")
start_icon = tkinter.PhotoImage(file="media/start_450x450.png")
history_icon = tkinter.PhotoImage(file="media/history_55x55.png")
versus_icon = tkinter.PhotoImage(file="media/vs_ai_155x96.png")
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
              pady=45,)
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

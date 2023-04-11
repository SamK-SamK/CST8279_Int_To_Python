"""
CST8279 - Final Python Project: Short Game Using Python 

Purpose:        This program is a single-player, user interactive, GUI-based "BINGO" game using the tkinter module.
Script Name:    CST8279_Final_Game.py
Created by:     Sam K
Date Created:   09/04/2023
Date Updated:   11/04/2023
Version:        2.4
"""

"""Modules"""
# Importing required modules.
import tkinter as tk
import random, os

"""Global Variables"""
# Text variable for initial text box display.
welcome_text = "CONTROLS\n\n"\
               "LEFT-CLICK   = Select\nRIGHT-CLICK  = Deselect\n"\
               "SCROLL WHEEL = Scroll Up or Down\n"\
               "BINGO?       = Check Bingo\n"\
               "QUIT!        = Exit Program\n"\
               "NEXT #       = Begin/Next Number\n\n"\
               "CALLED NUMBERS \n\n"

"""Lists"""
# BINGO letter list for "bingo_label" loop.
letter_list = ["B", "I", "N", "G", "O"]

# Random numbers generated for the bingo card - each session is different.
B_numbers = random.sample(range(1, 16), 5)
I_numbers = random.sample(range(16, 31), 5)
N_numbers = random.sample(range(31, 46), 5)
N_numbers[2] = "FREE"
G_numbers = random.sample(range(46, 61), 5)
O_numbers = random.sample(range(61, 76), 5)

# Adds selected random numbers to button grid in bingo card. 
number_list = [B_numbers,
               I_numbers,
               N_numbers,
               G_numbers,
               O_numbers]

# Master list for all the random numbers generated.
master_list = B_numbers + \
              I_numbers + \
              N_numbers + \
              G_numbers + \
              O_numbers

# Total range of all the numbers from 1 to 75 - called via "random_number_caller" function.
total_range_list = list(range(1, 76))

# After each number is called from "total_range_list", it is appended to this list.
removed_list = ["FREE"]

# Empty list to append which number user clicks.
click_list = []

# Lists of applicable bingos, based off of "master_list" index numbers.
b1_bingo = master_list[0:5]
i1_bingo = master_list[5:10]
n1_bingo = master_list[10:15]
g1_bingo = master_list[15:20]
o1_bingo = master_list[20:25]
b2_bingo = list(master_list[x] for x in (0, 5, 10, 15, 20))
i2_bingo = list(master_list[x] for x in (1, 6, 11, 16, 21))
n2_bingo = list(master_list[x] for x in (2, 7, 12, 17, 22))
g2_bingo = list(master_list[x] for x in (3, 8, 13, 18, 23))
o2_bingo = list(master_list[x] for x in (4, 9, 14, 19, 24))
d1_bingo = list(master_list[x] for x in (0, 6, 12, 18, 24))
d2_bingo = list(master_list[x] for x in (4, 8, 12, 16, 20))
c4_bingo = list(master_list[x] for x in (0, 4, 20, 24))

# Applicable bingos, concatinated into one master list - each list checked against "click_list".
master_bingo_list = [b1_bingo,
                     i1_bingo,
                     n1_bingo,
                     g1_bingo,
                     o1_bingo,
                     b2_bingo,
                     i2_bingo,
                     n2_bingo,
                     g2_bingo,
                     o2_bingo,
                     d1_bingo,
                     d2_bingo,
                     c4_bingo]

"""Functions"""
# Allows for left and right click functionality for the bingo "grid_button"s.
def grid_button_click():
    grid_button.bind("<Button-1>", left_click)
    grid_button.bind("<Button-2>", right_click)
    grid_button.bind("<Button-3>", right_click)

# If "grid_button" is left-clicked - change button to green, and add number to "click_list" if not present.
def left_click(event):
    event.widget.configure(bg="lightgreen", activebackground="lightgreen")
    clicked_number = event.widget.cget("text")
    if clicked_number in click_list:
        pass
    else:
        click_list.append(clicked_number)

# If "grid_button" is right-clicked - change button to original colour, and remove number from "click_list" if present.
def right_click(event):
    event.widget.configure(bg="white", activebackground="lightgrey")
    clicked_number = event.widget.cget("text")
    if clicked_number in click_list:
        click_list.remove(clicked_number)
    else:
        pass

# If "next_button" left-clicked - pull a random number from the "total_range_list", display it with applicable 
# letter in "called_tbox", append to "removed_list", removed from "total_range_list".
def random_number_caller():
    called_tbox.configure(state="normal")
    random_number = random.choice(total_range_list)
    if random_number in range(1, 16):
        letter_number = "B" + str(random_number)
    elif random_number in range(16, 31):
        letter_number = "I" + str(random_number)
    elif random_number in range(31, 46):
        letter_number = "N" + str(random_number)
    elif random_number in range(46, 61):
        letter_number = "G" + str(random_number)
    elif random_number in range(61, 76):
        letter_number = "O" + str(random_number)
    random_label["text"] = letter_number
    called_tbox.insert("end", letter_number + "   ")
    called_tbox.configure(state="disabled")
    removed_list.append(random_number)
    total_range_list.remove(random_number)

# If "bingo_button" left-clicked - check to see if "click_list" is part of "removed_list", if true evaluate bingo status 
# via "click_list" vs. "master_bingo_list". If "click_list" is a bingo, prompt to play again, else tell user no bingo. 
def bingo():
    winner_loser_list = []
    no_cheat = set(click_list).issubset(set(removed_list))
    if no_cheat is True:
        for bingos in master_bingo_list:
            winner_loser_list.append(set(bingos).issubset(set(click_list)))
            if any(winners is True for winners in winner_loser_list):
                random_label["text"] = "BINGO! :)"
                next_button.configure(text="Play Again!", command=restart)
            else:
                winner_loser_list = []
                random_label["text"] = "NO BINGO! :("
    else:
        random_label["text"] = "NO CHEATING!"

# If user has a bingo and wants to play again, restart the program.
def restart():
    window.destroy()
    bingo_file = str(os.path.abspath(os.path.abspath(__file__)))
    os.system('python "' + bingo_file + '"')

"""Main Program Body"""
# Build main window, and display window header.
window = tk.Tk()
frame = tk.Frame(window, padx=15, pady=15)
window.title("CST8729 Bingo: Just as Boring as The Real Thing!")

# Label to display numbers called from "total_range_list", and information on bingo status.
random_label = tk.Label(frame, text="", font="Courier 22 bold", width=2, height=2, relief="sunken", bg="white")
random_label.grid(row=0, column=1, columnspan=3, sticky="news", padx=5)

# Button to evaluate if user has a bingo.
bingo_button = tk.Button(frame, text="BINGO?", font="Courier 15", height=1, width=1, command=bingo)
bingo_button.grid(column=0, row=0, columnspan=1, sticky="news")

# Button to populate "random_label" with next number from "total_range_list".
next_button = tk.Button(frame, text="NEXT #", font="Courier 20", height=1, width=1, command=random_number_caller)
next_button.grid(column=0, row=1, columnspan=5, sticky="news")

# Button to quit program. 
quit_button = tk.Button(frame, text="QUIT!", font="Courier 15", height=1, width=1, command=quit)
quit_button.grid(column=4, row=0, columnspan=1, sticky="news")

# Text box to display initial "welcome_text" and numbers called from "total_range_list".
called_tbox = tk.Text(frame, height=10, width=15, font="Courier 14", wrap="word", state="normal")
called_tbox.insert("end", welcome_text)
called_tbox.configure(state="disabled")
called_tbox.grid(column=0, row=2, columnspan=5, sticky="news")

# Building the bingo label.
column = 0
row = 3
for letters in letter_list:
    bingo_label = tk.Label(frame, text=letters, font="Courier 25 bold", width=2, height=2)
    bingo_label.grid(row=row, column=column, sticky="news")
    column += 1

# Building the bingo number buttons from "number_list".
column = 0
for lists in number_list:
    row = 4
    for number in lists:
        frame.grid(column=column)
        grid_button = tk.Button(frame, text=number, height=3, width=5, font="Courier 18", bg="white")
        grid_button.grid(column=column, row=row, sticky="news")
        grid_button_click()
        row += 1
    column += 1

# Tkinter window loop for persistant GUI display. 
window.mainloop()

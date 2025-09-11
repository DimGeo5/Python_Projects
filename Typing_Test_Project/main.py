from tkinter import *
import time
import tkinter.font as tkFont
from random import shuffle
from Words_Dictionaries import easy_list, medium_list, hard_list
from Words_Dictionaries import state_dictionary as state


def easy():   # Choosing difficulty function which is bound with a tk Button
    shuffle(easy_list)
    state["typing_words"] = easy_list
    easy_button.place_forget()
    medium_button.place_forget()
    hard_button.place_forget()
    welcome_label.place_forget()
    intro()


def medium():      # Choosing difficulty function which is bound with a tk Button
    shuffle(medium_list)
    state["typing_words"] = medium_list
    easy_button.place_forget()
    medium_button.place_forget()
    hard_button.place_forget()
    welcome_label.place_forget()
    intro()


def hard():      # Choosing difficulty function which is bound with a tk Button. Shuffling words
    shuffle(hard_list)
    state["typing_words"] = hard_list
    easy_button.place_forget()
    medium_button.place_forget()
    hard_button.place_forget()
    welcome_label.place_forget()
    intro()


def intro():                   # Function that shows how to start the test
    text_entry.place(x=770, y=400)
    text_entry.insert(1.0, "Click in here to start")
    text_entry.config(state="disabled")
    main_window.bind('<Button-1>', start)


def clear_entry(event):      # Function that clears Entry widget every time a word is typed and 'space' is pressed
    typed_word = text_entry.get(1.0, END)
    state["typed_words"].append(typed_word)
    text_entry.delete(1.0, END)
    checking(typed_word)
    highlight_word(state["counter"])
    state["counter"] += 1


def start(event):           # Function that starts test
    text_entry.config(state="normal")
    main_window.bind('<space>', clear_entry)
    text_typing_words = " ".join(state["typing_words"])
    text_window.config(state="normal")
    text_window.delete(1.0, END)
    text_window.place(x=650, y=200)
    text_window.insert(END, text_typing_words)
    text_window.config(state="disabled")
    text_entry.delete(1.0, END)
    state["start_time"] = time.time()
    main_window.unbind('<Button-1>')
    highlight_word(0)


def stop():          # Function that stops the test
    main_window.unbind('<space>')
    text_window.place_forget()
    text_entry.place_forget()
    score_checking()


def highlight_word(list_index):       # Function that highlights each word that must be copied
    try:
        word = state["typing_words"][list_index]
        state["start_index"] = text_window.search(word, 1.0, stopindex="end")
        if state["start_index"]:
            text_window.see(state["start_index"])
            state["end_index"] = f"{state['start_index']} + {len(word)}c"
            text_window.tag_add(state["tag_name"], state["start_index"], state["end_index"])
            text_window.tag_config(state["tag_name"], background="orange")
    except IndexError:
        stop()           # When out of words test is finished


def checking(typed_word):        # Function that indicates if each word copied correctly or not
    a = state["typing_words"][state["counter"]-1].lower()
    b = typed_word.strip()
    if a == b:
        text_window.tag_add(state["correct_tag"], state["start_index"], state["end_index"])
        text_window.tag_config(state["correct_tag"], background="green")
        state["score"] += 1
    else:
        text_window.tag_add(state["false_tag"], state["start_index"], state["end_index"])
        text_window.tag_config(state["false_tag"], background="red")
        state["mistakes_words"].append(b)
        state["correct_word"].append(a)


def score_checking():            # Function that checks the score of the test and shows it
    state["stop_time"] = time.time()
    elapsed_time = int(state["stop_time"] - state["start_time"])
    wpm = (60 * len(state["typed_words"])) / elapsed_time
    correct_percentage = (len(state["typing_words"]) - len(state["mistakes_words"])) / len(state["typing_words"])
    final_score = wpm * correct_percentage
    test_result.place(x=530, y=200)
    test_result.delete("1.0", END)
    if state["score"] == len(state["typing_words"]):
        test_result.insert("1.0", f"Congratulations, you typed all words correctly\n")
        test_result.insert("2.0", f"Your score is {final_score}w.p.m.")
    else:
        test_result.insert("1.0", f"You made some mistakes!\n")
        i = 0
        z = 0
        try:
            while i >= 0:
                z = i + 2
                if state["mistakes_words"][i] == "":
                    state["mistakes_words"][i] = "'Nothing'"
                test_result.insert(f"{z}.0", f"Instead of {state['correct_word'][i]} you typed {state['mistakes_words'][i]}\n")
                i += 1
        except IndexError:
            pass
        test_result.insert(f"{z + 1}.0", f"Your score is {int(wpm)}w.p.m. * {int(correct_percentage*100)}% = "
                                         f"{int(final_score)}w.p.m.\n")
    reset_button.place(x=930, y=700)      # Placing a button to start again


def new_test():        # Function that initialises some variables and checks if it is the first time called or not
    try:
        reset_button.place_forget()
        test_result.place_forget()
        welcome_label.place(x=770, y=290)
        easy_button.place(x=820, y=370)
        medium_button.place(x=920, y=370)
        hard_button.place(x=1020, y=370)
        state["typing_words"] = []
        state["typed_words"] = []
        state["counter"] = 1
        state["start_index"] = ""
        state["end_index"] = ""
        state["tag_name"] = "highlight"
        state["correct_tag"] = "green"
        state["false_tag"] = "red"
        state["score"] = 0
        state["start_time"] = time.time()
        state["stop_time"] = time.time()
        state["mistakes_words"] = []
        state["correct_word"] = []
    except NameError:
        test_result.place_forget()
        welcome_label.place(x=770, y=290)
        easy_button.place(x=820, y=370)
        medium_button.place(x=920, y=370)
        hard_button.place(x=1020, y=370)


'''Initialising tk widgets'''
main_window = Tk()

main_window.state("zoomed")

font_style = tkFont.Font(size=30)

test_result = Text(main_window, width=40, height=10, font=font_style, wrap="word")

welcome_label = Label(main_window, text="Choose your difficulty", font=font_style)

easy_button = Button(main_window, text="Easy", width=10, height=5, borderwidth=5, command=easy)

medium_button = Button(main_window, text="Medium", width=10, height=5, borderwidth=5, command=medium)

hard_button = Button(main_window, text="Hard", width=10, height=5, borderwidth=5, command=hard)

text_window = Text(main_window, width=30, height=2, font=font_style, wrap="word")


text_entry = Text(main_window, width=20, height=2, font=font_style)


reset_button = Button(main_window, text="Reset", width=10, height=5, borderwidth=5, command=new_test)

new_test()

main_window.mainloop()

# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 15:23:30 2020

@author: singh
"""

from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
from pygame import mixer
import os
from mutagen.mp3 import MP3
import threading
import time
from tkinter import ttk

mixer.init()
root=Tk()
root.configure(bg='dodger blue')
root.geometry('500x300')
root.title("Melody")
root.iconbitmap(r'C:\Users\singh\PycharmProjects\music player\Images\music.ico')

statusbar = Label(root, text="Welcome to Melody", relief=SUNKEN, anchor=W)
statusbar.pack(side=BOTTOM, fill=X)

# Create menu
menubar = Menu(root)
root.config(menu=menubar)

playlist = []

def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)

def add_to_playlist(filename):
    filename = os.path.basename(filename)
    index = 0
    playlistbox.insert(index, filename)
    playlist.insert(index, filename_path)
    index += 1

# Create the submenu
subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open")
subMenu.add_command(label="Exit",command=root.destroy)

def about_us():
    tkinter.messagebox.showinfo('About Melody', 'This is a music player build using Python Tkinter by @ssbrar')

subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About Us", command=about_us)



leftframe = Frame(root,bg='dodger blue')
leftframe.pack(side=LEFT, padx=30)

playlistbox = Listbox(leftframe)
playlistbox.pack()

addbtn = Button(leftframe, text="+ Add", command=browse_file)
addbtn.pack(side=LEFT, padx=10)

def del_song():
    selected_song = playlistbox.curselection()
    selected_song = int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)

delbtn = Button(leftframe, text="- Del", command=del_song)
delbtn.pack(side=LEFT, padx=10)

rightframe = Frame(root,bg='dodger blue')
rightframe.pack()

topframe = Frame(rightframe,bg='dodger blue')
topframe.pack()

filelabel = Label(topframe, text='Lets make some noise!',font='Helvetica 10 bold',bg='dodger blue',fg='white')
filelabel.pack(pady=10)

lengthlabel = Label(topframe, text='Total Length : --:--',font='Helvetica 10 bold',bg='dodger blue',fg='white')
lengthlabel.pack(pady=10)

currenttimelabel = Label(topframe, text='Current Time : --:--', relief=GROOVE,font='Helvetica 10 bold',bg='dodger blue',fg='white')
currenttimelabel.pack()

def show_details(play_song):
    file_data = os.path.splitext(play_song)
    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()
    # div - total_length/60, mod - total_length % 60
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthlabel['text'] = "Total Length" + ' - ' + timeformat
    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()

def start_count(t):
    global paused
    # mixer.music.get_busy(): - Returns FALSE when we press the stop button (music stop playing)
    # Continue - Ignores all of the statements below it. We check if music is paused or not.
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currenttimelabel['text'] = "Current Time" + ' - ' + timeformat
            time.sleep(1)
            current_time += 1

def play_music():
    global paused
    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music Resumed"
        paused = FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = "Playing music" + ' - ' + os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror('File not found', 'Melody could not find the file. Please check again.')


def stop_music():
    mixer.music.stop()

paused=FALSE

def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Music Paused"

def rewind_music():
    play_music()
    statusbar['text'] = "Music Rewinded"

def set_vol(val):
    volume = int(val) / 100
    mixer.music.set_volume(volume)

muted = FALSE

def mute_music():
    global muted
    if muted:  # Unmute the music
        mixer.music.set_volume(70)
        volumeBtn.configure(image=volumePhoto)
        scale.set(70)
        muted = FALSE
    else:  # mute the music
        mixer.music.set_volume(0)
        volumeBtn.configure(image=mutePhoto)
        scale.set(0)
        muted = TRUE

middleframe = Frame(rightframe,bg='dodger blue')
middleframe.pack(padx=10,pady=10)

Playphoto = PhotoImage(file=r'C:\Users\singh\PycharmProjects\music player\Images\play.png')
Playbtn = Button(middleframe, image=Playphoto, command=play_music)
Playbtn.grid(row=0, column=0, padx=10)

stopPhoto = PhotoImage(file=r'C:\Users\singh\PycharmProjects\music player\Images\stop.png')
stopBtn = Button(middleframe, image=stopPhoto, command=stop_music)
stopBtn.grid(row=0, column=1, padx=10)

pausePhoto = PhotoImage(file=r'C:\Users\singh\PycharmProjects\music player\Images\pause.png')
pauseBtn = Button(middleframe, image=pausePhoto, command=pause_music)
pauseBtn.grid(row=0, column=2, padx=10 )

bottomframe = Frame(rightframe,bg='dodger blue')
bottomframe.pack()

rewindPhoto = PhotoImage(file=r'C:\Users\singh\PycharmProjects\music player\Images\rewind.png')
rewindBtn = Button(bottomframe, image=rewindPhoto, command=rewind_music)
rewindBtn.grid(row=0,column=0)

mutePhoto = PhotoImage(file=r'C:\Users\singh\PycharmProjects\music player\Images\mute.png')
volumePhoto = PhotoImage(file=r'C:\Users\singh\PycharmProjects\music player\Images\speaker.png')
volumeBtn = Button(bottomframe, image=volumePhoto, command=mute_music)
volumeBtn.grid(row=0, column=3)

scale = Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(70)
mixer.music.set_volume(70)
scale.grid(row=0, column=2, padx=10)

def on_closing():
    stop_music()
    root.destroy()

root.protocol("WM_WINDOW_DELETE", on_closing)
root.mainloop()
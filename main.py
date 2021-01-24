import os
import youtube_dl
import tkinter as tk
from tkinter import filedialog

#defaults
PATH = os.getcwd()
link = ""

#window setup
window = tk.Tk()
window.title("Music Scrape")
window.geometry("200x150")

#Path Frame setup
frmPath = tk.Frame(master=window)
pathLabel = tk.Label(
    master=frmPath,
    text="Place to save to"
)
pathLabel.grid(row=0, column=1)
pathButton = tk.Button(
    master=frmPath,
    text="..."
)
pathButton.grid(row=1, column=2)
path = tk.Entry(master=frmPath)
path.grid(row=1, column=1)
path.insert(0, PATH)

#Playlist Frame Setup
frmPlaylist = tk.Frame(master=window)
playlistLabel = tk.Label(
    master=frmPlaylist,
    text="Playlist Link"
)
playlistLabel.grid(row=0, column=1)
playlist = tk.Entry(master=frmPlaylist)
playlist.grid(row=1, column=1)
submitButton = tk.Button(
    master=frmPlaylist,
    text="Download"
)
submitButton.grid(row=1, column=2)

#status hooks
#frmHooks = tk.Frame(master=window)
#statusLabel = tk.Label(
    #master=frmHooks,
    #text="Status:"
#)
#statusLabel.grid(row=0, column=1)

#hooks
#def hooks(d):
    #if d['status'] == 'downloading':
        #statusLabel['text']="downloading "+ str(round(float(d['downloaded_bytes'])/float(d['total_bytes'])*100,1))+"%"
    #if d['status'] == 'finished':
        #filename=d['filename']
        #statusLabel.config(text=filename)
        
        

#path onclick handler
def getPath(context):
    path.delete(0, tk.END)
    PATH=os.getcwd()
    tempdir = tk.filedialog.askdirectory(parent=window, initialdir=PATH, title='Please select a directory to save your files to')
    if len(tempdir) > 0:
        PATH = tempdir
        path.insert(0, PATH)
        os.chdir(PATH)

#download on click handler
def dl(context):
    link = playlist.get()
    print(link)
    ydl = youtube_dl.YoutubeDL(
        {   
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': '%(title)s.%(ext)s',
            'download_archive': 'archive.txt',
            #'progress_hooks': [hooks]
        }
    )
    with ydl:
        ydl.download([link])

#button binds
pathButton.bind("<Button-1>", getPath)
submitButton.bind("<Button-1>", dl)

#grid setup
frmPath.grid(row=0, column=1)
frmPlaylist.grid(row=1, column=1)
#frmHooks.grid(row=2, column=1)
window.mainloop() 
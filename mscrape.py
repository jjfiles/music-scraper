import os
import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Progressbar
import configparser
import youtube_dl

#defaults
PATH = os.getcwd()
link = ""
inc = 1
config = configparser.ConfigParser()

if not os.path.exists('scraper.ini'):
    config['DEFAULT'] = {
        'path': PATH
    }
    with open('scraper.ini', 'w') as f:
        config.write(f)
 
else:
    config.read('scraper.ini')
    PATH = config['DEFAULT']['path']
    os.chdir(PATH)

#hooks
def hooks(d):
    if d['status'] == 'downloading':
        #update status label to reflect download % and force update tkinter window
        try:
            statusLabel['text'] = "Status:\ndownloading "+ str(round(float(d['downloaded_bytes'])/float(d['total_bytes'])*100,1))+"%"
            window.update()
            
        #if bytes not available display so
        except KeyError:
            statusLabel['text'] = "Status:\ndownloading but total bytes unavailable..."
            window.update()
    if d['status'] == 'finished':
        filename=d['filename']
        #update prgress bar and status label values after a video is finished
        bar['value'] += inc
        total = str(round(bar['value']))
        statusLabel['text'] = "Finished:\n" + str(filename) + "\n" + total + "% / 100%"
        window.update()

#path onclick handler
def getPath():
    global PATH
    #select new path
    tempdir = tk.filedialog.askdirectory(parent=window, initialdir=PATH, title='Please select a directory to save your files to')

    #if not null and not the same as the old path, update the tkinter entry, save the new path and change directory
    if len(tempdir) > 0 and tempdir != PATH:
        path.delete(0, tk.END)
        PATH = tempdir
        path.insert(0, PATH)
        config['DEFAULT']['path'] = PATH
        with open('scraper.ini', 'w') as f:
            config.write(f)
        os.chdir(PATH)

#download onclick handler
def dl():
    # reset tkinter values if downloading more
    bar['value'] = 0
    statusLabel['text'] = "Press 'Download' to begin..."
    
    #get playlist link from tkinter
    link = playlist.get()
    
    #set youtube dl options
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
            'progress_hooks': [hooks],
            'quiet': True,
        }
    )
    with ydl:
        #check if archive file has already been made. if not, create one
        if not os.path.exists('archive.txt'):
            f = open('archive.txt', 'x')
            f.close()
            
        #get playlist metadata and determine number of entries
        meta = ydl.extract_info(link, download=False)
      
        global inc
        #if the link is not a playlist set the increment percentage to 100 / the number of entries
        try:
            entries = len(meta['entries'])
            if entries != 0:
                inc = 100 / entries
        
            #read through the archive file to see if any entries have already been downloaded
            with open('archive.txt') as f:
                for video in meta['entries']:
                    if not video:
                        print("ERROR: Unable to retreive info. Continuing...")
                        continue
                    
                    #if so decrement the number of entries being downloaded
                    if video['id'] in f.read():
                        entries -= 1
                        
        #otherwise just increment the entire 100%
        except KeyError:
            inc = 100
            entries = 1
        
        
        
        
        #begin download and force tkinter update after/
        ydl.download([link])
        window.update()



#window setup
window = tk.Tk()
window.title("Music Scrape")
window.geometry("475x190")

#Path Frame setup
frmPath = tk.Frame(master=window)
pathLabel = tk.Label(
    master=frmPath,
    text="Place to save to",
    justify="center",
    anchor="center"
)
pathButton = tk.Button(
    master=frmPath,
    text="...",
    command=getPath
)
path = tk.Entry(master=frmPath)
path.grid(row=1, column=1, sticky="")
pathLabel.grid(row=0, column=1, sticky="", padx=(5, 5))
pathButton.grid(row=1, column=2, sticky="", padx=(5, 5))
path.insert(0, PATH)

#Playlist Frame Setup
frmPlaylist = tk.Frame(master=window)
playlistLabel = tk.Label(
    master=frmPlaylist,
    text="Playlist Link",
    justify="center",
    anchor="center"
)
playlist = tk.Entry(master=frmPlaylist)
submitButton = tk.Button(
    master=frmPlaylist,
    text="Download",
    command=dl,
)
playlist.grid(row=1, column=1, sticky="")
playlistLabel.grid(row=0, column=1, sticky="", padx=(5, 5))
submitButton.grid(row=1, column=2, sticky="", padx=(5, 5))

#status hooks
frmHooks = tk.Frame(master=window)
statusLabel = tk.Label(
    master=frmHooks,
    text="Press 'Download' to begin..."
)
bar = Progressbar(
    frmHooks,
    length = 100,
    mode = 'determinate'
)
statusLabel.grid(row=0, column=1, sticky="")
bar.grid(row=1, column=1, sticky="")

#grid setup
frmPath.grid(row=0, column=1)
frmPlaylist.grid(row=1, column=1)
frmHooks.grid(row=2, column=1)
window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(3, weight=1)
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(3, weight=1)
window.mainloop() 
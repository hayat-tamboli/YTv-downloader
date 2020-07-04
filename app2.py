from pytube import YouTube
import tkinter as tk
from tkinter import ttk
import threading


# main application shows:
# label Loading..
# label which configure values when file is downloading 
# inderterminate progress bar
class MainApplication(tk.Frame):

    def __init__(self, master=None, *args, **kwargs):
        tk.Frame.__init__(self, master)
        self.master = master

        self.master.grid_rowconfigure(0, weight=0)
        self.master.grid_columnconfigure(0, weight=1)

        self.youtubeEntry = "https://www.youtube.com/watch?v=kLZuut1fYzQ"
        self.FolderLoacation = "C:/Users/Asus/Desktop/ytdownloads"

        # pytube
        self.yt = YouTube(self.youtubeEntry)

        video_type = self.yt.streams.filter(only_audio = True).first()

        # file size of a file
        self.MaxfileSize = video_type.filesize

        # Loading label
        self.loadingLabel = ttk.Label(self.master, text="Loading...", font=("Agency FB", 30))
        self.loadingLabel.grid(pady=(100,0))

        # loading precent label which must show % donwloaded
        self.loadingPercent = tk.Label(self.master, text="0", fg="green", font=("Agency FB", 30))
        self.loadingPercent.grid(pady=(30,30))

        # indeterminate progress bar
        self.progressbar = ttk.Progressbar(self.master, orient="horizontal", length=500, mode='indeterminate')
        self.progressbar.grid(pady=(50,0))
        self.progressbar.start()    

        threading.Thread(target=self.yt.register_on_progress_callback(self.show_progress_bar)).start()

        # call Download file func
        threading.Thread(target=self.DownloadFile).start()



    def DownloadFile(self):


        self.yt.streams.filter(progressive=True).first().download(self.FolderLoacation)

    # func count precent of a file
    def show_progress_bar(self, stream=None, chunk=None, file_handle=None, bytes_remaining=1):

        # loadingPercent label configure value %
        self.loadingPercent.config(text=str(int(100 - (100*(bytes_remaining/self.MaxfileSize)))))


root = tk.Tk() 
root.title("Youtube downloader")
root.geometry("1920x1080")
app = MainApplication(root)
root.mainloop()
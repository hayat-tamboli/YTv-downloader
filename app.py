# author: Hayat Tamboli
import datetime
import speedtest
from pytube import YouTube
import tkinter as tk
from tkinter import ttk
import time
from pytube.cli import on_progress
import threading
from PIL import ImageTk, Image
import os
import requests
from io import BytesIO
from tkinter import filedialog
# from urllib.request import urlopen
# import io
# import base64
# test https://www.youtube.com/watch?v=YXPyB4XeYLA


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(padx=20, pady=20)
        self.create_widgets()

    def create_widgets(self):

        self.URL_request = tk.Label(
            self, text="Enter a youtube URL:⌨️ ", font=("Agency FB", 20))
        self.URL_request.grid(row=0, column=0)

        self.URL_input = tk.Entry(self)
        self.URL_input.grid(row=0, column=1, ipadx=50, ipady=3)
        self.get_details = tk.Button(
            self, text="Get details", command=self.getDetails, bg="white", font=("Helvetica", 10))
        self.get_details.grid(row=0, column=2, ipadx=5, ipady=5, padx=10)

        self.exit = tk.Button(self, text="Exit", fg="red", bg="white", font=("Helvetica", 10),
                              command=self.master.destroy)
        self.exit.grid(row=0, column=3, ipadx=5, ipady=5, padx=10)
        self.master.title("YouTube video downloader🔻")
        self.video_progressbar = ttk.Progressbar(
            self, length=300, mode='indeterminate')
        threading.Thread(target=self.getDataSpeed).start()
        self.button_explore = tk.Button(self,  
                        text = "Browse Files", 
                        command = self.browseFiles) 
        self.button_explore.grid(column = 2) 
        # self.master.iconbitmap('youtube.ico')
        self.master.minsize(1000, 400)

    def getDetails(self):
        try:
            yt = YouTube(self.URL_input.get(),
                         on_progress_callback=on_progress)
            # yt.prepare()
        except:
            self.err = tk.Label(self, text="ERROR EXIT AND RETRY",
                                fg="red", font=("Helvetica", 40))
            self.err.grid(row=2, column=1)
        else:
            conversion = datetime.timedelta(seconds=yt.length)
            converted_time = str(conversion)
            # image_url = yt.thumbnail_url
            # response = requests.get(image_url)
            # img_data = response.content
            # img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
            # self.panel = tk.Label(root, image=img)
            # self.panel.pack(side="bottom", fill="both", expand="yes")

            self.desc = tk.Label(self, font=("Helvetica", 15))
            self.desc["text"] = "name=> " + \
                str(yt.title) + "\nlength of video=> " + \
                converted_time + "\nviews=> " + str(yt.views)
            self.desc.grid(row=3, column=2)
            self.check_options = tk.Button(
                self, text="Check options", font=("Helvetica", 10), fg="green", bg="white", command=lambda: self.checkOptions(yt))
            self.check_options.grid(row=4, column=2, ipadx=5, ipady=5, padx=10)

    def checkOptions(self, yt):
        videos = yt.streams.filter(progressive=True).all()
        s = 1
        for v in videos:
            self.option = tk.Label(self, font=("Helvetica", 15), text=str(
                s)+". "+str(v.resolution)).grid(row=s, column=1)
            s += 1

        self.input_option = tk.Entry(self)
        self.input_option.grid(row=s, column=1, ipady=3)
        self.opt_select = tk.Button(
            self, font=("Helvetica", 15), text="Download", bg="white", command=lambda: self.download(videos))
        self.opt_select.grid(row=s+1, column=1, ipadx=5, ipady=5, padx=10)

    def download(self, videos):
        # self.video_progressbar.start(100)
        # self.video_progressbar.grid(column=1)
        self.master.title("downloading")
        vid = videos[int(self.input_option.get())-1]
        self.filesize = tk.Label(
            self, text=str(self.bytesto(vid.filesize, 'm')) + " MB", font=("Helvetica", 20)).grid(column=1)
        vid.download(str(self.folder_selected))
        self.dnld_complete = tk.Label(
            self, text="DOWNLOAD COMPLETED 😀👍", font=("Helvetica", 30)).grid()
        # self.video_progressbar.stop()
        self.master.title("Download complete! 👍")

    def browseFiles(self):
        self.folder_selected = filedialog.askdirectory()
        self.folder_label = tk.Label(text = self.folder_selected)
        self.folder_label.pack()

    def bytesto(self, bytes, to, bsize=1024):
        """convert bytes to megabytes, etc.
            sample code:
           print('mb= ' + str(bytesto(314575262000000, 'm')))
            sample output: 
           mb= 300002347.946
        """
        a = {'k': 1, 'm': 2, 'g': 3, 't': 4, 'p': 5, 'e': 6}
        r = float(bytes)
        for i in range(a[to]):
            r = r / bsize
        r = round(r, 1)
        return(r)

    def getDataSpeed(self):
        # speed test
        st = speedtest.Speedtest()
        self.speed_label = tk.Label(
            self, text="download speed=>"+str(round(self.bytesto(st.download(), 'k')/10, 1))+"kb/s")
        self.speed_label.grid(row=1, column=0)

    def start(self):
        self.video_progressbar.start(10)


root = tk.Tk()
app = Application(master=root)
app.mainloop()

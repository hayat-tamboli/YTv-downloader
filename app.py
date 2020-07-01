# author: Hayat Tamboli
import datetime
# import speedtest
from pytube import YouTube
import tkinter as tk
from pytube.cli import on_progress

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
        # self.master.iconbitmap('youtube.ico')
        self.master.minsize(600, 400)

    def getDetails(self):
        try:
            yt = YouTube(self.URL_input.get(),
                         on_progress_callback=on_progress)
            # self.getDataSpeed()
        except:
            self.err = tk.Label(self, text="ERROR EXIT AND RETRY",
                                fg="red", font=("Helvetica", 50))
            self.err.grid(row=2, column=2)
        else:
            conversion = datetime.timedelta(seconds=yt.length)
            converted_time = str(conversion)

            self.desc = tk.Label(self, font=("Helvetica", 15))
            self.desc["text"] = "name=> " + \
                str(yt.title) + "\nlength of video=> " + \
                converted_time + "\nviews=> " + str(yt.views)
            self.desc.grid(row=2, column=2)
            self.check_options = tk.Button(
                self, text="Check options", font=("Helvetica", 10), fg="green", bg="white", command=lambda: self.checkOptions(yt))
            self.check_options.grid(row=3, column=2, ipadx=5, ipady=5, padx=10)

    def checkOptions(self, yt):

        # print("downloading")
        videos = yt.streams.filter(progressive=True).all()

        s = 1
        for v in videos:
            self.option = tk.Label(self, font=("Helvetica", 15), text=str(
                s)+". "+str(v.resolution)).grid(row=s, column=1)
            # print(str(s)+". "+str(v))
            s += 1
        self.input_option = tk.Entry(self)
        self.input_option.grid(row=s, column=1, ipady=3)
        self.opt_select = tk.Button(
            self, font=("Helvetica", 15), text="Download", bg="white", command=lambda: self.download(videos))
        self.opt_select.grid(row=s+1, column=1, ipadx=5, ipady=5, padx=10)

    def download(self, videos):
        self.master.title("downloading")
        vid = videos[int(self.input_option.get())-1]
        vid.download("C:/Users/Asus/Desktop/ytdownloads")
        self.dnld_complete = tk.Label(
            self, text="DOWNLOAD COMPLETED 😀👍", font=("Helvetica", 30)).grid(column=1)

    def browseFiles(self):
        filename = tk.filedialog.askopenfilename(
            initialdir="/", title="Select a File", filetypes=(("all files", "*.*")))
        self.label_file_explorer.configure(text="File Opened: "+filename)

    # def getDataSpeed(self):
    #     # speed test
    #     st = speedtest.Speedtest()
    #     self.speed_label = tk.Label(
    #         self, text="download speed=>"+str(round(st.download() / 10000, 2))+"kb/s")
    #     self.speed_label.grid(row=1, column=0)


root = tk.Tk()
app = Application(master=root)
app.mainloop()

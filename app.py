import datetime
from pytube import YouTube


URL = input("Enter a youtube URL: ")
yt = YouTube(URL)
print('name=>', yt.title)

conversion = datetime.timedelta(seconds=yt.length)
converted_time = str(conversion)
print('length of video=>', converted_time)
print('views=>', yt.views)

choice = input("want to download:[Y]/[N]: ")
if(choice == "Y" or choice == "y"):
    stream = yt.streams.first()
    stream.download("C:/Users/Asus/Desktop/ytdownloads")
    print("DOWNLOAD COMPLETED :)")
else:
    exit()

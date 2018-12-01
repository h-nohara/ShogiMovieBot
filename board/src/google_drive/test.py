import os, sys
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.CommandLineAuth()
drive = GoogleDrive(gauth)

folder_id = "1cTnFkxo0QkG02_3saDWMqObVhS6D6M3f"


def upload_movie(fname, basename):

    ext = fname.split(".")[-1]
    mine_type = "audio/mp4"

    f = drive.CreateFile({
        'title': basename,
        'mimeType': mine_type,
        'parents': [{'kind': 'drive#fileLink', 'id':folder_id}]
    })

    f.SetContentFile(fname)
    f.Upload()
    print("success : upload movie : {}".format(fname))
    


if __name__ == "__main__":

    fname = "/Users/nohara/Desktop/スクリーンショット 2018-07-25 2.03.42.png"

    ext = fname.split(".")[-1]

    if (ext == "png") or (ext == "PNG"):
        mine_type = "image/png"

    elif (ext == "jpg") or (ext == "jpeg"):
        mine_type = "image/jpeg"

    f = drive.CreateFile({
        'title': 'hoge/test.jpg',
        'mimeType': mine_type,
        'parents': [{'kind': 'drive#fileLink', 'id':folder_id}]
        })

    f.SetContentFile(fname)
    f.Upload()

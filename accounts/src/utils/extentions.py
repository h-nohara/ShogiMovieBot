

# image
ExtList_jpeg = ["jpg", "jpeg", "JPG", "JPEG"]
ExtList_png = ["png", "PNG"]

ExtList_image = ExtList_jpeg + ExtList_png

# movie
ExtList_mp4 = ["mp4", "MP4"]

ExtList_movie = ExtList_mp4



def get_normalized_ext(ext, restriction=None):

    '''
    条件に合う拡張子ではなかったら、Noneを返す

    restriction : "image" or "movie"

    >>> get_normalized_ext("JPEG")
    "jpg"
    >>> get_normalized_ext("JPEG", restriction="movie")
    None
    '''

    # 拡張子のマッチング

    if ext in ExtList_jpeg:
        normalized_ext = ExtList_jpeg[0]

    elif ext in ExtList_png:
        normalized_ext = ExtList_png[0]

    elif ext in ExtList_mp4:
        normalized_ext = ExtList_mp4[0]

    else:
        return None

    # 制限の確認

    if restriction == "image":
        if normalized_ext not in ExtList_image:
            return None

    elif restriction == "movie":
        if normalized_ext not in ExtList_movie:
            return None

    return normalized_ext

import os, sys, glob2
from ShogiMovieBot.settings import BASE_DIR

# api
from accounts.src.utils.generate_fname import generate_basename
from accounts.src.utils import bucket, fname_cloud, upload_file


# db
from bot.models.kifu_movie import KifuMovie


def register_kifu_movies(dirname):

    movies = glob2.glob(os.path.join(dirname, "*.mp4"))
    print(movies)

    for i, movie in enumerate(movies):

        print(i)
        print(movie)

        key = generate_basename("kifumovie{}".format(i), "mp4")

        # アップロード
        upload_file(bucket, movie, key)

        # dbに登録
        record_KifuMovie = KifuMovie(path=fname_cloud(key), opening="四間飛車")
        record_KifuMovie.save()


if __name__ == "__main__":

    dirname = os.path.join(BASE_DIR, "bot/static/kifu_movies/四間飛車_packed_up")
    register_kifu_movies(dirname)
    print("all finished")

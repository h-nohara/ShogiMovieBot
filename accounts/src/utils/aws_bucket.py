
import os, sys
import boto3

# バケット名
AWS_S3_BUCKET_NAME = "shogi-movie-bot"
s3 = boto3.resource('s3')
bucket = s3.Bucket(AWS_S3_BUCKET_NAME)


def fname_cloud(basename):

    if (basename == "") or (basename is None):
        return None
        
    fname_cloud = os.path.join("https://s3-ap-northeast-1.amazonaws.com", AWS_S3_BUCKET_NAME, basename)
    return fname_cloud


def check_exists(bucket, key):

    if (key is None) or (key == ""):
        return False
    
    files = bucket.objects.filter(Prefix=key)
    files = [f for f in files]
    
    if len(files) > 0:
        return True
    else:
        return False


def copy_file(original_key, result_key):
    
    if check_exists(bucket, original_key):
        new_obj = bucket.Object(result_key)
        ret = new_obj.copy_from(CopySource={'Bucket': bucket.name, 'Key': original_key})

        return True

    else:
        return False


def delete_file(bucket, key, exist_check=True):

    if exist_check:
        if check_exists(bucket, key):
            obj = bucket.Object(key)
            obj.delete()

    else:
        obj = bucket.Object(key)
        obj.delete()


def ext2ContentType(ext):
    
    # image
    if (ext == "png") or (ext == "PNG"):
        return "image/png"
    elif (ext == "jpg") or (ext == "jpeg") or (ext == "JPG") or (ext == "JPEG"):
        return "image/jpeg"

    # movie
    elif (ext == "mp4") or (ext == "MP4"):
        return "audio/mp4"

    else:
        return None


def upload_file(bucket, fname, key):

    ext = fname.split(".")[-1]
    content_type = ext2ContentType(ext)
    bucket.upload_file(fname, key, ExtraArgs={"ContentType": content_type})
    print("uploaded : {}".format(fname_cloud(key)))
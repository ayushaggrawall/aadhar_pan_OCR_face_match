import boto3
import hashlib
import datetime
from storage.config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, REGION_NAME, BUCKET


def hash_input(images):
    m = str(images).encode("utf-8")
    m = hashlib.md5(m)
    mdpass = m.hexdigest()
    return mdpass


def upload_s3(images, bucket=BUCKET):
    """
    Upload File to S3
    """

    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=REGION_NAME,
    )

    s3 = session.resource("s3")
    bucket = s3.Bucket(BUCKET)
    with open(images, "rb") as data:
        key_img = hash_input(images + str(datetime.datetime.now()))
        bucket.put_object(Key=key_img, ACL="public-read", Body=data)


#MODIFY BELOW ACCORDING TO YOUR S3 BUCKET NAME
    #return "http://'''S3 BUCKET NAME OVER HERE'''.s3.amazonaws.com/" + str(key_img), str(key_img)

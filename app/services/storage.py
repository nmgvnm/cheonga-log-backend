import os
import uuid
import base64
import boto3
from botocore.exceptions import ClientError

R2_ACCOUNT_ID = os.getenv("R2_ACCOUNT_ID", "")
R2_ACCESS_KEY_ID = os.getenv("R2_ACCESS_KEY_ID", "")
R2_SECRET_ACCESS_KEY = os.getenv("R2_SECRET_ACCESS_KEY", "")
R2_BUCKET_NAME = os.getenv("R2_BUCKET_NAME", "")
R2_PUBLIC_URL = os.getenv("R2_PUBLIC_URL", "").rstrip("/")

s3 = boto3.client(
    "s3",
    endpoint_url=f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com",
    aws_access_key_id=R2_ACCESS_KEY_ID,
    aws_secret_access_key=R2_SECRET_ACCESS_KEY,
    region_name="auto",
)


def upload_base64_image(base64_str: str, folder: str = "images") -> str:
    """base64 이미지 문자열을 R2에 업로드하고 public URL을 반환"""
    if "," in base64_str:
        header, data = base64_str.split(",", 1)
        # data:image/jpeg;base64 → jpeg
        ext = header.split("/")[1].split(";")[0]
    else:
        data = base64_str
        ext = "jpg"

    image_bytes = base64.b64decode(data)
    filename = f"{folder}/{uuid.uuid4()}.{ext}"
    content_type = f"image/{ext}"

    s3.put_object(
        Bucket=R2_BUCKET_NAME,
        Key=filename,
        Body=image_bytes,
        ContentType=content_type,
    )

    return f"{R2_PUBLIC_URL}/{filename}"


def delete_image(url: str) -> None:
    """public URL로부터 R2 객체를 삭제"""
    if not url or not url.startswith(R2_PUBLIC_URL):
        return
    key = url[len(R2_PUBLIC_URL) + 1:]
    try:
        s3.delete_object(Bucket=R2_BUCKET_NAME, Key=key)
    except ClientError:
        pass

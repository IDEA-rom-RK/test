
import uuid
from io import BytesIO

from PIL import Image
from django.conf import settings
from supabase import create_client


def get_supabase():
    return create_client(
        settings.SUPABASE_URL,
        settings.SUPABASE_SECRET_KEY
    )


def upload_avatar(image_file, user_id):
    # Ограничиваем размер файла до 5 МБ
    if image_file.size > 5 * 1024 * 1024:
        raise ValueError("Размер изображения не должен превышать 5 МБ.")

    # Проверяем, что файл действительно является изображением
    try:
        image = Image.open(image_file)
        image.verify()
    except Exception:
        raise ValueError("Выбранный файл не является корректным изображением.")
    finally:
        image_file.seek(0)

    # Разрешаем только эти форматы
    image_format = image.format

    formats = {
        "JPEG": ("jpg", "image/jpeg"),
        "PNG": ("png", "image/png"),
        "WEBP": ("webp", "image/webp"),
    }

    if image_format not in formats:
        raise ValueError("Разрешены только JPG, PNG и WEBP.")

    extension, content_type = formats[image_format]

    # Создаём уникальное имя файла
    file_path = f"{user_id}/{uuid.uuid4().hex}.{extension}"

    # Загружаем изображение в Supabase Storage
    supabase = get_supabase()

    supabase.storage.from_(
        settings.SUPABASE_STORAGE_BUCKET
    ).upload(
        file_path,
        image_file.read(),
        file_options={
            "content-type": content_type,
            "upsert": "false"
        }
    )

    return file_path


def get_avatar_url(file_path):
    if not file_path:
        return None

    supabase = get_supabase()

    result = supabase.storage.from_(
        settings.SUPABASE_STORAGE_BUCKET
    ).create_signed_url(
        file_path,
        3600
    )

    return result.get("signedURL") or result.get("signedUrl")

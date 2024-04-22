import io

from PIL import Image


def convert2bytearray(image: Image) -> bytes:
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, "PNG")
    return img_byte_arr.getvalue()


def conver2pilimage(byte_array: bytes) -> Image:
    return Image.open(io.BytesIO(byte_array))

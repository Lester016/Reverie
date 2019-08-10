import os
import secrets
from PIL import Image
from flask import current_app


def save_post_image(imageFile):
    randomHex = secrets.token_hex(8)
    _, fExt = os.path.splitext(imageFile.filename)
    pictureFN = randomHex + fExt
    picturePN = os.path.join(current_app.root_path,
                             'static/post_images', pictureFN)

    outputSize = (1325, 825)
    resizedImage = Image.open(imageFile)
    resizedImage.thumbnail(outputSize)

    resizedImage.save(picturePN)
    return pictureFN

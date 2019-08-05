import os
import secrets
from PIL import Image
from flask import url_for, current_app


def save_picture(imageFile):
    randomHex = secrets.token_hex(8)
    _, fExt = os.path.splitext(imageFile.filename)
    pictureFN = randomHex + fExt
    picturePN = os.path.join(current_app.root_path,
                             'static/profile_pictures', pictureFN)

    outputSize = (325, 325)
    resizedImage = Image.open(imageFile)
    resizedImage.thumbnail(outputSize)

    resizedImage.save(picturePN)
    return pictureFN

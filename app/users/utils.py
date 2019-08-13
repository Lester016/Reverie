import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from app import mail


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


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@reverie.com',
                  recipients=[user.Email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

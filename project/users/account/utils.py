import os
import secrets
from flask import current_app
from PIL import Image

# metoda na ulozenie obrazka a jeho orezanie
def save_picture(form_picture):
    random_hex = secrets.token_hex(16)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_name = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, "static/pictures/users", picture_name)

    img_size = (200, 200)
    img = Image.open(form_picture)
    img.thumbnail(img_size)
    img.save(picture_path)

    return picture_name

def remove_picture(old_picture_name):
    if old_picture_name == "Default.png":
        return
    picture_path = os.path.join(current_app.root_path, "static/pictures/users", old_picture_name)
    os.remove(picture_path)

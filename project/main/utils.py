import concurrent.futures
from PIL import Image
import os


default_big_size = (500, 350)


main_folder = "C:/Users/marce/Desktop/PyProjects/Bookstore/project/static/pictures/main"

def get_pictures(path=main_folder):
    files = os.listdir(path)
    pictures = []
    for file in files:
        if file.endswith(".png") or file.endswith(".jpg"):
            pictures.append(file)

    return pictures
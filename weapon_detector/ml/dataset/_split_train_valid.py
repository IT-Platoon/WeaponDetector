"""Разделение данных на train/valid"""


import os
import random

SIZE_VALID = 0.12


def main():
    images = os.listdir('./new/train/images/')

    valid_images = random.sample(images, int(len(images) * SIZE_VALID))
    print(len(valid_images))
    for filename in valid_images:
        filename = filename[:-4]
        os.replace(f'./new/train/images/{filename}.jpg', f'./new/valid/images/{filename}.jpg')
        os.replace(f'./new/train/labels/{filename}.txt', f'./new/valid/labels/{filename}.txt')


if __name__ == '__main__':
    main()

"""Переименовывангие файлов в папке"""

import os


def main():

    counter = 9000
    for dir_name in ['rifles']:
        for filename in os.listdir(f'./{dir_name}/images/'):
            filename = filename[:-4]

            new_filename = f'hack{counter}'
            os.rename(f'./{dir_name}/images/{filename}.jpg', f'./{dir_name}/images/{new_filename}.jpg')
            os.rename(f'./{dir_name}/labels/{filename}.txt', f'./{dir_name}/labels/{new_filename}.txt')
            counter += 1

if __name__ == '__main__':
    main()

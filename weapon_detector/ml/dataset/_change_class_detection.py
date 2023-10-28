"""Меняем датасет файлы"""


import os
import shutil

if not os.path.isdir("new"):
    os.mkdir("new")
if not os.path.isdir("new/images"):
    os.mkdir("new/images")
if not os.path.isdir("new/labels"):
    os.mkdir("new/labels")

STAGES = ['train', 'valid', 'test']
FIND_CLASS = ['1', ]
NEW_CLASS = ['0', ]


def main():

    for stage in STAGES:
        for filename in os.listdir(f'./{stage}/labels'):

            with open(f'./{stage}/labels/{filename}') as f:
                text = []
                for row in f.readlines():
                    if row[0] in FIND_CLASS:
                        idx_find_class = FIND_CLASS.index(row[0])
                        row = f'{NEW_CLASS[idx_find_class]}{row[1:]}'
                        text.append(row)

            if text:
                with open(f'./new/labels/{filename}', 'w') as f:
                    f.writelines(text)

                filename = filename[:len(filename)-4]
                try:
                    pass
                    shutil.copyfile(f'./{stage}/images/{filename}.jpg', f'./new/images/{filename}.jpg')
                    # os.replace(f'./{stage}/images/{filename}.jpg', f'./new/images/{filename}.jpg')
                except:
                    pass


if __name__ == '__main__':
    main()

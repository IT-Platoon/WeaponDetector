"""Меняем датасет файлы"""

LIMIT = 0.6

import os
import shutil
from random import random
# from tqdm import tqdm

if not os.path.isdir("new"):
    os.mkdir("new")
if not os.path.isdir("new/train"):
    os.mkdir("new/train")
if not os.path.isdir("new/valid"):
    os.mkdir("new/valid")
if not os.path.isdir("new/train/images"):
    os.mkdir("new/train/images")
if not os.path.isdir("new/train/labels"):
    os.mkdir("new/train/labels")
if not os.path.isdir("new/valid/images"):
    os.mkdir("new/valid/images")
if not os.path.isdir("new/valid/labels"):
    os.mkdir("new/valid/labels")

# in_dir = set()

def main():

    counter = 0
    for stage in ['train', 'valid']:
        for filename in os.listdir(f'./{stage}/labels'):
            if 'desktop.ini' in filename:
                continue

            with open(f'./{stage}/labels/{filename}') as f:
                text = []
                all_text = []
                for row in f.readlines():
                    row = f'{row[0]}{row[1:]}'
                    sizes = row.split(' ')
                    
                    all_text.append(row)
                    try:
                        if float(sizes[-1]) <= LIMIT and float(sizes[-2]) <= LIMIT:
                            text.append(row)
                    except:
                        print(filename, sizes)

            part = None
            for t_part in ('_jpg', '_jpeg', '_png'):
                if t_part in filename:
                    part = filename.split(t_part)[0]
                    break
            if text:
            # if (part not in in_dir) and text:
                # in_dir.add(part)

                # new_stage = 'valid' if (random() < 0.2) else 'train'
                
                with open(f'./new/train/labels/{filename}', 'w') as f:
                    f.writelines(all_text)

                filename = filename[:len(filename)-4]
                try:
                    counter += 1
                    shutil.copyfile(f'./train/images/{filename}.jpg', f'./new/train/images/{filename}.jpg')
                except:
                    pass
    print(counter)


if __name__ == '__main__':
    main()

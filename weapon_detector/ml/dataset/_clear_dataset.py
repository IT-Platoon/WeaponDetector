"""Очистка основного датасета от мусора."""


import os


def main():
    for filename in os.listdir('./train/images'):
        # filename = filename[:-4]
        if filename in os.listdir('./categories/handgun/images'):
            os.remove(f'./train/images/{filename}')
        elif filename in os.listdir('./categories/imitations/images'):
            os.remove(f'./train/images/{filename}')
        elif filename in os.listdir('./categories/others/images'):
            os.remove(f'./train/images/{filename}')
        elif filename in os.listdir('./categories/rifles/images'):
            os.remove(f'./train/images/{filename}')
    print(1)
    for filename in os.listdir('./train/labels'):
        # filename = filename[:-4]
        if filename in os.listdir('./categories/handgun/labels'):
            os.remove(f'./train/labels/{filename}')
        elif filename in os.listdir('./categories/imitations/labels'):
            os.remove(f'./train/labels/{filename}')
        elif filename in os.listdir('./categories/others/labels'):
            os.remove(f'./train/labels/{filename}')
        elif filename in os.listdir('./categories/rifles/labels'):
            os.remove(f'./train/labels/{filename}')


if __name__ == '__main__':
    main()

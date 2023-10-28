"""Подсчёт классов в датасете."""


import os

STAGE = ['new/train', 'new/valid']


def main():
    for stage in STAGE:
        dict_counter = {}
        for filename in os.listdir(f'./{stage}/labels'):
            with open(f'./{stage}/labels/{filename}') as f:
                for row in f.readlines():

                    if not row[0].isdigit():
                        continue

                    if row[0] not in dict_counter:
                        dict_counter[row[0]] = 1
                    else:
                        dict_counter[row[0]] += 1
        print(stage, dict_counter)


if __name__ == '__main__':
    main()

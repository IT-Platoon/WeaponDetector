"""Меняем датасет файлы"""


import os
import fnmatch


def main(path_to):
    dir_path = os.path.dirname(os.path.realpath(__file__))

    def del_augment(path):
        counter = 0
        for root, dirs, files in os.walk(path):
            for directory in dirs:
                pattern = ''
                for dir_root, _, dir_files in os.walk(os.path.join(path, directory)):
                    for name in dir_files:
                        uniq_name = name.split('.rf.')[0]
                        if pattern != uniq_name:
                            pattern = uniq_name
                        else:
                            if fnmatch.fnmatch(uniq_name, pattern):
                                file_path = os.path.join(dir_root, name)
                                counter += 1
                                # os.remove(os.path.join(dir_path, file_path))
        print(counter)

    del_augment(path_to)


if __name__ == '__main__':
    main('./')

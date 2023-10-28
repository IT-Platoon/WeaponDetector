import os
from typing import Callable, Union
from datetime import datetime

import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def analyse_target_class_by_conf(classes: list, conf: list) -> str:
    """ Бывают случаи, когда модель на одном изображении видит
    лебедей нескольких классов.
    Здесь будет искаться по параметру сумме conf каждого класса.
    У какого класса больше conf, тот и будет таргетом.
    return: str - target class. """
    summator = {}
    for i in range(len(classes)):

        name_class = classes[i]

        if name_class not in summator:
            summator[name_class] = conf[i].item()

        else:
            summator[name_class] += conf[i].item()

    return max(summator, key=summator.get) if summator else None


def analyse_target_class_by_count(classes: list, conf: list = None) -> str:
    """ Бывают случаи, когда модель на одном изображении видит
    лебедей нескольких классов.
    Таргетом будет тот класс, которого больше предсказано на изображении.
    return: str - target class. """

    summator = {}
    for i in range(len(classes)):

        name_class = classes[i]

        if name_class not in summator:
            summator[name_class] = 1

        else:
            summator[name_class] += 1

    return max(summator, key=summator.get) if summator else None


def get_directory_name() -> str:
    bad_symbols = (" ", ".", ":")
    now_datetime = []
    for symbol in str(datetime.now()):
        now_datetime.append(
            symbol if symbol not in bad_symbols else "-"
        )
    return f"detection_{''.join(now_datetime)}"


def create_logfile(log_list: list, filename_txt: str) -> None:
    with open(filename_txt, '+a') as f:
        f.write(f'{log_list[0]} {log_list[1]}\n')


def create_submission_csv(
    filename_csv: str,
    list_final_dict: list,
    dir_save: str,
    ) -> None:
    """ Создание csv-файла с двумя колонками: (filename, target)
    для отправки submission.
>>>>>>> origin/ml
    filename_csv: str - название csv файла.
    list_final_dict: list[dict] - список предсказанных изображений.
    analyzer: function - функция подсчёта таргета на изображении.
    return: None """

    list_filename = []
    list_target = []

    # Определяю target каждого изображения.
    for final_dict in list_final_dict:

        list_filename.append(final_dict['filename'])
        target_class = final_dict['target_image']

        # Классы для отправки решения хакатона.
        if target_class in ('weapons', 'short_weapons', 'long_weapons', 'other'):
            target_class = 1
        else:
            target_class = 0

        list_target.append(target_class)

    new_list_filename = []
    for elem in list_filename:
        try:
            testing = elem.split("/")[-1]
            new_list_filename.append(testing)
        except ValueError:
            testing = elem
            new_list_filename.append(testing)

    df = pd.DataFrame({'name': new_list_filename,'class': list_target,})
    df.to_csv(os.path.join(dir_save, filename_csv), sep=";", index=False)


def save_imgs(list_final_dict: list, dir_save: str) -> list[dict]:
    """ Сохранение всех предсказанных изображений с боксами.
    list_final_dict: list[dict] - предсказанные данные.
    dir_save: str - директория, в которую сохранить предсказанные изображения.
    return: list[dict] """

    # Создание папки
    if not os.path.isdir(dir_save):
        os.mkdir(dir_save)

    for final_dict in list_final_dict:
        filename = os.path.basename(final_dict["filename"])
        path = os.path.join(dir_save, filename)
        final_dict["result_path"] = path
        image = cv2.cvtColor(final_dict["img"], cv2.COLOR_BGR2RGB)
        pixels = np.array(image)
        plt.imsave(path, pixels)
    return list_final_dict


def convert_images_to_video(images: list[np.ndarray], filename: str):
    """ Соединение изображений в одно видео.
    images: np.array - массив изображений.
    filename: str - название выходного файла.
    return - видео """

    img = images[0]

    height = img.shape[0]
    width = img.shape[1]
    fps = 24

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    
    video = cv2.VideoWriter(filename, fourcc, fps, (width, height))
    
    for img in images:
        # img =  cv2.cvtColor(img, cv2.COLO)
        video.write(img)
    
    video.release()
    return video

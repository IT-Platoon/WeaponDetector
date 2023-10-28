import os
from datetime import datetime
from typing import Callable

from ultralytics import YOLO
import torch
import cv2

from utils import (
    save_imgs,

    analyse_target_class_by_conf,
    convert_images_to_video,
    convert_images_to_video,
    get_directory_name,

    create_submission_csv,
    create_logfile,

    analyse_target_class_by_conf,
    analyse_target_class_by_count,
)


def load_model(path: str) -> YOLO:
    """ Загрузка модели.
    return: model """

    cuda_flag = torch.cuda.is_available()
    device = 'cuda' if cuda_flag else 'cpu'
    print(device)

    model = YOLO(path).to(device)
    return model


def predict_one(
        model,
        filename: str,
        analyzer: Callable = analyse_target_class_by_conf,
    ) -> dict:
    """ Предсказание.
    model: ранее загруженная модель для предсказания.
    filename: str - название ОДНОГО файла или url

    return: dict - результат предсказания в формате 
    {
        'filename': str,  # Название изображения.
        'classes': list,  # Классы, которые имеются на изображении.
        'conf': list,  # Достоверность предсказанного класса.
        'count': int,  # Кол-во объектов на изображении.
        'target_image': str,  # Предсказанный класс для картинки.
        'img': Image  # Изображение с боксами объектов.
    }
    """

    # Делаю предсказание.
    result = model(filename, conf=0.25, verbose=False)[0]

    # Преобразую результат в изображение с box.
    img = result.plot()

    # Получаю классы, которые есть на изображении.
    classes = []
    for i in result.boxes.cls:
        classes.append(model.names[int(i)])

    # Достоверность предсказания того или иного класса.
    conf = []
    for i in result.boxes.conf:
        conf.append(i)

    # Количество лебедей на изображении.
    count = len(classes)

    # Предсказанный класс для картинки.
    target_image = analyzer(classes, conf)

    # Результат предсказания хранится тут.
    final_dict = {
        'filename': filename,
        'classes': classes,
        'conf': conf,
        'count': count,
        'target_image': target_image,
        'img': img,
    }
    return final_dict


def run_detection_images(
        model,
        list_filenames: list[str],
        dir_save: str
    ) -> list[dict]:
    """Запуск обработки изображений."""

    list_final_dict = []
    for i, filename in enumerate(list_filenames):
        final_dict = predict_one(model, filename)
        list_final_dict.append(final_dict)
        yield i * 100 / len(list_filenames)

    # Создание папки
    if not os.path.isdir(dir_save):
        os.mkdir(dir_save)

    dir_name = get_directory_name()
    dir_save = os.path.join(dir_save, dir_name)
    list_final_dict = save_imgs(list_final_dict, dir_save)
    create_submission_csv(
        f"{dir_name}.csv",
        list_final_dict,
        dir_save,
    )
    return list_final_dict


def run_detection_videos(
        model,
        list_filenames: list[str],
        dir_save: str,
    ) -> None:
    """Запуск обработки видео."""

    # Создание папки
    if not os.path.isdir(dir_save):
        os.mkdir(dir_save)

    for i, filename in enumerate(list_filenames):
        cap = cv2.VideoCapture(filename) 

        dir_name = get_directory_name()
        dir_name = os.path.join(dir_save, dir_name)
        os.mkdir(dir_name)

        count_frame = 0
        lst_images = []
        while cap.isOpened():
            count_frame += 1
            # Считываем кадр
            success, frame = cap.read()

            if success:
                results = model(frame, verbose=False)
                annotated_frame = results[0].plot()
                lst_images.append(annotated_frame)

                classes = []
                for i in results[0].boxes.cls:
                    classes.append(model.names[int(i)])

                if len(classes) != 0:
                    filename_txt = os.path.join(dir_name, 'log.txt')
                    log_list = [f'{count_frame / 24} sec', classes]
                    create_logfile(log_list, filename_txt)

                annotated_frame = cv2.resize(
                    annotated_frame,
                    dsize=(640, 640),
                    interpolation=cv2.INTER_CUBIC,
                )
                cv2.imshow("Exit `q`", annotated_frame)

                # Остановка по нажатию 'q'
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            else:
                break  # Конец видео

        format_video = filename[-3:]
        filename = f'{filename[:-4]}_annot.{format_video}'
        path = os.path.join(dir_name, filename)
        convert_images_to_video(lst_images, path)

        # Закрытие окна
        cap.release()
        cv2.destroyAllWindows()
        yield i * 100 / len(list_filenames)


def run_detection_webcam(
        model,
        dir_save: str,
        source_webcam: str = '0',
    ) -> None:
    """Запуск детектирования в реальном времени по веб-камере."""

    # Создание папки
    if not os.path.isdir(dir_save):
        os.mkdir(dir_save)

    results = model.predict(source_webcam, show=True, stream=True)

    dir_name = f'cam{source_webcam}_' + get_directory_name()
    dir_save = os.path.join(dir_save, dir_name)
    os.mkdir(dir_save)
    filename_txt = os.path.join(dir_save, 'logs.txt')

    for result in results:

        classes = []
        for i in result.boxes.cls:
            classes.append(model.names[int(i)])

        # Если найдено оружие - сохраняем в логи.
        if len(classes) != 0:
            datetime_now = datetime.now()
            log_list = [datetime_now, classes]
            create_logfile(log_list, filename_txt)


if __name__ == '__main__':
    model = load_model('./weights/best_categorial.pt')
    list_filenames = ['./чвк.mp4']
    dir_save = './temp_results'
    detection = run_detection_videos(model, list_filenames, dir_save)
    try:
        while True:
            next(detection)
    except StopIteration as exception:
        print(exception.value)

    # model = load_model('./weights/best_categorial.pt')
    # list_filenames = '0'
    # dir_save = './temp_results'
    # detection = run_detection_webcam(model, list_filenames, dir_save)

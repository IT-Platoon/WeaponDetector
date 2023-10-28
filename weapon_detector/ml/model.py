import os
from datetime import datetime

from ultralytics import YOLO
import torch
import cv2

from utils import (
    save_imgs,
    create_csv_custom,
    analyse_target_class_by_conf,
    analyse_target_class_by_count,
    convert_images_to_video,
    convert_images_to_video,
)


def load_model(path: str) -> YOLO:
    """ Загрузка модели.
    return: model """

    cuda_flag = torch.cuda.is_available()
    device = 'cuda' if cuda_flag else 'cpu'
    print(device)

    model = YOLO(path).to(device)
    return model


def predict_one(model, filename: str) -> dict:
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
    target_image = analyse_target_class_by_count(classes, conf)

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


def get_directory_name() -> str:
    bad_symbols = (" ", ".", ":")
    now_datetime = []
    for symbol in str(datetime.now()):
        now_datetime.append(
            symbol if symbol not in bad_symbols else "-"
        )
    return f"detection_{''.join(now_datetime)}"


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
    create_csv_custom(
        f"{dir_name}.csv",
        list_final_dict,
        dir_save,
        submission_flag=True,
    )
    return list_final_dict


def run_detection_videos(
        model,
        list_filenames: list[str],
        dir_save: str = None,
    ) -> None:
    """Запуск обработки видео."""

    # Создание папки
    if not os.path.isdir(dir_save):
        os.mkdir(dir_save)

    for i, filename in enumerate(list_filenames):
        cap = cv2.VideoCapture(filename) 

        lst_images = []
        while cap.isOpened():
            # Считываем кадр
            success, frame = cap.read()

            if success:
                results = model(frame, verbose=False)
                annotated_frame = results[0].plot()
                lst_images.append(annotated_frame)

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

        if dir_save:
            format_video = filename[-3:]
            filename = f'{filename[:-4]}_annot.{format_video}'
            path = os.path.join(dir_save, filename)
            convert_images_to_video(lst_images, path)

        # Закрытие окна
        cap.release()
        cv2.destroyAllWindows()
        yield i * 100 / len(list_filenames)


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

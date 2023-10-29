# Weapon-Detector

## Запуск

Для тестирования приложения можно воспользоваться собранными версиями:
https://github.com/IT-Platoon/WeaponDetector/releases/latest

Для запуска нужно:
1. Распаковать
2. Распаковать для нужной ОС
3. Запустить соответствующий исполняемый файл

Модели для выбора:
https://drive.google.com/drive/folders/1btiD9tmcXb8exlLmJth9-5YqBZACS2-4

## Установка

Установка производилась на OS Linux Gnome Manjaro

1. Настройка виртуального окружения
```bash
make install_linux
```

2. Запуск приложения
```bash
make run
```

3. Сборка приложения
```bash
make build_linux
```

4. Для использования собранного приложения:
```bash
make run_prod
```

## Используемые технологии

- Python - язык программирования
- PyQt - библиотека для разработки интерфейса
- ultralytics - нейросеть для выделения объекта на изображении


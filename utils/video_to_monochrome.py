import cv2


def convert_video_to_grayscale(input_video_path, output_video_path):
    # Открываем входное видео
    cap = cv2.VideoCapture(input_video_path)

    # Проверяем, удалось ли открыть видео
    if not cap.isOpened():
        print("Ошибка: Не удалось открыть видеофайл.")
        return

    # Получаем параметры видео
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(frame_height, frame_width)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Создаем объект для записи видео
    out = cv2.VideoWriter(
        output_video_path,
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (frame_width, frame_height),
        isColor=False,
    )
    count = 0
    # Читаем и обрабатываем кадры видео
    while True:
        count += 1
        ret, frame = cap.read()
        print(f"{count}/{frame_count}", end="\r")
        if not ret:
            break

        # Переводим кадр в оттенки серого
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Записываем обработанный кадр
        out.write(gray_frame)

    # Освобождаем ресурсы
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print("Видео успешно преобразовано и сохранено.")


# Пример использования функции
input_video = r""
output_video = r""
convert_video_to_grayscale(input_video, output_video)

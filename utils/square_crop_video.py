import cv2

def crop_center_square(input_video_path, output_video_path, crop_size=640):
    # Открываем входное видео
    cap = cv2.VideoCapture(input_video_path)
    
    # Проверяем, удалось ли открыть видео
    if not cap.isOpened():
        print("Ошибка: Не удалось открыть видеофайл.")
        return

    # Получаем параметры видео
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Вычисляем координаты для обрезки
    x_center = frame_width // 2
    y_center = frame_height // 2
    x_start = x_center - crop_size // 2
    y_start = y_center - crop_size // 2

    # Создаем объект для записи видео
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (crop_size, crop_size))

    # Читаем и обрабатываем кадры видео
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break

        # Обрезаем кадр до квадратной области
        cropped_frame = frame[y_start:y_start+crop_size, x_start:x_start+crop_size]
        
        # Записываем обработанный кадр
        out.write(cropped_frame)

    # Освобождаем ресурсы
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print("Видео успешно обрезано и сохранено.")

# Пример использования функции
input_video = r''
output_video = r''
crop_center_square(input_video, output_video)
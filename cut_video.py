import cv2

"""
    Нарезает видео на заданное количество кусков и сохраняет каждый кусок отдельным файлом.

    Параметры:
    - input_video (str): Путь к исходному видеофайлу.
    - output_prefix (str): Префикс для имен выходных файлов.
    - num_segments (int): Количество сегментов, на которые нужно разрезать видео.

    Пример использования:
    cut_video('input_video.mp4', 'output_segment', 3)
"""

def cut_video(input_video, output_prefix, num_segments):
    # Открываем видеофайл
    cap = cv2.VideoCapture(input_video)

    # Получаем общее количество кадров
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Рассчитываем количество кадров на каждый сегмент
    frames_per_segment = total_frames // num_segments

    # Устанавливаем начальное значение номера кадра
    frame_num = 0

    # Нарезаем видео на сегменты
    for i in range(num_segments):
        # Устанавливаем начальную позицию для чтения
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)

        # Читаем кадры для текущего сегмента
        frames = []
        for j in range(frames_per_segment):
            ret, frame = cap.read()
            if ret:
                frames.append(frame)
            else:
                break

        # Сохраняем сегмент как новый видеофайл
        output_file = f"{output_prefix}_{i}.mp4"
        out = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'mp4v'), cap.get(cv2.CAP_PROP_FPS), (frames[0].shape[1], frames[0].shape[0]))
        for frame in frames:
            out.write(frame)
        out.release()

        # Обновляем номер кадра для следующего сегмента
        frame_num += frames_per_segment

    # Освобождаем ресурсы
    cap.release()

if __name__ == "__main__":
    # Пример использования
    input_video = r"C:\Users\boiko.k.v\Desktop\boiko\labTest.MOV"  # Путь к исходному видео
    output_prefix = 'output_segment'  # Префикс для имен выходных файлов
    num_segments = 6  # Количество сегментов, на которые нужно разрезать видео

    cut_video(input_video, output_prefix, num_segments)

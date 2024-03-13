import tkinter as tk


def process_number():
    try:
        # Получаем число из текстового поля
        input_number = float(entry.get())
        # Пример обработки: удвоение и утроение введенного числа
        output_number1 = input_number * 2
        output_number2 = input_number * 3
        # Обновляем метки результатов
        result_label1.config(text=f"Флегмовое число: {output_number1}")
        result_label2.config(text=f"Отношение кубового потока к сырьевому потоку: {output_number2}")
    except ValueError:
        # Обработка случая, когда введено не число
        result_label1.config(text="Ошибка: введите число")
        result_label2.config(text="")


# Создаем главное окно
root = tk.Tk()
root.minsize(300, 200)
root.title("Aspen UI")

# Создаем виджеты
entry_label = tk.Label(root, text="Мольный поток C6H5C2H5:")
entry = tk.Entry(root)
process_button = tk.Button(root, text="Обработать", command=process_number)
result_label1 = tk.Label(root, text="Флегмовое число: ")
result_label2 = tk.Label(root, text="Отношение кубового потока к сырьевому потоку: ")

# Располагаем виджеты
entry_label.pack()
entry.pack()
process_button.pack()
result_label1.pack()
result_label2.pack()

# Запускаем главный цикл обработки событий
root.mainloop()

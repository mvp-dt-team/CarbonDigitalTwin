import tkinter as tk
from tkinter import ttk


class SensorModuleUI(tk.Tk):
    def __init__(self, start_func, stop_func):
        super().__init__()
        self.title("Sensor Module")
        self.geometry("400x300")
        self.fields_frame = ttk.Frame(self)
        self.fields_frame.pack(padx=10, pady=10, fill="x", expand=True)
        self.start_stop_button = ttk.Button(
            self, text="Старт", command=self.toggle_start_stop
        )
        self.start_stop_button.pack(pady=(0, 10))
        self.is_started = False
        self.start_function = start_func
        self.stop_function = stop_func
        print("ui inited")

    def toggle_start_stop(self):
        print("toggle_start_stop: ", self.is_started)
        if self.is_started:
            self.start_stop_button.config(text="Старт")
            self.is_started = False
            self.stop_function()

        else:
            self.start_stop_button.config(text="Стоп")
            self.is_started = True
            self.start_function()
        print("toggle_start_stop: ", self.is_started)

    def update_interface(self, grouped_fields):
        print("update_interface: ", grouped_fields)
        # Удаление старых виджетов
        for widget in self.fields_frame.winfo_children():
            widget.destroy()

        # Создание новых полей на основе вложенного словаря
        for group_name, fields in grouped_fields.items():
            group_frame = ttk.LabelFrame(self.fields_frame, text=group_name)
            group_frame.pack(padx=5, pady=5, fill="x", expand=True)
            for field_name, value in fields.items():
                frame = ttk.Frame(group_frame)
                frame.pack(fill="x", expand=True, pady=2)
                ttk.Label(frame, text=f"{field_name}:").pack(side=tk.LEFT)
                # Использование ttk.Label для отображения значения
                label = ttk.Label(frame, text=f"{value}")
                label.pack(side=tk.RIGHT, fill="x", expand=True)
        print("interface updated")

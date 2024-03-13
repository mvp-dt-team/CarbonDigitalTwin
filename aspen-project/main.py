from CodeLibraryCustom import Simulation

sim = Simulation(AspenFileName= "Styrene.bkp", WorkingDirectoryPath= r"C:\\Users\\boiko.k.v\\Desktop\\pythonprojects\\schemes" ,VISIBILITY=False)


def setParam(amountEB, simulation):
    # print(Simulation.__dir__())
    simulation.STRM_Set_TotalFlowBasis(Streamname='10-FEED', TotalFlowBasis=amountEB, Compoundname='ETHYLBEN')
    convergence = sim.Run()
    col11_out = simulation.BLK_RADFRAC_GET_OUTPUTS('COL11')
    col21_out = simulation.BLK_RADFRAC_GET_OUTPUTS('COL21')
    return col11_out['Condenser_RefluxRatio'], col11_out['Reboiler_BottomsToFeedRatio'], col21_out['Reboiler_BottomsToFeedRatio'],

import tkinter as tk

def process_number():
    try:
        # Получаем число из текстового поля
        input_number = float(entry.get())
        # Пример обработки: удвоение и утроение введенного числа
        output_number1, output_number2, output_number3 = setParam(input_number, sim)
        # Обновляем метки результатов
        result_label1.config(text=f"Флегмовое число на колонне 1:: {output_number1}")
        result_label2.config(text=f"Отношение кубового потока к сырьевому потоку на колонне 1: {output_number2}")
        result_label3.config(text=f"Отношение кубового потока к сырьевому потоку на колонне 2: {output_number3}")
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
result_label1 = tk.Label(root, text="Флегмовое число на колонне 1: ")
result_label2 = tk.Label(root, text="Отношение кубового потока к сырьевому потоку на колонне 1: ")
result_label3 = tk.Label(root, text="Отношение кубового потока к сырьевому потоку на колонне 2: ")

# Располагаем виджеты
entry_label.pack()
entry.pack()
process_button.pack()
result_label1.pack()
result_label2.pack()
result_label3.pack()

# Запускаем главный цикл обработки событий
root.mainloop()

sim.CloseAspen()
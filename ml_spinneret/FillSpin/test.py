import numpy as np

# Создаем матрицу NumPy, где каждый элемент - это вектор
matrix = np.array([[[1, 2, 3],
                    [4, 5, 6]],
                   [[7, 8, 9],
                    [10, 11, 12]],
                   [[13, 14, 15],
                    [16, 17, 18]]])

# Определенный вектор, который вы хотите заменить
vector_to_replace = np.array([7, 8, 9])

# Определенный вектор, на который вы хотите заменить
replacement_vector = np.array([2.5, 2.5, 2.5])

# Находим индекс вектора в матрице
index = np.all(matrix == vector_to_replace, axis=(1, 2))

# Заменяем вектор на определенный вектор
matrix[index] = replacement_vector

print(matrix)
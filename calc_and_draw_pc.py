import os
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint
from polynoms import Polynomial


class CalculationDrawServicePC:
    def __init__(self):
        pass

    def calculate(self, data: dict) -> tuple:
    # Расчет системы дифференциальных уравнений на заданном интервале
        X = np.linspace(0, 50, 500)  # Временные значения от 0 до 50 (500 шагов)
    
    # Начальные условия: P0 = 1, остальные = 0
        initial_conditions = [1] + [0] * 31  # 32 состояния
        
        # Проверяем входные данные
        print("Initial conditions:", initial_conditions)
        print("mu values:", data["mu"])
        print("lat values:", data["lat"])

        # Вызов odeint для решения системы уравнений
        Y = odeint(
            self.__describe_difference_equations,
            initial_conditions,
            X,
            args=(data["mu"], data['lat'])
        )

        print("Shape of Y:", Y.shape)  # Проверяем размерность решения
        return X, Y


    def initFunctions(self, coefs):
        # Преобразование коэффициентов в объекты полиномиальных функций
        functions = []
        for coef_set in coefs:
            polynomial = Polynomial(*coef_set)
            functions.append(polynomial)
        return functions

    def __describe_difference_equations(self, u, t, mus, lat):
        # Распаковка переменных состояния
        (P0, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12, P13, P14, P15,
        P16, P17, P18, P19, P20, P21, P22, P23, P24, P25, P26, P27, P28, P29, P30, P31) = u

        mus1, mus2, mus3, mus4, mus5 = mus  # Интенсивности восстановления
        lat1, lat2, lat3, lat4, lat5 = lat  # Интенсивности отказов

        # Базовое состояние (все ПК исправны)
        dP0_dt = -(lat1 + lat2 + lat3 + lat4 + lat5) * P0 + mus1 * P1 + mus2 * P2 + mus3 * P4 + mus4 * P8 + mus5 * P16

        # Одиночные неисправности
        dP1_dt = lat1 * P0 - (mus1 + lat2 + lat3 + lat4 + lat5) * P1 + mus2 * P3 + mus3 * P5 + mus4 * P9 + mus5 * P17
        dP2_dt = lat2 * P0 - (mus2 + lat1 + lat3 + lat4 + lat5) * P2 + mus1 * P3 + mus3 * P6 + mus4 * P10 + mus5 * P18
        dP4_dt = lat3 * P0 - (mus3 + lat1 + lat2 + lat4 + lat5) * P4 + mus1 * P5 + mus2 * P6 + mus4 * P12 + mus5 * P20
        dP8_dt = lat4 * P0 - (mus4 + lat1 + lat2 + lat3 + lat5) * P8 + mus1 * P9 + mus2 * P10 + mus3 * P12 + mus5 * P24
        dP16_dt = lat5 * P0 - (mus5 + lat1 + lat2 + lat3 + lat4) * P16 + mus1 * P17 + mus2 * P18 + mus3 * P20 + mus4 * P24

        # Двойные неисправности
        dP3_dt = lat1 * P2 + lat2 * P1 - (mus1 + mus2 + lat3 + lat4 + lat5) * P3 + mus3 * P7 + mus4 * P11 + mus5 * P19
        dP5_dt = lat1 * P4 + lat3 * P1 - (mus1 + mus3 + lat2 + lat4 + lat5) * P5 + mus2 * P7 + mus4 * P13 + mus5 * P21
        dP6_dt = lat2 * P4 + lat3 * P2 - (mus2 + mus3 + lat1 + lat4 + lat5) * P6 + mus1 * P7 + mus4 * P14 + mus5 * P22
        dP9_dt = lat1 * P8 + lat4 * P1 - (mus1 + mus4 + lat2 + lat3 + lat5) * P9 + mus2 * P11 + mus3 * P13 + mus5 * P25
        dP10_dt = lat2 * P8 + lat4 * P2 - (mus2 + mus4 + lat1 + lat3 + lat5) * P10 + mus1 * P11 + mus3 * P14 + mus5 * P26
        dP11_dt = lat1 * P10 + lat2 * P9 + lat4 * P3 - (mus1 + mus2 + mus4 + lat3 + lat5) * P11
        dP12_dt = lat3 * P8 + lat4 * P4 - (mus3 + mus4 + lat1 + lat2 + lat5) * P12 + mus1 * P13 + mus2 * P14 + mus5 * P28
        dP13_dt = lat1 * P12 + lat3 * P9 + lat4 * P5 - (mus1 + mus3 + mus4 + lat2 + lat5) * P13
        dP14_dt = lat2 * P12 + lat3 * P10 + lat4 * P6 - (mus2 + mus3 + mus4 + lat1 + lat5) * P14
        dP15_dt = lat1 * P14 + lat2 * P13 + lat3 * P11 + lat4 * P7 - (mus1 + mus2 + mus3 + mus4 + lat5) * P15
        dP17_dt = lat1 * P16 + lat5 * P1 - (mus1 + mus5 + lat2 + lat3 + lat4) * P17 + mus2 * P19 + mus3 * P21 + mus4 * P25
        dP18_dt = lat2 * P16 + lat5 * P2 - (mus2 + mus5 + lat1 + lat3 + lat4) * P18 + mus1 * P19 + mus3 * P22 + mus4 * P26
        dP19_dt = lat1 * P18 + lat2 * P17 + lat5 * P3 - (mus1 + mus2 + mus5 + lat3 + lat4) * P19
        dP20_dt = lat3 * P16 + lat5 * P4 - (mus3 + mus5 + lat1 + lat2 + lat4) * P20 + mus1 * P21 + mus2 * P22 + mus4 * P28
        dP21_dt = lat1 * P20 + lat3 * P17 + lat5 * P5 - (mus1 + mus3 + mus5 + lat2 + lat4) * P21
        dP22_dt = lat2 * P20 + lat3 * P18 + lat5 * P6 - (mus2 + mus3 + mus5 + lat1 + lat4) * P22
        dP23_dt = lat1 * P22 + lat2 * P21 + lat3 * P19 + lat5 * P7 - (mus1 + mus2 + mus3 + mus5 + lat4) * P23
        dP24_dt = lat4 * P16 + lat5 * P8 - (mus4 + mus5 + lat1 + lat2 + lat3) * P24 + mus1 * P25 + mus2 * P26 + mus3 * P28
        dP25_dt = lat1 * P24 + lat4 * P17 + lat5 * P9 - (mus1 + mus4 + mus5 + lat2 + lat3) * P25
        dP26_dt = lat2 * P24 + lat4 * P18 + lat5 * P10 - (mus2 + mus4 + mus5 + lat1 + lat3) * P26
        dP27_dt = lat1 * P26 + lat2 * P25 + lat4 * P19 + lat5 * P11 - (mus1 + mus2 + mus4 + mus5 + lat3) * P27
        dP28_dt = lat3 * P24 + lat4 * P20 + lat5 * P12 - (mus3 + mus4 + mus5 + lat1 + lat2) * P28
        dP29_dt = lat1 * P28 + lat3 * P25 + lat4 * P21 + lat5 * P13 - (mus1 + mus3 + mus4 + mus5 + lat2) * P29
        dP30_dt = lat2 * P28 + lat3 * P26 + lat4 * P22 + lat5 * P14 - (mus2 + mus3 + mus4 + mus5 + lat1) * P30

        # Тройные и больше (пример — аналогичный подход можно расширить)
        dP7_dt = lat1 * P6 + lat2 * P5 + lat3 * P3 - (mus1 + mus2 + mus3 + lat4 + lat5) * P7
        dP31_dt = lat1 * P30 + lat2 * P29 + lat3 * P27 + lat4 * P23 + lat5 * P15 - (mus1 + mus2 + mus3 + mus4 + mus5) * P31

        # Возвращаем производные всех состояний
        return [
            dP0_dt, dP1_dt, dP2_dt, dP3_dt, dP4_dt, dP5_dt, dP6_dt, dP7_dt,
            dP8_dt, dP9_dt, dP10_dt, dP11_dt, dP12_dt, dP13_dt, dP14_dt, dP15_dt,
            dP16_dt, dP17_dt, dP18_dt, dP19_dt, dP20_dt, dP21_dt, dP22_dt, dP23_dt,
            dP24_dt, dP25_dt, dP26_dt, dP27_dt, dP28_dt, dP29_dt, dP30_dt, dP31_dt
        ]

    def save_plots(self, Y: list):
        fig1, ax1 = plt.subplots(figsize=(16, 8))
        time_intervals = np.linspace(0, 50, len(Y))  # X имеет 500 значений

        # Распаковка всех 32 состояний
        states = Y.T  # Теперь states содержит 32 строки (P0, P1, ..., P31)

        # Генерация подписей для состояний (битовые комбинации для 5 ПК)
        labels = ["Базовое состояние"]  # P0
        for i in range(1, 32):
            failed_pcs = ", ".join([f"ПК {j+1}" for j in range(5) if (i >> j) & 1])
            labels.append(f"Неисправность: {failed_pcs}")

        # Добавление всех линий на график
        for i, state in enumerate(states):
            ax1.plot(time_intervals, state, label=labels[i])

        # Настройка графика
        ax1.set_xlabel('Время, часы')
        ax1.set_ylabel('Вероятность')
        ax1.set_title('Вероятность нахождения системы в каждом состоянии')
        ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
        plt.tight_layout()

        # Сохранение первого графика
        images_dir = "images"
        os.makedirs(images_dir, exist_ok=True)  # Создаем папку, если её нет
        path1 = os.path.join(images_dir, "petal_plot_pc.png")
        plt.savefig(path1)

        # Построение увеличенного графика для первых 10 часов
        fig2, ax2 = plt.subplots(figsize=(16, 8))
        zoomed_intervals = time_intervals[time_intervals <= 10]
        zoomed_solution = Y[:len(zoomed_intervals)]

        for i, state in enumerate(zoomed_solution.T):
            ax2.plot(zoomed_intervals, state, label=labels[i])

        # Настройка увеличенного графика
        ax2.set_xlabel('Время (увеличенный масштаб), часы')
        ax2.set_ylabel('Вероятность')
        ax2.set_title('Увеличенный график вероятностей состояний')
        ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
        plt.tight_layout()

        # Сохранение второго графика
        path2 = os.path.join(images_dir, "petal_plot_pc_zoom.png")
        plt.savefig(path2)

        plt.clf()  # Очистка текущей фигуры

        print(f"Saving plots to: {path1}, {path2}")  # Логирование путей
        print("Plots saved successfully!")

        return {
            "image1": path1,
            "image2": path2
        }




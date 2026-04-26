# МУИВ. Обучающийся - Петроградский Вячеслав Максимович.
# Задание №2 по предмету "Безопасность операционных систем".
# Преподаватель (проверяющий) - Черемных Виктор Викторович.

import matplotlib.pyplot as plt


# Блок 1: "Исходные данные"

# Исходная строка в бинарном (двоичном) виде взятая из решенной задачи №1 по заданному исходному
# тексту, коим является мое ФИО (Петроградский Вячеслав Максимович)
bin_str = '11001111 11100101 11110010 11110000 11101110 11100011 11110000 11100000 11100100 11110001 11101010 11101000 11101001 00100000 11000010 11111111 11110111 11100101 11110001 11101011 11100000 11100010 00100000 11001100 11100000 11101010 11110001 11101000 11101100 11101110 11100010 11101000 11110111'
print ('Исходное сообщение (Петроградский Вячеслав Максимович) в битовом потоке:', bin_str)

# Необходимо исключить пробелы в строке bin_str (можно было пропустить данный шаг и вписать
# бинарный код без пробелов, т.к. они нужны только лишь для удобства чтение, но поскольку
# задачи разделены на отдельные решения, я считаю нужным сделать именно так).
bitstream = bin_str.replace(' ', '').replace('\n', '')
print ('\nОбщая длина потока исходного сообщения (без пробелов):', len(bitstream), 'бит')




# Блок 2: "Кодирование по методам: NRZ, Manchester, RZ, AMI"

# NRZ (Non Return to Zero) кодирование
nrz_signal = [1 if bit == '1' else 0 for bit in bitstream]
print ('\nNRZ кодирование:', nrz_signal)

# Manchester кодирование
manchester_signal = []
for bit in bitstream:
    if bit == '1':
          manchester_signal.extend([0,1])
    else:
        manchester_signal.extend([1,0])
print ('\nManchester кодирование:', manchester_signal)

# RZ (Return to Zero) кодирование
rz_signal = []
for bit in bitstream:
    if bit == '1':
          rz_signal.extend([1,0])
    else:
        rz_signal.extend([0,0])
print ('\nRZ кодирование:', rz_signal)

# AMI (Alternative Mark Inversion)  кодирование
ami_signal = []
level = 1 # начальный уровень 
for bit in bitstream:
    if bit == '1':
          ami_signal.append(level)
          level *= -1 # меняем знак
    else:
        ami_signal.append(0)
print ('\nAMI кодирование:', ami_signal)




# Блок 3: "Создание функции подсчета переходов"

def count_transitions(signal):
    transitions = 0
    for i in range(1, len(signal)):
        if signal[i] != signal[i - 1]:
            transitions += 1
    return transitions



# Блок 4: "Функция анализа способов кодирования"

Rb = 1e9  # Скорость передачи (бит/с)

def analyze_signal(signal, name):
    transitions = count_transitions(signal)
    duration = len(signal) / Rb  # длительность сигнала
    freq_avg = transitions / duration if duration != 0 else 0

    # Теоретические оценки
    f_low = 0  # нижняя граница 
    f_high = transitions * Rb / len(signal)

    bandwidth = f_high - f_low

    print(f'\n{name}:')
    print(f'Переходов: {transitions}')
    print(f'Нижняя граница частоты: {f_low:.2e} Гц')
    print(f'Верхняя граница частоты: {f_high:.2e} Гц')
    print(f'Средняя частота: {freq_avg:.2e} Гц')
    print(f'Полоса пропускания: {bandwidth:.2e} Гц')

# Вывод полученных данных

analyze_signal(nrz_signal, 'NRZ')
analyze_signal(manchester_signal, 'Manchester')
analyze_signal(rz_signal, 'RZ')
analyze_signal(ami_signal, 'AMI')




# Блок 5: "Построение графиков"

N = 32 # Ограничим кодирование для первых 4 байт (32 бита) согласно условию задания №2

plt.figure()

# NRZ график
plt.subplot(4, 1, 1)
plt.step(range(N), nrz_signal[:N])
plt.title('NRZ сигнал')
plt.grid()

# Manchester график
plt.subplot(4, 1, 2)
plt.step(range(N), manchester_signal[:N])
plt.title('Manchester сигнал')
plt.grid()

# RZ график
plt.subplot(4, 1, 3)
plt.step(range(N), rz_signal[:N])
plt.title('RZ сигнал')
plt.grid()

# AMI график 
plt.subplot(4, 1, 4)
plt.step(range(N), ami_signal[:N])
plt.title('AMI сигнал')
plt.grid()

plt.tight_layout()
plt.show()







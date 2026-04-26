# МУИВ. Обучающийся - Петроградский Вячеслав Максимович.
# Задание №3 по предмету "Безопасность операционных систем".
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



# Блок 2: "4B/5B кодирование"

# Таблица преобразования по методу 4B/5B 
table_4b5b = {
    '0000': '11110', '0001': '01001',
    '0010': '10100', '0011': '10101',
    '0100': '01010', '0101': '01011',
    '0110': '01110', '0111': '01111',
    '1000': '10010', '1001': '10011',
    '1010': '10110', '1011': '10111',
    '1100': '11010', '1101': '11011',
    '1110': '11100', '1111': '11101'
}

# Разбиение на тетрады (4 бита)
blocks_4bit = [bitstream[i:i+4] for i in range(0, len(bitstream), 4)]

# Кодирование
encoded_5b = ''.join([table_4b5b[b] for b in blocks_4bit])

print("\nИсходное сообщение по методу 4B/5B:", encoded_5b)



# Блок 3: "Перевод в двоичную (bin) и шестнадцатеричную (hex) системы"

hex_str = hex(int(encoded_5b, 2))[2:].upper()

print("\n4B/5B метод в двоичном коде:")
print(' '.join([encoded_5b[i:i+4] for i in range(0, len(encoded_5b), 4)]))

print("\n4B/5B метод в шестнадцатеричном коде:", hex_str)




# Блок 4: "Подсчет длины и избыточности"

original_len = len(bitstream)
new_len = len(encoded_5b)

redundancy = (new_len - original_len) / original_len

print("\nДлина исходного:", original_len, "бит")
print("Длина сообщения:", new_len, "бит (", new_len/8, "байт)")
print("Избыточность:", round(redundancy, 3), "(", int(redundancy*100), "% )")





# Блок 5: "Физическое кодирование"

bitstream_new = encoded_5b

# Manchester кодирования нового сообщения по методу 4B/5B
manchester_new = []
for bit in bitstream_new:
    if bit == '1':
        manchester_new.extend([0, 1])
    else:
        manchester_new.extend([1, 0])

# AMI кодирования нового сообщения по методу 4B/5B
ami_new = []
level = 1
for bit in bitstream_new:
    if bit == '1':
        ami_new.append(level)
        level *= -1
    else:
        ami_new.append(0)




# Блок 6: "Функция подсчета переходов (из задания №2)"

def count_transitions(signal):
    transitions = 0
    for i in range(1, len(signal)):
        if signal[i] != signal[i - 1]:
            transitions += 1
    return transitions



# Блок 7: "Функция анализа способов кодирования (из задания №2)"

Rb = 1e9  # Скорость передачи по условию задачи - 1 Гбит/с

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




print("\nАнализ для 4B/5B:")
analyze_signal(manchester_new, "Manchester (4B/5B)")
analyze_signal(ami_new, "AMI (4B/5B)")



# Блок 8: "Построение графиков"
N = 32 # Ограничим кодирование для первых 4 байт (32 бита) согласно условию задания №2 

plt.figure()

# Manchester график 
plt.subplot(2, 1, 1)
plt.step(range(N), manchester_new[:N])
plt.title('Manchester (Метод 4B/5B)')
plt.grid()

# AMI график
plt.subplot(2, 1, 2)
plt.step(range(N), ami_new[:N])
plt.title('AMI (Метод 4B/5B)')
plt.grid()

plt.tight_layout()
plt.show()

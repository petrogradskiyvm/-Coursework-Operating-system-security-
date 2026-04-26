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


# Блок 2: "Функция скремблирование данных"
       
def scramble(bitstream):
    # регистр длиной 7
    B = [1, 0, 1, 1, 0, 1, 0]

    output = []

    for i in range(len(bitstream)):
        Ai = int(bitstream[i])

        # Bi = Ai ^ B[i-5] ^ B[i-7]
        feedback = B[-5] ^ B[-7] # возвращаемый сигнал из выхода регистра обратно на вход через XOR (^)
        Bi = Ai ^ feedback

        output.append(str(Bi))

        # сдвиг регистра
        B.pop(0)
        B.append(Bi)

    return ''.join(output)

scrambled = scramble(bitstream)

print("\nСкремблированный:")
print(scrambled)

# Блок 3: "Перевод в двоичную (bin) и шестнадцатеричную (hex) системы"

hex_scrambled = hex(int(scrambled, 2))[2:].upper()

print("\nСкремблирование исходного сообщения в двоичном коде:")
print(' '.join([scrambled[i:i+4] for i in range(0, len(scrambled), 4)]))

print("\nСкремблирование исходного сообщения шестнадцатеричном коде:", hex_scrambled)


# Блок 4: "Физическое кодирование по методам Manchester и AMI"

# Manchester
manchester = []
for bit in scrambled:
    if bit == '1':
        manchester.extend([0, 1])
    else:
        manchester.extend([1, 0])

# AMI
ami = []
level = 1
for bit in scrambled:
    if bit == '1':
        ami.append(level)
        level *= -1
    else:
        ami.append(0)



# Блок 5: "Функция подсчета переходов (из задания №2)"

def count_transitions(signal):
    transitions = 0
    for i in range(1, len(signal)):
        if signal[i] != signal[i - 1]:
            transitions += 1
    return transitions


# Блок 6: "Функция анализа способов кодирования (из задания №2)"

Rb = 1e9  # Скорость передачи по условию задачи - 1 Гбит/с

def analyze_signal(signal, name):
    transitions = count_transitions(signal)

    duration = len(signal) / Rb
    freq_avg = transitions / duration if duration != 0 else 0

    f_low = 0
    f_high = transitions * Rb / len(signal)
    bandwidth = f_high - f_low

    print(f'\n{name}:')
    print(f'Переходов: {transitions}')
    print(f'Нижняя граница частоты: {f_low:.2e} Гц')
    print(f'Верхняя граница частоты: {f_high:.2e} Гц')
    print(f'Средняя частота: {freq_avg:.2e} Гц')
    print(f'Полоса пропускания: {bandwidth:.2e} Гц')

print("\nАНализ исходного скремблированного сообщения по методам Manchester и AMI:")

analyze_signal(manchester, "Manchester (скремблированный)")
analyze_signal(ami, "AMI (скремблированный)")

# Блок 7: "Построение графиков"

N = 32 # Ограничим кодирование для первых 4 байт (32 бита) согласно условию задания №2 

plt.figure()

plt.subplot(2, 1, 1)
plt.step(range(N), manchester[:N])
plt.title('Manchester (скремблированный)')
plt.grid()

plt.subplot(2, 1, 2)
plt.step(range(N), ami[:N])
plt.title('AMI (скремблированный)')
plt.grid()

plt.tight_layout()
plt.show()

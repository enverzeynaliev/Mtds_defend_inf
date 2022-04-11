# шифрование методом элептических кривых
# -*- coding: utf-8 -*-


def get_inverse_element(value, max_value):
    """
         Вычислить обратное значение между 1-max_value
    """
    for i in range(1, max_value):
        if (i * value) % max_value == 1:
            return i
    return -1


def gcd_x_y(x, y):
    """
         Вычислить наибольший общий делитель
    """
    if y == 0:
        return x
    else:
        return gcd_x_y(y, x % y)


def calculate_p_q(x1, y1, x2, y2, a, p):
    """
         Вычислить p + q
    """
    flag = 1  # Определить бит знака
    if x1 == x2 and y1 == y2:
        member = 3 * (x1 ** 2) + a  # Числитель
        denominator = 2 * y1  # Рассчитать знаменатель
    else:
        member = y2 - y1
        denominator = x2 - x1
        if member * denominator < 0:
            flag = 0
            member = abs(member)
            denominator = abs(denominator)

    # Упростить числитель и знаменатель
    gcd_value = gcd_x_y(member, denominator)
    member = int(member / gcd_value)
    denominator = int(denominator / gcd_value)
    # Найти обратный знаменатель
    inverse_value = get_inverse_element(denominator, p)
    k = (member * inverse_value)
    if flag == 0:
        k = -k
    k = k % p
    # Рассчитать х3, у3
    x3 = (k ** 2 - x1 - x2) % p
    y3 = (k * (x1 - x3) - y1) % p
    # print("%d<=====>%d" % (x3, y3))
    return [x3, y3]


def get_order(x0, y0, a, b, p):
    """
         Рассчитать порядок эллиптической кривой
    """
    # Расчет-р
    x1 = x0
    y1 = (-1 * y0) % p
    temp_x = x0
    temp_y = y0
    n = 1
    while True:
        n += 1
        p_value = calculate_p_q(temp_x, temp_y, x0, y0, a, p)
        if p_value[0] == x1 and p_value[1] == y1:
            print("========== Степень эллиптической кривой равна% d =========" % (n + 1))
            return n + 1

        temp_x = p_value[0]
        temp_y = p_value[1]

    # print("%d-%d-%d-%d" % (x0,y0,x1,y1))


def get_x0_y0_x1_y1(x0, a, b, p):
    """
         Рассчитайте p и -p
    """
    y0 = -1
    for i in range(0, p):
        if i ** 2 % p == (x0 ** 3 + a * x0 + b) % p:
            y0 = i
            break

    # Если y0 не найден, вернуть False
    if y0 == -1:
        return False
    # Расчет-у
    x1 = x0
    y1 = -1 * y0 % p
    # print("%d-%d-%d-%d" % (x0,y0,x1,y1))
    return [x0, y0, x1, y1]


def draw_graph(a, b, p):
    """
         Выходной хеш
    """
    x_y = []
    for i in range(p):
        x_y.append(["-" for i in range(p)])

    for i in range(p):
        value = get_x0_y0_x1_y1(i, a, b, p)
        if value:
            x0 = value[0]
            y0 = value[1]
            x1 = value[2]
            y1 = value[3]
            # print("%d-%d-%d-%d" % (x0,y0,x1,y1))
            x_y[x0][y0] = 1
            x_y[x1][y1] = 1
    print("Хэш - диаграмма эллиптической кривой:")
    for j in range(p):
        if p - 1 - j >= 10:
            print(p - 1 - j, end=" ")
        else:
            print(p - 1 - j, end="  ")
        for i in range(p):
            print(x_y[i][p - j - 1], end="  ")
        print()
    print("   ", end="")
    for i in range(p):
        if i >= 10:
            print(i, end=" ")
        else:
            print(i, end="  ")

    print()


def calculate_np(G_x, G_y, private_key, a, p):
    """
         Рассчитать нг
    """
    global p_value
    temp_x = G_x
    temp_y = G_y
    while private_key != 1:
        p_value = calculate_p_q(temp_x, temp_y, G_x, G_y, a, p)
        temp_x = p_value[0]
        temp_y = p_value[1]
        private_key -= 1
    return p_value

def ecc_encrypt_and_decrypt():
    while True:
        a = int(input("Пожалуйста, введите параметр a эллиптической кривой:"))
        b = int(input("Пожалуйста, введите параметр b эллиптической кривой:"))
        p = int(input("Пожалуйста, введите параметр p эллиптической кривой(p - простое число):"))

        if (4 * (a ** 3) + 27 * (b ** 2)) % p == 0:  # формула 8.2(проверка правильности ключей)
            print(
                "Выбранная эллиптическая кривая не может быть использована для шифрования, пожалуйста, выберите заново \ n")
        else:
            break
    # Вывести график рассеяния эллиптической кривой
    draw_graph(a, b, p)
    print("Выберите точку в качестве генератора G на картинке выше")
    G_x = int(input("Выбранная вами абсцисса G_x:"))
    G_y = int(input("Ордината, которую вы выбрали G_y:"))
    # Получить порядок эллиптической кривой
    n = get_order(G_x, G_y, a, b, p)
    # Получить закрытый ключ и ключ <порядок эллиптической кривой n
    private_key = int(input("Введите закрытый ключ (<% d):" % n))
    # Рассчитать открытый ключ нг
    Q = calculate_np(G_x, G_y, private_key, a, p)
    print(
        "====== Создать открытый ключ {a =% d, b =% d, p =% d, заказ% d, G (% d,% d) , Q (% d,% d)} ====== " % (
            a, b, p, n, G_x, G_y, Q[0], Q[1]))

    # Начало шифрования
    k = int(input("Пожалуйста, дайте целое число( < % d):" % n))
    k_G = calculate_np(G_x, G_y, k, a, p)  # Рассчитать кг
    k_Q = calculate_np(Q[0], Q[1], k, a, p)  # Рассчитать kQ
    plain_text = int(input("Пожалуйста, введите простой текст для шифрования:"))
    cipher_text = plain_text * k_Q[0]  # Рассчитать произведение простого текста и абсциссы kQ
    # Зашифрованный текст
    C = [k_G[0], k_G[1], cipher_text]
    print("Зашифрованный  текст: {(% d, % d), % d}" % (C[0], C[1], C[2]))
    # Расшифровать
    # Рассчитать private_key * кг
    decrypto_text = calculate_np(C[0], C[1], private_key, a, p)

    inverse_value = get_inverse_element(decrypto_text[0], p)
    m = C[2] * inverse_value % p
    print("Расшифрованный открытый текст% d" % m)


if __name__ == '__main__':
    ecc_encrypt_and_decrypt()

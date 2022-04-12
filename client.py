from server import DH_Endpoint

message = input("Введите текст: ")
a = 194  # по варианту публичный ключ первого пользователя s_public
x = 156 # по варианту приватный ключ первого пользователя  s _private
b = 145  # по варианту публичный ключ второго пользователя m_public
y = 112  # по варианту приватный ключ второго пользователя m _private
k1 = 1 # по варианту
k2 = 1 # по варианту
user_1 = DH_Endpoint(a, b, x)
user_2 = DH_Endpoint(a, b, y)

u1_partial = user_1.generate_partial_key()  #полученный защищенный ключ первого пользователя s _partial
# print(u1_partial)

u2_partial = user_2.generate_partial_key()  #полученный защищенный ключ второго пользователя m _partial
# print(u2_partial)

first_user_full = user_1.generate_full_key(u2_partial)
# print(first_user_full)
m_full = user_2.generate_full_key(u1_partial)
# print(m_full)

msg_encrypted = user_2.encrypt_message(message)
print(msg_encrypted)

message = user_1.decrypt_message(msg_encrypted)
print(message)

import ctypes

# Загрузка библиотеки
cfunctions = ctypes.CDLL('./libcfunctions.so')


# Указываем, что функция возвращает int
cfunctions.func_ret_int.restype = ctypes.c_int
# Указываем, что функция принимает аргумент int
cfunctions.func_ret_int.argtypes = [ctypes.c_int, ]

# Указываем, что функция возвращает double
cfunctions.func_ret_double.restype = ctypes.c_double
# Указываем, что функция принимает аргумент double
cfunctions.func_ret_double.argtypes = [ctypes.c_double]

# Указываем, что функция возвращает char *
cfunctions.func_ret_str.restype = ctypes.c_char_p
# Указываем, что функция принимает аргумент char *
cfunctions.func_ret_str.argtypes = [ctypes.POINTER(ctypes.c_char), ]

# Указываем, что функция возвращает char
cfunctions.func_many_args.restype = ctypes.c_char
# Указываем, что функция принимает аргументы int, double. char, short
cfunctions.func_many_args.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_char, ctypes.c_short]


#print('ret func_ret_int: ', test.func_ret_int(101))
#print('ret func_ret_double_py: ', test.func_ret_double(12.123456789))


def fun_r_d(inp):
    return cfunctions.func_ret_double(inp)

def fun_r_i(inp):
    return cfunctions.func_ret_int(inp)
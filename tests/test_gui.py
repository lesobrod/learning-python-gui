from src.gui import *
import random
import types

"""
Для проверки GUI в данном модуле мы заменяем get_user_data на 
генератор случайных чисел и смотрим, как это выглядит.
Не обращаясь к API.
Для данной замены нужен трюк с types.MethodType
"""


def rnd_data(self):
    return [random.uniform(-20, 20) for _ in range(300)]

test_root = MyApp()
test_root.get_user_data = types.MethodType(rnd_data, test_root)
test_root.info_label['text'] = 'TEST MODE'
test_root.mainloop()


"""
Задача 1: Уникальные посетители сайта
Есть список ID посетителей сайта. Некоторые заходили несколько раз.
Нужно:
- Найти всех уникальных посетителей
- Посчитать, сколько раз каждый заходил на сайт
- Найти самого активного посетителя
"""
from collections import Counter

# Исходные данные: лог посещений сайта
visits = ["user123", "user456", "user123", "user789", 
          "user456", "user123", "user999", "user456", "user123"]

# def get_unique_users(visits):
#     unique_users = []   
#     for visit in visits:
#         if visit not in unique_users:
#             unique_users.append(visit)
        
#     print(unique_users)
#     return unique_users


# assert get_unique_users(visits) == ['user123', 'user456', 'user789', 'user999']


unique_users = set(visits)
print(unique_users)


visit_counts = Counter(visits) # Counter — это специальный класс из модуля collections
# в Python. Он предназначен для быстрого подсчета частоты встречаемости элементов 
# в итерируемом объекте (например, списке, строке или кортеже).
unique_users = list(visit_counts.keys()) # извлекает уникальные ключи 
#из объекта Counter (или обычного словаря) 
# и преобразует их в список.
active_visitors = max(visit_counts, key=visit_counts.get) # находит ключ (элемент) 
# с максимальным значением в объекте Counter (или словаре) visit_counts
# Метод .get(key) для словаря. Возвращает значение по ключу, 
# или 0 если ключа нет. Работает как функция visit_counts.get(key)
print(unique_users)
print(dict(visit_counts))
print(active_visitors, visit_counts[active_visitors])

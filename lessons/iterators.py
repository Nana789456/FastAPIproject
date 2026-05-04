# n_start = 3
# n_end = 6



# class MyRange:
#     def __init__(self, n_start, n_end):
#         self.n_end = n_end
#         self.current = n_start

#     def __iter__(self):
#         return self
    
#     def __next__(self):
#         if self.current < self.n_end:
#             value = self.current
#             self.current += 1
#             return value
#         else:
#             return 'Итеррирование завершено'
        
# iterator = iter(MyRange(n_start, n_end))
# print(type(iterator))

# n_start = 3
# n_end = 6
# iterator = iter(MyRange(n_start, n_end))
# print(next(iterator))
# print(next(iterator))
# print(next(iterator))
# print(next(iterator))


# class FileReaderCleaner:
#     def __init__(self, filename):
#         self.file = open(filename)

#     def __iter__(self):
#         return self

#     def __next__(self):
#         line = self.file.readline()
#         if line:
#             return line.strip()
#         else:
#             self.file.close()
#             raise StopIteration
        
# for line in FileReaderCleaner('lessons/text.txt'):
#     print(line)



    # Напиши класс-итератор Countdown, который будет принимать число n и при итерации 
# возвращать четные числа от n до 0 включительно , а затем выводить "Финиш".

# for i in Countdown(3):
#     print(i)
# Ожидаемый вывод:
# 3
# 2
# 1
# Пуск!
n_start = 8
n_end = 0


class Countdown:
    def __init__(self, n_start, n_end):
        self.n_end = n_end
        self.current = n_start

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current >= self.n_end:
            value = self.current
            self.current -= 2
            print(value)
            return value
       
        else:
            print('Финиш')
            return 'Финиш'
        
iterator = iter(Countdown(n_start, n_end))
print(type(iterator))

next(iterator)
next(iterator)
next(iterator)
next(iterator)
next(iterator)
next(iterator)
# print(next(iterator))
# print(next(iterator))
# print(next(iterator))
# print(next(iterator))
# print(next(iterator))

# n = 8

# class Countdown:
#     def __init__(self, n):
#         self.n = n
#         # Начинаем с ближайшего четного числа, не превышающего n
#         self.current = n if n % 2 == 0 else n - 1
#         if self.current < 0:
#             self.current = 0  # Для случаев, если n < 0, но предполагаем n >= 0

#     def __iter__(self):
#         return self

#     def __next__(self):
#         if self.current < 0:
#             print("Финиш")
#             raise StopIteration
#         else:
#             value = self.current
#             self.current -= 2
#             return value


# Итеририруемые объекты: списки, кортежи, множества, словари, строка

# Строка тоже итерируемый объект
# for i in '123':
#     print(i)


# Задание: доработать MyRange, чтобы мог работать с интервалами
# class MyRange:
#     def __init__(self, n):
#         self.n = n
#         self.current = 0

#     def __iter__(self):
#         return self
    
#     def __next__(self):
#         if self.current < self.n:
#             value = self.current
#             self.current += 1
#             return value
#         else:
#             raise StopIteration

# n = 3
# iterator = iter(MyRange(n))
# print(type(iterator))
# print(next(iterator))
# print(next(iterator))
# print(next(iterator))


# n_start = 3
# n_end = 6
# iterator = iter(MyRange(n_start, n_end))


# class Countdown:
#     def __init__(self, filename):
#         self.file = open(filename)

#     def __iter__(self):
#         return self

#     def __next__(self):
#         line = self.file.readline()
#         if line:
#             return line
#         else:
#             self.file.close()
#             raise StopIteration
        
# for line in FileReader('lessons/text.txt'):
#     print(line)

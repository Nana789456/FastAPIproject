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
            print(value)
            self.current -= 2
            print(next(self))
            # print(value)
            return value
       
        else:
            # print('Финиш')
            return 'Финиш'
        
iterator = iter(Countdown(n_start, n_end))
print(type(iterator))

next(iterator)


# def countdown(n):
#     if n < 0:  
#         print("Финиш")
#         return
#     else:
#         print(n)  
#         countdown(n - 1)


# countdown(5)


numbers = [1, 2, 3, 4, 5]
squares = [x ** 2 for x in numbers]
print(squares)  # Вывод: [1, 4, 9, 16, 25]


numbers = [1, 2, 3, 4, 5, 6]
evens = [x for x in numbers if x % 2 == 0]
print(evens)  # Вывод: [2, 4, 6]



evens =[]
for x in numbers:
    if x % 2 == 0:
        evens.append(x) 
    
(x for x in numbers if x % 2 == 0)  # изучить что такое генератор

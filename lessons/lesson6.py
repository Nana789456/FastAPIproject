"""
Задача 1: Найти пользователя с наименьшим средним баллом
"""
users = {
    'user1':[3,1,2],
    'user2':[5,5,5],
    'user3':[5,4,5],
    'user4':[2,1,2],
}

def get_min_average_user(users: dict):
    min_user = ''
    min_avarage_value = float('inf')
    for user_name, user_marks in users.items():
        average = sum(user_marks)/ len(user_marks)
        if average < min_avarage_value:
            min_avarage_value = average
            min_user = user_name
    return min_user

print(get_min_average_user(users))
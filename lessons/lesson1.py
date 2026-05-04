user_marks = {
    'user1':[3,1,2],
    'user2':[5,5,5],
    'user3':[5,4,5],
    'user4':[2,1,2],
}

def get_average_value(key):
    marks = user_marks[key]  # [4,1,2]
    sum_marks = sum(marks)
    number_marks = len(marks)
    average = sum_marks / number_marks
    return average
    # return marks[0]

result = max(user_marks)
print(type(result), max(user_marks, key=get_average_value))

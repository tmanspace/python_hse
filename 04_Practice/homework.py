import re

def validate_car_number(car_id):
    pattern = r'^([АВЕКМНОРСТУХ])(\d{3})([АВЕКМНОРСТУХ]{2})(\d{2,3})$'
    
    match = re.match(pattern, car_id)
    
    if match:
        number = match.group(1) + match.group(2) + match.group(3)
        region = match.group(4)
        return f"Номер {number} валиден. Регион: {region}."
    else:
        return "Номер не валиден."

car_id1 = 'А222ВС96'
car_id2 = 'АБ22ВВ193'

print(validate_car_number(car_id1)) 
print(validate_car_number(car_id2))  


def remove_repeated_words(foo):
    pattern = r'\b(\w+)(\s+\1)+\b'
    result = re.sub(pattern, r'\1', foo)
    return result

example = 'Напишите функцию функцию, которая будет будет будет будет удалять все все все все последовательные повторы слов из из из из заданной строки строки при помощи регулярных выражений'
result = remove_repeated_words(example)
print(result)
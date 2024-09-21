
# Task 1
# word = test Результат: es
# word = testing Результат: t

# ZAD 3

ids = {
    'user1': [213, 213, 213, 15, 213],
    'user2': [54, 54, 119, 119, 119],
    'user3': [213, 98, 98, 35],
    }

def get_unique_ids(user_ids: dict[str, int]) -> set[int]:
    res = set()
    for id_list in user_ids.values():
        res.update(id_list)
    return res

print('Результат:')
print(get_unique_ids(ids))

# Результат: {98, 35, 15, 213, 54, 119}

queries = [
    'смотреть сериалы онлайн',
    'новости спорта',
    'афиша кино',
    'курс доллара',
    'сериалы этим летом',
    'курс по питону',
    'сериалы про спорт',
]

def get_queries_dis_str(queries: list[str]) -> str:
    result = {}
    queries_len = len(queries)
    for q in queries:
        query_len = len(q.split(' '))
        if not result.get(query_len):
            result[query_len] = 0
        result[query_len] += 1
    res_str = ['Результат']
    for k, _ in result.items():
        result[k] = result[k] / queries_len * 100
        res_str.append(f'Поисковых запросов, содержащих {k} слов(а): {result[k]:.2f}')
    return '\n'.join(res_str)

print(get_queries_dis_str(queries))    

# Результат:
# Поисковых запросов, содержащих 2 слов(а): 42.86%
# Поисковых запросов, содержащих 3 слов(а): 57.14%
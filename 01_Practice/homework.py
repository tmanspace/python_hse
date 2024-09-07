from json import loads
from csv import reader, writer, QUOTE_MINIMAL


FUNNEL_PATH: str = 'src/funnel.csv'
PURCHASE_SRC: str = 'src/purchase_log.txt'
COLS = 3


def get_purchases(src: str):
    temp = {}
    with open(src, 'r') as f:
        f.readline()
        for line in f:
            row = loads(line)
            temp[row['user_id']] = row['category']
    return temp

def show_first_n_strokes_dict(number: int, data: dict):
    for k, v in data.items():
        if not number:
            return
        print(k, v)
        number -= 1

def show_first_n_strokes_csv_as_str(number: int, src: str, delimeter: str = ','):
     with open(src, encoding='utf-8') as f:
        funnel = reader(f, delimiter=';', quotechar='|')
        for row in funnel:
            print(','.join(row))
            number -= 1
            if not number: return


def show_first_n_strokes_csv(number: int, src: str):
     with open(src, encoding='utf-8') as f:
        funnel = reader(f, delimiter=';', quotechar='|')
        for row in funnel:
            print(*row)
            number -= 1
            if not number: return


def main():
    purchases: dict[str, str] = get_purchases(PURCHASE_SRC)
    show_first_n_strokes_dict(3, purchases)

    
    funnel_f = open(FUNNEL_PATH, 'w', encoding='utf-8')
    funnel_csv = writer(funnel_f, delimiter=';', quotechar='|', quoting=QUOTE_MINIMAL)

    with open('src/visit_log.csv', encoding='utf-8', newline='') as csvfile:
        visit_log = reader(csvfile, delimiter=';', quotechar='|')

        row = next(visit_log)
        row[2] = 'category'
        funnel_csv.writerow(row[:COLS])

        for row in visit_log:
            category =  purchases.get(row[0], None)
            if category:
                row[2] = category
                funnel_csv.writerow(row[:COLS])

    funnel_f.close()

    show_first_n_strokes_csv_as_str(3, FUNNEL_PATH)

if __name__ == '__main__':
    main()



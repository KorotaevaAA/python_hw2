import csv


def open_and_reformat_csv_file(file_for_open_name: str):
    """Open, read csv file and save it as list of dictionaries"""
    reformat_data = []
    with open(file_for_open_name, newline='') as csv_file:
        data_from_file = csv.DictReader(csv_file, delimiter=';')
        for r in data_from_file:
            reformat_data.append(r)
    return reformat_data


def get_len_min_max_and_avg_from_list(a: list):
    """Get length of list, min, max and avg of list's elements"""
    list_min = a[0]
    list_max = a[0]
    list_sum = a[0]
    for i in a:
        if i != a[0]:
            list_sum += i
            if i < list_min:
                list_min = i
            if i > list_max:
                list_max = i
    return [len(a), list_min, list_max, round(list_sum / len(a))]


def ask_what_to_do(file_data):
    """Give user a choice and run needed function"""
    print('Что хотим сделать?')
    option = 0
    options = {1: 'Вывести иерархию команд', 2: 'Вывести сводный отчет', 3: 'Сохранить сводный отчет', 4: 'Выйти'}
    for k, v in options.items():
        print(f'{k} - {v}')
    while option not in options:
        print('Выберите: {}, {}, {} или {}?'.format(*options))
        option = int(input())
    if option == 1:
        print_command_department(file_data)
    elif option == 2:
        print_report(file_data)
    elif option == 3:
        save_report(file_data)
    else:
        return 0


def print_command_department(file_data):
    """Print department and all its command"""
    department_dict = {}
    for row in file_data:
        department = row.get('Департамент')
        department_dict[department] = set()

    for row in file_data:
        department = row.get('Департамент')
        command = row.get('Отдел')
        department_dict[department].add(command)
    print('Иерархия команд')
    for department in department_dict:
        all_command = ', '.join(command for command in department_dict[department])
        print(f'{department}: {all_command}')
    print('')
    ask_what_to_do(file_data)


def create_data_for_report(file_data):
    """Create data for report as dictionary format"""
    department_dict = {}
    for row in file_data:
        department = row.get('Департамент')
        department_dict[department] = []

    for row in file_data:
        department = row.get('Департамент')
        salary = row.get('Оклад')
        department_dict[department].append(int(salary))

    for department in department_dict:
        department_dict[department] = get_len_min_max_and_avg_from_list(department_dict[department])
    return department_dict


def print_report(file_data):
    """Print report"""
    dict_for_print = create_data_for_report(file_data)
    print('Отчет')
    for department in dict_for_print:
        print(f'{department}:')
        print('Численность - ', dict_for_print[department][0])
        print(f'Вилка зарплат- от {dict_for_print[department][1]} '
              f'до {dict_for_print[department][2]}')
        print('Средний оклад - ', dict_for_print[department][3])
        print('')
    print('')
    ask_what_to_do(file_data)


def save_report(file_data):
    """Save report as scv file"""
    dict_for_save = create_data_for_report(file_data)
    header_fields = (
        'Департамент',
        'Численность',
        'Минимальный оклад',
        'Максимальный оклад',
        'Средний оклад',
    )
    with open('Report.csv', 'w') as f:
        out_file = csv.writer(f, delimiter=';')
        out_file.writerow(header_fields)
        for department in dict_for_save:
            out_file.writerow((
                department,
                dict_for_save[department][0],
                dict_for_save[department][1],
                dict_for_save[department][2],
                dict_for_save[department][3],
            ))

    print('Файл сохранен')
    print('')
    ask_what_to_do(file_data)


print('Введите название файла:')
csv_file_name = input()
data = open_and_reformat_csv_file(file_for_open_name=csv_file_name)
ask_what_to_do(data)

import csv


def read_csv_file(file_for_open_name: str):
    """Open, read csv file and save it as list of dictionaries"""
    reformat_data = []
    with open(file_for_open_name, newline='') as csv_file:
        data_from_file = csv.DictReader(csv_file, delimiter=';')
        for r in data_from_file:
            reformat_data.append(r)
    return reformat_data


def ask_what_to_do(file_data):
    """Give user a choice and run needed function"""
    print('Что хотим сделать?')
    option = '0'
    options = {'1': 'Вывести иерархию команд', '2': 'Вывести сводный отчет',
               '3': 'Сохранить сводный отчет', '4': 'Выйти'}
    for k, v in options.items():
        print(f'{k} - {v}')
    while option not in options:
        print('Выберите: {}, {}, {} или {}?'.format(*options))
        option = input()
    if option == '1':
        print_command_department(file_data)
    elif option == '2':
        print_report(file_data)
    elif option == '3':
        save_report(file_data)


def print_command_department(file_data):
    """Print department and all its command"""
    department_dict = {}
    for row in file_data:
        department = row['Департамент']
        command = row['Отдел']
        department_dict.setdefault(department, set())
        department_dict[department].add(command)
    print('Иерархия команд')
    for department in department_dict:
        all_command = ', '.join(department_dict[department])
        print(f'{department}: {all_command}')
    print('')
    ask_what_to_do(file_data)


def get_department_stat(name_of_department: str, list_of_department_salaries: list):
    """Get count of department, min, max and avg salary"""
    min_salary = 1000000  # list_of_department_salaries[0]
    max_salary = 0  # list_of_department_salaries[0]
    sum_of_salary = 0
    for salary in list_of_department_salaries:
        sum_of_salary += salary
        if salary < min_salary:
            min_salary = salary
        if salary > max_salary:
            max_salary = salary
    return {'Департамент': name_of_department,
            'Численность': len(list_of_department_salaries),
            'Минимальный оклад': min_salary,
            'Максимальный оклад': max_salary,
            'Средний оклад': round(sum_of_salary / len(list_of_department_salaries))}


def create_data_for_report(file_data):
    """Create data for report as dictionary format"""
    department_dict = {}
    for row in file_data:
        department = row['Департамент']
        salary = row['Оклад']
        department_dict.setdefault(department, [])
        department_dict[department].append(int(salary))
    stat_list_of_dict = []
    for department_name, salaries in department_dict.items():
        stat_list_of_dict.append(get_department_stat(department_name, salaries))
    return stat_list_of_dict


def print_report(file_data):
    """Print report"""
    list_for_print = create_data_for_report(file_data)
    print('Отчет')
    for department_stat_dict in list_for_print:
        for key, value in department_stat_dict.items():
            print(f'{key}: {value}')
        print('')
    print('')
    ask_what_to_do(file_data)


def save_report(file_data):
    """Save report as scv file"""
    list_for_save = create_data_for_report(file_data)
    header_fields = (
        'Департамент',
        'Численность',
        'Минимальный оклад',
        'Максимальный оклад',
        'Средний оклад',
    )
    with open('Report.csv', 'w', encoding='utf-8', newline='') as f:  
        out_file = csv.DictWriter(f, fieldnames=header_fields, delimiter=';')
        out_file.writeheader()
        for department_stat_dict in list_for_save:
            out_file.writerow(department_stat_dict)

    print('Файл сохранен')
    print('')
    ask_what_to_do(file_data)


if __name__ == '__main__':
    print('Введите название файла:')
    csv_file_name = input()
    data = read_csv_file(file_for_open_name=csv_file_name)
    ask_what_to_do(data)

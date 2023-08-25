import os
import random
import shutil


# класс таблицы, где реализованы все необходимые функции для работы с ней
class Table:
    def __init__(self, name):
        # переменная, которая хранит имя таблицы, и переменная, в которой хрянятся все данные из таблицы
        self.name_of_table = name
        self.list_of_data = []

        # параметр нужен только для того, чтобы при создании нового элемента не получилось 2 элемента с одинаковым id
        self.count = 0

        # сразу при инициализации создаем файл таблицы, для удобства
        table = open(self.name_of_table + '.txt', 'w', encoding='utf-8')

    # функция, которая заполняет таблицу данными из другой таблицы
    def fill_table_from_file(self, data):
        file = open(data, 'r', encoding='utf-8')
        data_from_file = file.readlines()
        data_from_file = [x.rstrip() for x in data_from_file]
        self.list_of_data = [[str(x + 1), data_from_file[x]] for x in range(len(data_from_file))]
        self.count += len(data_from_file)
        # print("The table has been filled in successfully!")

    # функция, которая позволяет заполнить таблицу данными из двух других (только для testing_table)
    def fill_table_by_hand(self, list_1, list_2):
        self.list_of_data = [[list_1[x][0], random.choice(list_2)[0]] for x in range(len(list_1))]
        self.count += len(list_1)
        # print("The table has been filled in successfully!")

    # функция, которая экспортирует таблицу в файл .txt
    def export_table(self):
        table = open(self.name_of_table + '.txt', 'w', encoding='utf-8')
        for x in self.list_of_data:
            table.write(' '.join(x) + '\n')
        # print("The table has been successfully exported to a file -", self.name_of_table + '.txt')

    # функция, которая добавляет элемент в таблицу
    def add_elem(self, elem):
        if elem not in [x[1] for x in self.list_of_data]:
            self.list_of_data.append([str(self.count + 1), elem])
            self.count += 1
            print("The line was successfully added!")
            return True
        else:
            print("This element is already in the table . . .")
            return False

    # только для добавления строки в testing table
    def add_elem_by_hand(self, elem1, elem2):
        self.list_of_data.append([elem1, elem2])
        self.count += 1

    # функция, которая удаляет элемент из таблицы
    def delete_elem(self, id):
        for i in range(len(self.list_of_data)):
            if self.list_of_data[i][0] == id:
                del self.list_of_data[i]
                print("The item was successfully removed from the table!")
                return True
        else:
            print("There is no such element in the table . . .")
            return False

    # функция, которая редактирует элемент в таблице
    def edit_elem(self, id):
        id = str(id)
        for i in range(len(self.list_of_data)):
            if self.list_of_data[i][0] == id:
                print("You are changing an element:\n" + ' | '.join(self.list_of_data[i]))
                print("Please enter the new content of the item:")
                string = input()
                if string not in [x[1] for x in self.list_of_data]:
                    self.list_of_data[i] = [id, string]
                    print("The item has been successfully modified!")
                else:
                    print("This element is already in the table . . .")
                break
        else:
            print("There is no such element in the table . . .")

    # функция, которая выводит в консоль 1 элемент из таблицы
    def print_elem(self, id):
        for i in range(len(self.list_of_data)):
            if self.list_of_data[i][0] == id:
                print(' | '.join(self.list_of_data[i]))
                break
        else:
            print("There is no such element in the table . . .")

    # функция, которая выводит всю таблицу в консоль
    def print_table(self):
        print("id      data")
        for i in range(len(self.list_of_data)):
            print(' | '.join(self.list_of_data[i]), end='\n')
        print('\n')

    # функция, которая возвращает id некоторого элемента
    def get_id(self, elem):
        for x in self.list_of_data:
            if x[1] == elem:
                return x[0]
        else:
            print("There is no such element in the table . . .")

    # функция поиска элемента по id
    def find_elem(self, id):
        for x in self.list_of_data:
            if x[0] == id:
                return x[1]
        else:
            print("There is no such element in the table . . .")


# класс, который реализует работу базы данных
class DataBase:
    def __init__(self, name='', new=True):
        self.is_full = False
        # файл с именами всех баз данных, которые есть
        with open('all_db.txt', 'r', encoding='utf-8') as original:
            data = original.readlines()

        # если имя базы данных не было задано, то оно задается автоматически
        if name != '':
            self.name_of_db = name + '_db'
        else:
            self.name_of_db = str(len(data) + 1) + '_db'

        # обновляем файл со списком баз данных
        with open('all_db.txt', 'w', encoding='utf-8') as modified:
            for x in data:
                modified.write(x)
            if self.name_of_db not in data:
                modified.write('\n' + self.name_of_db)

        # создаем директорию под базу данных
        if not os.path.exists(self.name_of_db):
            try:
                os.mkdir(self.name_of_db)
            except OSError:
                print("Создать директорию не удалось")
            else:
                print("Успешно создана директория", self.name_of_db + " под базу данных!")

        if not new:
            # объявляем 3 переменные под таблицы
            self.students_table = 0
            self.variants_table = 0
            self.testing_table = 0
        else:
            # создаем 3 пустые таблицы
            self.students_table = Table(self.name_of_db + "/Students")
            self.variants_table = Table(self.name_of_db + "/Variants")
            self.testing_table = Table(self.name_of_db + "/Testing_table")

    # автоматически заполняем все 3 таблицы соответствующими данными
    def fill_db(self):
        # заполняем таблицу студентами
        self.students_table.fill_table_from_file('D:/Python/bd/names.txt')
        self.students_table.export_table()

        # заполняем таблицу вариантами
        self.variants_table.fill_table_from_file(create_variants(50))
        self.variants_table.export_table()

        # заполняем testing_table
        self.testing_table.fill_table_by_hand(self.students_table.list_of_data, self.variants_table.list_of_data)
        self.testing_table.export_table()

        self.is_full = True

    # функция для вывода каждого студента и его варианта в консоль
    def print_testing_table(self):
        for x in self.testing_table.list_of_data:
            print(self.students_table.find_elem(x[0]), '|', self.variants_table.find_elem(x[1]))

    # функция, которая возволяет сохранить текущую версию базы данных
    def save_db(self):
        new_name = self.name_of_db[:-3] + '(old_version)' + '_db'
        # создаем директорию под базу данных
        try:
            os.mkdir(new_name)
        except OSError:
            print("Создать директорию не удалось")
        else:
            print("Успешно создана директория", new_name + " под базу данных!")

        # копируем все таблицы
        shutil.copy(self.name_of_db + "/Students.txt", new_name + "/Students.txt")
        shutil.copy(self.name_of_db + "/Variants.txt", new_name + "/Variants.txt")
        shutil.copy(self.name_of_db + "/Testing_table.txt", new_name + "/Testing_table.txt")

    # функция, которая позволяет вернуться к старой версии
    def back_2_old_version(self):
        old_name = self.name_of_db[:-3] + '(old_version)' + '_db'
        if os.path.exists(old_name):
            # открываем таблицы старой версии базы данных и читаем данные от туда
            self.students_table = open_table(old_name + '/Students')
            self.students_table.name_of_table = self.name_of_db + '/Students'
            self.students_table.export_table()

            self.variants_table = open_table(old_name + '/Variants')
            self.variants_table.name_of_table = self.name_of_db + '/Variants'
            self.variants_table.export_table()

            self.testing_table = open_table(old_name + '/Testing_table')
            self.testing_table.name_of_table = self.name_of_db + '/Testing_table'
            self.testing_table.export_table()

            shutil.rmtree(old_name)
        else:
            print("Похоже, ты не сохранял предыдущую версию этой базы данных . . .")

    # при добавлении студента, нужно добавить его и в testing table
    def if_add_2_s(self, elem):
        if self.students_table.add_elem(elem):
            self.testing_table.add_elem_by_hand(self.students_table.get_id(elem),
                                                self.variants_table.get_id(random.choice(self.variants_table.list_of_data)[1]))

    # при удалении студента, нужно удалить его из testing table
    def if_del_f_s(self, id):
        if self.students_table.delete_elem(id):
            self.testing_table.delete_elem(id)

    # при удалении варианта, нужно убедиться в том, что студентам, к кого был этот вариант, был выдан новый вариант
    def if_del_f_v(self, id):
        if self.variants_table.delete_elem(id):
            for x in self.testing_table.list_of_data:
                if x[1] == id:
                    self.testing_table.delete_elem(x[0])
                    self.testing_table.add_elem_by_hand(x[0], random.choice(self.variants_table.list_of_data)[0])


# функция, которая генерирует варианты
def create_variants(size):
    file = open("var_" + str(size) + ".txt", "w")
    for i in range(size):
        file.write('C:/Users/User1/OneDrive/Variants/var' + str(i + 1) + '.pdf\n')
    return "var_" + str(size) + ".txt"


# функция, которая позволяет открыть таблицу, созданую ранее (напрмер, при прошлом исполнении программы)
def open_table(name):
    # открываем файл этой таблицы и считываем оттуда всю информацию
    file = open(name + '.txt', 'r', encoding='utf-8')
    data_from_file = file.readlines()
    data_from_file = [x.rstrip().split() for x in data_from_file]

    # создаем экземпляр класса таблицы и заполняем все переменные данными из таблицы
    table = Table(name)
    table.list_of_data = [[x[0], ' '.join(x[1:])] for x in data_from_file]
    table.count = max([int(x[0]) for x in data_from_file])
    return table


# функция, которая позволяет открыть базу данных, созданную ранее (например, при прошлом исполнении программы)
def open_db(name):
    if os.path.exists(name + '_db'):
        bd = DataBase(name, False)
        bd.students_table = open_table(bd.name_of_db + "/Students")
        bd.students_table.export_table()
        bd.variants_table = open_table(bd.name_of_db + "/Variants")
        bd.variants_table.export_table()
        bd.testing_table = open_table(bd.name_of_db + "/Testing_table")
        bd.testing_table.export_table()
        if open(bd.name_of_db + "/Testing_table.txt", 'r').readline():
            bd.is_full = True
        else:
            bd.is_full = False
        return bd
    else:
        print("Похоже, нет такой базы данных, поэтому я создал ее для тебя)")
        return DataBase(name)


# работа с таблицами
def change_db(db):
    print("\nЧто ты хотел изменить в базе данных?")
    while True:
        db.students_table.export_table()
        db.variants_table.export_table()
        db.testing_table.export_table()
        print("\n1 - добавить элемент в Students\n2 - удалить элемент из Students\n3 - изменить элемент в Students"
              "\n4 - вывести элемент из таблицы Students\n5 - добавить элемент в Variants"
              "\n6 - удалить элемент из Variants\n7 - изменить элемент в Variants"
              "\n8 - вывести элемент из таблицы Variants\n9 - вывести таблицу Students\n10 - вывести таблицу Variants"
              "\n11 - я закончил")
        command = input("Введи нужную цифру: ")
        if command == '1': db.if_add_2_s(input("Что добавим? : "))
        elif command == '2': db.if_del_f_s(input("Что удалим? (введите id элемента): "))
        elif command == '3': db.students_table.edit_elem(input("Что хотим поменять? (введите id элемента): "))
        elif command == '4': db.students_table.print_elem(input("Какой элемент вывести (введите id): "))
        elif command == '5': db.variants_table.add_elem(input("Что добавим? : "))
        elif command == '6': db.if_del_f_v(input("Что удалим? (введите id элемента): "))
        elif command == '7': db.variants_table.edit_elem(input("Что хотим поменять? (введите id элемента): "))
        elif command == '8': db.variants_table.print_elem(input("Какой элемент вывести (введите id): "))
        elif command == '9': db.students_table.print_table()
        elif command == '10': db.variants_table.print_table()
        elif command == '11': break
        else: print("Кажется, я тебя не понимаю . . .")


# работа с базой данных
def work_with_db(db):
    print("\nБаза данных " + db.name_of_db + " успешно открыта!")
    while True:
        db.students_table.export_table()
        db.variants_table.export_table()
        db.testing_table.export_table()
        print("\nЧто ты хочешь сделать?\n1 - заполнить базу данных информацией из файлов"
              "\n2 - вывести testing_table на экран\n3 - сохранить текущую версию\n4 - вернуться к старой версии"
                                               "\n5 - внести изменения в базу данных\n6 - я сделал все, что хотел!")
        command = input("Введи нужную цифру: ")
        if command == '1':
            if not db.is_full: db.fill_db()
            else: print("База данных уже заполнена информацией!")
        elif command == '2': db.print_testing_table()
        elif command == '3': db.save_db()
        elif command == '4': db.back_2_old_version()
        elif command == '5': change_db(db)
        elif command == '6':
            break
        else: print("Кажется, я тебя не понимаю . . .")


# старт программы
def start():
    while True:
        print("\nПривет, давай начнем работу!\nЧто ты хочешь сделать?\n1 - создать базу данных"
              "\n2 - открыть существующую базу данных\n0 - выйти")
        command = input("Введи нужную цифру: ")
        if command == '1': work_with_db(DataBase(input("Как назовем базу данных? ")))
        elif command == '2': work_with_db(open_db(input("Как называется база данных? ")))
        elif command == '0': break
        else: print("Кажется, я тебя не понимаю . . .")


if __name__ == '__main__':
    start()
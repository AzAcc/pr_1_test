import re
import sys
from optparse import OptionParser
from time import time
from random import randint, choice
from trans import trans


class fake_data():
    def __init__(self, pattern, region='ru'):
        self.pattern = pattern
        self.region = region
        self.sequence = sequence
        self.id = None
        self.last_name = None
        self.first_name = None
        self.sex = None
        self.country = None
        self.city = None
        self.date = None
        self.login = None
        self.email = None
        self.number = None
        self.first_name_translit = None
        self.second_name_translit = None

    def get_pattern():
        template = open(options.pattern).read()
        flag = False
        result = ""
        for char in template:
            if char == "%":
                if not flag:
                    char = "{"
                else:
                    char = "}"
                flag = not flag
            result += char
        return re.findall(r"%([a-zA-Z_]+)%", template), result

    def get_id(self, id_set, *args):
        while True:
            id = randint(100000000, 999999999)
            if id not in id_set:
                id_set.add(id)
                break
        self.id = id
        return self.id

    def get_sequence(self, *args):
        return self.sequence

    def get_first_name(self, *args):
        if self.sex is None:
            self.get_sex()
        self.first_name = choice(FIRST_NAMES[self.sex])
        return self.first_name

    def get_last_name(self, *args):
        if self.sex is None:
            self.get_sex()
        self.last_name = choice(SECOND_NAMES[self.sex])
        return self.last_name

    def get_sex(self, *args):
        self.sex = choice(["м", "ж"])
        return self.sex

    def get_country(self, *args):
        self.country = choice(list(country_city_names.keys()))
        return self.country

    def get_city(self, *args):
        if self.country is None:
            self.get_country()
        self.city = choice(country_city_names[self.country].split(","))
        return self.city

    def get_date(self, *args):
        self.date = str(randint(1, 31)) + '-' + str(randint(1, 12)) + '-' + str(randint(1996, 2020))
        return self.date

    def get_login(self, *args):
        if self.first_name_translit is None:
            self.to_translit()
        self.login = self.first_name_translit[0] + "." + self.last_name_translit
        return self.login

    def get_email(self, *args):
        if self.first_name_translit is None:
            self.to_translit()
        self.email = ''.join(
            [choice(list(self.first_name_translit + self.first_name_translit)) for x in range(12)]) + \
                     choice(email_domen_names)
        return self.email

    def get_number(self, *args):
        self.number = randint(1, 100)
        return self.number

    def to_translit(self, *args):
        if self.first_name is None:
            self.get_first_name()
        if self.last_name is None:
            self.get_first_name()
        self.first_name_translit = trans(self.first_name)
        self.last_name_translit = trans(self.last_name)

if __name__ == "__main__":
    # начало отсчёта работы программы
    start_time = time()
    # количество полей для записи
    number_to_write = options.num
    # множество id
    id_set = set()
    all_elements, pattern = get_pattern()
    pattern = pattern.rstrip() + '\n'
    # генерация значений в выходной файл
    my_file = None


    def get_pattern():
        template = open(options.pattern).read()
        flag = False
        result = ""
        for char in template:
            if char == "%":
                if not flag:
                    char = "{"
                else:
                    char = "}"
                flag = not flag
            result += char
        return re.findall(r"%([a-zA-Z_]+)%", template), result

    try:
        my_file = open(options.filename, 'w')

        for i in range(1, number_to_write + 1):
            elements = dict()
            record = Row.Record(i)
            for el in all_elements:
                elements[el] = getattr(record, "get_" + el)(id_set)

            # Вывод
            progress(i, number_to_write, stat='Loading')
            my_file.write(pattern.format(**elements))
    finally:
        if my_file is not None:
            my_file.close()

    print("Time spent: {0:4.4} sec".format(time() - start_time))






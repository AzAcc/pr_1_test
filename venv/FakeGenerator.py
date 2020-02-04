import re
import sys
from random import randint,choice
from trans import trans
from optparse import OptionParser
from time import time

#начало отсчёта работы программы
start_time = time()

# опции командной строки, можно получить при помощи -h
parser = OptionParser()
parser.add_option("-o", "--output", action="store", type="string", dest="filename", help="write result to output file")
parser.add_option("-r","--rows",action="store", type="int", dest="num", help="generate in output file this number lines")
parser.add_option("-t","--template",action="store", type="string", dest="pattern", help="read pattern from file")
(options, args) = parser.parse_args()

template = open(options.pattern).read()
# сепаратор для записи
separator = re.search(r"%.%", template).group(0)[1]
line_split= template.split(";")

#мужские имена
male_first_names = ["Александр", "Анатолий", "Алексей", "Антон", "Андрей", "Валерий", "Василий", "Виктор", "Виталий",
                    "Геннадий", "Дмитрий", "Иван", "Илья", "Максим", "Никита", "Семен", "Сергей", "Михаил", "Юрий", "Федор"]
#женские имена
female_first_names = ["Алина", "Алиса", "Анастасия", "Анна", "Арина", "Валерия", "Варвара", "Вероника", "Виктория", "Дарья",
                      "Диана", "Екатерина", "Елена", "Елизавета", "Ирина", "Кристина", "Ксения", "Маргарита", "Марина",
                      "Мария", "Милана", "Наталья", "Ольга", "Полина", "Светлана", "Татьяна", "Юлия"]
#фамилии
all_last_names = ["Смирнов", "Иванов", "Кузнецов", "Соколов", "Попов", "Лебедев", "Козлов", "Новиков", "Морозов", "Петров", "Волков",
              "Соловьёв", "Васильев", "Зайцев", "Павлов", "Семёнов", "Голубев", "Виноградов", "Богданов", "Воробьёв", "Фёдоров",
              "Михайлов", "Беляев", "Тарасов", "Белов"]
#страны и их города
country_city_names = {"Россия" : "Москва, Санк-Петербург, Казань, Уфа",
                      "Казахстан" : "Алма-Ата, Шымкент, Караганда, Актобе",
                      "Беларусь" : "Минск, Брест, Гомель, Бобруйск",
                      "Украина" : "Киев, Львов, Харьков, Луганск"}
#возможные домены почты
email_domen_names = ["gmail.com","yahoo.com","yandex.ru","mail.ru","free.fr","terra.com.br"]

#количество полей для записи
number_to_write = options.num
#множество id
id_set = set()

#шаблон для записи результата
result_pattern = ''
for item in line_split:
    result_pattern +="{"+item[1:-1]+"}"+f"{separator}"
result_pattern = result_pattern[0:-1]

# Открытие файла для записи или перезаписи
# if options.append != None:
#     my_file = open(str(options.filename),'a')
# else:
#     my_file = open(str(options.filename), 'w')
# my_file.write(template.replace("%","")+'\n')

#progress bar
def progress(count, total, stat=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', stat))
    sys.stdout.flush()
my_file = open(options.filename,"w")
#генерация значений в выходной файл
for i in range(1,number_to_write+1):
    #генерация случайного id
    while True:
        id = randint(100000000,999999999)
        if id not in id_set:
            id_set.add(id)
            break
    #генерация случайного пола
    sex = choice(["м","ж"])
    #генерация sequence в файле
    sequence = i
    #генерация случайного имени в зависимости от пола
    if sex == "м":
        first_name = choice(male_first_names)
        last_name = choice(all_last_names)
    else:
        first_name = choice(female_first_names)
        last_name = choice(all_last_names)+"a"

    #перевод имени в транслит
    first_name_translit = trans(first_name)
    last_name_translit = trans(last_name)
    #генерация случайной страны
    country = choice(list(country_city_names.keys()))
    # генерация случайного города в зависимости от страны
    city = choice(country_city_names[country].split(","))
    # генерация случайной даты
    date = str(randint(1,31)) + '-' + str(randint(1,12)) + '-' + str(randint(1996,2020))
    # генерация случайного email
    email = ''.join([choice(list(first_name_translit+last_name_translit)) for x in range(randint(4,12))])+"@"+choice(email_domen_names)
    # генерация транслитной записи - первая буква имени плюс фамилия
    translit = first_name_translit[0]+"."+last_name_translit
    # генерация случайного целого значения
    value_of_type = randint(1,100)
    result_line = f"{result_pattern}".format(id=id, sequence=sequence, first_name=first_name, last_name=last_name, sex=sex,
                                     country=country, city=city, date=date, translit=translit, email=email,
                                     value_of_type=value_of_type)
    #Вывод
    progress(i, number_to_write, stat='Loading')
    my_file.write(result_line+'\n')
my_file.close()
print(f"\nTask runs in {time() - start_time} seconds ")
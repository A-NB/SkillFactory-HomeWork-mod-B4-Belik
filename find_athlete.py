# импортируем модули стандартнй библиотеки uuid и datetime
import uuid
import datetime

# импортируем библиотеку sqlalchemy и некоторые функции из нее 
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# константа, указывающая способ соединения с базой данных
DB_PATH = "sqlite:///sochi_athletes.sqlite3"
# базовый класс моделей таблиц
Base = declarative_base()

# Задание 2
# Напишите модуль find_athlete.py поиска ближайшего к пользователю атлета. Логика работы модуля такова:
#     запросить идентификатор пользователя;
#     если пользователь с таким идентификатором существует в таблице user, то вывести на экран двух атлетов: ближайшего по дате рождения к данному пользователю и ближайшего по росту к данному пользователю;
#     если пользователя с таким идентификатором нет, вывести соответствующее сообщение.

# Структура таблиц в базе sochi_athletes.sqlite3
# CREATE TABLE athelete("id" integer primary key autoincrement, "age" integer,"birthdate" text,"gender" text,"height" real,"name" text,"weight" integer,"gold_medals" integer,"silver_medals" integer,"bronze_medals" integer,"total_medals" integer,"sport" text,"country" text);
# CREATE TABLE sqlite_sequence(name,seq);
# CREATE TABLE user("id" integer primary key autoincrement, "age" text, "birthdate" text, "gender" text, "height" text, "birthdate" text, "height" real);

class User(Base):
    """
    Описывает структуру таблицы user для хранения регистрационных данных пользователей
    """
    # задаем название таблицы
    __tablename__ = 'user'
    # идентификатор пользователя, первичный ключ
    id = sa.Column(sa.Integer, primary_key=True)
    # имя пользователя
    first_name = sa.Column(sa.Text)
    # фамилия пользователя
    last_name = sa.Column(sa.Text)
    # пол пользователя
    gender = sa.Column(sa.Text)    
    # адрес электронной почты пользователя
    email = sa.Column(sa.Text)
    # дата рождения пользователя
    birthdate = sa.Column(sa.Text)
    # рост пользователя в сантиметрах
    height = sa.Column(sa.Float)  

class Athelete(Base):
    """
    Описывает структуру таблицы athelete для хранения информации об атлетах
    """
    # задаём название таблицы
    __tablename__ = 'athelete'
    # идентификатор атлета, первичный ключ
    id = sa.Column(sa.Integer, primary_key=True)
    # возраст атлета
    age = sa.Column(sa.Integer)
    # дата рождения атлета
    birthdate = sa.Column(sa.Text)
    # пол атлета
    gender = sa.Column(sa.Text) 
    # рост атлета в сантиметрах
    height = sa.Column(sa.Float)       
    # имя атлета
    name = sa.Column(sa.Text)
    # вес атлета
    weight = sa.Column(sa.Integer)
    # количество завоёваннных золотых медалей
    gold_medals = sa.Column(sa.Integer)
    # количество завоёваннных серебряных медалей
    silver_medals = sa.Column(sa.Integer)
    # количество завоёваннных бронзовых медалей
    bronze_medals = sa.Column(sa.Integer)
    # общее количество завоёваннных медалей
    total_medals = sa.Column(sa.Integer) 
    # вид спорта
    sport = sa.Column(sa.Text)
    # страна
    country = sa.Column(sa.Text)                       

def connect_db():
    """
    Устанавливает соединение с базой данных, создаёт таблицы, если их ещё нет и возвращает объект сессии 
    """
    # создаём соединение с базой данных
    engine = sa.create_engine(DB_PATH)
    # создаём описанные таблицы
    Base.metadata.create_all(engine)
    # создаём фабрику сессий
    session = sessionmaker(engine)
    # возвращаем сессию
    return session()

def date_diff(d1, d2):
    """
    Вычисляет разность между двумя датами 
    """ 
    # Превращаем даты в целые числа путём разделения строк с датами на части, отбрасывая символы "-", сцепляя части в одну строку методом .join с последующим преобразованием при помощи встроенной функции int. Например, дата, имеющая строковое представление '1989-05-02', превратится в число 19890502   
    d1 = int("".join(d1.split("-")))
    d2 = int("".join(d2.split("-")))
    # Возвращаем модуль разности
    return abs(d1-d2)    

def find(u_id, session):
    """
    Производит поиск пользователя в таблице user по заданному идентификатору, а затем находит двух атлетов в таблице athelete - ближайшего по дате рождения и ближайшего по росту
    """
    # нахдим пользователя в таблице user, у которого поле user.id совпадает с парарметром u_id
    user = session.query(User).filter(User.id == u_id).first()
    # если пользователь с таким id есть в базе данных
    if user:
        # получаем из базы данных дату его рождения и его рост
        u_birthdate = user.birthdate      # Дата рождения пользователя
        u_height = user.height            # Рост пользователя
        # выводим в консоль информацию о найденном пользователе
        print(f"\nНайден пользователь с номером: {u_id}\nИмя: {user.first_name}\nФамилия: {user.last_name}\nПол: {user.gender}\ne-mail: {user.email}\nДата рождения: {u_birthdate}\nРост: {u_height}\n")

        atheletes = session.query(Athelete).all()
        # создаём словари для дат рождения и роста атлетов
        birthdate_dict = {athelete.id: athelete.birthdate for athelete in atheletes} # словарь с id атлетов в качестве ключей. В качестве значений - даты рождения атлетов
        height_dict = {athelete.id: athelete.height for athelete in atheletes} # словарь с id атлетов в качестве ключей. В качестве значений - рост атлетов       

        diff_birthdate = 1000000000 # Устанавливаем заведомо сильно завышенную начальную разность дат рождения
        # Проходимся по парам ключ:значение словаря с датами рождения атлетов
        for a_id, a_bd  in birthdate_dict.items():
            # Вычисляем настоящую разность дат рождения  между пользователем и очередным атлетом при помощи функции date_diff(u_birthdate, a_bd). Она определена выше ↑↑↑
            min_diff_birthdate = date_diff(u_birthdate, a_bd)
            # Если разность, вычисленная на текущем шаге, меньше diff_birthdate
            if min_diff_birthdate < diff_birthdate:
                # Присваиваем diff_birthdate новое (меньшее) значение
                diff_birthdate = min_diff_birthdate
                # Извлекаем в переменную id атлета с ближайшей датой рождения
                a_min_diff_bd_id = a_id

        diff_height = 10000 # Устанавливаем заведомо сильно завышенную начальную разность в росте
        # В случае, если в таблице athelete отсутствует поле "height" или оно не заполнено (рост атлета не указан), назначаем принудительно id = -1
        a_min_diff_hgh_id = -1            
        # Проходимся по парам ключ:значение словаря с ростом атлетов
        for a_id, a_hgh in height_dict.items():
            # Если у атлета в базе данных указан его рост
            if a_hgh is not None:
                # Вычисляем настоящую разность в росте между пользователем и очередным атлетом
                min_diff_height = abs(u_height - a_hgh)
                # Если разность, вычисленная на текущем шаге, меньше diff_height
                if min_diff_height < diff_height:
                    # Присваиваем diff_height новое (меньшее) значение
                    diff_height = min_diff_height
                    # Извлекаем в переменную id атлета с наименьшей разницей в росте
                    a_min_diff_hgh_id = a_id
        # возвращаем id атлетов, ближайших по дате рождения и по росту к пользователю
        return a_min_diff_bd_id, a_min_diff_hgh_id
    # если же пользователь с id = u_id отсутствует в базе данных
    else:
        # выводим сообщение об этом
        print("Пользователи с таким идентификатором не найдены.") 
        # и возвращаем отрицательные значения для id       
        return -1, -1


def print_athelete_list(a_find_bd, a_find_h, s1, s2, session):
    """
    Выводит на экран количество найденных атлетов и их данные.
    Для идентификаторов, равных -1, выводит сообщение о том, что атлетов не найдено.
    """
    # Создаём списки из аргументов функции
    id_list = [a_find_bd, a_find_h] # Список id найденных атлетов
    s = [s1, s2]                    # Список строк для вывода информмации о найденных атлетах
    print("Данные найденных атлетов:\n")
    # проходимся по каждому идентификатору
    for i in range(0, len(id_list)):
        # Если атлет найден (функция find вернула его id, и он не равен -1)
        if id_list[i] != -1:
            # находим атлета в таблице athelete, у которого идентификатор совпадает с одним из значений, содержащихся в списке id_list
            athelete = session.query(Athelete).filter(Athelete.id == id_list[i]).first()
            # выводим в консоль информацию о найденном атлете            
            print(f"{s[i]}\nНомер в списке: {athelete.id}\nВозраст: {athelete.age}\nДата рождения: {athelete.birthdate}\nПол: {athelete.gender}\nРост: {athelete.height}\nИмя: {athelete.name}\nВес: {athelete.weight}\nЗолотых медалей: {athelete.gold_medals}\nСеребряных медалей: {athelete.silver_medals}\nБронзовых медалей: {athelete.bronze_medals}\nВсего медалей: {athelete.total_medals}\nВид спорта: {athelete.sport}\nСтрана: {athelete.country}\n")
        else:
            print(f"{s[i]}\nне обнаружен:(")

def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    """
    session = connect_db()
    find_id = int(input("Введите идентификатор пользователя для поиска: "))
    # вызываем функцию печати на экран результатов поиска. Первым аргуменом в неё передаём вызов функции find(find_id, session), которая возвращает id атлетов, удовлетворяющих условию задачи (ближайшего по дате рождения и ближайшего по росту)
    a_bd, a_h = find(find_id, session)
    print_athelete_list(a_bd, a_h, "Атлет, ближайший по дате рождения:\n", "Атлет, ближайший по росту:\n", session)  

if __name__ == "__main__":
    main()

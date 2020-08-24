# испортируем модули стандартнй библиотеки uuid и datetime
import uuid
import datetime

# импортируем библиотеку sqlalchemy и некоторые функции из неё 
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# константа, указывающая способ соединения с базой данных
DB_PATH = "sqlite:///sochi_athletes.sqlite3"
# базовый класс моделей таблиц
Base = declarative_base()

# Структура таблиц в базе sochi_athletes.sqlite3
# CREATE TABLE athelete("id" integer primary key autoincrement, "age" integer,"birthdate" text,"gender" text,"height" real,"name" text,"weight" integer,"gold_medals" integer,"silver_medals" integer,"bronze_medals" integer,"total_medals" integer,"sport" text,"country" text);
# CREATE TABLE sqlite_sequence(name,seq);
# CREATE TABLE user("id" integer primary key autoincrement, "first_name" text, "last_name" text, "gender" text, "email" text, "birthdate" text, "height" real);

class User(Base):
    """
    Описывает структуру таблицы user для хранения регистрационных данных пользователей
    """
    # задаём название таблицы
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

def connect_db():
    """
    Устанавливает соединение с базой данных, создаёт таблицы, если их еще нет, возвращает объект сессии 
    """
    # создаём соединение к базе данных
    engine = sa.create_engine(DB_PATH)
    # создаём описанные таблицы
    Base.metadata.create_all(engine)
    # создаём фабрику сессий
    session = sessionmaker(engine)
    # возвращаем сессию
    return session()

def request_data():
    """
    Запрашивает у пользователя данные и добавляет их в таблицу user
    """
    # выводим приветствие
    print("Введите, пожалуйста, информацию о себе:")
    # запрашиваем у пользователя данные
    first_name = input("Введите Ваше имя: ")
    last_name = input("Введите Вашу фамилию: ")
    gender = input("Введите Ваш пол (м или ж): ")
    email = input("Введите адрес Вашей электронной почты: ")
    year_birthdate = input("Введите год Вашего рождения, например: 1989: ")    
    month_birthdate = input("Введите месяц Вашего рождения (не более двух цифр), например: 05 ") 
    if len(month_birthdate) < 1:
        print("Вы ввели некорректную информацию:", month_birthdate)
        month_birthdate = input("Введите месяц Вашего рождения (не более двух цифр), например: 05 ")
    elif len(month_birthdate) == 1:
        month_birthdate = "0" + month_birthdate
    elif len(month_birthdate) > 2:
        month_birthdate = month_birthdate[0:2]        
    day_birthdate = input("Введите день Вашего рождения (не более двух цифр), например: 02: ") 
    if len(day_birthdate) < 1:
        print("Вы ввели некорректную информацию:", day_birthdate)
        day_birthdate = input("Введите день Вашего рождения (не более двух цифр), например: 02: ")
    elif len(day_birthdate) == 1:
        day_birthdate = "0" + day_birthdate 
    elif len(day_birthdate) > 2:
        day_birthdate = day_birthdate[0:2]                                
    birthdate = f"{year_birthdate}-{month_birthdate}-{day_birthdate}"      
    height = float(input("Введите Ваш рост в метрах (разделитель - точка), например: 1.78 "))           
    # создаём нового пользователя
    user = User(
        first_name = first_name,
        last_name = last_name,
        gender = gender,
        email = email,
        birthdate = birthdate,   
        height = height        
    )
    # возвращаем созданного пользователя
    return user

def find(name, session):
    """
    Производит поиск пользователя в таблице user по заданному имени name
    """
    # нахдим все записи в таблице user, у которых поле user.first_name совпадает с парарметром name
    query = session.query(User).filter(User.first_name == name)
    # подсчитываем количество таких записей в таблице с помощью метода .count()
    users_count = query.count()
    # составляем списки с данными всех найденных пользователей
    u_id = [user.id for user in query.all()]
    u_first_name = [user.first_name for user in query.all()]
    u_last_name = [user.last_name for user in query.all()]
    u_gender = [user.gender for user in query.all()]
    u_email = [user.email for user in query.all()]
    u_birthdate = [user.birthdate for user in query.all()]
    u_height = [user.height for user in query.all()]
    # возвращаем кортеж, содержащий списки с данными всех найденных пользователей
    return (users_count, u_id, u_first_name, u_last_name, u_gender, u_email, u_birthdate, u_height)

def print_users_list(users_count, u_id, u_first_name, u_last_name, u_gender, u_email, u_birthdate, u_height):
    """
    Выводит на экран количество найденных пользователей, их идентификатор и время последней активности.
    Если передан пустой список идентификаторов, выводит сообщение о том, что пользователей не найдено.
    """
    # проверяем на пустоту список идентификаторов
    if u_id:
        # если список не пуст, распечатываем количество найденных пользователей
        print("Найдено пользователей: ", users_count)
        # распечатываем данные найденных пользователей
        print("Данные найденных пользователей:\n")
        # проходимся по каждому идентификатору
        for i in range(0, len(u_id)):
            print(f"Номер в списке: {u_id[i]}\nИмя: {u_first_name[i]}\nФамилия: {u_last_name[i]}\nПол: {u_gender[i]}\ne-mail: {u_email[i]}\nДата рождения: {u_birthdate[i]}\nРост: {u_height[i]}\n")
    else:
        # если список оказался пустым, выводим сообщение об этом
        print("Пользователей с таким именем нет.")


def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    """
    session = connect_db()
    # просим пользователя выбрать режим
    mode = input("Выберите режим работы с базой данных:\n1 - найти пользователя по имени\n2 - ввести данные нового пользователя\n")
    # проверяем режим
    if mode == "1":
        # выбран режим поиска, запускаем его
        name = input("Введите имя пользователя для поиска: ")
        # вызываем функцию поиска по имени
        users_count, u_id, u_first_name, u_last_name, u_gender, u_email, u_birthdate, u_height = find(name, session)
        # вызываем функцию печати на экран результатов поиска
        print_users_list(users_count, u_id, u_first_name, u_last_name, u_gender, u_email, u_birthdate, u_height)
    elif mode == "2":
        # запрашиваем данные пользоватлея
        user = request_data()
        # добавляем нового пользователя в сессию
        session.add(user)
        # сохраняем все изменения, накопленные в сессии
        session.commit()
        print("Спасибо, данные сохранены!")
    else:
        # при выборе режима, отличного от "1" или "2"
        print("Некорректный режим:(")

if __name__ == "__main__":
    main()

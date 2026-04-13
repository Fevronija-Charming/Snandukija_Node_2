from pydantic import BaseModel, Field, ValidationError
from sqlalchemy import  DateTime, String, Float, Column, Integer, func, Text,BIGINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
class Base(DeclarativeBase):
    pass
#class Ученики(Base):
#__tablename__="Ученики"
#id: Mapped[int]=mapped_column(primary_key=True, autoincrement=True, nullable=False)
#Фамилия: Mapped[str]=mapped_column(String(128), nullable=False)
#Имя: Mapped[str]=mapped_column(String(128), nullable=False)
#class Предметы(Base):
#__tablename__="Предметы"
#id: Mapped[int]=mapped_column(primary_key=True, autoincrement=True, nullable=False)
#Название_Предмета: Mapped[str]=mapped_column(String(32), nullable=False)
#class Даты(Base):
# __tablename__="Даты"
#id: Mapped[int]=mapped_column(primary_key=True, autoincrement=True, nullable=False)
#Дата: Mapped[str]=mapped_column(String(128), nullable=False)
#class Ступени_Обучения(Base):
# __tablename__ = "Ступени_Обучения"
#id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
#Ступень_Обучения: Mapped[str] = mapped_column(String(128), nullable=False)
class Проект(Base):
    __tablename__ = "Проект"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    Название_проекта: Mapped[str] = mapped_column(String(128), nullable=False)
    Критерий_завершенности: Mapped[str] = mapped_column(String(128), nullable=False)
    Завершённость_проекта: Mapped[int]  = mapped_column(nullable=False)
    Этап_1: Mapped[str] = mapped_column(String(128), nullable=False)
    Завершенность_Этап_1: Mapped[int]  = mapped_column(nullable=False)
    Этап_2: Mapped[str] = mapped_column(String(128), nullable=False)
    Завершенность_Этап_2: Mapped[int]  = mapped_column(nullable=False)
    Этап_3: Mapped[str] = mapped_column(String(128), nullable=False)
    Завершенность_Этап_3: Mapped[int]  = mapped_column(nullable=False)
    Этап_4: Mapped[str] = mapped_column(String(128), nullable=False)
    Завершенность_Этап_4: Mapped[int]  = mapped_column(nullable=False)
    Этап_5: Mapped[str] = mapped_column(String(128), nullable=False)
    Завершенность_Этап_5: Mapped[int]  = mapped_column(nullable=False)
    Этап_6: Mapped[str] = mapped_column(String(128), nullable=False)
    Завершенность_Этап_6: Mapped[int]  = mapped_column(nullable=False)
    Этап_7: Mapped[str] = mapped_column(String(128), nullable=False)
    Завершенность_Этап_7: Mapped[int]  = mapped_column(nullable=False)
    Этап_8: Mapped[str] = mapped_column(String(128), nullable=False)
    Завершенность_Этап_8: Mapped[int]  = mapped_column(nullable=False)
    Этап_9: Mapped[str] = mapped_column(String(128), nullable=False)
    Завершенность_Этап_9: Mapped[int]  = mapped_column(nullable=False)
    Этап_10: Mapped[str] = mapped_column(String(128), nullable=False)
    Завершенность_Этап_10: Mapped[int]  = mapped_column(nullable=False)
    Дата_регистрации: Mapped[str] = mapped_column(String(128), nullable=False)
    Дата_изменения: Mapped[str] = mapped_column(String(128), nullable=False)
    Синхронизация: Mapped[int] = mapped_column(nullable=False)
class Project_Schema_UI(BaseModel):
    id: int
    Название_проекта: str = Field(min_length=10, max_length=128)
    Критерий_завершенности: str =  Field(min_length=10, max_length=128)
    Завершённость_проекта: int
    Этап_1: str = Field(min_length=5, max_length=128)
    Завершенность_Этап_1: int
    Этап_2: str = Field(min_length=5, max_length=128)
    Завершенность_Этап_2: int
    Этап_3: str = Field(min_length=5, max_length=128)
    Завершенность_Этап_3: int
    Этап_4: str = Field(min_length=5, max_length=128)
    Завершенность_Этап_4: int
    Этап_5: str = Field(min_length=5, max_length=128)
    Завершенность_Этап_5: int
    Этап_6: str = Field(min_length=5, max_length=128)
    Завершенность_Этап_6: int
    Этап_7: str = Field(min_length=5, max_length=128)
    Завершенность_Этап_7: int
    Этап_8: str = Field(min_length=5, max_length=128)
    Завершенность_Этап_8: int
    Этап_9: str = Field(min_length=5, max_length=128)
    Завершенность_Этап_9: int
    Этап_10: str = Field(min_length=5, max_length=128)
    Завершенность_Этап_10: int
    Дата_регистрации: str = Field(min_length=10, max_length=128)
    Дата_изменения: str = Field(min_length=10, max_length=128)
    Синхронизация: int
class Уроки(Base):
    __tablename__ = "Уроки"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    Имя_Преподавателя: Mapped[str] = mapped_column(String(128), nullable=False)
    Фамилия_Преподавателя: Mapped[str] = mapped_column(String(128), nullable=False)
    Предмет_Обучения: Mapped[str] = mapped_column(String(128), nullable=False)
    Имя_Ученика: Mapped[str] = mapped_column(String(128), nullable=False)
    Фамилия_Ученика: Mapped[str] = mapped_column(String(128), nullable=False)
    Ступень_Обучения: Mapped[str] = mapped_column(String(128), nullable=False)
    Дата_Проведения: Mapped[str] = mapped_column(String(128), nullable=False)
    Время_Начала: Mapped[str] = mapped_column(String(128), nullable=False)
    Длительность_Занятия_Мин: Mapped[int]
    Стоимость_Занятия_Центов: Mapped[int]
    Что_Делали_На_Уроке: Mapped[str] = mapped_column(Text, nullable=False)
    Задание_На_Дом: Mapped[str] = mapped_column(String(128), nullable=False)
    Примечание: Mapped[str] = mapped_column(Text, nullable=False)
class Уроки_Архив(Base):
    __tablename__ = "Уроки_Архив"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    Имя_Преподавателя: Mapped[str] = mapped_column(String(128), nullable=False)
    Фамилия_Преподавателя: Mapped[str] = mapped_column(String(128), nullable=False)
    Предмет_Обучения: Mapped[str] = mapped_column(String(128), nullable=False)
    Имя_Ученика: Mapped[str] = mapped_column(String(128), nullable=False)
    Фамилия_Ученика: Mapped[str] = mapped_column(String(128), nullable=False)
    Ступень_Обучения: Mapped[str] = mapped_column(String(128), nullable=False)
    Дата_Проведения: Mapped[str] = mapped_column(String(128), nullable=False)
    Время_Начала: Mapped[str] = mapped_column(String(128), nullable=False)
    Длительность_Занятия_Мин: Mapped[int]
    Стоимость_Занятия_Центов: Mapped[int]
    Что_Делали_На_Уроке: Mapped[str] = mapped_column(Text, nullable=False)
    Задание_На_Дом: Mapped[str] = mapped_column(String(128), nullable=False)
    Примечание: Mapped[str] = mapped_column(Text, nullable=False)
class Project_Schema(BaseModel):
    id: int
    Название_проекта: str = Field(min_length=10, max_length=128)
    Критерий_завершенности: str =  Field(min_length=10, max_length=128)
    Этап_1: str = Field(min_length=10, max_length=128)
    Этап_2: str = Field(min_length=10, max_length=128)
    Этап_3: str = Field(min_length=10, max_length=128)
    Этап_4: str = Field(min_length=10, max_length=128)
    Этап_5: str = Field(min_length=10, max_length=128)
    Этап_6: str = Field(min_length=10, max_length=128)
    Этап_7: str = Field(min_length=10, max_length=128)
    Этап_8: str = Field(min_length=10, max_length=128)
    Этап_9: str = Field(min_length=10, max_length=128)
    Этап_10: str = Field(min_length=10, max_length=128)
class Urok_Schema(BaseModel):
    Имя_Преподавателя: str = Field(min_length=5, max_length=25)
    Фамилия_Преподавателя: str = Field(min_length=5, max_length=25)
    Предмет_Обучения: str = Field(min_length=5, max_length=25)
    Имя_Ученика: str= Field(min_length=5, max_length=25)
    Фамилия_Ученика: str= Field(min_length=5, max_length=25)
    Ступень_Обучения: str= Field(min_length=5, max_length=25)
    Дата_Проведения: str= Field(min_length=5, max_length=25)
    Время_Начала: str= Field(min_length=5, max_length=25)
    Длительность_Занятия_Мин: int
    Стоимость_Занятия_Центов: int
    Что_Делали_На_Уроке: str= Field(min_length=5, max_length=2500)
    Задание_На_Дом: str= Field(min_length=5, max_length=128)
    Примечание: str= Field(min_length=5, max_length=2000)
class Urok_Schema_UI(BaseModel):
    id: int
    Имя_Преподавателя: str = Field(min_length=5, max_length=25)
    Фамилия_Преподавателя: str = Field(min_length=5, max_length=25)
    Предмет_Обучения: str = Field(min_length=5, max_length=25)
    Имя_Ученика: str= Field(min_length=5, max_length=25)
    Фамилия_Ученика: str= Field(min_length=5, max_length=25)
    Ступень_Обучения: str= Field(min_length=5, max_length=25)
    Дата_Проведения: str= Field(min_length=5, max_length=25)
    Время_Начала: str= Field(min_length=5, max_length=25)
    Длительность_Занятия_Мин: int
    Стоимость_Занятия_Центов: int
    Что_Делали_На_Уроке: str= Field(min_length=5, max_length=2500)
    Задание_На_Дом: str= Field(min_length=5, max_length=128)
    Примечание: str= Field(min_length=5, max_length=2000)
class Uchenik_Poisk(BaseModel):
    Имя_Ученика: str = Field(min_length=5, max_length=25)
class Formir_Oceniv(BaseModel):
    id: int
    Имя_Ученика: str = Field(min_length=5, max_length=25)
    Фамилия_Ученика: str = Field(min_length=5, max_length=25)
    Дата_Проведения: str = Field(min_length=5, max_length=25)
    Что_Делали_На_Уроке: str = Field(min_length=5, max_length=2000)

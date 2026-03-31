from openpyxl import Workbook
#frontend часть
from fastui.forms import fastui_form
from fastapi.responses import HTMLResponse
from fastui import FastUI, AnyComponent, prebuilt_html, components as components
from fastui.components.display import DisplayMode,DisplayLookup
from fastui.events import GoToEvent, BackEvent
import fastui.forms as forms
import python_multipart
from pydoc import plain
from fastapi import Form, UploadFile
import psycopg2 as ps
import asyncio
import os
import datetime, time
from colorama import *
from dotenv import find_dotenv, load_dotenv
from fastui.forms import FastUIForm
load_dotenv(find_dotenv())
#заяц включён
from faststream.rabbit.fastapi import RabbitBroker, RabbitRouter
router=RabbitRouter(url=os.getenv("CLOUDAMQP_URL"))
from fastapi import FastAPI
from fastapi import HTTPException
app = FastAPI()
gamajun=FastAPI()
app.mount("/gamajun",gamajun)
import uvicorn
from typing import Annotated
from fastapi import Depends
from fastapi.responses import FileResponse
#работа с базой данных
from sqlalchemy import  DateTime, String, Float, Column, Integer, func, Text,BIGINT
from sqlalchemy import select, delete, insert, update
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
engine = create_async_engine(os.getenv("DBURL"),echo=True,max_overflow=5,pool_size=5)
session_factory = async_sessionmaker(bind=engine,class_=AsyncSession,expire_on_commit=False,autoflush=True)
from datamodels import Уроки, Уроки_Архив, Base, Проект
from datamodels import Project_Schema, Urok_Schema
#конфигурация сервиса по отправке почты
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr,BaseModel
from typing import List
configuracija_pochty=ConnectionConfig(MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
                                      MAIL_FROM=os.getenv("MAIL_FROM"),
                                      MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
                                      MAIL_FROM_NAME=os.getenv("MAIL_FROM_NAME"),
MAIL_PORT=os.getenv("MAIL_PORT"),MAIL_SERVER=os.getenv("MAIL_SERVER"),MAIL_STARTTLS=os.getenv("MAIL_STARTTLS"),
MAIL_SSL_TLS=os.getenv("MAIL_SSL_TLS"),USE_CREDENTIALS=os.getenv("USE_CREDENTIALS"))
#фоновая задача для отправки почты
from fastapi import BackgroundTasks
async def send_email_async(subject: str, recipients:str, body:str):
    recipient_list = []
    recipient_list.append(recipients)
    message=MessageSchema(subject=subject,recipients=recipient_list,body=body,subtype=MessageType.plain)
    fast_mail = FastMail(configuracija_pochty)
    await fast_mail.send_message(message)
async def send_email_async_file(subject: str, recipients:str, body:str,file_path:str):
    recipient_list = []
    recipient_list.append(recipients)
    message=MessageSchema(subject=subject,recipients=recipient_list,body=body,subtype=MessageType.plain,attachments=[file_path])
    fast_mail = FastMail(configuracija_pochty)
    await fast_mail.send_message(message)
    #os.remove(file_path)
#@gamajun.post("/gamajun/add/", response_model=FastUI,response_model_exclude_none=True)
#def insert_DB_urok_s_GrIntr(form:Annotated[Urok_Schema,FastUIForm[Urok_Schema]]):
#return Form()
#@app.post("/add/")
#async def insert_DB_urok_s_GrIntr(urok: Annotated[Urok_Schema, Depends()]):
#print(urok)
#return urok
#фронт на fastUI ВИДЖЕТЫ СТРАНИЦЫ ФРОНТА
from templates import field_labels_project
@app.post("/add/project")
async def insert_DB_project_s_GrIntr(background_task: BackgroundTasks, id: int= Form(), Название_проекта: str = Form(),
    Критерий_завершенности: str =  Form(), Этап_1: str = Form(), Этап_2: str = Form(), Этап_3: str = Form(),
    Этап_4: str = Form(), Этап_5: str = Form(), Этап_6: str = Form(), Этап_7: str = Form(), Этап_8: str = Form(),
    Этап_9: str = Form(), Этап_10: str = Form()):
    svedenija_project = [Название_проекта,Критерий_завершенности,Этап_1,Этап_2,Этап_3,Этап_4,Этап_5,Этап_6,Этап_7,
    Этап_8,Этап_9,Этап_10]
    peremycka1 = " -> "
    peremycka2 = "; "
    soobshenije=""
    for i in range(len(svedenija_project)):
        soobshenije=soobshenije + field_labels_project[i] + peremycka1 + svedenija_project[i] + peremycka2
    print(soobshenije)
    try:
        tochnoje_vremja = str(datetime.datetime.now())
        vremja_format = tochnoje_vremja[:-10]
        sekundi = int(time.time())
        Project_s_GrIntr = Проект(#id=id,
        Название_проекта=Название_проекта,Критерий_завершенности=Критерий_завершенности,
        Завершённость_проекта=0, Этап_1 = Этап_1, Завершенность_Этап_1=0, Этап_2 = Этап_2, Завершенность_Этап_2=0,
        Этап_3 = Этап_3, Завершенность_Этап_3=0, Этап_4 = Этап_4, Завершенность_Этап_4=0, Этап_5 = Этап_5,
        Завершенность_Этап_5=0, Этап_6 = Этап_6, Завершенность_Этап_6=0, Этап_7 = Этап_7, Завершенность_Этап_7=0,
        Этап_8 = Этап_8, Завершенность_Этап_8=0, Этап_9 = Этап_9, Завершенность_Этап_9=0, Этап_10 = Этап_10,
        Завершенность_Этап_10=0, Дата_регистрации=vremja_format, Дата_изменения=vremja_format,Синхронизация=sekundi)
        session = session_factory()
        session.add(Project_s_GrIntr)
        await session.commit()
        await session.close()
        try:
            # заяц включен
            await router.broker.publish(message="Добавлен новый проект", queue="UROKI")
            await router.broker.publish(message=f"{soobshenije}", queue="UROKI")
            try:
                recipient = os.getenv("RECIPIENT1")
                background_task.add_task(send_email_async, "Добавлен новый проект", recipient, soobshenije)
                return soobshenije
            except:
                raise HTTPException(status_code=500, detail="Проблема с почтой")
        except:
            raise HTTPException(status_code=500, detail="Проблема с брокером")
    except:
        raise HTTPException(status_code=500, detail="Проблема с базой данных")
@app.post("/add/")
async def insert_DB_urok_s_GrIntr(background_task: BackgroundTasks,Имя_Преподавателя: str = Form(),Фамилия_Преподавателя: str = Form(),
    Предмет_Обучения: str = Form(),Имя_Ученика: str= Form(),Фамилия_Ученика: str= Form(),Ступень_Обучения: str= Form(),
    Дата_Проведения: str= Form(),Время_Начала: str= Form(),Длительность_Занятия_Мин: int= Form(),
    Стоимость_Занятия_Центов: int= Form(), Что_Делали_На_Уроке: str= Form(),
    Задание_На_Дом: str= Form(), Примечание: str= Form()):
    peremycka1 = " -> "
    peremycka2 = "; "
    soobshenije1 = "Имя_Преподавателя"
    soobshenije2 = soobshenije1 + peremycka1 + Имя_Преподавателя + peremycka2
    soobshenije3 = "Фамилия_Преподавателя"
    soobshenije4 = soobshenije2 + soobshenije3 +  peremycka1 + Фамилия_Преподавателя + peremycka2
    soobshenije5="Предмет_Обучения"
    soobshenije6 = soobshenije4 + soobshenije5 + peremycka1 + Предмет_Обучения + peremycka2
    soobshenije7 = "Имя_Ученика"
    soobshenije8=soobshenije6 + soobshenije7 + peremycka1 + Имя_Ученика + peremycka2
    soobshenije9="Фамилия_Ученика"
    soobshenije10 = soobshenije8 + soobshenije9 + peremycka1 + Фамилия_Ученика + peremycka2
    soobshenije11= "Ступень_Обучения"
    soobshenije12 = soobshenije10 + soobshenije11 + peremycka1 + Ступень_Обучения + peremycka2
    soobshenije13 = "Дата_Проведения"
    soobshenije14 = soobshenije12 + soobshenije13 + peremycka1 + Дата_Проведения + peremycka2
    soobshenije15= "Время_Начала"
    soobshenije16= soobshenije14 + soobshenije15 + peremycka1 + Время_Начала + peremycka2
    soobshenije17 = "Длительность_Занятия_Мин"
    soobshenije18 = soobshenije16 + soobshenije17 + peremycka1 + str(Длительность_Занятия_Мин) + peremycka2
    soobshenije19 = "Стоимость_Занятия_Центов"
    soobshenije20 = soobshenije18 + soobshenije19 + peremycka1 + str(Стоимость_Занятия_Центов) + peremycka2
    soobshenije21="Что_Делали_На_Уроке"
    soobshenije22 = soobshenije20 + soobshenije21 + peremycka1 + Что_Делали_На_Уроке + peremycka2
    soobshenije23="Задание_На_Дом"
    soobshenije24= soobshenije22 + soobshenije23 + peremycka1 + Задание_На_Дом + peremycka2
    soobshenije25="Примечание"
    soobshenije26 = soobshenije24 + soobshenije25 + peremycka1 + Примечание
    try:
        Urok_s_GrIntr = Уроки(Имя_Преподавателя=Имя_Преподавателя,Фамилия_Преподавателя=Фамилия_Преподавателя,
        Предмет_Обучения = Предмет_Обучения, Имя_Ученика = Имя_Ученика,Фамилия_Ученика = Фамилия_Ученика,
        Ступень_Обучения = Ступень_Обучения,Дата_Проведения = Дата_Проведения, Время_Начала = Время_Начала,
        Длительность_Занятия_Мин = Длительность_Занятия_Мин, Стоимость_Занятия_Центов = Стоимость_Занятия_Центов,
        Что_Делали_На_Уроке = Что_Делали_На_Уроке, Задание_На_Дом = Задание_На_Дом, Примечание = Примечание)
        session = session_factory()
        session.add(Urok_s_GrIntr)
        await session.commit()
        await session.close()
        try:
            # заяц включен
            await router.broker.publish(message="Добавлен новый урок", queue="UROKI")
            await router.broker.publish(message=f"{soobshenije26}", queue="UROKI")
            try:
                recipient = os.getenv("RECIPIENT1")
                background_task.add_task(send_email_async, "Добавлен новый урок", recipient,soobshenije26)
                return soobshenije26
            except:
                raise HTTPException(status_code=500, detail="Проблема с почтой")
        except:
            raise HTTPException(status_code=500, detail="Проблема с брокером")
    except:
        raise HTTPException(status_code=500, detail="Проблема с базой данных")
@gamajun.get("/api/", response_model=FastUI,response_model_exclude_none=True)
def create_urok_graph_inter():
    return components.Page(components=
                            [components.Heading(text="Добавить урок",level=2),
                             components.ModelForm(model=Urok_Schema,submit_url="/add/")])
@gamajun.get("/api/project", response_model=FastUI,response_model_exclude_none=True)
def create_urok_graph_inter():
    return components.Page(components=
                            [components.Heading(text="Добавить проект",level=2),
                             components.ModelForm(model=Project_Schema,submit_url="/add/project")])
#переключение на зайца
#@app.post("/urok", summary="Зарегестрировать урок",tags=["УРОКИ"])
@router.post("/project", summary="Зарегестрировать проект", tags=["ПРОЕКТ"])
async def create_project(background_task: BackgroundTasks,project_infa: Annotated[Project_Schema, Depends()]):
    try:
        tochnoje_vremja= str(datetime.datetime.now())
        vremja_format = tochnoje_vremja[:-10]
        sekundi= int(time.time())
        project_eksemprljar=Проект(id=project_infa.id,Название_проекта=project_infa.Название_проекта,
Критерий_завершенности=project_infa.Критерий_завершенности, Завершённость_проекта=0,Этап_1=project_infa.Этап_1,
Завершенность_Этап_1=0, Этап_2=project_infa.Этап_2,Завершенность_Этап_2=0, Этап_3=project_infa.Этап_3,Завершенность_Этап_3=0,
Этап_4=project_infa.Этап_4, Завершенность_Этап_4=0, Этап_5=project_infa.Этап_5, Завершенность_Этап_5=0, Этап_6=project_infa.Этап_6,
Завершенность_Этап_6=0, Этап_7=project_infa.Этап_7, Завершенность_Этап_7=0, Этап_8=project_infa.Этап_8, Завершенность_Этап_8=0,
Этап_9=project_infa.Этап_9, Завершенность_Этап_9=0,Этап_10=project_infa.Этап_10, Завершенность_Этап_10=0, Дата_регистрации=vremja_format,
Дата_изменения=vremja_format,Синхронизация=sekundi)
        session=session_factory()
        session.add(project_eksemprljar)
        await session.commit()
    except:
        raise HTTPException(status_code=500, detail="Проблема с базой данных")
    await session.close()
    try:
        # заяц включен
        await router.broker.publish(message="Добавлен новый проект", queue="UROKI")
        await router.broker.publish(message=f"{project_infa}", queue="UROKI")
    except:
        raise HTTPException(status_code=500, detail="Проблема с брокером")
    try:
        peremycka = " -> "
        nazv_projekta_pochta = str(project_infa.Название_проекта)
        soobshenije1 = nazv_projekta_pochta
        kritery_zaver_pochta=str(project_infa.Критерий_завершенности)
        soobshenije2 = soobshenije1 + peremycka + kritery_zaver_pochta
        etap_1_pochta = str(project_infa.Этап_1)
        soobshenije3 = soobshenije2 + peremycka + etap_1_pochta
        etap_2_pochta = str(project_infa.Этап_2)
        soobshenije4 = soobshenije3 + peremycka + etap_2_pochta
        etap_3_pochta = str(project_infa.Этап_3)
        soobshenije5 = soobshenije4 + peremycka + etap_3_pochta
        etap_4_pochta = str(project_infa.Этап_4)
        soobshenije6 = soobshenije5 + peremycka + etap_4_pochta
        etap_5_pochta = str(project_infa.Этап_5)
        soobshenije7 = soobshenije6 + peremycka + etap_5_pochta
        etap_6_pochta = str(project_infa.Этап_6)
        soobshenije8 = soobshenije7 + peremycka + etap_6_pochta
        etap_7_pochta = str(project_infa.Этап_7)
        soobshenije9 = soobshenije8 + peremycka + etap_7_pochta
        etap_8_pochta = str(project_infa.Этап_8)
        soobshenije10 = soobshenije9 + peremycka + etap_8_pochta
        etap_9_pochta = str(project_infa.Этап_9)
        soobshenije11 = soobshenije10 + peremycka + etap_9_pochta
        etap_10_pochta = str(project_infa.Этап_10)
        projekt_na_pochtu = soobshenije11 + peremycka + etap_10_pochta
        recipient=os.getenv("RECIPIENT1")
        background_task.add_task(send_email_async,"Добавлен новый проект",recipient,projekt_na_pochtu)
        return project_infa, projekt_na_pochtu
    except:
        raise HTTPException(status_code=500, detail="Проблема с почтой")
@router.post("/urok", summary="Зарегестрировать урок", tags=["УРОКИ"])
async def create_urok(urok: Annotated[Urok_Schema, Depends()]):
    try:
        urok_eksemp = Уроки(Имя_Преподавателя=urok.Имя_Преподавателя,Фамилия_Преподавателя=urok.Фамилия_Преподавателя,
                            Предмет_Обучения=urok.Предмет_Обучения,Имя_Ученика=urok.Имя_Ученика,
                            Фамилия_Ученика=urok.Фамилия_Ученика,Ступень_Обучения=urok.Ступень_Обучения,
                            Дата_Проведения=urok.Дата_Проведения, Время_Начала=urok.Время_Начала,
                            Длительность_Занятия_Мин=urok.Длительность_Занятия_Мин,
                            Стоимость_Занятия_Центов=urok.Стоимость_Занятия_Центов,
                            Что_Делали_На_Уроке=urok.Что_Делали_На_Уроке,Задание_На_Дом=urok.Задание_На_Дом,
                            Примечание=urok.Примечание)
        session = session_factory()
        session.add(urok_eksemp)
        await session.commit()
        await session.close()
        try:
            #заяц включен
            await router.broker.publish(message="Добавлен новый урок", queue="UROKI")
            await router.broker.publish(message=f"{urok}", queue="UROKI")
            return urok_eksemp
        except:
            raise HTTPException(status_code=500, detail="Проблема с брокером")
    except:
        raise HTTPException(status_code=500, detail="Проблема с базой данных")
@app.get("/vedomost", summary="Получить ведомость", tags=["ВЕДОМОСТЬ"])
async def get_vedomost(background_task: BackgroundTasks):
    try:
        connection = ps.connect(host=os.getenv("DBHOST"), database=os.getenv("DBNAME"), user=os.getenv("DBUSERNAME"),
                            password=os.getenv("DBPASSWORD"), port=os.getenv("DBPORT"))
        # создание интерфейса для sql запроса
        cursor = connection.cursor()
        zapros = "SELECT * FROM Уроки ORDER BY Дата_Проведения ASC;"
        cursor.execute(zapros)
        vedomost=[]
        zarplata=0
        chasy=0
        # создание excel fail
        wb=Workbook()
        ws=wb.active
        ws.title="Ведомость"
        while True:
            next_row = cursor.fetchone()
            if next_row:
                chasy=chasy+(next_row[9])/60
                zarplata=zarplata+(next_row[10])/100
                vedomost.append(next_row)
                ws.append(next_row)
            else:
                cursor.close()
                connection.close()
                session = session_factory()
                offset_rjada=0
                for row in vedomost:
                    den_uroka=row[7]
                    cislo_mesjac=den_uroka[4]
                    print(cislo_mesjac)
                    id_uroka=100*int(cislo_mesjac)+offset_rjada
                    urok_eksemp = Уроки_Архив(id=id_uroka,Имя_Преподавателя=row[1],Фамилия_Преподавателя=row[2],
                    Предмет_Обучения=row[3], Имя_Ученика=row[4],Фамилия_Ученика=row[5], Ступень_Обучения=row[6],
                    Дата_Проведения=row[7], Время_Начала=row[8],Длительность_Занятия_Мин=row[9],
                    Стоимость_Занятия_Центов=row[10],Что_Делали_На_Уроке=row[11], Задание_На_Дом=row[12],
                    Примечание=row[13])
                    session.add(urok_eksemp)
                    offset_rjada+=1
                smdt=delete(Уроки)
                await session.execute(smdt)
                await session.commit()
                await session.close()
                try:
                    ws.append(["/","/","/","/","/","/","/","/","/",chasy,zarplata])
                    ws.append(["SH õpilaste mitteilmuse pretsentsioonid 87,50"])
                    ws.append(["Mittemakstud osa verbuarist 38,25"])
                    ws.append(["Mittemasktud osa januarist 39,00"])
                    ws.append(["Mittemasktud osa nomembrist 12,50"])
                    wb.save("Посчитать зарплату.xlsx")
                    try:
                            soobshenije="See on aruanne märtsi tundide kohta"
                            recipient = os.getenv("RECIPIENT2")
                            File_path="Посчитать зарплату.xlsx"
                            background_task.add_task(send_email_async_file, "Tunnid märtsis", recipient, soobshenije, File_path)
                            return FileResponse(path="Посчитать зарплату.xlsx", filename="Посчитать зарплату.xlsx",
                                        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                    except: raise HTTPException(status_code=500, detail="Проблема с почтой")
                except: raise HTTPException(status_code=500, detail="Проблема с файлом")
    except: raise HTTPException(status_code=500, detail="Проблема с базой данных")
@app.get("/zapr", summary="Посчитать зарплату",tags=["ЗАРПЛАТА"])
async def get_zapr():
    summa=0
    query = select(Уроки.Стоимость_Занятия_Центов)
    session = session_factory()
    result = await session.execute(query)
    zapka = result.scalars().all()
    for zapka in zapka:
        summa = summa + zapka
    return summa/100
@app.get("/chasy", summary="Посчитать часы",tags=["ЧАСЫ"])
async def get_chasy():
    chasy=0
    query = select(Уроки.Длительность_Занятия_Мин)
    session = session_factory()
    result = await session.execute(query)
    dlitelnost = result.scalars().all()
    for element in dlitelnost:
        chasy = chasy + element
    return chasy/60
# пока выключил, Хероку сам создаст базу
async def kostily_BD():
    # создать ДБ
    import psycopg2 as ps
    from psycopg2.errors import DuplicateDatabase as Oshibka
    from psycopg2 import sql
    connection = None
    try:
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print(Back.GREEN + Fore.BLACK + Style.BRIGHT + 'Создать базу Данных')
        databasename = os.getenv('DATABASENAME')
        connection = ps.connect(host="localhost", database="postgres", user="postgres", password=os.getenv("DBPASSWORD"),
                                port="5432")
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(databasename)))
        cursor.close()
        print(Back.LIGHTGREEN_EX + Fore.BLACK + Style.BRIGHT + 'БД успешно создана, моя Госпожа')
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    except Oshibka:
        print('Такая БД уже есть, моя Госпожа!!!')
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    finally:
        if connection:
            connection.close()
        if cursor:
            cursor.close()
async def create_tables():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
# пока выключил этот функционал не нужен
# async def create_predmety():
# predmet_eksempjar1=Предметы(Название_Предмета="Математика")
# session=session_factory()
# session.add(predmet_eksempjar1)
# await session.commit()
# await session.close()
# predmet_eksempjar2 = Предметы(Название_Предмета="Физика")
# session = session_factory()
# session.add(predmet_eksempjar2)
# await session.commit()
# await session.close()
# predmet_eksempjar3 = Предметы(Название_Предмета="Биология")
# session = session_factory()
# session.add(predmet_eksempjar3)
# await session.commit()
# await session.close()
# predmet_eksempjar4 = Предметы(Название_Предмета="Химия")
# session = session_factory()
# session.add(predmet_eksempjar4)
# await session.commit()
# await session.close()
# predmet_eksempjar5=Предметы(Название_Предмета="Английский")
# session = session_factory()
# session.add(predmet_eksempjar5)
# await session.commit()
# await session.close()
# async def create_stupeni():
# stupen_eksemprjar1=Ступени_Обучения(Ступень_Обучения="7-8-9 классы")
# session = session_factory()
# session.add(stupen_eksemprjar1)
# await session.commit()
# await session.close()
# stupen_eksemprjar2 = Ступени_Обучения(Ступень_Обучения="5-6-7 классы")
# session = session_factory()
# session.add(stupen_eksemprjar2)
# await session.commit()
# await session.close()
# stupen_eksemprjar3 = Ступени_Обучения(Ступень_Обучения="Гимназия-Техникум")
# session = session_factory()
# session.add(stupen_eksemprjar3)
# await session.commit()
# await session.close()
#stupen_eksemprjar4 = Ступени_Обучения(Ступень_Обучения="Студенты_Абитурьенты")
#session = session_factory()
#session.add(stupen_eksemprjar4)
#await session.commit()
#await session.close()
# stupen_eksemprjar5 = Ступени_Обучения(Ступень_Обучения="1-2-3-4 классы")
# session = session_factory()
# session.add(stupen_eksemprjar5)
# await session.commit()
# await session.close()
@gamajun.get('/{path:path}')
def gamajun_root() -> HTMLResponse:
    return HTMLResponse(prebuilt_html(title='FastUI Demo',api_root_url='/gamajun/api',api_path_strip='/gamajun'))
@gamajun.post('/{path:path}')
def gamajun_root2() -> HTMLResponse:
    return HTMLResponse(prebuilt_html(title='FastUI Demo',api_root_url='/gamajun/api',api_path_strip='/gamajun'))
async def main():
    init(autoreset=True)
    #await kostily_BD()
    await create_tables()
    uvicorn.run("main:app", reload=True)
    #создать предметы
    #await create_predmety()
    #await create_stupeni()
from fastapi.middleware.cors import CORSMiddleware
gamajun.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
# заяц включён
app.include_router(router)
if __name__ == "__main__":
    asyncio.run(main())
#web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --host=0.0.0.0 --port=8000

#!/usr/bin/env python
'''
SQL Introducción [Python]
Ejercicios de práctica
---------------------------
Autor: Inove Coding School
Version: 1.1

Descripcion:
Programa creado para poner a prueba los conocimientos
adquiridos durante la clase
'''

__author__ = "Inove Coding School"
__email__ = "alumnos@inove.com.ar"
__version__ = "1.1"

import sqlite3
import csv
import os


import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Crear el motor (engine) de la base de datos
engine = sqlalchemy.create_engine("sqlite:///secundaria.db")
base = declarative_base()

# Referenciamos el archivo init para localizar el path de archivos csv
from config import config

# Obtener la path de ejecución actual del script
script_path = os.path.dirname(os.path.realpath(__file__))

# Obtener los parámetros del archivo de configuración
config_path_name = os.path.join(script_path, 'config.ini')
datos = config('datos', config_path_name)




class Tutor(base):
    __tablename__ = "tutor"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    def __repr__(self):
        return f"Tutor: {self.name}"


class Estudiante(base):
    __tablename__ = "estudiante"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    grade = Column(Integer)
    tutor_id = Column(Integer, ForeignKey("tutor.id"))

    tutor = relationship("Tutor")

    def __repr__(self):
        return f"Estudiante: {self.name}, edad {self.age}, grado {self.grade}, tutor {self.tutor.name}"


def create_schema():
    # Borrar todos las tablas existentes en la base de datos
    # Esta linea puede comentarse sino se eliminar los datos
    base.metadata.drop_all(engine)

    # Crear las tablas
    base.metadata.create_all(engine)


def insert_tutor(name):

    Session = sessionmaker(bind=engine)
    session = Session()
    #Crear tutor
    tutory= Tutor(name = name)
 #   print(tutory)
    session.add(tutory)
    session.commit()
    


def insert_estudiante(name, age, grade, tutor):
   
    Session = sessionmaker(bind=engine)
    session = Session()

   
    query = session.query(Tutor).filter(Tutor.name == tutor)
    tutory = query.first()

    if tutory is None:
        # Podrá ver en este ejemplo que sucederá este error con la persona
        # de nacionalidad Inglaterra ya que no está definida en el archivo
        # de nacinoalidades
        print(f"Error la crear el estudiante {name}, no existe el tutor {name}")
        return

    # Crear estudiante
    estudiante = Estudiante(name=name, age=age, grade=grade, tutor=tutory)
    # print(estudiante)
   

    session.add(estudiante)
    session.commit()
    


def fill():
    # Llenar la tabla de la secundaria con al munos 2 tutores
    # Cada tutor tiene los campos:
    # id --> este campo es auto incremental por lo que no deberá completarlo
    # name --> El nombre del tutor (puede ser solo nombre sin apellido)

    # Llenar la tabla de la secundaria con al menos 5 estudiantes
    # Cada estudiante tiene los posibles campos:
    # id --> este campo es auto incremental por lo que no deberá completarlo
    # name --> El nombre del estudiante (puede ser solo nombre sin apellido)
    # age --> cuantos años tiene el estudiante
    # grade --> en que año de la secundaria se encuentra (1-6)
    # tutor --> el tutor de ese estudiante (el objeto creado antes)

    # No olvidarse que antes de poder crear un estudiante debe haberse
    # primero creado el tutor.

 
    # Insertar el archivo CSV de los tutores
    with open(datos['tutory']) as fi:
        data = list(csv.DictReader(fi))
        

    # Agregamos cada tutor a la tabla:
        for row in data:
            print(row)
            insert_tutor(row['tutory'])
        
    # Insertar el archivo CSV de los estudiantes
   
    with open(datos['student']) as fi:
        data = list(csv.DictReader(fi))
        print(data)
        #Agregamos cada estudiante a la tabla
        for row in data:
            insert_estudiante(row['name'],int(row['age']), row['grade'],row['tutor_id'])
            print(row)
            
           
    print('Completemos esta tablita!')
    

def fetch():
    print('Comprobemos su contenido, ¿qué hay en la tabla?')
    # Crear una query para imprimir en pantalla
    # todos los objetos creados de la tabla estudiante.
    # Imprimir en pantalla cada objeto que traiga la query
    # Realizar un bucle para imprimir de una fila a la vez
 
    #Incio Sesión
    Session = sessionmaker(bind=engine)
    session = Session()

    # Query de todos los objetos creados en la tabla estudiante

    query = session.query(Tutor)

    # Imprimir cada objeto que traiga la query

    for tutor in query:
        print(tutor)

    query = session.query(Estudiante)

    # Imprimir cada objeto que traiga la query

    for estudiante in query:
        print(estudiante)
        

def search_by_tutor(tutor):
    print('Operación búsqueda!')
    # Esta función recibe como parámetro el nombre de un posible tutor.
    # Crear una query para imprimir en pantalla
    # aquellos estudiantes que tengan asignado dicho tutor.

    # Para poder realizar esta query debe usar join, ya que
    # deberá crear la query para la tabla estudiante pero
    # buscar por la propiedad de tutor.name
    Session= sessionmaker(bind=engine)
    session=Session()
    tutory = tutor
    coincidencia = session.query(Estudiante.name).join(Estudiante.tutor).filter(Tutor.name==tutory)
    print("Los estudiantes que comparten el mismo tutor son : ", coincidencia.all())


def modify(id, name):
    print('Modificando la tabla')
    # Deberá actualizar el tutor de un estudiante, cambiarlo para eso debe
    # 1) buscar con una query el tutor por "tutor.name" usando name
    # pasado como parámetro y obtener el objeto del tutor
    # 2) buscar con una query el estudiante por "estudiante.id" usando
    # el id pasado como parámetro
    # 3) actualizar el objeto de tutor del estudiante con el obtenido
    # en el punto 1 y actualizar la base de datos

    # TIP: En clase se hizo lo mismo para las nacionalidades con
    # en la función update_persona_nationality
    Session = sessionmaker(bind=engine)
    session = Session()

    # Buscar el tutor a actualizar
    query = session.query(Tutor).filter(Tutor.name==name)
    nuevo_tutor = query.first()

    # Buscar el estudiante  a actualizar
    query = session.query(Estudiante).filter(Estudiante.id==id)
    estudiante = query.first()

    # Actualizar el estudiante con el nuevo tutor
    estudiante.tutor = nuevo_tutor

    session.add(estudiante)
    session.commit()

    print("Estudiante actualizado :", estudiante)


def count_grade(grade):
    print('Estudiante por grado')
    # Utilizar la sentencia COUNT para contar cuantos estudiante
    # se encuentran cursando el grado "grade" pasado como parámetro
    # Imprimir en pantalla el resultado

    # TIP: En clase se hizo lo mismo para las nacionalidades con
    # en la función count_persona

    Session = sessionmaker(bind=engine)
    session = Session()

    contar = session.query(Estudiante).filter(Estudiante.grade==grade).count()
    print('La cantidad de estudiantes que cursan el {} grado son {}'.format(grade,contar))


if __name__ == '__main__':
    print("Bienvenidos a otra clase de Inove con Python")
    create_schema()   # create and reset database (DB)
   # insert_estudiante("Carlos",23,1)
    # fill()
    fill()
    # fetch()
    fetch()

    tutor = 'Marcos'
    # search_by_tutor(tutor)
    search_by_tutor(tutor)

    nuevo_tutor = 'nombre_tutor'
    id = 2
    # modify(id, nuevo_tutor)
    modify(2,'Karina')
    grade = 2
    # count_grade(grade)
    count_grade(grade)

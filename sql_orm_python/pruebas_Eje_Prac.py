
# Este Archivo es para pruebas de código

import sqlite3

import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Crear el motor (engine) de la base de datos
engine = sqlalchemy.create_engine("sqlite:///secundaria.db")
base = declarative_base()


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

    Session = sessionmaker(bind=engine)
    session = Session()

    # Agregamos 4 (cuatro) tutores:
    tutores = ['Marcos', 'Ana', 'Oscar','Karina']

    for tutor in tutores:
     tutor = Tutor(name=tutor)
     #tutor = Tutor(tutor.name(tutor))
     session.add(tutor)
   
    # Agregamos 6 (seis) estudiantes:

    estudiantes = {(name = 'Juan', age=13, grade = '1', tutor = 1),
                   (name = 'Maia', age=16, grade = '4', tutor = 3)}
                    
    estudiante = Estudiante (name = 'Maia', age=16, grade = '4', tutor = 3)
    estudiante = Estudiante (name = 'Clara', age=14, grade = '2', tutor = 1)
    estudiante = Estudiante (name = 'José', age=17, grade = '5', tutor = 2)
    estudiante = Estudiante (name = 'Carlos', age=15, grade = '3', tutor = 4)
    estudiante = Estudiante (name = 'Julia', age=18, grade = '6', tutor = 3)

   # session.add(estudiante)
    #session.add(estudiante)
    session.commit()

    print('Completemos esta tablita!')
    


def fetch():
    print('Comprobemos su contenido, ¿qué hay en la tabla?')
    # Crear una query para imprimir en pantalla
    # todos los objetos creados de la tabla estudiante.
    # Imprimir en pantalla cada objeto que traiga la query
    # Realizar un bucle para imprimir de una fila a la vez
 
    #Incio Sesión
    Session = sessionmaker(bind=engine)
    session=Session()

    # Query de todos los objetos creados en la tabla estudiante

    query = session.query(Tutor)

    # Imprimir cada objeto que traiga la query

    for tutor in query:
        print(tutor)
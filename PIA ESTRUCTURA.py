separador = ("*" * 40)
import sys
from os import remove
import sqlite3
from sqlite3 import Error
with sqlite3.connect("CURSO.db") as conn:
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS materias (idmateria INTEGER PRIMARY KEY, nombre TEXT NOT NULL);")
    c.execute("CREATE TABLE IF NOT EXISTS alumnos (idalumno INTEGER PRIMARY KEY, nombre TEXT NOT NULL);")
    c.execute("CREATE TABLE IF NOT EXISTS calificaciones (idalumno INTEGER NOT NULL, idmateria INTEGER NOT NULL, calificacion INTEGER NOT NULL, FOREIGN KEY(idalumno) REFERENCES alumnos(idalumno), FOREIGN KEY(idmateria) REFERENCES materias(idmateria));")
    c.execute("INSERT INTO materias(idmateria, nombre) SELECT 1, 'PROGRAMACION' WHERE NOT EXISTS(SELECT idmateria FROM materias WHERE idmateria = 1)")
    c.execute("INSERT INTO materias(idmateria, nombre) SELECT 2, 'BASE DE DATOS' WHERE NOT EXISTS(SELECT idmateria FROM materias WHERE idmateria = 2)")
    c.execute("INSERT INTO materias(idmateria, nombre) SELECT 3, 'MACROECONOMIA' WHERE NOT EXISTS(SELECT idmateria FROM materias WHERE idmateria = 3)")
    c.execute("INSERT INTO materias(idmateria, nombre) SELECT 4, 'ESTADISTICAS' WHERE NOT EXISTS(SELECT idmateria FROM materias WHERE idmateria = 4)")
    c.execute("INSERT INTO materias(idmateria, nombre) SELECT 5, 'CONTABILIDAD' WHERE NOT EXISTS(SELECT idmateria FROM materias WHERE idmateria = 5)")
    conn.commit()    

def menu():
    print("1) Capturar 30 estudiantes")
    print("2) Capturar las calificaciones de los 30 estudiantes")
    print("3) Consultar calificaciones por alumno determinado")
    print("4) Consultar reporte de calificaciones por estudiantes")
    print("5) Consultar reporte de calificaciones por materias")
    print("6) Asignaturas con menor desempeño")
    print("7) Estudiantes que reprobaron mas de 2 materias")
    print("8) Listado de todos los alumnos inscritos")
    alumnos = conn.cursor()
    alumnos.execute("SELECT * FROM alumnos")
    alumnos1 = alumnos.fetchall()
    materias = conn.cursor()
    materias.execute("SELECT * FROM materias")
    materias = materias.fetchall()
        
    respuesta = int(input("Elige la opcion del menu que desees:"))
    print(separador)
    while (respuesta != 1) and (respuesta != 2) and (respuesta != 3) and (respuesta != 4) and (respuesta != 5) and (respuesta != 6) and (respuesta != 7) and (respuesta != 8):
        respuesta = int(input("Opcion invalida, teclea una opcion del menu"))
    if respuesta == 1:
        Opcion_1()
    elif respuesta == 2:
        Opcion_2()
    elif respuesta == 3:
        Opcion_3()
    elif respuesta == 4:
        Opcion_4()
    elif respuesta == 5:
        Opcion_5()
    elif respuesta == 6:
        Opcion_6()
    elif respuesta == 7:
        Opcion_7()
    else:
        Opcion_8()
        
registros_cant = 0
def Opcion_1():
    global registros_cant
    print("Ingrese los datos de los 30 alumnos(matricula y nombre) teclee 0 en la matricula para regresar al menu") 
    if registros_cant <= 30:
        while registros_cant <= 30:
            idalumno = int(input("Matricula del alumno: "))
            if idalumno == 0:
                registrados = registros_cant
                menu()
            else:
                try:
                    nombre = input("Nombre del alumno: ")
                    insertaralumnos = conn.cursor()
                    valores = {"idalumno":idalumno, "nombre": nombre}
                    insertaralumnos.execute("INSERT INTO alumnos VALUES(:idalumno,:nombre)", valores)
                    registros_cant = registros_cant + 1
                    print("ALUMNO REGISTRADOS CORRECTAMENTE")
                    conn.commit()
                except:
                    print("YA EXISTE UN ALUMNO CON ESA MATRICULA INTENTE DE NUEVO")
                    Opcion_1()
        else:
            print("30 ALUMNOS REGISTRADOS CORRECTAMENTE")
            registros_cant = registros_cant
            menu()
    else:
        print("NO HAY LUGARES DISPONIBLES")
        menu()

def Opcion_2():
    alumnos = conn.cursor()
    alumnos.execute("SELECT * FROM alumnos")
    registros = alumnos.fetchall()
    if registros:
        for idalumno,nombre in registros:
            print(f"INGRESA LAS CALIFICACIONES DE {nombre}: ")
            progra = int(input("Programacion: "))
            cal1 = conn.cursor()
            valores = {"idalumno":idalumno, "idmateria":1, "calificacion":progra}
            cal1.execute("INSERT INTO calificaciones VALUES(:idalumno,:idmateria,:calificacion)", valores)
            base = int(input("Base de datos: "))
            cal2 = conn.cursor()
            valores = {"idalumno":idalumno, "idmateria":2, "calificacion":base}
            cal2.execute("INSERT INTO calificaciones VALUES(:idalumno,:idmateria,:calificacion)", valores)
            macro = int(input("Macroeconomia: "))
            cal3 = conn.cursor()
            valores = {"idalumno":idalumno, "idmateria":3, "calificacion":macro}
            cal3.execute("INSERT INTO calificaciones VALUES(:idalumno,:idmateria,:calificacion)", valores)
            est = int(input("Estadistica: "))
            cal4 = conn.cursor()
            valores = {"idalumno":idalumno, "idmateria":4, "calificacion":est}
            cal4.execute("INSERT INTO calificaciones VALUES(:idalumno,:idmateria,:calificacion)", valores)
            conta = int(input("Contabilidad: "))
            cal5 = conn.cursor()
            valores = {"idalumno":idalumno, "idmateria":5, "calificacion":macro}
            cal5.execute("INSERT INTO calificaciones VALUES(:idalumno,:idmateria,:calificacion)", valores)
    else:
        print("Debe capturar los datos de los alumnos en la opcion 1 del menu")
        menu()
    conn.commit()
    print("CALIFICACIONES AGREGADAS CORRECTAMENTE")
    print(separador)
    menu()
    
def Opcion_3():
    idalumno = int(input("Ingresa la matricula del alumno para ver sus calificaciones: "))
    cal_alumno = conn.cursor()
    valores = {"idalumno":idalumno}
    cal_alumno.execute("SELECT nombre, calificacion FROM calificaciones JOIN materias ON calificaciones.idmateria = materias.idmateria WHERE idalumno=:idalumno", valores)
    calificaciones = cal_alumno.fetchall()
    nom_alumno = conn.cursor()
    nom_alumno.execute("SELECT nombre FROM alumnos WHERE idalumno=:idalumno", valores)
    nombre = nom_alumno.fetchall()
    nom = nombre[0]
    n = str(nom[0])
    if calificaciones:
        print(f"Calificaciones de {n}")
        for nombre,calificacion in calificaciones:
            print(f"{nombre}\t",end="")
            print(calificacion)
    else:
        print(f"No existe un alumno con la matricula {idalumno}, intenta con otra")
        Opcion_3()
    print(separador)
    menu()

def Opcion_4():
    idmateria = conn.cursor()
    idmateria.execute("SELECT idmateria FROM materias GROUP BY idmateria")
    materias = idmateria.fetchall()
    archivoTexto = open("Reportepormateria.txt", "w")
    archivoTexto.write("REPORTE DE CALIFICACIONES POR ALUMNOS \n")
    for claves in materias:
        clave = int(claves[0])     
        valores = {"idmateria":clave}
        nom_mat = conn.cursor()
        nom_mat.execute("SELECT nombre FROM materias WHERE idmateria=:idmateria", valores)
        nom_materia = nom_mat.fetchall()
        n = nom_materia[0]
        nom = str(n[0])
        print(f"{nom}\n")
        archivoTexto.write(f"\n{nom}\n")
        calif = conn.cursor()
        calif.execute("SELECT nombre, calificacion FROM calificaciones JOIN alumnos ON alumnos.idalumno = calificaciones.idalumno WHERE idmateria=:idmateria", valores)
        calificaciones = calif.fetchall()
        for nombre, calificacion in  calificaciones:
            print(f"{nombre}\t", end="")
            print(calificacion)
            archivoTexto.write(f"{nombre}\t")
            archivoTexto.write(str(f"{calificacion}\n"))
        print("\n")
    importacion = int(input("Desea importar el reporte aun archivo .txt? 1) Si 0) No, regresar al menu:"))
    if importacion == 1:
        archivoTexto.close()
        print("ARCHIVO IMPORTADO")
    else:
        archivoTexto.close()
        remove("Reportepormateria.txt")
        menu()
    print(separador)
    menu()

def Opcion_5():
    idalumno = conn.cursor()
    idalumno.execute("SELECT idalumno FROM alumnos GROUP BY idalumno")
    alumnos = idalumno.fetchall()
    archivoTexto2 = open("Reporteporestudiante.txt", "w")
    archivoTexto2.write("REPORTE DE CALIFICACIONES POR MATERIA \n")
    for claves in alumnos:
        clave = int(claves[0])
        valores = {"idalumno":clave}
        nom_alum = conn.cursor()
        nom_alum.execute("SELECT nombre FROM alumnos WHERE idalumno=:idalumno", valores)
        nom_alumno = nom_alum.fetchall()
        n = nom_alumno[0]
        nom = str(n[0])
        print(f"{nom}\n")
        archivoTexto2.write(f"\n{nom}\n")
        calif = conn.cursor()
        calif.execute("SELECT nombre, calificacion FROM calificaciones JOIN materias ON materias.idmateria = calificaciones.idmateria WHERE idalumno=:idalumno", valores)
        calificaciones = calif.fetchall()
        for nombre, calificacion in  calificaciones:
            print(f"{nombre}\t", end="")
            print(calificacion)
            archivoTexto2.write(f"{nombre}\t")
            archivoTexto2.write(str(f"{calificacion}\n"))
        print("\n")
    importacion = int(input("Desea importar el reporte aun archivo .txt? 1) Si 0) No, regresar al menu: "))
    if importacion == 1:
        archivoTexto2.close()
        print("ARCHIVO IMPORTADO")
    else: 
        archivoTexto2.close()
        remove("Reporteporestudiante.txt")
        menu()
    print(separador)
    menu()


def Opcion_6():
    materias = conn.cursor()
    nombre = conn.cursor()
    materias.execute("SELECT AVG(calificacion) FROM calificaciones GROUP BY idmateria")
    nombre.execute("SELECT nombre FROM materias")
    materias_ = materias.fetchall()
    nombre_ = nombre.fetchall()
    print("PROMEDIO DE CALIFICACIONES DE CADA MATERIA")
    for nombre, promedio in zip(nombre_,materias_):
        print(f"{nombre[0]}\t", end="")
        print(*promedio)
    print("LA MATERIA CON MAS BAJO RENDIMIENTO ES:")
    materia_baja = min(materias_)
    indice = materias_.index(materia_baja)
    nombremateria = nombre_[indice]
    print(f"{nombremateria[0]}\t", end="")
    print(*materia_baja)
    print(separador)
    menu()

def Opcion_7():
    reprobados = conn.cursor()
    reprobados.execute("SELECT idalumno, COUNT(calificacion) FROM calificaciones WHERE calificacion<70 GROUP BY idalumno ")
    reprobados_ = reprobados.fetchall()
    print("MATRICULA / MATERIAS REPROBADAS")
    for idalumno,reprobadas in reprobados_:
        if reprobadas >2:
            print(f"{idalumno}\t\t", end = "")
            print(reprobadas)
    print(separador)
    menu()
    
def Opcion_8():
    alumnos = conn.cursor()
    alumnos.execute("SELECT idalumno, nombre FROM alumnos")
    alumnos_ = alumnos.fetchall()
    print("LISTADO DE ALUMNOS")
    for idalu,nombre in alumnos_:
        print(f"{idalu}\t", end="")
        print(nombre)
    print(separador)
    
menu()
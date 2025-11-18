#tobias Artal
#programacion 1 - parcial


import os
import csv

RUTA_ARCHIVO_ALUMNOS = "alumnos.csv"

# lee el archivo alumnos.csv si existe y arma la lista de estudiantes
def leer_archivo_alumnos_si_existe():
    lista_estudiantes = []
    if os.path.exists(RUTA_ARCHIVO_ALUMNOS):
        with open(RUTA_ARCHIVO_ALUMNOS, "r", newline="", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                try:
                    nombre = fila["nombre"].strip()
                    nota = int(fila["nota"])
                    lista_estudiantes.append({"nombre": nombre, "nota": nota})
                except (ValueError, KeyError):
                    pass
    return lista_estudiantes

# pide un numero entero dentro de un rango y valida que sea correcto.
def pedir_numero_entero_en_rango(mensaje, valor_minimo, valor_maximo):
    while True:
        dato = input(mensaje).strip()
        if dato == "":
            print("debe ingresar un numero")
            continue
        try:
            n = int(dato)
            if n < valor_minimo or n > valor_maximo:
                print("fuera de rango, debe ser entre", valor_minimo, "y", valor_maximo)
            else:
                return n
        except ValueError:
            print("dato invalido, debe ser entero")

# pausa para que el usuario lea la salida
def esperar_tecla():
    input("\npresione enter para continuar...")

# guarda la lista completa en el archivo .csv
def guardar_lista_en_csv(lista_estudiantes):
    with open(RUTA_ARCHIVO_ALUMNOS, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["nombre", "nota"])
        for e in lista_estudiantes:
            escritor.writerow([e["nombre"], e["nota"]])

# carga N estudiantes validando nombre y nota.
def cargar_datos_de_estudiantes(lista_estudiantes):
    cantidad = pedir_numero_entero_en_rango("cuantos estudiantes desea cargar? ", 1, 1000)
    for i in range(cantidad):
        print("\nregistro", i + 1)
        while True:
            nombre = input("nombre del estudiante: ").strip()
            if nombre == "":
                print("el nombre no puede estar vacio")
            else:
                break
        nota = pedir_numero_entero_en_rango("nota (0 a 10): ", 0, 10)
        lista_estudiantes.append({"nombre": nombre, "nota": nota})
    guardar_lista_en_csv(lista_estudiantes)
    print("\ncarga completa. total de estudiantes:", len(lista_estudiantes))

# muestra listado de estudiantes en formato tabla
def mostrar_listado_de_estudiantes(lista_estudiantes):
    if len(lista_estudiantes) == 0:
        print("no hay estudiantes cargados todavia")
        return
    print("\n-------------------------------------------")
    print("listado de estudiantes")
    print("-------------------------------------------")
    for e in lista_estudiantes:
        print("Nombre:", e["nombre"], " | Nota:", e["nota"])
    print("-------------------------------------------")
    print("total de estudiantes:", len(lista_estudiantes))
    print("-------------------------------------------")

# busca por nombre sin importar mayusculas
def buscar_estudiante_por_nombre(lista_estudiantes):
    if len(lista_estudiantes) == 0:
        print("no hay estudiantes cargados para buscar")
        return
    nombre_buscado = input("ingrese el nombre que desea buscar: ").strip()
    encontrado = False
    for e in lista_estudiantes:
        if e["nombre"].lower() == nombre_buscado.lower():
            print("\nestudiante encontrado!")
            print("Nombre:", e["nombre"], " | Nota:", e["nota"])
            encontrado = True
            break
    if not encontrado:
        print("no se encontro ningun estudiante con ese nombre")

def mostrar_menu_principal():
    print("\nmenu principal")
    print("1) agregar/modificar datos")
    print("2) mostrar lista")
    print("3) buscar estudiante")
    print("4) salir del programa")

if __name__ == "__main__":
    lista_estudiantes = leer_archivo_alumnos_si_existe()
    if len(lista_estudiantes) > 0:
        print("se cargaron", len(lista_estudiantes), "estudiantes desde", RUTA_ARCHIVO_ALUMNOS)

    seguir = True
    while seguir:
        mostrar_menu_principal()
        opcion = pedir_numero_entero_en_rango("opcion: ", 1, 4)

        if opcion == 1:
            print("\n////////////////// elegiste la opcion 1 (agregar / modificar datos) ///////////////////////")
            if os.path.exists(RUTA_ARCHIVO_ALUMNOS):
                print("\n/////// se encontro un archivo .csv //////")
                print("//////// que desea hacer? ///////////")
                eleccion = ""
                while eleccion not in ("a", "b", "c"):
                    print("\na) reemplazar los datos")
                    print("b) agregar nuevos registros")
                    print("c) volver")
                    eleccion = input("elige a/b/c: ").strip().lower()

                if eleccion == "a":
                    lista_estudiantes = []
                    cargar_datos_de_estudiantes(lista_estudiantes)
                elif eleccion == "b":
                    if len(lista_estudiantes) == 0:
                        lista_estudiantes = leer_archivo_alumnos_si_existe()
                    cargar_datos_de_estudiantes(lista_estudiantes)

            else:
                print("\n/////// no se encontro un archivo .csv //////")
                print("//////// crear uno nuevo ///////////")
                eleccion = ""
                while eleccion not in ("a", "c"):
                    print("\na) agregar nuevos registros")
                    print("c) volver")
                    eleccion = input("elige a/c: ").strip().lower()

                if eleccion == "a":
                    lista_estudiantes = []
                    cargar_datos_de_estudiantes(lista_estudiantes)

            esperar_tecla()

        elif opcion == 2:
            if len(lista_estudiantes) == 0 and not os.path.exists(RUTA_ARCHIVO_ALUMNOS):
                print("no hay datos. primero use opcion 1 para cargar")
            else:
                if len(lista_estudiantes) == 0:
                    lista_estudiantes = leer_archivo_alumnos_si_existe()
                mostrar_listado_de_estudiantes(lista_estudiantes)
            esperar_tecla()

        elif opcion == 3:
            if len(lista_estudiantes) == 0 and not os.path.exists(RUTA_ARCHIVO_ALUMNOS):
                print("no hay datos. primero use opcion 1 para cargar")
            else:
                if len(lista_estudiantes) == 0:
                    lista_estudiantes = leer_archivo_alumnos_si_existe()
                buscar_estudiante_por_nombre(lista_estudiantes)
            esperar_tecla()

        else:
            print("fin del programa. hasta luego.")
            seguir = False

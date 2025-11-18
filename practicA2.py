from practica_pp.biblioteca.input import get_int
import colorama
import os
import csv
import time
colorama.init()

def mostrar_reservas(reservas: list[dict]) -> None:
    print(colorama.Fore.BLUE + "Mostrar reservas")
    if not reservas:
        print("No hay reservas para mostrar.")
        return
    
    print(f"{'ID':<5} {'Docente':<20} {'Materia':<20} {'Fecha':<12} {'Aula':<10} {'Horas Reservadas':<15}")
    print("-" * 85)
    for reserva in reservas:
        id = reserva['id']
        docente = reserva['docente']
        materia = reserva['materia']
        fecha = reserva['fecha']
        aula = reserva['aula']
        horas_reservadas = reserva['horas_reservadas']
        print(f"{id:<5} {docente:<20} {materia:<20} {fecha:<12} {aula:<10} {horas_reservadas:<15}")
    print(colorama.Style.RESET_ALL)

def cargar_reserva(reservas: list[dict]) -> None:
    print(colorama.Fore.BLUE + "Cargar reservas")

    # Verifico si el archivo existe
    if os.path.exists("reservas.csv"):
        opcion = get_int("El archivo reservas.csv ya existe. ¿Desea reemplazar los datos existentes (1) o agregar nuevas reservas (2)? ", "Opción no válida. Ingrese 1 o 2.", 1, 2, 3)
        if opcion is None:
            print("Se cancela la operacion de carga de reservas.")
            return
        
        if opcion == 1:
            # Limpio la lista y creo archivo nuevo
            reservas.clear()
            with open("reservas.csv", "w", newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["id", "docente", "materia", "fecha", "aula", "horas_reservadas"])

        elif opcion == 2:
            # Cargo reservas existentes del archivo
            with open("reservas.csv", "r") as file:
                reader = csv.DictReader(file)
                reservas.clear()  # Limpiar la lista actual
                for row in reader:
                    reservas.append({
                        'id': int(row['id']),
                        'docente': row['docente'],
                        'materia': row['materia'],
                        'fecha': row['fecha'],
                        'aula': row['aula'],
                        'horas_reservadas': int(row['horas_reservadas'])
                    })
    else:
        # Si no existe el archivo, creo uno nuevo
        with open("reservas.csv", "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["id", "docente", "materia", "fecha", "aula", "horas_reservadas"])

    # Creo reservas nuevas ya sea que el archivo no existia o se eligio agregar nuevas reservas
    while True:
        print("\n--- Agregar nueva reserva ---")

        # Genero ID autoincremental
        if len(reservas) == 0:
            nuevo_id = 1
        else:
            # Obtengo el ID máximo existente
            nuevo_id = max(reserva['id'] for reserva in reservas) + 1

        # Solicito  de la reserva
        from biblioteca.input import get_string, get_float

        docente = get_string("Ingrese el nombre del docente: ", "Nombre no válido", 2, 50, 3)
        if docente is None:
            print("Se cancela la carga de la reserva.")
            break

        materia = get_string("Ingrese la materia de la reserva: ", "Materia no válida", 2, 50, 3)
        if materia is None:
            print("Se cancela la carga de la reserva.")
            break

        fecha = get_string("Ingrese la fecha de la reserva (DD/MM/AAAA): ", "Fecha no válida", 10, 10, 3)
        if fecha is None:
            print("Se cancela la carga de la reserva.")
            break

        aula = get_string("Ingrese el aula de la reserva: ", "Aula no válida", 2, 10, 3)
        if aula is None:
            print("Se cancela la carga de la reserva.")
            break

        horas_reservadas = get_int("Ingrese la cantidad de horas reservadas: ", "Horas no válidas", 1, 10, 3)
        if horas_reservadas is None:
            print("Se cancela la carga de la reserva.")
            break

        estado = get_string("Ingrese el estado de la reserva (Nuevo/Usado/Dañado): ", "Estado no válido", 4, 15, 3)
        if estado is None:
            print("Se cancela la carga de la reserva.")
            break

        nuev_reserva = {
            'id': nuevo_id,
            'docente': docente,
            'materia': materia,
            'fecha': fecha,
            'aula': aula,
            'horas_reservadas': horas_reservadas
        }
        
        # Agrego a la lista
        reservas.append(nueva_reserva)

        # Guardo en el archivo CSV
        with open("reservas.csv", "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([nuevo_id, docente, materia, fecha, aula, horas_reservadas])
        
        print(f"Reserva '{docente}' agregada exitosamente con ID {nuevo_id}")

        # Preguntar si desea agregar otra reserva
        continuar = get_int("¿Desea agregar otra reserva? (1=Sí, 2=No): ", "Opción no válida", 1, 2, 3)
        if continuar != 1:
            break

    print(f"Carga completada. Total de reservas: {len(reservas)}")
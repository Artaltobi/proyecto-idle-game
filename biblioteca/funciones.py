import sys
import os
import csv
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from biblioteca.input import get_int

"""
Opción 1. Cargar equipos
Permitir ingresar N equipos (cantidad pedida al usuario).
Cada equipo se representa con un diccionario con las claves:
"id" (entero autoincremental),
"nombre",
"categoria" (router, pc, notebook, impresora),
"estado" (funcional o fuera de servicio),
"valor" (float, validado como número positivo).
Los datos se guardan en una lista y también en el archivo equipos.csv.
Si el archivo ya existe, preguntar:
“¿Desea reemplazar los datos existentes o agregar nuevos equipos?”

"""
import time
def p(message: str) -> None:
  for letter in message:
    print(letter, end='', flush=True)
    time.sleep(0.01)

import colorama
colorama.init()

def cargar_equipos(equipos: list[dict]) -> None:
    print(colorama.Fore.CYAN + colorama.Style.BRIGHT + "🔧 CARGAR EQUIPOS" + colorama.Style.RESET_ALL)
    
    # Verifico si el archivo existe
    if os.path.exists("equipos.csv"):
        opcion = get_int("El archivo equipos.csv ya existe. ¿Desea reemplazar los datos existentes (1) o agregar nuevos equipos (2)? ", "Opción no válida. Ingrese 1 o 2.", 1, 2, 3)
        if opcion is None:
            print("Se cancela la operacion de carga de equipos.")
            return
        
        if opcion == 1:
            # Limpio la lista y creo archivo nuevo
            equipos.clear()
            with open("equipos.csv", "w", newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["id", "nombre", "categoria", "estado", "valor"])
        
        elif opcion == 2:
            # Cargo equipos existentes del archivo
            with open("equipos.csv", "r") as file:
                reader = csv.DictReader(file)
                equipos.clear()  # Limpiar la lista actual
                for row in reader:
                    # 
                    equipos.append({
                        'id': int(row['id']),
                        'nombre': row['nombre'],
                        'categoria': row['categoria'],
                        'estado': row['estado'],
                        'valor': float(row['valor'])
                    })
    else:
        # Si no existe el archivo, creo uno nuevo
        with open("equipos.csv", "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["id", "nombre", "categoria", "estado", "valor"])
    
    # Creo equipos nuevos ya sea que el archivo no existia o se eligio agregar nuevos equipos
    while True:
        print("\n--- Agregar nuevo equipo ---")
        
        # Genero ID autoincremental
        if len(equipos) == 0:
            nuevo_id = 1
        else:
            # Obtengo el ID máximo existente
            nuevo_id = max(equipo['id'] for equipo in equipos) + 1
        
        # Solicito datos del equipo
        from biblioteca.input import get_string, get_float
        
        nombre = get_string("Ingrese el nombre del equipo: ", "Nombre no válido", 2, 50, 3)
        if nombre is None:
            print("Se cancela la carga del equipo.")
            break

        categoria = get_string("Ingrese la categoria del equipo (router, pc, notebook, impresora): ", "Categoria no válida", 2, 30, 3)
        if categoria is None:
            print("Se cancela la carga del equipo.")
            break
            
        estado = get_string("Ingrese el estado del equipo (Nuevo/Usado/Dañado): ", "Estado no válido", 4, 15, 3)
        if estado is None:
            print("Se cancela la carga del equipo.")
            break
            
        valor = get_float("Ingrese el valor del equipo: $", "Valor no válido", 0, 999999, 3)
        if valor is None:
            print("Se cancela la carga del equipo.")
            break
        
        nuevo_equipo = {
            'id': nuevo_id,
            'nombre': nombre,
            'categoria': categoria,
            'estado': estado,
            'valor': valor
        }
        
        # Agrego a la lista
        equipos.append(nuevo_equipo)
        
        # Guardo en el archivo CSV
        with open("equipos.csv", "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([nuevo_id, nombre, categoria, estado, valor])
        
        print(f"Equipo '{nombre}' agregado exitosamente con ID {nuevo_id}")
        
        # Preguntar si desea agregar otro equipo
        continuar = get_int("¿Desea agregar otro equipo? (1.Sí, 2.No): ", "Opción no válida", 1, 2, 3)
        if continuar != 1:
            break
    
    print(f"Carga completada. Total de equipos: {len(equipos)}")
                
def mostrar_equipos(lista_equipos: list[dict]) -> None:
    if len(lista_equipos) == 0:
        print(colorama.Fore.RED + "❌ No hay equipos cargados." + colorama.Style.RESET_ALL)
        return
    
    print(colorama.Fore.GREEN + colorama.Style.BRIGHT + "📋 INVENTARIO DE EQUIPOS" + colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW + "=" * 80 + colorama.Style.RESET_ALL)
    
    for equipo in lista_equipos:
        # Color según el estado
        if equipo['estado'].lower() in ['nuevo', 'funcional']:
            color_estado = colorama.Fore.GREEN
        elif equipo['estado'].lower() in ['usado']:
            color_estado = colorama.Fore.YELLOW
        else:  # dañado, fuera de servicio
            color_estado = colorama.Fore.RED
            
        print(f"{colorama.Fore.CYAN}ID: {equipo['id']:3d}{colorama.Style.RESET_ALL} | "
              f"{colorama.Fore.BLUE}Nombre: {equipo['nombre']:<20}{colorama.Style.RESET_ALL} | "
              f"{colorama.Fore.MAGENTA}Categoría: {equipo['categoria']:<12}{colorama.Style.RESET_ALL} | "
              f"{color_estado}Estado: {equipo['estado']:<15}{colorama.Style.RESET_ALL} | "
              f"{colorama.Fore.GREEN}Valor: ${equipo['valor']:>8.2f}{colorama.Style.RESET_ALL}")
    
    print(colorama.Fore.YELLOW + "=" * 80 + colorama.Style.RESET_ALL)
    print(f"{colorama.Fore.WHITE}Total de equipos: {len(lista_equipos)}{colorama.Style.RESET_ALL}")
        
def buscar_equipo(lista_equipos: list[dict]) -> None:
    if len(lista_equipos) == 0:
        print("No hay equipos cargados.")
        return
    id_buscar = get_int("Ingrese el ID del equipo a buscar: ", "ID no válido. Ingrese un número entero positivo.", 1, 999999, 3)
    if id_buscar is None:
        print("Operación cancelada.")
        return
    for equipo in lista_equipos:
        if equipo['id'] == id_buscar:
            print(f"Equipo encontrado: ID: {equipo['id']}, Nombre: {equipo['nombre']}, Categoría: {equipo['categoria']}, Estado: {equipo['estado']}, Valor: ${equipo['valor']:.2f}")
            return
    print("Equipo no encontrado.")
    
def estadisticas(lista_equipos: list[dict]) -> None:
    if len(lista_equipos) == 0:
        print("No hay equipos cargados.")
        return
    total_equipos = len(lista_equipos)
    valor_total = sum(equipo['valor'] for equipo in lista_equipos)
    valor_promedio = valor_total / total_equipos
    print(f"Total de equipos: {total_equipos}")
    print(f"Valor total del inventario: ${valor_total:.2f}")
    print(f"Valor promedio por equipo: ${valor_promedio:.2f}")
    
def filtrar_por_categoria(lista_equipos: list[dict]) -> None:
    if len(lista_equipos) == 0:
        print("No hay equipos cargados.")
        return
    categoria = input("Ingrese la categoría a filtrar (router, pc, notebook, impresora): ").strip().lower()
    categorias_validas = {"router", "pc", "notebook", "impresora"}
    if categoria not in categorias_validas:
        print("Categoría no válida.")
        return
    equipos_filtrados = [equipo for equipo in lista_equipos if equipo['categoria'] == categoria]
    if not equipos_filtrados:
        print(f"No hay equipos en la categoría '{categoria}'.")
        return
    print(f"Equipos en la categoría '{categoria}':")
    for equipo in equipos_filtrados:
        print(f"ID: {equipo['id']}, Nombre: {equipo['nombre']}, Estado: {equipo['estado']}, Valor: ${equipo['valor']:.2f}")

def ordenar_por_valor(lista_equipos: list[dict]) -> None:
    if len(lista_equipos) == 0:
        print("No hay equipos cargados.")
        return
    equipos_ordenados = sorted(lista_equipos, key=lambda x: x['valor'], reverse=True)
    print(f"{colorama.Fore.BLUE}Equipos ordenados por valor (de mayor a menor):{colorama.Style.RESET_ALL}")
    for equipo in equipos_ordenados:
        print(f"{colorama.Fore.BLUE}ID: {equipo['id']}{colorama.Style.RESET_ALL}, "
              f"{colorama.Fore.CYAN}Nombre: {equipo['nombre']}{colorama.Style.RESET_ALL}, "
              f"{colorama.Fore.MAGENTA}Categoria: {equipo['categoria']}{colorama.Style.RESET_ALL}, "
              f"{colorama.Fore.YELLOW}Estado: {equipo['estado']}{colorama.Style.RESET_ALL}, "
              f"{colorama.Fore.GREEN}Valor: ${equipo['valor']:.2f}{colorama.Style.RESET_ALL}")

def generar_informe(lista_equipos: list[dict]) -> None:
    if len(lista_equipos) == 0:
        print(colorama.Fore.RED + "❌ No hay equipos cargados para generar el informe." + colorama.Style.RESET_ALL)
        return
    
    try:
        from datetime import datetime
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        with open("informe_inventario.txt", "w", encoding="utf-8") as file:
            # Encabezado del informe
            file.write("=" * 80 + "\n")
            file.write("                    INFORME DE INVENTARIO DE EQUIPOS\n")
            file.write("=" * 80 + "\n")
            file.write(f"Fecha de generación: {fecha_actual}\n")
            file.write(f"Total de equipos registrados: {len(lista_equipos)}\n\n")
            
            # Listado detallado de equipos
            file.write("LISTADO DETALLADO DE EQUIPOS:\n")
            file.write("-" * 80 + "\n")
            file.write(f"{'ID':<4} | {'NOMBRE':<25} | {'CATEGORÍA':<12} | {'ESTADO':<15} | {'VALOR':<10}\n")
            file.write("-" * 80 + "\n")
            
            for equipo in lista_equipos:
                file.write(f"{equipo['id']:<4} | {equipo['nombre']:<25} | {equipo['categoria']:<12} | {equipo['estado']:<15} | ${equipo['valor']:<9.2f}\n")
            
            file.write("-" * 80 + "\n\n")
            
            # Estadísticas del inventario
            file.write("ESTADÍSTICAS DEL INVENTARIO:\n")
            file.write("-" * 40 + "\n")
            
            total_equipos = len(lista_equipos)
            valor_total = sum(equipo['valor'] for equipo in lista_equipos)
            valor_promedio = valor_total / total_equipos if total_equipos > 0 else 0
            
            # Estadísticas por categoría
            categorias = {}
            for equipo in lista_equipos:
                cat = equipo['categoria']
                if cat not in categorias:
                    categorias[cat] = {'cantidad': 0, 'valor_total': 0}
                categorias[cat]['cantidad'] += 1
                categorias[cat]['valor_total'] += equipo['valor']
            
            # Estadísticas por estado
            estados = {}
            for equipo in lista_equipos:
                est = equipo['estado']
                if est not in estados:
                    estados[est] = 0
                estados[est] += 1
            
            file.write(f"Total de equipos: {total_equipos}\n")
            file.write(f"Valor total del inventario: ${valor_total:.2f}\n")
            file.write(f"Valor promedio por equipo: ${valor_promedio:.2f}\n\n")
            
            file.write("DISTRIBUCIÓN POR CATEGORÍAS:\n")
            for categoria, datos in categorias.items():
                file.write(f"  - {categoria}: {datos['cantidad']} equipos (${datos['valor_total']:.2f})\n")
            
            file.write(f"\nDISTRIBUCIÓN POR ESTADOS:\n")
            for estado, cantidad in estados.items():
                porcentaje = (cantidad / total_equipos) * 100
                file.write(f"  - {estado}: {cantidad} equipos ({porcentaje:.1f}%)\n")
            
            file.write("\n" + "=" * 80 + "\n")
            file.write("Informe generado por Sistema de Inventario v1.0\n")
            file.write("=" * 80 + "\n")
        
        print(colorama.Fore.GREEN + "✅ Informe generado exitosamente en 'informe_inventario.txt'" + colorama.Style.RESET_ALL)
        
    except Exception as e:
        print(colorama.Fore.RED + f"❌ Error al generar el informe: {e}" + colorama.Style.RESET_ALL)


def salir(equipos: list[dict]) -> None:
    print(f"{colorama.Fore.YELLOW}🔄 Cerrando el sistema...{colorama.Style.RESET_ALL}")
    if len(equipos) > 0:
        print(f"{colorama.Fore.GREEN}💾 Se han guardado {len(equipos)} equipos en el inventario.{colorama.Style.RESET_ALL}")
    print(f"{colorama.Fore.CYAN}✨ Sistema cerrado correctamente. ¡Hasta pronto!{colorama.Style.RESET_ALL}")
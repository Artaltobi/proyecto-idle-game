import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import csv
import colorama
colorama.init()

#
from biblioteca.funciones import cargar_equipos, mostrar_equipos, buscar_equipo, estadisticas, filtrar_por_categoria, ordenar_por_valor, generar_informe, salir
from biblioteca.input import get_int


def init():
    MENU = {
        "1": cargar_equipos,
        "2": mostrar_equipos,
        "3": buscar_equipo,
        "4": estadisticas,
        "5": filtrar_por_categoria,
        "6": ordenar_por_valor,
        "7": generar_informe,
        "8": salir
    }
    
    MENSAJE_MENU = f"""
{colorama.Fore.CYAN}{colorama.Style.BRIGHT}
╔══════════════════════════════════════════════════════════════════════════════╗
║                        🖥️  SISTEMA DE INVENTARIO DE EQUIPOS                 ║
╚══════════════════════════════════════════════════════════════════════════════╝
{colorama.Style.RESET_ALL}
{colorama.Fore.YELLOW}┌─ MENÚ PRINCIPAL ───────────────────────────────────────────────────────────┐{colorama.Style.RESET_ALL}
{colorama.Fore.GREEN}│ 1. 📦 Cargar equipos                                                      │{colorama.Style.RESET_ALL}
{colorama.Fore.BLUE}│ 2. 📋 Mostrar inventario                                                   │{colorama.Style.RESET_ALL}
{colorama.Fore.MAGENTA}│ 3. 🔍 Buscar equipo                                                        │{colorama.Style.RESET_ALL}
{colorama.Fore.CYAN}│ 4. 📊 Estadísticas                                                         │{colorama.Style.RESET_ALL}
{colorama.Fore.WHITE}│ 5. 🏷️  Filtrar por categoría                                              │{colorama.Style.RESET_ALL}
{colorama.Fore.YELLOW}│ 6. 💰 Ordenar por valor                                                    │{colorama.Style.RESET_ALL}
{colorama.Fore.GREEN}│ 7. 📄 Generar informe TXT                                                  │{colorama.Style.RESET_ALL}
{colorama.Fore.RED}│ 8. 🚪 Salir                                                                │{colorama.Style.RESET_ALL}
{colorama.Fore.YELLOW}└────────────────────────────────────────────────────────────────────────────┘{colorama.Style.RESET_ALL}

{colorama.Fore.WHITE}Seleccione una opción (1-8): {colorama.Style.RESET_ALL}"""

    # Lista para almacenar los equipos
    equipos = []

    while(opcion := get_int(MENSAJE_MENU, "Opción no válida, solo debe ser de 1 a 8", 1, 8, 3)) != 8:
        print("")
        for numero in MENU:
            if str(opcion) == numero:
                try:
                    MENU[numero](equipos)
                except ValueError as ve:
                    print(f"{colorama.Fore.RED}❌ ERROR: {ve}{colorama.Style.RESET_ALL}")
                break
    
    print(f"\n{colorama.Fore.GREEN}{colorama.Style.BRIGHT}🎉 ¡Gracias por usar el Sistema de Inventario! 👋{colorama.Style.RESET_ALL}")
    print(f"{colorama.Fore.CYAN}Desarrollado con ❤️  - ¡Hasta luego!{colorama.Style.RESET_ALL}")

if __name__ == "__main__":
    init()
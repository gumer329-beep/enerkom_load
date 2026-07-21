#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# LayoutNewTPVAMEX.py - SCRIPT PRINCIPAL

import sys
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Agregar scripts al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scripts.config import TABLES_CONFIG, get_table_config
from libs.pipeline import run_pipeline
from scripts.services.cleaning_services import CLEANERS


def show_menu():
    """Muestra un menú para seleccionar la tabla a procesar"""
    print("\n" + "=" * 60)
    print("🚀 SELECCIONA LA TABLA DESTINO")
    print("=" * 60)

    table_names = list(TABLES_CONFIG.keys())
    for i, name in enumerate(table_names, 1):
        print(f"  {i}. {name}")
    print(f"  {len(table_names)+1}. Salir")
    print("=" * 60)

    while True:
        try:
            choice = input("\n📌 Elige una opción: ").strip()
            if choice == str(len(table_names) + 1):
                print("👋 Hasta luego")
                sys.exit(0)

            idx = int(choice) - 1
            if 0 <= idx < len(table_names):
                return table_names[idx]
            else:
                print("❌ Opción inválida, intenta de nuevo.")
        except ValueError:
            print("❌ Ingresa un número válido.")


def main():
    """Función principal - solo orquesta la ejecución"""
    # Muestra menú y obtiene tabla
    table_name = show_menu()
    print(f"\n📌 Tabla seleccionada: {table_name}")

    # Obtener configuración
    config = get_table_config(table_name)
    if not config:
        print(f"❌ No hay configuración para la tabla '{table_name}'")
        sys.exit(1)
    else:
        print(f"✅ Configuración encontrada para la tabla '{table_name}'")
        # Obtener función de limpieza (si existe)
        cleaner = CLEANERS.get(table_name)
        #print(cleaner().head(5))
        if cleaner is not None:
            print(
                f"🧹 Ejecutando limpieza de datos para '{table_name}' usando '{cleaner.__name__}'..."
            )
            # Ejecutar pipeline ETL
            run_pipeline(cleaner(), config, table_name, verbose=True)
        else:
            raise NotImplementedError(
                f"No hay función de limpieza definida para '{table_name}' no se cargará en la base de datos."
            )


if __name__ == "__main__":
    main()

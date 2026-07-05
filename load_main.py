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

from libs.pipeline import run_pipeline
from scripts.services.cleaning_services import clean_enerkom_data

def main():
    """Función principal - solo orquesta la ejecución"""
    df = clean_enerkom_data()
    
    # Ejecutar pipeline ETL
    run_pipeline(df)

if __name__ == "__main__":
    main()
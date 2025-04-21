from flask import Flask, jsonify
import json
from informes.src.adapters.lector_pdf_pdfplumber import LectorPDFPdfPlumber
from informes.src.application.usecase.extraer_alertas_usecase import ExtraerAlertasUseCase
from informes.src.application.usecase.extraer_aplicaciones_usecase import ExtraerAplicacionesUseCase
from informes.src.application.usecase.extraer_summary_usecase import ExtraerSummaryUseCase
from informes.src.application.usecase.extraer_toptalkers import ExtraerTopTalkersUseCase
from informes.src.Infraestructure.controllers.summary_plotter import plot_summary  # <- Aquí está tu función de graficado

app = Flask(__name__)

lector = LectorPDFPdfPlumber()
alertas_usecase = ExtraerAlertasUseCase(lector)
aplicaciones_usecase = ExtraerAplicacionesUseCase(lector)
summary_usecase = ExtraerSummaryUseCase(lector)
toptalkers_usecase = ExtraerTopTalkersUseCase(lector)

# Rutas Flask (comentadas si solo usas consola)
"""
@app.route("/extraer-alertas")
def extraer_alertas():
    ruta = "ECOSU-S-CLP-GL-PKF001_alerts.pdf"
    data = alertas_usecase.ejecutar(ruta)
    return jsonify(data)

@app.route("/extraer-aplicaciones")
def extraer_aplicaciones():
    ruta = "ECOSU-S-CLP-GL-PKF001_applications.pdf"
    data = aplicaciones_usecase.ejecutar(ruta)
    return jsonify(data)

@app.route("/extraer-summary")
def extraer_summary():
    data = summary_usecase.ejecutar("ECOSU-S-CLP-GL-PKF001_summary.pdf")
    return jsonify(data)

@app.route("/extraer-toptalkers")
def extraer_toptalkers():
    data = toptalkers_usecase.ejecutar("ECOSU-S-CLP-GL-PKF001_toptalkers.pdf")
    return jsonify(data)
"""

def menu_consola():
    print("=== Menú de extracción de PDF ===")
    print("1. Extraer alertas")
    print("2. Extraer aplicaciones")
    print("3. Extraer resumen de tráfico (con gráfico)")
    print("4. Extraer toptalkers")
    print("0. Salir")
    
    while True:
        opcion = input("\nSelecciona una opción: ")
        if opcion == "1":
            resultado = alertas_usecase.ejecutar("ECOSU-S-CLP-GL-PKF001_alerts.pdf")
            print(json.dumps(resultado, indent=2))
        elif opcion == "2":
            resultado = aplicaciones_usecase.ejecutar("ECOSU-S-CLP-GL-PKF001_applications.pdf")
            print(json.dumps(resultado, indent=2))
        elif opcion == "3":
            resultado = summary_usecase.ejecutar("ECOSU-S-CLP-GL-PKF001_summary.pdf")
            print(json.dumps(resultado, indent=2))
            plot_summary(resultado["summary"])  
        elif opcion == "4":
            resultado = toptalkers_usecase.ejecutar("ECOSU-S-CLP-GL-PKF001_toptalkers.pdf")
            print(json.dumps(resultado, indent=2))
        elif opcion == "0":
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    menu_consola()

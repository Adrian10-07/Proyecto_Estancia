from flask import Blueprint, request, jsonify
from informes.src.Infraestructure.controllers.applicaciones_controller import AplicacionesController
import os
from typing import List

aplicaciones_blueprint = Blueprint('aplicaciones', __name__)
controller = AplicacionesController()

@aplicaciones_blueprint.route('/aplicaciones', methods=['POST'])
def extract_aplicaciones():
    
    if 'files[]' not in request.files:
        return jsonify({"error": "No se proporcionaron archivos PDF", "suggestion": "Use el campo 'files[]' para enviar los archivos"}), 400
    
    files: List = request.files.getlist('files[]')
    if not files:
        return jsonify({"error": "Ningún archivo seleccionado"}), 400

    invalid_files = [f.filename for f in files if not f.filename.lower().endswith('.pdf')]
    if invalid_files:
        return jsonify({
            "error": "Algunos archivos no son PDF válidos",
            "invalid_files": invalid_files
        }), 400

    # Procesar archivos
    temp_files = []
    results = []
    
    try:
        os.makedirs('temp', exist_ok=True)
        
        for file in files:
            filepath = os.path.join('temp', file.filename)
            file.save(filepath)
            temp_files.append(filepath)

        # procesar todos juntos
        result = controller.process_aplicaciones_multiples(temp_files)

        return jsonify(result)


    except Exception as e:
        return jsonify({
            "error": f"Error general al procesar archivos: {str(e)}",
            "details": f"Falló en {len(temp_files)}/{len(files)} archivos"
        }), 500

    finally:
        for filepath in temp_files:
            if os.path.exists(filepath):
                os.remove(filepath)
from flask import Blueprint, request, jsonify
from informes.src.Infraestructure.controllers.summary_controller import SummaryController
import os
from typing import List

summary_blueprint = Blueprint('summary', __name__)
controller = SummaryController()

@summary_blueprint.route('/summary', methods=['POST'])
def extract_summary():
    if 'files[]' not in request.files:
        return jsonify({"error": "No se proporcionaron archivos PDF"}), 400

    files: List = request.files.getlist('files[]')
    if not files:
        return jsonify({"error": "Ningún archivo seleccionado"}), 400

    temp_files = []
    try:
        os.makedirs('temp', exist_ok=True)
        for file in files:
            filepath = os.path.join('temp', file.filename)
            file.save(filepath)
            temp_files.append(filepath)

        result = controller.process_summary_multiples(temp_files)
        return jsonify(result)

    except Exception as e:
        return jsonify({
            "error": f"Error al procesar archivos: {str(e)}"
        }), 500

    finally:
        for filepath in temp_files:
            if os.path.exists(filepath):
                os.remove(filepath)

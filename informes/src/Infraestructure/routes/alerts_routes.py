from flask import Blueprint, request, jsonify
import matplotlib
matplotlib.use('Agg')
from informes.src.Infraestructure.controllers.alerts_controller import AlertasController
import os

alertas_blueprint = Blueprint('alertas', __name__)

controller = AlertasController()

@alertas_blueprint.route('/alertas', methods=['POST'])
def extract_alertas():
    if 'files[]' not in request.files:
        return jsonify({"error": "No se proporcionaron archivos"}), 400

    files = request.files.getlist('files[]')

    if not files:
        return jsonify({"error": "Ningún archivo seleccionado"}), 400

    invalid_files = [f.filename for f in files if not f.filename.lower().endswith('.pdf')]
    if invalid_files:
        return jsonify({"error": f"Los siguientes archivos no son PDFs: {', '.join(invalid_files)}"}), 400

    try:
        os.makedirs('temp', exist_ok=True)
        filepaths = []

        for file in files:
            filepath = os.path.join('temp', file.filename)
            file.save(filepath)
            filepaths.append(filepath)

        result = controller.process_alertas_multiples(filepaths)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        for filepath in filepaths:
            if os.path.exists(filepath):
                os.remove(filepath)


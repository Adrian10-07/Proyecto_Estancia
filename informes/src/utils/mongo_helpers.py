from pymongo import MongoClient
import datetime
from core.database import MongoConnection

def guardar_pdf_en_mongo(collection_name: str, filename: str, base64_pdf: str):
    try:
        mongo_conn = MongoConnection()
        db = mongo_conn.get_db()
        collection = db[collection_name]

        document = {
            "filename": filename,
            "pdf_base64": base64_pdf,
            "fecha_guardado": datetime.datetime.now()
        }

        result = collection.insert_one(document)
        print(f"[OK] PDF guardado en MongoDB con ID: {result.inserted_id}")
        print(f"Guardando en base de datos: {db.name}, colección: {collection.name}")

    except Exception as e:
        print(f"[ERROR] No se pudo guardar el PDF en MongoDB: {e}")

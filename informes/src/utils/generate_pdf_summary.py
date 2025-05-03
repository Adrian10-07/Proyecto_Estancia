from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
)
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime
import os
import uuid
import matplotlib.pyplot as plt

def generar_pdf_summary(summary_list: list[dict], output_dir='temp') -> str:
    os.makedirs(output_dir, exist_ok=True)
    pdf_filename = os.path.join(output_dir, f"reporte_summary_{uuid.uuid4().hex}.pdf")
    imagenes_para_borrar = []

    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("Reporte de Métricas de Tráfico de Red (Summary)", styles['Title']))
    story.append(Paragraph(f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Este informe presenta estadísticas clave sobre el tráfico de red medido en bps (bits por segundo).", styles['Normal']))
    story.append(Paragraph("Las métricas incluyen tráfico entrante (In), saliente (Out), paquetes descartados (Dropped), y tráfico por backbone. Para cada uno se muestran los valores actuales, promedios, máximos y percentiles 95.", styles['Normal']))
    story.append(Spacer(1, 12))

    for i, resumen in enumerate(summary_list):
        story.append(Paragraph(f"🔹 Resumen #{i+1}", styles['Heading2']))
        for seccion, datos in resumen.items():
            story.append(Paragraph(f" Sección: <b>{seccion.capitalize()}</b>", styles['Heading3']))

            tabla_data = [['Current', 'Average', 'Max', '95th Percentile'],
                          [datos['current'], datos['average'], datos['max'], datos['percentile_95th']]]

            table = Table(tabla_data, colWidths=[100] * 4)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('BACKGROUND', (0, 1), (-1, 1), colors.beige),
            ]))
            story.append(table)
            story.append(Spacer(1, 6))

            # Crear gráfica para esta sección
            valores = [
                convertir_a_mbps(datos['current']),
                convertir_a_mbps(datos['average']),
                convertir_a_mbps(datos['max']),
                convertir_a_mbps(datos['percentile_95th']),
            ]
            etiquetas = ['Current', 'Average', 'Max', '95th %']

            plt.figure(figsize=(4, 3))
            plt.bar(etiquetas, valores, color='skyblue')
            plt.title(f"{seccion.capitalize()} (en Mbps)")
            plt.ylabel("Mbps")
            plt.tight_layout()

            image_path = os.path.join(output_dir, f"{seccion}_{uuid.uuid4().hex}.png")
            plt.savefig(image_path)
            plt.close()

            story.append(Image(image_path, width=300, height=180))
            story.append(Spacer(1, 12))
            imagenes_para_borrar.append(image_path)

        story.append(PageBreak())

    doc.build(story)

    for img_path in imagenes_para_borrar:
        if os.path.exists(img_path):
            os.remove(img_path)

    return pdf_filename


def convertir_a_mbps(valor_str: str) -> float:
    if not valor_str:
        return 0.0
    valor_str = valor_str.replace(" ", "").lower()
    try:
        if valor_str.endswith("kbps"):
            return float(valor_str[:-4]) / 1000
        elif valor_str.endswith("mbps"):
            return float(valor_str[:-4])
        elif valor_str.endswith("gbps"):
            return float(valor_str[:-4]) * 1000
        elif valor_str.endswith("bps"):
            return float(valor_str[:-3]) / 1_000_000
    except Exception:
        return 0.0
    return 0.0

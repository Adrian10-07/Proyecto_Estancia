import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import uuid
import os
from datetime import datetime
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
)
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generar_reporte_pdf(alertas: list[dict], output_dir='temp') -> str:
    if not alertas:
        raise ValueError("No se proporcionaron alertas para generar el reporte.")

    df = pd.DataFrame(alertas)
    
    plt.figure(figsize=(8, 5))
    sns.countplot(data=df, x='importance', order=['Low', 'Medium', 'High'], palette='pastel')
    plt.title('Cantidad de Alertas por Nivel de Importancia')
    plt.xlabel('Importancia')
    plt.ylabel('Cantidad')
    plt.tight_layout()

    image_path = os.path.join(output_dir, f"grafico_{uuid.uuid4().hex}.png")
    plt.savefig(image_path)
    plt.close()

    pdf_filename = os.path.join(output_dir, f"reporte_alertas_{uuid.uuid4().hex}.pdf")
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("Reporte de Alertas", styles['Title']))
    story.append(Paragraph(f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    story.append(Spacer(1, 12))

    story.append(Paragraph(f"Total de alertas procesadas: <b>{len(alertas)}</b>", styles['Normal']))
    resumen = df['importance'].value_counts().reindex(['High', 'Medium', 'Low']).fillna(0).astype(int)
    for nivel in ['High', 'Medium', 'Low']:
        story.append(Paragraph(f"→ {nivel}: {resumen[nivel]} alertas", styles['Normal']))
    story.append(Spacer(1, 12))
    #Grafica de barras
    story.append(Paragraph("Gráfico de Alertas por Importancia", styles['Heading2']))
    story.append(Image(image_path, width=400, height=250))
    story.append(Spacer(1, 24))

    # columnas de la tabla
    story.append(Paragraph("Muestra de alertas registradas:", styles['Heading2']))

    max_alertas = 10
    story.append(Paragraph(
        f"Mostrando {min(len(df), max_alertas)} de {len(df)} alertas registradas:", styles['Normal']
    ))
    story.append(Spacer(1, 6))

    tabla_data = [['ID', 'Importancia', 'Clasificación', 'Mes de registro', 'Duración', 'Rendimiento', 'Impacto']] + [
        [
            str(row.get('id', '')),
            row.get('importance', ''),
            row.get('classification', ''),
            row.get('start_time', ''),
            row.get('duration', ''),
            row.get('throughput', ''),
            row.get('max_impact', '')
        ]
        for _, row in df.head(max_alertas).iterrows()
    ]

    # estilos para la tabla
    table = Table(tabla_data, colWidths=[60, 70, 80, 60, 60, 90, 60])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ]))
    story.append(table)
    story.append(Spacer(1, 24))

    #Alertas de alta prioridad
    alertas_high = df[df['importance'] == 'High']
    if not alertas_high.empty:
        story.append(Paragraph("Alertas de Alta Prioridad", styles['Heading2']))
        for _, row in alertas_high.iterrows():
            story.append(Paragraph(f"<b>ID:</b> {row.get('id', '')}", styles['Normal']))
            story.append(Paragraph(f"<b>Descripción:</b> {row.get('description', '')}", styles['Normal']))
            story.append(Spacer(1, 6))
    else:
        story.append(Paragraph("No se encontraron alertas críticas (High).", styles['Normal']))
    
    doc.build(story)

    os.remove(image_path)

    return pdf_filename

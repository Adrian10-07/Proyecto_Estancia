import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import uuid
from datetime import datetime
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
)
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def formatear_bps_con_unidad(valor: float) -> str:
    if valor >= 1_000_000:
        return f"{valor / 1_000_000:.2f} Mbps"
    elif valor >= 1_000:
        return f"{valor / 1_000:.2f} Kbps"
    else:
        return f"{valor:.2f} bps"

def generar_pdf_aplicaciones(aplicaciones: list[dict], output_dir='temp') -> str:
    if not aplicaciones:
        raise ValueError("No se proporcionaron aplicaciones para generar el reporte.")

    df = pd.DataFrame(aplicaciones)

    # Convertir los valores 'total' a Mbps como flotantes para graficar
    # Convertir bps a Mbps directamente (los datos ya vienen como float)
    df['total_mbps'] = df['total'] / 1_000_000

    # Gráfico de tráfico total por aplicación
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df.sort_values('total_mbps', ascending=False).head(10),
                x='total_mbps', y='application', palette='Blues_d')
    plt.title('Top 10 Aplicaciones por Tráfico Total (Mbps)')
    plt.xlabel('Tráfico Total (Mbps)')
    plt.ylabel('Aplicación')
    plt.tight_layout()

    os.makedirs(output_dir, exist_ok=True)
    image_path = os.path.join(output_dir, f"grafico_apps_{uuid.uuid4().hex}.png")
    plt.savefig(image_path)
    plt.close()

    # Generar el PDF
    pdf_filename = os.path.join(output_dir, f"reporte_aplicaciones_{uuid.uuid4().hex}.pdf")
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("Reporte de Aplicaciones Detectadas", styles['Title']))
    story.append(Paragraph(f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    story.append(Spacer(1, 12))

    story.append(Paragraph(f"Total de aplicaciones detectadas: <b>{len(aplicaciones)}</b>", styles['Normal']))
    story.append(Spacer(1, 12))

    # Gráfico
    story.append(Paragraph("Gráfico de Tráfico Total por Aplicación", styles['Heading2']))
    story.append(Image(image_path, width=400, height=250))
    story.append(Spacer(1, 24))

    # Tabla de aplicaciones
    story.append(Paragraph("Resumen de Aplicaciones:", styles['Heading2']))
    tabla_data = [['Aplicación', 'Tráfico Entrada', 'Tráfico Salida', 'Tráfico Total']] + [
        [
            app['application'],
            formatear_bps_con_unidad(app['in']),
            formatear_bps_con_unidad(app['out']),
            formatear_bps_con_unidad(app['total']),
        ]
        for app in df.head(10).to_dict(orient='records')
    ]

    table = Table(tabla_data, colWidths=[160, 90, 90, 90])
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


    story.append(Paragraph("Aplicaciones con alto tráfico (más de 100 Mbps):", styles['Heading2']))
    apps_altas = df[df['total_mbps'] > 100]
    if not apps_altas.empty:
        for _, row in apps_altas.iterrows():
            story.append(Paragraph(
                f"<b>{row['application']}</b>: {formatear_bps_con_unidad(row['total'])} (≈ {row['total_mbps']:.2f} Mbps)",
                styles['Normal']
            ))
            story.append(Spacer(1, 6))
    else:
        story.append(Paragraph("No se encontraron aplicaciones con tráfico total mayor a 100 Mbps.", styles['Normal']))

    doc.build(story)
    os.remove(image_path)

    return pdf_filename

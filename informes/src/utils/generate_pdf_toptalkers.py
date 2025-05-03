from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
)
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime
import os
import uuid
import matplotlib.pyplot as plt
import pandas as pd

def generar_pdf_toptalkers(talkers: list[dict], output_dir='temp') -> str:
    if not talkers:
        raise ValueError("No se proporcionaron datos de top talkers.")

    os.makedirs(output_dir, exist_ok=True)
    pdf_filename = os.path.join(output_dir, f"reporte_toptalkers_{uuid.uuid4().hex}.pdf")
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    imagenes_para_borrar = []

    story.append(Paragraph("Reporte de Top Talkers de Red", styles['Title']))
    story.append(Paragraph(f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Este informe muestra las direcciones IP que generan mayor tráfico de red, conocidas como 'Top Talkers'.", styles['Normal']))
    story.append(Paragraph("Se incluyen métricas de tráfico entrante, saliente y total, expresadas en Mbps.", styles['Normal']))
    story.append(Spacer(1, 12))

    story.append(Paragraph(f"Total de IPs detectadas: <b>{len(talkers)}</b>", styles['Normal']))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Tabla de IPs con más tráfico (top 15):", styles['Heading2']))
    tabla_data = [['IP', 'Incoming', 'Outgoing', 'Total']] + [
        [t['ip'], t['incoming'], t['outgoing'], t['total']] for t in talkers[:15]
    ]

    table = Table(tabla_data, colWidths=[120, 90, 90, 90])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ]))
    story.append(table)
    story.append(Spacer(1, 12))

    df = pd.DataFrame(talkers)
    df['total_mbps'] = df['total'].apply(convertir_a_mbps)

    df_top10 = df.sort_values('total_mbps', ascending=False).head(10)
    plt.figure(figsize=(8, 4))
    plt.barh(df_top10['ip'], df_top10['total_mbps'], color='skyblue')
    plt.xlabel("Total (Mbps)")
    plt.title("Top 10 IPs por tráfico total")
    plt.tight_layout()
    grafico_top10 = os.path.join(output_dir, f"grafico_top10_{uuid.uuid4().hex}.png")
    plt.savefig(grafico_top10)
    plt.close()
    story.append(Paragraph("Top 10 IPs con más tráfico total:", styles['Heading2']))
    story.append(Image(grafico_top10, width=450, height=250))
    story.append(Spacer(1, 12))
    imagenes_para_borrar.append(grafico_top10)

    if len(df) <= 50:
        plt.figure(figsize=(10, 5))
        plt.bar(df['ip'], df['total_mbps'], color='salmon')
        plt.xticks(rotation=90)
        plt.ylabel("Total (Mbps)")
        plt.title("Tráfico total por IP (todas las detectadas)")
        plt.tight_layout()
        grafico_all = os.path.join(output_dir, f"grafico_all_{uuid.uuid4().hex}.png")
        plt.savefig(grafico_all)
        plt.close()
        story.append(Paragraph("Tráfico total por cada IP detectada:", styles['Heading2']))
        story.append(Image(grafico_all, width=500, height=300))
        imagenes_para_borrar.append(grafico_all)

    doc.build(story)

    for img in imagenes_para_borrar:
        if os.path.exists(img):
            os.remove(img)

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

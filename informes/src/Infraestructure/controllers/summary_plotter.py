import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import re

def convertir_a_mbps(valor):
    unidades = {"Kbps": 0.001, "Mbps": 1, "Gbps": 1000}
    match = re.match(r"([\d\.]+)\s*([KMG]?bps)", valor)
    if match:
        numero = float(match.group(1))
        unidad = match.group(2)
        factor = unidades.get(unidad, 1)
        return numero * factor
    return 0

def plot_summary(summary: dict):
    datos = []
    for seccion, metricas in summary.items():
        for tipo, valor in metricas.items():
            datos.append({
                "Sección": seccion.capitalize(),
                "Tipo": tipo.capitalize(),
                "Valor (Mbps)": convertir_a_mbps(valor)
            })

    df = pd.DataFrame(datos)

    plt.figure(figsize=(12, 6))
    sns.barplot(data=df, x="Sección", y="Valor (Mbps)", hue="Tipo")
    plt.title("Resumen de Tráfico por Sección")
    plt.ylabel("Mbps")
    plt.xlabel("Sección")
    plt.legend(title="Métrica")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

import csv
from datetime import datetime
import os

def save_report(metadata_list, output_dir="foca_results", basename="reporte_foca"):
    if not metadata_list:
        print("⚠️ No hay metadatos que reportar.")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = os.path.join(output_dir, f"{basename}_{timestamp}")

    # HTML
    html_path = f"{base}.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write("<html><head><meta charset='utf-8'><title>FOCA Report</title></head><body>")
        f.write("<h2>Reporte FOCA-LITE</h2><table border='1' cellpadding='5'><tr><th>Archivo</th><th>Clave</th><th>Valor</th></tr>")
        for entry in metadata_list:
            file = entry["file"]
            for k, v in entry["metadata"].items():
                f.write(f"<tr><td>{file}</td><td>{k}</td><td>{v}</td></tr>")
        f.write("</table></body></html>")
    print(f"📄 Reporte HTML guardado en: {html_path}")

    # CSV
    csv_path = f"{base}.csv"
    with open(csv_path, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Archivo", "Clave", "Valor"])
        for entry in metadata_list:
            file = entry["file"]
            for k, v in entry["metadata"].items():
                writer.writerow([file, k, v])
    print(f"📄 Reporte CSV guardado en: {csv_path}")
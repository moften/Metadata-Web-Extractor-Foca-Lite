import os
import requests
from urllib.parse import urlparse

def download_files(urls, output_dir):
    for i, url in enumerate(urls, 1):
        try:
            print(f"⬇️ [{i}/{len(urls)}] Descargando: {url}")
            response = requests.get(url, timeout=10)

            if response.status_code != 200 or not response.content:
                print("   ⚠️ No se pudo descargar (vacío o error HTTP).")
                continue

            # Obtener nombre del archivo de la URL
            filename = os.path.basename(urlparse(url).path)
            if not filename:
                filename = f"archivo_{i}.bin"

            # Ruta completa
            filepath = os.path.join(output_dir, filename)

            with open(filepath, "wb") as f:
                f.write(response.content)

            print(f"   ✅ Guardado como: {filename}")

        except Exception as e:
            print(f"   ❌ Error descargando {url}: {e}")
import argparse
import os
import tempfile
from crawler import search_documents
from downloader import download_files
from scanner import scan_metadata
from utils import print_banner

def main():
    print_banner("FOCA-LITE by m10sec")

    parser = argparse.ArgumentParser(description="Fingerprinting Organizations with Collected Archives - Lite version")
    parser.add_argument("--domain", required=True, help="Dominio a auditar, por ejemplo: chequemotiva.com")
    parser.add_argument("--filetypes", default="pdf,docx,xlsx", help="Tipos de archivos (separados por coma)")
    parser.add_argument("--output", default="foca_results", help="Nombre de carpeta de salida para los archivos")
    parser.add_argument("--max", type=int, default=20, help="Número máximo de archivos a descargar")

    args = parser.parse_args()
    filetypes = args.filetypes.split(",")
    
    print(f"\n🔍 Buscando documentos públicos de {args.domain}...\n")
    urls = search_documents(args.domain, filetypes, max_results=args.max)

    if not urls:
        print("❌ No se encontraron documentos.")
        return

    os.makedirs(args.output, exist_ok=True)

    print(f"\n⬇️ Descargando {len(urls)} archivos...")
    download_files(urls, args.output)

    print(f"\n🧪 Escaneando metadatos en carpeta: {args.output}\n")
    scan_metadata(args.output)

if __name__ == "__main__":
    main()
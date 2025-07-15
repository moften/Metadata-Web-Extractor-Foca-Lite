import os
from utils import get_supported_files, extract_metadata, print_file_info, show_metadata_details

def scan_metadata(path, return_data=False):
    metadata_list = []

    files = get_supported_files(path)
    if not files:
        print("⚠️ No se encontraron archivos compatibles.")
        return [] if return_data else None

    print(f"\n🧾 Archivos encontrados: {len(files)}")
    for file in files:
        print_file_info(file)

    for file in files:
        print(f"\n📂 Metadatos de: {file}")
        metadata = extract_metadata(file)
        show_metadata_details(metadata)

        if return_data:
            metadata_list.append({
                "file": os.path.basename(file),
                "metadata": metadata
            })

    if return_data:
        return metadata_list
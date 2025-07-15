import os
import mimetypes
import zipfile
import PyPDF2
import docx
import openpyxl
import exiftool

def print_banner(name="Metadata Scanner"):
    print(f"""
███████╗ ██████╗  ██████╗ █████╗     ██╗     ██╗████████╗███████╗
██╔════╝██╔═══██╗██╔════╝██╔══██╗    ██║     ██║╚══██╔══╝██╔════╝
█████╗  ██║   ██║██║     ███████║    ██║     ██║   ██║   █████╗  
██╔══╝  ██║   ██║██║     ██╔══██║    ██║     ██║   ██║   ██╔══╝  
██      ╚██████╔╝╚██████╗██║  ██║    ███████╗██║   ██║   ███████╗
╚╝       ╚═════╝  ╚═════╝╚═╝  ╚═╝    ╚══════╝╚═╝   ╚═╝   ╚══════╝
    {name} - m10sec | m10sec@proton.me | by hackers for hackers
    """)

def get_supported_files(path):
    supported_exts = ('.pdf', '.docx', '.xlsx', '.png', '.jpg', '.jpeg', '.txt', '.csv', '.zip')
    file_list = []

    if os.path.isfile(path):
        if path.lower().endswith(supported_exts):
            file_list.append(path)
    elif os.path.isdir(path):
        for root, _, files in os.walk(path):
            for name in files:
                full_path = os.path.join(root, name)
                if name.lower().endswith(supported_exts):
                    file_list.append(full_path)

    return file_list

def print_file_info(path):
    size = os.path.getsize(path) / 1024
    mime_type, _ = mimetypes.guess_type(path)
    print(f"📄 {os.path.basename(path)} - {size:.2f} KB - Tipo: {mime_type}")

def extract_metadata(path):
    ext = path.lower().split('.')[-1]
    metadata = {}

    try:
        if ext == 'pdf':
            with open(path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                metadata = reader.metadata or {}

        elif ext == 'docx':
            doc = docx.Document(path)
            cp = doc.core_properties
            metadata = {
                "author": cp.author,
                "title": cp.title,
                "comments": cp.comments,
                "created": cp.created,
                "modified": cp.modified,
                "last_modified_by": cp.last_modified_by,
                "revision": cp.revision
            }

        elif ext == 'xlsx':
            wb = openpyxl.load_workbook(path)
            props = wb.properties
            metadata = {
                "author": props.creator,
                "title": props.title,
                "created": props.created,
                "modified": props.modified,
                "last_modified_by": props.lastModifiedBy,
                "keywords": props.keywords
            }

        elif ext in ['jpg', 'jpeg', 'png']:
            with exiftool.ExifTool() as et:
                meta = et.get_metadata(path)
                metadata = meta or {}

        elif ext == 'txt' or ext == 'csv':
            metadata["line_count"] = sum(1 for _ in open(path, 'r', errors='ignore'))

        elif ext == 'zip':
            with zipfile.ZipFile(path, 'r') as zip_ref:
                metadata["num_files"] = len(zip_ref.infolist())
                metadata["file_names"] = [info.filename for info in zip_ref.infolist()]

        else:
            metadata["info"] = "Formato no soportado."

    except Exception as e:
        metadata["error"] = str(e)

    return metadata

def show_metadata_details(metadata: dict):
    if not metadata:
        print("  ❌ Sin metadatos encontrados.")
        return

    for key, value in metadata.items():
        key_str = f"  • {key}:"
        val_str = f"{value}" if value else "None"
        print(f"{key_str:<30} {val_str}")
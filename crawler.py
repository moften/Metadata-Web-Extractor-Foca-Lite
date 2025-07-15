from googlesearch import search

def search_documents(domain: str, filetypes: list, max_results: int = 20) -> list:
    urls = []
    
    # 1. Dorks por tipo de archivo
    for ext in filetypes:
        dork = f"site:{domain} filetype:{ext}"
        print(f"🔎 Dork: {dork}")
        try:
            results = list(search(dork, num_results=max_results))
            urls.extend(results)
        except Exception as e:
            print(f"⚠️ Error en dork '{dork}': {e}")
    
    # 2. Dorks para directorios expuestos
    index_dorks = [
        f'site:{domain} intitle:"index of" "parent directory"',
        f'site:{domain} intitle:"index of /" "Last modified"',
        f'"index of /" site:{domain}'
    ]

    print("\n🔍 Buscando directorios expuestos...\n")
    for dork in index_dorks:
        print(f"🗂 Dork: {dork}")
        try:
            results = list(search(dork, num_results=10))
            urls.extend(results)
        except Exception as e:
            print(f"⚠️ Error en dork de índice: {e}")

    return list(set(urls))  # eliminamos duplicados
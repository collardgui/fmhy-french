import re
import urllib.request

# Liste des URLs sources possibles (FMHY change parfois de dépôt principal)
URLS = [
    "https://raw.githubusercontent.com/fmhy/FMHYedit/main/docs/non-english.md",
    "https://raw.githubusercontent.com/fmhy/FMHY/main/docs/non-english.md",
    "https://raw.githubusercontent.com/nbq/FMHYedit/main/docs/non-english.md"
]

def download_content():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    for url in URLS:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as response:
                content = response.read().decode('utf-8')
                if content and len(content) > 1000:
                    print(f"Téléchargement réussi depuis : {url}")
                    return content
        except Exception as e:
            print(f"Échec pour {url} : {e}")
    return None

def fetch_and_extract():
    content = download_content()
    
    french_content = None
    if content:
        # Recherche souple : cherche un titre contenant 'French' ou 'Français'
        pattern = r"(##\s*.*(?:French|Français).*?)(?=\n##\s|\Z)"
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            french_content = match.group(1).strip()

    if not french_content:
        french_content = "## French / Français\n\nImpossible de charger la section pour le moment. Nouvelle tentative programmée."

    final_markdown = "# 🇫🇷 Ressources Françaises (FMHY)\n\n"
    final_markdown += "> *Mise à jour automatique quotidienne depuis la source officielle FMHY.*\n\n"
    final_markdown += french_content

    with open("index.md", "w", encoding="utf-8") as f:
        f.write(final_markdown)
    print("Fichier index.md mis à jour avec succès !")

if __name__ == "__main__":
    fetch_and_extract()
    

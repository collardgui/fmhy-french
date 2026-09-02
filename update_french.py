import re
import urllib.request

# URL du fichier brut markdown
URL = "https://raw.githubusercontent.com/fmhy/FMHYedit/main/docs/non-english.md"

def fetch_and_extract():
    req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')
    except Exception as e:
        print(f"Erreur de téléchargement : {e}")
        content = ""

    # Expression régulière flexible pour trouver la section French
    pattern = r"(## French / Français.*?)(\n## |\Z)"
    match = re.search(pattern, content, re.DOTALL)

    if match:
        french_content = match.group(1)
    else:
        french_content = "## French / Français\n\nImpossible de charger la section pour le moment."

    final_markdown = "# 🇫🇷 Ressources Françaises (FMHY)\n\n"
    final_markdown += "> *Mise à jour automatique depuis FMHY.*\n\n"
    final_markdown += french_content

    # Écriture forcée du fichier index.md
    with open("index.md", "w", encoding="utf-8") as f:
        f.write(final_markdown)
    print("Fichier index.md généré avec succès !")

if __name__ == "__main__":
    fetch_and_extract()
    

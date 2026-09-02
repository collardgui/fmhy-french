import re
import urllib.request

# URL du fichier brut markdown officiel chez FMHY
URL = "https://raw.githubusercontent.com/fmhy/FMHYedit/main/docs/non-english.md"

def fetch_and_extract():
    # Déguisement du script en navigateur classique pour éviter d'être bloqué
    req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')
    except Exception as e:
        print(f"Erreur de téléchargement : {e}")
        return

    # Expressions régulières pour isoler uniquement la partie "French / Français"
    # Capture tout entre '## French / Français' et le prochain header '## ' ou la fin du fichier
    pattern = r"(## French / Français.*?)(\n## |\Z)"
    match = re.search(pattern, content, re.DOTALL)

    if match:
        french_content = match.group(1)
        
        # En-tête injecté en haut de votre page web
        final_markdown = "# 🇫🇷 Ressources Françaises (FMHY)\n\n"
        final_markdown += "> *Cette page est mise à jour automatiquement chaque jour depuis la source officielle FMHY.*\n\n"
        final_markdown += french_content

        # Écriture dans le fichier index.md qui servira de site internet
        with open("index.md", "w", encoding="utf-8") as f:
            f.write(final_markdown)
        print("Extraction réussie et index.md mis à jour !")
    else:
        print("Erreur : Impossible de localiser la section French / Français.")

if __name__ == "__main__":
    fetch_and_extract()
  

import re
import urllib.request

URL = "https://raw.githubusercontent.com/fmhy/FMHYedit/main/docs/non-english.md"

def fetch_and_extract():
    try:
        req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            text = response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Erreur de téléchargement : {e}")
        text = ""

    french_section = ""
    if text:
        # Regex qui capture depuis "French / Français" jusqu'au prochain pays "German / Deutsch" ou "Greek"
        # de manière à inclure tous les sous-titres (Downloading, Streaming, Torrenting, Reading...)
        pattern = r"(##\s*French\s*/\s*Français.*?)(\n##\s*[A-Z][a-z]+(?:\s*/|\s*$)|\Z)"
        match = re.search(pattern, text, re.DOTALL)
        
        if match:
            french_section = match.group(1).strip()
        else:
            # Plan B de secours par découpage
            start_pos = text.find("French / Français")
            if start_pos != -1:
                # On cherche le début de la section suivante (German)
                end_pos = text.find("\n## German", start_pos)
                if end_pos == -1:
                    end_pos = text.find("\n## Greek", start_pos)
                
                if end_pos != -1:
                    french_section = "## " + text[start_pos:end_pos].strip()
                else:
                    french_section = "## " + text[start_pos:].strip()

    if not french_section:
        french_section = "## French / Français\n\nImpossible de charger la section pour le moment."

    final_markdown = "# 🇫🇷 Ressources Françaises (FMHY)\n\n"
    final_markdown += "> *Mise à jour automatique quotidienne depuis la source officielle FMHY.*\n\n"
    final_markdown += french_section

    with open("index.md", "w", encoding="utf-8") as f:
        f.write(final_markdown)

if __name__ == "__main__":
    fetch_and_extract()

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
        # Repérage du début exact de la section française
        start_marker = "French / Français"
        start_pos = text.find(start_marker)

        if start_pos != -1:
            # Repérage de la fin (début du pays suivant : German / Deutsch)
            end_marker = "German / Deutsch"
            end_pos = text.find(end_marker, start_pos)

            if end_pos != -1:
                # On remonte un peu avant "German / Deutsch" pour couper proprement le titre
                content = text[start_pos:end_pos].rsplit("\n#", 1)[0].strip()
            else:
                content = text[start_pos:].strip()

            french_section = "## " + content

    if not french_section:
        french_section = "## French / Français\n\nImpossible de charger la section pour le moment."

    final_markdown = "# 🇫🇷 Ressources Françaises (FMHY)\n\n"
    final_markdown += "> *Mise à jour automatique quotidienne depuis la source officielle FMHY.*\n\n"
    final_markdown += french_section

    with open("index.md", "w", encoding="utf-8") as f:
        f.write(final_markdown)

if __name__ == "__main__":
    fetch_and_extract()
    

import urllib.request

# URLs des fichiers sources bruts sur GitHub
URL_NON_ENGLISH = "https://raw.githubusercontent.com/fmhy/FMHYedit/main/docs/non-english.md"
URL_STREAMING = "https://raw.githubusercontent.com/fmhy/FMHYedit/main/docs/streaming.md"

def download_text(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Erreur de téléchargement depuis {url} : {e}")
        return ""

def extract_french_section():
    text = download_text(URL_NON_ENGLISH)
    if not text:
        return "## French / Français\n\nImpossible de charger la section pour le moment."

    start_marker = "French / Français"
    start_pos = text.find(start_marker)

    if start_pos != -1:
        end_marker = "German / Deutsch"
        end_pos = text.find(end_marker, start_pos)

        if end_pos != -1:
            content = text[start_pos:end_pos].rsplit("\n#", 1)[0].strip()
        else:
            content = text[start_pos:].strip()

        return "## " + content
    return "## French / Français\n\nSection non trouvée."

def extract_sports_section():
    text = download_text(URL_STREAMING)
    if not text:
        return "## Live TV / Sports\n\nImpossible de charger la section pour le moment."

    # Repérage du début de la section Live TV / Sports
    start_marker = "Live TV / Sports"
    start_pos = text.find(start_marker)

    if start_pos != -1:
        # Repérage de la section suivante dans le fichier streaming (Anime)
        end_marker = "Anime"
        end_pos = text.find(end_marker, start_pos)

        if end_pos != -1:
            content = text[start_pos:end_pos].rsplit("\n#", 1)[0].strip()
        else:
            content = text[start_pos:].strip()

        return "## " + content
    return "## Live TV / Sports\n\nSection non trouvée."

def main():
    french_content = extract_french_section()
    sports_content = extract_sports_section()

    # Assemblage de la page globale
    final_markdown = "# 🇫🇷 Ressources Françaises & 📺 Live TV / Sports (FMHY)\n\n"
    final_markdown += "> *Mise à jour automatique quotidienne depuis les sources officielles FMHY.*\n\n"
    final_markdown += "---\n\n"
    final_markdown += french_content + "\n\n"
    final_markdown += "---\n\n"
    final_markdown += sports_content

    # Écriture dans index.md
    with open("index.md", "w", encoding="utf-8") as f:
        f.write(final_markdown)

    print("Mise à jour réussie de index.md avec French + Live TV / Sports !")

if __name__ == "__main__":
    main()
    

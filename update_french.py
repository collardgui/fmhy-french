import urllib.request
import re

# Sources exactes
URL_NON_ENGLISH = "https://raw.githubusercontent.com/fmhy/FMHYedit/main/docs/non-english.md"
# Page brute du Wiki GitHub "Streaming" de FMHY
URL_WIKI_STREAMING = "https://raw.githubusercontent.com/wiki/fmhy/FMHY/Streaming.md"

def download_text(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Erreur de téléchargement pour {url}: {e}")
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
    text = download_text(URL_WIKI_STREAMING)
    if not text:
        return "## Live TV / Sports\n\nImpossible de charger la page Streaming.md du Wiki."

    # Cherche la section "Live TV / Sports" ou "Live TV" ou "Sports"
    start_pos = -1
    for marker in ["Live TV / Sports", "Live TV", "Sports"]:
        pos = text.find(marker)
        if pos != -1:
            start_pos = pos
            break

    if start_pos != -1:
        # Cherche le début de la section suivante (titre de niveau 1 ou 2)
        end_pos = text.find("\n# ", start_pos)
        if end_pos == -1:
            end_pos = text.find("\n## ", start_pos + 20)

        if end_pos != -1:
            content = text[start_pos:end_pos].strip()
        else:
            content = text[start_pos:].strip()

        return "## " + content

    # Si la section exacte n'est pas découpable, renvoie la page wiki
    return "## Live TV / Sports\n\n" + text.strip()

def main():
    french_content = extract_french_section()
    sports_content = extract_sports_section()

    final_markdown = "# 🇫🇷 Ressources Françaises & 📺 Live TV / Sports (FMHY)\n\n"
    final_markdown += "> *Mise à jour automatique quotidienne depuis les sources officielles FMHY.*\n\n"
    final_markdown += french_content + "\n\n"
    final_markdown += "---\n\n"
    final_markdown += sports_content

    with open("index.md", "w", encoding="utf-8") as f:
        f.write(final_markdown)

    print("Mise à jour de index.md réussie !")

if __name__ == "__main__":
    main()
    

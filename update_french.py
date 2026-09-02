import urllib.request
import re

URL_NON_ENGLISH = "https://raw.githubusercontent.com/fmhy/FMHYedit/main/docs/non-english.md"
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
        return "## Live TV & Live Sports\n\nImpossible de charger la section."

    # 1. Repérage du début de Live TV
    start_pos = -1
    for marker in ["▷ Live TV", "Live TV", "## Live TV"]:
        pos = text.find(marker)
        if pos != -1:
            start_pos = pos
            break

    if start_pos == -1:
        return "## Live TV / Sports\n\nSection non trouvée dans la source."

    # 2. On cherche la fin de la partie 'Live Sports'
    # On s'arrête dès qu'on croise des sous-sections qu'on ne veut pas (Replays, IPTV, Movies, Anime, etc.)
    end_pos = -1
    cut_markers = [
        "Sports Replays", 
        "▷ Sports Replays", 
        "IPTV", 
        "▷ IPTV", 
        "## Movies", 
        "▷ Movies", 
        "## Anime", 
        "▷ Anime", 
        "↪️ Sports Calendars"
    ]

    for marker in cut_markers:
        pos = text.find(marker, start_pos)
        if pos != -1 and (end_pos == -1 or pos < end_pos):
            end_pos = pos

    if end_pos != -1:
        content = text[start_pos:end_pos].strip()
    else:
        # Si aucun marqueur de fin n'est trouvé, on prend 4000 caractères max
        content = text[start_pos:start_pos+4000].strip()

    # Si le texte commence par ▷, on le remplace par un titre propre ##
    if content.startswith("▷"):
        content = "## " + content[1:].strip()
    elif not content.startswith("#"):
        content = "## " + content

    return content

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
    

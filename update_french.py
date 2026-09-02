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
        return "## Live TV / Sports\n\nImpossible de charger la section."

    output_sections = []

    # 1. Extraction de la sous-section Live TV
    live_tv_match = re.search(r"(?:▷|##|\##\#)\s*Live TV\b.*?(?=\n(?:▷|##|\##\#)|\Z)", text, re.DOTALL | re.IGNORECASE)
    if live_tv_match:
        tv_content = live_tv_match.group(0).strip()
        # Retrait des lignes IPTV s'il y en a à la fin de la liste TV
        tv_lines = [line for line in tv_content.split("\n") if "iptv" not in line.lower()]
        output_sections.append("\n".join(tv_lines))

    # 2. Extraction de la sous-section Live Sports
    live_sports_match = re.search(r"(?:▷|##|\##\#)\s*Live Sports\b.*?(?=\n(?:▷|##|\##\#|\*\*Sports Replays\*\*|\*\*IPTV\*\*|\*\*Replays\*\*|\*\*Calendars\*\*)|$)", text, re.DOTALL | re.IGNORECASE)
    if live_sports_match:
        sports_content = live_sports_match.group(0).strip()
        # Retrait des lignes Replays ou IPTV
        sports_lines = [line for line in sports_content.split("\n") if "replay" not in line.lower() and "iptv" not in line.lower()]
        output_sections.append("\n".join(sports_lines))

    if output_sections:
        result = "\n\n---\n\n".join(output_sections)
        # Normalisation des titres sous forme de ##
        result = re.sub(r'^(?:▷|###)\s*', '## ', result, flags=re.MULTILINE)
        return result

    return "## Live TV / Sports\n\nSection non trouvée dans la source."

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
    

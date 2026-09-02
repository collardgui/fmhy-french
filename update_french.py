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

    # Début exact de la section Live TV / Sports
    start_pos = text.find("Live TV / Sports")
    if start_pos == -1:
        start_pos = text.find("Live TV")

    if start_pos != -1:
        # Fin de la section globale (avant Movies, Anime, etc.)
        end_pos = -1
        for next_marker in ["\n## Movies", "\n## Anime", "\n## Asian", "\n# Movies", "\n# Anime"]:
            pos = text.find(next_marker, start_pos)
            if pos != -1 and (end_pos == -1 or pos < end_pos):
                end_pos = pos

        if end_pos != -1:
            content = text[start_pos:end_pos].strip()
        else:
            content = text[start_pos:].strip()

        # Nettoyage : suppression des sous-sections IPTV et Replays
        # On coupe dès qu'on rencontre IPTV ou Sports Replays
        cut_markers = [
            "IPTV", 
            "Sports Replays", 
            "Replays", 
            "### IPTV", 
            "### Sports Replays", 
            "## IPTV"
        ]
        
        cleaned_lines = []
        for line in content.split("\n"):
            # Si la ligne contient un des marqueurs d'exclusion en titre/sous-titre
            if any(line.strip().startswith(m) or line.strip() == f"### {m}" or line.strip() == f"## {m}" for m in cut_markers):
                break
            cleaned_lines.append(line)

        content = "\n".join(cleaned_lines).strip()
        return "## " + content

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
    

import urllib.request
import re

URL_NON_ENGLISH = "https://raw.githubusercontent.com/fmhy/FMHYedit/main/docs/non-english.md"

# FMHY utilise 'videostreams.md' ou 'tv.md' pour cette section
URLS_STREAMING = [
    "https://raw.githubusercontent.com/fmhy/FMHYedit/main/docs/videostreams.md",
    "https://raw.githubusercontent.com/fmhy/FMHYedit/main/docs/tv.md",
    "https://raw.githubusercontent.com/fmhy/FMHYedit/main/docs/sports.md"
]

def download_text(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Échec sur {url} : {e}")
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
    text = ""
    # Test des différentes URLs possibles
    for url in URLS_STREAMING:
        downloaded = download_text(url)
        if downloaded:
            text = downloaded
            break

    if not text:
        return "## Live TV / Sports\n\nImpossible de charger le fichier source streaming/videostreams."

    # Recherche de 'Live TV' ou 'Sports' dans le fichier videostreams
    start_pos = -1
    for term in ["Live TV", "Sports", "Live Sports"]:
        pos = text.find(term)
        if pos != -1 and (start_pos == -1 or pos < start_pos):
            start_pos = pos

    if start_pos != -1:
        # On essaie d'extraire depuis ce point jusqu'à la section suivante ou la fin
        end_pos = -1
        for next_term in ["\n## Anime", "\n## Asian", "\n## Cartoons", "\n## Movies", "\n## Android"]:
            pos = text.find(next_term, start_pos)
            if pos != -1 and (end_pos == -1 or pos < end_pos):
                end_pos = pos

        if end_pos != -1:
            content = text[start_pos:end_pos].strip()
        else:
            content = text[start_pos:].strip()

        return "## " + content

    # Si pas de découpe spécifique trouvée, on retourne le contenu du fichier
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

    print("Mise à jour réussie de index.md avec French + Live TV / Sports !")

if __name__ == "__main__":
    main()
    

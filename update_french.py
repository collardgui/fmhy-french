import urllib.request
import re

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
        return "## Live TV / Sports\n\nImpossible de charger le fichier streaming.md."

    # Recherche souple pour Live TV / Sports ou Live TV ou Sports
    # Cherche un titre '## Live TV' ou '## Sports' ou '## Live TV / Sports'
    pattern = r"(##\s*.*?(?:Live TV|Sports).*?)(?=\n##\s|\Z)"
    matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)

    if matches:
        # On regroupe toutes les sections correspondantes (Live TV + Sports)
        combined_sports = "\n\n".join([m.strip() for m in matches])
        return combined_sports

    # Plan B : extrait depuis 'Live TV' jusqu'à 'Anime' ou 'Podcasts' ou 'Asian'
    start_pos = -1
    for term in ["Live TV", "Sports"]:
        pos = text.lower().find(term.lower())
        if pos != -1 and (start_pos == -1 or pos < start_pos):
            start_pos = pos

    if start_pos != -1:
        # On cherche la fin de la section
        end_pos = -1
        for next_term in ["\n## Anime", "\n## Asian", "\n## Cartoons", "\n## Movies"]:
            pos = text.find(next_term, start_pos)
            if pos != -1 and (end_pos == -1 or pos < end_pos):
                end_pos = pos

        if end_pos != -1:
            content = text[start_pos:end_pos].strip()
        else:
            content = text[start_pos:start_pos+5000].strip()

        return "## " + content

    return "## Live TV / Sports\n\nSection non trouvée dans le fichier source."

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
    

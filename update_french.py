import re
import urllib.request

URLS = [
    "https://raw.githubusercontent.com/fmhy/FMHYedit/main/docs/non-english.md",
    "https://raw.githubusercontent.com/fmhy/FMHY/main/docs/non-english.md",
    "https://raw.githubusercontent.com/nbq/FMHYedit/main/docs/non-english.md"
]

def download_content():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    for url in URLS:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                return response.read().decode('utf-8', errors='ignore')
        except Exception as e:
            print(f"Échec sur {url} : {e}")
    return ""

def fetch_and_extract():
    content = download_content()
    
    # Regex pour isoler la section French / Français
    pattern = r"(##\s*.*?(?:French|Français).*?)(?=\n##\s|\Z)"
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE) if content else None

    if match:
        french_content = match.group(1).strip()
    else:
        french_content = "## French / Français\n\nImpossible de charger la section pour le moment."

    final_markdown = "# 🇫🇷 Ressources Françaises (FMHY)\n\n"
    final_markdown += "> *Mise à jour automatique quotidienne depuis la source officielle FMHY.*\n\n"
    final_markdown += french_content

    with open("index.md", "w", encoding="utf-8") as f:
        f.write(final_markdown)

if __name__ == "__main__":
    fetch_and_extract()
    

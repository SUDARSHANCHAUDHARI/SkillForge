
import os
from rich.console import Console
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

console = Console()


def compare_cmd(file_a: str, file_b: str):
    for f in [file_a, file_b]:
        if not os.path.isfile(f):
            console.print(f"[red]Error:[/red] File not found: {f}")
            return

    try:
        text_a = open(file_a, encoding="utf-8").read()
        text_b = open(file_b, encoding="utf-8").read()
    except OSError as e:
        console.print(f"[red]Error:[/red] {e}")
        return

    vec = TfidfVectorizer().fit_transform([text_a, text_b])
    sim = float(cosine_similarity(vec[0], vec[1])[0][0])

    color = "red" if sim >= 0.8 else "yellow" if sim >= 0.5 else "green"
    label = "Likely duplicate" if sim >= 0.8 else "Similar" if sim >= 0.5 else "Distinct"

    console.print(f"[bold]{os.path.basename(file_a)}[/bold]  vs  [bold]{os.path.basename(file_b)}[/bold]\n")
    console.print(f"Similarity: [{color}]{sim:.2f}[/{color}]  ({label})")
    console.print(f"Words A:    {len(text_a.split())}")
    console.print(f"Words B:    {len(text_b.split())}")

    words_a = set(text_a.lower().split())
    words_b = set(text_b.lower().split())
    common = words_a & words_b
    if common:
        console.print(f"Common words ({len(common)}): [dim]{', '.join(sorted(common)[:10])}{'...' if len(common) > 10 else ''}[/dim]")

import os
import json
import re

DATA_DIR = "data"
README_PATH = "README.md"


def get_latest_round_file(season_dir):
    """Localiza el archivo JSON correspondiente a la última ronda de una temporada."""
    files = [
        f
        for f in os.listdir(season_dir)
        if f.startswith("round_") and f.endswith(".json")
    ]
    if not files:
        return None
    # Ordena alfabéticamente/numéricamente (ej: round_01.json < round_02.json)
    files.sort()
    return os.path.join(season_dir, files[-1])


def format_percentage(val):
    """Convierte un decimal (0.31) en porcentaje formateado (31%)."""
    try:
        return f"{int(float(val) * 100)}%"
    except (ValueError, TypeError):
        return "0%"


def generate_season_markdown(json_path, is_latest_season=False):
    """Lee un JSON de ronda y construye el bloque Markdown HTML colapsable."""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    meta = data.get("Meta", {})
    season = meta.get("season", "N/A")
    race_id = meta.get("race_id", 0)

    # 1. Top 5 Pilotos de la ronda
    drivers = data.get("Drivers", [])
    top_drivers = sorted(
        drivers,
        key=lambda x: x.get("Round_Fantasy_Points", 0),
        reverse=True,
    )[:5]

    # 2. Top 3 Escuderías de la ronda
    teams = data.get("Teams", [])
    top_teams = sorted(
        teams,
        key=lambda x: x.get("Round_Fantasy_Points", 0),
        reverse=True,
    )[:3]

    # La temporada más reciente se muestra desplegada por defecto (open)
    open_attr = " open" if is_latest_season else ""

    md = [
        f"<details{open_attr}>",
        f"  <summary><b>🏎️ {season} Season — Round {race_id:02d} (Latest Data)</b></summary>",
        "  <br>",
        "  #### 👤 Top 5 Drivers",
        "  | Driver | Team | Round Pts | Value | Selected % |",
        "  | :--- | :--- | :--- | :--- | :--- |",
    ]

    for d in top_drivers:
        name = d.get("Driver_Name", "N/A")
        team = d.get("Team_Name", "N/A")
        pts = d.get("Round_Fantasy_Points", 0)
        val = d.get("Value", 0)
        sel = format_percentage(d.get("Selected_Percentage", 0))
        md.append(f"  | **{name}** | {team} | {pts} pts | ${val}M | {sel} |")

    md.extend(
        [
            "",
            "  #### 🏢 Top 3 Constructors",
            "  | Team | Round Pts | Value | Selected % |",
            "  | :--- | :--- | :--- | :--- |",
        ]
    )

    for t in top_teams:
        name = t.get("Team_Name", "N/A")
        pts = t.get("Round_Fantasy_Points", 0)
        val = t.get("Value", 0)
        sel = format_percentage(t.get("Selected_Percentage", 0))
        md.append(f"  | **{name}** | {pts} pts | ${val}M | {sel} |")

    md.append("</details>\n")
    return "\n".join(md)


def update_readme():
    if not os.path.exists(DATA_DIR):
        print(f"Directory '{DATA_DIR}' not found.")
        return

    # Buscar todas las carpetas dentro de data/ que sean números (años)
    seasons = [
        s
        for s in os.listdir(DATA_DIR)
        if os.path.isdir(os.path.join(DATA_DIR, s)) and s.isdigit()
    ]

    if not seasons:
        print("No season directories found in data/.")
        return

    # Ordenar de más reciente a más antigua (2026, 2025, 2024...)
    seasons.sort(reverse=True)

    summary_blocks = []
    for idx, season in enumerate(seasons):
        season_dir = os.path.join(DATA_DIR, season)
        latest_file = get_latest_round_file(season_dir)

        if latest_file:
            # Solo la primera (año más reciente) tendrá 'open_attr'
            is_latest = idx == 0
            block = generate_season_markdown(
                latest_file, is_latest_season=is_latest
            )
            summary_blocks.append(block)

    full_summary_md = "\n".join(summary_blocks)

    # Inyectar el contenido en README.md
    if not os.path.exists(README_PATH):
        print(f"'{README_PATH}' not found.")
        return

    with open(README_PATH, "r", encoding="utf-8") as f:
        readme_content = f.read()

    pattern = r"(<!-- SEASONS_SUMMARY_START -->)(.*?)(<!-- SEASONS_SUMMARY_END -->)"
    
    if not re.search(pattern, readme_content, flags=re.DOTALL):
        print("Error: Could not find HTML markers in README.md")
        return

    replacement = f"\\1\n{full_summary_md}\n\\3"
    updated_readme = re.sub(pattern, replacement, readme_content, flags=re.DOTALL)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(updated_readme)

    print("README.md updated successfully!")


if __name__ == "__main__":
    update_readme()

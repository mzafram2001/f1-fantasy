import os
import json
import re

DATA_DIR = "data"
README_PATH = "README.md"


def get_latest_round_file(season_dir, is_latest_season=False):
    """
    Localiza el archivo JSON de la ronda a mostrar:
    - Si es la temporada actual y hay más de 1 ronda, coge la penúltima (files[-2]).
    - Para temporadas pasadas (o si solo hay 1 ronda), coge la última (files[-1]).
    """
    files = [
        f
        for f in os.listdir(season_dir)
        if f.startswith("round_") and f.endswith(".json")
    ]
    if not files:
        return None

    files.sort()

    if is_latest_season and len(files) > 1:
        return os.path.join(season_dir, files[-2])

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

    drivers = data.get("Drivers", [])
    top_drivers = sorted(
        drivers,
        key=lambda x: x.get("Round_Fantasy_Points", 0),
        reverse=True,
    )[:5]

    teams = data.get("Teams", [])
    top_teams = sorted(
        teams,
        key=lambda x: x.get("Round_Fantasy_Points", 0),
        reverse=True,
    )[:3]

    open_attr = " open" if is_latest_season else ""

    md = [
        f"<details{open_attr}>",
        f"<summary><b>🏎️ {season} Season — Round {race_id:02d}</b></summary>",
        "",
        "#### 👤 Top 5 Drivers",
        "",
        "| Driver | Team | Round Pts | Total Season Pts | Value | Selected % |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |",
    ]

    for d in top_drivers:
        name = d.get("Driver_Name", "N/A")
        team = d.get("Team_Name", "N/A")
        pts = d.get("Round_Fantasy_Points", 0)
        season_pts = d.get("Season_Fantasy_Points", 0)
        val = d.get("Value", 0)
        sel = format_percentage(d.get("Selected_Percentage", 0))
        md.append(f"| **{name}** | {team} | {pts} pts | {season_pts} pts | ${val}M | {sel} |")

    md.extend(
        [
            "",
            "#### 🏢 Top 3 Constructors",
            "",
            "| Team | Round Pts | Total Season Pts | Value | Selected % |",
            "| :--- | :--- | :--- | :--- | :--- |",
        ]
    )

    for t in top_teams:
        name = t.get("Team_Name", "N/A")
        pts = t.get("Round_Fantasy_Points", 0)
        season_pts = t.get("Season_Fantasy_Points", 0)
        val = t.get("Value", 0)
        sel = format_percentage(t.get("Selected_Percentage", 0))
        md.append(f"| **{name}** | {pts} pts | {season_pts} pts | ${val}M | {sel} |")

    md.extend(["", "</details>", ""])
    return "\n".join(md)


def update_readme():
    if not os.path.exists(DATA_DIR):
        print(f"Directory '{DATA_DIR}' not found.")
        return

    seasons = [
        s
        for s in os.listdir(DATA_DIR)
        if os.path.isdir(os.path.join(DATA_DIR, s)) and s.isdigit()
    ]

    if not seasons:
        print("No season directories found in data/.")
        return

    seasons.sort(reverse=True)

    summary_blocks = []
    for idx, season in enumerate(seasons):
        season_dir = os.path.join(DATA_DIR, season)
        is_latest = (idx == 0)
        
        latest_file = get_latest_round_file(season_dir, is_latest_season=is_latest)

        if latest_file:
            block = generate_season_markdown(
                latest_file, is_latest_season=is_latest
            )
            summary_blocks.append(block)

    full_summary_md = "\n\n".join(summary_blocks)

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

import os
import json
import re
from datetime import datetime

DATA_DIR = "data"
README_PATH = "README.md"


def get_latest_round_file(season_dir, is_latest_season=False):
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
    try:
        return f"{int(float(val) * 100)}%"
    except (ValueError, TypeError):
        return "0%"


def generate_season_markdown(json_path, is_latest_season=False):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    meta = data.get("Meta", {})
    season = meta.get("season", "N/A")
    race_id = meta.get("race_id", 0)

    drivers = data.get("Drivers", [])
    top_drivers = sorted(
        drivers,
        key=lambda x: x.get("Season_Fantasy_Points", 0),
        reverse=True,
    )[:5]

    teams = data.get("Teams", [])
    top_teams = sorted(
        teams,
        key=lambda x: x.get("Season_Fantasy_Points", 0),
        reverse=True,
    )[:3]

    open_attr = " open" if is_latest_season else ""

    md = [
        f"<details{open_attr}>",
        f"<summary><b>🏎️ {season} Season — Round {race_id:02d}</b></summary>",
        "",
        "#### 👤 Top 5 Drivers",
        "",
        "| Driver | Team | Total Season Pts | Value | Selected % |",
        "| :--- | :--- | :--- | :--- | :--- |",
    ]

    for d in top_drivers:
        name = d.get("Driver_Name", "N/A")
        team = d.get("Team_Name", "N/A")
        season_pts = d.get("Season_Fantasy_Points", 0)
        val = d.get("Value", 0)
        sel = format_percentage(d.get("Selected_Percentage", 0))
        md.append(f"| **{name}** | {team} | {season_pts} pts | ${val}M | {sel} |")

    md.extend(
        [
            "",
            "#### 🏢 Top 3 Constructors",
            "",
            "| Team | Total Season Pts | Value | Selected % |",
            "| :--- | :--- | :--- | :--- |",
        ]
    )

    for t in top_teams:
        name = t.get("Team_Name", "N/A")
        season_pts = t.get("Season_Fantasy_Points", 0)
        val = t.get("Value", 0)
        sel = format_percentage(t.get("Selected_Percentage", 0))
        md.append(f"| **{name}** | {season_pts} pts | ${val}M | {sel} |")

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

    # 1. Actualizar las tablas de resumen
    summary_pattern = r"(<!-- SEASONS_SUMMARY_START -->)(.*?)(<!-- SEASONS_SUMMARY_END -->)"
    if re.search(summary_pattern, readme_content, flags=re.DOTALL):
        readme_content = re.sub(summary_pattern, f"\\1\n{full_summary_md}\n\\3", readme_content, flags=re.DOTALL)

    # 2. Actualizar la fecha de última revisión ("Last checked")
    today_str = datetime.now().strftime("%Y-%m-%d")
    checked_pattern = r"(<!-- LAST_CHECKED_START -->)(.*?)(<!-- LAST_CHECKED_END -->)"
    if re.search(checked_pattern, readme_content, flags=re.DOTALL):
        readme_content = re.sub(checked_pattern, f"\\1Last checked: {today_str}\\3", readme_content, flags=re.DOTALL)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(readme_content)

    print(f"README.md updated successfully with date {today_str}!")


if __name__ == "__main__":
    update_readme()

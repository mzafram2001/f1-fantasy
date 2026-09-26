import os
import json
import re
from datetime import datetime

DATA_DIR = "data"
README_PATH = "README.md"


def get_round_files(season_dir, is_latest_season=False):
    files = [
        f
        for f in os.listdir(season_dir)
        if f.startswith("round_") and f.endswith(".json")
    ]
    if not files:
        return None, None

    files.sort()

    if is_latest_season and len(files) > 1:
        base_file = os.path.join(season_dir, files[-2])
        latest_file = os.path.join(season_dir, files[-1])
        return base_file, latest_file

    return os.path.join(season_dir, files[-1]), None


def format_percentage(val):
    try:
        return f"{int(float(val) * 100)}%"
    except (ValueError, TypeError):
        return "0%"


def generate_season_markdown(base_json_path, latest_json_path=None, is_latest_season=False):
    with open(base_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    latest_drivers_map = {}
    latest_teams_map = {}
    if latest_json_path and os.path.exists(latest_json_path):
        with open(latest_json_path, "r", encoding="utf-8") as f:
            latest_data = json.load(f)
            latest_drivers_map = {
                d.get("Driver_Name"): d for d in latest_data.get("Drivers", [])
            }
            latest_teams_map = {
                t.get("Team_Name"): t for t in latest_data.get("Teams", [])
            }

    # 🔥 HELPER 100% SÓLIDO: Distingue entre ceros reales y ceros de API sin actualizar
    def get_best_val(item_name, key, maps, base_item, default=0, is_market_data=False):
        latest_item = maps.get(item_name, base_item)
        val = latest_item.get(key)
        
        # 1. Si la clave literalmente no existe o está vacía (None o "")
        if val is None or val == "":
            return base_item.get(key, default)
            
        # 2. Si es un dato de "Mercado" (Porcentaje o Valor) y la API manda 0.0 por error o falta de update
        if is_market_data and (val == 0 or val == 0.0):
            return base_item.get(key, default)
            
        # 3. Si son Puntos, equipos, etc. Devolvemos el valor (incluso si es 0.0 real)
        return val

    meta = data.get("Meta", {})
    season = meta.get("season", "N/A")
    race_id = meta.get("race_id", 0)

    drivers = data.get("Drivers", [])
    top_drivers = sorted(
        drivers,
        key=lambda x: x.get("Season_Fantasy_Points", 0),
        reverse=True,
    )[:10]

    teams = data.get("Teams", [])
    top_teams = sorted(
        teams,
        key=lambda x: x.get("Season_Fantasy_Points", 0),
        reverse=True,
    )[:5]

    open_attr = " open" if is_latest_season else ""

    md = [
        f"<details{open_attr}>",
        f"<summary><b>🏎️ {season} Season — Round {race_id:02d}</b></summary>",
        "",
        "#### 👤 Top 10 Drivers",
        "",
        "| Driver | Team | Total fantasy pts | Value | Selected % |",
        "| :--- | :--- | :--- | :--- | :--- |",
    ]

    for d in top_drivers:
        name = d.get("Driver_Name", "N/A")
        
        team = get_best_val(name, "Team_Name", latest_drivers_map, d, "N/A")
        
        # Los puntos respetarán el 0 si el piloto puntúa 0 (is_market_data=False por defecto)
        season_pts = get_best_val(name, "Season_Fantasy_Points", latest_drivers_map, d)
        
        # El precio y el porcentaje de selección NO pueden ser 0, si lo son, usamos is_market_data=True
        val = get_best_val(name, "Value", latest_drivers_map, d, is_market_data=True)
        sel = format_percentage(get_best_val(name, "Selected_Percentage", latest_drivers_map, d, is_market_data=True))
        
        md.append(f"| **{name}** | {team} | {season_pts} pts | ${val}M | {sel} |")

    md.extend(
        [
            "",
            "#### 🏢 Top 5 Constructors",
            "",
            "| Team | Total fantasy pts | Value | Selected % |",
            "| :--- | :--- | :--- | :--- |",
        ]
    )

    for t in top_teams:
        name = t.get("Team_Name", "N/A")
        
        # Aplicamos la misma lógica súper segura a los constructores
        season_pts = get_best_val(name, "Season_Fantasy_Points", latest_teams_map, t)
        val = get_best_val(name, "Value", latest_teams_map, t, is_market_data=True)
        sel = format_percentage(get_best_val(name, "Selected_Percentage", latest_teams_map, t, is_market_data=True))
        
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
        
        base_file, latest_file = get_round_files(season_dir, is_latest_season=is_latest)

        if base_file:
            block = generate_season_markdown(
                base_file,
                latest_json_path=latest_file,
                is_latest_season=is_latest,
            )
            summary_blocks.append(block)

    full_summary_md = "\n\n".join(summary_blocks)

    if not os.path.exists(README_PATH):
        print(f"'{README_PATH}' not found.")
        return

    with open(README_PATH, "r", encoding="utf-8") as f:
        readme_content = f.read()

    summary_pattern = r"(<!-- SEASONS_SUMMARY_START -->)(.*?)(<!-- SEASONS_SUMMARY_END -->)"
    if re.search(summary_pattern, readme_content, flags=re.DOTALL):
        readme_content = re.sub(summary_pattern, f"\\1\n{full_summary_md}\n\\3", readme_content, flags=re.DOTALL)

    today_str = datetime.now().strftime("%Y-%m-%d")
    checked_pattern = r"(<!-- LAST_CHECKED_START -->)(.*?)(<!-- LAST_CHECKED_END -->)"
    if re.search(checked_pattern, readme_content, flags=re.DOTALL):
        readme_content = re.sub(checked_pattern, f"\\1Last checked: {today_str}\\3", readme_content, flags=re.DOTALL)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(readme_content)

    print(f"README.md updated successfully with date {today_str}!")


if __name__ == "__main__":
    update_readme()

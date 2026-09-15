import asyncio
import json
import os
from datetime import datetime
from fantasy import APIClient, Client

# Mapeo de normalización de códigos de equipo
TEAM_CODE_OVERRIDES = {
    "RBS": "VRB",
    "RBR": "RED",
}


def safe_float(value, default=0.0):
    """Convierte un valor a float de forma segura si está vacío o es nulo."""
    if value is None or value == "":
        return default
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def safe_percentage(value, default=0.0):
    """
    Convierte un valor de porcentaje a float relativo (0.0 a 1.0).
    Acepta strings como "24%", "24", o enteros/floats directamente.
    """
    if value is None or value == "":
        return default
    try:
        clean_val = str(value).replace("%", "").strip()
        val = float(clean_val)
        return round(val / 100.0, 4) if val > 1.0 else round(val, 4)
    except (ValueError, TypeError):
        return default


def load_previous_round_totals(season, previous_race_id):
    """
    Si se procesa una ronda individual, lee el JSON de la ronda previa
    para mantener la continuidad de los puntos acumulados.
    """
    filename = f"data/{season}/round_{previous_race_id:02d}.json"
    if not os.path.exists(filename):
        return {}, {}
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        d_totals = {d["Driver_Code"]: d["Season_Fantasy_Points"] for d in data.get("Drivers", [])}
        t_totals = {t["Team_Code"]: t["Season_Fantasy_Points"] for t in data.get("Teams", [])}
        return d_totals, t_totals
    except Exception:
        return {}, {}


def merge_driver_records(records):
    """
    Si un piloto tiene más de un registro en la misma ronda (por cambio de equipo),
    toma como base la ficha activa en la carrera y consolida el porcentaje de selección.
    """
    if len(records) == 1:
        return records[0]

    active_record = max(
        records,
        key=lambda r: (
            any([
                abs(r["Round_Fantasy_Points"]) > 0,
                abs(r["Qualifying_Points"]) > 0,
                abs(r["Sprint_Points"]) > 0,
                abs(r["Race_Points"]) > 0,
            ]),
            r["Value"],
        ),
    )

    total_selected = sum(r["Selected_Percentage"] for r in records)

    merged = dict(active_record)
    merged["Selected_Percentage"] = round(min(total_selected, 1.0), 4)

    return merged


def save_round_json(processed_drivers, processed_teams, race_id=1, season=None):
    """Guarda la información de la ronda en un archivo JSON independiente."""
    if season is None:
        season = datetime.now().year

    payload = {
        "Meta": {
            "season": season,
            "race_id": race_id,
            "generated_at": datetime.now().isoformat(),
        },
        "Drivers": processed_drivers,
        "Teams": processed_teams,
    }

    output_dir = f"data/{season}"
    os.makedirs(output_dir, exist_ok=True)

    filename = f"{output_dir}/round_{race_id:02d}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=4, ensure_ascii=False)

    print(f"📁 Guardado local: {filename}")


async def process_single_round(client, race_id, season, cumulative_drivers, cumulative_teams):
    """Descarga, procesa y guarda los datos de una única ronda respetando el esquema de campos."""
    url = f"/feeds/drivers/{race_id}_en.json"

    try:
        data = await client.api.request("GET", url)
    except Exception as e:
        print(f"⚠️ Ronda {race_id}: No disponible o error de red ({e})")
        return False

    if not data or not isinstance(data, dict):
        return False

    items = data.get("Data", {}).get("Value", [])
    if not items:
        print(f"ℹ️ Ronda {race_id}: Sin registros devueltos (fin de rondas disponibles).")
        return False

    if race_id > 1 and not cumulative_drivers:
        prev_d, prev_t = load_previous_round_totals(season, race_id - 1)
        cumulative_drivers.update(prev_d)
        cumulative_teams.update(prev_t)

    # 1. PROCESAMIENTO DE PILOTOS
    raw_drivers = [i for i in items if i.get("PositionName") == "DRIVER"]
    drivers_by_code = {}

    for d in raw_drivers:
        driver_code = d.get("DriverTLA", "N/A")

        # Se declara Season_Fantasy_Points en su orden exacto
        driver_payload = {
            "Driver_Name": d.get("DisplayName", "N/A"),
            "Driver_Code": driver_code,
            "Team_Name": d.get("TeamName", "N/A"),
            "Round_Fantasy_Points": safe_float(d.get("GamedayPoints")),
            "Season_Fantasy_Points": 0.0,
            "Selected_Percentage": safe_percentage(d.get("SelectedPercentage")),
            "Value": safe_float(d.get("Value")),
            "Qualifying_Points": safe_float(d.get("QualifyingPoints")),
            "Sprint_Points": safe_float(d.get("SprintPoints")),
            "Race_Points": safe_float(d.get("RacePoints")),
        }

        drivers_by_code.setdefault(driver_code, []).append(driver_payload)

    processed_drivers = [
        merge_driver_records(records)
        for records in drivers_by_code.values()
    ]

    for d in processed_drivers:
        code = d["Driver_Code"]
        prev_points = cumulative_drivers.get(code, 0.0)
        round_points = d["Round_Fantasy_Points"]
        total = round(prev_points + round_points, 1)

        cumulative_drivers[code] = total
        d["Season_Fantasy_Points"] = total

    processed_drivers.sort(
        key=lambda x: x["Season_Fantasy_Points"],
        reverse=True,
    )

    # 2. PROCESAMIENTO DE EQUIPOS
    raw_teams = [i for i in items if i.get("PositionName") == "CONSTRUCTOR"]
    processed_teams = []

    for t in raw_teams:
        raw_code = t.get("DriverTLA", "N/A")
        team_code = TEAM_CODE_OVERRIDES.get(raw_code, raw_code)

        # Se declara Season_Fantasy_Points en su orden exacto
        processed_teams.append({
            "Team_Name": t.get("DisplayName", "N/A"),
            "Team_Code": team_code,
            "Round_Fantasy_Points": safe_float(t.get("GamedayPoints")),
            "Season_Fantasy_Points": 0.0,
            "Selected_Percentage": safe_percentage(t.get("SelectedPercentage")),
            "Value": safe_float(t.get("Value")),
            "Qualifying_Points": safe_float(t.get("QualifyingPoints")),
            "Sprint_Points": safe_float(t.get("SprintPoints")),
            "Race_Points": safe_float(t.get("RacePoints")),
        })

    for t in processed_teams:
        code = t["Team_Code"]
        prev_points = cumulative_teams.get(code, 0.0)
        round_points = t["Round_Fantasy_Points"]
        total = round(prev_points + round_points, 1)

        cumulative_teams[code] = total
        t["Season_Fantasy_Points"] = total

    processed_teams.sort(
        key=lambda x: x["Season_Fantasy_Points"],
        reverse=True,
    )

    # 3. GUARDADO LOCAL EN JSON
    save_round_json(
        processed_drivers=processed_drivers,
        processed_teams=processed_teams,
        race_id=race_id,
        season=season,
    )

    return True


async def main():
    user_guid = os.getenv("F1_USER_GUID")
    token = os.getenv("F1_TOKEN")

    if not user_guid or not token:
        raise ValueError(
            "❌ Error: Las variables de entorno 'F1_USER_GUID' y/o 'F1_TOKEN' no están configuradas."
        )

    client = Client(APIClient(user_guid=user_guid, token=token))

    season = datetime.now().year
    max_rondas = 24

    cumulative_drivers = {}
    cumulative_teams = {}

    print(f"🚀 Descargando e historizando rondas de la temporada {season}...\n")

    for race_id in range(1, max_rondas + 1):
        print(f"Procesando Ronda {race_id}...")
        exito = await process_single_round(
            client,
            race_id,
            season,
            cumulative_drivers,
            cumulative_teams,
        )

        if not exito:
            print(f"\n⏹️ Bucle finalizado en Ronda {race_id}. Se han procesado todas las rondas jugadas.")
            break


if __name__ == "__main__":
    asyncio.run(main())

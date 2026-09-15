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


def merge_driver_records(records):
    """
    Si un piloto tiene más de un registro en la misma ronda (por cambio o sustitución de equipo),
    toma como base la ficha activa en la carrera y consolida los puntos acumulados de la temporada.
    """
    if len(records) == 1:
        return records[0]

    # Priorizamos la ficha que registró actividad o puntos en cualquiera de las sesiones;
    # en caso de empate (o fichas inactivas), desempata por la de mayor valor de mercado.
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

    # Consolidamos los puntos totales acumulados de la temporada y el porcentaje de selección
    total_season_points = sum(r["Season_Fantasy_Points"] for r in records)
    total_selected = sum(r["Selected_Percentage"] for r in records)

    merged = dict(active_record)
    merged["Season_Fantasy_Points"] = round(total_season_points, 1)
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


async def process_single_round(client, race_id, season):
    """Descarga, procesa y guarda los datos de una única ronda."""
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

    # 1. PROCESAMIENTO DE PILOTOS (con agrupación y fusión por Driver_Code)
    raw_drivers = [i for i in items if i.get("PositionName") == "DRIVER"]
    drivers_by_code = {}

    for d in raw_drivers:
        season_points = d.get("OverallPpints") if d.get("OverallPpints") is not None else d.get("OverallPoints")
        driver_code = d.get("DriverTLA", "N/A")

        driver_payload = {
            "Driver_Name": d.get("DisplayName", "N/A"),
            "Driver_Code": driver_code,
            "Team_Name": d.get("TeamName", "N/A"),
            "Round_Fantasy_Points": safe_float(d.get("GamedayPoints")),
            "Season_Fantasy_Points": safe_float(season_points),
            "Selected_Percentage": safe_percentage(d.get("SelectedPercentage")),
            "Value": safe_float(d.get("Value")),
            "Qualifying_Points": safe_float(d.get("QualifyingPoints")),
            "Sprint_Points": safe_float(d.get("SprintPoints")),
            "Race_Points": safe_float(d.get("RacePoints")),
        }

        drivers_by_code.setdefault(driver_code, []).append(driver_payload)

    # Fusionamos fichas duplicadas si las hay y ordenamos por puntos de temporada
    processed_drivers = [
        merge_driver_records(records)
        for records in drivers_by_code.values()
    ]

    processed_drivers.sort(
        key=lambda x: x["Season_Fantasy_Points"],
        reverse=True,
    )

    # 2. PROCESAMIENTO DE EQUIPOS
    raw_teams = [i for i in items if i.get("PositionName") == "CONSTRUCTOR"]
    processed_teams = []

    for t in raw_teams:
        season_points = t.get("OverallPpints") if t.get("OverallPpints") is not None else t.get("OverallPoints")
        raw_code = t.get("DriverTLA", "N/A")
        team_code = TEAM_CODE_OVERRIDES.get(raw_code, raw_code)

        processed_teams.append({
            "Team_Name": t.get("DisplayName", "N/A"),
            "Team_Code": team_code,
            "Round_Fantasy_Points": safe_float(t.get("GamedayPoints")),
            "Season_Fantasy_Points": safe_float(season_points),
            "Selected_Percentage": safe_percentage(t.get("SelectedPercentage")),
            "Value": safe_float(t.get("Value")),
            "Qualifying_Points": safe_float(t.get("QualifyingPoints")),
            "Sprint_Points": safe_float(t.get("SprintPoints")),
            "Race_Points": safe_float(t.get("RacePoints")),
        })

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

    print(f"🚀 Descargando e historizando rondas de la temporada {season}...\n")

    for race_id in range(1, max_rondas + 1):
        print(f"Procesando Ronda {race_id}...")
        exito = await process_single_round(client, race_id, season)

        if not exito:
            print(f"\n⏹️ Bucle finalizado en Ronda {race_id}. Se han procesado todas las rondas jugadas.")
            break


if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import json
import os
from datetime import datetime
from fantasy import APIClient, Client


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

    # 1. PROCESAMIENTO DE PILOTOS
    drivers = [i for i in items if i.get("PositionName") == "DRIVER"]
    processed_drivers = []

    for d in drivers:
        # Fallback defensivo: 'OverallPpints' (typo histórico) u 'OverallPoints'
        season_points = d.get("OverallPpints") if d.get("OverallPpints") is not None else d.get("OverallPoints")

        processed_drivers.append({
            "Driver_Name": d.get("DisplayName", "N/A"),
            "Driver_Code": d.get("DriverTLA", "N/A"),
            "Team_Name": d.get("TeamName", "N/A"),
            "Round_Fantasy_Points": safe_float(d.get("GamedayPoints")),
            "Season_Fantasy_Points": safe_float(season_points),
            "Selected_Percentage": safe_percentage(d.get("SelectedPercentage")),
            "Value": safe_float(d.get("Value")),
            "Qualifying_Points": safe_float(d.get("QualifyingPoints")),
            "Sprint_Points": safe_float(d.get("SprintPoints")),
            "Race_Points": safe_float(d.get("RacePoints")),
        })

    processed_drivers = sorted(
        processed_drivers,
        key=lambda x: x["Season_Fantasy_Points"],
        reverse=True,
    )

    # 2. PROCESAMIENTO DE EQUIPOS
    teams = [i for i in items if i.get("PositionName") == "CONSTRUCTOR"]
    processed_teams = []

    for t in teams:
        season_points = t.get("OverallPpints") if t.get("OverallPpints") is not None else t.get("OverallPoints")

        processed_teams.append({
            "Team_Name": t.get("DisplayName", "N/A"),
            "Team_Code": t.get("DriverTLA", "N/A"),
            "Round_Fantasy_Points": safe_float(t.get("GamedayPoints")),
            "Season_Fantasy_Points": safe_float(season_points),
            "Selected_Percentage": safe_percentage(t.get("SelectedPercentage")),
            "Value": safe_float(t.get("Value")),
            "Qualifying_Points": safe_float(t.get("QualifyingPoints")),
            "Sprint_Points": safe_float(t.get("SprintPoints")),
            "Race_Points": safe_float(t.get("RacePoints")),
        })

    processed_teams = sorted(
        processed_teams,
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

    # Temporada actual dinámica
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

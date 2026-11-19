import json
import os
import sys
from pathlib import Path

DATA_DIR = Path("data")
REQUIRED_META_KEYS = {
    "Id",
    "Season",
    "Race_Id",
    "Event_Name",
    "Is_Sprint",
    "Circuit",
    "Start_Times",
    "Generated_At",
}
REQUIRED_ENTITY_KEYS = {
    "Round_Fantasy_Points",
    "Season_Fantasy_Points",
    "Selected_Percentage",
    "Value",
    "Qualifying_Points",
    "Sprint_Points",
    "Race_Points",
}


def validate_entity(entity, kind, path, season, errors, warnings):
    code_key = "Driver_Code" if kind == "Drivers" else "Team_Code"
    name_key = "Driver_Name" if kind == "Drivers" else "Team_Name"

    missing = REQUIRED_ENTITY_KEYS - entity.keys()
    if missing:
        errors.append(f"{path} [{kind}]: faltan claves {sorted(missing)}")
        return

    code = entity.get(code_key)
    name = entity.get(name_key, "?")
    if not code or code == "N/A":
        errors.append(f"{path} [{kind}]: '{name}' tiene {code_key} inválido ({code})")

    if kind == "Drivers":
        t_code = entity.get("Team_Code")
        if not t_code or t_code == "N/A":
            errors.append(f"{path} [Drivers]: '{name}' tiene Team_Code inválido ({t_code})")
        elif code:
            driver_svg = f"src/drivers/{code.lower()}-{t_code.lower()}-{season}.svg"
            if not os.path.exists(driver_svg):
                warnings.append(f"{path}: falta SVG de piloto {driver_svg} (usará default.svg)")
    elif code:
        team_svg = f"src/constructors/{code.lower()}-{season}.svg"
        if not os.path.exists(team_svg):
            warnings.append(f"{path}: falta SVG de equipo {team_svg} (usará default.svg)")

    # Comprobación aritmética del desglose de puntos (solo aviso por sanciones post-carrera en la API)
    q_pts = float(entity["Qualifying_Points"])
    s_pts = float(entity["Sprint_Points"])
    r_pts = float(entity["Race_Points"])
    total_round = float(entity["Round_Fantasy_Points"])

    if abs((q_pts + s_pts + r_pts) - total_round) > 0.1:
        warnings.append(
            f"{path} [{kind} {code}]: desglose oficial difiere del total "
            f"({q_pts} + {s_pts} + {r_pts} != {total_round})"
        )

    sel = float(entity["Selected_Percentage"])
    if not (0.0 <= sel <= 1.0):
        errors.append(f"{path} [{kind} {code}]: Selected_Percentage fuera de rango ({sel})")


def validate_all():
    if not DATA_DIR.exists():
        print("❌ No existe el directorio 'data/'.")
        sys.exit(1)

    files = sorted(DATA_DIR.glob("*/*.json"))
    if not files:
        print("❌ No se encontraron archivos JSON en 'data/'.")
        sys.exit(1)

    errors = []
    warnings = []

    for path in files:
        try:
            with path.open("r", encoding="utf-8") as f:
                payload = json.load(f)
        except Exception as e:
            errors.append(f"{path}: JSON inválido ({e})")
            continue

        meta = payload.get("Meta")
        if not isinstance(meta, dict):
            errors.append(f"{path}: falta el objeto 'Meta'")
            continue

        missing_meta = REQUIRED_META_KEYS - meta.keys()
        if missing_meta:
            errors.append(f"{path}: faltan claves en Meta {sorted(missing_meta)}")

        season = meta.get("Season")
        circuit = meta.get("Circuit")
        if isinstance(circuit, dict):
            svg_path = circuit.get("Svg_Path")
            if not svg_path or not os.path.exists(svg_path):
                errors.append(f"{path}: no existe el SVG del circuito '{svg_path}'")
        else:
            warnings.append(f"{path}: Meta.Circuit es nulo (posible fallo puntual de Jolpica)")

        drivers = payload.get("Drivers", [])
        teams = payload.get("Teams", [])
        if not drivers or not teams:
            errors.append(f"{path}: listas 'Drivers' o 'Teams' vacías")

        for d in drivers:
            validate_entity(d, "Drivers", path, season, errors, warnings)
        for t in teams:
            validate_entity(t, "Teams", path, season, errors, warnings)

    if warnings:
        print(f"⚠️ Avisos ({len(warnings)}):")
        for w in warnings:
            print(f"  - {w}")

    if errors:
        print(f"\n❌ Validación fallida con {len(errors)} errores:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)

    print(f"✅ Validación superada: {len(files)} archivos JSON verificados correctamente.")


if __name__ == "__main__":
    validate_all()

import json
import os
from datetime import datetime
from urllib.error import URLError
from urllib.request import Request, urlopen

JOLPICA_BASE = "https://api.jolpi.ca/ergast/f1"
HEADERS = {"User-Agent": "f1-fantasy-repo/1.0"}

# circuitId de Jolpica -> (nombre SVG en src/circuits/, código ISO-3)
CIRCUIT_MAP = {
    "albert_park":   ("melbourne", "AUS"),
    "americas":      ("austin", "USA"),
    "bahrain":       ("bahrain", "BHR"),
    "baku":          ("baku", "AZE"),
    "catalunya":     ("catalunya", "ESP"),
    "hungaroring":   ("hungaroring", "HUN"),
    "imola":         ("imola", "ITA"),
    "interlagos":    ("interlagos", "BRA"),
    "istanbul":      ("istanbul", "TUR"),
    "jeddah":        ("jeddah", "SAU"),
    "losail":        ("lusail", "QAT"),
    "madrid":        ("madring", "ESP"),
    "madring":       ("madring", "ESP"),
    "marina_bay":    ("marina-bay", "SGP"),
    "miami":         ("miami", "USA"),
    "monaco":        ("monaco", "MCO"),
    "monza":         ("monza", "ITA"),
    "portimao":      ("portimao", "PRT"),
    "red_bull_ring": ("spielberg", "AUT"),
    "rodriguez":     ("mexico-city", "MEX"),
    "sepang":        ("sepang", "MYS"),
    "shanghai":      ("shanghai", "CHN"),
    "silverstone":   ("silverstone", "GBR"),
    "spa":           ("spa-francorchamps", "BEL"),
    "suzuka":        ("suzuka", "JPN"),
    "vegas":         ("las-vegas", "USA"),
    "villeneuve":    ("montreal", "CAN"),
    "yas_marina":    ("yas-marina", "ARE"),
    "zandvoort":     ("zandvoort", "NLD"),
}

# Normalización de nombres de país abreviados en Jolpica-F1
COUNTRY_NAME_OVERRIDES = {
    "US": "United States",
    "USA": "United States",
    "UK": "United Kingdom",
    "UAE": "United Arab Emirates",
}


def to_iso_utc(session_obj):
    if not session_obj or not session_obj.get("date"):
        return None
    date_str = session_obj["date"]
    time_str = session_obj.get("time")
    return f"{date_str}T{time_str}" if time_str else date_str


def fetch_season_schedule(season):
    """Descarga el calendario oficial de la temporada desde Jolpica-F1."""
    url = f"{JOLPICA_BASE}/{season}.json"
    try:
        req = Request(url, headers=HEADERS)
        with urlopen(req, timeout=20) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        races = payload["MRData"]["RaceTable"]["Races"]
        return {int(r["round"]): r for r in races}
    except (URLError, TimeoutError, KeyError, json.JSONDecodeError) as e:
        print(f"⚠️ No se pudo obtener el calendario {season} de Jolpica-F1: {e}")
        return {}


def build_meta(season, race_id, race_info=None, generated_at=None, strict=False):
    """Construye el bloque Meta en Pascal_Snake_Case."""
    generated_at = generated_at or datetime.now().isoformat()

    if not race_info:
        return {
            "Id": f"{season}_{race_id:02d}",
            "Season": season,
            "Race_Id": race_id,
            "Event_Name": None,
            "Is_Sprint": False,
            "Circuit": None,
            "Start_Times": {
                "Qualifying": None,
                "Sprint_Qualifying": None,
                "Sprint": None,
                "Race": None,
            },
            "Generated_At": generated_at,
        }

    circuit = race_info["Circuit"]
    loc = circuit["Location"]
    jolpica_cid = circuit["circuitId"]

    if jolpica_cid in CIRCUIT_MAP:
        svg_slug, country_code = CIRCUIT_MAP[jolpica_cid]
    elif strict:
        raise KeyError(f"circuitId no mapeado: '{jolpica_cid}' ({race_info['raceName']} {season})")
    else:
        print(f"⚠️ circuitId no mapeado en CIRCUIT_MAP: '{jolpica_cid}'")
        svg_slug, country_code = jolpica_cid, None

    svg_path = f"src/circuits/{svg_slug}.svg"
    if not os.path.exists(svg_path):
        print(f"⚠️ No existe el archivo SVG: {svg_path}")

    country_name = COUNTRY_NAME_OVERRIDES.get(loc["country"], loc["country"])
    sprint_obj = race_info.get("Sprint")
    sprint_quali_obj = race_info.get("SprintQualifying") or race_info.get("SprintShootout")

    return {
        "Id": f"{season}_{race_id:02d}",
        "Season": season,
        "Race_Id": race_id,
        "Event_Name": race_info["raceName"],
        "Is_Sprint": sprint_obj is not None,
        "Circuit": {
            "Id": svg_slug,
            "City": loc["locality"],
            "Country_Code": country_code,
            "Country_Name": country_name,
            "Svg_Path": svg_path,
        },
        "Start_Times": {
            "Qualifying": to_iso_utc(race_info.get("Qualifying")),
            "Sprint_Qualifying": to_iso_utc(sprint_quali_obj),
            "Sprint": to_iso_utc(sprint_obj),
            "Race": to_iso_utc({"date": race_info.get("date"), "time": race_info.get("time")}),
        },
        "Generated_At": generated_at,
    }

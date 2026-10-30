# 🏎️ f1-fantasy

![Status](https://img.shields.io/badge/Status-Available-green)
![License](https://img.shields.io/badge/License-MIT-blue)
![Format](https://img.shields.io/badge/Format-JSON-orange)
![Stack](https://img.shields.io/badge/Stack-Python-yellow)
![Last updated](https://img.shields.io/github/last-commit/mzafram2001/f1-fantasy?label=Last%20update)

An open-source, automated historical dataset of F1 Fantasy statistics.

This repository automatically fetches, cleans, and structures official F1 Fantasy data after every Grand Prix weekend. Providing points breakdowns, value fluctuations, selection trends, and constructor stats for analytics, machine learning and data visualization.

---

## 📂 Repository structure

```text
f1-fantasy/
│
├── .github/
│   ├── workflows/
│   │   └── get_round_data.yml
│   └── FUNDING.yml
│ 
├── data/
│   ├── 2023/
│   │   ├── round_01.json
│   │   ├── round_02.json
│   │   └── ...
│   ├── 2024/
│   │   ├── round_01.json
│   │   ├── round_02.json
│   │   └── ...
│   └── ...
│
├── scripts/
│   ├── get_round_data.py
│   └── update_readme.py
│
├── AUTHORS.md
├── LICENSE.md
└── README.md
```

---

## 📊 Data schema

Each round file (`data/{season}/round_{id}.json`) follows a standardized JSON schema divided into **Meta**, **Drivers**, and **Teams**. Both driver and team arrays share identical attributes:

| Attribute | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `Driver_Name` / `Team_Name` | `String` | Display name of the driver or team | `"K. Antonelli"` / `"Mercedes"` |
| `Driver_Code` / `Team_Code` | `String` | Three-letter shorthand identifier (TLA) | `"ANT"` / `"MER"` |
| `Team_Name` *(Drivers only)* | `String` | Constructor associated with the driver | `"Mercedes"` |
| `Round_Fantasy_Points` | `Float` | Total fantasy points scored in the current round | `55.0` |
| `Season_Fantasy_Points` | `Float` | Total cumulative fantasy points scored up to this round | `305.0` |
| `Selected_Percentage` | `Float` | Player selection rate across fantasy teams | `0.33` *(33%)* |
| `Value` | `Float` | Current asset price for the round (in $M) | `24.7` |
| `Qualifying_Points` | `Float` | Fantasy points earned in qualifying | `10.0` |
| `Sprint_Points` | `Float` | Fantasy points earned in sprint | `0.0` |
| `Race_Points` | `Float` | Fantasy points earned in race | `45.0` |

---

## 💻 Data results

<!-- SEASONS_SUMMARY_START -->
<details open>
<summary><b>🏎️ 2026 Season — Round 18</b></summary>

#### 👤 Drivers Standings

| Driver | Total fantasy pts | Value | Selected % |
| :--- | :--- | :--- | :--- |
| <img src='src/drivers/ant-mer-2026.svg' width='44' height='32' align='center'> | 720.0 pts | $27.4M | 36% |
| <img src='src/drivers/ver-red-2026.svg' width='44' height='32' align='center'> | 513.0 pts | $28.5M | 22% |
| <img src='src/drivers/ham-fer-2026.svg' width='44' height='32' align='center'> | 483.0 pts | $24.7M | 18% |
| <img src='src/drivers/lec-fer-2026.svg' width='44' height='32' align='center'> | 480.0 pts | $24.4M | 27% |
| <img src='src/drivers/rus-mer-2026.svg' width='44' height='32' align='center'> | 434.0 pts | $27.6M | 21% |
| <img src='src/drivers/nor-mcl-2026.svg' width='44' height='32' align='center'> | 380.0 pts | $26.0M | 8% |
| <img src='src/drivers/pia-mcl-2026.svg' width='44' height='32' align='center'> | 278.0 pts | $23.3M | 9% |
| <img src='src/drivers/law-vrb-2026.svg' width='44' height='32' align='center'> | 227.0 pts | $10.5M | 28% |
| <img src='src/drivers/had-red-2026.svg' width='44' height='32' align='center'> | 214.0 pts | $16.5M | 28% |
| <img src='src/drivers/oco-haa-2026.svg' width='44' height='32' align='center'> | 168.0 pts | $10.1M | 13% |
| <img src='src/drivers/lin-vrb-2026.svg' width='44' height='32' align='center'> | 147.0 pts | $10.6M | 44% |
| <img src='src/drivers/gas-alp-2026.svg' width='44' height='32' align='center'> | 139.0 pts | $9.6M | 20% |
| <img src='src/drivers/sai-wil-2026.svg' width='44' height='32' align='center'> | 120.0 pts | $8.2M | 22% |
| <img src='src/drivers/col-alp-2026.svg' width='44' height='32' align='center'> | 105.0 pts | $8.2M | 19% |
| <img src='src/drivers/bor-aud-2026.svg' width='44' height='32' align='center'> | 84.0 pts | $6.4M | 31% |
| <img src='src/drivers/bea-haa-2026.svg' width='44' height='32' align='center'> | 81.0 pts | $6.2M | 52% |
| <img src='src/drivers/hul-aud-2026.svg' width='44' height='32' align='center'> | 47.0 pts | $7.2M | 36% |
| <img src='src/drivers/alo-ast-2026.svg' width='44' height='32' align='center'> | 39.0 pts | $6.0M | 10% |
| <img src='src/drivers/per-cad-2026.svg' width='44' height='32' align='center'> | 19.0 pts | $3.0M | 21% |
| <img src='src/drivers/alb-wil-2026.svg' width='44' height='32' align='center'> | 0.0 pts | $4.0M | 10% |
| <img src='src/drivers/bot-cad-2026.svg' width='44' height='32' align='center'> | -117.0 pts | $3.0M | 20% |
| <img src='src/drivers/str-ast-2026.svg' width='44' height='32' align='center'> | -147.0 pts | $3.0M | 4% |

#### 🏢 Constructors Standings

| Team | Total fantasy pts | Value | Selected % |
| :--- | :--- | :--- | :--- |
| <img src='src/constructors/mer-2026.svg' width='44' height='32' align='center'> | 1430.0 pts | $34.0M | 35% |
| <img src='src/constructors/fer-2026.svg' width='44' height='32' align='center'> | 1179.0 pts | $28.5M | 41% |
| <img src='src/constructors/red-2026.svg' width='44' height='32' align='center'> | 934.0 pts | $33.0M | 9% |
| <img src='src/constructors/mcl-2026.svg' width='44' height='32' align='center'> | 894.0 pts | $32.7M | 10% |
| <img src='src/constructors/vrb-2026.svg' width='44' height='32' align='center'> | 559.0 pts | $17.1M | 33% |
| <img src='src/constructors/alp-2026.svg' width='44' height='32' align='center'> | 372.0 pts | $18.5M | 7% |
| <img src='src/constructors/haa-2026.svg' width='44' height='32' align='center'> | 297.0 pts | $12.6M | 24% |
| <img src='src/constructors/aud-2026.svg' width='44' height='32' align='center'> | 267.0 pts | $11.0M | 21% |
| <img src='src/constructors/wil-2026.svg' width='44' height='32' align='center'> | 198.0 pts | $12.0M | 9% |
| <img src='src/constructors/ast-2026.svg' width='44' height='32' align='center'> | -73.0 pts | $5.1M | 3% |
| <img src='src/constructors/cad-2026.svg' width='44' height='32' align='center'> | -102.0 pts | $3.0M | 9% |

</details>


<details>
<summary><b>🏎️ 2025 Season — Round 24</b></summary>

#### 👤 Drivers Standings

| Driver | Total fantasy pts | Value | Selected % |
| :--- | :--- | :--- | :--- |
| <img src='src/drivers/ver-red-2025.svg' width='44' height='32' align='center'> | 776.0 pts | $30.1M | 21% |
| <img src='src/drivers/nor-mcl-2025.svg' width='44' height='32' align='center'> | 707.0 pts | $30.3M | 23% |
| <img src='src/drivers/pia-mcl-2025.svg' width='44' height='32' align='center'> | 644.0 pts | $25.1M | 35% |
| <img src='src/drivers/rus-mer-2025.svg' width='44' height='32' align='center'> | 580.0 pts | $23.7M | 12% |
| <img src='src/drivers/lec-fer-2025.svg' width='44' height='32' align='center'> | 407.0 pts | $23.0M | 14% |
| <img src='src/drivers/ham-fer-2025.svg' width='44' height='32' align='center'> | 391.0 pts | $21.9M | 11% |
| <img src='src/drivers/ant-mer-2025.svg' width='44' height='32' align='center'> | 311.0 pts | $18.1M | 21% |
| <img src='src/drivers/bea-haa-2025.svg' width='44' height='32' align='center'> | 206.0 pts | $9.3M | 43% |
| <img src='src/drivers/alb-wil-2025.svg' width='44' height='32' align='center'> | 198.0 pts | $12.6M | 27% |
| <img src='src/drivers/tsu-red-2025.svg' width='44' height='32' align='center'> | 183.0 pts | $11.4M | 6% |
| <img src='src/drivers/oco-haa-2025.svg' width='44' height='32' align='center'> | 177.0 pts | $7.9M | 22% |
| <img src='src/drivers/hul-kck-2025.svg' width='44' height='32' align='center'> | 147.0 pts | $5.0M | 32% |
| <img src='src/drivers/str-ast-2025.svg' width='44' height='32' align='center'> | 146.0 pts | $6.7M | 10% |
| <img src='src/drivers/sai-wil-2025.svg' width='44' height='32' align='center'> | 130.0 pts | $7.7M | 44% |
| <img src='src/drivers/had-vrb-2025.svg' width='44' height='32' align='center'> | 111.0 pts | $6.9M | 56% |
| <img src='src/drivers/law-vrb-2025.svg' width='44' height='32' align='center'> | 64.0 pts | $5.9M | 12% |
| <img src='src/drivers/gas-alp-2025.svg' width='44' height='32' align='center'> | 58.0 pts | $6.5M | 20% |
| <img src='src/drivers/alo-ast-2025.svg' width='44' height='32' align='center'> | 58.0 pts | $4.7M | 38% |
| <img src='src/drivers/bor-kck-2025.svg' width='44' height='32' align='center'> | 53.0 pts | $5.5M | 24% |
| <img src='src/drivers/col-alp-2025.svg' width='44' height='32' align='center'> | 8.0 pts | $4.5M | 10% |

#### 🏢 Constructors Standings

| Team | Total fantasy pts | Value | Selected % |
| :--- | :--- | :--- | :--- |
| <img src='src/constructors/mcl-2025.svg' width='44' height='32' align='center'> | 1744.0 pts | $36.1M | 38% |
| <img src='src/constructors/red-2025.svg' width='44' height='32' align='center'> | 1227.0 pts | $31.1M | 11% |
| <img src='src/constructors/mer-2025.svg' width='44' height='32' align='center'> | 1185.0 pts | $28.4M | 19% |
| <img src='src/constructors/fer-2025.svg' width='44' height='32' align='center'> | 1145.0 pts | $31.8M | 18% |
| <img src='src/constructors/wil-2025.svg' width='44' height='32' align='center'> | 490.0 pts | $19.5M | 25% |
| <img src='src/constructors/haa-2025.svg' width='44' height='32' align='center'> | 482.0 pts | $15.6M | 18% |
| <img src='src/constructors/vrb-2025.svg' width='44' height='32' align='center'> | 462.0 pts | $16.2M | 27% |
| <img src='src/constructors/ast-2025.svg' width='44' height='32' align='center'> | 344.0 pts | $10.3M | 16% |
| <img src='src/constructors/kck-2025.svg' width='44' height='32' align='center'> | 307.0 pts | $8.7M | 15% |
| <img src='src/constructors/alp-2025.svg' width='44' height='32' align='center'> | 165.0 pts | $10.1M | 11% |

</details>


<details>
<summary><b>🏎️ 2024 Season — Round 24</b></summary>

#### 👤 Drivers Standings

| Driver | Total fantasy pts | Value | Selected % |
| :--- | :--- | :--- | :--- |
| <img src='src/drivers/ver-red-2024.svg' width='44' height='32' align='center'> | 754.0 pts | $32.3M | 36% |
| <img src='src/drivers/nor-mcl-2024.svg' width='44' height='32' align='center'> | 695.0 pts | $27.5M | 30% |
| <img src='src/drivers/lec-fer-2024.svg' width='44' height='32' align='center'> | 684.0 pts | $26.1M | 31% |
| <img src='src/drivers/pia-mcl-2024.svg' width='44' height='32' align='center'> | 584.0 pts | $25.7M | 19% |
| <img src='src/drivers/sai-fer-2024.svg' width='44' height='32' align='center'> | 504.0 pts | $24.4M | 19% |
| <img src='src/drivers/ham-mer-2024.svg' width='44' height='32' align='center'> | 495.0 pts | $25.8M | 15% |
| <img src='src/drivers/rus-mer-2024.svg' width='44' height='32' align='center'> | 455.0 pts | $23.2M | 13% |
| <img src='src/drivers/per-red-2024.svg' width='44' height='32' align='center'> | 319.0 pts | $23.2M | 8% |
| <img src='src/drivers/alo-ast-2024.svg' width='44' height='32' align='center'> | 173.0 pts | $15.3M | 28% |
| <img src='src/drivers/mag-haa-2024.svg' width='44' height='32' align='center'> | 165.0 pts | $14.3M | 18% |
| <img src='src/drivers/zho-kck-2024.svg' width='44' height='32' align='center'> | 105.0 pts | $9.6M | 16% |
| <img src='src/drivers/gas-alp-2024.svg' width='44' height='32' align='center'> | 92.0 pts | $11.8M | 27% |
| <img src='src/drivers/str-ast-2024.svg' width='44' height='32' align='center'> | 87.0 pts | $14.3M | 11% |
| <img src='src/drivers/hul-haa-2024.svg' width='44' height='32' align='center'> | 86.0 pts | $11.8M | 34% |
| <img src='src/drivers/tsu-vrb-2024.svg' width='44' height='32' align='center'> | 69.0 pts | $11.9M | 33% |
| <img src='src/drivers/bot-kck-2024.svg' width='44' height='32' align='center'> | 46.0 pts | $7.1M | 28% |
| <img src='src/drivers/law-vrb-2024.svg' width='44' height='32' align='center'> | 35.0 pts | $10.9M | 5% |
| <img src='src/drivers/doo-alp-2024.svg' width='44' height='32' align='center'> | 8.0 pts | $10.9M | 1% |
| <img src='src/drivers/col-wil-2024.svg' width='44' height='32' align='center'> | 7.0 pts | $7.4M | 19% |
| <img src='src/drivers/alb-wil-2024.svg' width='44' height='32' align='center'> | -9.0 pts | $8.6M | 48% |

#### 🏢 Constructors Standings

| Team | Total fantasy pts | Value | Selected % |
| :--- | :--- | :--- | :--- |
| <img src='src/constructors/mcl-2024.svg' width='44' height='32' align='center'> | 1506.0 pts | $27.0M | 27% |
| <img src='src/constructors/red-2024.svg' width='44' height='32' align='center'> | 1421.0 pts | $29.7M | 22% |
| <img src='src/constructors/fer-2024.svg' width='44' height='32' align='center'> | 1414.0 pts | $25.3M | 37% |
| <img src='src/constructors/mer-2024.svg' width='44' height='32' align='center'> | 1146.0 pts | $25.1M | 15% |
| <img src='src/constructors/ast-2024.svg' width='44' height='32' align='center'> | 395.0 pts | $14.4M | 18% |
| <img src='src/constructors/haa-2024.svg' width='44' height='32' align='center'> | 356.0 pts | $12.2M | 16% |
| <img src='src/constructors/alp-2024.svg' width='44' height='32' align='center'> | 316.0 pts | $12.1M | 8% |
| <img src='src/constructors/vrb-2024.svg' width='44' height='32' align='center'> | 296.0 pts | $12.9M | 27% |
| <img src='src/constructors/kck-2024.svg' width='44' height='32' align='center'> | 179.0 pts | $7.5M | 8% |
| <img src='src/constructors/wil-2024.svg' width='44' height='32' align='center'> | 56.0 pts | $6.1M | 22% |

</details>


<details>
<summary><b>🏎️ 2023 Season — Round 22</b></summary>

#### 👤 Drivers Standings

| Driver | Total fantasy pts | Value | Selected % |
| :--- | :--- | :--- | :--- |
| <img src='src/drivers/ver-red-2023.svg' width='44' height='32' align='center'> | 1014.0 pts | $30.0M | 65% |
| <img src='src/drivers/per-red-2023.svg' width='44' height='32' align='center'> | 579.0 pts | $20.8M | 43% |
| <img src='src/drivers/ham-mer-2023.svg' width='44' height='32' align='center'> | 506.0 pts | $25.3M | 18% |
| <img src='src/drivers/nor-mcl-2023.svg' width='44' height='32' align='center'> | 438.0 pts | $19.8M | 25% |
| <img src='src/drivers/alo-ast-2023.svg' width='44' height='32' align='center'> | 403.0 pts | $15.8M | 77% |
| <img src='src/drivers/sai-fer-2023.svg' width='44' height='32' align='center'> | 394.0 pts | $20.4M | 23% |
| <img src='src/drivers/rus-mer-2023.svg' width='44' height='32' align='center'> | 384.0 pts | $20.2M | 20% |
| <img src='src/drivers/lec-fer-2023.svg' width='44' height='32' align='center'> | 335.0 pts | $23.5M | 28% |
| <img src='src/drivers/pia-mcl-2023.svg' width='44' height='32' align='center'> | 279.0 pts | $15.4M | 17% |
| <img src='src/drivers/str-ast-2023.svg' width='44' height='32' align='center'> | 231.0 pts | $14.0M | 26% |
| <img src='src/drivers/gas-alp-2023.svg' width='44' height='32' align='center'> | 230.0 pts | $14.5M | 28% |
| <img src='src/drivers/tsu-alt-2023.svg' width='44' height='32' align='center'> | 160.0 pts | $9.4M | 10% |
| <img src='src/drivers/zho-alf-2023.svg' width='44' height='32' align='center'> | 135.0 pts | $7.7M | 16% |
| <img src='src/drivers/alb-wil-2023.svg' width='44' height='32' align='center'> | 126.0 pts | $11.3M | 13% |
| <img src='src/drivers/oco-alp-2023.svg' width='44' height='32' align='center'> | 120.0 pts | $13.5M | 10% |
| <img src='src/drivers/mag-haa-2023.svg' width='44' height='32' align='center'> | 89.0 pts | $9.6M | 13% |
| <img src='src/drivers/hul-haa-2023.svg' width='44' height='32' align='center'> | 59.0 pts | $6.2M | 23% |
| <img src='src/drivers/ric-alt-2023.svg' width='44' height='32' align='center'> | 49.0 pts | $5.5M | 12% |
| <img src='src/drivers/bot-alf-2023.svg' width='44' height='32' align='center'> | 43.0 pts | $9.6M | 18% |
| <img src='src/drivers/sar-wil-2023.svg' width='44' height='32' align='center'> | 3.0 pts | $5.8M | 8% |

#### 🏢 Constructors Standings

| Team | Total fantasy pts | Value | Selected % |
| :--- | :--- | :--- | :--- |
| <img src='src/constructors/red-2023.svg' width='44' height='32' align='center'> | 1847.0 pts | $29.7M | 56% |
| <img src='src/constructors/mer-2023.svg' width='44' height='32' align='center'> | 1060.0 pts | $26.0M | 13% |
| <img src='src/constructors/fer-2023.svg' width='44' height='32' align='center'> | 1007.0 pts | $25.0M | 23% |
| <img src='src/constructors/mcl-2023.svg' width='44' height='32' align='center'> | 899.0 pts | $17.1M | 15% |
| <img src='src/constructors/ast-2023.svg' width='44' height='32' align='center'> | 757.0 pts | $13.4M | 68% |
| <img src='src/constructors/alp-2023.svg' width='44' height='32' align='center'> | 467.0 pts | $14.2M | 9% |
| <img src='src/constructors/alt-2023.svg' width='44' height='32' align='center'> | 312.0 pts | $8.7M | 2% |
| <img src='src/constructors/alf-2023.svg' width='44' height='32' align='center'> | 222.0 pts | $6.6M | 5% |
| <img src='src/constructors/haa-2023.svg' width='44' height='32' align='center'> | 215.0 pts | $7.2M | 4% |
| <img src='src/constructors/wil-2023.svg' width='44' height='32' align='center'> | 171.0 pts | $7.8M | 3% |

</details>

<!-- SEASONS_SUMMARY_END -->

---

## ⚡ Quick start

```
import pandas as pd

# Load round data directly from GitHub into a DataFrame
url = "https://raw.githubusercontent.com/mzafram2001/f1-fantasy/main/data/2026/round_11.json"
data = pd.read_json(url)

# Convert Drivers into a Pandas DataFrame
df_drivers = pd.DataFrame(data["Drivers"].tolist())
print(df_drivers.sort_values(by="Season_Fantasy_Points", ascending=False).head())
```

---

> [!CAUTION]
> **Disclaimer:** Data is collected from public sources. This repository is for educational and research purposes only. Not financial advice.

> [!TIP]
> **Want to help?**
> ⭐ Do you like this project? If you find this data useful, please give it a star! It helps me keep updating it.
>
> ☕ If this dataset saves you time in your analysis or fantasy leagues, you can also [buy me a coffee on Ko-fi](https://ko-fi.com/mzm0102).
<br>
<!-- LAST_CHECKED_START -->Last checked: 2026-10-30<!-- LAST_CHECKED_END -->

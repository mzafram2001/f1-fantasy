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
<summary><b>🏎️ 2026 Season — Round 14</b></summary>

#### 👤 Top 10 Drivers

| Driver | Team | Total fantasy pts | Value | Selected % |
| :--- | :--- | :--- | :--- | :--- |
| **K. Antonelli** | Mercedes | 594.0 pts | $26.6M | 38% |
| **L. Hamilton** | Ferrari | 380.0 pts | $24.9M | 19% |
| **G. Russell** | Mercedes | 368.0 pts | $27.8M | 22% |
| **L. Norris** | McLaren | 339.0 pts | $27.0M | 9% |
| **M. Verstappen** | Red Bull Racing | 333.0 pts | $27.3M | 17% |
| **C. Leclerc** | Ferrari | 331.0 pts | $24.0M | 27% |
| **O. Piastri** | McLaren | 228.0 pts | $24.1M | 9% |
| **L. Lawson** | Red Bull Racing | 184.0 pts | $15.1M | 3% |
| **F. Colapinto** | Alpine | 156.0 pts | $10.6M | 20% |
| **P. Gasly** | Alpine | 148.0 pts | $12.0M | 20% |

#### 🏢 Top 5 Constructors

| Team | Total fantasy pts | Value | Selected % |
| :--- | :--- | :--- | :--- |
| **Mercedes** | 1181.0 pts | $33.5M | 36% |
| **Ferrari** | 882.0 pts | $27.5M | 42% |
| **McLaren** | 742.0 pts | $31.9M | 10% |
| **Red Bull Racing** | 645.0 pts | $31.8M | 7% |
| **Racing Bulls** | 418.0 pts | $14.7M | 33% |

</details>


<details>
<summary><b>🏎️ 2025 Season — Round 24</b></summary>

#### 👤 Top 10 Drivers

| Driver | Team | Total fantasy pts | Value | Selected % |
| :--- | :--- | :--- | :--- | :--- |
| **M. Verstappen** | Red Bull Racing | 776.0 pts | $30.1M | 21% |
| **L. Norris** | McLaren | 707.0 pts | $30.3M | 23% |
| **O. Piastri** | McLaren | 644.0 pts | $25.1M | 35% |
| **G. Russell** | Mercedes | 580.0 pts | $23.7M | 12% |
| **C. Leclerc** | Ferrari | 407.0 pts | $23.0M | 14% |
| **L. Hamilton** | Ferrari | 391.0 pts | $21.9M | 11% |
| **K. Antonelli** | Mercedes | 311.0 pts | $18.1M | 21% |
| **O. Bearman** | Haas F1 Team | 206.0 pts | $9.3M | 43% |
| **A. Albon** | Williams | 198.0 pts | $12.6M | 27% |
| **E. Ocon** | Haas F1 Team | 177.0 pts | $7.9M | 22% |

#### 🏢 Top 5 Constructors

| Team | Total fantasy pts | Value | Selected % |
| :--- | :--- | :--- | :--- |
| **McLaren** | 1744.0 pts | $36.1M | 38% |
| **Red Bull Racing** | 1227.0 pts | $31.1M | 11% |
| **Mercedes** | 1185.0 pts | $28.4M | 19% |
| **Ferrari** | 1145.0 pts | $31.8M | 18% |
| **Williams** | 490.0 pts | $19.5M | 25% |

</details>


<details>
<summary><b>🏎️ 2024 Season — Round 24</b></summary>

#### 👤 Top 10 Drivers

| Driver | Team | Total fantasy pts | Value | Selected % |
| :--- | :--- | :--- | :--- | :--- |
| **M. Verstappen** | Red Bull Racing | 754.0 pts | $32.3M | 36% |
| **L. Norris** | McLaren | 695.0 pts | $27.5M | 30% |
| **C. Leclerc** | Ferrari | 684.0 pts | $26.1M | 31% |
| **O. Piastri** | McLaren | 584.0 pts | $25.7M | 19% |
| **C. Sainz** | Ferrari | 504.0 pts | $24.4M | 19% |
| **L. Hamilton** | Mercedes | 495.0 pts | $25.8M | 15% |
| **G. Russell** | Mercedes | 455.0 pts | $23.2M | 13% |
| **S. Perez** | Red Bull Racing | 319.0 pts | $23.2M | 8% |
| **F. Alonso** | Aston Martin | 173.0 pts | $15.3M | 28% |
| **K. Magnussen** | Haas F1 Team | 165.0 pts | $14.3M | 18% |

#### 🏢 Top 5 Constructors

| Team | Total fantasy pts | Value | Selected % |
| :--- | :--- | :--- | :--- |
| **McLaren** | 1506.0 pts | $27.0M | 27% |
| **Red Bull Racing** | 1421.0 pts | $29.7M | 22% |
| **Ferrari** | 1414.0 pts | $25.3M | 37% |
| **Mercedes** | 1146.0 pts | $25.1M | 15% |
| **Aston Martin** | 395.0 pts | $14.4M | 18% |

</details>


<details>
<summary><b>🏎️ 2023 Season — Round 22</b></summary>

#### 👤 Top 10 Drivers

| Driver | Team | Total fantasy pts | Value | Selected % |
| :--- | :--- | :--- | :--- | :--- |
| **M. Verstappen** | Red Bull Racing | 1014.0 pts | $30.0M | 65% |
| **S. Perez** | Red Bull Racing | 579.0 pts | $20.8M | 43% |
| **L. Hamilton** | Mercedes | 506.0 pts | $25.3M | 18% |
| **L. Norris** | McLaren | 438.0 pts | $19.8M | 25% |
| **F. Alonso** | Aston Martin | 403.0 pts | $15.8M | 77% |
| **C. Sainz** | Ferrari | 394.0 pts | $20.4M | 23% |
| **G. Russell** | Mercedes | 384.0 pts | $20.2M | 20% |
| **C. Leclerc** | Ferrari | 335.0 pts | $23.5M | 28% |
| **O. Piastri** | McLaren | 279.0 pts | $15.4M | 17% |
| **L. Stroll** | Aston Martin | 231.0 pts | $14.0M | 26% |

#### 🏢 Top 5 Constructors

| Team | Total fantasy pts | Value | Selected % |
| :--- | :--- | :--- | :--- |
| **Red Bull Racing** | 1847.0 pts | $29.7M | 56% |
| **Mercedes** | 1060.0 pts | $26.0M | 13% |
| **Ferrari** | 1007.0 pts | $25.0M | 23% |
| **McLaren** | 899.0 pts | $17.1M | 15% |
| **Aston Martin** | 757.0 pts | $13.4M | 68% |

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
<!-- LAST_CHECKED_START -->Last checked: 2026-09-20<!-- LAST_CHECKED_END -->

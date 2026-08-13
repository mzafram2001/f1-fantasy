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
│   └── workflows/
│       └── get_round_data.yml
│
├── data/
│   ├── 2023/
│   │    ├── round_01.json
│   │    ├── round_02.json
│   │    └── ...
│   ├── 2024/
│   │    ├── round_01.json
│   │    ├── round_02.json
│   │    └── ...
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

| Attribute | Type | Description | Format | Example |
| :--- | :--- | :--- | :--- | :--- |
| `Driver_Name` / `Team_Name` | `String` | Display name of the driver or team | Text | `"K. Antonelli"` / `"Mercedes"` |
| `Driver_Code` / `Team_Code` | `String` | Three-letter shorthand identifier (TLA) | Text | `"ANT"` / `"MER"` |
| `Team_Name` *(Drivers only)* | `String` | Constructor associated with the driver | Text | `"Mercedes"` |
| `Round_Fantasy_Points` | `Float` | Total fantasy points scored in the current round | Numeric | `55.0` |
| `Season_Fantasy_Points` | `Float` | Total cumulative fantasy points scored up to this round | Numeric | `305.0` |
| `Selected_Percentage` | `Float` | Player selection rate across fantasy teams | Numeric | `0.33` *(33%)* |
| `Value` | `Float` | Current asset price for the round (in $M) | Numeric | `24.7` |
| `Qualifying_Points` | `Float` | Fantasy points earned in qualifying | Numeric | `10.0` |
| `Sprint_Points` | `Float` | Fantasy points earned in sprint | Numeric | `0.0` |
| `Race_Points` | `Float` | Fantasy points earned in race | Numeric | `45.0` |

---

## 💻 Example of data

<!-- SEASONS_SUMMARY_START -->
<details open>
  <summary><b>🏎️ 2026 Season — Round 12 (Latest Data)</b></summary>
  <br>
  #### 👤 Top 5 Drivers
  | Driver | Team | Round Pts | Value | Selected % |
  | :--- | :--- | :--- | :--- | :--- |
  | **K. Antonelli** | Mercedes | 0.0 pts | $25.7M | 36% |
  | **L. Hamilton** | Ferrari | 0.0 pts | $25.0M | 20% |
  | **C. Leclerc** | Ferrari | 0.0 pts | $23.9M | 27% |
  | **G. Russell** | Mercedes | 0.0 pts | $27.9M | 22% |
  | **M. Verstappen** | Red Bull Racing | 0.0 pts | $27.6M | 17% |

  #### 🏢 Top 3 Constructors
  | Team | Round Pts | Value | Selected % |
  | :--- | :--- | :--- | :--- |
  | **Mercedes** | 0.0 pts | $32.6M | 35% |
  | **Ferrari** | 0.0 pts | $26.6M | 43% |
  | **McLaren** | 0.0 pts | $31.0M | 10% |
</details>

<details>
  <summary><b>🏎️ 2025 Season — Round 24 (Latest Data)</b></summary>
  <br>
  #### 👤 Top 5 Drivers
  | Driver | Team | Round Pts | Value | Selected % |
  | :--- | :--- | :--- | :--- | :--- |
  | **M. Verstappen** | Red Bull Racing | 46.0 pts | $30.1M | 21% |
  | **C. Leclerc** | Ferrari | 35.0 pts | $23.0M | 14% |
  | **L. Norris** | McLaren | 29.0 pts | $30.3M | 23% |
  | **O. Piastri** | McLaren | 28.0 pts | $25.1M | 35% |
  | **L. Hamilton** | Ferrari | 28.0 pts | $21.9M | 11% |

  #### 🏢 Top 3 Constructors
  | Team | Round Pts | Value | Selected % |
  | :--- | :--- | :--- | :--- |
  | **Ferrari** | 83.0 pts | $31.8M | 18% |
  | **McLaren** | 77.0 pts | $36.1M | 38% |
  | **Red Bull Racing** | 52.0 pts | $31.1M | 11% |
</details>

<details>
  <summary><b>🏎️ 2024 Season — Round 24 (Latest Data)</b></summary>
  <br>
  #### 👤 Top 5 Drivers
  | Driver | Team | Round Pts | Value | Selected % |
  | :--- | :--- | :--- | :--- | :--- |
  | **C. Leclerc** | Ferrari | 55.0 pts | $26.1M | 31% |
  | **L. Norris** | McLaren | 35.0 pts | $27.5M | 30% |
  | **L. Hamilton** | Mercedes | 33.0 pts | $25.8M | 15% |
  | **C. Sainz** | Ferrari | 27.0 pts | $24.4M | 19% |
  | **M. Verstappen** | Red Bull Racing | 23.0 pts | $32.3M | 36% |

  #### 🏢 Top 3 Constructors
  | Team | Round Pts | Value | Selected % |
  | :--- | :--- | :--- | :--- |
  | **Ferrari** | 82.0 pts | $25.3M | 37% |
  | **McLaren** | 65.0 pts | $27.0M | 27% |
  | **Mercedes** | 55.0 pts | $25.1M | 15% |
</details>

<details>
  <summary><b>🏎️ 2023 Season — Round 23 (Latest Data)</b></summary>
  <br>
  #### 👤 Top 5 Drivers
  | Driver | Team | Round Pts | Value | Selected % |
  | :--- | :--- | :--- | :--- | :--- |
  | **M. Verstappen** | Red Bull Racing | 47.0 pts | $30.0M | 0% |
  | **G. Russell** | Mercedes | 32.0 pts | $20.2M | 0% |
  | **S. Perez** | Red Bull Racing | 30.0 pts | $20.8M | 0% |
  | **C. Leclerc** | Ferrari | 29.0 pts | $23.5M | 0% |
  | **L. Norris** | McLaren | 22.0 pts | $19.8M | 0% |

  #### 🏢 Top 3 Constructors
  | Team | Round Pts | Value | Selected % |
  | :--- | :--- | :--- | :--- |
  | **Red Bull Racing** | 87.0 pts | $29.7M | 0% |
  | **McLaren** | 59.0 pts | $17.1M | 0% |
  | **Mercedes** | 51.0 pts | $26.0M | 0% |
</details>

<!-- SEASONS_SUMMARY_END -->

---

> [!CAUTION]
> **Disclaimer:** Data is collected from public sources. This repository is for educational and research purposes only. Not financial advice.

> [!TIP]
> **Want to help?**
> ⭐ Do you like this project? If you find this data useful, please give it a star! It helps me keep updating it.

---

*Created by Miguel Zafra*

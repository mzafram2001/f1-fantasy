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
<!-- SEASONS_SUMMARY_END -->

---

> [!CAUTION]
> **Disclaimer:** Data is collected from public sources. This repository is for educational and research purposes only. Not financial advice.

> [!TIP]
> **Want to help?**
> ⭐ Do you like this project? If you find this data useful, please give it a star! It helps me keep updating it.

---

*Created by Miguel Zafra*

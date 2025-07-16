# 💳 DeFi Wallet Credit Scoring – Aave V2

This project assigns a **credit score (0 to 1000)** to DeFi wallets based on behavioral analysis of their transaction history with the **Aave V2 protocol**. It combines **feature engineering, rule-based scoring, and machine learning** to build a transparent, explainable credit infrastructure suitable for decentralized lending.

---

## 📂 Folder Structure

```
wallet-credit-scoring/
├── data/
│   └── user_transactions.json     # Raw JSON input file (~87MB)
├── main.py                        # Main runner script (feature extraction, ML, visualization)
├── scoring_utils.py              # Feature extraction and scoring functions
├── analysis.md                   # In-depth report & analysis of scoring results
├── README.md                     # This file
├── requirements.txt              # Python dependencies
├── Output files:
│   ├── wallet_scores.csv
│   ├── score_distribution.png
│   ├── top_10_wallets.png
│   ├── feature_importance.png
│   ├── correlation_heatmap.png
│   ├── repayratio_vs_score.png
│   └── liquidation_vs_score.png
```

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/your-username/wallet-credit-scoring.git
cd wallet-credit-scoring
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add the data
Place the provided `user_transactions.json` inside the `data/` folder.

### 4. Run the pipeline
```bash
python main.py
```

---

## ⚙️ Features Engineered

- `num_deposit`, `num_borrow`, `num_repay`
- `repay_ratio` (repays ÷ borrows)
- `avg_amount`, `total_amount`
- `avg_time_gap` between transactions
- `liquidation_rate` and `num_unique_actions`

---

## 🧮 Scoring Logic

- Rule-based credit score (0–1000) from normalized behavior
- Penalty for liquidation behavior
- Machine Learning model (Random Forest) validates and learns scoring patterns
- Feature importance highlights most influential behaviors

---

## 📊 Visualizations

- **Score Histogram**: Distribution across buckets of 100
- **Top Wallets**: Highest scoring DeFi actors
- **Feature Importance**: What behaviors matter most
- **Heatmap**: Feature correlation with scores
- **Scatterplots**: Score vs repay ratio / liquidation

---

## 🤖 Machine Learning

- Trained `RandomForestRegressor` on engineered features
- **R² = 0.9901** | **RMSE = 6.15**
- Model confirms rule-based logic and can be deployed to infer credit scores dynamically

---

## 📈 Output Samples

| File                     | Description                         |
|--------------------------|-------------------------------------|
| `wallet_scores.csv`      | Final wallet credit scores          |
| `feature_importance.png` | ML insights into key score drivers  |
| `correlation_heatmap.png`| Feature inter-relationships         |
| `top_10_wallets.png`     | Top scorers overview                |
| `repayratio_vs_score.png`| Scatterplot: Repay behavior         |
| `liquidation_vs_score.png`| Scatterplot: Risky behavior         |

---

## 📄 Analysis Report

For full behavioral insights, scoring patterns, model performance, and conclusions, see [`analysis.md`](analysis.md).

---

## 👨‍💻 Author

**Rushikesh Kadam**  
Final Year B.Tech | Artificial Intelligence & Data Science  
AI Intern @ Zeru | GitHub: [github.com/rushikesh1912](https://github.com/rushikesh1912)

---

## 📜 License

MIT License. Free to use, extend, and integrate into DeFi infrastructure.

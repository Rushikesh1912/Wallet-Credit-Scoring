import json
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from scoring_utils import process_all_wallets
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Load JSON data
with open('data/user-wallet-transactions.json', 'r') as file:
    data = json.load(file)

print("✅ JSON data loaded successfully.")
print("🔍 Type of loaded data:", type(data))
print("🔍 Total transactions loaded:", len(data))
print("🔍 First transaction sample:", data[0])

# Group by wallet
wallet_dict = {}
for txn in data:
    wallet_id = txn['userWallet']
    if wallet_id not in wallet_dict:
        wallet_dict[wallet_id] = []
    wallet_dict[wallet_id].append(txn)

print("🔁 Grouped transactions into", len(wallet_dict), "wallets.")
print("🔧 Extracting features from all wallets...")

# Extract features
df = process_all_wallets(wallet_dict)

# Normalize features for rule-based scoring
scalable_cols = [
    'num_deposit',
    'num_borrow',
    'num_repay',
    'repay_ratio',
    'total_amount',
    'avg_amount',
    'num_unique_actions'
]

scaler = MinMaxScaler()
df_scaled = scaler.fit_transform(df[scalable_cols])
df_scaled = pd.DataFrame(df_scaled, columns=[
    col + "_scaled" for col in scalable_cols])

# Rule-based scoring
df['base_score'] = df_scaled.sum(axis=1) / len(scalable_cols) * 1000
df['score_penalty'] = df['liquidation_rate'] * 300
df['final_score'] = (df['base_score'] - df[
    'score_penalty']).clip(0, 1000).astype(int)

df.rename(columns={'wallet_id': 'userWallet'}, inplace=True)
df[['userWallet', 'final_score']].to_csv('wallet_scores.csv', index=False)
print("📁 Saved wallet scores to 'wallet_scores.csv'")

# Score distribution plot
plt.figure(figsize=(10, 5))
plt.hist(df['final_score'], bins=10, range=(
    0, 1000), edgecolor='black', color='skyblue')
plt.title('DeFi Wallet Credit Score Distribution')
plt.xlabel('Score (0 to 1000)')
plt.ylabel('Number of Wallets')
plt.grid(True)
plt.savefig('score_distribution.png')
plt.show()
print("📊 Score distribution saved as 'score_distribution.png'")

# Top 10 wallet score bar chart
top_wallets = df.sort_values('final_score', ascending=False).head(10)
plt.figure(figsize=(12, 6))
plt.bar(top_wallets['userWallet'], top_wallets['final_score'], color='green')
plt.xticks(rotation=45, ha='right', fontsize=8)
plt.title("Top 10 Wallets by Final Score")
plt.xlabel("Wallet ID")
plt.ylabel("Final Score")
plt.tight_layout()
plt.savefig("top_10_wallets.png")
plt.show()
print("📊 Top 10 wallet chart saved as 'top_10_wallets.png'")

ml_features = [
    'num_deposit',
    'num_borrow',
    'num_repay',
    'repay_ratio',
    'total_amount',
    'avg_amount',
    'avg_time_gap',
    'num_unique_actions',
    'liquidation_rate'
]

X = df[ml_features]
y = df['final_score']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("🤖 ML Model Performance:")
print(f"    RMSE: {rmse:.2f}")
print(f"    R² Score: {r2:.4f}")

# Feature importance plot
importances = model.feature_importances_
plt.figure(figsize=(10, 6))
plt.barh(ml_features, importances, color='orange')
plt.xlabel("Importance")
plt.title("Feature Importance for Credit Scoring (Random Forest)")
plt.tight_layout()
plt.savefig("feature_importance.png")
plt.show()
print("📈 Feature importance chart saved as 'feature_importance.png'")

# 1. Correlation heatmap
plt.figure(figsize=(10, 8))
corr_matrix = df[ml_features + ['final_score']].corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Feature Correlation Heatmap")
plt.tight_layout()
plt.savefig("correlation_heatmap.png")
plt.show()
print("📊 Heatmap saved as 'correlation_heatmap.png'")

# 2. Liquidation rate vs Final score
plt.figure(figsize=(8, 5))
sns.scatterplot(x=df['liquidation_rate'], y=df['final_score'], alpha=0.6)
plt.title("Liquidation Rate vs Final Score")
plt.xlabel("Liquidation Rate")
plt.ylabel("Final Score")
plt.grid(True)
plt.savefig("liquidation_vs_score.png")
plt.show()
print("📈 Saved 'liquidation_vs_score.png'")

# 3. Repay ratio vs Final score
plt.figure(figsize=(8, 5))
sns.scatterplot(x=df['repay_ratio'], y=df['final_score'], alpha=0.6)
plt.title("Repay Ratio vs Final Score")
plt.xlabel("Repay Ratio")
plt.ylabel("Final Score")
plt.grid(True)
plt.savefig("repayratio_vs_score.png")
plt.show()
print("📈 Saved 'repayratio_vs_score.png'")

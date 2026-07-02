# 📊 LPG Supply Chain & Distribution Analytics Dashboard

A simple application built with Python and Streamlit to analyze LPG cylinder deliveries, customer complaints, and global oil market risks in India.

---

## 🎯 1. Project Goal
Logistics bottlenecks and global energy shocks cause delivery delays and stock shortages across India. This project analyzes **504 operational records** to understand why these delays happen and how they impact customer satisfaction.

---

## 💡 2. Key Findings
* **The Customer Friction Link:** There is a near-perfect correlation of **0.98** between delivery delays and customer complaints. This proves that shipping delays are the main cause of customer complaints.
* **Top Market Risk:** LPG demand is heavily concentrated in a few specific states. Any shipping delay in these major hubs hurts company revenue immediately.
* **Global Risk Impact:** When international shipping routes (like the Strait of Hormuz) face restrictions, domestic Indian delivery delays spike to their highest levels.

---

## 🚀 3. How to Run the App

### Step 1: Install the required libraries
Open your terminal and run:
```bash
pip install streamlit pandas numpy matplotlib seaborn
```

### Step 2: Run the Streamlit application
```bash
streamlit run app.py
```

---

## 🏁 4. Actionable Business Recommendations
1. **Automate Customer Alerts:** Since delays directly cause customer complaints (0.98 correlation), send automated SMS updates to customers as soon as a delivery is delayed. 
2. **Buffer Top States:** Keep 60% of safety stock in high-demand states to prevent inventory shortages during peak seasons.
3. **Diversify Shipping Routes:** Create backup contracts with suppliers on India's eastern coast to protect the supply chain from Middle Eastern transport disruptions.

---

## 🛠️ Tools Used
* **Language:** Python
* **Dashboard:** Streamlit
* **Data & Charts:** Pandas, Matplotlib, Seaborn

---


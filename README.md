# ✈ Airline Ticket Pricing Analysis

This project provides an end-to-end **data analysis** of airline ticket pricing trends using Python.  
It includes **data cleaning, exploratory data analysis (EDA), visualizations, and key business insights** that can help optimize booking decisions.

---

## 📂 Project Files
- **airline_analysis.ipynb** → Full Python analysis notebook
- **airline_cleaned.csv** → Cleaned dataset ready for further use
- **requirements.txt** → Python dependencies

---

## 📊 Key Insights

### 1️⃣ Cheapest Booking Window
- Lowest prices are found **around 45–50 days before departure**.
- Prices rise sharply when fewer than 10 days remain.

### 2️⃣ Price by Travel Class
- **Economy median price:** ₹5,772  
- **Business median price:** ₹53,164  
- Business class is **~9× more expensive** than economy.

### 3️⃣ Airline-Wise Average Prices
- **Cheapest airlines:** IndiGo, Air Asia  
- **Most expensive airlines:** Vistara, Air India (Business class routes increase averages).

### 4️⃣ Route Pricing Trends
- **Most expensive route:** Chennai → Bangalore (~₹25,082 avg)  
- **Cheapest route:** Delhi → Mumbai (~₹4,250 avg)

### 5️⃣ Flight Duration vs Price
- Shorter flights (<2 hrs) are usually cheaper,  
  but some premium short routes break this trend due to demand.

---

## 🛠 Tech Stack
- **Python:** Pandas, NumPy, Matplotlib, Seaborn
- **Jupyter Notebook** for interactive analysis

---

## 🚀 How to Run
1. Clone this repository:
   ```bash
   git clone https://github.com/nishanthselvakumar1302/airline-ticket-pricing-analysis.git
   cd airline-ticket-pricing-analysis

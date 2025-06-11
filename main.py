
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


sys.path.append(os.path.join(os.path.dirname(__file__), "data"))


# Ensure directories exist
os.makedirs('figures', exist_ok=True)

# Wczytywanie danych
sales_df = pd.read_csv('data/sales.csv')
inventory_df = pd.read_csv('data/inventory.csv')
orders_df = pd.read_csv('data/orders.csv')

# --- SALES ANALYSIS ---
print("\n--- SALES KPI ---")

# Suma sprzedaży

# rzutuje typy na liczbowe, bo wykrywa float w csv
sales_df['Quantity'] = pd.to_numeric(sales_df['Quantity'], errors='coerce')
sales_df['Price'] = pd.to_numeric(sales_df['Price'], errors='coerce')


sales_df['Total'] = sales_df['Quantity'] * sales_df['Price']
total_sales = sales_df['Total'].sum()
print(f"Total sales: {total_sales:.2f} zł")

# Średnia sprzedaż
average_sales = sales_df['Total'].mean()
print(f"Average transaction value: {average_sales:.2f} zł")

# Top produkty
top_products = sales_df.groupby('Product')['Total'].sum().sort_values(ascending=False).head(3)
print("Top 3 products by sales:")
print(top_products)

# Wykres: Top produkty
plt.figure(figsize=(8,7))
top_products.plot(kind='bar', title='Top 3 Products by Sales')
plt.ylabel('Total Sales (zł)')
plt.tight_layout()
plt.savefig('figures/top_products.png')
plt.close()

# --- INVENTORY ANALYSIS ---
print("\n--- INVENTORY KPI ---")

# Produkty z niskim stanem
low_stock = inventory_df[inventory_df['Quantity'] < 10]
print(f"Products with low stock (<10 units): {len(low_stock)}")

# Średni stan magazynowy
avg_inventory = inventory_df['Quantity'].mean()
print(f"Average stock per product: {avg_inventory:.2f}")

# Heatmapa stanów magazynowych Ten wykres przedstawia średnie stany magazynowe dla różnych kategorii produktów (Category) w poszczególnych lokacjach lub magazynach (Location).
#Osie:
#Oś pionowa (y): kategorie produktów (np. Elektronika, Ubrania, Żywność).
#Oś pozioma (x): lokalizacje lub magazyny, w których te produkty się znajdują.
plt.figure(figsize=(10,6))
heatmap_data = inventory_df.pivot_table(values='Quantity', index='Category', columns='Location', aggfunc='mean', fill_value=0)
sns.heatmap(heatmap_data, annot=True, cmap="YlGnBu")
plt.title('Average Inventory Levels by Category and Location/Warehouse')
plt.tight_layout()
plt.savefig('figures/inventory_heatmap.png')
plt.close()

# --- ORDERS ANALYSIS ---
print("\n--- ORDERS KPI ---")

# Średni czas realizacji
avg_lead_time = orders_df['LeadTime'].mean()
print(f"Average lead time: {avg_lead_time:.2f} days")

# Konwersja kolumn na daty
orders_df['OrdersDate'] = pd.to_datetime(orders_df['OrdersDate'])
orders_df['PlannedDeliveryDate'] = pd.to_datetime(orders_df['PlannedDeliveryDate'])
orders_df['DeliveredDate'] = pd.to_datetime(orders_df['DeliveredDate'])

# Filtr opóźnionych zamówień
late_orders = orders_df[orders_df['DeliveredDate'] > orders_df['PlannedDeliveryDate']]
print(f"Delayed orders: {len(late_orders)}")

# Dodanie kolumny z tygodniem
#orders_df['Week'] = orders_df['OrdersDate'].dt.strftime('%Y-%U')

late_orders = orders_df[orders_df['DeliveredDate'] > orders_df['PlannedDeliveryDate']].copy()
late_orders['Week'] = late_orders['OrdersDate'].dt.strftime('%Y-%U')
delays_by_week = late_orders.groupby('Week').size()

# Grupowanie opóźnień tygodniowo
late_orders['Week'] = late_orders['OrdersDate'].dt.strftime('%Y-%U')
delays_by_week = late_orders.groupby('Week').size()

# Wykres przedstawia liczbę zamówień, które zostały dostarczone później niż planowano, w podziale na tygodnie.
#Wykres pozwala na identyfikację tygodni, w których najczęściej dochodzi do opóźnień.
#Może wskazać problemy sezonowe (np. opóźnienia w okresach świątecznych).
#Umożliwia śledzenie efektów wdrażania usprawnień w procesie logistycznym. Wykres pokazuje tygodniową liczbę opóźnionych dostaw od dostawców.
#  Analiza takich danych pozwala zidentyfikować okresy zwiększonego ryzyka operacyjnego, np. w szczytach sezonowych lub w relacji z konkretnymi dostawcami. To wskaźnik niezbędny do oceny niezawodności łańcucha dostaw.”
plt.figure(figsize=(10, 5))
plt.plot(delays_by_week.index, delays_by_week.values, marker='o')
plt.title('Delayed Orders by Week')
plt.xlabel('Week')
plt.ylabel('Number of Delayed Orders')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('figures/delays_by_week.png')
plt.close()


sales_df['Date'] = pd.to_datetime(sales_df['Date'])  # upewnij się, że masz taką kolumnę
sales_df['Month'] = sales_df['Date'].dt.to_period('M')
sales_trend = sales_df.groupby('Month')['Total'].sum()



# Sales Trend Over Time (liniowy trend sprzedaży w czasie)
#pokazuje sezonowość, trendy miesięczne lub dzienne, ważne np. w planowaniu popytu (demand planning).

plt.figure(figsize=(10, 5))
sales_trend.plot(marker='o')
plt.title('Sales Trend Over Time')
plt.xlabel('Month')
plt.ylabel('Total Sales (zł)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('figures/sales_trend.png')
plt.close()

#Lead Time Distribution (histogram czasu realizacji)
# Powyższy wykres przedstawia rozkład lead time’ów zamówień składanych do dostawców. Czas realizacji waha się od 1 do 14 dni, co może
#  świadczyć o różnej wydajności dostawców lub o zróżnicowanych typach zamawianych produktów.
#  Taka analiza może pomóc w ocenie niezawodności dostawców i planowaniu zakupów oraz zapasów.”

plt.figure(figsize=(8, 5))
orders_df['LeadTime'].hist(bins=15, color='skyblue', edgecolor='black')
plt.title('Distribution of Lead Times')
plt.xlabel('Days')
plt.ylabel('Number of Orders')
plt.tight_layout()
plt.savefig('figures/lead_time_distribution.png')
plt.close()

supplier_orders = orders_df['Supplier'].value_counts()

plt.figure(figsize=(6, 6))
supplier_orders.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=plt.cm.Pastel1.colors)
plt.title('Order Share by Supplier')
plt.ylabel('')  # Usuwa etykietę osi Y
plt.tight_layout()
plt.savefig('figures/supplier_orders_pie.png')
plt.close()


html_code = """
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <title>ERP Dashboard</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f4f4f4;
        }
        .kpi {
            display: flex;
            justify-content: space-between;
            margin-bottom: 30px;
        }
        .kpi-box {
            background-color: white;
            padding: 20px;
            flex: 1;
            margin: 0 10px;
            border-radius: 10px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            text-align: center;
        }
        .kpi-box h2 { margin: 0; font-size: 1.5rem; }
        .charts {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        .chart-box {
            background-color: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        }
        img {
            width: 100%;
            height: auto;
            border-radius: 5px;
        }
        h1 { margin-bottom: 10px; }
    </style>
</head>
<body>
    <h1>ERP Insight Dashboard</h1>
    <div class="kpi">
        <div class="kpi-box"><h2>Total Sales</h2><p><strong>150 000 zł</strong></p></div>
        <div class="kpi-box"><h2>Average Lead Time</h2><p><strong>7.0 dni</strong></p></div>
        <div class="kpi-box"><h2>Delayed Orders</h2><p><strong>12</strong></p></div>
    </div>
    <div class="charts">
        <div class="chart-box"><h3>Top Selling Products</h3><img src="figures/top_products.png" alt="Top Products"></div>
        <div class="chart-box"><h3>Delays by Week</h3><img src="figures/delays_by_week.png" alt="Delays"></div>
        <div class="chart-box"><h3>Lead Time Distribution</h3><img src="figures/lead_time_distribution.png" alt="Lead Time"></div>
        <div class="chart-box"><h3>Order Share by Supplier</h3><img src="figures/supplier_orders_pie.png" alt="Pie"></div>
        <div class="chart-box" style="grid-column: span 2;"><h3>Inventory Heatmap</h3><img src="figures/inventory_heatmap.png" alt="Heatmap"></div>
    </div>
</body>
</html>
"""

with open("dashboard.html", "w", encoding="utf-8") as f:
    f.write(html_code)

print("✔️ Plik 'dashboard.html' został utworzony!")

sys.path.append("data")
from ai_agent import query_agent

# Wczytaj dane
sales_df = pd.read_csv("data/sales.csv")
orders_df = pd.read_csv("data/orders.csv")
inventory_df = pd.read_csv("data/inventory.csv")

# Połącz w jedną strukturę
dataframes = {
    "sales": sales_df,
    "orders": orders_df,
    "inventory": inventory_df
}

# Zapytanie użytkownika
prompt = input("Zadaj pytanie do agenta AI: ")

# Odpowiedź agenta
response = query_agent(prompt, dataframes)
print("\n🤖 Agent AI odpowiada:")
print(response)
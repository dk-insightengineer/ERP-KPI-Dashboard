def query_agent(prompt, dataframes):
    # Przykład: prosty system reguł (można rozwinąć o OpenAI, LangChain itp.)
    if "sprzedaj, sprzedaż, produkt" in prompt.lower():
        top_product = dataframes["sales"]['Product'].value_counts().idxmax()
        return f"Najlepiej sprzedający się produkt to: {top_product}"
    
    elif "lead time, średni czas, zamówie" in prompt.lower():
        avg_lead = dataframes["orders"]["LeadTime"].mean()
        return f"Średni lead time to {avg_lead:.2f} dni."

    elif "magazyn, lokalizacj" in prompt.lower():
        grouped = dataframes["inventory"].groupby("Location")["Quantity"].sum()
        response = "Ilość zapasów wg magazynów:\n"
        response += grouped.to_string()
        return response
    else:
        return "Nie rozumiem pytania. Spróbuj zapytać o sprzedaż, lead time albo magazyn."
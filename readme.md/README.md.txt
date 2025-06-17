# ERP Insight Dashboard 📊

**Autorka:** Dorota K.  
**GitHub:** [dk-insightengineer](https://github.com/dk-insightengineer)  
**Cel projektu:** Zbudowanie interaktywnego pulpitu analitycznego ERP z uwzględnieniem AI.


Projekt typu proof-of-concept (PoC), którego celem jest symulacja działania prostego analitycznego dashboardu ERP przy użyciu języka Python. 
Narzędzie umożliwia analizę danych operacyjnych takich jak sprzedaż, lead time zamówień i stany magazynowe, bazując na załadowanych plikach CSV.

---

Funkcjonalności
- ✅ Analiza sprzedaży – identyfikacja najlepiej sprzedających się produktów
- ✅ Analiza lead time – średni czas realizacji zamówień
- ✅ Analiza zapasów – podsumowanie ilości zapasów wg lokalizacji magazynowych
- ✅ Moduł `query_agent` – interfejs do odpowiadania na pytania tekstowe w stylu prostego chatbota opartego o zalezności
- ✅ Wizualizacja danych – generowanie wykresów w folderze `figures`

---

 Struktura projektu
ERP-Insight-Bot/
│
├── data/ # Przykładowe dane ERP (sprzedaż, zapasy, zamówienia)
├── figures/ # Wygenerowane wykresy KPI
├── main.py # Główna logika projektu
├── agent.py # Prosty silnik zapytań tekstowych
├── README.md # Ten dokument
└── .gitignore # Ignorowane pliki

Jak to działa?

1. **Załaduj dane:** CSV-y w folderze `data/`
2. **Uruchom skrypt:** `python main.py`
3. **Zadawaj pytania:** Program odpowiada na pytania związane ze sprzedażą, stanami magazynowymi i lead time
4. **Zobacz wykresy:** Tworzone automatycznie i zapisywane w `figures/`


Przykładowe pytania, na które odpowiada `query_agent`

- *"Jaki produkt sprzedaje się najlepiej?"*  
- *"Jaki jest średni lead time zamówień?"*  
- *"Jakie są stany magazynowe w poszczególnych lokalizacjach?"*


Technologie
Python 3.12

Pandas – analiza danych

Matplotlib – wykresy

(planowane) OpenAI API / LangChain – automatyzacja odpowiedzi



Ten projekt jest częścią mojej ścieżki rozwojowej jako analityka danych z zainteresowaniem w stronę systemów ERP, automatyzacji i wizualizacji wskaźników KPI.
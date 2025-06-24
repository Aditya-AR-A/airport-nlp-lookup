
# ✈️ Airport Locator – NLP-based Nearest Airport Finder

A simple Python-based tool that takes a user-provided location (even noisy or unstructured) and returns the **nearest airport** using **spaCy-based NLP**, **geocoding**, and **distance filtering**.

---

## 📌 Features

- 🔍 Extracts location-related keywords using **spaCy NER** (`en_core_web_trf`)
- 🌍 Geocodes text to latitude/longitude using **Nominatim (OpenStreetMap)**
- 📏 Calculates **geodesic distances** to airports using **GeoPy**
- 🌐 Filters results by **country** to avoid cross-border mismatches
- 🧠 Handles vague or fuzzy input like `"near E75 Godrej, Gurgaon"`

---

## 🚀 Demo

```bash
$ python main.py

Enter a location or 'exit' to quit: gurgaon sector 56 near E block
The nearest airport is: Indira Gandhi International Airport (DEL) - New Delhi

Enter a location or 'exit' to quit: behind Burj Khalifa
The nearest airport is: Dubai International Airport (DXB) - Dubai
```

---

## 🛠️ Requirements

- Python 3.8+
- pip

### 📦 Dependencies

_Install all required packages via_:

```bash
pip install -r requirements.txt
```

_OR manually install_:

```bash
pip install pandas spacy geopy
python -m spacy download en_core_web_trf
```

---

## 📁 Project Structure

```folder
airport-nlp-lookup/
│
├── main.py                 # Entry point for the script
├── dataset/
│   └── airports.csv        # Cached cleaned airport data
├── requirements.txt        # All dependencies
└── README.md               # This file
```

---

## 🧠 How It Works

1. **Text Input:** User provides any text containing or implying a location.
2. **NER Extraction:** spaCy extracts geographic entities (`GPE`, `LOC`, `FAC`, etc.)
3. **Geocoding:** Each entity is passed to Nominatim to convert into coordinates.
4. **Filtering:** Airports are filtered by the same country (ISO alpha-2).
5. **Distance Calc:** Computes distance to each airport in the country.
6. **Nearest Match:** Returns the closest airport’s name, IATA code, and municipality.

---

## 📌 Limitations

- May fail for completely vague input (e.g., `"next to store"`)
- Geocoding depends on OpenStreetMap (rate-limited and network-dependent)
- Not meant for commercial-grade or high-volume production use

---

## 💡 Future Improvements

- Add support for reverse-geocoding addresses to neighborhoods
- Cache geocoding results to improve performance
- Integrate fuzzy address matching (like FuzzyWuzzy or RapidFuzz)
- Wrap into a REST API or Streamlit frontend

---

## 🧑‍💻 Author

- **Aditya Raj** – Data Scientist & NLP Engineer

---

## 📄 License

MIT License – free to use, modify, and distribute.

---

## 📚 References

- ✈️ **Airport Dataset**: [OurAirports Data](https://ourairports.com/data/) [Github Link](https://davidmegginson.github.io/ourairports-data/airports.csv)

- 🧠 **spaCy NLP**: [spaCy Industrial-Strength NLP](https://spacy.io)
- 🔍 **NER Transformer Model**: [`en_core_web_trf`](https://spacy.io/models/en#en_core_web_trf)
- 🌍 **Geocoding API**: [Nominatim - OpenStreetMap](https://nominatim.org/)
- 📏 **Distance Calculation**: [GeoPy - Geodesic Distance](https://geopy.readthedocs.io/)
- 📦 **Pandas**: [pandas.pydata.org](https://pandas.pydata.org/)
- 📦 **Python**: [Python 3.8+](https://www.python.org/)

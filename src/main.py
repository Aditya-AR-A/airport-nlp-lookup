"""
Airport Locator Module

This script provides a class `AirportLocator` for extracting location-based keywords
from text and identifying the nearest airport using geocoding and spatial distance computation.
"""

import os
import spacy
import pandas as pd
from geopy.distance import geodesic
from geopy.geocoders import Nominatim

# Ensure the transformer model is downloaded
if not spacy.util.is_package("en_core_web_trf"):
    print("Downloading spaCy model 'en_core_web_trf'...")
    spacy.cli.download("en_core_web_trf")
    print("Model downloaded successfully. Please restart the script.")
    exit(0)


class AirportLocator:
    """
    A class to extract location-related keywords and find the nearest airport
    based on textual input using NLP and geospatial distance.
    """

    def __init__(self):
        """
        Initializes the AirportLocator by loading and cleaning the airport dataset,
        setting up the geolocator, and loading the spaCy NLP pipeline.
        """
        self.df = self.get_and_clean_dataset()
        self.geolocator = Nominatim(user_agent="airport_locator")
        self.nlp = spacy.load("en_core_web_trf", disable=["parser", "tagger", "attribute_ruler", "lemmatizer"])

    def get_and_clean_dataset(self) -> pd.DataFrame:
        """
        Downloads and cleans the airport dataset by:
        - Removing missing IATA codes and coordinates
        - Filtering out non-commercial airports
        - Selecting relevant columns

        Returns:
            pd.DataFrame: Cleaned DataFrame of airports.
        """
        df = pd.read_csv("https://davidmegginson.github.io/ourairports-data/airports.csv")
        
        df = df.dropna(subset=["iata_code", "latitude_deg", "longitude_deg"])
        df = df[df['scheduled_service'] == 'yes']
        df = df[df['type'].isin(['large_airport', 'medium_airport', 'small_airport'])]
        df = df[["name", "iata_code", "latitude_deg", "longitude_deg", "municipality", "iso_country"]]
        
        df.columns = ["name", "iata_code", "latitude", "longitude", "municipality", "country"]

        os.makedirs("dataset", exist_ok=True)
        df.to_csv(os.path.join("dataset", "airports.csv"), index=False)
        return df

    def extract_location_keywords(self, text: str) -> list:
        """
        Extracts location-related named entities from the input text using spaCy.

        Args:
            text (str): Input sentence or phrase.

        Returns:
            list: A list of location-relevant keywords (e.g., cities, places, organizations).
        """
        doc = self.nlp(text)
        for ent in doc.ents:
            print(f" - {ent.text} ({ent.label_})")
        return [ent.text for ent in doc.ents if ent.label_ in ["GPE", "LOC", "FAC", "ORG"]]

    def geocode_location(self, text: str):
        """
        Geocodes the given text string into (latitude, longitude) coordinates using Nominatim.

        Args:
            text (str): Location string to be geocoded.

        Returns:
            tuple or None: Tuple of (latitude, longitude) if geocoding is successful, else None.
        """
        try:
            location = self.geolocator.geocode(text)
        except Exception as e:
            print(f"Error during geocoding '{text}': {e}")
            return None
        if location:
            print(f"Geocoded {text} to coordinates: ({location.latitude}, {location.longitude})")
            return (location.latitude, location.longitude)
        return None

    def get_nearest_airport(self, text: str):
        """
        Finds the nearest airport to the extracted or geocoded location from input text.

        Process:
        1. Extract location keywords using NER.
        2. Attempt geocoding for each candidate.
        3. Match the result against airports in the same country.
        4. Return the nearest one using geodesic distance.

        Args:
            text (str): Text input possibly containing a location.

        Returns:
            str or None: Formatted string with airport name, IATA code, and city; or None if no match is found.
        """
        keywords = self.extract_location_keywords(text)
        if not keywords:
            print("No location keywords found. Trying to geocode full text...")
            keywords = [text]

        for keyword in keywords:
            location = self.geolocator.geocode(keyword, addressdetails=True)
            if location:
                lat, lon = location.latitude, location.longitude
                country = location.raw.get("address", {}).get("country_code", "").upper()
                if not country:
                    print(f"Could not determine country for: {keyword}")
                    continue

                country_filtered_df = self.df[self.df["country"] == country].copy()
                country_filtered_df.loc[:, 'distance'] = country_filtered_df.apply(
                    lambda row: geodesic((lat, lon), (row['latitude'], row['longitude'])).km,
                    axis=1
                )
                nearest = country_filtered_df.loc[country_filtered_df['distance'].idxmin()]
                return f"{nearest['name']} ({nearest['iata_code']}) - {nearest['municipality']}"

            else:
                print(f"Could not geocode the location: {keyword}")
        return None


if __name__ == "__main__":
    locator = AirportLocator()
    while True:
        text = input("Enter a location or 'exit' to quit: ")
        if text.lower() == 'exit':
            break
        if not text.strip():
            print("Please enter a valid location.")
            continue
        nearest_airport = locator.get_nearest_airport(text)
        if nearest_airport:
            print(f"The nearest airport is: {nearest_airport}")
        else:
            print("No nearby airport found.")
        print('\n' + '-' * 40 + '\n')

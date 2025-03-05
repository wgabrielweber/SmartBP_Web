import os
import json
from configs_st import COLLECTION_NAME
from database_init import db

collection = db[COLLECTION_NAME]

def log_measure(new_data):
    """
    Append new data to the existing MongoDB document.
    Data is grouped by sensor parameters, with each measure numbered sequentially within its group.
    """
    try:
        # Find the existing document
        existing_doc = collection.find_one()

        if not existing_doc:
            # If no document exists, create a new one with the new data
            collection.insert_one(new_data)
            print("New document created in MongoDB.")
            return

        # Process each sensor parameter in the new data
        for sensor_param, data in new_data.items():
            # Ensure the sensor parameter exists in the document
            if sensor_param not in existing_doc:
                existing_doc[sensor_param] = {}

            # Get the existing measure count for the sensor parameter
            existing_count = len(existing_doc[sensor_param])

            # Add each new measure with a sequential key
            new_measures = {}
            for measure in data["measures"]:
                measure_key = f"measure_{existing_count + 1}"
                new_measures[measure_key] = measure
                existing_count += 1  # Increment count
            
            # Update only the specific sensor_param in MongoDB
            collection.update_one(
                {},  # Match any document (since there's only one)
                {"$set": {sensor_param: {**existing_doc[sensor_param], **new_measures}}}  
                # Merging new measures with existing ones
            )

        print("New measures successfully saved to MongoDB.")

    except Exception as e:
        print(f"Failed to save measure: {e}")

   
def load_measures():
    """
    Load all measures stored in MongoDB.
    Assumes the entire database is stored inside a single document.
    """
    try:
        doc = collection.find_one()
        if doc:
            return doc
        return {}  # Return empty dictionary if no data is found
    except Exception as e:
        print(f"Failed to load measures: {e}")
        return {}
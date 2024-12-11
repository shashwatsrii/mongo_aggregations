import os
import json
import logging
from pymongo import MongoClient

# Replace with your MongoDB Atlas connection string
MONGO_URI = "mongodb+srv://shashwatswork:mongodbaggregations@cluster0.d9gck.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Setup logging
logging.basicConfig(level=logging.INFO)

# Function to load a pipeline from a JSON file
def load_pipeline(file_name):
    try:
        with open(file_name, "r") as file:
            return json.load(file)
    except Exception as e:
        logging.error(f"Error loading pipeline from {file_name}: {e}")
        return None

# Function to execute an aggregation pipeline
def test_pipeline(question, pipeline):
    try:
        # Connect to MongoDB
        client = MongoClient(MONGO_URI)
        db = client["sample_mflix"]  # Database name
        collection = db["movies"]  # Collection name
        
        logging.info(f"Running pipeline for {question}")
        # Run the aggregation pipeline
        results = collection.aggregate(pipeline)
        
        logging.info(f"Results for {question}:")
        for result in results:
            logging.info(result)
    except Exception as e:
        logging.error(f"Error executing pipeline for {question}: {e}")
    finally:
        client.close()

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    for file_name in sorted(os.listdir(current_dir)):
        if file_name.endswith(".json"):
            logging.info(f"Found file: {file_name}")
            question = file_name.split(".")[0].capitalize()  
            file_path = os.path.join(current_dir, file_name)
            pipeline = load_pipeline(file_path)
            
            if pipeline:
                test_pipeline(question, pipeline)

if __name__ == "__main__":
    main()

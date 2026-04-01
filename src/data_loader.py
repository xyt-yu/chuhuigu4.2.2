import pandas as pd
import json

from sentence_transformers import SentenceTransformer

# Initialize the Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

class DataLoader:
    def __init__(self, data_frame):
        self.data_frame = data_frame

    def filter_data(self, salary=None, location=None, keywords=None):
        filtered_data = self.data_frame
        
        if salary:
            filtered_data = filtered_data[filtered_data['salary'] >= salary]
        
        if location:
            filtered_data = filtered_data[filtered_data['location'] == location]
        
        if keywords:
            filtered_data = filtered_data[filtered_data['keywords'].apply(lambda x: any(k in x for k in keywords))]
        
        return filtered_data

    def vectorize_data(self, text_column):
        return model.encode(text_column.tolist(), convert_to_tensor=True)

    def export_to_json(self, filepath):
        self.data_frame.to_json(filepath, orient='records', lines=True)

# Example usage
# df = pd.read_csv('data.csv')
# loader = DataLoader(df)
# filtered = loader.filter_data(salary=50000, location='New York', keywords=['Python', 'Data Science'])
# vectors = loader.vectorize_data(filtered['job_description'])
# loader.export_to_json('filtered_data.json')
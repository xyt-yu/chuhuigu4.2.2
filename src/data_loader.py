import json
from sentence_transformers import SentenceTransformer

class DataLoader:
    def __init__(self, json_path):
        self.json_path = json_path
        self.data = self.load_data()
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # Load a pre-trained SentenceTransformer model

    def load_data(self):
        with open(self.json_path, 'r') as file:
            return json.load(file)

    def filter_jobs(self, location=None, min_salary=None, keywords=None):
        filtered_jobs = self.data
        if location:
            filtered_jobs = [job for job in filtered_jobs if job.get('location') == location]
        if min_salary:
            filtered_jobs = [job for job in filtered_jobs if job.get('salary', 0) >= min_salary]
        if keywords:
            filtered_jobs = [job for job in filtered_jobs if any(keyword.lower() in job.get('description', '').lower() for keyword in keywords)]
        return filtered_jobs

    def vectorize_jobs(self, jobs):
        descriptions = [job['description'] for job in jobs]
        vectors = self.model.encode(descriptions)
        return vectors

    def export_to_json(self, filtered_jobs, export_path):
        with open(export_path, 'w') as file:
            json.dump(filtered_jobs, file, indent=4)

    def process_pipeline(self, location=None, min_salary=None, keywords=None, export_path='filtered_jobs.json'):
        filtered_jobs = self.filter_jobs(location, min_salary, keywords)
        vectors = self.vectorize_jobs(filtered_jobs)
        self.export_to_json(filtered_jobs, export_path)
        return filtered_jobs, vectors

# Example usage:
# loader = DataLoader('path/to/job_data.json')
# loader.process_pipeline(location='New York', min_salary=100000, keywords=['data scientist'])
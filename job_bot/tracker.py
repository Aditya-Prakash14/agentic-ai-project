import json
import os

class Tracker:
    """Manages deduplication across runs"""
    
    def __init__(self, filepath='tracker.json'):
        self.filepath = filepath
        self.data = self._load()
    
    def _load(self):
        """Load tracker from JSON file"""
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as f:
                return json.load(f)
        return {}
    
    def save(self):
        """Save tracker to JSON file"""
        with open(self.filepath, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def is_processed(self, url: str) -> bool:
        """Check if URL has already been processed"""
        return url in self.data
    
    def add_job(self, url: str, fit_score: int, proceeded: bool):
        """Record a processed job"""
        self.data[url] = {
            'fit_score': fit_score,
            'proceeded': proceeded
        }
    
    def get_all_jobs(self) -> dict:
        """Get all tracked jobs"""
        return self.data
    
    def get_proceeded_jobs(self) -> dict:
        """Get only jobs where proceed=true, sorted by fit_score"""
        proceeded = {url: data for url, data in self.data.items() if data['proceeded']}
        return dict(sorted(proceeded.items(), key=lambda x: x[1]['fit_score'], reverse=True))

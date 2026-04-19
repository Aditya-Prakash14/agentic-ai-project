import json
import os
import uuid

class Tracker:
    """Persistent job tracking system for Job Bot"""
    
    def __init__(self, filepath='tracker.json'):
        self.filepath = filepath
        self.data = self._load()
    
    def _load(self):
        """Load tracker from JSON file"""
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as f:
                return json.load(f)
        return {"results": [], "seen": {}, "applied": set()}
    
    def save(self):
        """Save tracker to JSON file"""
        data_to_save = {
            "results": self.data.get("results", []),
            "seen": self.data.get("seen", {}),
            "applied": list(self.data.get("applied", set()))
        }
        with open(self.filepath, 'w') as f:
            json.dump(data_to_save, f, indent=2)
    
    def _ensure_structure(self):
        """Ensure data structure has required keys"""
        if "results" not in self.data:
            self.data["results"] = []
        if "seen" not in self.data:
            self.data["seen"] = {}
        if "applied" not in self.data:
            self.data["applied"] = set()
    
    # Deduplication methods
    def has_seen(self, job_key: str) -> bool:
        """Check if job URL has been seen"""
        self._ensure_structure()
        return job_key in self.data.get("seen", {})
    
    def mark_seen(self, job_key: str, job_id: str = None):
        """Mark a job URL as seen"""
        self._ensure_structure()
        if "seen" not in self.data:
            self.data["seen"] = {}
        self.data["seen"][job_key] = job_id or str(uuid.uuid4())
        self.save()
    
    # Result management methods
    def add_result(self, job_data: dict):
        """Add or update a job result"""
        self._ensure_structure()
        job_id = job_data.get("id") or str(uuid.uuid4())
        job_data["id"] = job_id
        
        # Check if result exists
        existing = next((r for r in self.data["results"] if r.get("id") == job_id), None)
        if existing:
            existing.update(job_data)
        else:
            self.data["results"].append(job_data)
        
        self.save()
        return job_id
    
    def get_all(self) -> list:
        """Get all job results"""
        self._ensure_structure()
        return self.data.get("results", [])
    
    def get_by_id(self, job_id: str) -> dict:
        """Get a specific job result by ID"""
        self._ensure_structure()
        results = self.data.get("results", [])
        job = next((r for r in results if r.get("id") == job_id), None)
        if job:
            # Include applied status
            job["applied"] = job_id in self.data.get("applied", set())
        return job
    
    # Application tracking
    def mark_applied(self, job_id: str):
        """Mark a job as applied"""
        self._ensure_structure()
        if "applied" not in self.data:
            self.data["applied"] = set()
        self.data["applied"].add(job_id)
        self.save()
    
    def is_applied(self, job_id: str) -> bool:
        """Check if job has been applied to"""
        self._ensure_structure()
        return job_id in self.data.get("applied", set())
    
    # Result deletion
    def delete_result(self, job_id: str):
        """Delete a job result"""
        self._ensure_structure()
        self.data["results"] = [r for r in self.data.get("results", []) if r.get("id") != job_id]
        if "applied" in self.data:
            self.data["applied"].discard(job_id)
        self.save()
    
    # Utility methods
    def reset(self):
        """Clear all data"""
        self.data = {"results": [], "seen": {}, "applied": set()}
        self.save()
    
    def get_stats(self):
        """Get statistics"""
        self._ensure_structure()
        results = self.data.get("results", [])
        applied = self.data.get("applied", set())
        
        high_fit_count = len([r for r in results if r.get("fit_score", 0) >= 70])
        
        return {
            "total_jobs": len(results),
            "high_fit_jobs": high_fit_count,
            "applied_count": len(applied),
            "pending_count": len(results) - len(applied)
        }

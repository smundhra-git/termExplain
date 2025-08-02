"""
Cache Module for termExplain

Handles caching of error explanations to avoid repeated API calls.
"""

import json
import hashlib
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import logging

class ErrorCache:
    """Cache for storing error explanations locally."""
    
    def __init__(self, cache_dir: str = "history", max_age_days: int = 30):
        """
        Initialize the cache.
        
        Args:
            cache_dir: Directory to store cache files
            max_age_days: Maximum age of cache entries in days
        """
        self.cache_dir = cache_dir
        self.max_age_days = max_age_days
        self.cache_file = os.path.join(cache_dir, "error_logs.json")
        
        # Ensure cache directory exists
        os.makedirs(cache_dir, exist_ok=True)
        
        # Initialize logging - suppress INFO messages
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.WARNING)
        
        # Load existing cache
        self.cache_data = self._load_cache()
    
    def get(self, error_text: str) -> Optional[str]:
        """
        Get cached explanation for an error.
        
        Args:
            error_text: The error text to look up
            
        Returns:
            Cached explanation if found and not expired, None otherwise
        """
        error_hash = self._hash_error(error_text)
        
        if error_hash in self.cache_data:
            entry = self.cache_data[error_hash]
            
            # Check if entry is expired
            if self._is_expired(entry):
                self.logger.info(f"Cache entry expired for error: {error_text[:50]}...")
                del self.cache_data[error_hash]
                self._save_cache()
                return None
            
            self.logger.info(f"Cache hit for error: {error_text[:50]}...")
            return entry['explanation']
        
        return None
    
    def save(self, error_text: str, explanation: str):
        """
        Save an explanation to cache.
        
        Args:
            error_text: The error text
            explanation: The AI-generated explanation
        """
        error_hash = self._hash_error(error_text)
        
        entry = {
            'error_text': error_text,
            'explanation': explanation,
            'timestamp': datetime.now().isoformat(),
            'hash': error_hash
        }
        
        self.cache_data[error_hash] = entry
        self._save_cache()
        
        self.logger.info(f"Cached explanation for error: {error_text[:50]}...")
    
    def clear_expired(self) -> int:
        """
        Clear expired cache entries.
        
        Returns:
            Number of entries cleared
        """
        initial_count = len(self.cache_data)
        expired_keys = []
        
        for key, entry in self.cache_data.items():
            if self._is_expired(entry):
                expired_keys.append(key)
        
        for key in expired_keys:
            del self.cache_data[key]
        
        if expired_keys:
            self._save_cache()
            self.logger.info(f"Cleared {len(expired_keys)} expired cache entries")
        
        return len(expired_keys)
    
    def clear_all(self):
        """Clear all cache entries."""
        self.cache_data = {}
        self._save_cache()
        self.logger.info("Cleared all cache entries")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with cache statistics
        """
        total_entries = len(self.cache_data)
        expired_entries = sum(1 for entry in self.cache_data.values() if self._is_expired(entry))
        valid_entries = total_entries - expired_entries
        
        # Calculate cache size
        cache_size = os.path.getsize(self.cache_file) if os.path.exists(self.cache_file) else 0
        
        return {
            'total_entries': total_entries,
            'valid_entries': valid_entries,
            'expired_entries': expired_entries,
            'cache_size_bytes': cache_size,
            'cache_size_mb': round(cache_size / (1024 * 1024), 2)
        }
    
    def _hash_error(self, error_text: str) -> str:
        """
        Create a hash for the error text.
        
        Args:
            error_text: The error text to hash
            
        Returns:
            SHA-256 hash of the error text
        """
        return hashlib.sha256(error_text.encode('utf-8')).hexdigest()
    
    def _is_expired(self, entry: Dict[str, Any]) -> bool:
        """
        Check if a cache entry is expired.
        
        Args:
            entry: Cache entry dictionary
            
        Returns:
            True if expired, False otherwise
        """
        try:
            timestamp = datetime.fromisoformat(entry['timestamp'])
            expiry_date = timestamp + timedelta(days=self.max_age_days)
            return datetime.now() > expiry_date
        except (KeyError, ValueError):
            # If timestamp is invalid, consider it expired
            return True
    
    def _load_cache(self) -> Dict[str, Any]:
        """
        Load cache from file.
        
        Returns:
            Cache data dictionary
        """
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.logger.info(f"Loaded cache with {len(data)} entries")
                    return data
        except (json.JSONDecodeError, IOError) as e:
            self.logger.warning(f"Failed to load cache: {e}")
        
        return {}
    
    def _save_cache(self):
        """Save cache to file."""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache_data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            self.logger.error(f"Failed to save cache: {e}")
    
    def export_cache(self, output_file: str):
        """
        Export cache to a file.
        
        Args:
            output_file: Path to export cache to
        """
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache_data, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Exported cache to {output_file}")
        except IOError as e:
            self.logger.error(f"Failed to export cache: {e}")
    
    def import_cache(self, input_file: str):
        """
        Import cache from a file.
        
        Args:
            input_file: Path to import cache from
        """
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                imported_data = json.load(f)
            
            # Merge with existing cache
            self.cache_data.update(imported_data)
            self._save_cache()
            self.logger.info(f"Imported {len(imported_data)} entries from {input_file}")
        except (json.JSONDecodeError, IOError) as e:
            self.logger.error(f"Failed to import cache: {e}") 
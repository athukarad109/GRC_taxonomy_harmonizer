"""
Performance and configuration settings for the harmonization service
"""
import os
from typing import Dict, Any

class HarmonizationConfig:
    """Configuration for harmonization performance and behavior"""
    
    def __init__(self):
        # Clustering parameters
        self.clustering_eps = float(os.getenv("CLUSTERING_EPS", "0.4"))
        self.clustering_min_samples = int(os.getenv("CLUSTERING_MIN_SAMPLES", "2"))
        
        # LLM settings
        self.llm_model = os.getenv("LLM_MODEL", "llama2")
        self.llm_temperature = float(os.getenv("LLM_TEMPERATURE", "0.3"))
        self.llm_host = os.getenv("LLM_HOST", "http://localhost:11434")
        
        # Parallel processing
        self.max_workers = int(os.getenv("MAX_WORKERS", "4"))
        self.enable_parallel = os.getenv("ENABLE_PARALLEL", "true").lower() == "true"
        
        # Caching
        self.enable_embedding_cache = os.getenv("ENABLE_EMBEDDING_CACHE", "true").lower() == "true"
        self.max_cache_size = int(os.getenv("MAX_CACHE_SIZE", "1000"))
        
        # Performance modes
        self.default_fast_mode = os.getenv("DEFAULT_FAST_MODE", "false").lower() == "true"
        
        # Text processing
        self.max_description_length = int(os.getenv("MAX_DESCRIPTION_LENGTH", "200"))
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary for API responses"""
        return {
            "clustering_eps": self.clustering_eps,
            "clustering_min_samples": self.clustering_min_samples,
            "llm_model": self.llm_model,
            "llm_temperature": self.llm_temperature,
            "max_workers": self.max_workers,
            "enable_parallel": self.enable_parallel,
            "enable_embedding_cache": self.enable_embedding_cache,
            "default_fast_mode": self.default_fast_mode
        }

# Global config instance
config = HarmonizationConfig() 
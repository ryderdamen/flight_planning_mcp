import requests
from typing import Dict, List, Optional, Any
from datetime import datetime
import json


class ATISRetriever:
    """
    A class to retrieve ATIS (Automatic Terminal Information Service) data from the FAA Digital ATIS API.
    Provides Python bindings for all available endpoints.
    """
    
    def __init__(self, base_url: str = "https://datis.clowd.io/api"):
        """
        Initialize the ATISRetriever.
        
        Args:
            base_url: Base URL for the FAA Digital ATIS API
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'AviationWeatherMCP/1.0'
        })
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make a request to the API and handle common errors.
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
            
        Returns:
            API response as dictionary
            
        Raises:
            requests.RequestException: For network/HTTP errors
        """
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            # Try to parse as JSON first
            try:
                data = response.json()
                # Check for error response from the API
                if isinstance(data, dict) and "error" in data:
                    return {"error": data["error"], "status_code": response.status_code}
                
                # Ensure we always return a dictionary
                if isinstance(data, list):
                    return {"data": data, "count": len(data)}
                elif isinstance(data, dict):
                    return data
                else:
                    return {"data": data, "raw_value": str(data)}
            except json.JSONDecodeError:
                # Return as text if not JSON
                return {"raw_data": response.text}
                
        except requests.RequestException as e:
            return {"error": str(e), "status_code": getattr(e.response, 'status_code', None)}
    
    def get_stations(self) -> Dict[str, Any]:
        """
        Get a list of all airport identifiers that have a D-ATIS.
        
        Returns:
            List of airport identifiers with D-ATIS
        """
        return self._make_request("/stations")
    
    def get_all_atis(self) -> Dict[str, Any]:
        """
        Get D-ATIS data for all airports.
        
        Returns:
            D-ATIS data for all airports
        """
        return self._make_request("/all")
    
    def get_airport_atis(self, airport_id: str) -> Dict[str, Any]:
        """
        Get D-ATIS data for a specific airport.
        
        Args:
            airport_id: Airport identifier (e.g., "KLAX", "CYYZ")
            
        Returns:
            D-ATIS data for the specified airport
        """
        # Force capitalize the airport ID
        airport_id = airport_id.upper().strip()
        
        return self._make_request(f"/{airport_id}")
    
    def get_airport_atis_with_info(self, airport_id: str) -> Dict[str, Any]:
        """
        Get D-ATIS data for a specific airport with additional metadata.
        
        Args:
            airport_id: Airport identifier (e.g., "KLAX", "CYYZ")
            
        Returns:
            D-ATIS data with metadata for the specified airport
        """
        # Force capitalize the airport ID
        airport_id = airport_id.upper().strip()
        
        result = self.get_airport_atis(airport_id)
        
        # Add metadata
        if "error" not in result:
            result["metadata"] = {
                "airport_id": airport_id,
                "timestamp": datetime.now().isoformat(),
                "source": "FAA Digital ATIS API"
            }
        
        return result

import requests
from typing import Dict, List, Optional, Union, Any
from datetime import datetime
import json


class WeatherRetriever:
    """
    A class to retrieve aviation weather data from aviationweather.gov's API.
    Provides Python bindings for all available endpoints.
    """
    
    def __init__(self, base_url: str = "https://aviationweather.gov/api"):
        """
        Initialize the WeatherRetriever.
        
        Args:
            base_url: Base URL for the aviation weather API
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
    
    def get_metar(self, 
                  ids: Optional[str] = None,
                  format: str = "json",
                  taf: Optional[bool] = None,
                  hours: Optional[int] = None,
                  bbox: Optional[str] = None,
                  date: Optional[str] = None) -> Dict[str, Any]:
        """
        Get METAR (Meteorological Terminal Air Report) data.
        
        Args:
            ids: Station ID(s) - comma separated
            format: Output format (raw, json, geojson, xml, html)
            taf: Include TAF data
            hours: Hours back to search
            bbox: Geographic bounding box (lat0,lon0,lat1,lon1)
            date: Date in yyyymmdd_hhmm or yyyy-mm-ddThh:mm:ssZ format
            
        Returns:
            METAR data
        """
        params = {}
        if ids:
            params['ids'] = ids
        if format:
            params['format'] = format
        if taf is not None:
            params['taf'] = str(taf).lower()
        if hours:
            params['hours'] = hours
        if bbox:
            params['bbox'] = bbox
        if date:
            params['date'] = date
            
        return self._make_request("/data/metar", params)
    
    def get_taf(self,
                ids: Optional[str] = None,
                format: str = "json",
                metar: Optional[bool] = None,
                bbox: Optional[str] = None,
                time: Optional[str] = None,
                date: Optional[str] = None) -> Dict[str, Any]:
        """
        Get TAF (Terminal Aerodrome Forecast) data.
        
        Args:
            ids: Station ID(s) - comma separated
            format: Output format (raw, json, geojson, xml, html)
            metar: Include METAR data
            bbox: Geographic bounding box (lat0,lon0,lat1,lon1)
            time: Process time by valid or issue
            date: Date in yyyymmdd_hhmm or yyyy-mm-ddThh:mm:ssZ format
            
        Returns:
            TAF data
        """
        params = {}
        if ids:
            params['ids'] = ids
        if format:
            params['format'] = format
        if metar is not None:
            params['metar'] = str(metar).lower()
        if bbox:
            params['bbox'] = bbox
        if time:
            params['time'] = time
        if date:
            params['date'] = date
            
        return self._make_request("/data/taf", params)
    
    def get_pirep(self,
                  id: Optional[str] = None,
                  format: str = "raw",
                  raw: Optional[bool] = None,
                  age: Optional[int] = None,
                  distance: Optional[int] = None,
                  level: Optional[int] = None,
                  inten: Optional[str] = None,
                  date: Optional[str] = None) -> Dict[str, Any]:
        """
        Get PIREP (Pilot Report) data.
        
        Args:
            id: Station ID
            format: Output format (raw, json, geojson, xml)
            raw: Raw data flag
            age: Hours back to search
            distance: Distance in nautical miles
            level: Level ±3000' to search
            inten: Minimum intensity (lgt, mod, sev)
            date: Date in yyyymmdd_hhmm or yyyy-mm-ddThh:mm:ssZ format
            
        Returns:
            PIREP data
        """
        params = {}
        if id:
            params['id'] = id
        if format:
            params['format'] = format
        if raw is not None:
            params['raw'] = str(raw).lower()
        if age:
            params['age'] = age
        if distance:
            params['distance'] = distance
        if level:
            params['level'] = level
        if inten:
            params['inten'] = inten
        if date:
            params['date'] = date
            
        return self._make_request("/data/pirep", params)
    
    def get_airsigmet(self,
                      format: str = "json",
                      hazard: Optional[str] = None,
                      level: Optional[int] = None,
                      date: Optional[str] = None) -> Dict[str, Any]:
        """
        Get Domestic SIGMET data.
        
        Args:
            format: Output format (raw, json, xml)
            hazard: Hazard type (conv, turb, ice, ifr)
            level: Level ±3000' to search
            date: Date in yyyymmdd_hhmm or yyyy-mm-ddThh:mm:ssZ format
            
        Returns:
            Domestic SIGMET data
        """
        params = {}
        if format:
            params['format'] = format
        if hazard:
            params['hazard'] = hazard
        if level:
            params['level'] = level
        if date:
            params['date'] = date
            
        return self._make_request("/data/airsigmet", params)
    
    def get_isigmet(self,
                    format: str = "json",
                    hazard: Optional[str] = None,
                    level: Optional[int] = None,
                    date: Optional[str] = None) -> Dict[str, Any]:
        """
        Get International SIGMET data.
        
        Args:
            format: Output format (raw, json, xml)
            hazard: Hazard type (turb, ice)
            level: Level ±3000' to search
            date: Date in yyyymmdd_hhmm or yyyy-mm-ddThh:mm:ssZ format
            
        Returns:
            International SIGMET data
        """
        params = {}
        if format:
            params['format'] = format
        if hazard:
            params['hazard'] = hazard
        if level:
            params['level'] = level
        if date:
            params['date'] = date
            
        return self._make_request("/data/isigmet", params)
    
    def get_gairmet(self,
                    type: Optional[str] = None,
                    format: str = "decoded",
                    hazard: Optional[str] = None,
                    date: Optional[str] = None) -> Dict[str, Any]:
        """
        Get US Graphical AIRMET data.
        
        Args:
            type: Product type (sierra, tango, zulu)
            format: Output format (decoded, json, geojson, xml)
            hazard: Hazard type (turb-hi, turb-lo, llws, sfc_wind, ifr, mtn_obs, ice, fzlvl)
            date: Date in yyyymmdd_hhmm format
            
        Returns:
            G-AIRMET data
        """
        params = {}
        if type:
            params['type'] = type
        if format:
            params['format'] = format
        if hazard:
            params['hazard'] = hazard
        if date:
            params['date'] = date
            
        return self._make_request("/data/gairmet", params)
    
    def get_cwa(self,
                hazard: Optional[str] = None,
                date: Optional[str] = None) -> Dict[str, Any]:
        """
        Get Center Weather Advisories.
        
        Args:
            hazard: Hazard type (ts, turb, ice, ifr, pcpn, unk)
            date: Date in yyyymmdd_hhmm format
            
        Returns:
            CWA data
        """
        params = {}
        if hazard:
            params['hazard'] = hazard
        if date:
            params['date'] = date
            
        return self._make_request("/data/cwa", params)
    
    def get_windtemp(self,
                     region: str = "us",
                     level: Optional[str] = None,
                     fcst: Optional[str] = None) -> Dict[str, Any]:
        """
        Get Wind/Temperature Point Data.
        
        Args:
            region: Region (us, bos, mia, chi, dfw, slc, sfo, alaska, hawaii, other_pac)
            level: Level (low, high)
            fcst: Forecast cycle (06, 12, 24)
            
        Returns:
            Wind/Temperature data
        """
        params = {'region': region}
        if level:
            params['level'] = level
        if fcst:
            params['fcst'] = fcst
            
        return self._make_request("/data/windtemp", params)
    
    def get_areafcst(self, region: str) -> Dict[str, Any]:
        """
        Get US Area Forecasts.
        
        Args:
            region: Region (aknorth, akcentral, akaleutian, aksouth, aksouthwest, aksoutheast, akpanhandle)
            
        Returns:
            Area forecast data
        """
        return self._make_request("/data/areafcst", {'region': region})
    
    def get_fcstdisc(self,
                     cwa: Optional[str] = None,
                     type: str = "afd") -> Dict[str, Any]:
        """
        Get US Forecast Discussions.
        
        Args:
            cwa: County Warning Area (WFO)
            type: Type of output (afd, af)
            
        Returns:
            Forecast discussion data
        """
        params = {'type': type}
        if cwa:
            params['cwa'] = cwa
            
        return self._make_request("/data/fcstdisc", params)
    
    def get_mis(self, loc: Optional[str] = None) -> Dict[str, Any]:
        """
        Get Meteorological Information Statements.
        
        Args:
            loc: CWSU location
            
        Returns:
            MIS data
        """
        params = {}
        if loc:
            params['loc'] = loc
            
        return self._make_request("/data/mis", params)
    
    def get_stationinfo(self,
                        ids: Optional[str] = None,
                        bbox: Optional[str] = None,
                        format: str = "json") -> Dict[str, Any]:
        """
        Get station information.
        
        Args:
            ids: Station ID(s) - comma separated
            bbox: Geographic bounding box (lat0,lon0,lat1,lon1)
            format: Output format (raw, json, geojson, xml)
            
        Returns:
            Station information
        """
        params = {'format': format}
        if ids:
            params['ids'] = ids
        if bbox:
            params['bbox'] = bbox
            
        return self._make_request("/data/stationinfo", params)
    
    def get_airport(self,
                    ids: Optional[str] = None,
                    bbox: Optional[str] = None,
                    format: str = "json") -> Dict[str, Any]:
        """
        Get airport information.
        
        Args:
            ids: Station ID(s) - comma separated
            bbox: Geographic bounding box (lat0,lon0,lat1,lon1)
            format: Output format (decoded, json, geojson)
            
        Returns:
            Airport information
        """
        params = {'format': format}
        if ids:
            params['ids'] = ids
        if bbox:
            params['bbox'] = bbox
            
        return self._make_request("/data/airport", params)
    
    def get_navaid(self,
                   ids: Optional[str] = None,
                   bbox: Optional[str] = None,
                   format: str = "json") -> Dict[str, Any]:
        """
        Get navigational aid information.
        
        Args:
            ids: 5-letter Fix ID(s) - comma separated
            bbox: Geographic bounding box (lat0,lon0,lat1,lon1)
            format: Output format (raw, json, geojson)
            
        Returns:
            Navigational aid information
        """
        params = {'format': format}
        if ids:
            params['ids'] = ids
        if bbox:
            params['bbox'] = bbox
            
        return self._make_request("/data/navaid", params)
    
    def get_fix(self,
                ids: Optional[str] = None,
                bbox: Optional[str] = None,
                format: str = "json") -> Dict[str, Any]:
        """
        Get navigational fix information.
        
        Args:
            ids: 5-letter Fix ID(s) - comma separated
            bbox: Geographic bounding box (lat0,lon0,lat1,lon1)
            format: Output format (raw, json, geojson)
            
        Returns:
            Navigational fix information
        """
        params = {'format': format}
        if ids:
            params['ids'] = ids
        if bbox:
            params['bbox'] = bbox
            
        return self._make_request("/data/fix", params)
    
    def get_feature(self,
                    bbox: Optional[str] = None,
                    format: str = "json") -> Dict[str, Any]:
        """
        Get additional geographic features.
        
        Args:
            bbox: Geographic bounding box (lat0,lon0,lat1,lon1)
            format: Output format (raw, json, geojson)
            
        Returns:
            Geographic feature information
        """
        params = {'format': format}
        if bbox:
            params['bbox'] = bbox
            
        return self._make_request("/data/feature", params)
    
    def get_obstacle(self,
                     bbox: Optional[str] = None,
                     format: str = "json") -> Dict[str, Any]:
        """
        Get aviation obstacle information.
        
        Args:
            bbox: Geographic bounding box (lat0,lon0,lat1,lon1)
            format: Output format (raw, json, geojson)
            
        Returns:
            Obstacle information
        """
        params = {'format': format}
        if bbox:
            params['bbox'] = bbox
            
        return self._make_request("/data/obstacle", params)
    
    def get_weather_summary(self, 
                           station_ids: List[str],
                           include_taf: bool = True,
                           hours_back: int = 2) -> Dict[str, Any]:
        """
        Get a comprehensive weather summary for multiple stations.
        
        Args:
            station_ids: List of station IDs
            include_taf: Whether to include TAF data
            hours_back: Hours back to search for METAR data
            
        Returns:
            Comprehensive weather summary
        """
        ids_str = ','.join(station_ids)
        
        # Get METAR data
        metar_data = self.get_metar(
            ids=ids_str,
            format="json",
            taf=include_taf,
            hours=hours_back
        )
        
        # Get TAF data if requested
        taf_data = None
        if include_taf:
            taf_data = self.get_taf(
                ids=ids_str,
                format="json",
                metar=False
            )
        
        # Get station information
        station_info = self.get_stationinfo(ids=ids_str, format="json")
        
        return {
            "metar": metar_data,
            "taf": taf_data,
            "station_info": station_info,
            "timestamp": datetime.now().isoformat(),
            "stations_requested": station_ids
        }
    
    def get_area_weather(self,
                         bbox: str,
                         include_taf: bool = True,
                         include_sigmet: bool = True) -> Dict[str, Any]:
        """
        Get comprehensive weather data for a geographic area.
        
        Args:
            bbox: Geographic bounding box (lat0,lon0,lat1,lon1)
            include_taf: Whether to include TAF data
            include_sigmet: Whether to include SIGMET data
            
        Returns:
            Area weather data
        """
        # Get METAR data for the area
        metar_data = self.get_metar(
            bbox=bbox,
            format="json",
            taf=include_taf
        )
        
        # Get TAF data if requested
        taf_data = None
        if include_taf:
            taf_data = self.get_taf(
                bbox=bbox,
                format="json",
                metar=False
            )
        
        # Get SIGMET data if requested
        sigmet_data = None
        if include_sigmet:
            sigmet_data = self.get_airsigmet(format="json")
        
        # Get station information for the area
        station_info = self.get_stationinfo(bbox=bbox, format="json")
        
        return {
            "metar": metar_data,
            "taf": taf_data,
            "sigmet": sigmet_data,
            "station_info": station_info,
            "bbox": bbox,
            "timestamp": datetime.now().isoformat()
        }

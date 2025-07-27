from fastmcp import FastMCP
from typing import List, Optional, Dict, Any
import os
from datetime import datetime
from starlette.responses import JSONResponse
from weather import WeatherRetriever
from atis import ATISRetriever


def ensure_dict_response(result: Any) -> Dict[str, Any]:
    """
    Ensure that the result is always returned as a dictionary for MCP tools.
    
    Args:
        result: The result from the weather API
        
    Returns:
        A dictionary representation of the result
    """
    if isinstance(result, list):
        return {"data": result, "count": len(result)}
    elif isinstance(result, dict):
        return result
    else:
        return {"data": result, "raw_value": str(result)}


mcp = FastMCP(
    name="aviation-weather-mcp-server",
    instructions="A server for getting aviation weather data from aviationweather.gov's API and ATIS data from the FAA Digital ATIS API."
)
weather_retriever = WeatherRetriever()
atis_retriever = ATISRetriever()


@mcp.custom_route("/mcp/", methods=["GET"])
async def mcp_probe(request):
    return JSONResponse(content={"ok": True})


@mcp.tool()
def get_metar_data(
    station_id: str,
    format: str = "json",
    hours_back: Optional[int] = None,
    date: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get METAR (Meteorological Terminal Air Report) data for a single aviation weather station.
    
    Args:
        station_id: Single station ID (e.g., "CYYZ", "KJFK")
        format: Output format (raw, json, geojson, xml, html)
        hours_back: Hours back to search for historical data
        date: Date in yyyymmdd_hhmm or yyyy-mm-ddThh:mm:ssZ format
    """
    # Force capitalize the station ID
    station_id = station_id.upper().strip()
    
    result = weather_retriever.get_metar(
        ids=station_id,
        format=format,
        taf=False,  # Never include TAF in METAR calls
        hours=hours_back,
        date=date
    )
    
    return ensure_dict_response(result)


@mcp.tool()
def get_taf_data(
    station_id: str,
    format: str = "json",
    time: Optional[str] = None,
    date: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get TAF (Terminal Aerodrome Forecast) data for a single aviation weather station.
    
    Args:
        station_id: Single station ID (e.g., "CYYZ", "KJFK")
        format: Output format (raw, json, geojson, xml, html)
        time: Process time by "valid" or "issue"
        date: Date in yyyymmdd_hhmm or yyyy-mm-ddThh:mm:ssZ format
    """
    # Force capitalize the station ID
    station_id = station_id.upper().strip()
    
    result = weather_retriever.get_taf(
        ids=station_id,
        format=format,
        metar=False,  # Never include METAR in TAF calls
        time=time,
        date=date
    )
    
    return ensure_dict_response(result)


@mcp.tool()
def get_pirep_data(
    station_id: Optional[str] = None,
    format: str = "raw",
    age: Optional[int] = None,
    distance: Optional[int] = None,
    level: Optional[int] = None,
    intensity: Optional[str] = None,
    date: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get PIREP (Pilot Report) data for pilot weather reports.
    
    Args:
        station_id: Station ID for the report
        format: Output format (raw, json, geojson, xml)
        age: Hours back to search
        distance: Distance in nautical miles
        level: Level ±3000' to search
        intensity: Minimum intensity (lgt, mod, sev)
        date: Date in yyyymmdd_hhmm or yyyy-mm-ddThh:mm:ssZ format
    """
    result = weather_retriever.get_pirep(
        id=station_id,
        format=format,
        age=age,
        distance=distance,
        level=level,
        inten=intensity,
        date=date
    )
    
    return ensure_dict_response(result)


@mcp.tool()
def get_airport_information(
    airport_id: str,
    format: str = "json"
) -> Dict[str, Any]:
    """
    Get information about a single airport.
    
    Args:
        airport_id: Single airport ID (e.g., "CYYZ", "KJFK")
        format: Output format (decoded, json, geojson)
    """
    # Force capitalize the airport ID
    airport_id = airport_id.upper().strip()
    
    result = weather_retriever.get_airport(
        ids=airport_id,
        format=format
    )
    return ensure_dict_response(result)


@mcp.tool()
def get_atis_data(
    airport_id: str
) -> Dict[str, Any]:
    """
    Get ATIS (Automatic Terminal Information Service) data for a specific airport.
    
    Args:
        airport_id: Airport identifier (e.g., "KLAX", "CYYZ", "KJFK")
    """
    # Force capitalize the airport ID
    airport_id = airport_id.upper().strip()
    
    result = atis_retriever.get_airport_atis_with_info(airport_id)
    return ensure_dict_response(result)


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)

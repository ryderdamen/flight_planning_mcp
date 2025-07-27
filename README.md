# Aviation MCP Server
An MCP (Model Context Protocol) server for retrieving Aviation weather data from aviationweather.gov's data API.

**Important:** This is an experimental project and should not be relied upon for flight planning or mission critical situations. This server is designed for experimental and entertainment purposes only.

---

## Tools & Features
The Aviation Weather MCP Server provides the following tools for accessing aviation weather data:

### Weather Data Tools
- **`get_metar_data`** - Get METAR (Meteorological Terminal Air Report) data for a single aviation weather station
  - Parameters: `station_id` (e.g., "CYYZ", "KJFK"), `format` (json/raw/geojson/xml/html), `hours_back`, `date`
  
- **`get_taf_data`** - Get TAF (Terminal Aerodrome Forecast) data for a single aviation weather station
  - Parameters: `station_id`, `format` (json/raw/geojson/xml/html), `time` (valid/issue), `date`
  
- **`get_pirep_data`** - Get PIREP (Pilot Report) data for pilot weather reports
  - Parameters: `station_id`, `format` (raw/json/geojson/xml), `age`, `distance`, `level`, `intensity`, `date`
  
- **`get_airport_information`** - Get information about a single airport
  - Parameters: `airport_id`, `format` (decoded/json/geojson)

### ATIS (Automatic Terminal Information Service) Tools
- **`get_atis_data`** - Get ATIS data for a specific airport
  - Parameters: `airport_id` (e.g., "KLAX", "CYYZ", "KJFK")

### Data Sources
- **Weather Data**: Sourced from aviationweather.gov's comprehensive weather API
- **ATIS Data**: Sourced from the FAA Digital ATIS API via datis.clowd.io

## Local Development

### Prerequisites
- Python 3.8+
- Docker and Docker Compose (for containerized development)

### Running Locally

#### Docker Development
```bash
# Build and run with Docker Compose
make build
make run

# Or directly with docker-compose
docker-compose up --build
```

The server will be available at `http://localhost:8000`

### Testing Your MCP Server

#### 1. Test with Claude Desktop
1. Add the MCP server configuration to your Claude Desktop config file:
   ```json
   {
     "mcpServers": {
       "aviation-mcp": {
         "command": "npx",
         "args": [
           "mcp-remote",
           "http://localhost:8000/mcp/",
           "--allow-http"
         ]
       }
     }
   }
   ```

2. Restart Claude Desktop
3. Ask Claude to use the aviation weather tools, for example:
   - "What runway is in use at Newark Liberty?"
   - "What's Toronto pearson's altimeter?"
   - "Current atis at LAX"

#### 2. Test with MCP Inspector
1. Install MCP Inspector: `npm install -g @modelcontextprotocol/inspector`
2. Run the inspector: `mcp-inspector`
3. Connect to your server at `http://localhost:8000/mcp/`
4. Explore and test all available tools through the inspector interface

---

## Configuration Examples

### Claude Desktop Configuration
Add this to your Claude Desktop config file (typically located at `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "aviation-mcp": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "http://localhost:8000/mcp/",
        "--allow-http"
      ]
    }
  }
}
```

## License

This project is for experimental and educational purposes only. Please ensure compliance with aviationweather.gov's terms of service when using this tool.

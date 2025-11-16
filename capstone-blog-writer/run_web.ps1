# Wrapper script to run ADK web with environment variables set
# This script loads the .env file and runs the web server

# Load .env file
$envFile = Join-Path (Get-Location) ".env"
if (Test-Path $envFile) {
    Get-Content $envFile | ForEach-Object {
        if ($_ -match '^\s*([^#=]+)=(.*)$') {
            $key = $matches[1].Trim()
            $value = $matches[2].Trim()
            [System.Environment]::SetEnvironmentVariable($key, $value, "Process")
            Write-Host "Loaded env: $key"
        }
    }
}

# Set environment variables explicitly
$env:GOOGLE_GENAI_USE_VERTEXAI = "False"
$env:GOOGLE_API_KEY = "AIzaSyCKXY6XAOUcd67_Ly3-IZwikj3_8RV_udc"

# Run ADK web server
Write-Host "Starting ADK web server on http://127.0.0.1:8000"
uv run adk web

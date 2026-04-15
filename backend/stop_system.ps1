Write-Host "Stopping all services..."

# Stop Mosquitto
net stop mosquitto 2>$null
Get-Process mosquitto -ErrorAction SilentlyContinue | Stop-Process -Force

# Stop backend & flask safely
Get-Process python -ErrorAction SilentlyContinue | Where-Object {
  $_.Path -like "*main.py*" -or $_.Path -like "*flask_app.py*"
} | Stop-Process -Force

# Stop ngrok
Get-Process ngrok -ErrorAction SilentlyContinue | Stop-Process -Force

Write-Host "All services stopped."

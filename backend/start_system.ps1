Write-Host "Starting all services..."

# -----------------------------
# START MOSQUITTO (FIXED)
# -----------------------------
Write-Host "Starting Mosquitto..."

$mosqCmd = @"
`$host.UI.RawUI.WindowTitle='MQTT';
cd '$PSScriptRoot';
mosquitto -c mosquitto.conf -v
"@

$mosqEncoded = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($mosqCmd))

Start-Process powershell -ArgumentList "-NoExit", "-EncodedCommand", $mosqEncoded -PassThru

Start-Sleep -Seconds 2

# -----------------------------
# MOVE TO PROJECT DIR
# -----------------------------
cd $PSScriptRoot

# -----------------------------
# START BACKEND
# -----------------------------
$backendCmd = @"
`$host.UI.RawUI.WindowTitle='BACKEND';
cd '$PSScriptRoot';
if (Test-Path '.\venv\Scripts\activate') { .\venv\Scripts\activate }
python main.py
"@

$backendEncoded = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($backendCmd))

Start-Process powershell -ArgumentList "-NoExit", "-EncodedCommand", $backendEncoded -PassThru

# -----------------------------
# START FLASK
# -----------------------------
$flaskCmd = @"
`$host.UI.RawUI.WindowTitle='FLASK';
cd '$PSScriptRoot';
if (Test-Path '.\venv\Scripts\activate') { .\venv\Scripts\activate }
python flask_app.py
"@

$flaskEncoded = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($flaskCmd))

Start-Process powershell -ArgumentList "-NoExit", "-EncodedCommand", $flaskEncoded -PassThru

# -----------------------------
# START NGROK
# -----------------------------
Write-Host "Starting ngrok..."

Start-Process powershell -ArgumentList "-NoExit", "-Command", "
title NGROK;
ngrok http 5000
"

Write-Host "All services started!"

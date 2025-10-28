FocusProxy - Real-time Activity Monitoring

A system that captures screen activity, analyzes it with Azure OpenAI Vision, and reports activity state to a server for remote monitoring.

## Components

- **screen_capture.py**: Captures screenshots of the screen
- **activity_analyzer.py**: Analyzes screenshots using Azure OpenAI Vision API to determine activity state
- **monitor.py**: Automated service that captures, analyzes, and POSTs activity every 5 minutes
- **server.py**: Flask server that receives and serves activity state

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your Azure OpenAI credentials:
```env
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com
SERVER_URL=http://localhost:8080
```

## Usage

### Run the server
```bash
python server.py
```

### Run the monitor (captures every 5 minutes)
```bash
python monitor.py
```

The monitor will:
1. Capture a screenshot
2. Analyze it using Azure OpenAI Vision
3. POST the activity state to the server
4. Repeat every 5 minutes

### Manual analysis
```bash
python inference/activity_analyzer.py
```

### Manual capture
```bash
python inference/screen_capture.py
```

## Activity Detection

The system analyzes screenshots and returns one of these states:
- reading
- writing  
- coding
- browsing
- watching
- chatting
- idle

These states are based on what application/website the user is using and their apparent level of focus.
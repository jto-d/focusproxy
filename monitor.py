import os
import time
import mss
from datetime import datetime
from io import BytesIO
from PIL import Image
import requests
from inference.activity_analyzer import ActivityAnalyzer
from inference.screen_capture import capture_once, timestamp
from dotenv import load_dotenv

load_dotenv()

class MonitorService:
    def __init__(self, screenshots_dir: str = "screenshots"):
        self.screenshots_dir = screenshots_dir
        self.api_key = os.getenv('AZURE_OPENAI_API_KEY')
        self.endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
        self.server_url = os.getenv('SERVER_URL', 'https://focusproxy-production.up.railway.app')
        
        if not self.api_key or not self.endpoint:
            raise ValueError("Please set AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT environment variables")
        
        self.analyzer = ActivityAnalyzer(self.api_key, self.endpoint)
        os.makedirs(screenshots_dir, exist_ok=True)
    
    def capture_screenshot(self) -> str:
        """Capture a screenshot and return the file path"""
        with mss.mss() as sct:
            ts = timestamp()
            mon = sct.monitors[0]
            shot = sct.grab(mon)
            raw = mss.tools.to_png(shot.rgb, shot.size)
            
            path = os.path.join(self.screenshots_dir, f"shot_full_{ts}.png")
            img = Image.open(BytesIO(raw))
            img.save(path, format="PNG")
            
            return path
    
    def analyze_and_post(self):
        """Capture, analyze, and POST activity to server"""
        try:
            screenshot_path = self.capture_screenshot()
            print(f"[{datetime.now()}] Captured: {screenshot_path}")
            
            activity = self.analyzer.analyze_screenshot(screenshot_path)
            print(f"[{datetime.now()}] Activity: {activity}")
            
            response = requests.post(
                f"{self.server_url}/activity",
                json={"state": activity},
                timeout=30
            )
            
            if response.status_code == 200:
                print(f"[{datetime.now()}] Posted to server: {activity}")
            else:
                print(f"[{datetime.now()}] Error posting: {response.status_code}")
                
        except Exception as e:
            print(f"[{datetime.now()}] Error: {str(e)}")
    
    def run(self, interval_minutes: int = 5):
        """Run the monitor continuously"""
        # interval_seconds = interval_minutes * 60
        interval_seconds = 20
        
        print(f"Starting monitor service (interval: {interval_minutes} minutes)")
        print(f"Server URL: {self.server_url}")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                self.analyze_and_post()
                time.sleep(interval_seconds)
        except KeyboardInterrupt:
            print("\nStopping monitor service...")


if __name__ == "__main__":
    monitor = MonitorService()
    monitor.run(interval_minutes=5)


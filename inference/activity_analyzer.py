import base64
import os
from typing import Optional
import requests
from PIL import Image
import json

class ActivityAnalyzer:
    def __init__(self, api_key: str, endpoint: str, deployment_name: str = "gpt-4o-vision"):
        self.api_key = api_key
        self.endpoint = endpoint.rstrip('/')
        self.deployment_name = deployment_name
        self.api_version = "2024-02-15-preview"
        
    def encode_image(self, image_path: str) -> str:
        """Convert image to base64 string for API"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def analyze_screenshot(self, image_path: str, custom_prompt: Optional[str] = None) -> str:
        """Analyze screenshot and return activity description"""
        
        # Default prompt for activity recognition
        default_prompt = """Analyze this screenshot and provide a single lowercase words that describes the user's primary activity. Focus on:
        - What application or website they're using
        - What specific task or activity they appear to be engaged in
        - Their level of focus/attention (focused work, browsing, distracted, etc.)
        
        Choose only from this list (or the closest match): 
        reading, typing, relaxing, chatting.

        Return ONLY the single word, no punctuation or explanation."""
        
        prompt = custom_prompt or default_prompt
        
        # Encode image
        base64_image = self.encode_image(image_path)
        
        # Prepare API request
        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key,
        }
        
        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300,
            "temperature": 0.3
        }
        
        # Make API call
        url = f"{self.endpoint}/openai/deployments/{self.deployment_name}/chat/completions?api-version={self.api_version}"
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
            
        except requests.exceptions.RequestException as e:
            return f"Error analyzing screenshot: {str(e)}"
        except KeyError as e:
            return f"Error parsing response: {str(e)}"
    
    def get_latest_screenshot(self, screenshots_dir: str = "screenshots") -> Optional[str]:
        """Get the most recent screenshot from the screenshots directory"""
        if not os.path.exists(screenshots_dir):
            return None
            
        screenshots = [
            f for f in os.listdir(screenshots_dir) 
            if f.lower().endswith(('.png', '.jpg', '.jpeg'))
        ]
        
        if not screenshots:
            return None
            
        # Sort by modification time, newest first
        screenshots.sort(key=lambda x: os.path.getmtime(os.path.join(screenshots_dir, x)), reverse=True)
        
        return os.path.join(screenshots_dir, screenshots[0])
    
    def analyze_latest_screenshot(self, screenshots_dir: str = "screenshots", custom_prompt: Optional[str] = None) -> str:
        """Analyze the most recent screenshot"""
        latest_screenshot = self.get_latest_screenshot(screenshots_dir)
        
        if not latest_screenshot:
            return "No screenshots found in the screenshots directory."
            
        print(f"Analyzing: {latest_screenshot}")
        return self.analyze_screenshot(latest_screenshot, custom_prompt)


def main():
    # Load configuration from .env file and environment variables
    from dotenv import load_dotenv
    load_dotenv()  # Load .env file
    
    api_key = os.getenv('AZURE_OPENAI_API_KEY')
    endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
    
    if not api_key or not endpoint:
        print("Please set AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT environment variables")
        return
    
    analyzer = ActivityAnalyzer(api_key, endpoint)
    
    # Analyze the latest screenshot
    result = analyzer.analyze_latest_screenshot()
    print("\nActivity Analysis:")
    print("-" * 50)
    print(result)


if __name__ == "__main__":
    main()

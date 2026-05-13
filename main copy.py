from fastapi import FastAPI
import subprocess
import ollama
import webbrowser
from pydantic import BaseModel
import requests
import json
import uvicorn
import asyncio
import sys

# Fix for Windows asyncio subprocess issue
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(
        asyncio.WindowsProactorEventLoopPolicy()
    )

from playwright.async_api import async_playwright


# -----------------------------------
# FastAPI App
# -----------------------------------
app = FastAPI()


# -----------------------------------
# Request Model
# -----------------------------------
class UserPrompt(BaseModel):
    prompt: str


# -----------------------------------
# Generate Actions From Ollama
# -----------------------------------
def generate_actions(user_prompt: str):

    system_prompt = f"""
You are an AI Browser Automation Agent.

Convert user prompts into browser automation JSON actions.

Rules:
1. Return ONLY valid JSON
2. No explanation
3. Output must be JSON array
4. Supported actions:
   - goto
   - type
   - press
   - click

Example:

User:
Open youtube and search India capital

Output:
[
    {{
        "type": "goto",
        "url": "https://youtube.com"
    }},
    {{
        "type": "type",
        "selector": "input[name='search_query']",
        "text": "India capital"
    }},
    {{
        "type": "press",
        "key": "Enter"
    }}
]

User:
{user_prompt}
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen2.5-coder:1.5b",
            "prompt": system_prompt,
            "stream": False
        }
    )

    result = response.json()

    print("\nFULL OLLAMA RESPONSE:")
    print(result)

    if "response" not in result:
       raise Exception(f"Ollama Error: {result}")

    content = result["response"]

    # Clean markdown if model returns ```json
    content = content.replace("```json", "")
    content = content.replace("```", "")
    content = content.strip()

    print("\nOLLAMA RAW RESPONSE:")
    print(content)

    actions = json.loads(content)

    return actions

async def run_browser_actions(actions):

    try:
        async with async_playwright() as p:

            # Use a separate profile directory for automation
            browser = await p.chromium.launch_persistent_context(
                user_data_dir=r"C:\Users\swara\AppData\Local\Temp\playwright_chrome_profile",
                channel="chrome",
                headless=False
            )

            page = await browser.new_page()

            for action in actions:

                print("RUNNING:", action)

                if action["type"] == "goto":

                    await page.goto(action["url"])

                elif action["type"] == "type":

                    await page.fill(
                        action["selector"],
                        action["text"]
                    )

                elif action["type"] == "press":

                    await page.keyboard.press(
                        action["key"]
                    )

                elif action["type"] == "click":

                    await page.click(
                        action["selector"]
                    )

            await page.wait_for_timeout(5000)
            
            # Close the browser when done
            await browser.close()
            
    except Exception as e:
        print(f"Browser error: {e}")
        raise


def extract_app_name(user_input: str):
    """Extract app name from user input using Ollama"""
    prompt = f"""
    Extract only app name.

    User Input: {user_input}

    Return only app name.
    """

    response = ollama.chat(
        model='qwen2.5-coder:1.5b',
        messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ]
    )

    app_name = response['message']['content'].strip().lower()
    print("Detected App:", app_name)
    return app_name


def open_windows_app(app_name: str):
    """Try to open a Windows app by name"""
    try:
        powershell_cmd = f"""
        Get-StartApps | Where-Object {{$_.Name -like "*{app_name}*"}}
        """
        result = subprocess.check_output(
            ["powershell", "-Command", powershell_cmd],
            text=True
        )
        
        print(result)

        lines = result.strip().split("\n")

        if len(lines) < 3:
            return {
                "status": "error",
                "message": "App not found in Windows"
            }

        # Get AppID
        app_id = lines[-1].split()[-1]

        print("App ID:", app_id)

        # Open Store App
        subprocess.Popen(
            ["explorer.exe", f"shell:AppsFolder\\{app_id}"]
        )

        return {
            "status": "success",
            "app": app_name,
            "app_id": app_id,
            "method": "windows_app"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


def extract_search_query(user_input: str):
    """Extract search query from user input using Ollama"""
    prompt = f"""
    Extract only search query for web browser.

    User Input: {user_input}

    Return only search text.
    """

    response = ollama.chat(
        model='qwen2.5-coder:1.5b',
        messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ]
    )

    search_query = response['message']['content'].strip()
    print("Search Query:", search_query)
    return search_query


# -----------------------------------
# Merged API Route - Smart Open
# -----------------------------------
@app.post("/smart-open")
async def smart_open(data: UserPrompt):
    """
    Smart API that first tries to open as Windows app,
    if not found, then falls back to browser automation
    """
    
    print("\n==============================")
    print("USER PROMPT:")
    print(data.prompt)
    print("==============================")
    
    # Step 1: Extract app name from user input
    app_name = extract_app_name(data.prompt)
    
    # Step 2: Try to open as Windows app
    print("\n--- TRYING WINDOWS APP ---")
    windows_result = open_windows_app(app_name)
    
    if windows_result["status"] == "success":
        print("✓ Windows app opened successfully")
        return {
            "status": "success",
            "method": "windows_app",
            "result": windows_result,
            "message": f"Successfully opened {app_name} as Windows app"
        }
    
    # Step 3: If Windows app not found, try browser automation
    print(f"\n--- Windows app '{app_name}' not found, falling back to browser ---")
    print("--- TRYING BROWSER AUTOMATION ---")
    
    try:
        # Generate actions from Ollama for browser automation
        actions = generate_actions(data.prompt)
        print("\nGENERATED ACTIONS:")
        print(actions)
        
        # Execute browser actions
        await run_browser_actions(actions)
        
        print("✓ Browser automation completed")
        return {
            "status": "success",
            "method": "browser_automation",
            "actions": actions,
            "message": f"Opened in browser using automation"
        }
        
    except Exception as e:
        print(f"✗ Browser automation failed: {e}")
        return {
            "status": "error",
            "method": "fallback_failed",
            "windows_error": windows_result["message"],
            "browser_error": str(e),
            "message": "Failed to open using both Windows app and browser automation"
        }

# -----------------------------------
# Run Server
# -----------------------------------
if __name__ == "__main__":

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )
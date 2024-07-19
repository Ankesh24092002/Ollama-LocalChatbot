from flask import Flask, request, render_template, jsonify
import aiohttp
import asyncio
import logging

app = Flask(__name__)
url = "http://localhost:11434/api/generate"
headers = {'Content-Type': 'application/json'}

# Configure logging
logging.basicConfig(level=logging.INFO)

async def fetch_response(session, data):
    try:
        async with session.post(url, headers=headers, json=data) as response:
            response.raise_for_status()  # Raises an exception for HTTP errors
            return await response.json()
    except aiohttp.ClientError as e:
        logging.error(f"Client error: {e}")
        return {"response": "Error: Unable to fetch response from the server."}
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return {"response": "Error: An unexpected error occurred."}

def fetch_response_sync(data):
    return asyncio.run(fetch_response_async(data))

async def fetch_response_async(data):
    async with aiohttp.ClientSession() as session:
        return await fetch_response(session, data)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        prompt = request.form['prompt'].lower()
        
        # Create a context for the current question
        data = {
            "model": "mlguru",
            "prompt": f"User asked: '{prompt}'\nProvide a concise response:",
            "stream": False
        }

        response_data = fetch_response_sync(data)
        actual_response = response_data.get('response', "Error: Unable to fetch response.")
        return jsonify({"response": actual_response})
    
    return render_template("dots.html")

if __name__ == "__main__":
    app.run(debug=True)


from flask import Flask, render_template_string, request
import requests

# -----------------------------
# Configuration
# -----------------------------
# Replace with your ngrok URL from Colab (without /health or /translate)
COLAB_NGROK_URL = "https://19699838395f.ngrok-free.app"

# -----------------------------
# Flask App
# -----------------------------
app = Flask(__name__)

# -----------------------------
# HTML Template
# -----------------------------
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Romanized Text Translator</title>
    <meta charset="UTF-8">
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .container {
            background: white;
            max-width: 700px;
            width: 100%;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }
        h2 {
            color: #333;
            margin-bottom: 30px;
            text-align: center;
            font-size: 28px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            color: #555;
            font-weight: 600;
        }
        textarea {
            width: 100%;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            font-family: inherit;
            resize: vertical;
            transition: border-color 0.3s;
        }
        textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        button {
            width: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 18px;
            font-weight: 600;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }
        button:active {
            transform: translateY(0);
        }
        .result {
            margin-top: 30px;
            padding: 20px;
            border-radius: 8px;
            background-color: #f0f9ff;
            border-left: 4px solid #667eea;
        }
        .result h3 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 20px;
        }
        .result p {
            color: #333;
            font-size: 16px;
            line-height: 1.6;
        }
        .error {
            background-color: #fee;
            border-left-color: #f44336;
        }
        .error h3 {
            color: #f44336;
        }
        .loading {
            text-align: center;
            color: #667eea;
            font-weight: 600;
        }
        .status {
            text-align: center;
            padding: 10px;
            margin-bottom: 20px;
            border-radius: 8px;
            font-size: 14px;
        }
        .status.connected {
            background-color: #e7f5e7;
            color: #2e7d32;
        }
        .status.disconnected {
            background-color: #fee;
            color: #c62828;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>🌐 Romanized Text Translator</h2>
        
        {% if status %}
        <div class="status {{ 'connected' if 'connected' in status.lower() else 'disconnected' }}">
            {{ status }}
        </div>
        {% endif %}
        
        <form method="POST">
            <div class="form-group">
                <label for="text">Enter Romanized Text:</label>
                <textarea 
                    name="text" 
                    id="text"
                    rows="6" 
                    placeholder="Example: namaste, arigato, bonjour..."
                    required>{{ request.form.get('text', '') }}</textarea>
            </div>
            <button type="submit">Translate to English</button>
        </form>
        
        {% if translation %}
        <div class="result {% if 'error' in translation.lower() %}error{% endif %}">
            <h3>{% if 'error' in translation.lower() %}❌ Error{% else %}✅ Translation{% endif %}</h3>
            <p>{{ translation }}</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

# -----------------------------
# Helper Functions
# -----------------------------
def check_server_health():
    """Check if the Colab server is reachable"""
    try:
        response = requests.get(
            f"{COLAB_NGROK_URL}/health",
            headers={"ngrok-skip-browser-warning": "true"},
            timeout=5
        )
        if response.status_code == 200:
            return "✅ Connected to server"
        return f"⚠️ Server returned status {response.status_code}"
    except requests.exceptions.RequestException:
        return "❌ Cannot connect to server - Check your ngrok URL"

# -----------------------------
# Routes
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    translation = None
    status = None
    
    # Check server health on page load
    if request.method == "GET":
        status = check_server_health()
    
    if request.method == "POST":
        text_to_translate = request.form.get("text", "").strip()
        
        if not text_to_translate:
            translation = "Error: Please enter some text to translate."
        else:
            try:
                print(f"\n{'='*50}")
                print(f"🔄 Full URL: {COLAB_NGROK_URL}/translate")
                print(f"📝 Text: {text_to_translate}")
                print(f"🔍 Checking if URL ends with /translate...")
                
                # Ensure proper URL format
                base_url = COLAB_NGROK_URL.rstrip('/')
                translate_url = f"{base_url}/translate"
                
                print(f"🌐 Final URL: {translate_url}")
                
                headers = {
                    "Content-Type": "application/json",
                    "ngrok-skip-browser-warning": "true"
                }
                
                payload = {"text": text_to_translate}
                print(f"📦 Payload: {payload}")
                
                response = requests.post(
                    translate_url,
                    json=payload,
                    headers=headers,
                    timeout=60
                )
                
                print(f"📊 Status: {response.status_code}")
                print(f"📄 Response Text: {response.text[:500]}")
                
                if response.status_code == 200:
                    result = response.json()
                    translation = result.get("translation", "No translation received")
                    print(f"✅ Translation: {translation}")
                else:
                    translation = f"Error: Server returned status {response.status_code}. Response: {response.text[:200]}"
                    print(f"❌ {translation}")
                
                print(f"{'='*50}\n")
                    
            except requests.exceptions.Timeout:
                translation = "Error: Request timed out. The server might be processing or unavailable."
            except requests.exceptions.ConnectionError:
                translation = "Error: Cannot connect to server. Please check if your ngrok URL is correct and the Colab server is running."
            except requests.exceptions.JSONDecodeError:
                translation = f"Error: Invalid response from server. Response: {response.text[:200]}"
            except Exception as e:
                translation = f"Error: {str(e)}"
    
    return render_template_string(HTML_TEMPLATE, translation=translation, status=status)

# -----------------------------
# Run Server
# -----------------------------
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🌐 ROMANIZED TEXT TRANSLATOR - FRONTEND")
    print("="*60)
    print(f"📡 Backend URL: {COLAB_NGROK_URL}")
    print(f"🚀 Frontend URL: http://127.0.0.1:5000")
    print(f"\n⚠️  Make sure to update COLAB_NGROK_URL with your ngrok URL!")
    print("="*60 + "\n")
    
    app.run(host="127.0.0.1", port=5000, debug=True)
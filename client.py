import google.generativeai as genai

genai.configure(api_key="AIzaSyCzCs1Qwz3RexR2-p3QnvnJSsmGEcJL9I0")

def aiProcess(command):
    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = f"""
You are Jarvis, a calm and intelligent AI voice assistant.
Respond in short sentences, be helpful, clear, and friendly.
Do not write long paragraphs.

User: {command}
Jarvis:
"""
    response = model.generate_content(prompt)
    return response.text
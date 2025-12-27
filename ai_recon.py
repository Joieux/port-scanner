import openai
import os

# You need an API Key in your environment variables
# export OPENAI_API_KEY='sk-...'
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_threat_summary(scan_data, tool_type="network scan"):
    """
    Takes raw text output from Nmap or your Port Scanner
    and returns an Executive Summary of vulnerabilities.
    """
    print(f"\n[+] Sending {len(scan_data)} bytes of data to AI Analyst...")
    
    prompt = f"""
    You are a Senior Red Team Lead. Analyze the following raw output from a {tool_type}.
    1. Identify the most critical open ports or exposed assets.
    2. Suggest one immediate attack vector.
    3. Keep it brief (3 sentences max).
    
    RAW DATA:
    {scan_data}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # Cheap and fast
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        summary = response.choices[0].message.content
        return f"\n--- AI THREAT ANALYSIS ---\n{summary}\n--------------------------"
    except Exception as e:
        return f"[!] AI Analysis Failed: {e}"
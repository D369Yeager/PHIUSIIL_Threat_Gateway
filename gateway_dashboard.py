import time
import os
import requests
from production_gateway import PhishingThreatGateway
from persistence_manager import StatePersistenceManager

def launch_production_gateway_dashboard(target_url: str, target_html: str):
    """
   Operational Hub: Collects live web payloads, inspects physical 
    storage health, extracts features, and runs real-time ensemble auditing.
    """
    print("=" * 75)
    print("         🔒 PHIUSIIL ENTERPRISE THREAT GATEWAY SYSTEM DASHBOARD")
    print("=" * 75)
    print(f" [System Boot] Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    db_path = "phiusiil_state.db"
    
    # 1. Audit the physical database file state on disk
    if os.path.exists(db_path):
        db_size_kb = os.path.getsize(db_path) / 1024
        print(f" [DB Health]   Found persistent storage vault: '{db_path}' ({db_size_kb:.2f} KB)")
    else:
        print(f" [DB Health]   ⚠️ No persistent database file detected on disk yet.")
        
    print("-" * 75)
    print(" INITIALIZING LIVE INTERCEPTION BOUNDARY CHANNEL...")
    start_init = time.time()
    
    # 2. Boot up our gateway (which automatically loads the database states)
    gateway = PhishingThreatGateway(db_path=db_path)
    init_time = (time.time() - start_init) * 1000
    print(f" -> Gateway online and routing active. Core warm-up time: {init_time:.2f}ms")
    print("-" * 75)
    
    # 3. Intercept and evaluate the live target input payload
    print(f" INTERCEPTING ACTIVE TRAFFIC TARGET:")
    print(f"   URL  : {target_url}")
    
    # Preview the first 60 characters of raw HTML cleanly
    html_preview = target_html.strip()[:60].replace('\n', ' ')
    print(f"   HTML : {html_preview}... [Truncated]")
    print(" Running real-time heuristic feature parsing & ensemble vote...")
    
    start_eval = time.time()
    payload_response = gateway.evaluate_live_url(target_url, target_html)
    eval_time = (time.time() - start_eval) * 1000
    
    # 4. Render the human-readable security dashboard panel
    print("\n" + "#" * 55)
    print("          LIVE TRAFFIC SECURITY EVALUATION REPORT")
    print("#" * 55)
    print(f" TARGET TARGET URL    : {payload_response['target_url']}")
    
    # Highlight final threat status cleanly
    if payload_response['classification'] == 'LEGITIMATE':
        print(f" FINAL STATUS VERDICT : ✅ {payload_response['classification']}")
    else:
        print(f" FINAL STATUS VERDICT : ❌ {payload_response['classification']}")
        
    print(f" VERDICT DECISION CODE: {payload_response['verdict_code']} (1=Safe, 0=Phish)")
    print(f" EXTRACTED FEATURES   : {payload_response['features_extracted']} Dimensions Parsed")
    print(f" GATEWAY LATENCY SPEED: {eval_time:.2f} ms")
    print("#" * 55)
    
    print("\n [System Status] All perimeter monitoring matrices running stably.")
    print("=" * 75)

if __name__ == "__main__":
    # 🌟 CHANGE THIS TO TEST ANY URL YOU WANT TO LIVE AUDIT 🌟
    target_url = "https://www.google.com"
    
    print("\n" + "-" * 75)
    print(f" [Scraper] Initiating live network request to: {target_url}")
    print("-" * 75)
    
    try:
        # Standard headers to prevent web servers from blocking the scraper request
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        
        # Pull live page directly from the internet
        response = requests.get(target_url, timeout=5, headers=headers)
        
        # Grab raw source code HTML
        live_html = response.text
        
        # Feed the extracted parameters live into our dashboard evaluation flow
        launch_production_gateway_dashboard(target_url, live_html)
        
    except requests.exceptions.RequestException as e:
        print(f"\n ❌ Network Request Failed: Could not contact target server.")
        print(f" Error Diagnostic Details: {e}")
        print("-" * 75)
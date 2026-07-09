from production_gateway import PhishingThreatGateway
from persistence_manager import StatePersistenceManager

def inject_analyst_override(drifted_url: str, drifted_html: str, actual_label: int):
    """
    Simulates a Security Operations Center (SOC) analyst catching a 
    missed threat and feeding the correction directly into the gateway brain.
    """
    db_path = "phiusiil_state.db"
    
    print(f"🔒 [SOC Override] Connecting to Security Gateway Vault...")
    # 1. Initialize the gateway wrapper (which automatically loads your trained weights)
    gateway = PhishingThreatGateway(db_path=db_path)
    
    print(f"📡 [SOC Override] Dispatching dynamic feedback update for: {drifted_url}")
    # 2. Pass the novel, drifted threat sample directly to the live gateway
    gateway.learn_from_feedback(url=drifted_url, raw_html=drifted_html, true_label=actual_label)
    
    print(f"✅ [SUCCESS] Gateway weights optimized and autosaved to disk.")

if __name__ == "__main__":
    # Example: A new, stealthy login phish that bypassed the initial 240k baseline
    new_threat_url = "https://secure-update-gemini-verification.com/login"
    new_threat_html = "<html><body><form>Enter your administrative master password</form></body></html>"
    
    # 0 = Phishing, 1 = Legitimate
    inject_analyst_override(new_threat_url, new_threat_html, actual_label=0)
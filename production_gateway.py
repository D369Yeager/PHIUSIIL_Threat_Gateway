import numpy as np
import time
from bs4 import BeautifulSoup

# Core architectural components from our previous files
from master_pipeline import generate_master_feature_vector
from ensemble_voting import get_ensemble_majority_vote
from ensemble_core import initialize_online_ensemble
from sklearn.preprocessing import StandardScaler
from persistence_manager import StatePersistenceManager

class PhishingThreatGateway:
    def __init__(self, db_path: str = "phiusiil_state.db"):
        """
        Core Target: Bind the state persistence manager natively 
        to the live gateway for seamless initialization and automatic storage.
        """
        self.db_manager = StatePersistenceManager(db_path)
        self.target_classes = np.array([0, 1])
        
        # 🌟 AUTOMATIC STATE RESTORATION ON APP STARTUP
        print("  [System Startup] Querying SQLite State Persistence database...")
        recovered_scaler = self.db_manager.load_state("streaming_scaler")
        recovered_ensemble = self.db_manager.load_state("online_ensemble")
        
        if recovered_scaler and recovered_ensemble:
            self.scaler = recovered_scaler
            self.ensemble = recovered_ensemble
            print("  [SUCCESS] Existing state recovered safely from SQL layer. Ready for live traffic.")
        else:
            print("  [Notice] No active state found in DB. Initializing baseline matrices from scratch...")
            self.scaler = StandardScaler()
            self.ensemble = initialize_online_ensemble()

    def evaluate_live_url(self, url: str, raw_html: str) -> dict:
        """Intercepts an incoming target payload, scales it, and executes a majority prediction vote."""
        soup = BeautifulSoup(raw_html, 'html.parser')
        raw_vector, _ = generate_master_feature_vector(url, raw_html, soup)
        
        X_clean = raw_vector[:50].reshape(1, -1) if len(raw_vector) >= 50 else np.pad(raw_vector, (0, 50 - len(raw_vector))).reshape(1, -1)
        
        # Dynamic safety handling if the scaler hasn't seen training updates yet
        try:
            X_scaled = self.scaler.transform(X_clean)
        except Exception:
            X_scaled = X_clean 
            
        final_verdict = get_ensemble_majority_vote(self.ensemble, X_scaled)
        
        return {
            'target_url': url,
            'classification': 'LEGITIMATE' if final_verdict == 1 else 'PHISHING_THREAT',
            'verdict_code': final_verdict,
            'features_extracted': len(X_clean[0])
        }

    def learn_from_feedback(self, url: str, raw_html: str, true_label: int):
        """Processes corrective analyst override feedback and immediately triggers an autosave sync."""
        soup = BeautifulSoup(raw_html, 'html.parser')
        raw_vector, _ = generate_master_feature_vector(url, raw_html, soup)
        
        X_clean = raw_vector[:50].reshape(1, -1) if len(raw_vector) >= 50 else np.pad(raw_vector, (0, 50 - len(raw_vector))).reshape(1, -1)
        
        # Update components on the streaming point
        self.scaler.partial_fit(X_clean)
        X_scaled = self.scaler.transform(X_clean)
        
        for model_name, model_obj in self.ensemble.items():
            model_obj.partial_fit(X_scaled, np.array([true_label]), classes=self.target_classes)
            
        # 🌟 AUTOMATIC SQL DATABASE PERSISTENT AUTOSAVE
        self.db_manager.save_state("streaming_scaler", self.scaler)
        self.db_manager.save_state("online_ensemble", self.ensemble)
        print(f"  [Async Worker Thread] State persistent sync saved to database file for: {url}")

# =====================================================================
# Live Persistence Production Audit Simulation
# =====================================================================
if __name__ == "__main__":
    print("=" * 75)
    print("         PERSISTENT PRODUCTION THREAT GATEWAY MONITOR")
    print("=" * 75)
    
    # 1. Initialize gateway (Will notice no database exists yet on first run and initialize scratch baselines)
    gateway = PhishingThreatGateway()
    print("-" * 75)
    
    # 2. Run a sample interaction feedback update to kick off an automatic database save
    url_target = "https://www.google.com/"
    html_target = "<html><head><title>Google</title></head><body><h1>Search Engine</h1></body></html>"
    
    print("Simulating User Feedback Override (Declaring Google as Legitimate = 1)...")
    gateway.learn_from_feedback(url_target, html_target, true_label=1)
    print("-" * 75)
    
    # 3. Re-instantiate a BRAND NEW gateway object instance to prove it pulls the state from the DB file!
    print("Simulating System Reboot / App Crash recovery process...")
    rebooted_gateway = PhishingThreatGateway()
    print("=" * 75)
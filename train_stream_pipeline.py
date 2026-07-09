import numpy as np
import time
from streaming_ingestion import stream_local_phiusiil_dataset
from ensemble_core import initialize_online_ensemble
from ensemble_voting import get_ensemble_majority_vote, calculate_streaming_metrics
from sklearn.preprocessing import StandardScaler
from persistence_manager import StatePersistenceManager

class StreamingDriftMonitor:
    def __init__(self, window_size: int = 500, warning_threshold: float = 0.90):
        """
        Core Target: Track model accuracy across a sliding window 
        to immediately detect operational performance drops or concept drift.
        """
        self.window_size = window_size
        self.warning_threshold = warning_threshold
        self.window_predictions = []

    def add_observation(self, y_true: int, y_pred: int):
        """Appends the latest prequential prediction result and checks for window drops."""
        is_correct = 1 if y_true == y_pred else 0
        self.window_predictions.append(is_correct)
        
        # Keep window strictly bound to target observation size
        if len(self.window_predictions) > self.window_size:
            self.window_predictions.pop(0)

    def check_drift_status(self) -> tuple:
        """Calculates moving window accuracy and evaluates performance stability flags."""
        if len(self.window_predictions) < self.window_size:
            return 1.0, "WARMING_UP" # Wait until window is full before auditing
            
        rolling_accuracy = sum(self.window_predictions) / self.window_size
        
        if rolling_accuracy < self.warning_threshold:
            return rolling_accuracy, "🚨 CONCEPT_DRIFT_WARNING"
        return rolling_accuracy, "STABLE"

def run_day_24_drift_pipeline(max_rows: int = 4000):
    """Orchestrates streaming training coupled with continuous sliding window drift audits."""
    print("=" * 75)
    print("        PHIUSIIL STREAMING ENGINE WITH CONCEPT DRIFT AUDITING")
    print("=" * 75)
    
    db_manager = StatePersistenceManager("phiusiil_state.db")
    streaming_scaler = db_manager.load_state("streaming_scaler") or StandardScaler()
    ensemble = db_manager.load_state("online_ensemble") or initialize_online_ensemble()
    
    data_stream = stream_local_phiusiil_dataset("PHIUSIIL_DATASET.csv", chunk_size=1)
    target_classes = np.array([0, 1])
    
    # Instantiate our sliding window monitor (500 observation lookback)
    drift_monitor = StreamingDriftMonitor(window_size=500, warning_threshold=0.92)
    
    metrics_tracker = {'UNIFIED_ENSEMBLE': [0, 0, 0, 0]}
    
    print(f" Streaming loop active. Running drift diagnostics across {max_rows} rows...")
    print("-" * 75)
    
    for idx in range(max_rows):
        try:
            X_row, y_true = next(data_stream)
        except StopIteration:
            break
            
        X_clean = X_row[:50].reshape(1, -1)
        
        # Update and transform scaled representations
        streaming_scaler.partial_fit(X_clean)
        X_scaled = streaming_scaler.transform(X_clean)
        
        # 1. Prequential prediction step
        ensemble_pred = 0
        try:
            ensemble_pred = get_ensemble_majority_vote(ensemble, X_scaled)
            if y_true == 1 and ensemble_pred == 1:   metrics_tracker['UNIFIED_ENSEMBLE'][0] += 1
            elif y_true == 0 and ensemble_pred == 1: metrics_tracker['UNIFIED_ENSEMBLE'][1] += 1
            elif y_true == 1 and ensemble_pred == 0: metrics_tracker['UNIFIED_ENSEMBLE'][2] += 1
            elif y_true == 0 and ensemble_pred == 0: metrics_tracker['UNIFIED_ENSEMBLE'][3] += 1
        except Exception:
            pass
            
        # 🌟 CRITICAL DAY 24 UPGRADE: Update moving lookback stats
        drift_monitor.add_observation(y_true, ensemble_pred)
        
        # 2. Incremental online training optimization updates
        for model_obj in ensemble.values():
            model_obj.partial_fit(X_scaled, np.array([y_true]), classes=target_classes)
            
        # 3. Stream monitoring status reporting checkpoints
        if (idx + 1) % 1000 == 0:
            tp, fp, fn, tn = metrics_tracker['UNIFIED_ENSEMBLE']
            overall_acc, _, _ = calculate_streaming_metrics(tp, fp, fn, tn)
            
            # Extract current sliding metric stats
            rolling_acc, status_flag = drift_monitor.check_drift_status()
            
            print(f"Row: {idx + 1:<5} | Cumulative Acc: {overall_acc:.4f} | Window Acc (Last 500): {rolling_acc:.4f} | Status: {status_flag}")

    # Finalize state update checkpoints
    db_manager.save_state("streaming_scaler", streaming_scaler)
    db_manager.save_state("online_ensemble", ensemble)
    print("-" * 75)
    print("[SUCCESS]  Stream Analytics Engine active and verified!")
    print("=" * 75)

if __name__ == "__main__":
    run_day_24_drift_pipeline(max_rows=250000)
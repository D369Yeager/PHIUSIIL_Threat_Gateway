import numpy as np
import time
from sklearn.preprocessing import StandardScaler
from ensemble_core import initialize_online_ensemble
from streaming_ingestion import stream_local_phiusiil_dataset

def get_ensemble_majority_vote(ensemble, X_scaled):
    """
    Gathers raw predictions from all active models using the 
    properly scaled features matrix, applying the majority threshold.
    """
    votes = []
    for model_name, model_obj in ensemble.items():
        try:
            pred = int(model_obj.predict(X_scaled)[0])
            votes.append(pred)
        except Exception:
            votes.append(0)
            
    # Tally votes: Majority rule (2 or 3 votes for 1 means Legitimate, else Phishing)
    majority_verdict = 1 if sum(votes) >= 2 else 0
    return majority_verdict

def calculate_streaming_metrics(tp, fp, fn, tn):
    """Computes mathematical classification metrics safely avoiding division by zero."""
    accuracy = (tp + tn) / (tp + fp + fn + tn) if (tp + fp + fn + tn) > 0 else 0.0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    return accuracy, precision, recall

def run_day_18_scaled_pipeline(max_stream_rows: int = 5000):
    """
    Day 18 Core Target: Introduces a streaming StandardScaler via .partial_fit()
    to normalize features before passing them to the ensemble matrix.
    """
    print("=" * 75)
    print("        PHIUSIIL ENSEMBLE WITH STREAMING STANDARD SCALER")
    print("=" * 75)
    
    # 1. Initialize models, ingestion pointer, and our new streaming scaler
    ensemble = initialize_online_ensemble()
    data_stream = stream_local_phiusiil_dataset("PHIUSIIL_DATASET.csv", chunk_size=1)
    streaming_scaler = StandardScaler()
    target_classes = np.array([0, 1])
    
    metrics_tracker = {
        'NaiveBayes': [0, 0, 0, 0],
        'PassiveAggressive': [0, 0, 0, 0],
        'SGDClassifier': [0, 0, 0, 0],
        'UNIFIED_ENSEMBLE': [0, 0, 0, 0]
    }
    
    print(f"  Streaming Ingestion Loop Engaged (Cap: {max_stream_rows} observations)...")
    print("-" * 75)
    
    start_time = time.time()
    
    for idx in range(max_stream_rows):
        try:
            X_row, y_true = next(data_stream)
        except StopIteration:
            break
            
        X_clean = X_row[:50].reshape(1, -1)
        y_ground_truth = np.array([y_true])
        
        #  Update scaler metrics on the raw row, then transform it
        streaming_scaler.partial_fit(X_clean)
        X_scaled = streaming_scaler.transform(X_clean)
        
        # --- PHASE 1: EVALUATE ENSEMBLE VOTER (Using Scaled Data) ---
        try:
            ensemble_pred = get_ensemble_majority_vote(ensemble, X_scaled)
            if y_true == 1 and ensemble_pred == 1:   metrics_tracker['UNIFIED_ENSEMBLE'][0] += 1
            elif y_true == 0 and ensemble_pred == 1: metrics_tracker['UNIFIED_ENSEMBLE'][1] += 1
            elif y_true == 1 and ensemble_pred == 0: metrics_tracker['UNIFIED_ENSEMBLE'][2] += 1
            elif y_true == 0 and ensemble_pred == 0: metrics_tracker['UNIFIED_ENSEMBLE'][3] += 1
        except Exception:
            pass
            
        # --- PHASE 2: EVALUATE INDIVIDUAL BASE MODELS (Using Scaled Data) ---
        for model_name, model_obj in ensemble.items():
            try:
                pred = int(model_obj.predict(X_scaled)[0])
                if y_true == 1 and pred == 1:   metrics_tracker[model_name][0] += 1
                elif y_true == 0 and pred == 1: metrics_tracker[model_name][1] += 1
                elif y_true == 1 and pred == 0: metrics_tracker[model_name][2] += 1
                elif y_true == 0 and pred == 0: metrics_tracker[model_name][3] += 1
            except Exception:
                pass
                
        # --- PHASE 3: INCREMENTAL LEARNING UPDATE STEP (Using Scaled Data) ---
        for model_obj in ensemble.values():
            model_obj.partial_fit(X_scaled, y_ground_truth, classes=target_classes)
            
        # --- PHASE 4: LIVE SCORES REPORTING ---
        if (idx + 1) == max_stream_rows:
            elapsed = time.time() - start_time
            print(f"Final Summary Post {idx + 1} Rows | Processing Duration: {elapsed:.2f}s")
            print(f"{'ONLINE SYSTEM COMPONENT':<24} | {'ACCURACY':<10} | {'PRECISION':<10} | {'RECALL':<10}")
            print("-" * 65)
            
            for name in metrics_tracker.keys():
                tp, fp, fn, tn = metrics_tracker[name]
                acc, prec, rec = calculate_streaming_metrics(tp, fp, fn, tn)
                highlight = "🌟 " if name == "UNIFIED_ENSEMBLE" else "   "
                print(f"{highlight}{name:<22} | {acc:<10.4f} | {prec:<10.4f} | {rec:<10.4f}")
            print("-" * 75)

if __name__ == "__main__":
    run_day_18_scaled_pipeline(max_stream_rows=5000)
import pandas as pd
import numpy as np

def stream_local_phiusiil_dataset(file_path: str = "PHIUSIIL_DATASET.csv", chunk_size: int = 1):
    """
    Core Ingestion Tool: Iterates through your local dataset row-by-row,
    dynamically filtering out any text columns to maintain a clean mathematical matrix row.
    """
    try:
        for chunk in pd.read_csv(file_path, chunksize=chunk_size):
            # Clean up all column headers by stripping whitespace and forcing lowercase
            chunk.columns = chunk.columns.str.strip().str.lower()
            
            # 1. Locate the exact label target column cleanly
            if 'label' in chunk.columns:
                y_label = int(chunk['label'].values[0])
                chunk = chunk.drop(columns=['label'])
            elif 'target' in chunk.columns:
                y_label = int(chunk['target'].values[0])
                chunk = chunk.drop(columns=['target'])
            else:
                y_label = -1
            
            # 2. Drop human-readable text strings automatically
            numeric_df = chunk.select_dtypes(include=[np.number])
                
            # 3. Convert clean numeric properties to our 1D array row format
            X_projected_row = numeric_df.to_numpy(dtype=float)[0]
            
            yield X_projected_row, y_label
            
    except FileNotFoundError:
        print(f"  [CSV Error] Could not find '{file_path}' in your working folder.")
        return

# =====================================================================
# Verification Execution
# =====================================================================
if __name__ == "__main__":
    print("=" * 75)
    print("        LOCAL PHIUSIIL REAL-DATA STREAM CHECK (FIXED)")
    print("=" * 75)
    
    local_stream = stream_local_phiusiil_dataset("PHIUSIIL_DATASET.csv", chunk_size=1)
    
    print("  [SUCCESS] Local file stream point open and tracking.\n")
    
    for idx in range(3):
        try:
            X_row, y_label = next(local_stream)
            print(f"Ingested Real Row #{idx + 1} From Local CSV")
            print(f"  Vector Columns Count (Dropped Text) : {len(X_row)} features")
            print(f"  Target Classification Verdict       : {y_label} ({'Legitimate' if y_label == 1 else 'Phishing'})")
            print(f"  First 5 Math Values in Row Array    : {X_row[:5]}")
            print("-" * 75)
        except StopIteration:
            print("  Stream ended safely.")
            break
        except Exception as e:
            print(f"  [Error]: Stream execution interrupted: {e}")
            break
            
    print("=" * 75)
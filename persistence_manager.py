import sqlite3
import pickle
import os

class StatePersistenceManager:
    def __init__(self, db_path: str = "phiusiil_state.db"):
        """
        Core Target: Establish a persistent SQL storage vault to save
        and recover online model states and streaming scaler metrics across reboots.
        """
        self.db_path = db_path
        self._initialize_database()

    def _initialize_database(self):
        """Creates the internal storage structure if it doesn't already exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS model_state (
                    component_name TEXT PRIMARY KEY,
                    binary_blob BLOB,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def save_state(self, component_name: str, python_object):
        """Serializes a living python machine learning state object into a SQL binary row."""
        binary_data = pickle.dumps(python_object)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO model_state (component_name, binary_blob, last_updated)
                VALUES (?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(component_name) DO UPDATE SET
                    binary_blob = excluded.binary_blob,
                    last_updated = CURRENT_TIMESTAMP
            """, (component_name, binary_data))
            conn.commit()

    def load_state(self, component_name: str):
        """Retrieves and reconstructs a saved model from its database binary blob."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT binary_blob FROM model_state WHERE component_name = ?", (component_name,))
            row = cursor.fetchone()
            
        if row:
            return pickle.loads(row[0])
        return None

# =====================================================================
# Live Persistence Storage Audit Execution
# =====================================================================
if __name__ == "__main__":
    print("=" * 75)
    print("        SQLITE BACKEND PERSISTENCE STATE AUDIT")
    print("=" * 75)
    
    from sklearn.preprocessing import StandardScaler
    
    # 1. Instantiate manager
    db_manager = StatePersistenceManager()
    
    # 2. Simulate a scaler learning state info
    test_scaler = StandardScaler()
    dummy_data = [[10.0, 20.0], [30.0, 40.0]]
    test_scaler.fit(dummy_data)
    
    print(f"Original Scaler Mean Prior to Save : {test_scaler.mean_}")
    
    # 3. Commit it to SQLite
    db_manager.save_state("streaming_scaler", test_scaler)
    print("  [SUCCESS] Serialized state successfully injected into local SQL layer.")
    
    # 4. Load it back fresh to verify absolute bit-level accuracy
    recovered_scaler = db_manager.load_state("streaming_scaler")
    print(f"Recovered Scaler Mean Post Load    : {recovered_scaler.mean_}")
    print("-" * 75)
    
    if list(test_scaler.mean_) == list(recovered_scaler.mean_):
        print("  [CRITICAL SUCCESS] Persistence state verification passed perfectly!")
    else:
        print("  [Error] Data mismatch during serialization loop.")
    print("=" * 75)
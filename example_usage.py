from client import StateSnapshotCheckpointResumer

resumer = StateSnapshotCheckpointResumer()
session_id = "agent_run_9942"
state = {
    "step": 3,
    "completed_tasks": ["auth", "fetch_records"],
    "extracted_lead_count": 48
}

save_telemetry = resumer.save_checkpoint(session_id, state, step_index=3)
print("=== Snapshot Save Telemetry ===")
print("Saved:", save_telemetry)

restored = resumer.restore_checkpoint(session_id)
print("=== Snapshot Restore Telemetry ===")
print("Restore Status:", restored["status"])
print("Restored State:", restored["state_data"])

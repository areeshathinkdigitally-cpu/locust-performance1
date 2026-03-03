import csv
import os
import sys

FAIL_RATIO_MAX = float(os.getenv("LOCUST_FAIL_RATIO_MAX", "0.01"))  # 1%
P95_MAX_MS = float(os.getenv("LOCUST_P95_MAX_MS", "1200"))         # 1.2s

stats_csv = sys.argv[1] if len(sys.argv) > 1 else "reports/locust_stats.csv"

with open(stats_csv, newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

agg = next((r for r in rows if (r.get("Name") or "").strip() == "Aggregated"), None)
if not agg:
    print("Aggregated row not found in stats CSV.")
    sys.exit(2)

fail_ratio = float(agg.get("Failure Ratio") or 0.0)
p95 = float(agg.get("95%") or 0.0)

print(f"[THRESHOLDS] Failure Ratio={fail_ratio} (max {FAIL_RATIO_MAX})")
print(f"[THRESHOLDS] P95={p95}ms (max {P95_MAX_MS}ms)")

if fail_ratio > FAIL_RATIO_MAX or p95 > P95_MAX_MS:
    print("[THRESHOLDS] FAILED")
    sys.exit(1)

print("[THRESHOLDS] PASSED")
sys.exit(0)

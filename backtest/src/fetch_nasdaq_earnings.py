"""Fetch the Nasdaq earnings calendar (one request per weekday) and store raw JSON rows.

Usage: python3 -I fetch_nasdaq_earnings.py <out_dir> <start YYYY-MM-DD> <end YYYY-MM-DD>
Polite: ~2.5 requests/second, resumable (skips dates already saved).
"""
import sys, os, json, time, datetime as dt, urllib.request

out_dir, start, end = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(out_dir, exist_ok=True)
d = dt.date.fromisoformat(start)
end_d = dt.date.fromisoformat(end)
hdr = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)", "Accept": "application/json"}
n_ok = n_err = 0
while d <= end_d:
    if d.weekday() < 5:
        fn = os.path.join(out_dir, f"{d.isoformat()}.json")
        if not os.path.exists(fn):
            url = f"https://api.nasdaq.com/api/calendar/earnings?date={d.isoformat()}"
            for attempt in range(4):
                try:
                    req = urllib.request.Request(url, headers=hdr)
                    raw = urllib.request.urlopen(req, timeout=30).read()
                    j = json.loads(raw)
                    rows = (j.get("data") or {}).get("rows") or []
                    with open(fn, "w") as f:
                        json.dump(rows, f)
                    n_ok += 1
                    break
                except Exception as e:  # noqa
                    time.sleep(2 + 3 * attempt)
            else:
                n_err += 1
            time.sleep(0.4)
    d += dt.timedelta(days=1)
    if d.day == 1 and d.month in (1, 7):
        print(d, "ok", n_ok, "err", n_err, flush=True)
print("done ok", n_ok, "err", n_err)

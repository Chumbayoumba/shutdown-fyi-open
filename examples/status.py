"""Что сейчас не так: сервисы со сбоем и сервисы, закрытые из России.

    python3 examples/status.py
Данные: shutdown.fyi, CC BY 4.0.
"""
import json
import urllib.request

BASE = "https://shutdown.fyi"


def get(path):
    req = urllib.request.Request(BASE + path, headers={"User-Agent": "shutdown-fyi-example"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


status = get("/api/status.json")
print("Индекс связности:", status["country"]["connectivityIndex"])

bad = [i for i in status["items"] if i["status"] in ("degraded", "down")]
print("\nСбой сейчас:" if bad else "\nМассовых сбоев сейчас нет.")
for i in bad:
    print(f"  {i['name']}: {i['status']}  {i['url']}")

print("\nНе открываются из России:")
for i in status["items"]:
    if i["kind"] != "service":
        continue
    probe = get(f"/api/status/service/{i['slug']}.json").get("probe") or {}
    if probe.get("verdict") == "blocked":
        steps = {h["host"]: h["verdict"] for h in probe.get("hosts", [])}
        print(f"  {i['name']}: {steps}")

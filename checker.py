from playwright.sync_api import sync_playwright
import json
import requests

WEBHOOK_URL = "https://discord.com/api/webhooks/1500567744704282634/Ed5eaz2Fnr31MqUIM1IOJuUQ0RD4Lof9FShcYVHF9h9PTrkctShJ-Z4tzaXYA3Yywo_S"
URL = "https://www.eticketing.co.uk/tottenhamhotspur/Events"

def get_events():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)"
        )
        page = context.new_page()

        page.goto(URL, timeout=60000)
        page.wait_for_timeout(7000)

        elements = page.query_selector_all("h3")

        events = []
        for el in elements:
            text = el.inner_text().strip()
            if text:
                events.append(text)

        browser.close()
        return list(set(events))

def load_old():
    try:
        with open("events.json", "r") as f:
            return json.load(f)
    except:
        return []

def save(events):
    with open("events.json", "w") as f:
        json.dump(events, f)

def send(msg):
    requests.post(WEBHOOK_URL, json={"content": msg})

old = load_old()
new = get_events()

for event in new:
    if event not in old:
        send(f"🚨 New event: {event}")

save(new)

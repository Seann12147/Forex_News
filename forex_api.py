from flask import Flask, jsonify
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/forex-news', methods=['GET'])
def get_forex_news():
    try:
        url = "https://cdn-nfs.faireconomy.media/ff_calendar_thisweek.xml"
        response = requests.get(url)
        root = ET.fromstring(response.content)

        now = datetime.utcnow()
        in_30_min = now + timedelta(minutes=30)

        events = []
        for event in root.findall('event'):
            impact = event.find('impact').text
            currency = event.find('currency').text
            date_str = event.find('date').text
            time_str = event.find('time').text
            title = event.find('title').text

            try:
                event_time = datetime.strptime(date_str + ' ' + time_str, '%b %d, %Y %I:%M %p')
            except:
                continue

            if impact == "High" and currency in ["USD", "EUR"]:
                if now <= event_time <= in_30_min:
                    events.append({
                        "currency": currency,
                        "impact": impact,
                        "title": title,
                        "time": event_time.isoformat()
                    })

        return jsonify({"news": events})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)

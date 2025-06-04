{\rtf1\ansi\ansicpg1252\cocoartf2821
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 from flask import Flask, jsonify\
import requests\
import xml.etree.ElementTree as ET\
from datetime import datetime, timedelta\
\
app = Flask(__name__)\
\
@app.route('/forex-news', methods=['GET'])\
def get_forex_news():\
    try:\
        url = "https://cdn-nfs.faireconomy.media/ff_calendar_thisweek.xml"\
        response = requests.get(url)\
        root = ET.fromstring(response.content)\
\
        now = datetime.utcnow()\
        in_30_min = now + timedelta(minutes=30)\
\
        events = []\
        for event in root.findall('event'):\
            impact = event.find('impact').text\
            currency = event.find('currency').text\
            date_str = event.find('date').text\
            time_str = event.find('time').text\
            title = event.find('title').text\
\
            try:\
                event_time = datetime.strptime(date_str + ' ' + time_str, '%b %d, %Y %I:%M %p')\
            except:\
                continue\
\
            if impact == "High" and currency in ["USD", "EUR"]:\
                if now <= event_time <= in_30_min:\
                    events.append(\{\
                        "currency": currency,\
                        "impact": impact,\
                        "title": title,\
                        "time": event_time.isoformat()\
                    \})\
\
        return jsonify(\{"news": events\})\
\
    except Exception as e:\
        return jsonify(\{"error": str(e)\})\
\
if __name__ == '__main__':\
    app.run(debug=True)\
}
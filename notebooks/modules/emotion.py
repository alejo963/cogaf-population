import os
from dotenv import load_dotenv

import requests
import re

load_dotenv()

LANG = 'es'
APIKEY = os.getenv("APIKEY")
APIURL = 'https://sentic.net/api/' + LANG + '/' + APIKEY + '.py?text='

SENTIC_LEVELS = {
    "introspection": ["Grief", "Sadness", "Melancholy", "Contentment", "Joy", "Ecstasy"],
    "temper": ["Rage", "Anger", "Annoyance", "Serenity", "Calmness", "Bliss"],
    "attitude": ["Loathing", "Disgust", "Dislike", "Acceptance", "Pleasantness", "Delight"],
    "sensitivity": ["Terror", "Fear", "Anxiety", "Responsiveness", "Eagerness", "Enthusiasm"],
}


def get_senticnet_response(text: str):
    response = requests.get(APIURL + text)
    result = {
        "status_code": response.status_code,
        "content": response.content.decode()
    }
    if result["status_code"] == 200:
        introspection_value = get_dimension_value(result["content"], 2)
        temper_value = get_dimension_value(result["content"], 3)
        attitude_value = get_dimension_value(result["content"], 4)
        sensitivity_value = get_dimension_value(result["content"], 5)
        result.update({
            "introspection": {
                "value": introspection_value,
                "emotion": get_emotion(introspection_value, "introspection")
            },
            "temper": {
                "value": temper_value,
                "emotion": get_emotion(temper_value, "temper")
            },
            "attitude": {
                "value": attitude_value,
                "emotion": get_emotion(attitude_value, "attitude")
            },
            "sensitivity": {
                "value": sensitivity_value,
                "emotion": get_emotion(sensitivity_value, "sensitivity")
            }
        })
    return result


def get_dimension_value(output: str, index: int):
    result = re.findall(r'-*[0-9]+\.[0-9]+', output)
    return float(result[index]) / 100


def get_emotion(value: float, dimension: str):
    if value >= -1 and value < -2 / 3:
        return SENTIC_LEVELS[dimension][0]
    if value >= -2 / 3 and value < -1 / 3:
        return SENTIC_LEVELS[dimension][1]
    if value >= -1 / 3 and value < 0:
        return SENTIC_LEVELS[dimension][2]
    if value >= 0 and value < 1 / 3:
        return SENTIC_LEVELS[dimension][3]
    if value >= 1 / 3 and value < 2 / 3:
        return SENTIC_LEVELS[dimension][4]
    if value >= 2 / 3 and value <= 1:
        return SENTIC_LEVELS[dimension][5]

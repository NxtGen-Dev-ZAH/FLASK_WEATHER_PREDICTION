import requests
import json


def emotion_detector(text_to_analyze):
    url = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    data = {"raw_document": {"text": text_to_analyze}}
    response = requests.post(url, headers=headers, json=data)
    response_dict = json.loads(response.text)
    emotions = {
            "anger": response_dict["emotionPredictions"][0]["emotion"]["anger"],
            "disgust": response_dict["emotionPredictions"][0]["emotion"]["disgust"],
            "fear": response_dict["emotionPredictions"][0]["emotion"]["fear"],
            "joy": response_dict["emotionPredictions"][0]["emotion"]["joy"],
            "sadness": response_dict["emotionPredictions"][0]["emotion"]["sadness"],
        }
    dominant_emotion = max(emotions, key=emotions.get)
    emotions["dominant_emotion"] = dominant_emotion
    return emotions

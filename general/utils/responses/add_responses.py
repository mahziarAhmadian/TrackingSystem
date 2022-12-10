from general.models import Response
import json
from core.settings import BASE_DIR
import os


def load_response_json():
    json_filename = "response.json"
    json_path = os.path.join(BASE_DIR, 'general', 'utils', 'responses', json_filename)
    with open(json_path, 'r', encoding="utf8") as json_file:
        return json.load(json_file)


def add_responses():
    exist_responses = Response.objects.all()
    exist_responses.delete()

    json_responses = load_response_json()
    for response in json_responses:
        if response['status'] == 'success':
            response['status'] = 'S'
        elif response['status'] == 'failed':
            response['status'] = 'F'
        r = Response(**response)
        r.save()
    print("all responses was added to the database successfully!")

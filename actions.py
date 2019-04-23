from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet
import json
import os
import infermedica_api
import requests
import string

api = infermedica_api.API(app_id='bc1dd653',
                                  app_key='76b11cd1b2b2e684e261346544731fb7')

class ActionMed(Action):
    def name(self):
        return 'action_medicine'

    def run(self, dispatcher, tracker, domain):
        api = infermedica_api.API(app_id='bc1dd653',
                                  app_key='76b11cd1b2b2e684e261346544731fb7')

        choices = {}
        buttons = []
        symp = tracker.get_slot('symptom')
        request = infermedica_api.Diagnosis(sex='male', age='25')

        symp = api.parse(symp).to_dict()
        symp_id = symp['mentions'][0]['id']
        request.add_symptom(symp_id, 'present')

        request = api.diagnosis(request)
        items = request.question.items

        #dispatcher.utter_message(items)
        for choice in items:
            choices[choice['id']] = choice['name']

        for key, value in choices.items():
            title = value
            #payload = ('/slot{\"choice\": ' + key + '}')
            #buttons.append({"title": title, "payload": payload})
            request.add_symptom(key, 'present')
            request = api.diagnosis(request)
            text = request.question.text
        #  response = "Let's try this medicine"
        dispatcher.utter_message(text)
        #dispatcher.utter_button_message(response, buttons)
        return [SlotSet('symptom', symp)]

class ActionDig(Action):
    def name(self):
        return 'action_diagnosis'

    def run(self, dispatcher, tracker, domain):
        api = infermedica_api.API(app_id='bc1dd653',
                                  app_key='76b11cd1b2b2e684e261346544731fb7')

        rr = tracker.get_slot('symptom')
        request = infermedica_api.Diagnosis(sex='male', age='25')
        rr = api.parse(rr).to_dict()
        rr_id = rr['mentions'][0]['id']
        request.conditions.to_dict()
        request = api.diagnosis(request)

        dispatcher.utter_message(request)
        return [SlotSet('diagnosis',rr)]


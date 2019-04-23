from rasa_core.channels.socketio import SocketIOInput
from rasa_core.agent import Agent
from rasa_core.interpreter import NaturalLanguageInterpreter
from flask import Blueprint, request, render_template
from rasa_core.events import SlotSet
from flask_cors import CORS
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.policies.fallback import FallbackPolicy
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.utils import EndpointConfig

from bot_server_channel import BotServerInputChannel

# Creating the Interpreter and Agent
def load_agent():


    interpreter = RasaNLUInterpreter('./models/current/healthbot')
    #agent = Agent()
    action_endpoint = EndpointConfig(url='http://localhost:5055/webhook')
    return Agent.load('./models/current/dialogue', interpreter=interpreter,
                   action_endpoint=action_endpoint)

# Creating the server
def main_server():
    agent = load_agent()

    channel = BotServerInputChannel(agent, port=5005)
    agent.handle_channels([channel], http_port=5005)

main_server()

from rasa_nlu.model import Interpreter

interpreter = Interpreter.load('./models/default/healthbot')

response = interpreter.parse('Will you be calling me Qasim or someone else?')

print(response)

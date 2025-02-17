from use_cases.nlu_use_cases import ProcessUserMessage  # Importar ProcessUserMessage

class DialogManager:
    def __init__(self, user_id):
        self.user_id = user_id

    def process_message(self, text):
        # Crear una instancia de ProcessUserMessage
        use_case = ProcessUserMessage()

        # Procesar el mensaje y obtener la intención y entidades
        result = use_case.execute(text)
        intent = result["intent"]
        entities = result["entities"]

        # Generar una respuesta basada en la intención
        if intent == "saludo":
            response = "¡Hola! ¿En qué puedo ayudarte?"
        elif intent == "despedida":
            response = "¡Adiós! Que tengas un buen día."
        elif intent == "pregunta":
            response = "Has hecho una pregunta. Estoy procesando tu consulta."
        else:
            response = "Mensaje procesado."

        return response
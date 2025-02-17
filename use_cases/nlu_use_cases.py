# use_cases/nlu_use_cases.py

import spacy
from googletrans import Translator
import re
from entities.models import UserMessage
from .sharepoint_use_cases import SharePointUseCases  # Importar los casos de uso de SharePoint

# Cargar el modelo de spaCy para español
nlp = spacy.load("es_core_news_sm")

# Crear una instancia de Translator
translator = Translator()

class ProcessUserMessage:
    def __init__(self):
        """
        Inicializa el procesador de mensajes del usuario.
        """
        self.sharepoint_use_cases = SharePointUseCases()  # Inicializar los casos de uso de SharePoint

    def execute(self, text: str, language: str = "es"):
        """
        Procesa un mensaje del usuario y genera una respuesta.
        
        :param text: Texto del mensaje del usuario.
        :param language: Idioma deseado para la respuesta.
        :return: Diccionario con la intención, entidades, mensaje y respuesta.
        """
        # Detectar el idioma del texto
        detected_language = translator.detect(text).lang

        # Traducir el texto al idioma deseado
        if detected_language != language:
            translated_text = translator.translate(text, dest=language).text
        else:
            translated_text = text

        # Procesar el texto (identificar intenciones y entidades)
        doc = nlp(translated_text)
        intent = self.detect_intent(doc)
        entities = self.extract_entities(doc)

        # Guardar el mensaje en la base de datos
        message = UserMessage.objects.create(
            text=translated_text,
            language=language,
            intent=intent,
            entities=entities
        )

        # Si la intención es una pregunta, buscar en SharePoint
        if intent == "pregunta":
            response = self.handle_question(translated_text)
            return {"intent": intent, "entities": entities, "message": translated_text, "response": response}
        else:
            return {"intent": intent, "entities": entities, "message": translated_text}

    def detect_intent(self, doc):
        """
        Detecta la intención del mensaje del usuario.
        
        :param doc: Documento de spaCy con el texto procesado.
        :return: Intención detectada (saludo, despedida, pregunta).
        """
        # Convertir el texto a minúsculas para hacer la comparación insensible a mayúsculas
        text = doc.text.lower()

        # Expresiones regulares para saludos y despedidas
        saludo_regex = re.compile(r"\b(hola|buenos\s*días|buenas\s*tardes|buenas\s*noches|saludos|qué\s*tal)\b")
        despedida_regex = re.compile(r"\b(adios|adiós|chao)\b")

        if saludo_regex.search(text):
            return "saludo"
        elif despedida_regex.search(text):
            return "despedida"
        else:
            return "pregunta"

    def extract_entities(self, doc):
        """
        Extrae entidades del mensaje del usuario.
        
        :param doc: Documento de spaCy con el texto procesado.
        :return: Lista de entidades encontradas.
        """
        entities = []
        for ent in doc.ents:
            entities.append({"text": ent.text, "label": ent.label_})
        return entities

    def handle_question(self, question):
        """
        Maneja una pregunta del usuario buscando información en SharePoint.
        
        :param question: Pregunta del usuario.
        :return: Respuesta generada basada en la información de SharePoint.
        """
        # Extraer palabras clave de la pregunta
        keywords = self.extract_keywords(question)
        
        # Buscar información en SharePoint usando las palabras clave
        search_results = self.sharepoint_use_cases.get_document_info(keywords)
        
        # Generar una respuesta basada en los resultados
        if search_results:
            return self.generate_response(search_results)
        else:
            return "Lo siento, no pude encontrar información relevante."

    def extract_keywords(self, question):
        """
        Extrae palabras clave de la pregunta del usuario.
        
        :param question: Pregunta del usuario.
        :return: Palabras clave extraídas.
        """
        doc = nlp(question)
        keywords = [token.text for token in doc if token.is_alpha and not token.is_stop]
        return " ".join(keywords)

    def generate_response(self, search_results):
        """
        Genera una respuesta basada en los resultados de la búsqueda en SharePoint.
        
        :param search_results: Resultados de la búsqueda en SharePoint.
        :return: Respuesta generada.
        """
        response = "Encontré la siguiente información:\n"
        for result in search_results:
            response += f"- {result.properties['Name']}\n"
        return response
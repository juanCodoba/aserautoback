# frameworks/db/nlu_repository_impl.py
from interfaces.nlu_repository import NLURepository
from entities.models import UserMessage

class DjangoNLURepository(NLURepository):
    def process_message(self, text: str, language: str):
        return UserMessage.objects.create(text=text, language=language)
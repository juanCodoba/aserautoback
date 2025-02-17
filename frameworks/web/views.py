from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from use_cases.nlu_use_cases import ProcessUserMessage
from use_cases.dialog_use_cases import DialogManager
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
import json

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@csrf_exempt
def process_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            text = data.get('text')
            user_id = data.get('user_id', 'default_user')  # Identificador del usuario
        except json.JSONDecodeError:
            return JsonResponse({"error": "Cuerpo de la solicitud no válido"}, status=400)

        if not text:
            return JsonResponse({"error": "El campo 'text' es requerido"}, status=400)

        # Crear una instancia de DialogManager y procesar el mensaje
        dialog_manager = DialogManager(user_id)
        response = dialog_manager.process_message(text)

        # Devolver la intención y la respuesta
        return JsonResponse({"response": response})
    return JsonResponse({"error": "Método no permitido"}, status=405)
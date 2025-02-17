# use_cases/sharepoint_use_cases.py

from frameworks.sharepoint.client import SharePointClient

class SharePointUseCases:
    def __init__(self):
        """
        Inicializa los casos de uso de SharePoint.
        """
        self.sharepoint_client = SharePointClient(
            client_id="ed5dad09-911c-4b7a-8efe-e6f09b0f7974",  # Reemplaza con tu Client ID
            client_secret="ENr8Q~wS2Pi~ricGAg52OddnR6fs3d1ksq0ucbeU",  # Reemplaza con tu Client Secret
            tenant_id="dd505be5-ec69-47f5-92df-caa55febf5fa",  # Reemplaza con tu Tenant ID
            site_url="https://poligran.sharepoint.com/sites/PruebaChatGPTSharepoint/Datos%20Relevantes"  # Reemplaza con la URL de tu sitio
        )

    def get_document_info(self, query):
        """
        Busca información en SharePoint basada en una consulta.
        
        :param query: Palabras clave para la búsqueda.
        :return: Información relevante encontrada en SharePoint.
        """
        return self.sharepoint_client.search_documents(query)
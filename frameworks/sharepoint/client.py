import msal
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext

class SharePointClient:
    def __init__(self, client_id, client_secret, tenant_id, site_url):
        """
        Inicializa el cliente de SharePoint.
        
        :param client_id: ID de la aplicación registrada en Azure AD.
        :param client_secret: Secreto de la aplicación.
        :param tenant_id: ID del tenant de Azure AD.
        :param site_url: URL del sitio de SharePoint.
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.site_url = site_url
        self.ctx = self._connect_to_sharepoint()

    def _get_access_token(self):
        """
        Obtiene un token de acceso usando MSAL.
        """
        app = msal.ConfidentialClientApplication(
            self.client_id,
            authority=f"https://login.microsoftonline.com/{self.tenant_id}",
            client_credential=self.client_secret
        )
        result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
        if "access_token" in result:
            return result["access_token"]
        else:
            raise Exception("Error al obtener el token de acceso: " + str(result.get("error_description")))

    def _connect_to_sharepoint(self):
        """
        Conecta a SharePoint usando el token de acceso.
        """
        access_token = self._get_access_token()
        ctx_auth = AuthenticationContext(self.site_url)
        
        # Autenticación usando el token de acceso
        ctx_auth.acquire_token(
            client_id=self.client_id,
            client_secret=self.client_secret
        )
        
        ctx = ClientContext(self.site_url, ctx_auth)
        return ctx

    def search_documents(self, query):
        """
        Busca documentos en SharePoint basados en una consulta.
        
        :param query: Palabras clave para la búsqueda.
        :return: Resultados de la búsqueda.
        """
        try:
            # Ejemplo: Buscar en una carpeta específica
            folder = self.ctx.web.get_folder_by_server_relative_url("/sites/tusitio/Documentos%20Compartidos")
            self.ctx.load(folder)
            self.ctx.execute_query()

            # Filtrar archivos que coincidan con la consulta
            files = folder.files
            self.ctx.load(files)
            self.ctx.execute_query()

            results = []
            for file in files:
                if query.lower() in file.properties["Name"].lower():
                    results.append(file)

            return results
        except Exception as e:
            raise Exception(f"Error al buscar documentos en SharePoint: {str(e)}")
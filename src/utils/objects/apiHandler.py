from requests.sessions import Session
from . import querySerializer
from . import mainExecutable
from ..blocks import *

class handler():
    def __init__(self):
        # Cambiar de un dominio externo a una ruta local
        # Puedes ajustar 'self.ROOT' a una carpeta local si es necesario
        # o dejarlo vacío si no necesitas rutas específicas.
        self.ROOT = "file://localhost/path/to/local/data"  # Cambia este valor a la ruta local deseada
        self.RP = mainExecutable.Generator.selector(querySerializer.cursor().getConfig("libs")[2])
        self.SYS = mainExecutable.Generator.selector(querySerializer.cursor().getConfig("libs")[4])
        self.RQ = mainExecutable.Generator.selector(querySerializer.cursor().getConfig("libs")[3])

    def pull(self):
        DIRREPO = self.SYS.path.join(querySerializer.cursor().hereFile, "..", "..", "..")
        repo = self.RP.Repo(DIRREPO)
        configUser = self.SYS.path.join(DIRREPO, "src", "config", "config.json")

        try:
            # Stash changes to config.json if there are any
            if repo.is_dirty(path=configUser):
                repo.git.stash('save', 'Auto stash config.json before pull', configUser)

            # Perform the pull
            repo.remotes.origin.pull()
            
            # Restore the stashed config.json if it was stashed
            stashes = repo.git.stash('list')
            if 'Auto stash config.json before pull' in stashes:
                repo.git.stash('pop')

        except self.RP.exc.GitCommandError as e:
            animERROR(f"Git pull failed: {e}")
            raise

    def deprecated(self) -> dict:
        echo = str(self.RP.Repo(self.SYS.path.join(querySerializer.cursor().hereFile, "..", "..", "..")).head.commit.hexsha)
        # Para evitar el uso de la API de GitHub, puedes comparar commits de manera local
        # Aquí podrías usar un archivo local o una configuración para manejar versiones locales
        # Ejemplo básico si tienes un archivo local con el hash del último commit:
        local_hash = "a1b2c3d4e5f6"  # Usa tu hash local en vez de conectar a GitHub
        return {'STTS': echo != local_hash}

    def getNews(self) -> list:
        try:
            # Usa un archivo local JSON o similar en lugar de conectarte a un servidor externo
            local_path = self.SYS.path.join("local_data", "news.json")
            with open(local_path, "r") as file:
                rsp = json.load(file)
        except Exception as Error:
            return []
        else:
            return rsp.get("news", [])

    def api(self) -> Session:
        # Si necesitas la funcionalidad de 'requests', mantenla
        return self.RQ.session()
    
    def joinerDirs(self, listData: list) -> str:
        # Ajustar para construir rutas locales en lugar de URLs remotas
        subdirs = "/".join(listData)
        DIR = self.SYS.path.join("local_data", subdirs)  # Ajustar para rutas locales
        return DIR 

    def listDataRequirements(self) -> list:
        # Ajusta las rutas a archivos locales en vez de URLs remotas
        return ([
            handler().joinerDirs(["DisponibleValor", "agregarName.json"]),
            handler().joinerDirs(["DisponibleValor", "upload.json"]),
            handler().joinerDirs(["DisponibleValor", "Comprobantes", "descargar.json"])
        ], ["NumeroNequi", "Nombre", "Valor"])

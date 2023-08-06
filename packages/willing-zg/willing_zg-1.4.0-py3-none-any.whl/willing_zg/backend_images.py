from zygoat.components import Component, FileComponent
from zygoat.constants import Projects

from . import resources


class BackendBaseImages(Component):
    pass


class DevImage(FileComponent):
    resource_pkg = resources
    base_path = Projects.BACKEND
    overwrite = True
    filename = "Dockerfile.local"


class ProdImage(DevImage):
    filename = "Dockerfile"


backend_images = BackendBaseImages(sub_components=[DevImage(), ProdImage()])

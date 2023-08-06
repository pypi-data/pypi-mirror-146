from zygoat.components import Component
from zygoat.components.backend.reformat import reformat

from .tokens import token_util
from .django_willing_zg import django_willing_zg
from .google_analytics import google_analytics
from .get_env import get_env_util
from .idle_session_handler import idle_session_handler
from .backend_images import backend_images


class AllComponents(Component):
    pass


all_components = AllComponents(
    sub_components=[
        token_util,
        reformat,
        get_env_util,
        django_willing_zg,
        google_analytics,
        idle_session_handler,
        backend_images,
    ]
)

from .forge_v1 import RepositoryV1 as RepositoryV1
from .forge_v1 import TemplateV1 as TemplateV1

ALL_EXPORTABLE_FORGE = RepositoryV1 | TemplateV1

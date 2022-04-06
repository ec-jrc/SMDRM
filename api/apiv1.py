from flask import Blueprint
from flask_restx import Api

# API namespaces
from api.namespaces.infov1 import ns as info_ns
from api.namespaces.uploadv1 import ns as upload_ns

# API main blueprint setting root and version
blueprint = Blueprint("api", __name__, url_prefix='/api/v1')

# API instance
api = Api(
    blueprint,
    title='SMDRM API',
    version='1.0',
    description='Allows the end-user to interacts with the SMDRM components.',
    # All API metadatas
)

# add namespaces to API
api.add_namespace(info_ns)
api.add_namespace(upload_ns)

from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.images.api.v2.views import ImagesAPIViewSet
from wagtail.documents.api.v2.views import DocumentsAPIViewSet


class CustomPagesAPIViewSet(PagesAPIViewSet):
    """
    Custom Pages API ViewSet that exposes custom page fields
    """
    # Don't override body_fields - let api_fields in models handle it
    pass


# Create the router
api_router = WagtailAPIRouter('pages_api')

# Add the endpoints
api_router.register_endpoint('pages', CustomPagesAPIViewSet)
api_router.register_endpoint('images', ImagesAPIViewSet)
api_router.register_endpoint('documents', DocumentsAPIViewSet)

from rest_framework import routers
from .views import PasswordViewSet

router = routers.SimpleRouter()
router.register(r"passwords", PasswordViewSet)
urlpatterns = router.urls

from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'directors',DirectorsView)
router.register(r'movies',MoviesView)
router.register(r'plans',PlansView)

urlpatterns = router.urls


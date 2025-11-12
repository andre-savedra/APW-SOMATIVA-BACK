from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'directors',DirectorView)
router.register(r'movies',MovieView)
router.register(r'plans',PlanView)
router.register(r'user-plans',UserPlanView)
router.register(r'favorites',FavoriteMovieView)

urlpatterns = router.urls
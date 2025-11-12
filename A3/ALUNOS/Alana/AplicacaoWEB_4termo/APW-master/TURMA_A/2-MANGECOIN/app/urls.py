from .views import *
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'users', CustomUserView)
router.register(r'tokens', TokenView)
router.register(r'accounts/tokens', AccountTokenView)
router.register(r'accounts', AccountView)
router.register(r'bets', BetsView)
router.register(r'transactions', TransactionsView)

urlpatterns = router.urls
urlpatterns.append(path('bets/try', BetTryView.as_view(), name='bet-try'))
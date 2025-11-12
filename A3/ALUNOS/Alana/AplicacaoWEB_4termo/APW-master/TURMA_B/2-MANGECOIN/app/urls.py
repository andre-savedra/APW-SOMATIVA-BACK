from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register(r'users', CustomUserView)
router.register(r'tokens', TokenView)
router.register(r'accounts/tokens', AccountTokenView)
router.register(r'accounts', AccountView)
router.register(r'bets', BetView)
router.register(r'transactions', TransactionView)

urlpatterns = router.urls
urlpatterns.append(path('bets/try', BetTryView.as_view(), name='bet-try'))
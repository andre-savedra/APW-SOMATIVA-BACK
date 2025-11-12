# app/views/__init__.py (Versão Limpa)

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django.utils import timezone
from datetime import timedelta

from ..models.customuser import Funcionario, Cargo  
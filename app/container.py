# containers.py
from dependency_injector import containers, providers
import sys

from .serv import server
from socketio_views import socketio_views

class ServerContainer(containers.DeclarativeContainer):
    user_service = providers.Singleton(server)

class SocketIOViewsContainer(containers.DeclarativeContainer):
    user_service = providers.Singleton(socketio_views)
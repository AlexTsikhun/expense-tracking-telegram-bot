from bot.services.api import APIService
from bot.services.file import FileService
from bot.services.http_client import HttpClient
from config import settings

http_client = HttpClient(settings.API_URL)
api_service = APIService(http_client)
file_service = FileService()

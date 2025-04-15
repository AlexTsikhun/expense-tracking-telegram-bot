from bot.services.api import APIService
from bot.services.file import FileService
from bot.services.http_client import HttpClient

http_client = HttpClient()
api_service = APIService(http_client)
file_service = FileService()

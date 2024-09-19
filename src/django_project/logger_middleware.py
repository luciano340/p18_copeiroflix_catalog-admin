
import json
import os
from src._shared.logger import get_logger
from django.urls import resolve

logger = get_logger(__name__)

class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        resolver_match = resolve(request.path)
        route_name = resolver_match.view_name if resolver_match.view_name else 'Rota desconhecida'
        logger.info(f'Request recebido: {request.path} - {route_name} - {request.method}')

        if os.getenv("LOGLEVEL", "DEBUG") == "DEBUG":
            try:
                query_params = request.GET.dict()
                body_params = request.POST.dict() if request.method in ["POST", "PUT", "PATCH"] else {}
                raw_body = request.body.decode('utf-8') if request.body else None
                headers = {k: v for k, v in request.headers.items()}
                cookies = {k: v for k, v in request.COOKIES.items()}
                session_data = {k: v for k, v in request.session.items()} if request.session else {}

                # Logando as informações
                log_message = (
                    f"Request Information:\n"
                    f"  Method          : {request.method}\n"
                    f"  Path            : {request.path}\n"
                    f"  Route           : {route_name}\n"
                    f"  Query Params    : {json.dumps(query_params, indent=2)}\n"
                    f"  Body Params     : {json.dumps(body_params, indent=2)}\n"
                    f"  Request Body    : {raw_body}\n"
                    f"  Headers         : {json.dumps(headers, indent=2)}\n"
                    f"  Cookies         : {json.dumps(cookies, indent=2)}\n"
                    f"  Session Data    : {json.dumps(session_data, indent=2)}\n"
                    f"  Content-Type    : {request.content_type}\n"
                    f"  Encoding        : {request.encoding}\n"
                    f"  Client IP       : {request.META.get('REMOTE_ADDR')}\n"
                    f"  User-Agent      : {request.META.get('HTTP_USER_AGENT')}\n"
                    f"  Secure          : {'HTTPS' if request.is_secure() else 'HTTP'}"
                )
                logger.debug(log_message)
            except Exception as e:
                logger.error(f"Erro ao logar request: {e}")
            
        response = self.get_response(request)
        logger.info(f'Response enviado: {response.status_code} para {request.path} - {route_name}')

        return response
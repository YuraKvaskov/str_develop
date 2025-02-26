from django.http import JsonResponse

class InternalRequestMiddleware:
    """
    Middleware, который запрещает доступ к API, если запрос не прошёл через Nginx.
    Nginx добавляет заголовок X-Internal-Request, который проверяется здесь.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Проверяем, начинается ли запрос с /api/
        if request.path.startswith("/api/"):
            # Проверяем заголовок X-Internal-Request, который добавляет Nginx
            internal_header = request.headers.get("X-Internal-Request")

            # Если заголовка нет или он неверный – запретить доступ
            if internal_header != "allowed":
                return JsonResponse({"error": "Unauthorized"}, status=403)

        return self.get_response(request)

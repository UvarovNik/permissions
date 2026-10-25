from rest_framework.settings import api_settings
from rest_framework.throttling import UserRateThrottle


class CustomRateThrottle(UserRateThrottle):
    """
    Кастомный throttle, который возвращает разный лимит
    для авторизованных и неавторизованных пользователей.
    """

    def __init__(self):
        self.history = None
        self.cache = None
        self.rate = None

    def get_rate(self):
        """Определяем rate на основе авторизации пользователя."""
        if not getattr(self, 'scope', None):
            return None

        THROTTLE_RATES = api_settings.THROTTLE_RATES
        return THROTTLE_RATES[self.scope]

    def allow_request(self, request, view):
        if request.user.is_authenticated:
            self.scope = 'authenticated'
        else:
            self.scope = 'anonymous'
        return super().allow_request(request, view)

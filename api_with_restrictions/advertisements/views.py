from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement
from advertisements.serializers import AdvertisementSerializer


class IsAuthorOrAdmin(BasePermission):
    """Разрешение: только автор объявления или админ."""

    def has_permission(self, request, view):
        # Админы имеют доступ всегда
        if request.user.is_authenticated and request.user.is_staff:
            return True
        # Для чтения (list, retrieve) — доступ всем
        if view.action in ['list', 'retrieve']:
            return True
        # Для изменения/удаления — нужна авторизация
        if not request.user.is_authenticated:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        # Админы имеют доступ к любому объекту
        if request.user.is_staff:
            return True
        # Автор может менять и удалять своё объявление
        return obj.creator == request.user


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update"]:
            return [IsAuthenticated()]
        if self.action == "destroy":
            return [IsAuthorOrAdmin()]
        return []

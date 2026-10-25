from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement, AdvertisementStatusChoices


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', 'updated_at')

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        request = self.context.get("request")

        if request and request.user.is_authenticated:
            # Проверяем количество открытых объявлений пользователя
            # При создании — новое объявление ещё не в БД, поэтому учитываем +1
            count = Advertisement.objects.filter(
                creator=request.user,
                status=AdvertisementStatusChoices.OPEN
            ).count()

            # Если это обновление существующего объявления, которое уже OPEN,
            # и статус не меняется — не учитываем его в лимите
            instance = self.instance
            if instance and instance.status == Advertisement.status_choices.OPEN:
                count -= 1

            # Если в данных указан новый статус OPEN, проверяем лимит
            new_status = data.get('status', instance.status if instance else AdvertisementStatusChoices.OPEN)
            if new_status == AdvertisementStatusChoices.OPEN and count >= 10:
                raise serializers.ValidationError(
                    "У вас не может быть больше 10 открытых объявлений."
                )

        return data

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, ProfileSerializer
from .models import User, Profile
from .UserPermissions import IsAuthenticatedOrOnlyCreate
from rest_framework.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)


class UserModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticatedOrOnlyCreate]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        # Extraer datos del perfil si están presentes
        user_data = request.data
        profile_data = user_data.pop("profile", None)

        # Validar el serializador principal
        serialized = UserSerializer(data=user_data)
        if serialized.is_valid():
            # Crear el usuario
            new_user = User.objects.create_user(
                username=serialized.validated_data["username"],
                email=serialized.validated_data.get("email"),
                password=user_data["password"],
            )

            # Crear el perfil si se proporcionaron datos del perfil
            if profile_data:
                profile_serializer = ProfileSerializer(data=profile_data)
                if profile_serializer.is_valid():
                    Profile.objects.create(
                        user=new_user, **profile_serializer.validated_data
                    )
                else:
                    # Devolver errores si el perfil no es válido
                    raise ValidationError(profile_serializer.errors)

            return Response(
                {"message": "User created successfully"},
                status=status.HTTP_201_CREATED,
            )

        # Devolver errores si la validación del usuario falla
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        user_with_pk = self.get_object()
        if user_with_pk.pk != request.user.pk and not request.user.is_staff:
            return Response({"message": "This operation is only allowed fro, staff"})

        serialized = UserSerializer(data=user_with_pk)
        if serialized.is_valid():
            return Response(serialized.data, status.HTTP_200_OK)
        return Response(
            {"message": "Need authenticated to get user"}, status.HTTP_401_UNAUTHORIZED
        )

    def update(self, request, *args, **kwargs):

        user_with_pk = self.get_object()
        if user_with_pk.pk != request.user.pk and not request.user.is_staff:
            return Response({"message": "This operation is only allowed fro, staff"})

        user_data = request.data
        profile_data = user_data.pop("profile", None)

        user_serialized = self.get_serializer(
            user_with_pk, data=user_data, partial=False
        )
        user_serialized.is_valid(raise_exception=True)
        self.perform_update(user_serialized)

        if profile_data:
            current_profile = getattr(user_with_pk, "profile")
            profile_serialized = ProfileSerializer(
                current_profile, data=profile_data, partial=False
            )

            profile_serialized.is_valid(raise_exception=True)
            profile_serialized.save()

        return Response(user_serialized.data, status=status.HTTP_200_OK)
        return Response("ok", status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        if request.user and not request.user.is_staff:
            return Response(
                {"message": "This action is only allowed to staff"},
                status=status.HTTP_403_FORBIDDEN,
            )
        user_list_serialized = UserSerializer(self.get_queryset(), many=True)
        return Response(user_list_serialized.data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        user_with_pk = self.get_object()
        if user_with_pk.pk != request.user.pk and not request.user.is_staff:
            return Response({"message": "This operation is only allowed fro, staff"})

        user_data = request.data
        profile_data = user_data.pop("profile")
        user_serialized = UserSerializer(user_with_pk, data=user_data, partial=True)
        user_serialized.is_valid(raise_exception=True)
        user_serialized.save()
        if profile_data:
            profile_serialized = ProfileSerializer(
                user_with_pk.profile, data=profile_data, partial=True
            )
            profile_serialized.is_valid(raise_exception=True)
            profile_serialized.save()
        return Response(user_serialized.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        user_with_pk = self.get_object()
        if user_with_pk.pk != request.user.pk and not request.user.is_staff:
            return Response({"message": "This operation is only allowed fro, staff"})

        user_with_pk = self.get_object()
        user_with_pk.is_active = False
        user_with_pk.save()
        return Response(
            {"message": "User deleted successful"}, status=status.HTTP_200_OK
        )

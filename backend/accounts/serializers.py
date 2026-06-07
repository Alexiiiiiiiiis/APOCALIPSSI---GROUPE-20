"""
Sérialiseurs pour l'app accounts.

[Note pédagogique] Choix « email = identifiant » : à l'inscription on ne demande
QUE l'email + le mot de passe ; en interne, username = email. Le login se fait
donc par email. On gère explicitement les doublons d'email avec un message clair.
"""
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password as django_validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from .models import Profile, get_or_create_profile


class UserSerializer(serializers.ModelSerializer):
    """Serializer en lecture pour l'utilisateur connecté."""

    email_verified = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name",
                  "date_joined", "email_verified"]
        read_only_fields = fields

    def get_email_verified(self, obj) -> bool:
        return get_or_create_profile(obj).email_verified


class SignupSerializer(serializers.ModelSerializer):
    """Inscription par EMAIL (identifiant). Le username interne = email."""

    password = serializers.CharField(
        write_only=True, min_length=8,
        style={"input_type": "password"}, help_text="Au moins 8 caractères.",
    )

    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name"]
        extra_kwargs = {
            "email":      {"required": True, "allow_blank": False},
            "first_name": {"required": False},
            "last_name":  {"required": False},
        }

    def validate_email(self, value: str) -> str:
        value = value.strip().lower()
        # L'email est l'identifiant -> il doit être unique (sur email ET username).
        if (User.objects.filter(email__iexact=value).exists()
                or User.objects.filter(username__iexact=value).exists()):
            raise serializers.ValidationError(
                "Un compte existe déjà avec cet email. Connectez-vous, ou "
                "utilisez « mot de passe oublié » pour le réinitialiser."
            )
        return value

    def validate_password(self, value: str) -> str:
        try:
            django_validate_password(value)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(list(exc.messages))
        return value

    def create(self, validated_data: dict) -> User:
        password = validated_data.pop("password")
        email = validated_data["email"]
        user = User(username=email, **validated_data)  # username = email (identifiant)
        user.set_password(password)
        user.save()
        get_or_create_profile(user)  # profil avec email_verified=False
        return user


class LoginSerializer(serializers.Serializer):
    """Authentification par EMAIL + mot de passe."""

    email = serializers.CharField()
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    def validate(self, attrs: dict) -> dict:
        email = attrs.get("email", "").strip().lower()
        password = attrs.get("password")

        # On retrouve l'utilisateur par email (insensible à la casse), puis on
        # authentifie via son username réel. Cela fonctionne aussi pour les
        # comptes anciens dont le username diffère de l'email.
        user_obj = User.objects.filter(email__iexact=email).first()
        username = user_obj.username if user_obj else email

        user = authenticate(
            request=self.context.get("request"), username=username, password=password
        )
        if user is None:
            raise serializers.ValidationError("Email ou mot de passe invalide.")
        if not user.is_active:
            raise serializers.ValidationError("Ce compte est désactivé.")
        attrs["user"] = user
        return attrs


class PasswordResetRequestSerializer(serializers.Serializer):
    """Demande de réinitialisation : juste l'email."""
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Confirmation : uid + token (du lien email) + nouveau mot de passe."""
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(
        write_only=True, min_length=8, style={"input_type": "password"}
    )

    def validate_new_password(self, value: str) -> str:
        try:
            django_validate_password(value)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(list(exc.messages))
        return value


class EmailVerifySerializer(serializers.Serializer):
    """Validation d'email : le token reçu par email."""
    token = serializers.CharField()

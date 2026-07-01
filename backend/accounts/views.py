"""
Endpoints d'authentification (Lot 3 : email-identifiant + validation + reset).

    POST /api/accounts/signup/                  — créer un compte (par email)
    POST /api/accounts/login/                   — se connecter (par email) -> token
    POST /api/accounts/logout/                  — se déconnecter
    GET  /api/accounts/me/                       — utilisateur courant (+ email_verified)
    POST /api/accounts/verify-email/             — confirmer l'email (token du lien)
    POST /api/accounts/resend-verification/      — renvoyer l'email de validation
    POST /api/accounts/password-reset/           — demander un reset (envoie un email)
    POST /api/accounts/password-reset/confirm/   — définir le nouveau mot de passe
"""

import csv
import hashlib
import io
import json
import logging

from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.utils import timezone
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .emails import EmailError, send_password_reset_email, send_verification_email
from .models import DataRequest, get_or_create_profile
from .serializers import (
    ChangePasswordSerializer,
    DeleteAccountSerializer,
    EmailVerifySerializer,
    LoginSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    ProfileUpdateSerializer,
    SignupSerializer,
    UserSerializer,
)
from .tokens import read_email_verify_token, read_password_reset_tokens

logger = logging.getLogger(__name__)


SAR_SCOPE = [
    "account",
    "uploaded_courses",
    "generated_quizzes",
    "quiz_answers_and_scores",
    "reports",
    "audit_logs",
]


def _client_ip(request) -> str | None:
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def _build_user_export(user, include_audit: bool = True) -> dict:
    """Construit l'export Art. 15 strictement filtré sur l'utilisateur courant."""
    from quizzes.models import Quiz

    profile = get_or_create_profile(user)
    quizzes = Quiz.objects.filter(user=user).prefetch_related("questions").order_by("created_at")

    quiz_payload = []
    answers_payload = []
    for quiz in quizzes:
        questions = []
        for question in quiz.questions.all():
            q_payload = {
                "index": question.index,
                "prompt": question.prompt,
                "options": question.options,
                "correct_index": question.correct_index,
                "selected_index": question.selected_index,
                "is_correct": (
                    None
                    if question.selected_index is None
                    else question.selected_index == question.correct_index
                ),
            }
            questions.append(q_payload)
            answers_payload.append(
                {
                    "quiz_id": quiz.id,
                    "quiz_title": quiz.title,
                    "question_index": question.index,
                    "selected_index": question.selected_index,
                    "correct_index": question.correct_index,
                    "is_correct": q_payload["is_correct"],
                }
            )
        quiz_payload.append(
            {
                "id": quiz.id,
                "title": quiz.title,
                "score": quiz.score,
                "source_text": quiz.source_text,
                "created_at": quiz.created_at,
                "updated_at": quiz.updated_at,
                "questions": questions,
            }
        )

    audit_logs = []
    if include_audit:
        audit_logs = [
            {
                "id": dr.id,
                "requested_at": dr.requested_at,
                "responded_at": dr.responded_at,
                "status": dr.status,
                "export_format": dr.export_format,
                "file_hash": dr.file_hash,
                "scope": dr.scope,
            }
            for dr in DataRequest.objects.filter(user=user).order_by("-requested_at")[:50]
        ]

    return {
        "exported_at": timezone.now(),
        "format_version": "2026-07-j3bis-v1",
        "scope": SAR_SCOPE,
        "account": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "date_joined": user.date_joined,
            "email_verified": profile.email_verified,
            "is_active": user.is_active,
        },
        "uploaded_courses": [
            {
                "quiz_id": quiz["id"],
                "title": quiz["title"],
                "source_text": quiz["source_text"],
                "created_at": quiz["created_at"],
            }
            for quiz in quiz_payload
        ],
        "generated_quizzes": quiz_payload,
        "quiz_answers_and_scores": answers_payload,
        # Le modèle de signalement arrive en J4 ; on expose déjà la catégorie attendue.
        "reports": [],
        "audit_logs": audit_logs,
    }


def _json_bytes(payload: dict) -> bytes:
    return json.dumps(payload, cls=DjangoJSONEncoder, ensure_ascii=False, indent=2).encode("utf-8")


def _csv_bytes(payload: dict) -> bytes:
    """Export CSV machine-readable : une ligne par question/réponse."""
    buffer = io.StringIO()
    writer = csv.DictWriter(
        buffer,
        fieldnames=[
            "user_id",
            "email",
            "quiz_id",
            "quiz_title",
            "quiz_score",
            "quiz_created_at",
            "question_index",
            "question_prompt",
            "selected_index",
            "correct_index",
            "is_correct",
        ],
    )
    writer.writeheader()
    account = payload["account"]
    for quiz in payload["generated_quizzes"]:
        for question in quiz["questions"]:
            writer.writerow(
                {
                    "user_id": account["id"],
                    "email": account["email"],
                    "quiz_id": quiz["id"],
                    "quiz_title": quiz["title"],
                    "quiz_score": quiz["score"],
                    "quiz_created_at": quiz["created_at"],
                    "question_index": question["index"],
                    "question_prompt": question["prompt"],
                    "selected_index": question["selected_index"],
                    "correct_index": question["correct_index"],
                    "is_correct": question["is_correct"],
                }
            )
    return buffer.getvalue().encode("utf-8-sig")


class SignupView(APIView):
    """Inscription par email. Envoie l'email de validation (best-effort)."""

    permission_classes = [AllowAny]
    authentication_classes = []  # endpoint public : pas de CSRF via session (cf. LoginView)

    @extend_schema(request=SignupSerializer, responses={201: UserSerializer})
    def post(self, request):
        # Lot 8 : l'admin peut fermer les inscriptions depuis l'interface.
        from administration.models import SiteConfig

        if not SiteConfig.load().allow_signups:
            return Response(
                {"detail": "Les inscriptions sont actuellement fermées."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Validation SOFT : on tente d'envoyer l'email de confirmation, mais on
        # NE bloque PAS l'inscription si l'envoi échoue (clé Brevo expirée, etc.).
        try:
            send_verification_email(user)
        except EmailError as exc:
            logger.warning("Email de validation non envoyé pour %s : %s", user.email, exc)

        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """Connexion par email + mot de passe. Renvoie un token DRF + crée la session."""

    permission_classes = [AllowAny]
    # Endpoint PUBLIC (pré-auth) : on désactive l'authentification de requête.
    # Sinon DRF SessionAuthentication, dès qu'un cookie `sessionid` résiduel est
    # présent (posé par django_login au login précédent), impose un contrôle CSRF
    # et rejette l'appel : « CSRF Failed: CSRF token missing ». Le frontend
    # s'authentifie par token, pas par session — il n'envoie pas de jeton CSRF.
    authentication_classes = []

    @extend_schema(
        request=LoginSerializer, responses={200: OpenApiResponse(description="{ token, user }")}
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        token, _ = Token.objects.get_or_create(user=user)
        django_login(request, user)  # session utile pour la Swagger UI
        return Response({"token": token.key, "user": UserSerializer(user).data})


class LogoutView(APIView):
    """Déconnexion : invalide le token + détruit la session."""

    permission_classes = [IsAuthenticated]

    @extend_schema(responses={204: OpenApiResponse(description="Déconnexion réussie")})
    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        django_logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class MeView(APIView):
    """Renvoie l'utilisateur connecté (avec email_verified pour le bandeau front)."""

    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: UserSerializer})
    def get(self, request):
        return Response(UserSerializer(request.user).data)


class VerifyEmailView(APIView):
    """Confirme l'adresse email à partir du token reçu par email."""

    permission_classes = [AllowAny]
    authentication_classes = []  # endpoint public : pas de CSRF via session (cf. LoginView)

    @extend_schema(
        request=EmailVerifySerializer,
        responses={200: OpenApiResponse(description="Email confirmé")},
    )
    def post(self, request):
        serializer = EmailVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uid = read_email_verify_token(serializer.validated_data["token"])
        if uid is None:
            return Response(
                {"detail": "Lien de validation invalide ou expiré."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            return Response(
                {"detail": "Utilisateur introuvable."}, status=status.HTTP_400_BAD_REQUEST
            )

        profile = get_or_create_profile(user)
        profile.email_verified = True
        profile.save(update_fields=["email_verified"])
        return Response({"detail": "Adresse email confirmée avec succès."})


class ResendVerificationView(APIView):
    """Renvoie l'email de validation à l'utilisateur connecté."""

    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: OpenApiResponse(description="Email renvoyé")})
    def post(self, request):
        if get_or_create_profile(request.user).email_verified:
            return Response({"detail": "Votre email est déjà confirmé."})
        try:
            send_verification_email(request.user)
        except EmailError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_502_BAD_GATEWAY)
        return Response({"detail": "Email de validation renvoyé."})


class PasswordResetRequestView(APIView):
    """Demande de réinitialisation : envoie un email avec un lien (si le compte existe)."""

    permission_classes = [AllowAny]
    authentication_classes = []  # endpoint public : pas de CSRF via session (cf. LoginView)

    @extend_schema(
        request=PasswordResetRequestSerializer,
        responses={200: OpenApiResponse(description="Email envoyé si le compte existe")},
    )
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"].strip().lower()

        user = User.objects.filter(email__iexact=email).first()
        if user is not None:
            try:
                send_password_reset_email(user)
            except EmailError as exc:
                logger.warning("Email de reset non envoyé pour %s : %s", email, exc)

        # Anti-énumération : réponse IDENTIQUE que le compte existe ou non
        # (on ne révèle pas quels emails sont enregistrés).
        return Response(
            {
                "detail": "Si un compte existe pour cet email, un lien "
                "de réinitialisation vient d'être envoyé."
            }
        )


class PasswordResetConfirmView(APIView):
    """Définit le nouveau mot de passe à partir du lien (uid + token)."""

    permission_classes = [AllowAny]
    authentication_classes = []  # endpoint public : pas de CSRF via session (cf. LoginView)

    @extend_schema(
        request=PasswordResetConfirmSerializer,
        responses={200: OpenApiResponse(description="Mot de passe réinitialisé")},
    )
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = read_password_reset_tokens(
            serializer.validated_data["uid"], serializer.validated_data["token"]
        )
        if user is None:
            return Response(
                {"detail": "Lien de réinitialisation invalide ou expiré."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(serializer.validated_data["new_password"])
        user.save(update_fields=["password"])
        return Response({"detail": "Mot de passe réinitialisé. Vous pouvez vous connecter."})


# ---------------------------------------------------------------------------
# Gestion du profil (Lot 4)
# ---------------------------------------------------------------------------


class ProfileView(APIView):
    """Profil de l'utilisateur connecté : consulter, modifier, supprimer.

    GET    /api/accounts/profile/  — lire son profil
    PATCH  /api/accounts/profile/  — modifier prénom / nom / email
    DELETE /api/accounts/profile/  — supprimer définitivement son compte
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: UserSerializer})
    def get(self, request):
        return Response(UserSerializer(request.user).data)

    @extend_schema(request=ProfileUpdateSerializer, responses={200: UserSerializer})
    def patch(self, request):
        serializer = ProfileUpdateSerializer(instance=request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Si l'email a changé, on (re)envoie un email de validation (best-effort,
        # validation SOFT : on ne bloque pas si l'envoi échoue).
        if getattr(user, "_email_changed", False):
            try:
                send_verification_email(user)
            except EmailError as exc:
                logger.warning("Email de validation non renvoyé pour %s : %s", user.email, exc)

        return Response(UserSerializer(user).data)

    @extend_schema(
        request=DeleteAccountSerializer,
        responses={204: OpenApiResponse(description="Compte supprimé")},
    )
    def delete(self, request):
        # Suppression DURE (hard delete) : confirmée par le mot de passe.
        # J3-bis : l'export RGPD est disponible via /api/accounts/me/export/.
        serializer = DeleteAccountSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        user = request.user
        Token.objects.filter(user=user).delete()  # invalide le token courant
        django_logout(request)
        user.delete()  # supprime aussi le Profile (on_delete=CASCADE)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangePasswordView(APIView):
    """Changement de mot de passe (en étant connecté, avec l'ancien mot de passe)."""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=ChangePasswordSerializer,
        responses={200: OpenApiResponse(description="Mot de passe modifié")},
    )
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        user = request.user
        user.set_password(serializer.validated_data["new_password"])
        user.save(update_fields=["password"])

        # Changer le mot de passe invalide les tokens DRF existants : on en
        # régénère un pour que l'utilisateur reste connecté sans avoir à se
        # reconnecter manuellement.
        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user)
        return Response({"detail": "Mot de passe modifié.", "token": token.key})


class ExportMyDataView(APIView):
    """Export RGPD Art. 15/20 de l'utilisateur authentifié.

    GET /api/accounts/me/export/?format=json|csv
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: OpenApiResponse(description="Export RGPD JSON ou CSV")})
    def get(self, request):
        export_format = (request.query_params.get("format") or "json").lower()
        if export_format not in {"json", "csv"}:
            return Response(
                {"detail": "Format non supporté. Utilisez json ou csv."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data_request = DataRequest.objects.create(
            user=request.user,
            status=DataRequest.Status.PROCESSING,
            export_format=export_format,
            scope=SAR_SCOPE,
            ip_address=_client_ip(request),
            user_agent=request.META.get("HTTP_USER_AGENT", "")[:1000],
        )

        try:
            payload = _build_user_export(request.user)
            if export_format == "csv":
                content = _csv_bytes(payload)
                content_type = "text/csv; charset=utf-8"
                extension = "csv"
            else:
                content = _json_bytes(payload)
                content_type = "application/json; charset=utf-8"
                extension = "json"

            file_hash = hashlib.sha256(content).hexdigest()
            data_request.status = DataRequest.Status.RESPONDED
            data_request.responded_at = timezone.now()
            data_request.file_hash = file_hash
            data_request.save(update_fields=["status", "responded_at", "file_hash"])

            filename = f"edututor-export-{request.user.id}-{timezone.now():%Y%m%d%H%M%S}.{extension}"
            response = HttpResponse(content, content_type=content_type)
            response["Content-Disposition"] = f'attachment; filename="{filename}"'
            response["X-Export-SHA256"] = file_hash
            return response
        except Exception:
            data_request.status = DataRequest.Status.FAILED
            data_request.responded_at = timezone.now()
            data_request.save(update_fields=["status", "responded_at"])
            raise

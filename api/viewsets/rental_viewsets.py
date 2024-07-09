""" Viewsets for rental models."""

from django.db import connection
from django.db.models import Q, Min, Max, F, Case, When, IntegerField, BooleanField
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, filters
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.pagination import PageNumberPagination

from api.filters import RentalFilterSet
from api.serializers.rental_serializers import (
    CategorySerializer,
    CreateRentalSerializer,
    ChatSerializer,
    DetailRentalSerializer,
    ListRentalSerializer,
    CreateCategorySerializer,
    NotificationSerializer,
    MarkReadSerializer,
)
from rentals.models import Category, Chat, Rental, Notification


@extend_schema(tags=["Category"])
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@extend_schema(tags=["Rental"])
class RentalViewSet(viewsets.ModelViewSet):
    """Viewset for CRUD of Rental instance."""

    queryset = Rental.objects.all()
    serializer_class = CreateRentalSerializer
    http_method_names = ["get"]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = RentalFilterSet
    search_fields = ["location__address", "title"]
    ordering_fields = ["id", "date_added", "monthly_rent"]
    ordering = ["-date_added"]

    def get_serializer_class(self):
        if self.action == "list":
            return ListRentalSerializer
        elif self.action == "retrieve":
            return DetailRentalSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        if self.action == "list":
            return (
                self.queryset.select_related("category", "location")
                .prefetch_related("rental_images")
                .only(
                    "title",
                    "monthly_rent",
                    "description",
                    "category__name",
                    "location__address",
                    "date_modified",
                    "date_added",
                )
            )
        return super().get_queryset()


@extend_schema(tags=["Rental"])
@api_view(["GET"])
def get_rent_range(request):
    """Returns lower and higher end of monthly rent"""
    rent = Rental.objects.aggregate(
        min_rent=Min("monthly_rent"), max_rent=Max("monthly_rent")
    )

    return Response(rent)


@extend_schema(tags=["Rental"])
class AddRentalView(APIView):
    """Add Rental View for HTML UI."""

    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = CreateRentalSerializer
    template_name = "rental_add.html"

    def get(self, request):
        serialzer = self.serializer_class(context={"request": request})
        return Response(data={"form": serialzer}, template_name=self.template_name)


@extend_schema(tags=["Category"])
class AddCategoryView(APIView):
    """Add Category View for HTML UI."""

    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = CreateCategorySerializer
    template_name = "rental_add.html"

    def get(self, request):
        serializer = self.serializer_class(context={"request": request})
        return Response(data={"form": serializer}, template_name=self.template_name)

    def post(self, request):
        data = request.POST
        return Response(data={"data": data}, template_name=self.template_name)


@extend_schema(tags=["Notification"])
class NotificationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user, read=False).order_by(
            "-created_at"
        )

    @action(detail=False, methods=["post"])
    def mark_read(self, request):
        serializer = MarkReadSerializer(data=request.data)
        if serializer.is_valid():
            Notification.objects.filter(
                id__in=serializer.validated_data["ids"], read=False, user=request.user
            ).update(read=True)
            return Response({"message": "Successfully updated"}, status=200)
        else:
            return Response(serializer.errors, status=400)

    @action(detail=False, methods=["post"])
    def mark_all_read(self, request):
        try:
            Notification.objects.filter(read=False, user=request.user).update(read=True)
            return Response({"message": "Successfully updated"})
        except Exception as e:
            return Response({"error": f"Failed update: {e}"}, status=400)


class ChatViewSet(viewsets.ModelViewSet):
    """Viewset for listing and updating chat messages."""

    permission_classes = [IsAuthenticated]
    serializer_class = ChatSerializer
    http_method_names = ["get", "put"]

    def get_queryset(self):
        other_user_id = self.request.GET.get("user_id", None)
        user = self.request.user

        query = Q(sender=user) | Q(receiver=user)
        if other_user_id:
            query &= Q(sender=int(other_user_id)) | Q(receiver=int(other_user_id))

        queryset = (
            Chat.objects.filter(query)
            .order_by("-created_at")
            .annotate(
                user_id=Case(
                    When(sender=user, then=F("receiver_id")),
                    When(receiver=user, then=F("sender_id")),
                    output_field=IntegerField(),
                ),
                sent=Case(
                    When(sender=user, then=True),
                    When(receiver=user, then=False),
                    output_field=BooleanField(),
                ),
            )
        )
        return queryset


@permission_classes([IsAuthenticated])
@api_view(["GET"])
def get_latest_chat_for_user(request):

    user_id = request.user.id
    page_number = int(request.query_params.get("page", 1))
    page_size = int(request.query_params.get("page_size", 10))
    skip = (page_number - 1) * page_size

    query = f"""
        SELECT id, sender_id, receiver_id, message, created_at
        FROM rentals_chat c
        WHERE c.id IN (
            SELECT MAX(id) AS max_id
            FROM rentals_chat
            WHERE receiver_id = {user_id} OR sender_id = {user_id}
            GROUP BY CASE
                WHEN sender_id = {user_id} THEN receiver_id
                WHEN receiver_id = {user_id} THEN sender_id
            END
        )
        ORDER BY created_at DESC
        LIMIT {page_size} OFFSET {skip}
    """

    # Count query to fetch total number of results
    count_query = f"""
        SELECT COUNT(*) AS total_count
        FROM rentals_chat c
        WHERE c.id IN (
            SELECT MAX(id) AS max_id
            FROM rentals_chat
            WHERE receiver_id = {user_id} OR sender_id = {user_id}
            GROUP BY CASE
                WHEN sender_id = {user_id} THEN receiver_id
                WHEN receiver_id = {user_id} THEN sender_id
            END
        )
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

        cursor.execute(count_query)
        total_count = cursor.fetchone()[0]

    chats = []
    for row in rows:
        if row[1] == user_id:
            other_user_id = row[2]
        else:
            other_user_id = row[1]

        chat = {
            "id": row[0],
            "user_id": other_user_id,
            "message": row[3],
            "created_at": row[4].isoformat(),
        }
        chats.append(chat)
    return Response(
        {
            "count": total_count,
            "results": chats,
        }
    )

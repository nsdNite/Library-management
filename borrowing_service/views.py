from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from borrowing_service.models import Borrowing
from borrowing_service.serializers import BorrowingSerializer


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer

    @action(detail=False, methods=["get"])
    def get_borrowing_by_user_and_status(self, request):
        user_id = request.query_params.get("user_id")
        is_active = request.query_params.get("is_active") == "true"

        queryset = self.get_queryset().filter(user_id=user_id)

        if is_active:
            queryset = queryset.filter(actual_return_date__isnull=True)
        else:
            queryset = queryset.exclude(actual_return_date__isnull=True)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

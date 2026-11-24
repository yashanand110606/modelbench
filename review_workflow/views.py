from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Review
from .serializers import ReviewSerializer
from .permissions import IsReviewerOrReadOnly, CanApproveReject


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewerOrReadOnly]
    filterset_fields = ['evaluation', 'reviewer', 'status']
    search_fields = ['comments']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        review = self.get_object()
        if review.status == Review.Status.APPROVED:
            return Response({'status': 'already_approved'}, status=status.HTTP_400_BAD_REQUEST)
        review.status = Review.Status.APPROVED
        review.save()
        return Response({'status': 'approved', 'reviewer': request.user.username})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        review = self.get_object()
        if review.status == Review.Status.REJECTED:
            return Response({'status': 'already_rejected'}, status=status.HTTP_400_BAD_REQUEST)
        review.status = Review.Status.REJECTED
        review.save()
        return Response({'status': 'rejected', 'reviewer': request.user.username})

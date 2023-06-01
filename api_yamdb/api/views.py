from rest_framework import filters, viewsets
from django.shortcuts import get_object_or_404

from reviews.models import Review, Title
from .serializers import CommentSerializer, ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related('title').all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        )

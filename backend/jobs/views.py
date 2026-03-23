from rest_framework import viewsets, permissions, filters
from django_filters import rest_framework as django_filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import JobApplication
from .serializers import JobApplicationSerializer


class JobApplicationFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=JobApplication.Status.choices)
    company_name = django_filters.CharFilter(field_name='company_name', lookup_expr='icontains')
    applied_date_from = django_filters.DateFilter(field_name='applied_date', lookup_expr='gte')
    applied_date_to = django_filters.DateFilter(field_name='applied_date', lookup_expr='lte')

    class Meta:
        model = JobApplication
        fields = ['status', 'company_name', 'applied_date_from', 'applied_date_to']


class JobApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = JobApplicationFilter
    search_fields = ['company_name', 'role']
    ordering_fields = ['created_at', 'applied_date', 'status']
    ordering = ['-created_at']

    def get_queryset(self):
        return JobApplication.objects.filter(
            user=self.request.user
        ).select_related('user')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

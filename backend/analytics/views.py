from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services import calculate_user_analytics, compute_weekly_analytics
from .models import WeeklyAnalytics


class UserAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        
        overall = calculate_user_analytics(user)
        
        weekly = WeeklyAnalytics.objects.filter(
            user=user
        ).values(
            'week_start_date',
            'total_applications',
            'total_responses',
            'total_interviews',
            'response_rate',
            'interview_conversion_rate',
            'average_response_time'
        )
        
        return Response({
            'overall': overall,
            'weekly': list(weekly),
        })


class RecomputeAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        compute_weekly_analytics(user)
        
        return Response({
            'message': 'Analytics recomputed successfully',
            'data': calculate_user_analytics(user)
        })

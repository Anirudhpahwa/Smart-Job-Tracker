from django.db import models
from django.conf import settings


class WeeklyAnalytics(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='weekly_analytics',
    )
    week_start_date = models.DateField(db_index=True)
    total_applications = models.IntegerField(default=0)
    total_responses = models.IntegerField(default=0)
    total_interviews = models.IntegerField(default=0)
    response_rate = models.FloatField(default=0.0)
    interview_conversion_rate = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)

    class Meta:
        ordering = ['-week_start_date']
        unique_together = ['user', 'week_start_date']
        indexes = [
            models.Index(fields=['user', '-week_start_date']),
            models.Index(fields=['week_start_date']),
        ]

    def __str__(self):
        return f"Analytics for {self.user.username} - Week of {self.week_start_date}"

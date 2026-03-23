from celery import shared_task
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task
def recompute_all_user_analytics():
    users = User.objects.all()
    from analytics.services import compute_weekly_analytics
    for user in users:
        compute_weekly_analytics(user)
    return f"Recomputed analytics for {users.count()} users"


@shared_task
def recompute_user_analytics(user_id):
    from analytics.services import compute_weekly_analytics
    from django.contrib.auth import get_user_model
    User = get_user_model()
    try:
        user = User.objects.get(id=user_id)
        compute_weekly_analytics(user)
        return f"Recomputed analytics for user {user.username}"
    except User.DoesNotExist:
        return f"User {user_id} not found"

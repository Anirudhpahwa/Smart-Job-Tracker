import logging
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def recompute_all_user_analytics(self):
    from django.contrib.auth import get_user_model
    from analytics.services import compute_weekly_analytics
    
    User = get_user_model()
    
    logger.info("Starting analytics recomputation for all users")
    
    try:
        users = User.objects.all()
        count = 0
        for user in users:
            try:
                compute_weekly_analytics(user)
                count += 1
            except Exception as e:
                logger.error(f"Failed to compute analytics for user {user.id}: {str(e)}")
        
        logger.info(f"Completed analytics recomputation for {count} users")
        return f"Recomputed analytics for {count} users"
    except Exception as e:
        logger.error(f"Failed to recompute analytics: {str(e)}")
        raise self.retry(exc=e)


@shared_task(bind=True, max_retries=3, default_retry_delay=30)
def recompute_user_analytics(self, user_id):
    from django.contrib.auth import get_user_model
    from analytics.services import compute_weekly_analytics
    
    User = get_user_model()
    
    logger.info(f"Starting analytics recomputation for user {user_id}")
    
    try:
        user = User.objects.get(id=user_id)
        compute_weekly_analytics(user)
        logger.info(f"Completed analytics recomputation for user {user.username}")
        return f"Recomputed analytics for user {user.username}"
    except User.DoesNotExist:
        logger.warning(f"User {user_id} not found")
        return f"User {user_id} not found"
    except Exception as e:
        logger.error(f"Failed to recompute analytics for user {user_id}: {str(e)}")
        raise self.retry(exc=e)

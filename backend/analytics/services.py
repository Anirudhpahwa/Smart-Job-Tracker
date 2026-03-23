from datetime import timedelta
from django.db.models import Avg, Count, Q, F
from django.db.models.functions import ExtractDay
from jobs.models import JobApplication
from .models import WeeklyAnalytics
from datetime import date


def get_week_start(d):
    return d - timedelta(days=d.weekday())


def calculate_user_analytics(user):
    jobs = JobApplication.objects.filter(user=user)
    
    total_applications = jobs.count()
    total_responses = jobs.exclude(response_date__isnull=True).count()
    total_interviews = jobs.filter(status=JobApplication.Status.INTERVIEW).count()
    
    response_rate = (total_responses / total_applications * 100) if total_applications > 0 else 0.0
    interview_rate = (total_interviews / total_applications * 100) if total_applications > 0 else 0.0
    
    response_jobs = jobs.exclude(response_date__isnull=True)
    avg_response_time = 0.0
    if response_jobs.exists():
        total_days = sum(
            (job.response_date - job.applied_date).days 
            for job in response_jobs 
            if job.response_date and job.applied_date
        )
        count = response_jobs.count()
        avg_response_time = total_days / count if count > 0 else 0.0
    
    return {
        'total_applications': total_applications,
        'total_responses': total_responses,
        'total_interviews': total_interviews,
        'response_rate': round(response_rate, 2),
        'interview_conversion_rate': round(interview_rate, 2),
        'average_response_time': round(avg_response_time, 2),
    }


def compute_weekly_analytics(user):
    jobs = JobApplication.objects.filter(user=user)
    
    if not jobs.exists():
        return []
    
    job_list = list(jobs.values('applied_date', 'response_date', 'status'))
    
    weeks = {}
    for job in job_list:
        if job['applied_date']:
            week_start = get_week_start(job['applied_date'])
            if week_start not in weeks:
                weeks[week_start] = {
                    'applications': 0,
                    'responses': 0,
                    'interviews': 0,
                    'response_times': []
                }
            weeks[week_start]['applications'] += 1
            
            if job['response_date']:
                weeks[week_start]['responses'] += 1
                if job['applied_date'] and job['response_date']:
                    days = (job['response_date'] - job['applied_date']).days
                    weeks[week_start]['response_times'].append(days)
            
            if job['status'] == JobApplication.Status.INTERVIEW:
                weeks[week_start]['interviews'] += 1
    
    analytics_data = []
    for week_start, data in weeks.items():
        total = data['applications']
        response_rate = (data['responses'] / total * 100) if total > 0 else 0.0
        interview_rate = (data['interviews'] / total * 100) if total > 0 else 0.0
        avg_time = sum(data['response_times']) / len(data['response_times']) if data['response_times'] else 0.0
        
        analytics_data.append({
            'week_start_date': week_start,
            'total_applications': data['applications'],
            'total_responses': data['responses'],
            'total_interviews': data['interviews'],
            'response_rate': round(response_rate, 2),
            'interview_conversion_rate': round(interview_rate, 2),
            'average_response_time': round(avg_time, 2),
        })
        
        WeeklyAnalytics.objects.update_or_create(
            user=user,
            week_start_date=week_start,
            defaults={
                'total_applications': data['applications'],
                'total_responses': data['responses'],
                'total_interviews': data['interviews'],
                'response_rate': round(response_rate, 2),
                'interview_conversion_rate': round(interview_rate, 2),
                'average_response_time': round(avg_time, 2),
            }
        )
    
    return analytics_data

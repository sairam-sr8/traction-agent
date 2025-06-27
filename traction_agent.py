"""
TractionAgent – Startup Traction & Analytics Engine
Aggregates and interprets traction-related metrics for a given startup.
"""
from collections import Counter, defaultdict
from datetime import datetime
from typing import List, Dict, Any


def analyze_traction(startup_id: str, events: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyze traction metrics for a given startup based on event logs.

    Args:
        startup_id (str): Unique identifier for the startup.
        events (list): List of event dicts. Each dict may contain:
            - event_type (str): e.g., 'page_view', 'click', 'pitch_download'
            - timestamp (str, optional): ISO format datetime string
            - referrer (str, optional): Source of the event
            - device_type (str, optional): Device used
            - region (str, optional): User region
            - ... (other metadata)

    Returns:
        dict: Aggregated metrics and insights, e.g.:
            {
                'total_views': int,
                'clicks': int,
                'pitch_downloads': int,
                'conversion_rate': str,
                'top_referrers': list,
                'active_days': int,
                'heatmap_data': dict,
                'daily_trend': dict,
                'weekly_trend': dict,
                'alerts': list,
                'data_status': str
            }
    """
    if not events or len(events) == 0:
        return {
            'alerts': ['insufficient activity'],
            'data_status': 'insufficient activity'
        }

    # Initialize counters
    total_views = 0
    clicks = 0
    pitch_downloads = 0
    referrers = []
    days_set = set()
    heatmap_counter = Counter({day: 0 for day in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']})
    daily_trend = defaultdict(int)
    weekly_trend = defaultdict(int)
    incomplete_logs = False

    for event in events:
        etype = event.get('event_type')
        ts = event.get('timestamp')
        ref = event.get('referrer')

        # Aggregate event types
        if etype == 'page_view':
            total_views += 1
        elif etype == 'click':
            clicks += 1
        elif etype == 'pitch_download':
            pitch_downloads += 1
        # Add more event types as needed

        # Referrer aggregation
        if ref:
            referrers.append(ref)

        # Time-based aggregation
        if ts:
            try:
                dt = datetime.fromisoformat(ts)
                day_name = dt.strftime('%a')  # e.g., 'Mon'
                heatmap_counter[day_name] += 1
                day_str = dt.strftime('%Y-%m-%d')
                week_str = dt.strftime('%Y-W%U')
                daily_trend[day_str] += 1
                weekly_trend[week_str] += 1
                days_set.add(day_str)
            except Exception:
                incomplete_logs = True
        else:
            incomplete_logs = True

    # Conversion rate (clicks/views)
    conversion_rate = f"{(clicks / total_views * 100):.1f}%" if total_views else "0%"

    # Top referrers
    top_referrers = [r for r, _ in Counter(referrers).most_common(3)]

    # Active days
    active_days = len(days_set)

    # Format heatmap data
    heatmap_data = {day: heatmap_counter[day] for day in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']}

    # Format trends
    daily_trend = dict(sorted(daily_trend.items()))
    weekly_trend = dict(sorted(weekly_trend.items()))

    # Alerts and data status
    alerts = []
    data_status = 'complete'
    if incomplete_logs:
        alerts.append('partial data: some events missing timestamps or fields')
        data_status = 'partial'

    return {
        'total_views': total_views,
        'clicks': clicks,
        'pitch_downloads': pitch_downloads,
        'conversion_rate': conversion_rate,
        'top_referrers': top_referrers,
        'active_days': active_days,
        'heatmap_data': heatmap_data,
        'daily_trend': daily_trend,
        'weekly_trend': weekly_trend,
        'alerts': alerts,
        'data_status': data_status
    }

if __name__ == "__main__":
    # Example usage and test case
    sample_events = [
        {"event_type": "page_view", "timestamp": "2024-06-01T10:00:00", "referrer": "linkedin.com", "device_type": "mobile"},
        {"event_type": "click", "timestamp": "2024-06-01T10:01:00", "referrer": "linkedin.com", "device_type": "mobile"},
        {"event_type": "pitch_download", "timestamp": "2024-06-01T10:02:00", "referrer": "angel.co", "device_type": "desktop"},
        {"event_type": "page_view", "timestamp": "2024-06-02T11:00:00", "referrer": "angel.co", "device_type": "desktop"},
        {"event_type": "click", "timestamp": "2024-06-02T11:05:00", "referrer": "angel.co", "device_type": "desktop"},
        {"event_type": "page_view", "timestamp": "2024-06-03T12:00:00", "referrer": "twitter.com", "device_type": "mobile"},
        {"event_type": "page_view", "timestamp": "2024-06-03T13:00:00", "referrer": "linkedin.com", "device_type": "desktop"},
        # Event with missing timestamp (to test incomplete log handling)
        {"event_type": "click", "referrer": "linkedin.com", "device_type": "mobile"},
    ]
    result = analyze_traction("startup_123", sample_events)
    import pprint
    pprint.pprint(result)

# Usage example and test cases can be added in a separate test file or docstring. 
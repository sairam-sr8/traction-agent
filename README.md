# TractionAgent – Startup Traction & Analytics Engine

## Overview
The TractionAgent is a Python analytics engine that aggregates and interprets traction-related metrics for startups. It helps founders and teams understand their startup's momentum, growth, and user engagement patterns by analyzing event logs and outputting actionable insights.

## Features
- Aggregates core metrics: views, clicks, downloads, etc.
- Calculates conversion rates and top referrers
- Computes weekday heatmap data for visualization
- Computes daily and weekly activity trends
- Handles edge cases (no data, incomplete logs)
- Returns results in a structured dictionary for dashboard integration

## Function Usage

### Function Signature
```python
def analyze_traction(startup_id: str, events: list) -> dict:
```

### Input
- `startup_id` (str): Unique identifier for the startup
- `events` (list of dict): Each event dict may contain:
  - `event_type` (str): e.g., 'page_view', 'click', 'pitch_download'
  - `timestamp` (str, optional): ISO format datetime string
  - `referrer` (str, optional): Source of the event
  - `device_type` (str, optional): Device used
  - `region` (str, optional): User region
  - ... (other metadata)

### Output
A dictionary with aggregated metrics and insights, e.g.:
```python
{
  "total_views": 1423,
  "clicks": 312,
  "pitch_downloads": 27,
  "conversion_rate": "21.9%",
  "top_referrers": ["linkedin.com", "angel.co"],
  "active_days": 14,
  "heatmap_data": {
    "Mon": 12, "Tue": 48, "Wed": 71, "Thu": 32, "Fri": 90, "Sat": 0, "Sun": 0
  },
  "daily_trend": {"2024-06-01": 120, ...},
  "weekly_trend": {"2024-W22": 500, ...},
  "alerts": [],
  "data_status": "complete"
}
```

## Example
Run the following to see the function in action:

```bash
python traction_agent.py
```

Sample output:
```
{'active_days': 3,
 'alerts': ['partial data: some events missing timestamps or fields'],
 'clicks': 3,
 'conversion_rate': '60.0%',
 'data_status': 'partial',
 'daily_trend': {'2024-06-01': 3, '2024-06-02': 2, '2024-06-03': 2},
 'heatmap_data': {'Mon': 0, 'Tue': 0, 'Wed': 0, 'Thu': 0, 'Fri': 0, 'Sat': 0, 'Sun': 0},
 'pitch_downloads': 1,
 'top_referrers': ['linkedin.com', 'angel.co', 'twitter.com'],
 'total_views': 4,
 'weekly_trend': {'2024-W22': 7}}
```

## Extensibility
- Add more event types as needed
- Filtering, drop-off prediction, and inactivity alerts can be added in future versions

## License
MIT 
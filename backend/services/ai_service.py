from models.complaint import ComplaintCategory, ComplaintPriority, ComplaintAIResult
import re

# Rule-based keyword matching for complaint classification
# This is a simple implementation that can be enhanced with ML models later

CATEGORY_KEYWORDS = {
    ComplaintCategory.ROAD: [
        "road", "street", "pavement", "highway", "traffic", "lane", "asphalt",
        "pot hole", "pothole", "crack", "repair", "construction", "sidewalk"
    ],
    ComplaintCategory.WATER: [
        "water", "leak", "pipe", "plumbing", "drain", "sewage", "flood",
        "tap", "faucet", "supply", "contamination", "clean water"
    ],
    ComplaintCategory.ELECTRICITY: [
        "electric", "power", "light", "bulb", "wire", "cable", "outage",
        "voltage", "transformer", "pole", "meter", "current", "short circuit"
    ],
    ComplaintCategory.SANITATION: [
        "garbage", "waste", "trash", "bin", "collection", "dump", "sewage",
        "toilet", "bathroom", "cleanliness", "hygiene", "pest", "rat"
    ]
}

PRIORITY_KEYWORDS = {
    ComplaintPriority.HIGH: [
        "emergency", "urgent", "danger", "hazard", "accident", "injury",
        "flood", "fire", "explosion", "breakdown", "no water", "no electricity",
        "dark", "unsafe", "life threatening"
    ],
    ComplaintPriority.MEDIUM: [
        "problem", "issue", "broken", "damaged", "leak", "noise", "smell",
        "dirty", "maintenance", "repair needed", "not working"
    ],
    ComplaintPriority.LOW: [
        "improvement", "suggestion", "better", "enhancement", "minor",
        "cosmetic", "appearance", "aesthetic"
    ]
}

def classify_complaint(text: str) -> ComplaintAIResult:
    """
    Classify complaint text into category and priority using rule-based keyword matching.

    Args:
        text: The complaint description text

    Returns:
        ComplaintAIResult: Contains category and priority classifications
    """
    text_lower = text.lower()

    # Determine category
    category_scores = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for keyword in keywords if re.search(r'\b' + re.escape(keyword) + r'\b', text_lower))
        category_scores[category] = score

    # Get category with highest score, default to OTHER
    max_score = max(category_scores.values()) if category_scores else 0
    if max_score > 0:
        category = max(category_scores, key=category_scores.get)
    else:
        category = ComplaintCategory.OTHER

    # Determine priority
    priority_scores = {}
    for priority, keywords in PRIORITY_KEYWORDS.items():
        score = sum(1 for keyword in keywords if re.search(r'\b' + re.escape(keyword) + r'\b', text_lower))
        priority_scores[priority] = score

    # Get priority with highest score, default to MEDIUM
    max_priority_score = max(priority_scores.values()) if priority_scores else 0
    if max_priority_score > 0:
        priority = max(priority_scores, key=priority_scores.get)
    else:
        priority = ComplaintPriority.MEDIUM

    return ComplaintAIResult(category=category, priority=priority)
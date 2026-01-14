"""
Pytest checks for the EmailCleaner Pro webhook.
Requires the API server to be running on localhost:8000.
"""

from __future__ import annotations

from datetime import datetime

import pytest
import requests

API_URL = "http://127.0.0.1:8000/api/email/webhook"
HEALTH_URL = "http://127.0.0.1:8000/health"

TEST_EMAILS = [
    {
        "name": "Refund Request",
        "data": {
            "from_address": "ruhulcom53@gmail.com",
            "subject": "Need refund for order #12345",
            "body": "I want to return my product and get a refund. The item is defective.",
            "received_at": datetime.now().isoformat(),
        },
        "expected_action": "AUTO_REPLY",
    },
    {
        "name": "Shipping Question",
        "data": {
            "from_address": "ruhulcom553@gmail.com",
            "subject": "How long does shipping take?",
            "body": "I placed an order yesterday. When will it arrive in Bangladesh?",
            "received_at": datetime.now().isoformat(),
        },
        "expected_action": "AUTO_REPLY",
    },
    {
        "name": "Complaint",
        "data": {
            "from_address": "ruhulcom553@gmail.com",
            "subject": "Very disappointed with service",
            "body": "This is unacceptable. I want to speak with a manager immediately.",
            "received_at": datetime.now().isoformat(),
        },
        "expected_action": "ESCALATE",
    },
    {
        "name": "General Inquiry",
        "data": {
            "from_address": "ruhulcom553@gmail.com",
            "subject": "Product information",
            "body": "Can you tell me more about your warranty policy?",
            "received_at": datetime.now().isoformat(),
        },
        "expected_action": "AUTO_REPLY",
    },
]


def _server_available() -> bool:
    try:
        response = requests.get(HEALTH_URL, timeout=60)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


@pytest.mark.skipif(not _server_available(), reason="API server is not running")
@pytest.mark.parametrize("email_case", TEST_EMAILS)
def test_email(email_case: dict) -> None:
    response = requests.post(API_URL, json=email_case["data"], timeout=120)
    assert response.status_code == 200
    result = response.json()
    assert result.get("status") == "processed"
    assert result.get("action") == email_case["expected_action"]

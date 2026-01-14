import os

import requests
import streamlit as st

API_BASE_URL = os.getenv("DASHBOARD_API_BASE_URL", "http://localhost:8000").rstrip("/")
STATS_URL = f"{API_BASE_URL}/api/admin/stats"


def _coerce_int(value: object) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


@st.cache_data(ttl=5)
def load_stats() -> tuple[dict, str | None]:
    try:
        response = requests.get(STATS_URL, timeout=3)
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException:
        return (
            {
                "processed": 0,
                "auto_replies": 0,
                "tagged": 0,
                "escalations": 0,
            },
            f"Cannot reach API at {STATS_URL}. Start the FastAPI server.",
        )

    return (
        {
            "processed": _coerce_int(payload.get("processed")),
            "auto_replies": _coerce_int(payload.get("auto_replies")),
            "tagged": _coerce_int(payload.get("tagged")),
            "escalations": _coerce_int(payload.get("escalations")),
        },
        None,
    )


st.set_page_config(page_title="EmailCleaner Pro", layout="wide")
st.title("EmailCleaner Pro Dashboard")

stats, error = load_stats()
if error:
    st.warning(error)

col_processed, col_auto, col_tagged, col_escalations = st.columns(4)
col_processed.metric("Processed", stats["processed"])
col_auto.metric("Auto Replies", stats["auto_replies"])
col_tagged.metric("Tagged", stats["tagged"])
col_escalations.metric("Escalations", stats["escalations"])

if st.button("Refresh"):
    st.cache_data.clear()
    st.rerun()

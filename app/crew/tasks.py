from crewai import Task

from app.crew.agents import (
    build_intent_agent,
    build_classifier_agent,
    build_autoreply_agent,
    build_tagging_agent,
    build_escalation_agent,
)


def build_intent_task(subject: str, body: str) -> Task:
    return Task(
        description=f"Identify intent for email: {subject}\n{body}",
        expected_output="intent label",
        agent=build_intent_agent(),
    )


def build_classifier_task(intent: str) -> Task:
    return Task(
        description=f"Decide action for intent: {intent}",
        expected_output="action: AUTO_REPLY, TAG_ARCHIVE, or ESCALATE",
        agent=build_classifier_agent(),
    )


def build_autoreply_task(subject: str, body: str, intent: str) -> Task:
    return Task(
        description=f"Write reply for intent {intent}: {subject}\n{body}",
        expected_output="reply draft",
        agent=build_autoreply_agent(),
    )


def build_tagging_task(intent: str) -> Task:
    return Task(
        description=f"Suggest tags for intent: {intent}",
        expected_output="list of tags",
        agent=build_tagging_agent(),
    )


def build_escalation_task(subject: str, body: str) -> Task:
    return Task(
        description=f"Summarize for escalation: {subject}\n{body}",
        expected_output="summary",
        agent=build_escalation_agent(),
    )

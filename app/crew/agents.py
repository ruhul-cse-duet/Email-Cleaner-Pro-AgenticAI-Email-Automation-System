from crewai import Agent


def build_email_fetch_agent() -> Agent:
    return Agent(
        role="Email Fetch Agent",
        goal="Fetch new emails from the inbox",
        backstory="You connect to Gmail/IMAP and pull unread emails.",
    )


def build_intent_agent() -> Agent:
    return Agent(
        role="Intent Detection Agent",
        goal="Identify the intent of the email",
        backstory="You read emails and label the intent.",
    )


def build_classifier_agent() -> Agent:
    return Agent(
        role="Classifier Agent",
        goal="Decide whether to auto reply, tag/archive, or escalate",
        backstory="You decide the best next step for the email.",
    )


def build_autoreply_agent() -> Agent:
    return Agent(
        role="Auto Reply Agent",
        goal="Generate helpful replies using templates and RAG",
        backstory="You draft on-brand customer responses.",
    )


def build_tagging_agent() -> Agent:
    return Agent(
        role="Tagging Agent",
        goal="Assign labels and folders",
        backstory="You keep the inbox organized.",
    )


def build_escalation_agent() -> Agent:
    return Agent(
        role="Escalation Agent",
        goal="Create concise summaries for humans",
        backstory="You escalate complex cases with context.",
    )

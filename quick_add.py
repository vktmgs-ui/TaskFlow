import re


SYSTEM_PROMPT = """
You are a task parser.
Convert a user's task description into:
- title
- priority
- due_date_hint

Priority must be low, medium, or high.
Due date must be a raw phrase such as today, tomorrow, or next friday.
"""


def build_prompt(description: str):
    return [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": description
        }
    ]


def parse_quick_add(description: str):
    lower_text = description.lower()

    # -------------------------
    # 1. PRIORITY
    # -------------------------

    if (
        "urgent" in lower_text
        or "asap" in lower_text
        or "high priority" in lower_text
        or "high-priority" in lower_text
    ):
        priority = "high"

    elif (
        "whenever" in lower_text
        or "low priority" in lower_text
        or "low-priority" in lower_text
    ):
        priority = "low"

    else:
        priority = "medium"

    # -------------------------
    # 2. DUE DATE
    # -------------------------

    date_phrases = [
        "today",
        "tomorrow",
        "next week",
        "next monday",
        "next tuesday",
        "next wednesday",
        "next thursday",
        "next friday",
        "next saturday",
        "next sunday",
    ]

    due_date_hint = None

    for phrase in date_phrases:
        if phrase in lower_text:
            due_date_hint = phrase
            break

    # Check weekday names
    if due_date_hint is None:
        weekdays = [
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
        ]

        for day in weekdays:
            if re.search(rf"\b{day}\b", lower_text):
                due_date_hint = day
                break

    # -------------------------
    # 3. TITLE
    # -------------------------

    title = description

    # Remove priority phrases from title
    priority_patterns = [
        r"\burgent\b",
        r"\basap\b",
        r"\bwhenever\b",
        r"\bhigh[\s-]+priority\b",
        r"\blow[\s-]+priority\b",
    ]

    for pattern in priority_patterns:
        title = re.sub(
            pattern,
            "",
            title,
            flags=re.IGNORECASE
        )

    # Clean extra spaces before/after punctuation
    title = re.sub(r"\s*,\s*", " ", title)
    title = re.sub(r"\s+", " ", title)

    title = title.strip(" ,.-")

    if not title:
        title = "Untitled task"

    return {
        "title": title,
        "priority": priority,
        "due_date_hint": due_date_hint
    }
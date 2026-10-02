"""
StudySync -- Session Log (Ticket 2, Tinker 2B).

Tinker 2B compares a resetting local counter with a persistent session-state
counter, validates session inputs, and contrasts PlainSession with SessionDC.
It also demonstrates daily/weekly recurrence and matching time slots.
"""

from dataclasses import dataclass
from datetime import date, timedelta

FREQUENCY_DAYS = {"daily": 1, "weekly": 7}


class PlainSession:
    def __init__(self, subject, minutes, priority="medium"):
        self.subject = subject
        self.minutes = minutes
        self.priority = priority

    def __repr__(self):
        return f"PlainSession(subject={self.subject!r}, minutes={self.minutes}, priority={self.priority!r})"


@dataclass
class SessionDC:
    subject: str
    minutes: int
    priority: str = "medium"


def next_occurrence(last_date: date, frequency: str) -> date:
    """Return the next date for a supported daily or weekly frequency."""
    try:
        days = FREQUENCY_DAYS[frequency]
    except KeyError:
        raise ValueError(f"Unsupported frequency: {frequency!r}") from None

    return last_date + timedelta(days=days)


def find_conflicts(sessions: list) -> list:
    """
    Return each pair of sessions that shares the same ``slot`` value.

    Each session is a dictionary with a ``slot`` key. An empty list or a
    list with no duplicate slots returns an empty list.
    """
    conflicts = []
    for index, session_a in enumerate(sessions):
        for session_b in sessions[index + 1 :]:
            if session_a["slot"] == session_b["slot"]:
                conflicts.append((session_a, session_b))

    return conflicts


def render_session_log_tab():
    import streamlit as st

    if "fixed_count" not in st.session_state:
        st.session_state.fixed_count = 0

    st.subheader("Parts 1-2: Log a Session")

    # This counter resets because Streamlit reruns the script after each click.
    broken_count = 0
    if st.button("Click me (broken)"):
        broken_count += 1
    st.metric("Broken count", broken_count)

    if st.button("Click me (fixed)"):
        st.session_state.fixed_count += 1
    st.metric("Fixed count", st.session_state.fixed_count)

    st.divider()
    st.subheader("Part 2: Session List (with validation)")

    if "mini_sessions" not in st.session_state:
        st.session_state.mini_sessions = []

    subject = st.text_input("Subject")
    duration = st.number_input("Duration (minutes)", value=30, step=1)

    if st.button("Add session"):
        valid = True
        if not subject.strip():
            st.error("Subject cannot be empty.")
            valid = False
        if duration <= 0:
            st.error("Duration must be greater than 0.")
            valid = False
        if valid:
            st.session_state.mini_sessions.append(
                {"subject": subject.strip(), "duration": duration}
            )

    st.write(st.session_state.mini_sessions)

    st.divider()
    st.subheader("Part 4: Conflict Check")
    if st.button("Check for time conflicts"):
        sample = [
            {"subject": "Calc II", "slot": "08:00"},
            {"subject": "Chem Lab", "slot": "08:00"},
            {"subject": "History", "slot": "09:00"},
        ]
        conflicts = find_conflicts(sample)
        st.write(conflicts if conflicts else "No conflicts found.")


if __name__ == "__main__":
    plain = PlainSession("Study group: Calc II", 45, priority="high")
    print(plain)

    session_dc = SessionDC("Study group: Calc II", 45, priority="high")
    print(session_dc)

    print(next_occurrence(date(2026, 1, 1), "daily"))
    print(next_occurrence(date(2026, 1, 1), "weekly"))

    print(
        find_conflicts(
            [
                {"subject": "Calc II", "slot": "08:00"},
                {"subject": "Chem Lab", "slot": "08:00"},
                {"subject": "History", "slot": "09:00"},
            ]
        )
    )
    print(find_conflicts([]))
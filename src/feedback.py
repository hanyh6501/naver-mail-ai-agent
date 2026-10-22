
import json
from pathlib import Path

FEEDBACK_FILE = Path("data/feedback.json")
VALID_CATEGORIES = {
    "ADVERTISEMENT", "IMPORTANT", "REVIEW"
}


def load_feedback():
    if not FEEDBACK_FILE.exists():
        return []

    with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError(
            "기존 피드백 형식입니다. "
            "data/feedback.json을 백업 후 초기화하세요."
        )

    return data


def save_feedback(sender, subject, category):
    if category not in VALID_CATEGORIES:
        raise ValueError("지원하지 않는 분류입니다.")

    feedback = load_feedback()

    record = {
        "sender": sender,
        "subject": subject,
        "corrected_category": category
    }

    # 동일 발신자 + 제목의 기존 기록 업데이트
    for item in feedback:
        if (
            item["sender"] == sender
            and item["subject"] == subject
        ):
            item.update(record)
            break
    else:
        feedback.append(record)

    FEEDBACK_FILE.parent.mkdir(
        parents=True, exist_ok=True
    )

    with open(
        FEEDBACK_FILE, "w", encoding="utf-8"
    ) as f:
        json.dump(
            feedback, f,
            ensure_ascii=False, indent=2
        )


def find_feedback(sender, subject, limit=3):
    """관련 피드백 사례 검색"""
    records = load_feedback()

    # 현재는 같은 발신자의 사례를 우선 검색
    matches = [
        item for item in records
        if item["sender"].lower() == sender.lower()
    ]

    return matches[-limit:]

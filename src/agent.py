
import csv

from src.mail_client import fetch_emails
from src.classifier import classify_email
from src.feedback import find_feedback


def main():
    print("===== Naver Mail AI Agent =====")

    # 1. 네이버 메일 수집
    emails = fetch_emails(limit=10)

    if not emails:
        print("분석할 메일이 없습니다.")
        return

    results = []

    # 2. Ollama를 이용한 메일 분류
    for index, mail in enumerate(emails, 1):
        print(f"\n[{index}/{len(emails)}] AI 분석 중...")

        try:
            previous_feedback = find_feedback(
                sender=mail["sender"],
                subject=mail["subject"]
            )

            result = classify_email(
                sender=mail["sender"],
                subject=mail["subject"],
                body=mail["body"],
                feedback=previous_feedback
            )

        except Exception as exc:
            print(f"분류 오류: {type(exc).__name__}")
            result = {
                "category": "REVIEW",
                "reason": "AI 분류 실패 - 수동 확인 필요"
            }

        print("제목:", mail["subject"])
        print("분류:", result["category"])
        print("이유:", result.get("reason", ""))

        results.append({
            "uid": mail["uid"],
            "sender": mail["sender"],
            "subject": mail["subject"],
            "category": result["category"],
            "reason": result.get("reason", ""),
            "corrected_category": ""
        })


    # 3. CSV 결과 저장
    with open(
        "mail_results.csv",
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "uid",
                "sender",
                "subject",
                "category",
                "reason",
                "corrected_category"
            ]
        )

        writer.writeheader()
        writer.writerows(results)

    print("\n===== 분석 완료 =====")
    print("결과 파일: mail_results.csv")
    print("메일 삭제 및 이동은 수행하지 않았습니다.")


if __name__ == "__main__":
    main()

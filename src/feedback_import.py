import csv
from pathlib import Path

from src.feedback import save_feedback, VALID_CATEGORIES


CSV_FILE = Path("mail_results.csv")


def import_feedback():
    if not CSV_FILE.exists():
        print("mail_results.csv 파일이 없습니다.")
        return

    saved_count = 0

    with open(
        CSV_FILE,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        if not reader.fieldnames or (
            "corrected_category" not in reader.fieldnames
        ):
            print("corrected_category 열이 없습니다.")
            return

        for row in reader:
            corrected = (
                row.get("corrected_category") or ""
            ).strip().upper()

            if not corrected:
                continue

            if corrected not in VALID_CATEGORIES:
                print(
                    "잘못된 분류 값:",
                    corrected
                )
                continue

            sender = row.get("sender", "").strip()

            if not sender:
                continue

            subject = row.get("subject", "").strip()

            if not subject:
                continue

            save_feedback(sender, subject, corrected)
            saved_count += 1

    print(f"피드백 {saved_count}개 저장 완료!")


if __name__ == "__main__":
    import_feedback()

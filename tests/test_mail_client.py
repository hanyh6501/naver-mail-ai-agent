from src.mail_client import fetch_emails


def main():
    print("===== 네이버 메일 연결 테스트 =====")

    emails = fetch_emails(limit=3)

    for index, mail in enumerate(emails, 1):
        print(f"\n메일 {index}")
        print("UID:", mail["uid"])
        print("발신자:", mail["sender"])
        print("제목:", mail["subject"])
        print("-" * 40)

    print("\n테스트 완료!")


if __name__ == "__main__":
    main()
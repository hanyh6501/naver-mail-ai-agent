
import os
import imaplib
import email

from email.header import decode_header, make_header
from dotenv import load_dotenv

load_dotenv()


def decode_text(value):
    """메일 제목과 발신자 인코딩 처리"""
    if not value:
        return ""

    try:
        return str(make_header(decode_header(value)))
    except Exception:
        return str(value)


def extract_body(message):
    """메일의 텍스트 본문 추출"""
    parts = (
        message.walk()
        if message.is_multipart()
        else [message]
    )

    for part in parts:
        if part.get_content_type() != "text/plain":
            continue

        if part.get_content_disposition() == "attachment":
            continue

        payload = part.get_payload(decode=True)

        if not payload:
            continue

        charset = part.get_content_charset() or "utf-8"

        try:
            return payload.decode(
                charset, errors="replace"
            )[:2000]
        except LookupError:
            return payload.decode(
                "utf-8", errors="replace"
            )[:2000]

    return ""


def fetch_emails(limit=3):
    """네이버 메일을 읽기 전용으로 조회"""

    naver_id = os.environ["NAVER_ID"]
    password = os.environ["NAVER_APP_PASSWORD"]

    emails = []

    print("네이버 IMAP 서버 연결 중...")

    with imaplib.IMAP4_SSL(
        "imap.naver.com", 993
    ) as mail:

        mail.login(naver_id, password)
        print("로그인 성공!")

        status, _ = mail.select(
            "INBOX", readonly=True
        )

        if status != "OK":
            raise RuntimeError("받은편지함 접근 실패")

        status, data = mail.uid(
            "search", None, "ALL"
        )

        if status != "OK":
            raise RuntimeError("메일 검색 실패")

        uids = data[0].split()[-limit:]

        print(f"조회할 메일: {len(uids)}개")

        for uid in reversed(uids):

            status, fetched = mail.uid(
                "fetch", uid, "(BODY.PEEK[])"
            )

            if status != "OK":
                continue

            raw = next(
                (
                    item[1]
                    for item in fetched
                    if isinstance(item, tuple)
                    and isinstance(item[1], bytes)
                ),
                None
            )

            if raw is None:
                continue

            message = email.message_from_bytes(raw)

            emails.append({
                "uid": uid.decode(),
                "sender": decode_text(
                    message.get("From")
                ),
                "subject": decode_text(
                    message.get("Subject")
                ),
                "body": extract_body(message)
            })

    return emails

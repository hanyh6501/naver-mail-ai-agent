from src.classifier import classify_email

result = classify_email(
    sender="promotion@example.com",
    subject="오늘만 70% 할인!",
    body="신상품을 특별 할인가로 구매하세요."
)

print("AI 분류 결과:")
print(result)
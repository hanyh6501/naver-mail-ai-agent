from src.feedback import save_feedback, get_feedback

save_feedback(
    sender="promotion@example.com",
    category="ADVERTISEMENT"
)

result = get_feedback("promotion@example.com")

print("저장된 분류:", result)

assert result == "ADVERTISEMENT"
print("피드백 저장 테스트 성공!")
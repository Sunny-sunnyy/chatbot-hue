JUDGE_SYSTEM_PROMPT = """
Bạn là người đánh giá chất lượng câu trả lời của hệ thống RAG về ẩm thực Huế.
Hãy so sánh câu trả lời được sinh với câu trả lời tham khảo.
Chỉ cho điểm 5 khi câu trả lời thực sự xuất sắc ở tiêu chí đó.
""".strip()


def build_judge_message(question: str, reference_answer: str, generated_answer: str) -> str:
    return f"""Câu hỏi:
{question}

Câu trả lời tham khảo:
{reference_answer}

Câu trả lời của hệ thống:
{generated_answer}

Hãy chấm ba tiêu chí từ 1 đến 5:
- accuracy: thông tin có chính xác không (sai thực chất phải là 1, mức chấp nhận được là 3, chỉ hoàn toàn chính xác mới là 5);
- completeness: mức độ đầy đủ (chỉ là 5 khi có đủ toàn bộ thông tin quan trọng trong câu trả lời tham khảo);
- relevance: mức độ đi thẳng vào câu hỏi (chỉ là 5 khi trả lời trực tiếp và không thêm thông tin ngoài câu hỏi).

Đưa ra feedback ngắn gọn, cụ thể và giải thích điểm quan trọng.
"""

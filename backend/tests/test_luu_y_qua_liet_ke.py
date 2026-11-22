"""Dòng "lưu ý của nguồn" cho bài đi qua công cụ liệt kê (soát khác hãng 22/11/2026, phiên đo tái hiện trên 267 bài) — 0 USD, không model, không Qdrant.
Vì sao: `set_notice` đưa cho `dong_tam_ngung` từng DÒNG RỜI của bài mục lục; câu an toàn nằm trên hai dòng vật lý của file thì không dòng nào tự đủ ý ⇒
mất dòng lưu ý (bài "Đi lại ở Huế": câu thuyền dừng chạy mùa mưa lũ), trong khi cùng bài vào ngữ cảnh qua tìm kho thì có."""
from llm import liet_ke as lk
from llm.assistant import _doan_bai
from llm.luu_y_nguon import dong_tam_ngung

HAI_DONG = lk.bai_tu_markdown("travel/thu.md", "# Đi lại thử\n\nĐi thuyền trên sông mất khoảng 30 phút. Vào mùa mưa lũ, thuyền có thể phải dừng chạy\n"
                              "khi nước sông dâng cao hoặc có lệnh cấm xuất bến.\n")
MOT_DONG = lk.bai_tu_markdown("travel/thu2.md", "# Suối thử\n\n- Vào mùa mưa lũ, khu suối có thể tạm ngừng đón khách khi nước dâng cao.\n- Gửi xe ở cổng.\n")


def test_safety_sentence_split_over_two_file_lines_still_reaches_the_notice():
    assert dong_tam_ngung("", [(HAI_DONG.tieu_de, HAI_DONG.dong)]) is None  # lỗi cũ: từng dòng rời không đủ ý
    dong = dong_tam_ngung("", [(HAI_DONG.tieu_de, _doan_bai(HAI_DONG))])
    assert dong is not None and "dừng chạy" in dong and "cấm xuất bến" in dong


def test_articles_whose_sentence_sits_on_one_line_keep_the_same_notice():
    assert dong_tam_ngung("", [(MOT_DONG.tieu_de, _doan_bai(MOT_DONG))]) == dong_tam_ngung("", [(MOT_DONG.tieu_de, MOT_DONG.dong)]) is not None

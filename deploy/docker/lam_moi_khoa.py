"""Dịch vụ phụ `khoa` (compose.vai-may.yml): giữ cho /run/hue-khoa/bedrock.json luôn là khoá tạm CÒN HẠN của vai gắn vào máy EC2.

Vì sao cần: lớp nối model (`backend/llm/bedrock_model.py`) không dùng thư viện AWS — nó tự ký từ MỘT file JSON ba khoá `accessKeyId`,
`secretAccessKey`, `sessionToken`, đọc lại ở mỗi lời gọi. Trên máy có vai gắn, khoá tạm của vai nằm ở dịch vụ thông tin máy (IMDSv2) dưới tên
trường khác (`AccessKeyId`, `SecretAccessKey`, `Token`) ⇒ tiến trình này đổi tên trường và ghi file; code sản phẩm không phải sửa.
Ghi kiểu "file tạm rồi đổi tên" để app không bao giờ đọc trúng file viết dở. Không in, không log giá trị khoá — chỉ giờ hết hạn và tên lớp lỗi.
Chỉ dùng thư viện chuẩn. Biến: HUE_IMDS (địa chỉ gốc, mặc định của AWS) · HUE_KHOA_DICH (file đích) · HUE_KHOA_NGHI (giây giữa hai lần, mặc định 300).
"""
import json
import os
import sys
import time
import urllib.request

IMDS = os.getenv("HUE_IMDS", "http://169.254.169.254")
DICH = os.getenv("HUE_KHOA_DICH", "/run/hue-khoa/bedrock.json")
NGHI = int(os.getenv("HUE_KHOA_NGHI", "300"))  # AWS đưa khoá mới ra trước khi khoá cũ hết hạn ít nhất 5 phút ⇒ 5 phút hỏi một lần là luôn còn hạn
NGHI_KHI_LOI = 15


def goi(duong: str, method: str = "GET", headers: dict | None = None) -> str:
    yeu_cau = urllib.request.Request(IMDS + duong, method=method, headers=headers or {})
    with urllib.request.urlopen(yeu_cau, timeout=5) as tra:
        return tra.read().decode()


def lay_khoa() -> dict:
    the = {"X-aws-ec2-metadata-token": goi("/latest/api/token", "PUT", {"X-aws-ec2-metadata-token-ttl-seconds": "300"})}
    vai = goi("/latest/meta-data/iam/security-credentials/", headers=the).split()[0]
    return json.loads(goi(f"/latest/meta-data/iam/security-credentials/{vai}", headers=the))


def ghi(khoa: dict) -> None:
    tam = DICH + ".tam"
    with os.fdopen(os.open(tam, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600), "w", encoding="utf-8") as f:
        json.dump({"accessKeyId": khoa["AccessKeyId"], "secretAccessKey": khoa["SecretAccessKey"], "sessionToken": khoa["Token"]}, f)
    os.replace(tam, DICH)


def main() -> None:
    while True:
        try:
            khoa = lay_khoa()
            ghi(khoa)
            print(f"đã ghi khoá tạm của vai, hết hạn {khoa.get('Expiration')}", flush=True)
            nghi = NGHI
        except Exception as loi:  # mạng, máy không có vai, JSON thiếu trường: giữ file cũ, thử lại sớm; chỉ in tên lớp lỗi (lời lỗi có thể mang dữ liệu)
            print(f"CHƯA lấy được khoá tạm của vai: {type(loi).__name__}", file=sys.stderr, flush=True)
            nghi = NGHI_KHI_LOI
        time.sleep(nghi)


if __name__ == "__main__":
    main()

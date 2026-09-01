# Bàn giao hiện hành

Target role: implementer
Authored by: reviewer
Handoff kind: implementation
State: active
Base commit: ba6b694
Head commit: worktree
Risk level: low
Git authorization: commit_and_push
Sub-agent authorization: none

---

## 1. Trạng thái hiện tại

- Triển khai xây dựng dữ liệu tri thức chuẩn hóa (curated answer-facing knowledge base) cho domain `festivals/` dưới `/home/minhhieu/hue_rag/knowledge-base-hue/festivals/`.
- Khuôn mẫu biên soạn chuẩn: `knowledge-base-hue/meta/festivals-template.md`.
- Danh mục 25 lễ hội cốt lõi đã phê duyệt: `knowledge-base-hue/festivals/hue_festivals_core_25.md`.
- Đã hoàn thành, rà soát và kiểm chứng độc lập với các nguồn tư liệu chính thống (Cổng thông tin Chính phủ, Bộ VHTTDL, Báo Nhân Dân, Cổng TTĐT TP Huế) cho 2 entity lễ hội đầu tiên:
  1. `knowledge-base-hue/festivals/festival/1 Festival Huế.md`
  2. `knowledge-base-hue/festivals/festival/2 Festival Nghề truyền thống Huế.md`
- Người dùng đã xác nhận phê duyệt chất lượng của 2 entity đầu tiên và ủy quyền Git: `commit_and_push`.

## 2. Nhiệm vụ tiếp theo của Implementer

- Tiếp tục biên soạn dữ liệu các entity tiếp theo trong danh sách 25 lễ hội cốt lõi tại `knowledge-base-hue/festivals/festival/` theo khuôn mẫu `knowledge-base-hue/meta/festivals-template.md`.
- Entity tiếp theo:
  - Entity 3: `3 Lễ hội Áo dài Huế.md`
  - Entity 4: `4 Lễ hội Điện Huệ Nam.md`
  - ... (tuần tự theo danh mục `hue_festivals_core_25.md`).
- Tiếp tục tuân thủ nghiêm ngặt nguyên tắc: chính xác, ranh giới entity rõ ràng, tri thức bền vững (bảo vệ temporal grounding), không suy diễn quan hệ nhân quả, không đưa giá vé chi tiết vào entity file.

## 3. Ranh giới hiện hành

Chưa authorize:
- Thay đổi chunker, embedding, vectorstore Qdrant, retrieval runtime hoặc code backend;
- Thay đổi các domain dữ liệu khác ngoài `festivals/`;
- Tự ý khởi tạo sub-agent.

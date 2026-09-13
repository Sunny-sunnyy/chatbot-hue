# Qwen3 Remote GPU Offloading — Research Context

Status: queued after Full-corpus Phase 4 final review/User closure; not an
approved design or implementation plan
Owner: Reviewer
Date: 2026-09-13 +07

## 1. Mục tiêu deferred

Nghiên cứu cách chạy riêng dense inference của
`Qwen/Qwen3-Embedding-0.6B` trên GPU remote có khoảng 16 GB VRAM, trong khi ba
candidate E5-small, E5-base và HuyDang tiếp tục chạy CPU local. Qdrant vẫn local.

Ưu tiên hai nhánh:

1. GPU miễn phí/free-credit có cách sử dụng hợp lệ và ổn định, ưu tiên T4
   16 GB cùng SSH/remote job nếu nền tảng chính thức hỗ trợ;
2. fallback thuê Vast.ai qua SSH, ưu tiên RTX 5060 Ti 16 GB hoặc GPU 16 GB phù
   hợp hơn nếu evidence về compatibility/reliability/cost tốt hơn.

Không giả định có thể chuyển một GPU của Colab sang nền tảng khác. GPU gắn với
runtime của provider; cần dùng Colab theo notebook batch hoặc thuê/tạo một
instance tương đương ở provider khác.

## 2. Trạng thái project liên quan

Contract Qwen hiện hành:

```text
model: Qwen/Qwen3-Embedding-0.6B
revision: 97b0c614be4d77ee51c0cef4e5f07c00f9eb65b3
dimension: 1024
device/dtype: cuda/float16
attention: eager
document preprocessing: raw Representation A
batch size: 1
chunk count: 8460
max observed Qwen tokens: 560
```

Phase 3 smoke trên GTX 1650 ghi nhận model allocation khoảng 1.20 GB, reserved
1.41 GB và peak khoảng 1.32 GB ở batch 1. Vì vậy 16 GB VRAM là đủ cho model và
có headroom tăng batch; chưa có evidence để khóa batch 32 hoặc 64.

Ngày 2026-09-13, Reviewer read-only quan sát cả bốn Phase 4 collections có đúng
8.460 points và bốn final build records tồn tại. Đây là observed state, chưa
thay completion report/final review/User closure. Remote offloading nhắm tới
re-indexing hoặc experiment tiếp theo; không rewrite provenance của live build
vừa hoàn thành.

## 3. Kết luận sơ bộ phải kiểm chứng tiếp

### Colab

Colab Free phù hợp với interactive notebook/batch artifact. Không chọn reverse
tunnel API làm baseline vì free managed runtime không bảo đảm GPU/quota, có thể
timeout, và Google liệt kê SSH/remote control cùng distributed workers trong
nhóm hoạt động bị hạn chế khi không có positive compute-unit balance.

Nguồn chính thức:

- https://research.google.com/colaboratory/faq.html
- https://research.google.com/colaboratory/local-runtimes.html

### Lightning AI hoặc nền tảng free-credit khác

Lightning AI hiện công bố free monthly credits, T4 16 GB và SSH/IDE access.
Research phải xác minh availability theo khu vực/tài khoản, điều kiện phone
verification, interruptibility, quota thực nhận, storage/network và khả năng
chạy exact locked environment. Không coi thông tin quảng cáo là guaranteed
capacity.

Nguồn chính thức:

- https://lightning.ai/docs/overview/ai-studio/
- https://lightning.ai/pricing/

### Vast.ai

Vast.ai hỗ trợ SSH key-only, direct hoặc proxy SSH, file transfer và instance
theo marketplace. Direct SSH được ưu tiên nếu offer hỗ trợ. On-demand phù hợp
cho first controlled run; interruptible chỉ phù hợp sau khi workflow đã có
checkpoint/resume.

Instance bị stop vẫn có storage charges; destroy mới dừng toàn bộ billing và
xóa dữ liệu không thể phục hồi. Mọi rent/create/stop/destroy là external paid
mutation, cần exact User approval riêng.

Nguồn chính thức:

- https://docs.vast.ai/guides/instances/connect/ssh
- https://docs.vast.ai/guides/instances/overview
- https://docs.vast.ai/guides/instances/choosing/instance-types
- https://docs.vast.ai/cli/hello-world
- https://docs.vast.ai/api-reference/instances/destroy-instance

### RTX 5060 Ti 16 GB

RTX 5060 Ti là GPU Blackwell và có phiên bản 16 GB. 16 GB VRAM đủ về capacity
cho Qwen3-Embedding-0.6B FP16; throughput/batch vẫn phải benchmark trên corpus.
Blackwell cần software stack phù hợp. NVIDIA ghi CUDA 12.8 là first toolkit
support; PyTorch hỗ trợ Blackwell từ 2.7 với CUDA 12.8, và các release mới dùng
CUDA 13.x. Offer Vast phải được kiểm driver, compute capability và một real
smoke encode trước full run.

Nguồn chính thức:

- https://nvidianews.nvidia.com/_gallery/download_pdf/67fe58ae3d63325f115ecd52/
- https://docs.nvidia.com/cuda/blackwell-compatibility-guide/index.html
- https://pytorch.org/blog/pytorch-2-7/

## 4. Kiến trúc candidate cần so sánh

### A — Batch artifact, Qdrant local

```text
local canonical chunks
  -> content-addressed input bundle
  -> remote GPU dense encode only
  -> matrix + manifest + SHA-256
  -> local fail-closed import
  -> local sparse construction/Qdrant upsert/verification
```

Đây là baseline được khuyến nghị cho Colab và cũng là baseline đơn giản nhất
trên Vast/Lightning. Không upload `.env`, Qdrant credentials, Foods data hoặc
toàn repository nếu không cần.

Current Phase 4 contract không cho persist dense matrix. Muốn dùng kiến trúc
này trong production re-index phải có design addendum/spec/plan/Review Contract
và User approval trước implementation.

### B — Remote embedding service qua SSH tunnel

Chỉ đánh giá như option thứ hai trên provider chính thức hỗ trợ SSH/service
hosting, ví dụ Vast/Lightning. Không dùng public unauthenticated endpoint.
Research phải chứng minh service giải quyết repeated online workload thật;
one-off ingestion không đủ lý do thêm FastAPI, tunnel và lifecycle server.

Không expose local Qdrant ra Internet. Nếu cần service, local client kết nối qua
SSH port forwarding, có authentication/request bounds/timeouts và exact query
instruction. Colab Free reverse tunnel không phải candidate baseline.

## 5. Research questions bắt buộc

1. Nền tảng free/free-credit nào thực sự cho SSH hoặc remote job hợp lệ, T4
   16 GB, thời lượng đủ và availability khả dụng tại Việt Nam?
2. Colab batch, Lightning T4 SSH và Vast on-demand khác nhau thế nào về setup,
   interruption, storage, bandwidth, privacy, reproducibility và tổng chi phí?
3. Vast offer filters nào phải khóa: GPU RAM, verified/Secure Cloud,
   reliability, direct ports, CUDA/driver, CPU/RAM, disk, bandwidth, max
   duration và on-demand/interruptible?
4. RTX 5060 Ti 16 GB hay T4 16 GB phù hợp hơn với exact PyTorch stack? Có
   compatibility trap nào với Blackwell kernels/attention backend?
5. Batch 1/4/8/16/32 có throughput, peak VRAM và output drift thế nào trên
   representative short/median/max-token samples? Batch 64 chỉ xét nếu có
   headroom evidence.
6. Artifact contract tối thiểu nào đủ bảo vệ corpus identity, ordered row IDs,
   model revision, preprocessing, runtime, shape/dtype/norm và file integrity?
7. Exact cleanup/billing procedure nào bảo đảm đã lấy output và destroy instance
   mà không mất evidence hoặc tiếp tục phát sinh phí?

## 6. Safety và authority

- Research dùng web/read-only local evidence; không đăng nhập provider.
- Không tạo tài khoản, SSH/API key, instance, volume, tunnel hoặc public port.
- Không upload corpus/repository/secret và không thuê GPU khi chưa có approval.
- Không sửa runtime, dependencies, Phase 4 records/collections hoặc current
  artifacts.
- Không query/access Foods collections.
- Không dự báo thời gian/throughput/cost như fact khi chưa đo hoặc chưa đọc live
  marketplace offer.
- Không Git operation.

## 7. Deliverable mong đợi

Một research report có source links và bảng decision gồm ít nhất:

- Colab batch;
- một nền tảng T4 free/free-credit hỗ trợ SSH/remote workflow nếu xác minh được;
- Vast.ai T4 16 GB;
- Vast.ai RTX 5060 Ti 16 GB.

Report phải chọn một baseline, một fallback, nêu exact provider/GPU/runtime/data
flow, ước tính chi phí dưới dạng snapshot có timestamp, benchmark plan,
security/billing teardown và các User approval gates. Dừng để thảo luận; chưa
viết implementation spec/plan và chưa triển khai.

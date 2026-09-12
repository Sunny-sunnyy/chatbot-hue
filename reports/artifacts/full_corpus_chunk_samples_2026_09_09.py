#!/usr/bin/env python3
"""
Khảo sát phân chia mẫu văn bản và đo token thực tế bằng các tokenizer local.
Dự án: /home/minhhieu/hue_rag
Mục tiêu: Đề xuất cách chia chung các mẫu Gia Lạc, Ngọ Môn, bảng Ca Huế và đối chứng Mệ Kéo, Biển/Đầm phá;
đo độ dài input thực tế (không truncation) bằng từng tokenizer local:
- intfloat/multilingual-e5-small (limit: 512)
- intfloat/multilingual-e5-base (limit: 512)
- CODE4LIFEOFFICIAL/huydang-dek21-embedding (limit: 256)
- cross-encoder/ms-marco-MiniLM-L-6-v2 (limit: 512 pair query/doc)

LƯỢT CẬP NHẬT 2 (2026-09-09):
- Chuẩn hóa query cố định theo từng tài liệu nguồn (1 query gốc + 1 query dài duy nhất cho mọi phương án đem so sánh).
- Bổ sung Phương án 3 cho Ca Huế (chia theo hàng/nhóm nhỏ kèm điều kiện lặp khi ingest: Biến thể 3A và Biến thể 3B).
- Phân biệt rành mạch giữa độ bao phủ nội dung (content coverage) và độ bao phủ ký tự tuyệt đối (character coverage).
"""

import json
from pathlib import Path
from transformers import AutoTokenizer
from pyvi import ViTokenizer

ROOT = Path('/home/minhhieu/hue_rag/knowledge-base-hue')
CACHE = Path('/home/minhhieu/.cache/huggingface/hub')
OUT_JSON = Path('/home/minhhieu/hue_rag/reports/artifacts/full_corpus_chunk_samples_2026_09_09.json')

MODELS = {
    'e5_small': ('intfloat--multilingual-e5-small', '614241f622f53c4eeff9890bdc4f31cfecc418b3'),
    'e5_base': ('intfloat--multilingual-e5-base', 'd128750597153bb5987e10b1c3493a34e5a4502a'),
    'huydang': ('CODE4LIFEOFFICIAL--huydang-dek21-embedding', '517f1af7dd04a57194f1de2990f0c6ede0a3109b'),
    'minilm': ('cross-encoder--ms-marco-MiniLM-L-6-v2', '233902d25c440f23af6f7d6e94d2946bac0bee0a'),
}

LIMITS = {
    'e5_small': 512,
    'e5_base': 512,
    'huydang': 256,
    'minilm': 512,
}

# QUERIES CỐ ĐỊNH THEO TỪNG TÀI LIỆU NGUỒN (Dùng chung cho mọi phương án của cùng tài liệu)
QUERIES = {
    'gia_lac': {
        'orig': 'Hội xuân Gia Lạc tổ chức ở đâu và vào thời gian nào?',
        'long': 'Lễ hội xuân Gia Lạc trong lịch sử và các kỳ phục dựng chuyên đề hiện nay được tổ chức vào thời gian nào, tại địa điểm nào?'
    },
    'ngo_mon': {
        'orig': 'Ngọ Môn có cấu trúc và ý nghĩa lịch sử như thế nào?',
        'long': 'Cửa Ngọ Môn Hoàng thành Huế được xây dựng vào năm nào, cấu trúc đài nền cùng lầu Ngũ Phụng có đặc điểm kiến trúc và ý nghĩa lịch sử ra sao?'
    },
    'ca_hue': {
        'orig': 'Vé Ca Huế cho trẻ em được tính như thế nào?',
        'long': 'Giá vé xem Ca Huế ghép thuyền trên sông Hương cho người lớn và trẻ em bao nhiêu tiền một người, áp dụng điều kiện bao gồm và không bao gồm những dịch vụ gì?'
    },
    'control_me_keo': {
        'orig': 'Quán bún bò Mệ Kéo mở cửa đến mấy giờ?',
        'long': 'Quán bún bò Mệ Kéo nằm ở địa chỉ nào tại Huế, mở bán trong khung giờ nào và mức giá mỗi tô dao động khoảng bao nhiêu?'
    },
    'control_sea_module': {
        'orig': 'Có thể thay ngày cuối bằng đi biển và đầm phá không?',
        'long': 'Nếu muốn đổi lịch trình ngày thứ ba sang tham quan biển Thuận An hoặc phá Tam Giang thì cần lưu ý những điều kiện thời tiết nào?'
    }
}

print("Đang nạp tokenizer từ local cache HF (local_files_only=True)...")
TOK = {
    key: AutoTokenizer.from_pretrained(
        str(CACHE / ('models--' + model) / 'snapshots' / rev),
        local_files_only=True
    )
    for key, (model, rev) in MODELS.items()
}

def load_source(rel_path: str) -> str:
    """Đọc tệp nguồn UTF-8, chuẩn hóa CRLF/CR thành LF; không Unicode-normalize."""
    raw = (ROOT / rel_path).read_bytes().decode('utf-8')
    return raw.replace('\r\n', '\n').replace('\r', '\n')

def measure_tokens(search_text: str, query_orig: str, query_long: str):
    """Đo số lượng token không truncation cho 4 mô hình."""
    counts = {}
    for name, tok in TOK.items():
        if name.startswith('e5'):
            data = tok('passage: ' + search_text, add_special_tokens=True, truncation=False, verbose=False)
            counts[name] = len(data['input_ids'])
        elif name == 'huydang':
            segmented = ViTokenizer.tokenize(search_text)
            data = tok(segmented, add_special_tokens=True, truncation=False, verbose=False)
            counts[name] = len(data['input_ids'])
        else:
            data_orig = tok(query_orig, search_text, add_special_tokens=True, truncation=False, verbose=False)
            counts['minilm_orig'] = len(data_orig['input_ids'])
            data_long = tok(query_long, search_text, add_special_tokens=True, truncation=False, verbose=False)
            counts['minilm_long'] = len(data_long['input_ids'])
    return counts

def build_chunk(
    chunk_id: str,
    sample_group: str,
    proposal_type: str,
    rel_path: str,
    title: str,
    heading_path: list[str],
    evidence_specs: list[dict],
    search_text_builder,
    description: str
):
    source_text = load_source(rel_path)
    evidence_parts = []
    for spec in evidence_specs:
        start = spec['start']
        end = spec['end']
        part_text = source_text[start:end]
        if 'expected_text' in spec:
            assert part_text == spec['expected_text'], f"Mismatch at span [{start}:{end}]"
        exact_match = (source_text[start:end] == part_text)
        evidence_parts.append({
            'role': spec['role'],
            'span': {'start': start, 'end': end},
            'characters': len(part_text),
            'text': part_text,
            'exact_match': exact_match
        })

    label = title + '\n' + ' > '.join(heading_path) + '\n'
    search_text = search_text_builder(label, evidence_parts)

    query_orig = QUERIES[sample_group]['orig']
    query_long = QUERIES[sample_group]['long']
    tokens = measure_tokens(search_text, query_orig, query_long)

    exceeded = []
    if tokens['e5_small'] > LIMITS['e5_small']: exceeded.append('e5_small')
    if tokens['e5_base'] > LIMITS['e5_base']: exceeded.append('e5_base')
    if tokens['huydang'] > LIMITS['huydang']: exceeded.append('huydang')
    if tokens['minilm_orig'] > LIMITS['minilm']: exceeded.append('minilm_orig')
    if tokens['minilm_long'] > LIMITS['minilm']: exceeded.append('minilm_long')

    status = 'PASS_ALL' if not exceeded else f"EXCEEDS_{'_'.join(exceeded)}"

    return {
        'chunk_id': chunk_id,
        'sample_group': sample_group,
        'proposal_type': proposal_type,
        'source_file': rel_path,
        'title': title,
        'heading_path': heading_path,
        'description': description,
        'evidence_parts': evidence_parts,
        'search_text': search_text,
        'search_text_characters': len(search_text),
        'label_characters': len(label),
        'body_characters': len(search_text) - len(label),
        'query_orig': query_orig,
        'query_long': query_long,
        'tokens': tokens,
        'limits': LIMITS,
        'exceeded_models': exceeded,
        'status': status
    }

# ==============================================================================
# ĐỊNH NGHĨA CÁC MẪU VÀ PHƯƠNG ÁN CHIA
# ==============================================================================

chunks = []

# ------------------------------------------------------------------------------
# 1. HỘI XUÂN GIA LẠC (festivals/festival/Hội xuân Gia Lạc.md)
# ------------------------------------------------------------------------------
gia_lac_path = 'festivals/festival/Hội xuân Gia Lạc.md'
gia_lac_title = "Hội xuân Gia Lạc"
gia_lac_hpath = ["Thông tin chung"]

# 1.0 Khối cũ khảo sát mục 19 (Oversized Baseline)
chunks.append(build_chunk(
    chunk_id="gia_lac_baseline_oversized",
    sample_group="gia_lac",
    proposal_type="baseline_oversized",
    rel_path=gia_lac_path,
    title=gia_lac_title,
    heading_path=gia_lac_hpath,
    evidence_specs=[
        {'role': 'full_body', 'start': 40, 'end': 1211}
    ],
    search_text_builder=lambda lbl, parts: lbl + parts[0]['text'],
    description="Khối nguyên mẫu mục Thông tin chung đo ở phiên trước; vượt giới hạn HuyDang (272 > 256) và chạm trần MiniLM (512)."
))

# 1.1 Phương án 1 (Ưu tiên: 2 chunks chia theo nhóm ý nghĩa liền mạch)
chunks.append(build_chunk(
    chunk_id="gia_lac_p1_chunk_1",
    sample_group="gia_lac",
    proposal_type="preferred_p1",
    rel_path=gia_lac_path,
    title=gia_lac_title,
    heading_path=gia_lac_hpath,
    evidence_specs=[
        {'role': 'body', 'start': 40, 'end': 590}
    ],
    search_text_builder=lambda lbl, parts: lbl + parts[0]['text'],
    description="Định danh, loại hình phiên chợ và thời gian tổ chức; bảo toàn quan hệ cha-con phân biệt mốc 3 ngày Tết cổ truyền và phục dựng hiện nay."
))

chunks.append(build_chunk(
    chunk_id="gia_lac_p1_chunk_2",
    sample_group="gia_lac",
    proposal_type="preferred_p1",
    rel_path=gia_lac_path,
    title=gia_lac_title,
    heading_path=gia_lac_hpath,
    evidence_specs=[
        {'role': 'body', 'start': 591, 'end': 1211}
    ],
    search_text_builder=lambda lbl, parts: lbl + parts[0]['text'],
    description="Địa điểm tổ chức lịch sử vs đương đại và nét văn hóa đặc thù du xuân cầu may, phân biệt với chợ thương mại."
))

# 1.2 Phương án 2 (Trade-off: 3 chunks chia nhỏ theo khía cạnh hẹp)
chunks.append(build_chunk(
    chunk_id="gia_lac_p2_chunk_1",
    sample_group="gia_lac",
    proposal_type="alternative_p2",
    rel_path=gia_lac_path,
    title=gia_lac_title,
    heading_path=gia_lac_hpath,
    evidence_specs=[
        {'role': 'identity_and_type', 'start': 40, 'end': 396},
        {'role': 'cultural_nature', 'start': 939, 'end': 1211}
    ],
    search_text_builder=lambda lbl, parts: lbl + parts[0]['text'] + '\n' + parts[1]['text'],
    description="Phương án 2 Chunk 1: Tách riêng định danh và tính chất phi thương mại (ghép 2 đoạn không liên tục; 155 HuyDang tokens)."
))

chunks.append(build_chunk(
    chunk_id="gia_lac_p2_chunk_2",
    sample_group="gia_lac",
    proposal_type="alternative_p2",
    rel_path=gia_lac_path,
    title=gia_lac_title,
    heading_path=gia_lac_hpath,
    evidence_specs=[
        {'role': 'time_schedule', 'start': 397, 'end': 590}
    ],
    search_text_builder=lambda lbl, parts: lbl + parts[0]['text'],
    description="Phương án 2 Chunk 2: Chỉ giữ mục thời gian tổ chức (giữ phân nhánh lịch sử và hiện nay; 51 HuyDang tokens)."
))

chunks.append(build_chunk(
    chunk_id="gia_lac_p2_chunk_3",
    sample_group="gia_lac",
    proposal_type="alternative_p2",
    rel_path=gia_lac_path,
    title=gia_lac_title,
    heading_path=gia_lac_hpath,
    evidence_specs=[
        {'role': 'locations', 'start': 591, 'end': 938}
    ],
    search_text_builder=lambda lbl, parts: lbl + parts[0]['text'],
    description="Phương án 2 Chunk 3: Chỉ giữ mục địa điểm tổ chức (phân biệt ngã ba Nam Phổ và địa điểm công cộng như Chợ Mai; 85 HuyDang tokens)."
))

# ------------------------------------------------------------------------------
# 2. NGỌ MÔN — ĐẠI NỘI HUẾ (heritages/heritage/Đại Nội Huế.md)
# ------------------------------------------------------------------------------
ngo_mon_path = 'heritages/heritage/Đại Nội Huế.md'
ngo_mon_title = "Đại Nội Huế"
ngo_mon_hpath = ["Các công trình kiến trúc hạt nhân của Hoàng thành", "Ngọ Môn"]

# 2.0 Khối cũ khảo sát mục 19 (Oversized Baseline)
chunks.append(build_chunk(
    chunk_id="ngo_mon_baseline_oversized",
    sample_group="ngo_mon",
    proposal_type="baseline_oversized",
    rel_path=ngo_mon_path,
    title=ngo_mon_title,
    heading_path=ngo_mon_hpath,
    evidence_specs=[
        {'role': 'full_body', 'start': 10219, 'end': 11945}
    ],
    search_text_builder=lambda lbl, parts: lbl + parts[0]['text'],
    description="Toàn bộ mục Ngọ Môn 1.726 ký tự đo ở phiên trước; vượt giới hạn của tất cả mô hình (E5: 530 > 512, HuyDang: 423 > 256, MiniLM: 738 > 512)."
))

# 2.1 Phương án 1 (Ưu tiên: 2 chunks chia theo cấu trúc vật lý: Nền đài & Lầu Ngũ Phụng)
chunks.append(build_chunk(
    chunk_id="ngo_mon_p1_chunk_1",
    sample_group="ngo_mon",
    proposal_type="preferred_p1",
    rel_path=ngo_mon_path,
    title=ngo_mon_title,
    heading_path=ngo_mon_hpath,
    evidence_specs=[
        {'role': 'intro_and_base_platform', 'start': 10219, 'end': 11068}
    ],
    search_text_builder=lambda lbl, parts: lbl + parts[0]['text'],
    description="Khái quát khởi dựng 1833, ý nghĩa Kinh Dịch phương Nam và cấu trúc đài nền chữ U với 5 lối đi vòm cuốn (Ngọ Môn, Tả/Hữu Giáp, Tả/Hữu Dịch)."
))

chunks.append(build_chunk(
    chunk_id="ngo_mon_p1_chunk_2",
    sample_group="ngo_mon",
    proposal_type="preferred_p1",
    rel_path=ngo_mon_path,
    title=ngo_mon_title,
    heading_path=ngo_mon_hpath,
    evidence_specs=[
        {'role': 'ngu_phung_and_history', 'start': 11069, 'end': 11945}
    ],
    search_text_builder=lambda lbl, parts: lbl + parts[0]['text'],
    description="Kiến trúc lầu Ngũ Phụng (100 cột, 9 bộ mái phụng bay, ngói hoàng/thanh lưu ly) và các đại lễ quốc gia cùng sự kiện vua Bảo Đại thoái vị 30/08/1945."
))

# 2.2 Phương án 2 (Trade-off: 3 chunks chia nhỏ độc lập kiến trúc lầu và ý nghĩa lịch sử)
chunks.append(build_chunk(
    chunk_id="ngo_mon_p2_chunk_1",
    sample_group="ngo_mon",
    proposal_type="alternative_p2",
    rel_path=ngo_mon_path,
    title=ngo_mon_title,
    heading_path=ngo_mon_hpath,
    evidence_specs=[
        {'role': 'intro_and_base_platform', 'start': 10219, 'end': 11068}
    ],
    search_text_builder=lambda lbl, parts: lbl + parts[0]['text'],
    description="Phương án 2 Chunk 1: Tương tự P1 Chunk 1 (Đoạn dẫn + Đài nền 5 cửa vòm; đo cùng bộ query chuẩn hóa)."
))

chunks.append(build_chunk(
    chunk_id="ngo_mon_p2_chunk_2",
    sample_group="ngo_mon",
    proposal_type="alternative_p2",
    rel_path=ngo_mon_path,
    title=ngo_mon_title,
    heading_path=ngo_mon_hpath,
    evidence_specs=[
        {'role': 'ngu_phung_architecture', 'start': 11069, 'end': 11550}
    ],
    search_text_builder=lambda lbl, parts: lbl + parts[0]['text'],
    description="Phương án 2 Chunk 2: Tách riêng mô tả mỹ thuật và kết cấu kiến trúc của Lầu Ngũ Phụng."
))

chunks.append(build_chunk(
    chunk_id="ngo_mon_p2_chunk_3",
    sample_group="ngo_mon",
    proposal_type="alternative_p2",
    rel_path=ngo_mon_path,
    title=ngo_mon_title,
    heading_path=ngo_mon_hpath,
    evidence_specs=[
        {'role': 'historical_significance', 'start': 11551, 'end': 11945}
    ],
    search_text_builder=lambda lbl, parts: lbl + parts[0]['text'],
    description="Phương án 2 Chunk 3: Tách riêng các đại lễ quốc gia và biến cố thoái vị năm 1945 thành chunk độc lập."
))

# ------------------------------------------------------------------------------
# 3. BẢNG CA HUẾ KHÁCH LẺ (travel/tickets/Vé biểu diễn nghệ thuật và trải nghiệm sông Hương.md)
# ------------------------------------------------------------------------------
ca_hue_path = 'travel/tickets/Vé biểu diễn nghệ thuật và trải nghiệm sông Hương.md'
ca_hue_title = "Vé biểu diễn nghệ thuật và trải nghiệm sông Hương"
ca_hue_hpath = [
    "2. Ca Huế trên sông Hương và dịch vụ thuyền rồng",
    "2.3. Chi tiết bảng giá khảo sát dịch vụ Ca Huế",
    "A. Vé khách lẻ ghép thuyền (Tour ghép đoàn)"
]

# Spans chuẩn xác:
# Survey intro 2.3: [10409, 10591) (182 chars)
# Heading A: [10593, 10641) (48 chars)
# Intro tour format: [10643, 10758) (115 chars)
# Header table: [10760, 10900) (140 chars)
# Row Khách VN: [10901, 11158) (257 chars)
# Row Khách QT: [11159, 11317) (158 chars)
# Row Adults (VN+QT): [10901, 11317) (416 chars)
# Row Child Height (Lá Quê): [11318, 11581) (263 chars)
# Row Child Age (Thuyền Rồng): [11582, 11810) (228 chars)
# Row Children (cả 2): [11318, 11810) (492 chars)
# Cond All (Bao gồm + Không bao gồm): [11812, 12287) (475 chars)
# Cond Bao gồm: [11812, 12116] (304 chars)
# Cond Không bao gồm: [12117, 12287] (170 chars)

# 3.0 Khối cũ khảo sát mục 19 (Chỉ bảng 4 hàng, chưa có intro và điều kiện)
chunks.append(build_chunk(
    chunk_id="ca_hue_baseline_table_only",
    sample_group="ca_hue",
    proposal_type="baseline_oversized",
    rel_path=ca_hue_path,
    title=ca_hue_title,
    heading_path=ca_hue_hpath,
    evidence_specs=[
        {'role': 'table_header', 'start': 10760, 'end': 10900},
        {'role': 'table_all_rows', 'start': 10901, 'end': 11810}
    ],
    search_text_builder=lambda lbl, parts: lbl + parts[0]['text'] + '\n' + parts[1]['text'],
    description="Khối bảng 4 hàng đo ở phiên trước; thiếu intro và thiếu điều kiện bao gồm/không bao gồm; vượt HuyDang (339 > 256) và MiniLM (574 > 512)."
))

# 3.0b Thử nghiệm ép gộp điều kiện vào bảng giá lớn
chunks.append(build_chunk(
    chunk_id="ca_hue_test_forced_adult_with_cond",
    sample_group="ca_hue",
    proposal_type="diagnostic_forced_violation",
    rel_path=ca_hue_path,
    title=ca_hue_title,
    heading_path=ca_hue_hpath,
    evidence_specs=[
        {'role': 'table_header', 'start': 10760, 'end': 10900},
        {'role': 'adult_rows', 'start': 10901, 'end': 11317},
        {'role': 'conditions', 'start': 11812, 'end': 12287}
    ],
    search_text_builder=lambda lbl, parts: lbl + parts[0]['text'] + '\n' + parts[1]['text'] + '\n\n' + parts[2]['text'],
    description="Thử nghiệm ép gộp điều kiện Bao gồm/Không bao gồm vào bảng vé người lớn; vượt HuyDang (283 > 256) và MiniLM (548 > 512)."
))

chunks.append(build_chunk(
    chunk_id="ca_hue_test_forced_child_with_cond",
    sample_group="ca_hue",
    proposal_type="diagnostic_forced_violation",
    rel_path=ca_hue_path,
    title=ca_hue_title,
    heading_path=ca_hue_hpath,
    evidence_specs=[
        {'role': 'table_header', 'start': 10760, 'end': 10900},
        {'role': 'child_rows', 'start': 11318, 'end': 11810},
        {'role': 'conditions', 'start': 11812, 'end': 12287}
    ],
    search_text_builder=lambda lbl, parts: lbl + parts[0]['text'] + '\n' + parts[1]['text'] + '\n\n' + parts[2]['text'],
    description="Thử nghiệm ép gộp điều kiện Bao gồm/Không bao gồm vào bảng vé trẻ em; vượt HuyDang (344 > 256) và MiniLM (598 > 512)."
))

# 3.1 Phương án 1 (3 chunks phân tách đối tượng & điều kiện dịch vụ riêng)
chunks.append(build_chunk(
    chunk_id="ca_hue_p1_chunk_1",
    sample_group="ca_hue",
    proposal_type="preferred_p1",
    rel_path=ca_hue_path,
    title=ca_hue_title,
    heading_path=ca_hue_hpath,
    evidence_specs=[
        {'role': 'table_header', 'start': 10760, 'end': 10900},
        {'role': 'adult_rows', 'start': 10901, 'end': 11317}
    ],
    search_text_builder=lambda lbl, parts: lbl + parts[0]['text'] + '\n' + parts[1]['text'],
    description="P1 Chunk 1: Vé ghép thuyền người lớn (Khách VN 100k-130k và Khách QT 150k kèm hoa đăng, thuyết minh song ngữ)."
))

chunks.append(build_chunk(
    chunk_id="ca_hue_p1_chunk_2",
    sample_group="ca_hue",
    proposal_type="preferred_p1",
    rel_path=ca_hue_path,
    title=ca_hue_title,
    heading_path=ca_hue_hpath,
    evidence_specs=[
        {'role': 'table_header', 'start': 10760, 'end': 10900},
        {'role': 'child_rows', 'start': 11318, 'end': 11810}
    ],
    search_text_builder=lambda lbl, parts: lbl + parts[0]['text'] + '\n' + parts[1]['text'],
    description="P1 Chunk 2: Chính sách vé trẻ em theo 2 tiêu chí khảo sát: chiều cao (Lá Quê) và độ tuổi (Thuyền Rồng Huế); HuyDang 243 tokens (sát trần 95%)."
))

chunks.append(build_chunk(
    chunk_id="ca_hue_p1_chunk_3",
    sample_group="ca_hue",
    proposal_type="preferred_p1",
    rel_path=ca_hue_path,
    title=ca_hue_title,
    heading_path=ca_hue_hpath,
    evidence_specs=[
        {'role': 'intro_tour_format', 'start': 10643, 'end': 10758},
        {'role': 'conditions', 'start': 11812, 'end': 12287}
    ],
    search_text_builder=lambda lbl, parts: lbl + parts[0]['text'] + '\n\n' + parts[1]['text'],
    description="P1 Chunk 3: Hình thức ghép thuyền rồng đôi (25-35 khách) và điều kiện chi tiết: Bao gồm (50 phút, áo dài, hoa đăng) + Không bao gồm (đưa đón, ăn uống cá nhân, tip)."
))

# 3.2 Phương án 2 (4 chunks phân định nhà cung cấp vé trẻ em & điều kiện riêng)
chunks.append(build_chunk(
    chunk_id="ca_hue_p2_chunk_1",
    sample_group="ca_hue",
    proposal_type="alternative_p2",
    rel_path=ca_hue_path,
    title=ca_hue_title,
    heading_path=ca_hue_hpath,
    evidence_specs=[
        {'role': 'table_header', 'start': 10760, 'end': 10900},
        {'role': 'adult_rows', 'start': 10901, 'end': 11317}
    ],
    search_text_builder=lambda lbl, parts: lbl + parts[0]['text'] + '\n' + parts[1]['text'],
    description="P2 Chunk 1: Vé người lớn (tương tự P1 Chunk 1)."
))

chunks.append(build_chunk(
    chunk_id="ca_hue_p2_chunk_2a",
    sample_group="ca_hue",
    proposal_type="alternative_p2",
    rel_path=ca_hue_path,
    title=ca_hue_title,
    heading_path=ca_hue_hpath,
    evidence_specs=[
        {'role': 'table_header', 'start': 10760, 'end': 10900},
        {'role': 'child_row_la_que', 'start': 11318, 'end': 11581}
    ],
    search_text_builder=lambda lbl, parts: lbl + parts[0]['text'] + '\n' + parts[1]['text'],
    description="P2 Chunk 2a: Bảng giá trẻ em Lá Quê Travel theo chiều cao (<1m miễn phí, 1m-<1.3m 70k-100k, >=1.3m vé người lớn)."
))

chunks.append(build_chunk(
    chunk_id="ca_hue_p2_chunk_2b",
    sample_group="ca_hue",
    proposal_type="alternative_p2",
    rel_path=ca_hue_path,
    title=ca_hue_title,
    heading_path=ca_hue_hpath,
    evidence_specs=[
        {'role': 'table_header', 'start': 10760, 'end': 10900},
        {'role': 'child_row_thuyen_rong', 'start': 11582, 'end': 11810}
    ],
    search_text_builder=lambda lbl, parts: lbl + parts[0]['text'] + '\n' + parts[1]['text'],
    description="P2 Chunk 2b: Bảng giá trẻ em Thuyền Rồng Huế theo độ tuổi (<4 tuổi miễn phí, 4-9 tuổi 50%-70%, >=10 tuổi 100%)."
))

chunks.append(build_chunk(
    chunk_id="ca_hue_p2_chunk_3",
    sample_group="ca_hue",
    proposal_type="alternative_p2",
    rel_path=ca_hue_path,
    title=ca_hue_title,
    heading_path=ca_hue_hpath,
    evidence_specs=[
        {'role': 'intro_tour_format', 'start': 10643, 'end': 10758},
        {'role': 'conditions', 'start': 11812, 'end': 12287}
    ],
    search_text_builder=lambda lbl, parts: lbl + parts[0]['text'] + '\n\n' + parts[1]['text'],
    description="P2 Chunk 3: Điều kiện dịch vụ và hình thức tour ghép (tương tự P1 Chunk 3)."
))

# 3.3 PHƯƠNG ÁN 3 BỔ SUNG: CHIA THEO HÀNG/NHÓM NHỎ KÈM ĐIỀU KIỆN LẶP KHI INGEST
# ------------------------------------------------------------------------------
# Biến thể 3A: Chia lẻ từng hàng + Lặp ĐẦY ĐỦ cả Bao gồm & Không bao gồm (475 ký tự)
chunks.append(build_chunk(
    chunk_id="ca_hue_p3a_chunk_1",
    sample_group="ca_hue",
    proposal_type="supplementary_p3a",
    rel_path=ca_hue_path,
    title=ca_hue_title,
    heading_path=ca_hue_hpath,
    evidence_specs=[
        {'role': 'table_header', 'start': 10760, 'end': 10900},
        {'role': 'row_khach_vn', 'start': 10901, 'end': 11158},
        {'role': 'conditions_all', 'start': 11812, 'end': 12287}
    ],
    search_text_builder=lambda lbl, parts: lbl + parts[0]['text'] + '\n' + parts[1]['text'] + '\n\n' + parts[2]['text'],
    description="P3a Chunk 1: Hàng Khách VN + Header + ĐẦY ĐỦ Bao gồm & Không bao gồm; vượt MiniLM long (517 > 512)."
))

chunks.append(build_chunk(
    chunk_id="ca_hue_p3a_chunk_2",
    sample_group="ca_hue",
    proposal_type="supplementary_p3a",
    rel_path=ca_hue_path,
    title=ca_hue_title,
    heading_path=ca_hue_hpath,
    evidence_specs=[
        {'role': 'table_header', 'start': 10760, 'end': 10900},
        {'role': 'row_khach_qt', 'start': 11159, 'end': 11317},
        {'role': 'conditions_all', 'start': 11812, 'end': 12287}
    ],
    search_text_builder=lambda lbl, parts: lbl + parts[0]['text'] + '\n' + parts[1]['text'] + '\n\n' + parts[2]['text'],
    description="P3a Chunk 2: Hàng Khách QT + Header + ĐẦY ĐỦ Bao gồm & Không bao gồm; PASS các model do hàng QT ngắn."
))

chunks.append(build_chunk(
    chunk_id="ca_hue_p3a_chunk_3",
    sample_group="ca_hue",
    proposal_type="supplementary_p3a",
    rel_path=ca_hue_path,
    title=ca_hue_title,
    heading_path=ca_hue_hpath,
    evidence_specs=[
        {'role': 'table_header', 'start': 10760, 'end': 10900},
        {'role': 'child_row_la_que', 'start': 11318, 'end': 11581},
        {'role': 'conditions_all', 'start': 11812, 'end': 12287}
    ],
    search_text_builder=lambda lbl, parts: lbl + parts[0]['text'] + '\n' + parts[1]['text'] + '\n\n' + parts[2]['text'],
    description="P3a Chunk 3: Trẻ em Lá Quê (chiều cao) + Header + ĐẦY ĐỦ Bao gồm & Không bao gồm; vượt HuyDang (267 > 256) và MiniLM long (534 > 512)."
))

chunks.append(build_chunk(
    chunk_id="ca_hue_p3a_chunk_4",
    sample_group="ca_hue",
    proposal_type="supplementary_p3a",
    rel_path=ca_hue_path,
    title=ca_hue_title,
    heading_path=ca_hue_hpath,
    evidence_specs=[
        {'role': 'table_header', 'start': 10760, 'end': 10900},
        {'role': 'child_row_thuyen_rong', 'start': 11582, 'end': 11810},
        {'role': 'conditions_all', 'start': 11812, 'end': 12287}
    ],
    search_text_builder=lambda lbl, parts: lbl + parts[0]['text'] + '\n' + parts[1]['text'] + '\n\n' + parts[2]['text'],
    description="P3a Chunk 4: Trẻ em Thuyền Rồng (độ tuổi) + Header + ĐẦY ĐỦ Bao gồm & Không bao gồm; vượt HuyDang (264 > 256) và MiniLM long (514 > 512)."
))

chunks.append(build_chunk(
    chunk_id="ca_hue_p3a_chunk_5",
    sample_group="ca_hue",
    proposal_type="supplementary_p3a",
    rel_path=ca_hue_path,
    title=ca_hue_title,
    heading_path=ca_hue_hpath,
    evidence_specs=[
        {'role': 'intro_tour_format', 'start': 10643, 'end': 10758}
    ],
    search_text_builder=lambda lbl, parts: lbl + parts[0]['text'],
    description="P3a Chunk 5: Chỉ giữ đoạn dẫn hình thức tour ghép thuyền rồng đôi (sức chứa 25-35 khách)."
))

# Biến thể 3B: Nhóm hàng có nghĩa + Lặp điều kiện loại trừ tối cần thiết 'Không bao gồm' (170 chars), tách 'Bao gồm' chi tiết vào dịch vụ
chunks.append(build_chunk(
    chunk_id="ca_hue_p3b_chunk_1",
    sample_group="ca_hue",
    proposal_type="supplementary_p3b",
    rel_path=ca_hue_path,
    title=ca_hue_title,
    heading_path=ca_hue_hpath,
    evidence_specs=[
        {'role': 'table_header', 'start': 10760, 'end': 10900},
        {'role': 'adult_rows', 'start': 10901, 'end': 11317},
        {'role': 'condition_exclusions', 'start': 12117, 'end': 12287}
    ],
    search_text_builder=lambda lbl, parts: lbl + parts[0]['text'] + '\n' + parts[1]['text'] + '\n\n' + parts[2]['text'],
    description="P3b Chunk 1: Vé người lớn (VN+QT) + Header + Điều kiện loại trừ 'Không bao gồm' (không đưa đón, ăn uống cá nhân, tip); HuyDang 224 tokens (PASS)."
))

chunks.append(build_chunk(
    chunk_id="ca_hue_p3b_chunk_2",
    sample_group="ca_hue",
    proposal_type="supplementary_p3b",
    rel_path=ca_hue_path,
    title=ca_hue_title,
    heading_path=ca_hue_hpath,
    evidence_specs=[
        {'role': 'table_header', 'start': 10760, 'end': 10900},
        {'role': 'child_row_la_que', 'start': 11318, 'end': 11581},
        {'role': 'condition_exclusions', 'start': 12117, 'end': 12287}
    ],
    search_text_builder=lambda lbl, parts: lbl + parts[0]['text'] + '\n' + parts[1]['text'] + '\n\n' + parts[2]['text'],
    description="P3b Chunk 2: Trẻ em Lá Quê Travel (chiều cao) + Header + Điều kiện loại trừ 'Không bao gồm'; HuyDang 208 tokens (PASS)."
))

chunks.append(build_chunk(
    chunk_id="ca_hue_p3b_chunk_3",
    sample_group="ca_hue",
    proposal_type="supplementary_p3b",
    rel_path=ca_hue_path,
    title=ca_hue_title,
    heading_path=ca_hue_hpath,
    evidence_specs=[
        {'role': 'table_header', 'start': 10760, 'end': 10900},
        {'role': 'child_row_thuyen_rong', 'start': 11582, 'end': 11810},
        {'role': 'condition_exclusions', 'start': 12117, 'end': 12287}
    ],
    search_text_builder=lambda lbl, parts: lbl + parts[0]['text'] + '\n' + parts[1]['text'] + '\n\n' + parts[2]['text'],
    description="P3b Chunk 3: Trẻ em Thuyền Rồng Huế (độ tuổi) + Header + Điều kiện loại trừ 'Không bao gồm'; HuyDang 205 tokens (PASS)."
))

chunks.append(build_chunk(
    chunk_id="ca_hue_p3b_chunk_4",
    sample_group="ca_hue",
    proposal_type="supplementary_p3b",
    rel_path=ca_hue_path,
    title=ca_hue_title,
    heading_path=ca_hue_hpath,
    evidence_specs=[
        {'role': 'intro_tour_format', 'start': 10643, 'end': 10758},
        {'role': 'condition_inclusions', 'start': 11812, 'end': 12116}
    ],
    search_text_builder=lambda lbl, parts: lbl + parts[0]['text'] + '\n\n' + parts[1]['text'],
    description="P3b Chunk 4: Dịch vụ bổ sung: Đoạn dẫn tour ghép + Điều kiện 'Bao gồm' chi tiết (50 phút, trang phục áo dài, ngắm cầu, hoa đăng giấy); HuyDang 125 tokens (PASS)."
))

# ------------------------------------------------------------------------------
# 3.4 BIẾN THỂ 3B BỔ SUNG (LƯỢT 3): BỔ SUNG CÂU DẪN KHẢO SÁT MỤC 2.3 THEO REVIEWER
# Câu dẫn: "Dưới đây là mức giá khảo sát thực tế từ các đơn vị cung cấp dịch vụ tiêu biểu (Thuyền Rồng Huế, Ca Huế Trên Sông Hương - Lá Quê Travel, Đại Việt Tourist) tại thời điểm tháng 09/2026:"
# Span: [10409, 10591) (182 ký tự). Xác định 3 đơn vị khảo sát và mốc thời gian 09/2026.
# ------------------------------------------------------------------------------

# Thử nghiệm 1: Gộp người lớn VN + QT + Header + Câu dẫn 2.3 + Không bao gồm
chunks.append(build_chunk(
    chunk_id="ca_hue_p3b_lead_chunk_1_merged",
    sample_group="ca_hue",
    proposal_type="supplementary_p3b_lead",
    rel_path=ca_hue_path,
    title=ca_hue_title,
    heading_path=ca_hue_hpath,
    evidence_specs=[
        {'role': 'survey_lead_2_3', 'start': 10409, 'end': 10591},
        {'role': 'table_header', 'start': 10760, 'end': 10900},
        {'role': 'adult_rows', 'start': 10901, 'end': 11317},
        {'role': 'condition_exclusions', 'start': 12117, 'end': 12287}
    ],
    search_text_builder=lambda lbl, parts: lbl + parts[0]['text'] + '\n\n' + parts[1]['text'] + '\n' + parts[2]['text'] + '\n\n' + parts[3]['text'],
    description="P3b Lượt 3 (Thử nghiệm gộp VN+QT + Câu dẫn 2.3 + Không bao gồm): VƯỢT HuyDang (264 > 256) và MiniLM long (527 > 512)."
))

# Tách riêng 1a: Khách VN riêng + Header + Câu dẫn 2.3 + Không bao gồm
chunks.append(build_chunk(
    chunk_id="ca_hue_p3b_lead_chunk_1a",
    sample_group="ca_hue",
    proposal_type="supplementary_p3b_lead",
    rel_path=ca_hue_path,
    title=ca_hue_title,
    heading_path=ca_hue_hpath,
    evidence_specs=[
        {'role': 'survey_lead_2_3', 'start': 10409, 'end': 10591},
        {'role': 'table_header', 'start': 10760, 'end': 10900},
        {'role': 'row_khach_vn', 'start': 10901, 'end': 11158},
        {'role': 'condition_exclusions', 'start': 12117, 'end': 12287}
    ],
    search_text_builder=lambda lbl, parts: lbl + parts[0]['text'] + '\n\n' + parts[1]['text'] + '\n' + parts[2]['text'] + '\n\n' + parts[3]['text'],
    description="P3b Lượt 3 Chunk 1a: Tách riêng Khách VN + Header + Câu dẫn 2.3 + Không bao gồm; HuyDang 230 tokens, MiniLM long 462 tokens (PASS ALL)."
))

# Tách riêng 1b: Khách QT riêng + Header + Câu dẫn 2.3 + Không bao gồm
chunks.append(build_chunk(
    chunk_id="ca_hue_p3b_lead_chunk_1b",
    sample_group="ca_hue",
    proposal_type="supplementary_p3b_lead",
    rel_path=ca_hue_path,
    title=ca_hue_title,
    heading_path=ca_hue_hpath,
    evidence_specs=[
        {'role': 'survey_lead_2_3', 'start': 10409, 'end': 10591},
        {'role': 'table_header', 'start': 10760, 'end': 10900},
        {'role': 'row_khach_qt', 'start': 11159, 'end': 11317},
        {'role': 'condition_exclusions', 'start': 12117, 'end': 12287}
    ],
    search_text_builder=lambda lbl, parts: lbl + parts[0]['text'] + '\n\n' + parts[1]['text'] + '\n' + parts[2]['text'] + '\n\n' + parts[3]['text'],
    description="P3b Lượt 3 Chunk 1b: Tách riêng Khách QT + Header + Câu dẫn 2.3 + Không bao gồm; HuyDang 203 tokens, MiniLM long 418 tokens (PASS ALL)."
))

# Chunk 2: Trẻ em Lá Quê Travel (chiều cao) + Header + Câu dẫn 2.3 + Không bao gồm
chunks.append(build_chunk(
    chunk_id="ca_hue_p3b_lead_chunk_2",
    sample_group="ca_hue",
    proposal_type="supplementary_p3b_lead",
    rel_path=ca_hue_path,
    title=ca_hue_title,
    heading_path=ca_hue_hpath,
    evidence_specs=[
        {'role': 'survey_lead_2_3', 'start': 10409, 'end': 10591},
        {'role': 'table_header', 'start': 10760, 'end': 10900},
        {'role': 'child_row_la_que', 'start': 11318, 'end': 11581},
        {'role': 'condition_exclusions', 'start': 12117, 'end': 12287}
    ],
    search_text_builder=lambda lbl, parts: lbl + parts[0]['text'] + '\n\n' + parts[1]['text'] + '\n' + parts[2]['text'] + '\n\n' + parts[3]['text'],
    description="P3b Lượt 3 Chunk 2: Trẻ em Lá Quê Travel (chiều cao) + Header + Câu dẫn 2.3 + Không bao gồm; HuyDang 248 tokens (sát trần 96.9%), MiniLM long 479 tokens (PASS ALL)."
))

# Chunk 3: Trẻ em Thuyền Rồng Huế (độ tuổi) + Header + Câu dẫn 2.3 + Không bao gồm
chunks.append(build_chunk(
    chunk_id="ca_hue_p3b_lead_chunk_3",
    sample_group="ca_hue",
    proposal_type="supplementary_p3b_lead",
    rel_path=ca_hue_path,
    title=ca_hue_title,
    heading_path=ca_hue_hpath,
    evidence_specs=[
        {'role': 'survey_lead_2_3', 'start': 10409, 'end': 10591},
        {'role': 'table_header', 'start': 10760, 'end': 10900},
        {'role': 'child_row_thuyen_rong', 'start': 11582, 'end': 11810},
        {'role': 'condition_exclusions', 'start': 12117, 'end': 12287}
    ],
    search_text_builder=lambda lbl, parts: lbl + parts[0]['text'] + '\n\n' + parts[1]['text'] + '\n' + parts[2]['text'] + '\n\n' + parts[3]['text'],
    description="P3b Lượt 3 Chunk 3: Trẻ em Thuyền Rồng Huế (độ tuổi) + Header + Câu dẫn 2.3 + Không bao gồm; HuyDang 245 tokens (sát trần 95.7%), MiniLM long 459 tokens (PASS ALL)."
))

# Chunk 4: Dịch vụ bổ sung (không mang theo câu dẫn 2.3 vì không chứa dữ liệu giá khảo sát)
chunks.append(build_chunk(
    chunk_id="ca_hue_p3b_lead_chunk_4_service",
    sample_group="ca_hue",
    proposal_type="supplementary_p3b_lead",
    rel_path=ca_hue_path,
    title=ca_hue_title,
    heading_path=ca_hue_hpath,
    evidence_specs=[
        {'role': 'intro_tour_format', 'start': 10643, 'end': 10758},
        {'role': 'condition_inclusions', 'start': 11812, 'end': 12116}
    ],
    search_text_builder=lambda lbl, parts: lbl + parts[0]['text'] + '\n\n' + parts[1]['text'],
    description="P3b Lượt 3 Chunk 4 (Dịch vụ riêng, không mang theo câu dẫn 2.3): Tour ghép + Bao gồm chi tiết; HuyDang 125 tokens, MiniLM long 316 tokens (PASS ALL)."
))

# Chunk 4 (Biến thể thử nghiệm mang theo câu dẫn 2.3 để đối chiếu):
chunks.append(build_chunk(
    chunk_id="ca_hue_p3b_lead_chunk_4_service_with_lead",
    sample_group="ca_hue",
    proposal_type="supplementary_p3b_lead",
    rel_path=ca_hue_path,
    title=ca_hue_title,
    heading_path=ca_hue_hpath,
    evidence_specs=[
        {'role': 'survey_lead_2_3', 'start': 10409, 'end': 10591},
        {'role': 'intro_tour_format', 'start': 10643, 'end': 10758},
        {'role': 'condition_inclusions', 'start': 11812, 'end': 12116}
    ],
    search_text_builder=lambda lbl, parts: lbl + parts[0]['text'] + '\n\n' + parts[1]['text'] + '\n\n' + parts[2]['text'],
    description="P3b Lượt 3 Chunk 4 (Biến thể thử nghiệm: mang theo câu dẫn 2.3 vào dịch vụ): HuyDang 165 tokens, MiniLM long 385 tokens (PASS ALL)."
))

# ------------------------------------------------------------------------------
# 4. CÁC MẪU ĐỐI CHỨNG MỤC NGẮN (giữ nguyên khối nếu vừa)
# ------------------------------------------------------------------------------
me_keo_path = 'foods/restaurants/quan bun bo me keo.md'
chunks.append(build_chunk(
    chunk_id="control_me_keo_info",
    sample_group="control_me_keo",
    proposal_type="control_intact",
    rel_path=me_keo_path,
    title="Quán bún bò Mệ Kéo",
    heading_path=["Thông tin"],
    evidence_specs=[
        {'role': 'body', 'start': 516, 'end': 790}
    ],
    search_text_builder=lambda lbl, parts: lbl + parts[0]['text'],
    description="Đối chứng mục ngắn Foods: Địa chỉ, mức giá, giờ hoạt động và lưu ý 'thường hết sớm hơn'."
))

sea_module_path = 'travel/services/Lịch trình du lịch Huế 3 ngày 2 đêm.md'
chunks.append(build_chunk(
    chunk_id="control_sea_module",
    sample_group="control_sea_module",
    proposal_type="control_intact",
    rel_path=sea_module_path,
    title="Lịch trình du lịch Huế 3 ngày 2 đêm",
    heading_path=["Module thay thế: Biển và đầm phá"],
    evidence_specs=[
        {'role': 'body', 'start': 3182, 'end': 3811}
    ],
    search_text_builder=lambda lbl, parts: lbl + parts[0]['text'],
    description="Đối chứng mục cẩm nang có cấu trúc H3 lồng và điều kiện áp dụng: Phạm vi thay thế, cách chọn và điều kiện thời tiết."
))

# ==============================================================================
# KIỂM TRA ĐỘ BAO PHỦ (COVERAGE AUDIT)
# ==============================================================================

coverage_audit = {
    'gia_lac': {
        'source_file': gia_lac_path,
        'target_section': '## Thông tin chung',
        'target_span': [40, 1211],
        'total_target_characters': 1171,
        'content_coverage_status': 'complete_excluding_whitespace_gaps',
        'preferred_p1_coverage': {
            'chunks': ['gia_lac_p1_chunk_1', 'gia_lac_p1_chunk_2'],
            'covered_spans': [[40, 590], [591, 1211]],
            'covered_content_characters': 550 + 620,
            'whitespace_gaps': [
                {'span': [590, 591], 'char': '\\n', 'count': 1, 'explanation': 'Ký tự xuống dòng giữa bullet thời gian và bullet nơi tổ chức'}
            ],
            'repeated_parts': [],
            'extra_parts': [],
            'character_accounting': '550 (chunk 1) + 1 (gap \\n) + 620 (chunk 2) = 1171 / 1171 ký tự'
        }
    },
    'ngo_mon': {
        'source_file': ngo_mon_path,
        'target_section': '### Ngọ Môn (thuộc ## Các công trình kiến trúc hạt nhân của Hoàng thành)',
        'target_span': [10219, 11945],
        'total_target_characters': 1726,
        'content_coverage_status': 'complete_excluding_whitespace_gaps',
        'preferred_p1_coverage': {
            'chunks': ['ngo_mon_p1_chunk_1', 'ngo_mon_p1_chunk_2'],
            'covered_spans': [[10219, 11068], [11069, 11945]],
            'covered_content_characters': 849 + 876,
            'whitespace_gaps': [
                {'span': [11068, 11069], 'char': '\\n', 'count': 1, 'explanation': 'Ký tự xuống dòng giữa bullet đài nền và bullet Lầu Ngũ Phụng'}
            ],
            'repeated_parts': [],
            'extra_parts': [],
            'character_accounting': '849 (chunk 1) + 1 (gap \\n) + 876 (chunk 2) = 1726 / 1726 ký tự'
        }
    },
    'ca_hue': {
        'source_file': ca_hue_path,
        'target_section': '### 2.3. Chi tiết bảng giá khảo sát dịch vụ Ca Huế -> #### A. Vé khách lẻ ghép thuyền (Tour ghép đoàn)',
        'target_span': [10409, 12287],
        'total_target_characters': 1878,
        'content_coverage_status': 'complete_excluding_whitespace_gaps_and_heading_A',
        'preferred_p1_coverage': {
            'scope': 'Chỉ tính riêng tiểu mục A (chưa gồm câu dẫn 2.3)',
            'target_span': [10643, 12287],
            'total_target_characters': 1644,
            'chunks': ['ca_hue_p1_chunk_1', 'ca_hue_p1_chunk_2', 'ca_hue_p1_chunk_3'],
            'covered_spans': [
                {'chunk': 'ca_hue_p1_chunk_1', 'spans': [[10760, 10900], [10901, 11317]]},
                {'chunk': 'ca_hue_p1_chunk_2', 'spans': [[10760, 10900], [11318, 11810]]},
                {'chunk': 'ca_hue_p1_chunk_3', 'spans': [[10643, 10758], [11812, 12287]]}
            ],
            'covered_content_characters': 140 + 416 + 492 + 115 + 475,
            'whitespace_gaps': [
                {'span': [10758, 10760], 'chars': '\\n\\n', 'count': 2, 'explanation': 'Dòng trống giữa đoạn dẫn tour ghép và bảng giá'},
                {'span': [10900, 10901], 'chars': '\\n', 'count': 1, 'explanation': 'Dấu xuống dòng giữa header bảng và hàng dữ liệu đầu tiên'},
                {'span': [11317, 11318], 'chars': '\\n', 'count': 1, 'explanation': 'Dấu xuống dòng giữa hàng vé người lớn và hàng vé trẻ em'},
                {'span': [11810, 11812], 'chars': '\\n\\n', 'count': 2, 'explanation': 'Dòng trống giữa bảng giá và khối điều kiện Bao gồm'}
            ],
            'repeated_parts': [
                {
                    'role': 'table_header',
                    'span': [10760, 10900],
                    'characters': 140,
                    'explanation': 'Tiêu đề cột bảng lặp lại ở Chunk 1 và Chunk 2 (ở P2/P3 lặp thêm ở các hàng con).'
                }
            ],
            'extra_parts': [
                {
                    'role': 'intro_and_conditions',
                    'spans': [[10643, 10758], [11812, 12287]],
                    'characters': 115 + 475,
                    'explanation': 'Đoạn dẫn tour ghép và khối điều kiện Bao gồm/Không bao gồm ngoài bảng giá.'
                }
            ],
            'character_accounting': '115 (intro) + 2 (gap) + 140 (header) + 1 (gap) + 416 (adults) + 1 (gap) + 492 (children) + 2 (gap) + 475 (cond) = 1644 / 1644 ký tự'
        },
        'updated_p3b_coverage': {
            'scope': 'Toàn bộ khối khảo sát giá mục 2.3 gồm câu dẫn thời điểm 09/2026 và tiểu mục A',
            'target_span': [10409, 12287],
            'total_target_characters': 1878,
            'chunks': [
                'ca_hue_p3b_lead_chunk_1a',
                'ca_hue_p3b_lead_chunk_1b',
                'ca_hue_p3b_lead_chunk_2',
                'ca_hue_p3b_lead_chunk_3',
                'ca_hue_p3b_lead_chunk_4_service'
            ],
            'covered_spans': [
                {'role': 'survey_lead_2_3', 'span': [10409, 10591], 'chars': 182},
                {'role': 'table_header', 'span': [10760, 10900], 'chars': 140},
                {'role': 'row_khach_vn', 'span': [10901, 11158], 'chars': 257},
                {'role': 'row_khach_qt', 'span': [11159, 11317], 'chars': 158},
                {'role': 'child_row_la_que', 'span': [11318, 11581], 'chars': 263},
                {'role': 'child_row_thuyen_rong', 'span': [11582, 11810], 'chars': 228},
                {'role': 'intro_tour_format', 'span': [10643, 10758], 'chars': 115},
                {'role': 'condition_inclusions', 'span': [11812, 12116], 'chars': 304},
                {'role': 'condition_exclusions', 'span': [12117, 12287], 'chars': 170}
            ],
            'covered_content_characters': 1817,
            'heading_metadata_span': {
                'role': 'heading_A',
                'span': [10593, 10641],
                'chars': 48,
                'explanation': 'Được bảo toàn nguyên vẹn trong metadata heading_path và label của tất cả chunk.'
            },
            'whitespace_gaps': [
                {'span': [10591, 10593], 'chars': '\\n\\n', 'count': 2, 'explanation': 'Dòng trống giữa câu dẫn 2.3 và heading A'},
                {'span': [10641, 10643], 'chars': '\\n\\n', 'count': 2, 'explanation': 'Dòng trống giữa heading A và đoạn dẫn tour ghép'},
                {'span': [10758, 10760], 'chars': '\\n\\n', 'count': 2, 'explanation': 'Dòng trống giữa đoạn dẫn tour ghép và bảng giá'},
                {'span': [10900, 10901], 'chars': '\\n', 'count': 1, 'explanation': 'Dấu xuống dòng sau header bảng'},
                {'span': [11158, 11159], 'chars': '\\n', 'count': 1, 'explanation': 'Dấu xuống dòng giữa hàng VN và hàng QT'},
                {'span': [11317, 11318], 'chars': '\\n', 'count': 1, 'explanation': 'Dấu xuống dòng giữa hàng QT và hàng Trẻ em Lá Quê'},
                {'span': [11581, 11582], 'chars': '\\n', 'count': 1, 'explanation': 'Dấu xuống dòng giữa hàng Trẻ em Lá Quê và hàng Trẻ em Thuyền Rồng'},
                {'span': [11810, 11812], 'chars': '\\n\\n', 'count': 2, 'explanation': 'Dòng trống sau bảng giá'},
                {'span': [12116, 12117], 'chars': '\\n', 'count': 1, 'explanation': 'Dấu xuống dòng giữa điều kiện Bao gồm và Không bao gồm'}
            ],
            'repeated_parts': [
                {'role': 'survey_lead_2_3', 'span': [10409, 10591], 'chars': 182, 'repeat_count': 4, 'explanation': 'Lặp ở 4 chunk giá vé (1a, 1b, 2, 3) để xác định mốc thời gian 09/2026 và 3 đơn vị khảo sát.'},
                {'role': 'table_header', 'span': [10760, 10900], 'chars': 140, 'repeat_count': 4, 'explanation': 'Lặp ở 4 chunk giá vé để giữ cấu trúc cột bảng.'},
                {'role': 'condition_exclusions', 'span': [12117, 12287], 'chars': 170, 'repeat_count': 4, 'explanation': 'Lặp ở 4 chunk giá vé để bảo đảm điều kiện loại trừ tối cần thiết.'}
            ],
            'service_chunk_lead_analysis': {
                'included_in_service_chunk': False,
                'explanation': 'Chunk dịch vụ (ca_hue_p3b_lead_chunk_4_service) không chứa mức giá khảo sát nào, chỉ chứa quy cách dịch vụ chung (thuyền rồng đôi 25-35 khách, thời lượng tối thiểu 50 phút theo quy chuẩn nhà nước, dàn nghệ sĩ áo dài, thả hoa đăng giấy). Câu dẫn 2.3 xác định mức giá khảo sát thời điểm 09/2026 không cần thiết cho dịch vụ và có thể gây nhiễu ngữ nghĩa (semantic noise). Biến thể có câu dẫn (ca_hue_p3b_lead_chunk_4_service_with_lead) vẫn PASS tokenizer (165 tokens HuyDang).'
            },
            'character_accounting': '182 (lead) + 2 (gap) + 48 (heading A) + 2 (gap) + 115 (intro) + 2 (gap) + 140 (header) + 1 (gap) + 257 (VN) + 1 (gap) + 158 (QT) + 1 (gap) + 263 (child Lá Quê) + 1 (gap) + 228 (child Thuyền Rồng) + 2 (gap) + 304 (bao gồm) + 1 (gap) + 170 (không bao gồm) = 1878 / 1878 ký tự'
        }
    },
    'control_me_keo': {
        'source_file': me_keo_path,
        'target_span': [516, 790],
        'total_target_characters': 274,
        'content_coverage_status': 'exact_character_coverage_100'
    },
    'control_sea_module': {
        'source_file': sea_module_path,
        'target_span': [3182, 3811],
        'total_target_characters': 629,
        'content_coverage_status': 'exact_character_coverage_100'
    }
}

# ==============================================================================
# XUẤT ARTIFACT VÀ IN BẢNG BÁO CÁO
# ==============================================================================

out_payload = {
    'metadata': {
        'timestamp': '2026-09-09T16:30:00+07:00',
        'title': 'Khảo sát độ dài tokenizer thực tế cho các mẫu chunking toàn corpus Huế (Cập nhật 3)',
        'scope': 'Khảo sát text/tokenizer có mục tiêu; không chạy inference embedding/reranker, không gọi Qdrant/API',
        'models': MODELS,
        'limits': LIMITS,
        'queries': QUERIES,
        'normalization': 'UTF-8 decoded; CRLF/CR -> LF; Unicode code points zero-based, end exclusive; no Unicode normalization'
    },
    'chunks': chunks,
    'coverage_audit': coverage_audit
}

OUT_JSON.write_text(json.dumps(out_payload, ensure_ascii=False, indent=2), encoding='utf-8')
print(f"\n Đã lưu thành công artifact JSON tại: {OUT_JSON}")

# In bảng Markdown kết quả đo
print("\n" + "="*120)
print(f"{'Chunk ID':<35} | {'Chars':<5} | {'E5-sm':<5} | {'E5-bs':<5} | {'HuyDang':<7} | {'MLM-orig':<8} | {'MLM-long':<8} | {'Status'}")
print("-" * 120)
for c in chunks:
    tok = c['tokens']
    status_str = " PASS" if c['status'] == 'PASS_ALL' else f"❌ {c['status']}"
    print(f"{c['chunk_id']:<35} | {c['search_text_characters']:<5} | {tok['e5_small']:<5} | {tok['e5_base']:<5} | {tok['huydang']:<7} | {tok['minilm_orig']:<8} | {tok['minilm_long']:<8} | {status_str}")
print("="*120)

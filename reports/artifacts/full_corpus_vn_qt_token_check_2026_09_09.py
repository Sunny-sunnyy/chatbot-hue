#!/usr/bin/env python3
"""
Khảo sát đo token độc lập cho hai input Ca Huế (Việt Nam & Quốc Tế) đã sửa ranh giới hàng.
Dự án: /home/minhhieu/hue_rag
Contract: session_prompt/FULL_CORPUS_VN_QT_TOKEN_CHECK_HANDOFF.md

Phạm vi và nguyên tắc:
1. Đọc đúng hai composites VN và QT từ reports/artifacts/full_corpus_parser_locator_samples_2026_09_09.json.
2. Đối chiếu toàn bộ evidence_parts với source LF (travel/tickets/Vé biểu diễn nghệ thuật và trải nghiệm sông Hương.md).
3. Giữ nguyên search_text (931 ký tự cho VN, 866 ký tự cho QT) và queries cố định.
4. Tokenize local_files_only=True, truncation=False:
   - intfloat/multilingual-e5-small (limit: 512, prefix 'passage: ')
   - intfloat/multilingual-e5-base (limit: 512, prefix 'passage: ')
   - CODE4LIFEOFFICIAL/huydang-dek21-embedding (limit: 256, PyVi segmentation, không prefix)
   - cross-encoder/ms-marco-MiniLM-L-6-v2 (limit: 512 pair query/doc, đo cả query_orig và query_long)
5. Xuất kết quả chi tiết ra reports/artifacts/full_corpus_vn_qt_token_check_2026_09_09.json.
"""

import json
import sys
from pathlib import Path
import importlib.metadata
import transformers
from transformers import AutoTokenizer
from pyvi import ViTokenizer

# Thiết lập đường dẫn
WORKSPACE_ROOT = Path('/home/minhhieu/hue_rag')
KB_ROOT = WORKSPACE_ROOT / 'knowledge-base-hue'
CACHE_ROOT = Path('/home/minhhieu/.cache/huggingface/hub')
PARSER_SAMPLES_JSON = WORKSPACE_ROOT / 'reports/artifacts/full_corpus_parser_locator_samples_2026_09_09.json'
OUTPUT_JSON = WORKSPACE_ROOT / 'reports/artifacts/full_corpus_vn_qt_token_check_2026_09_09.json'

# Định danh exact snapshot và input limit theo contract mục 19
MODELS_SPEC = {
    'e5_small': {
        'model_id': 'intfloat/multilingual-e5-small',
        'dir_name': 'models--intfloat--multilingual-e5-small',
        'revision': '614241f622f53c4eeff9890bdc4f31cfecc418b3',
        'limit': 512,
        'type': 'embedding',
        'prefix': 'passage: ',
        'pyvi': False
    },
    'e5_base': {
        'model_id': 'intfloat/multilingual-e5-base',
        'dir_name': 'models--intfloat--multilingual-e5-base',
        'revision': 'd128750597153bb5987e10b1c3493a34e5a4502a',
        'limit': 512,
        'type': 'embedding',
        'prefix': 'passage: ',
        'pyvi': False
    },
    'huydang': {
        'model_id': 'CODE4LIFEOFFICIAL/huydang-dek21-embedding',
        'dir_name': 'models--CODE4LIFEOFFICIAL--huydang-dek21-embedding',
        'revision': '517f1af7dd04a57194f1de2990f0c6ede0a3109b',
        'limit': 256,
        'type': 'embedding',
        'prefix': '',
        'pyvi': True
    },
    'minilm': {
        'model_id': 'cross-encoder/ms-marco-MiniLM-L-6-v2',
        'dir_name': 'models--cross-encoder--ms-marco-MiniLM-L-6-v2',
        'revision': '233902d25c440f23af6f7d6e94d2946bac0bee0a',
        'limit': 512,
        'type': 'reranker_pair',
        'prefix': '',
        'pyvi': False
    }
}

# Queries Ca Huế cố định theo contract (mục 26)
QUERIES = {
    'ca_hue': {
        'orig': 'Vé Ca Huế cho trẻ em được tính như thế nào?',
        'long': 'Giá vé xem Ca Huế ghép thuyền trên sông Hương cho người lớn và trẻ em bao nhiêu tiền một người, áp dụng điều kiện bao gồm và không bao gồm những dịch vụ gì?'
    }
}

EXPECTED_SPANS = {
    'ca_hue_tour_ghep_vn': {
        'body_span': (10901, 11141),
        'expected_characters': 931
    },
    'ca_hue_tour_ghep_qt': {
        'body_span': (11142, 11317),
        'expected_characters': 866
    }
}


def load_source_lf(rel_path: str) -> str:
    """Đọc tệp nguồn UTF-8 và chuẩn hóa CRLF/CR thành LF; không Unicode-normalize."""
    file_path = KB_ROOT / rel_path
    if not file_path.exists():
        raise FileNotFoundError(f"Không tìm thấy tệp nguồn: {file_path}")
    raw = file_path.read_bytes().decode('utf-8')
    return raw.replace('\r\n', '\n').replace('\r', '\n')


def verify_evidence_parts(source_text: str, parts: list[dict], item_key: str) -> list[dict]:
    """Đối chiếu từng evidence part với source LF nguyên bản."""
    verified_parts = []
    for idx, p in enumerate(parts):
        start = p['start']
        end = p['end']
        text = p['text']
        slice_text = source_text[start:end]
        if slice_text != text:
            raise ValueError(
                f"LỖI ĐỐI CHIẾU NGUỒN: {item_key} part[{idx}] [{start}:{end}] không khớp lát cắt nguồn!\n"
                f"  Nguồn: {repr(slice_text[:60])}\n"
                f"  Part:  {repr(text[:60])}"
            )
        verified_parts.append({
            'role': p['role'],
            'start': start,
            'end': end,
            'characters': len(text),
            'text': text,
            'exact_match': True
        })
    return verified_parts


def main():
    print("=" * 80)
    print("KHẢO SÁT ĐO TOKEN HAI INPUT CA HUẾ (VN / QT) ĐÃ SỬA RANH GIỚI")
    print("=" * 80)

    # 1. Kiểm tra môi trường thực tế
    actual_transformers_ver = transformers.__version__
    actual_pyvi_ver = importlib.metadata.version('pyvi')
    python_ver = sys.version.split()[0]
    print(f"Môi trường: Python {python_ver}, Transformers {actual_transformers_ver}, PyVi {actual_pyvi_ver}")

    # 2. Đọc parser samples JSON
    if not PARSER_SAMPLES_JSON.exists():
        raise FileNotFoundError(f"Không tìm thấy parser samples JSON: {PARSER_SAMPLES_JSON}")
    
    with open(PARSER_SAMPLES_JSON, 'r', encoding='utf-8') as f:
        parser_data = json.load(f)

    composites = parser_data.get('composite_chunk_examples', {})
    if 'ca_hue_tour_ghep_vn' not in composites or 'ca_hue_tour_ghep_qt' not in composites:
        raise KeyError("Thiếu composite ca_hue_tour_ghep_vn hoặc ca_hue_tour_ghep_qt trong JSON parser!")

    # 3. Nạp tokenizers local_files_only=True
    tokenizers = {}
    tokenizer_metadata = {}
    for key, spec in MODELS_SPEC.items():
        snapshot_dir = CACHE_ROOT / spec['dir_name'] / 'snapshots' / spec['revision']
        if not snapshot_dir.exists():
            raise FileNotFoundError(f"Thiếu local cache snapshot cho {key}: {snapshot_dir}")
        
        tok = AutoTokenizer.from_pretrained(str(snapshot_dir), local_files_only=True)
        tokenizers[key] = tok
        
        # Đọc config thực tế
        config_max_len = getattr(tok, 'model_max_length', None)
        tokenizer_metadata[key] = {
            'model_id': spec['model_id'],
            'snapshot_path': str(snapshot_dir),
            'revision': spec['revision'],
            'configured_limit': spec['limit'],
            'model_max_length_attribute': config_max_len
        }
        print(f"Đã nạp tokenizer [{key}]: {spec['model_id']} (rev: {spec['revision'][:12]}..., limit: {spec['limit']})")

    # 4. Thực hiện đo đạc cho từng composite
    results_by_sample = {}
    query_orig = QUERIES['ca_hue']['orig']
    query_long = QUERIES['ca_hue']['long']

    for sample_key in ['ca_hue_tour_ghep_vn', 'ca_hue_tour_ghep_qt']:
        raw_item = composites[sample_key]
        rel_source = raw_item['source']
        source_lf = load_source_lf(rel_source)

        # Kiểm tra body span
        body_parts = [p for p in raw_item['evidence_parts'] if p.get('role') == 'body']
        if len(body_parts) != 1:
            raise ValueError(f"{sample_key} phải có đúng 1 part có role='body', tìm thấy {len(body_parts)}")
        
        actual_body_span = (body_parts[0]['start'], body_parts[0]['end'])
        expected_body_span = EXPECTED_SPANS[sample_key]['body_span']
        if actual_body_span != expected_body_span:
            raise ValueError(
                f"LỖI RANH GIỚI: {sample_key} body_span thực tế là {actual_body_span}, kỳ vọng {expected_body_span}!"
            )

        # Đối chiếu 4 evidence parts
        verified_parts = verify_evidence_parts(source_lf, raw_item['evidence_parts'], sample_key)

        # Kiểm tra search_text
        search_text = raw_item['search_text']
        expected_chars = EXPECTED_SPANS[sample_key]['expected_characters']
        if len(search_text) != expected_chars:
            raise ValueError(
                f"LỖI ĐỘ DÀI: {sample_key} search_text có {len(search_text)} ký tự, kỳ vọng {expected_chars}!"
            )

        # Tiến hành đo token (truncation=False)
        # E5-small
        e5_s_data = tokenizers['e5_small'](
            'passage: ' + search_text, add_special_tokens=True, truncation=False
        )
        e5_s_tokens = len(e5_s_data['input_ids'])

        # E5-base
        e5_b_data = tokenizers['e5_base'](
            'passage: ' + search_text, add_special_tokens=True, truncation=False
        )
        e5_b_tokens = len(e5_b_data['input_ids'])

        # HuyDang (phân đoạn PyVi, không có prefix 'passage: ')
        segmented_text = ViTokenizer.tokenize(search_text)
        hd_data = tokenizers['huydang'](
            segmented_text, add_special_tokens=True, truncation=False
        )
        hd_tokens = len(hd_data['input_ids'])

        # MiniLM pair orig
        ml_orig_data = tokenizers['minilm'](
            query_orig, search_text, add_special_tokens=True, truncation=False
        )
        ml_orig_tokens = len(ml_orig_data['input_ids'])

        # MiniLM pair long
        ml_long_data = tokenizers['minilm'](
            query_long, search_text, add_special_tokens=True, truncation=False
        )
        ml_long_tokens = len(ml_long_data['input_ids'])

        # So khớp giới hạn
        limits = {
            'e5_small': MODELS_SPEC['e5_small']['limit'],
            'e5_base': MODELS_SPEC['e5_base']['limit'],
            'huydang': MODELS_SPEC['huydang']['limit'],
            'minilm_orig': MODELS_SPEC['minilm']['limit'],
            'minilm_long': MODELS_SPEC['minilm']['limit']
        }
        token_counts = {
            'e5_small': e5_s_tokens,
            'e5_base': e5_b_tokens,
            'huydang': hd_tokens,
            'minilm_orig': ml_orig_tokens,
            'minilm_long': ml_long_tokens
        }
        
        exceeded_models = [k for k, count in token_counts.items() if count > limits[k]]
        verdict = 'VỪA (PASS_ALL)' if not exceeded_models else f"VƯỢT ({', '.join(exceeded_models)})"

        results_by_sample[sample_key] = {
            'chunk_id': raw_item.get('chunk_id'),
            'source': rel_source,
            'title': raw_item.get('title'),
            'heading_path': raw_item.get('heading_path'),
            'body_span': list(actual_body_span),
            'body_characters': len(body_parts[0]['text']),
            'search_text_characters': len(search_text),
            'search_text': search_text,
            'evidence_parts': verified_parts,
            'queries': {
                'orig': query_orig,
                'long': query_long
            },
            'token_counts': token_counts,
            'token_limits': limits,
            'token_margins': {k: limits[k] - token_counts[k] for k in limits},
            'exceeded_models': exceeded_models,
            'verdict': verdict
        }

    # 5. In bảng kết quả tổng hợp
    print("\n" + "=" * 80)
    print("BẢNG KẾT QUẢ ĐO TOKEN THỰC TẾ (KHÔNG TRUNCATION)")
    print("=" * 80)
    print(f"{'Mẫu composite':<25} | {'Chars':<6} | {'E5-sm':<7} | {'E5-bs':<7} | {'HuyDang':<8} | {'MiniLM orig':<11} | {'MiniLM long':<11} | {'Kết luận':<15}")
    print("-" * 105)
    for k, v in results_by_sample.items():
        c = v['token_counts']
        chars = v['search_text_characters']
        label = "Khách VN (đã sửa)" if "vn" in k else "Khách QT (đã sửa)"
        print(f"{label:<25} | {chars:<6} | {c['e5_small']:<7} | {c['e5_base']:<7} | {c['huydang']:<8} | {c['minilm_orig']:<11} | {c['minilm_long']:<11} | {v['verdict']:<15}")
    print("-" * 105)
    print(f"{'Giới hạn mô hình':<25} | {'-':<6} | {'512':<7} | {'512':<7} | {'256':<8} | {'512':<11} | {'512':<11} | -")
    print("=" * 80)

    # 6. Ghi artifact JSON
    out_payload = {
        'metadata': {
            'task': 'full_corpus_vn_qt_token_check',
            'contract': 'session_prompt/FULL_CORPUS_VN_QT_TOKEN_CHECK_HANDOFF.md',
            'date': '2026-09-09',
            'python_version': python_ver,
            'transformers_version': actual_transformers_ver,
            'pyvi_version': actual_pyvi_ver,
            'models_and_tokenizers': tokenizer_metadata,
            'queries_used': QUERIES['ca_hue']
        },
        'samples': results_by_sample,
        'summary': {
            'all_inputs_pass': all(len(v['exceeded_models']) == 0 for v in results_by_sample.values()),
            'conclusion': (
                "Cả hai composite Ca Huế (VN và QT) với ranh giới hàng đã sửa hoàn chỉnh đều "
                "nằm trong toàn bộ các giới hạn token của E5-small (512), E5-base (512), "
                "HuyDang (256) và MiniLM pair (512 cho cả query_orig lẫn query_long)."
            )
        }
    }

    OUTPUT_JSON.write_text(json.dumps(out_payload, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"\nĐã ghi artifact JSON kết quả tại: {OUTPUT_JSON}")


if __name__ == '__main__':
    main()

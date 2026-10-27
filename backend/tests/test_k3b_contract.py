"""Hợp đồng đầu ra K3b (plan `phase_8_2_k3b_plan.md` §2): đúng 10 số hợp lệ ⇒ dùng thứ tự luna; sai ⇒ nguyên top-10 RRF."""
from experiments.phase_8_2.k3b import apply_contract, clopper_pearson

RRF_TOP10 = list(range(1, 11))


def test_valid_order_is_used_as_is():
    order = [12, 3, 30, 1, 7, 25, 9, 18, 2, 14]
    picked, counts = apply_contract(order)
    assert picked == order
    assert counts == {"n_returned": 10, "n_out_of_range": 0, "n_duplicate": 0, "contract_violation": False}


def test_wrong_length_falls_back_to_rrf_top10():
    for order in ([5, 4, 3, 2, 1, 6, 7, 8, 9], list(range(30, 19, -1))):  # 9 số; 11 số
        picked, counts = apply_contract(order)
        assert picked == RRF_TOP10 and counts["contract_violation"] and counts["n_returned"] == len(order)


def test_duplicate_or_out_of_range_falls_back_to_rrf_top10():
    picked, counts = apply_contract([12, 12, 3, 30, 1, 7, 25, 9, 18, 2])
    assert picked == RRF_TOP10 and counts["n_duplicate"] == 1 and counts["contract_violation"]
    picked, counts = apply_contract([31, 0, 3, 30, 1, 7, 25, 9, 18, 2])
    assert picked == RRF_TOP10 and counts["n_out_of_range"] == 2 and counts["contract_violation"]


def test_clopper_pearson_known_values():
    # 1 / 40: CI chính xác 95 % ≈ [0,000633; 0,1316] (cùng số report K3 tính bằng scipy beta)
    low, high = clopper_pearson(1, 40)
    assert abs(low - 0.000633) < 1e-5 and abs(high - 0.13159) < 1e-4
    assert clopper_pearson(0, 10)[0] == 0.0 and clopper_pearson(10, 10)[1] == 1.0

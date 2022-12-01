from hawa.paper.mht import MhtData
from test.mock import prepare_test

prepare_test()


def test_mht_init():
    rows = [
        {"meta_unit_type": "school", "meta_unit_id": 4107110001,
         "target_year": 2022, "test_type": "mht"},
    ]
    for row in rows:
        MhtData(**row)

from loguru import logger

from hawa.paper.health import HealthApiData
from test.mock import prepare_test

prepare_test()


def test_health_api_run():
    rows = [
        # {"meta_unit_id": 5134010001, "target_year": 2021},
        # {"meta_unit_id": 5134310010, "target_year": 2023},
        {"meta_unit_id": 1101089005, "target_year": 2023, "meta_unit_type": "school"},
        {"meta_unit_id": 110108, "target_year": 2023, "meta_unit_type": "district"},
        {"meta_unit_id": 110000, "target_year": 2023, "meta_unit_type": "province"},
        # {"meta_unit_id": 4107000001, "target_year": 2023},
    ]
    for row in rows:
        logger.info(row)
        d = HealthApiData(**row)
        for i in range(10, 12):
            print(f"{d.meta_unit_id} {i=} {d.score_rank(i)}")

    other_rows = [
        {"meta_unit_id": 511900, "target_year": 2023, "meta_unit_type": "city"},
    ]
    for row in other_rows:
        logger.info(row)
        d = HealthApiData(**row)
        for i in range(3, 6):
            print(f"{d.meta_unit_id} {i=} {d.score_rank(i)}")

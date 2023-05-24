from loguru import logger

from hawa.data.klass import ClassHealthApiData
from hawa.paper.health import HealthApiData
from test.mock import prepare_test

prepare_test()


def test_health_api_run():
    rows = [
        # {"meta_unit_id": 5134010001, "target_year": 2021},
        # {"meta_unit_id": 5134310010, "target_year": 2023},
        # {"meta_unit_id": 1101089005, "target_year": 2023, "meta_unit_type": "school", "grade": 10},
        {"meta_unit_type": "school", "meta_unit_id": 3707030001, "target_year": 2021, "grade": 3},
        # {"meta_unit_id": 110108, "target_year": 2023, "meta_unit_type": "district", "grade": 10},
        # {"meta_unit_id": 110000, "target_year": 2023, "meta_unit_type": "province", "grade": 10},
        # {"meta_unit_id": 4107000001, "target_year": 2023},
    ]
    for row in rows:
        logger.info(row)
        d = HealthApiData(**row)
        for i in range(10, 11):
            print(f"{d.meta_unit_id} {i=} {d.score_rank(i)}")

    other_rows = [
        {"meta_unit_id": 511900, "target_year": 2023, "meta_unit_type": "city", "grade": 3},
    ]
    for row in other_rows:
        logger.info(row)
        d = HealthApiData(**row)
        for i in range(3, 4):
            print(f"{d.meta_unit_id} {i=} {d.score_rank(i)}")


def test_class_health_api_run():
    data = [
        {"meta_unit_id": 5134010001, "target_year": 2023, "meta_unit_type": "class", "grade": 3,
         "meta_class_id": 513401000102301},
    ]
    for row in data:
        logger.info(row)
        d = ClassHealthApiData(**row)
        for i in range(3, 4):
            try:
                print(f"{d.meta_unit_id} {i=} {d.score_rank(i)}")
            except Exception as e:
                print(f"{str(e)=}")

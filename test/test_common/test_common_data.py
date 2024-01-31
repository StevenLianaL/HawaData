from loguru import logger

from hawa.common.data import CommonData
from hawa.paper.health import HealthReportData
from test.mock import prepare_test

prepare_test()


def test_common_init():
    rows = [
        {"meta_unit_type": "school", "meta_unit_id": 1101089005, "target_year": 2023},
        {"meta_unit_type": "district", "meta_unit_id": 370703, "target_year": 2021},
        {"meta_unit_type": "city", "meta_unit_id": 331100, "target_year": 2021},
        {"meta_unit_type": "province", "meta_unit_id": 410000, "target_year": 2021},
        # {"meta_unit_type": "country", "meta_unit_id": 0, "target_year": 2023},

    ]
    for row in rows:
        logger.info(row)
        # common data without default  test_types and code_word_list
        CommonData(
            **row, test_types=['publicWelfare', 'ZjpublicWelfare'],
            code_word_list={'dimension', 'field'}
        )


def test_gen_year_data():
    pass
    # HealthReportData.cache_year_data(year=2023)


def test_a_case():
    rows = [
        {"meta_unit_type": "school", "meta_unit_id": 5134010001,
         "target_year": 2023},
    ]
    for row in rows:
        logger.info(row)
        c = HealthReportData(
            **row, code_word_list={'dimension', 'field'}
        )
        print(f"{c.final_scores.columns=}")
        print(f"{c.final_answers.columns=}")
        # c.final_answers['student_id'] = c.final_answers['student_id'].astype('str')
        # c.final_answers.to_excel('final_answers.xlsx')
        print(f"{len(c.final_answers.student_id.unique())=}")

        for r in c.grade_class_student_table:
            print(r)
            print('---')

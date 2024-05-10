from pprint import pprint

from loguru import logger

from hawa.data.assemble import AssembleHealthApiData, AssembleMhtPlusQusPlusApiData, AssembleMhtPlusPlusApiData
from hawa.data.klass import ClassHealthApiData
from hawa.data.province import ProvinceHealthApiDataLess
from hawa.data.student import StudentHealthApiData, StudentMhtPlusApiData
from hawa.paper.health import HealthReportData
from test.mock import prepare_test

prepare_test()


def test_health_api_run():
    rows = [
        # {"meta_unit_id": 5134010001, "target_year": 2021},
        # {"meta_unit_id": 5134310010, "target_year": 2023},
        # {"meta_unit_id": 513400, "target_year": 2023, "meta_unit_type": "city"},
        # {"meta_unit_id": 513401, "target_year": 2023, "meta_unit_type": "district"},
        # {"meta_unit_id": 0, "target_year": 2023, "meta_unit_type": "country"},
        # {"meta_unit_id": 5134010001, "target_year": 2023, "meta_unit_type": "school"},
        # {"meta_unit_id": 1101088012, "target_year": 2023, "meta_unit_type": "school"},
        # {"meta_unit_id": 3308250001, "target_year": 2024, "meta_unit_type": "school"},
        {"meta_unit_id": 1101019056, "target_year": 2024, "meta_unit_type": "school"},
        # {"meta_unit_type": "school", "meta_unit_id": 3707030003, "target_year": 2021},
        # {"meta_unit_id": 110108, "target_year": 2023, "meta_unit_type": "district", "grade": 10},
        # {"meta_unit_id": 110000, "target_year": 2023, "meta_unit_type": "province", "grade": 10},
        # {"meta_unit_id": 4107000001, "target_year": 2023},
    ]
    for row in rows:
        logger.info(row)
        dd = HealthReportData(**row)
        # dd.count_field_point_target()
        # pprint(dd.temp_school_grade_class_data())
        # a = (dd.grade_class_map, dd.grade_class_student_table)
        # pprint(dd.measurement.fields)
        # dd.get_grade_focus(limit=60, step=1, mode='field')
        # pprint(dd.grade_class_map)
        # print(dd.case.join_date, dd.case.start_date, dd.case.end_date)
        pprint(dd.count_grade_class_item_target())


def test_assemble_health_api_run():
    rows = [
        {'school_ids': [5134010006, 5134010005], "target_year": 2023}
    ]
    for row in rows:
        logger.info(row)
        dd = AssembleHealthApiData(**row)
        print(dd.final_scores)


def test_cascade_schools_from_province():
    rows = [
        {"meta_unit_id": 110000, "target_year": 2023, "meta_unit_type": "province"},
        {"meta_unit_id": 510000, "target_year": 2023, "meta_unit_type": "province"},
    ]
    for row in rows:
        dd = ProvinceHealthApiDataLess(**row)
        pprint(dd.get_cascade_schools_from_province())


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
                print(f"{d.meta_unit_id} {i=} {d.score_rank(i, gender='F')}")
            except Exception as e:
                print(f"{str(e)=}")

        print(f"{d.count_dim_field_ranks('field')=}")


def test_student_health_api_run():
    data = [
        # {"meta_unit_id": 5134010001, "target_year": 2023, "meta_unit_type": "student",
        #  "meta_student_id": 513401000102301216},
        {"meta_unit_id": 5134010001, "target_year": 2023, "meta_unit_type": "student",
         "meta_student_id": 513401000102301216, "grade": 3},
    ]
    for row in data:
        logger.info(row)
        d = StudentHealthApiData(**row)
        print(f"{d.score_rank(grade=3)=}")
        print(
            f"{d.count_dim_or_field_scores_by_answers(answers=d.final_answers,item_code='dimension',res_format='list')=}")
        print(f"{d.count_dim_or_field_scores_by_answers(answers=d.final_answers,item_code='field')=}")


def test_student_mht_api_run():
    data = [
        {"meta_unit_id": 4107000020, "target_year": 2023, "meta_unit_type": "student",
         "meta_student_id": 410700002002301001, "grade": 7},
        {"meta_unit_id": 4107820676, "target_year": 2023, "meta_unit_type": "student",
         "meta_student_id": 1652332, "grade": 10},
        {"meta_unit_id": 4107820676, "target_year": 2023, "meta_unit_type": "student",
         "meta_student_id": 1652332},
    ]
    for row in data:
        logger.info(row)
        d = StudentMhtPlusApiData(**row, is_filter_cls_less10=False)
        d.count_student_archive()


def test_mht_plus_assemble_run():
    s = AssembleMhtPlusPlusApiData(
        school_ids=[4107820676], target_year=2023, different_mode='xx'
    )


def test_mht_assemble_api_run():
    s = AssembleMhtPlusQusPlusApiData(
        school_ids=[4107210104, 4107810203], target_year=2023, different_mode='xx'
    )

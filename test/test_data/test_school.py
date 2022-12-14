from loguru import logger

from hawa.data.school import SchoolHealthReportData, SchoolMhtWebData
from test.mock import prepare_test, validate_data_for_web

prepare_test()


def test_health_report_run():
    rows = [
        {"meta_unit_id": 3707030003, "target_year": 2021},
    ]
    for row in rows:
        logger.info(row)
        SchoolHealthReportData(**row)


def test_mht_web_run():
    rows = [
        {"meta_unit_id": 4107110001, "target_year": 2022},
    ]
    for row in rows:
        md = SchoolMhtWebData(**row)
        assert len(md.scale_student_score) == 3
        assert len(md.sub_scale_score) == 3
        assert len(md.grade_scale_student_score) == 3
        assert len(md.grade_special_students) == 3

        data = [
            md.scale_student_score, md.sub_scale_score,
            md.grade_scale_student_score, md.grade_sub_scale_score,
            md.grade_special_students
        ]
        for d in data:
            validate_data_for_web(d)

        assert len(md.scale_student_score['x_axis']) == 100
        assert len(md.scale_student_score['y_axis']) == 100
        print(md.sub_scale_score)

        print(md.grade_sub_scale_score)

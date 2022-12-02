from loguru import logger

from hawa.data.school import SchoolHealthReportData, SchoolMhtWebData
from test.mock import prepare_test

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
        assert len(md.sub_scale_score) == 4
        assert len(md.grade_scale_student_score) == 3
        assert len(md.grade_special_students) == 3

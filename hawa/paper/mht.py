from dataclasses import dataclass, field
from typing import Set

from hawa.common.data import CommonData


@dataclass
class MhtData(CommonData):
    test_type: str = 'mht'
    code_word_list: Set[str] = field(default_factory=lambda: {'mht'})

    def _to_count_c_student_score(self):
        """学生总量表得分图数据，横轴分数，纵轴分数"""

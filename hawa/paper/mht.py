from dataclasses import dataclass, field
from typing import Set

from hawa.common.data import CommonData


@dataclass
class MhtData(CommonData):
    test_type: str = 'mht'
    code_word_list: Set[str] = field(default_factory=lambda: {'mht'})

    def _to_count_c_student_score(self):
        """学生总量表得分图数据，横轴分数，纵轴人数"""
        data = []
        for score, row in self.final_scores.groupby('score'):
            data.append((int(score), row.score.count()))
        data.sort(key=lambda x: x[0])
        scores, people_count = [], []
        for (score, student_count) in data:
            scores.append(score)
            people_count.append(student_count)
        return {
            "name": f"{self.meta_unit.name}参测学生总量表得分图",
            "scores": scores,
            "counts": people_count
        }

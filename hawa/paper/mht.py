from collections import defaultdict
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
        x_axis, y_axis = [], []
        for (score, student_count) in data:
            x_axis.append(score)
            y_axis.append(student_count)
        return {
            "name": f"{self.meta_unit.name}参测学生总量表得分图",
            "x_scores": x_axis,
            "y_counts": y_axis
        }

    def _to_count_d_sub_code_score(self):
        """在 8 个子量表上的得分图，横轴量表，纵轴分数"""
        mht_scores = defaultdict(list)
        x_axis, y_axis = [], []
        for (student_id, mht), group in self.final_answers.groupby(by=['student_id', 'mht']):
            if mht == '效度':
                continue
            mht_scores[mht].append(group.score.sum())
        for mht, score_list in mht_scores.items():
            y_axis.append(round(sum(score_list) / len(score_list), 1))
        return {
            "name": f"{self.meta_unit.name}参测学生在 8 个子量表上的得分图",
            "x_mht": x_axis,
            "y_count": y_axis,
        }

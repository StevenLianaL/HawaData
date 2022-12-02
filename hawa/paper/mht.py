from collections import defaultdict
from dataclasses import dataclass, field
from typing import Set

import pandas as pd

from hawa.common.data import CommonData
from hawa.config import project


@dataclass
class MhtData(CommonData):
    test_type: str = 'mht'
    code_word_list: Set[str] = field(default_factory=lambda: {'mht'})

    # 计算数据
    scale_student_score: dict = field(default_factory=dict)
    sub_scale_score: dict = field(default_factory=dict)
    grade_scale_student_score: dict = field(default_factory=list)
    grade_special_students: dict = field(default_factory=dict)

    def _to_count_c_scale_student_score(self):
        """学生总量表得分图数据，横轴分数，纵轴人数 （总 及 各年级）"""
        self.scale_student_score = self._tool_count_student_score(score=self.final_scores)

    def _to_count_d_sub_scale_code_score(self):
        """在 8 个子量表上的得分图，横轴量表，纵轴分数"""
        self.sub_scale_score = self._tool_count_sub_code_score(
            answers=self.final_answers, unit_name=self.meta_unit.name
        )

    def _to_count_e_grade_student_score(self):
        """参考 _to_count_c_student_score， 分年级计算"""
        res = {}
        for grade, grade_group in self.final_scores.groupby(by='grade'):
            grade_data = self._tool_count_student_score(score=grade_group, grade=grade)
            res[grade] = grade_data
        self.grade_scale_student_score = res

    def _to_count_f_grade_special_students(self):
        """计算各年级 某量表超过8分的学生"""
        res = defaultdict(list)
        for grade, grade_ans_group in self.final_answers.groupby('grade'):
            for student_id, student_group in grade_ans_group.groupby('student_id'):
                student_name = student_group['username'].tolist()[0]
                res[grade].append(
                    self._tool_count_sub_code_score(
                        answers=student_group,
                        name=f"{student_name}8个子量表得分",
                        unit_name=student_name
                    )
                )
        self.grade_special_students = res

    # 计算工具
    def _tool_count_student_score(self, score: pd.DataFrame, grade: int = None):
        score['score'] = score['score'].astype(int)
        data = []
        handred = set(range(1, 101))
        for score, row in score.groupby('score'):
            handred.discard(score)
            data.append((score, int(row.score.count())))
        for score in handred:
            data.append((score, 0))
        data.sort(key=lambda x: x[0])
        x_axis, y_axis = [], []
        for (score, student_count) in data:
            x_axis.append(score)
            y_axis.append(student_count)

        if grade:
            name = f"{self.meta_unit.name}{project.grade_mapping[grade]}年级参测学生总量表得分图"
        else:
            name = f"{self.meta_unit.name}参测学生总量表得分图"

        return {
            "name": name,
            "x_scores": x_axis,
            "y_counts": y_axis
        }

    def _tool_count_sub_code_score(self, answers: pd.DataFrame, name: str = '', unit_name: str = '', grade: int = None):
        mht_scores = defaultdict(list)
        x_axis, y_axis = [], []
        for (student_id, mht), group in answers.groupby(by=['student_id', 'mht']):
            if mht == '效度':
                continue
            mht_scores[mht].append(group.score.sum())
        for mht, score_list in mht_scores.items():
            x_axis.append(mht)
            y_axis.append(round(float(sum(score_list) / len(score_list)), 1))

        if grade:
            name = f"{self.meta_unit.name}{project.grade_mapping[grade]}年级参测学生在8个子量表上的得分图"
        else:
            name = f"{self.meta_unit.name}参测学生在8个子量表上的得分图"

        return {
            "name": name,
            "unit_name": unit_name,
            "x_mht": x_axis,
            "y_count": y_axis,
        }


@dataclass
class MhtWebData(MhtData):
    pass

"""通用的 report data 构造器，支持 校、区、市、省、全国级别的通用报告数据构造"""
from dataclasses import dataclass, field
from typing import Optional, ClassVar, Any, Set

import pandas as pd
import pendulum

from hawa.base.db import DbUtil, RedisUtil
from hawa.common.query import DataQuery
from hawa.common.utils import GradeData, CaseData, Measurement
from hawa.config import project


class MetaCommomData(type):
    def __new__(cls, name, bases, attrs):
        attrs['db'] = DbUtil()
        attrs['redis'] = RedisUtil()
        attrs['query'] = DataQuery()
        return super().__new__(cls, name, bases, attrs)


@dataclass
class CommonData(metaclass=MetaCommomData):
    # 构造单位
    meta_unit_type: Optional[str] = ''  # school/district/city/province/country
    meta_unit_id: Optional[int] = None
    meta_unit: Optional[Any] = None

    # 时间目标
    target_year: Optional[int] = None
    last_year_num: Optional[int] = None
    is_load_last: bool = True  # 仅计算往年数据时 为 False

    # 卷子
    test_type: str = ''
    test_types: list = field(default_factory=list)
    code_word_list: Set[str] = field(default=set)  # 卷子使用指标的词表，详见继承

    # meta class tool
    db: ClassVar[DbUtil] = None
    redis: ClassVar[RedisUtil] = None
    query: ClassVar[DataQuery] = None

    # 原始数据

    school_ids: list[int] = field(default_factory=list)
    schools: pd.DataFrame = pd.DataFrame()

    cases: pd.DataFrame = pd.DataFrame()
    case_ids: list[int] = field(default_factory=list)

    answers: pd.DataFrame = pd.DataFrame()

    students: pd.DataFrame = pd.DataFrame()
    student_ids: list[int] = field(default_factory=list)
    student_count: Optional[int] = None

    item_ids: Optional[set[int]] = None
    items: Optional[pd.DataFrame] = None

    # 辅助工具
    grade_util: Optional[GradeData] = None
    case_util: Optional[CaseData] = None
    measurement = Measurement()

    # 计算数据
    final_answers: pd.DataFrame = pd.DataFrame()
    final_scores: pd.DataFrame = pd.DataFrame()

    # 去年全国数据
    last_year = None
    last_year_code_scores: Optional[pd.DataFrame] = pd.DataFrame()

    def __post_init__(self):
        # 初始化数据
        init_functions = [i for i in dir(self) if i.startswith('_to_init_')]
        for func in init_functions:
            getattr(self, func)()

        # 构建辅助工具
        self._to_build_helper()

        # 计算数据
        count_functions = [i for i in dir(self) if i.startswith('_to_count_')]
        for func in count_functions:
            getattr(self, func)()

    def _to_init_a_meta_unit(self):
        self.meta_unit = self.query.query_unit(self.meta_unit_type, self.meta_unit_id)

    def _to_init_b_time(self):
        if not self.target_year:
            self.target_year = pendulum.now().year
        self.last_year_num = self.target_year - 1
        project.logger.info(f'target_year: {self.target_year}')

    def _to_init_c_schools(self):
        if self.school_ids:
            self.schools = self.query.query_schools_by_ids(self.school_ids)
        else:
            if self.meta_unit_type == 'country':
                self.schools = self.query.query_schools_all()
            else:
                self.schools = self.query.query_schools_by_startwith(self.meta_unit_id)
            self.school_ids = self.schools['id'].tolist()
        project.logger.debug(f'schools: {len(self.schools)}')

    def _to_init_d_cases(self):
        start_stamp = pendulum.datetime(self.target_year, 1, 1)
        end_stamp = pendulum.datetime(self.target_year + 1, 1, 1)
        start_stamp_str = start_stamp.format(project.format)
        end_stamp_str = end_stamp.format(project.format)

        papers = self.query.query_papers(test_types=self.test_types, test_type=self.test_type)
        paper_ids = papers['id'].tolist()

        self.cases = self.query.query_cases(
            school_ids=self.school_ids,
            paper_ids=paper_ids,
            valid_to_start=start_stamp_str,
            valid_to_end=end_stamp_str,
        )
        if self.cases.empty:
            raise Exception(f'no cases:{self.meta_unit} {self.school_ids}')
        self.case_ids = self.cases['id'].tolist()
        project.logger.debug(f'cases: {len(self.cases)}')

    def _to_init_e_answers(self):
        self.answers = self.query.query_answers(case_ids=self.case_ids)
        project.logger.debug(f'answers: {len(self.answers)}')

    def _to_init_f_students(self):
        self.student_ids = set(self.answers['student_id'].tolist())
        student_id_list = list(self.student_ids)
        self.students = self.query.query_students(student_id_list)
        self.student_count = len(self.student_ids)
        project.logger.debug(f'students: {self.student_count}')

    def _to_init_g_items(self):
        self.item_ids = set(self.answers['item_id'].drop_duplicates())
        self.items = self.query.query_items(self.item_ids)
        project.logger.debug(f'items: {len(self.items)}')

    def _to_build_helper(self):
        self.grade = GradeData(case_ids=self.case_ids)
        self.case = CaseData(cases=self.cases)

    def _to_count_a_final_answers(self):
        items = {}
        item_codes = self.query.query_item_codes(self.item_ids)
        project.logger.debug(f"{self.code_word_list=}")
        for item_id, codes in item_codes.groupby('item_id'):
            items[item_id] = [i for i in codes.to_dict(orient='records')
                              if i['category'] in self.code_word_list]

        data = pd.merge(
            self.answers, self.students.loc[:, ['id', 'gender', 'first_name', 'last_name']],
            left_on='student_id', right_on='id'
        )
        project.logger.debug(f"ans merge students {len(data)}")
        # inner 时，final_answers 和 answers 数目不等：final_answers 过滤掉了 没有 code_word_list（维度领域或其他）的题目
        # outer 时，数目相等，不过滤任何题目
        data = pd.merge(data, item_codes, left_on='item_id', right_on='item_id', how='inner')

        data['cls'] = data['id_y'].apply(lambda x: int(str(x)[13:15]))
        data['grade'] = data['case_id'].apply(lambda x: int(str(x)[-2:]))
        data['username'] = data.apply(lambda x: f"{x.last_name}{x.first_name}", axis=1)
        for code_word in self.code_word_list:
            data[code_word] = data.item_id.apply(self._count_field, args=(code_word, items))
        self.final_answers = data.drop_duplicates(subset=['case_id', 'student_id', 'item_id'])
        project.logger.debug(f'final_answers: {len(self.final_answers)}')

    def _to_count_b_final_scores(self):
        self.final_scores = self.count_final_score(answers=self.final_answers)
        project.logger.debug(f'final_scores: {len(self.final_scores)}')

    def _count_field(self, item_id: int, code: str, items: dict):
        return [i for i in items[item_id] if i['category'] == code][0]['name']

    @staticmethod
    def count_level(score, mode: str = 'f'):
        assert mode in ('f', 'r'), 'only support feedback or report'
        if score >= 90:
            a = 'A'
        elif score >= 80:
            a = 'B'
        elif score >= 60:
            a = 'C'
        else:
            a = 'D'
        key = "RANK_LABEL" if mode == 'r' else 'FEEDBACK_LEVEL'
        return project.ranks[key][a]

    def count_final_score(self, answers: pd.DataFrame):
        res = answers.groupby(by=['grade', 'gender', 'student_id']).score.mean().reset_index()
        res = res.assign(score=res.score * 100)
        res['level'] = res.score.apply(lambda x: self.count_level(x))
        return res

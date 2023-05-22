from dataclasses import dataclass

from hawa.paper.health import HealthApiData


@dataclass
class ClassMixin:
    """为了在 __mro__ 中有更高的优先级， mixin 在继承时，应该放在最前"""
    meta_unit_type: str = 'class'


@dataclass
class ClassHealthApiData(ClassMixin, HealthApiData):
    """使用 school id 作为 meta_unit_id，额外增加班级的逻辑"""

    def _to_init_a_meta_unit(self):
        self.meta_unit = self.query.query_unit(self.meta_unit_type, str(self.meta_unit_id))

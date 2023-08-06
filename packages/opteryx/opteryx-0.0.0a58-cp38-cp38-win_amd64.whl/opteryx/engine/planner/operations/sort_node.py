# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Sort Node

This is a SQL Query Execution Plan Node.

This node orders a dataset
"""
from typing import Iterable
from pyarrow import concat_tables, Table
from opteryx.engine.query_statistics import QueryStatistics
from opteryx.engine.planner.operations.base_plan_node import BasePlanNode
from opteryx.utils.columns import Columns

class SortNode(BasePlanNode):
    def __init__(self, statistics: QueryStatistics, **config):
        self._order = config.get("order", [])

    def greedy(self):
        return True

    def __repr__(self) -> str:
        return ",".join([str(i) for i in self._order])

    @property
    def name(self):
        return "Sort"

    def execute(self, data_pages: Iterable) -> Iterable:

        if isinstance(data_pages, Table):
            data_pages = [data_pages]

        table = concat_tables(data_pages)
        columns = Columns(table)

        self._mapped_order = []
        for column, direction in self._order:
            self._mapped_order.append((columns.get_column_from_alias(column, only_one=True), direction,))

        yield table.sort_by(self._mapped_order)

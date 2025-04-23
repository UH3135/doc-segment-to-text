import re
from typing import List, Dict, Tuple
from bs4 import BeautifulSoup
from collections import deque
from dataclasses import dataclass
from utils.logger import init_logger


logger = init_logger(__file__, "DEBUG")


@dataclass
class Table:
    html: str
    row: int
    col: int


class TableParser:
    def __init__(self) -> None:
        pass

    def parse_table_from_html(self, html: str) -> Dict[str, List[str]]:
        """
        Table 객체를 Dict 형식으로 변환하는 함수

        Args:
            html: html 문자열 데이터

        Returns:
            result(Dict[List[str]]): 표의 첫번째 행을 Key로 가지는 Dict
        """
        try:
            row_len, col_len = self._get_row_and_column_length(html)

            table = Table(html, row_len, col_len)
            if not table:
                logger.warning("Table is Empty")

            matrix = self._html_to_matrix(table)
            if not matrix:
                logger.error("Table is Empty")
                return
            if row_len == 1 and col_len == 1:
                return {'content': matrix[0][0]}
            elif row_len == 1:
                return {matrix[0][0]: matrix[0][1:]}
            elif col_len == 1:
                return {matrix[0][0]: [matrix[i][0] for i in range(row_len)]}
            result = self._convert_matrix_to_dict(matrix)
            logger.info("Success parsing table from html")

            return result
        
        except Exception as e:
            logger.critical(f"Unexpect Error {e}")
    
    def _convert_matrix_to_dict(self, matrix: List[List]) -> Dict:
        """
        2차원 배열을 Dict로 변환하는 함수
            만약 첫번째 행에서 중복되는 값이 있는 경우 두번째 행을 이용하여 Primary Key를 생성함
            두번째 키와 조합해서도 중복이 생기면 뒤에 수를 추가해서 차이를 만듦

        Args:
            matrix: 2차원 배열로 된 표 데이터

        Returns:
            result(Dict[List[str]]): 표의 첫번째 행을 Key로 가지는 Dict
        """
        header_row = matrix[0]
        second_row = matrix[1]

        header_counts = set()
        has_duplicates = False

        for header in header_row:
            if header in header_counts:
                has_duplicates = True
                break
            else:
                header_counts.add(header)

        keys = []
        seen_keys = set()
        for i, (header, value) in enumerate(zip(header_row, second_row)):
            if has_duplicates:
                base_key = f"{value}_{header}" if value is not None and value != header else header
                key = base_key
                if key in seen_keys:
                    key = f"{base_key}_{i}"
            else:
                key = header

            keys.append(key)
            seen_keys.add(key)

        result = {key: [] for key in keys}
        start = 1 if not has_duplicates else 2
        for row in matrix[start:]:
            for i, value in enumerate(row):
                if i < len(keys):
                    result[keys[i]].append(value)

        return result
    
    def _get_row_and_column_length(self, html: str) -> Tuple[int, int]:
        """
        html 데이터에서 행렬의 크기를 구하는 함수

        Args:
            html: html 문자열 데이터

        Returns:
            row_len, col_len: 각각 행의 길이, 열의 길이
        """        
        soup = BeautifulSoup(html, "html.parser")
        table_html = soup.find("table")

        rows = table_html.find_all("tr")
        row_len = len(rows)

        col_lens = []

        for row in rows:
            col_len = 0
            for cell in row.find_all(["th", "td"]):
                colspan = int(cell.get("colspan", 1))
                if colspan > 1:
                    col_len += (colspan-1)
                col_len += 1
            col_lens.append(col_len)
        return row_len, max(col_lens)

    def _html_to_matrix(self, table: Table) -> List[List[str]]:
        """
        Table 객체에서 2차원 행렬로 변환하는 함수
            만약 행 또는 열끼리 결합한 경우 같은 값을 추가해 줌
            또 값이 없다면 None으로 표의 형태를 유지함

        Args:
            table: Table 크기와 html이 담긴 객체

        Returns:
            matrix: 2차원 행렬로 표현한 표 데이터
        """        
        soup = BeautifulSoup(table.html, "html.parser")
        table_html = soup.find("table")

        if not table_html:
            return []
        
        matrix = []
        rowspan_tracker = {}

        for row in table_html.find_all("tr"):
            row_data = []
            col_idx = 0
                
            cells = deque(row.find_all(["th", "td"]))
            while col_idx < table.col:
                while col_idx in rowspan_tracker:
                    row_data.append(rowspan_tracker[col_idx]["value"])
                    rowspan_tracker[col_idx]["remaining_rows"] -= 1
                    if rowspan_tracker[col_idx]["remaining_rows"] == 0:
                        del rowspan_tracker[col_idx]
                    col_idx += 1
                
                if col_idx >= table.col:
                    break

                if cells:
                    cell = cells.popleft()

                    cell_value = cell.get_text(strip=True)
                    rowspan = int(cell.get("rowspan", 1))
                    colspan = int(cell.get("colspan", 1))

                    if colspan > 1:
                        for _ in range(colspan-1):
                            row_data.append(cell_value)
                            col_idx += 1

                    if rowspan > 1:
                        rowspan_tracker[col_idx] = {
                            "remaining_rows": rowspan - 1,
                            "value": cell_value
                        }

                    row_data.append(cell_value)

                else:
                    row_data.append(None)

                col_idx += 1
            
            matrix.append(row_data)
            
        return matrix

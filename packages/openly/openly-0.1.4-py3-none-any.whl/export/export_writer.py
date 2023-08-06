from io import BytesIO

HEADER_FORMAT = {
    'bold': True,
    'size': 22,
    'align': 'center',
    'valign': 'vcenter'
}

COLUMN_TITLE_FORMAT = {
    'bold': True,
    'size': 12,
    'align': 'center',
    'valign': 'vcenter',
    'border': 1,
    'fg_color': '#DDDDDD',
}

MONEY_FORMAT = {
    'num_format': '$#,##0'
}

TEXT_FORMAT = {'text_wrap': 1,
               'size': 10,
               'align': 'left',
               'valign': 'top'}


class ExportTemplateWriter(object):
    """ Interface for writing data to excel spreadsheets

    The ExportTemplateWriter provides a convenient way to specify templates for column-based
    excel data. On initialization the user provides a tuple of parameters specifying the format
    for each column as well as a tuple of tuples specifying the column titles. Optionally,
    specifications for summary columns and rows can be given detailing a spreadsheet function
    to be called on row/column data.

    Once the template is specified, the write_data method can be called with a tuple of tuples
    representing the data to write. This returns the data written as a StringIO.StringIO to
    be written into an excel file.
    """

    # Some commonly used column parameters
    WIDE_COLUMN_PARAMS = {'width': 45}
    DEFAULT_COLUMN_PARAMS = {'width': 20}
    MONEY_COLUMN_PARAMS = {'width': 20, 'format': 'money'}
    TEXT_COLUMN_PARAMS = {'width': 25, 'format': 'text'}

    def __init__(self, title, column_params, column_titles,
                 summary_columns={}, summary_rows=None):
        """ Set the parameters for the export writer

        Arguments:
        title -- Title that will be written into the first row of the sheet
        column_params -- tuple of dicts specifying the column parameters for the spreadsheet's
          columns where the first tuple-entry corresponds to the first column in the
          spreadsheet etc.. The dict should contain keywords 'width' specifying the column's
          width and 'format' specifying the string key for the format object stored in
          self.formats
        column_titles -- tuple of tuples the titles for each column. In order to merge row and
          column cells set tuple entries to None. In general a column title will be written
          across cells representing the maximal rectangle of None tuple-entries looking first
          right along the current tuple and then down across remaining tuples. For instance
          (('a',None,None),('1','2','3')) will write 'a' into cells A2:C2, '1' into A3, '2' into
          B3 and '3' into C3 while (('a', None, 'b'),(None,None,'2')) will write 'a' into
          the rectange A2:B3, 'b' into D2, and '2' into D3.

        Keyword arguments:
        summary_columns -- A dictionary containing tuples (Excel Function Name, (Column Numbers))
          keyed off of the column number to write the summary into, e.g. {12: ('SUM', (1, 5, 9))}
        summary_rows -- A tuple of summary rows with entries (Row Name, Excel Function Name,
          (Column Numbers)). Here Row Name will be written into the first column in the
          appropriate row and then the given excel function will be applied to all data entries
          in the given columns, e.g. ('Total', 'SUM', (1, 3, 4)) will call the excel SUM function
          on the data entries in the second, fourth, and fifth columns.
        """
        from xlsxwriter import Workbook
        self.output = BytesIO()
        self.workbook = Workbook(self.output)
        self.worksheet = self.workbook.add_worksheet(name='Data')
        self.filter_worksheet = self.workbook.add_worksheet(name='Filters Applied')

        # Add basic formatting to the workbook
        self.header = self.workbook.add_format(HEADER_FORMAT)
        self.column_title = self.workbook.add_format(COLUMN_TITLE_FORMAT)
        self.money = self.workbook.add_format(MONEY_FORMAT)
        self.text = self.workbook.add_format(TEXT_FORMAT)
        self.formats = {
            'header': self.header,
            'column_title': self.column_title,
            'money': self.money,
            'text': self.text
        }

        # Store template information
        self.title = title
        self.column_params = column_params
        self.column_titles = column_titles
        self.summary_columns = summary_columns
        self.summary_rows = summary_rows

        self.num_cols = len(self.column_params)
        self.num_summary_cols = len(summary_columns) if summary_columns is not None else 0

        # Check that the given column_param and column_title tuples have consistent size
        self._assert_valid_dimensions()

    def _assert_valid_dimensions(self):
        """ Check that the sheet will contain at least one data column and the column title
        entries all have the same size
        """
        assert self.num_cols > 0
        for i in range(len(self.column_titles)):
            assert len(self.column_titles[i]) == self.num_cols,\
                '{} {}'.format(self.num_cols, self.column_titles[i])

    def write_data(self, data, filters=None):
        # If we are passed the filters used write them
        from xlsxwriter.utility import xl_rowcol_to_cell
        if filters is not None:
            self.write_filters(filters)

        # Format the columns and write the titles
        self._set_column_widths()
        self._write_title()
        self._write_column_titles()

        # Check that the given data has the correct size
        for row in data:
            assert len(row) == self.num_cols - len(self.summary_columns)

        row_offset = 1 + len(self.column_titles)  # Adjust for title rows
        data_col = 0
        for j in range(self.num_cols):
            # Get the format for the column
            column_format = None
            if 'format' in self.column_params[j]:
                column_format = self.formats[self.column_params[j]['format']]

            if j not in self.summary_columns:
                # Normal data
                for i in range(len(data)):
                    self.worksheet.write(i + row_offset, j, data[i][data_col], column_format)
                data_col += 1
            else:
                summary_func, summary_cols = self.summary_columns[j]
                # Summary data
                for i in range(len(data)):
                    formula_str = '={func}({cells})'.format(
                        func=summary_func,
                        cells=','.join([xl_rowcol_to_cell(i + row_offset, col)
                                        for col
                                        in summary_cols]))
                    self.worksheet.write(i + row_offset, j, formula_str, column_format)

        # Add summary rows if specified
        if self.summary_rows is not None:
            for i, (row_name, row_func, cols) in enumerate(self.summary_rows):
                # Find the current row, write its title, then summarize the specified cols
                row = i + len(data) + row_offset
                self.worksheet.write(row, 0, row_name, self.column_title)
                for j in range(1, self.num_cols):
                    if j in cols:
                        formula_str = '={func}({first}:{last})'.format(
                            func=row_func,
                            first=xl_rowcol_to_cell(row_offset, j),
                            last=xl_rowcol_to_cell(row_offset + len(data) - 1, j))
                    else:
                        formula_str = ''
                    self.worksheet.write(row, j, formula_str, self.column_title)

        self.workbook.close()
        return self.output

    def write_filters(self, filters):
        self.filter_worksheet.set_column(0, 0, 20)
        self.filter_worksheet.set_column(1, 1, 50)
        self.filter_worksheet.write(0, 0, 'Filter Name', self.column_title)
        self.filter_worksheet.write(0, 1, 'Filter Value', self.column_title)
        for row, (filter_name, filter_value) in enumerate(filters.items()):
            if type(filter_value) is list or type(filter_value) is tuple:
                filter_value = ', '.join(filter_value)
            self.filter_worksheet.write(row + 1, 0, str(filter_name))
            self.filter_worksheet.write(row + 1, 1, str(filter_value), self.text)

    def _set_column_widths(self):
        for i in range(len(self.column_params)):
            self.worksheet.set_column(i, i, self.column_params[i]['width'])

    def _write_title(self):
        self.worksheet.merge_range(0, 0, 0, self.num_cols - 1,
                                   self.title, self.header)

    def _write_column_titles(self):
        for i in range(len(self.column_titles)):
            for j in range(self.num_cols):
                title = self.column_titles[i][j]
                if title is None:
                    continue
                k, el = self._find_range(i, j)
                if (i == k and j == el):
                    # Write title to a single cell, adjusting row by one because of title
                    self.worksheet.write(i + 1, j, title, self.column_title)
                else:
                    # Write title to a range, adjusting row by one because of title
                    self.worksheet.merge_range(i + 1, j, k + 1, el, title, self.column_title)

    def _find_range(self, i, j):
        # Find number of rows to merge
        k = i
        while k < len(self.column_titles) - 1:
            if self.column_titles[k + 1][j] is not None:
                break
            k += 1

        # Find number of columns to merge
        el = j
        while el < self.num_cols - 1:
            if self.column_titles[i][el + 1] is not None:
                break
            unmerged_column = True
            for r in range(i, -1, -1):
                if self.column_titles[r][el + 1] is not None:
                    unmerged_column = False
                    break
            if not unmerged_column:
                break
            el += 1

        # Assert this range is valid
        for m in range(i, k + 1):
            for n in range(j, el + 1):
                if (m == i and n == j):
                    continue
                assert self.column_titles[m][n] is None
        return k, el

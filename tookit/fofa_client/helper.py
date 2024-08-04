import locale
import sys
import base64

def get_language():
    """ get shell language """
    if hasattr(locale, 'getdefaultlocale'):
        shell_lang, _ = locale.getdefaultlocale()
    else:
        shell_lang = locale.getdefaultlocale()[0]
    return shell_lang


if sys.version_info[0] > 2:
    # Python 3
    def encode_query(query_str):
        encoded_query = query_str.encode()
        encoded_query = base64.b64encode(encoded_query)
        return encoded_query.decode()
else:
    # Python 2
    def encode_query(query_str):
        encoded_query = base64.b64encode(query_str)
        return encoded_query


# import csv
# import xlsxwriter
#
# class CSVWriter:
#     def __init__(self, file_path):
#         self.file_path = file_path
#         self.file = open(file_path, 'w', newline='', encoding='utf-8')
#         self.writer = csv.writer(self.file)
#
#     def write_data(self, data):
#         self.writer.writerow(data)
#
#     def close_writer(self):
#         self.file.close()
#
#
# class XLSWriter:
#     def __init__(self, file_path):
#         self.file_path = file_path
#         self.workbook = xlsxwriter.Workbook(file_path)
#         self.worksheet = self.workbook.add_worksheet()
#         self.current_row = 0
#
#     def write_data(self, data):
#         self.worksheet.write_row(self.current_row, 0, data)
#         self.current_row += 1
#
#     def close_writer(self):
#         self.workbook.close()

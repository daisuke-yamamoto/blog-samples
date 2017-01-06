# coding: utf-8
import os
import csv
import openpyxl


def main():
    # ブックを読み込みます。
    filepath = os.path.join('data', 'test.xlsx')
    book = openpyxl.load_workbook(filepath, read_only=True, keep_vba=False)

    dest_dir = os.path.join('output', 'openpyxl_sample')
    os.makedirs(dest_dir, exist_ok=True)

    # シートでループ
    for sheet in book.worksheets:
        sheet_name = sheet.title  # シート名を取得
        dest_path = os.path.join(dest_dir, sheet_name + '.csv')

        with open(dest_path, 'w', encoding='utf-8') as fp:
            writer = csv.writer(fp)

            for cols in sheet.rows:
                writer.writerow([str(col.value or '') for col in cols])


if __name__ == '__main__':
    main()

import xlsxwriter
from sqlalchemy import text

workbook = xlsxwriter.Workbook('نتيجة الصف الأول الثانوي.xlsx')
worksheet = workbook.add_worksheet()

# Start from the first cell. Rows and columns are zero indexed.


def generate_excel(engine) -> None:
    row = 0
    col = 0

    with engine.connect() as con:
        query = "SELECT * FROM student"
        rs = con.execute(text(query))

        for item in (rs):

            worksheet.write(row, col, item.seating_num)
            worksheet.write(row, col + 1, item.code)
            worksheet.write(row, col + 2, item.full_name)
            worksheet.write(row, col + 3, item.general_grade)

            row += 1

    workbook.close()
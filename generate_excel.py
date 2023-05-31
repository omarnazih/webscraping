import xlsxwriter
from sqlalchemy import text

workbook = xlsxwriter.Workbook('نتيجة الصف الأول الثانوي.xlsx')
worksheet = workbook.add_worksheet()

# Start from the first cell. Rows and columns are zero indexed.
def generate_excel(engine) -> None:
    row = 0
    col = 0

    with engine.connect() as con:
        query = """SELECT *
                    FROM student
                    JOIN test_results ON student.id = test_results.student_id;"""
        rs = con.execute(text(query))

        for item in rs:
            worksheet.write(row, col, item[1])  # assuming seating_num is at index 1
            worksheet.write(row, col + 1, item[2])  # assuming code is at index 2
            worksheet.write(row, col + 2, item[3])  # assuming full_name is at index 3
            worksheet.write(row, col + 3, item[5])  # assuming general_grade is at index 5

            # Write test results (starting from index 6)
            for i in range(6, len(item)):
                worksheet.write(row, col + i, item[i])

            row += 1

    workbook.close()

import os
import sqlalchemy as db
from dotenv import load_dotenv
load_dotenv()

engine = db.create_engine(os.getenv('DATABASE_URI'))
generate_excel(engine)    
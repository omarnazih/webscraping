import sqlalchemy as db
from sqlalchemy import (MetaData, ForeignKey, Table, Column, Integer, String, Float, insert)

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

from dao import insert_item

meta = MetaData()

# driver = webdriver.Chrome('chromedriver.exe')
driver = webdriver.Chrome()
engine = db.create_engine('postgresql://ocgfzzrr:Mr3RM_g4ndeaOnDYoTlu9flI3nIZAZ0s@mouse.db.elephantsql.com/ocgfzzrr')

# Drop old Tables
meta.drop_all(engine)

student = Table(
    'student', meta,
    Column('id', Integer, primary_key = True),
    Column('seating_num', String),
    Column('code', String),
    Column('full_name', String),
    Column('nat_id', String),
    Column('general_grade', String)
)


test_results = Table(
    'test_results', meta,
    Column('id', Integer, primary_key = True),
    Column("student_id", ForeignKey("student.id"), nullable=False),
    Column('arabic', String),
    Column('english', String),
    Column('secondary_language', String),
    Column('math', String),
    Column('chemistry', String),
    Column('physics', String),
    Column('biology', String),
    Column('history', String),
    Column('philosophy', String),
    Column('geographic', String)
)

# Create Tables
meta.create_all(engine)

url = "http://madrasetna.com/NAT/SNTE.aspx"


driver.get(url)
driver.implicitly_wait(2) # Wait for page to load


# Locating and selecting Elements
dropdown1 = Select(driver.find_element(By.NAME, "DropDownList1")) #Select val = 10
dropdown1.select_by_visible_text('مشتول')

dropdown2 = Select(driver.find_element(By.NAME, "DropDownList2")) #Select val = 13026366
dropdown2.select_by_visible_text('كفر ابراش ث')

dropdown3 = Select(driver.find_element(By.NAME, "DropDownList3")) #Select val = A1
dropdown3.select_by_visible_text('أولى')


for i in range(1,500):
    driver.find_element(By.ID,"TextBox1").clear()
    driver.find_element(By.ID,"TextBox1").send_keys(i)
    driver.find_element(By.ID,"Button1").click()

    # Find First Table Data
    table_body1 = driver.find_element(By.XPATH, '//*[@id="GridView1"]/tbody')
    entries = table_body1.find_elements(By.TAG_NAME  ,'tr')
    col_data = entries[1].find_elements(By.TAG_NAME, 'td')


    stmt = insert(student).values(seating_num=col_data[0].text, code=col_data[1].text, full_name=col_data[2].text, nat_id=col_data[3].text, general_grade=col_data[4].text)

    compiled = stmt.compile()
    # print(compiled.params)

    student_id = insert_item(engine, stmt)

    # Find Second Table Data
    table_body = driver.find_element(By.XPATH, '//*[@id="GridView2"]/tbody')
    entries = table_body.find_elements(By.TAG_NAME  ,'tr')
    col_data = entries[1].find_elements(By.TAG_NAME, 'td')


    stmt = insert(test_results).values(student_id=1, arabic=col_data[0].text, english=col_data[1].text, secondary_language=col_data[2].text, math=col_data[3].text, chemistry=col_data[4].text, physics=col_data[5].text, biology=col_data[6].text, history=col_data[7].text, philosophy=col_data[8].text, geographic=col_data[9].text)

    compiled = stmt.compile()
    # print(compiled.params)

    insert_item(engine, stmt)



# Quitting and Clearing
driver.close()
driver.quit()


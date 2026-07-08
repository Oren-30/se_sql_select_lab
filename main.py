import sqlite3
import pandas as pd

# STEP 1A
# Import SQL Library and Pandas

# STEP 1B
# Connect to the database
conn = sqlite3.connect("data.sqlite")

# STEP 2
df_first_five = pd.read_sql("""
SELECT employeeNumber, lastName
FROM employees;
""", conn)

# STEP 3
df_five_reverse = pd.read_sql("""
SELECT lastName, employeeNumber
FROM employees;
""", conn)

# STEP 4
df_alias = pd.read_sql("""
SELECT
    employeeNumber AS ID,
    lastName
FROM employees;
""", conn)

# STEP 5
df_executive = pd.read_sql("""
SELECT
    employeeNumber,
    firstName,
    lastName,
    jobTitle,
    CASE
        WHEN jobTitle IN ('President', 'VP Sales', 'VP Marketing')
        THEN 'Executive'
        ELSE 'Not Executive'
    END AS role
FROM employees;
""", conn)

# STEP 6
df_name_length = pd.read_sql("""
SELECT
    LENGTH(lastName) AS name_length
FROM employees;
""", conn)

# STEP 7
df_short_title = pd.read_sql("""
SELECT
    SUBSTR(jobTitle, 1, 2) AS short_title
FROM employees;
""", conn)

# STEP 8
sum_total_price = pd.read_sql("""
SELECT
    ROUND(priceEach * quantityOrdered) AS total_price
FROM orderDetails;
""", conn).sum()

# STEP 9
df_day_month_year = pd.read_sql("""
SELECT
    orderDate,
    strftime('%d', orderDate) AS day,
    strftime('%m', orderDate) AS month,
    strftime('%Y', orderDate) AS year
FROM orders;
""", conn)

# Leave the connection open for the tests.
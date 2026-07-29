import sqlite3
import pandas as pd

# Connect
conn = sqlite3.connect("data.sqlite")


# STEP 2
df_first_five = pd.read_sql("""
SELECT employeeNumber, lastName
FROM employees
""", conn)


# STEP 3
df_five_reverse = pd.read_sql("""
SELECT lastName, employeeNumber
FROM employees
""", conn)


# STEP 4
df_alias = pd.read_sql("""
SELECT lastName, employeeNumber AS ID
FROM employees
""", conn)


# STEP 5
df_executive = pd.read_sql("""
SELECT 
    firstName,
    lastName,
    jobTitle,
    CASE
        WHEN jobTitle = 'President'
          OR jobTitle = 'VP Sales'
          OR jobTitle = 'VP Marketing'
        THEN 'Executive'
        ELSE 'Not Executive'
    END AS role
FROM employees
""", conn)


# STEP 6
df_name_length = pd.read_sql("""
SELECT LENGTH(lastName) AS name_length
FROM employees
""", conn)


# STEP 7
df_short_title = pd.read_sql("""
SELECT SUBSTR(jobTitle, 1, 2) AS short_title
FROM employees
""", conn)


# STEP 8
sum_total_price = pd.read_sql("""
SELECT ROUND(priceEach * quantityOrdered) AS total_price
FROM orderDetails
""", conn).sum()


# STEP 9
df_day_month_year = pd.read_sql("""
SELECT 
    orderDate,
    STRFTIME('%d', orderDate) AS day,
    STRFTIME('%m', orderDate) AS month,
    STRFTIME('%Y', orderDate) AS year
FROM orders
""", conn)


conn.close()





import sqlite3
import pandas as pd

# Connect database
conn = sqlite3.connect("data.sqlite")


# Part 1
df_boston = pd.read_sql("""
SELECT
    e.firstName,
    e.lastName,
    e.jobTitle
FROM employees e
JOIN offices o
ON e.officeCode = o.officeCode
WHERE o.city = 'Boston';
""", conn)



# Part 2
df_employee = pd.read_sql("""
SELECT
    e.firstName,
    e.lastName,
    o.city,
    o.state
FROM employees e
LEFT JOIN offices o
ON e.officeCode = o.officeCode
ORDER BY e.firstName, e.lastName;
""", conn)



# Part 3
df_payment = pd.read_sql("""
SELECT
    c.contactFirstName,
    c.contactLastName,
    p.amount,
    p.paymentDate
FROM customers c
JOIN payments p
ON c.customerNumber = p.customerNumber
ORDER BY CAST(p.amount AS DECIMAL) DESC;
""", conn)



# Part 4
df_credit = pd.read_sql("""
SELECT
    e.employeeNumber,
    e.firstName,
    e.lastName,
    COUNT(c.customerNumber) AS numcustomers
FROM employees e
JOIN customers c
ON e.employeeNumber = c.salesRepEmployeeNumber
GROUP BY
    e.employeeNumber,
    e.firstName,
    e.lastName
HAVING AVG(c.creditLimit) > 90000
ORDER BY numcustomers DESC;
""", conn)



# Part 5
df_total_customers = pd.read_sql("""
SELECT
    p.productName,
    p.productCode,
    COUNT(DISTINCT o.customerNumber) AS numpurchasers
FROM products p
JOIN orderdetails od
ON p.productCode = od.productCode
JOIN orders o
ON od.orderNumber = o.orderNumber
GROUP BY
    p.productCode,
    p.productName
ORDER BY numpurchasers DESC;
""", conn)



# Part 6
df_under_20 = pd.read_sql("""
SELECT DISTINCT
    e.employeeNumber,
    e.firstName,
    e.lastName,
    o.city,
    o.officeCode
FROM employees e
JOIN offices o
ON e.officeCode = o.officeCode
JOIN customers c
ON e.employeeNumber = c.salesRepEmployeeNumber
JOIN orders ord
ON c.customerNumber = ord.customerNumber
JOIN orderdetails od
ON ord.orderNumber = od.orderNumber
WHERE od.productCode IN
(
    SELECT productCode
    FROM orderdetails od2
    JOIN orders ord2
    ON od2.orderNumber = ord2.orderNumber
    GROUP BY productCode
    HAVING COUNT(DISTINCT ord2.customerNumber) < 20
);
""", conn)


# Leave connection open for pytest
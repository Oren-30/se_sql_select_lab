import sqlite3
import pandas as pd

# STEP 1
# Connect to database
conn = sqlite3.connect("data.sqlite")


# Part 1

# Return employees in Boston
df_boston_employees = pd.read_sql("""
SELECT
    e.firstName,
    e.lastName,
    e.jobTitle
FROM employees e
JOIN offices o
ON e.officeCode = o.officeCode
WHERE o.city = 'Boston';
""", conn)


# Offices with zero employees
df_empty_offices = pd.read_sql("""
SELECT
    o.officeCode,
    o.city,
    o.state
FROM offices o
LEFT JOIN employees e
ON o.officeCode = e.officeCode
WHERE e.employeeNumber IS NULL;
""", conn)



# Part 2

# All employees and their office information
df_employee_offices = pd.read_sql("""
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


# Customers without orders
df_customers_without_orders = pd.read_sql("""
SELECT
    c.contactFirstName,
    c.contactLastName,
    c.phone,
    c.salesRepEmployeeNumber
FROM customers c
LEFT JOIN orders o
ON c.customerNumber = o.customerNumber
WHERE o.orderNumber IS NULL
ORDER BY c.contactLastName;
""", conn)



# Part 3

# Customer payments
df_customer_payments = pd.read_sql("""
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

# Employees with customers average credit limit > 90000
df_credit_limit = pd.read_sql("""
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



# Product sales
df_product_sales = pd.read_sql("""
SELECT
    p.productName,
    COUNT(od.orderNumber) AS numorders,
    SUM(od.quantityOrdered) AS totalunits
FROM products p
JOIN orderdetails od
ON p.productCode = od.productCode
GROUP BY
    p.productCode,
    p.productName
ORDER BY totalunits DESC;
""", conn)



# Part 5

# Product customer reach
df_product_customers = pd.read_sql("""
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



# Customers per office
df_customers_per_office = pd.read_sql("""
SELECT
    COUNT(c.customerNumber) AS n_customers,
    o.officeCode,
    o.city
FROM offices o
JOIN employees e
ON o.officeCode = e.officeCode
JOIN customers c
ON e.employeeNumber = c.salesRepEmployeeNumber
GROUP BY
    o.officeCode,
    o.city;
""", conn)



# Part 6

# Employees selling products ordered by fewer than 20 customers
df_underperforming_products = pd.read_sql("""
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


# Keep connection open for tests
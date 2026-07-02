USE retail_business;

SELECT ROUND(SUM(sales), 2) AS total_sales FROM retail_sales;
SELECT ROUND(SUM(profit), 2) AS total_profit FROM retail_sales;
SELECT ROUND(AVG(sales), 2) AS average_sales FROM retail_sales;

SELECT product, ROUND(SUM(sales), 2) AS total_sales
FROM retail_sales
GROUP BY product
ORDER BY total_sales DESC
LIMIT 10;

SELECT customer, ROUND(SUM(sales), 2) AS total_sales
FROM retail_sales
GROUP BY customer
ORDER BY total_sales DESC
LIMIT 10;

SELECT order_month, ROUND(SUM(sales), 2) AS monthly_sales
FROM retail_sales
GROUP BY order_month
ORDER BY order_month;

SELECT region, ROUND(SUM(sales), 2) AS regional_sales
FROM retail_sales
GROUP BY region
ORDER BY regional_sales DESC;

SELECT category, ROUND(SUM(sales), 2) AS category_sales
FROM retail_sales
GROUP BY category
ORDER BY category_sales DESC;

SELECT category, ROUND(SUM(profit), 2) AS profit_by_category
FROM retail_sales
GROUP BY category
ORDER BY profit_by_category DESC;

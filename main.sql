-- Inventory Performance & Insight Analysis

-- Understand how many products are currently in the system
SELECT COUNT(*) AS total_products
FROM inventory;

-- Get a sense of overall stock availability across the business
SELECT SUM(stock_quantity) AS total_stock
FROM inventory;

-- Identify products that are running low and may need urgent restocking
SELECT 
    product_name,
    stock_quantity,
    reorder_level
FROM inventory
WHERE stock_quantity <= reorder_level;

-- Classify inventory health so the business can act faster
-- CRITICAL = immediate attention
-- LOW = monitor closely
-- OK = healthy stock level
SELECT 
    product_name,
    stock_quantity,
    CASE 
        WHEN stock_quantity <= reorder_level THEN 'CRITICAL'
        WHEN stock_quantity <= reorder_level * 2 THEN 'LOW'
        ELSE 'OK'
    END AS stock_status
FROM inventory;

-- Identify best-performing products based on actual customer demand
SELECT 
    i.product_name,
    SUM(s.quantity_sold) AS total_units_sold
FROM sales s
JOIN inventory i ON s.product_id = i.product_id
GROUP BY i.product_name
ORDER BY total_units_sold DESC;

-- Understand which product categories are driving the most sales
SELECT 
    i.category,
    SUM(s.quantity_sold) AS total_units_sold
FROM sales s
JOIN inventory i ON s.product_id = i.product_id
GROUP BY i.category
ORDER BY total_units_sold DESC;

-- Estimate how long each product will last based on current sales trends
-- This helps predict potential stockouts before they happen
SELECT 
    i.product_name,
    i.stock_quantity,
    AVG(s.quantity_sold) AS avg_daily_sales,
    i.stock_quantity / NULLIF(AVG(s.quantity_sold), 0) AS days_until_stockout
FROM inventory i
JOIN sales s ON i.product_id = s.product_id
GROUP BY i.product_name, i.stock_quantity;

-- =========================================
-- BASIC DATA VALIDATION
-- =========================================

SELECT COUNT(*) AS total_applications FROM applications;
SELECT COUNT(*) AS total_vehicles FROM vehicles;
SELECT COUNT(*) AS total_compatibility FROM compatibility;


-- =========================================
-- SAMPLE JOINS
-- =========================================

SELECT a.headline, v.model_name
FROM applications a
JOIN compatibility c ON a.app_id = c.app_id
JOIN vehicles v ON c.vehicle_id = v.id
LIMIT 10;


-- =========================================
-- AGGREGATIONS
-- =========================================

SELECT v.manufacturer_name, COUNT(*) AS part_count
FROM vehicles v
JOIN compatibility c ON v.id = c.vehicle_id
GROUP BY v.manufacturer_name
ORDER BY part_count DESC
LIMIT 10;


-- =========================================
-- BUSINESS-STYLE QUESTIONS
-- =========================================

-- Which categories have the most listings?
SELECT pc.category_name, COUNT(*) AS total_listings
FROM applications a
JOIN product_category pc ON a.category_id = pc.id
GROUP BY pc.category_name
ORDER BY total_listings DESC
LIMIT 10;

-- Average price per category
SELECT pc.category_name, AVG(a.price_usd) AS avg_price
FROM applications a
JOIN product_category pc ON a.category_id = pc.id
GROUP BY pc.category_name
ORDER BY avg_price DESC;
-- VERIFY DATA QUALITY
SELECT
    COUNT(*) AS total_rows,
    COUNT(Booking_Value) AS non_null_booking_value,
    COUNT(Ride_Distance) AS non_null_ride_distance
FROM ola_rides_clean;

-- SQL QUESTIONS – ANSWERS

-- 1. Retrieve all successful bookings
SELECT *
FROM ola_rides_clean
WHERE Booking_Status = 'Success'
ORDER BY Date, Time ASC;

-- 2️. Average ride distance for each vehicle type
SELECT 
    Vehicle_Type,
    CAST(AVG(CAST(Ride_Distance AS DECIMAL(10,2))) AS DECIMAL(10,2)) AS avg_ride_distance
FROM ola_rides_clean
WHERE Ride_Distance <> 0
GROUP BY Vehicle_Type
ORDER BY avg_ride_distance DESC;

-- 3. Total number of cancelled rides by customers
SELECT 
    COUNT(*) AS total_customer_cancellations
FROM ola_rides_clean
WHERE Canceled_Rides_by_Customer <> 'null';

-- 4. Top 5 customers with highest number of bookings
SELECT TOP 5
    Customer_ID,
    COUNT(Booking_ID) AS total_bookings
FROM ola_rides_clean
GROUP BY Customer_ID
ORDER BY total_bookings DESC;

-- 5. Rides cancelled by drivers due to personal or car issues
SELECT 
    COUNT(*) AS driver_cancellations
FROM ola_rides
WHERE 
    Canceled_Rides_by_Driver <> 'null'
    AND Incomplete_Rides_Reason IN ('Vehicle Breakdown');

-- 6. Max & Min driver ratings for Prime Sedan
SELECT 
    MAX(Driver_Ratings) AS max_driver_rating,
    MIN(Driver_Ratings) AS min_driver_rating
FROM ola_rides_clean
WHERE 
    Vehicle_Type = 'Prime Sedan';

-- 7. Rides paid using UPI
SELECT *
FROM ola_rides_clean
WHERE Payment_Method = 'UPI'
ORDER BY Date, Time ASC;

-- 8. Average customer rating per vehicle type
SELECT 
    Vehicle_Type,
    CAST(AVG(CAST(Customer_Rating AS DECIMAL(10,2))) AS DECIMAL(10,2)) AS avg_customer_rating
FROM ola_rides_clean
GROUP BY Vehicle_Type
ORDER BY avg_customer_rating DESC;

-- 9. Total booking value of successfully completed rides
SELECT 
    FORMAT(ROUND(SUM(CAST(Booking_Value AS DECIMAL(10,2))) / 1000000, 2), 'N2') + ' M' AS total_revenue
FROM ola_rides_clean
WHERE 
    Booking_Status = 'Success';

-- 10. Incomplete rides along with the reason
SELECT 
    Booking_ID,
    Incomplete_Rides_Reason
FROM ola_rides
WHERE Incomplete_Rides = 'Yes';











-- CREATE CLEAN ANALYTICS TABLE
CREATE TABLE ola_rides_clean (
    Date DATE,
    Time TIME(0),
    Booking_ID VARCHAR(50) PRIMARY KEY,
    Booking_Status VARCHAR(20),
    Customer_ID VARCHAR(50),
    Vehicle_Type VARCHAR(30),
    Pickup_Location VARCHAR(100),
    Drop_Location VARCHAR(100),

    V_TAT INT NULL,
    C_TAT INT NULL,

    Canceled_Rides_by_Customer VARCHAR(100),
    Canceled_Rides_by_Driver VARCHAR(100),

    Incomplete_Rides BIT NULL,
    Incomplete_Rides_Reason VARCHAR(100),

    Booking_Value DECIMAL(10,2) NULL,
    Payment_Method VARCHAR(20),
    Ride_Distance DECIMAL(6,2) NULL,

    Driver_Ratings DECIMAL(2,1) NULL,
    Customer_Rating DECIMAL(2,1) NULL
);

-- TRANSFORM & LOAD DATA
INSERT INTO ola_rides_clean
SELECT
    Date,
    Time,
    Booking_ID,
    Booking_Status,
    Customer_ID,
    Vehicle_Type,
    Pickup_Location,
    Drop_Location,

    CASE WHEN CAST(V_TAT AS NVARCHAR(20)) = 'null' THEN NULL ELSE V_TAT END,
    CASE WHEN CAST(C_TAT AS NVARCHAR(20)) = 'null' THEN NULL ELSE C_TAT END,

    Canceled_Rides_by_Customer,
    Canceled_Rides_by_Driver,
    
    CASE 
        WHEN Incomplete_Rides = 'Yes' THEN 1
        WHEN Incomplete_Rides = 'No' THEN 0
        ELSE NULL
    END,

    Incomplete_Rides_Reason,

    CASE 
        WHEN CAST(Booking_Value AS NVARCHAR(50)) = 'null' THEN NULL 
        ELSE Booking_Value 
    END,

    Payment_Method,

    CASE 
        WHEN CAST(Ride_Distance AS NVARCHAR(20)) = 'null' THEN NULL 
        ELSE Ride_Distance 
    END,

    CASE 
        WHEN CAST(Driver_Ratings AS NVARCHAR(10)) = 'null' THEN NULL 
        ELSE Driver_Ratings 
    END,

    CASE 
        WHEN CAST(Customer_Rating AS NVARCHAR(10)) = 'null' THEN NULL 
        ELSE Customer_Rating 
    END
FROM ola_rides;


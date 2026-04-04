-- PRODUCT CATEGORY
CREATE TABLE product_category (
    id INT PRIMARY KEY,
    category_name VARCHAR(255) NOT NULL
);

-- SELLER
CREATE TABLE seller (
    id INT PRIMARY KEY,
    seller_name VARCHAR(255) NOT NULL
);

-- APPLICATION STATUS
CREATE TABLE application_status (
    id INT PRIMARY KEY,
    status_name VARCHAR(255) NOT NULL
);

-- VEHICLE TYPE
CREATE TABLE vehicle_type (
    id INT PRIMARY KEY,
    vehicle_type_name VARCHAR(255) NOT NULL
);

-- VEHICLES
CREATE TABLE vehicles (
    id INT PRIMARY KEY,
    model_name VARCHAR(255) NOT NULL,
    manufacturer_name VARCHAR(255) NOT NULL,
    vehicle_type_id INT NOT NULL,
    FOREIGN KEY (vehicle_type_id) REFERENCES vehicle_type(id)
);

-- APPLICATIONS
CREATE TABLE applications (
    app_id BIGINT PRIMARY KEY,
    headline VARCHAR(255) NOT NULL,
    price_usd FLOAT NOT NULL,
    category_id INT NOT NULL,
    seller_id INT NOT NULL,
    status_id INT NOT NULL,
    vehicle_type_id INT NOT NULL,
    in_stock INT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES product_category(id),
    FOREIGN KEY (seller_id) REFERENCES seller(id),
    FOREIGN KEY (status_id) REFERENCES application_status(id),
    FOREIGN KEY (vehicle_type_id) REFERENCES vehicle_type(id)
);

-- COMPATIBILITY (bridge table)
CREATE TABLE compatibility (
    app_id BIGINT NOT NULL,
    vehicles_id INT NOT NULL,
    bottom_year INT,
    top_year INT,
    PRIMARY KEY (app_id, vehicles_id),
    FOREIGN KEY (app_id) REFERENCES applications(app_id),
    FOREIGN KEY (vehicles_id) REFERENCES vehicles(id)
);
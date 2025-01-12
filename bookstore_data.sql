CREATE DATABASE BOOKSTORE;
USE BOOKSTORE;

-- Create customer table
CREATE TABLE customer (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(20) NOT NULL,
    password VARCHAR(20) NOT NULL,
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    house_num INT NOT NULL,
    street VARCHAR(20) NOT NULL,
    city VARCHAR(20) NOT NULL,
    country VARCHAR(20) NOT NULL,
    age INT NOT NULL,
    gender VARCHAR(20) NOT NULL,
    login_status VARCHAR(20) NOT NULL,
    wallet DECIMAL(10,2),
    customer_status VARCHAR(20) NOT NULL
);

-- Create customer_phone table
CREATE TABLE customer_phone (
    cust_user_id INT,
    phone_num INT,
    PRIMARY KEY (cust_user_id, phone_num)
);

ALTER TABLE customer_phone
modify phone_num BIGINT;

CREATE TABLE gifts (
	send_user_id INT,
    recv_user_id INT,
	PRIMARY KEY (send_user_id, recv_user_id)
);

-- Create offers table
CREATE TABLE offers (
    offer_id INT PRIMARY KEY NOT NULL,
    description VARCHAR(100) NOT NULL
);

-- Create apply table
CREATE TABLE apply (
    cust_id INT,
    offer_id INT,
    PRIMARY KEY (cust_id, offer_id)
);

-- Create cart table
CREATE TABLE cart (
    cust_cart_id INT,
    date DATE,
    time TIME,
    num_items INT,
    total_amount DECIMAL(10,2),
    PRIMARY KEY (cust_cart_id, date, time)
);

-- Create history table
CREATE TABLE history (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    cart_id INT NOT NULL,
    date DATE NOT NULL,
    time TIME NOT NULL,
    cust_viewed INT
);

-- Create accounts table
CREATE TABLE accounts (
    account_type VARCHAR(20) NOT NULL,
    account_date DATE NOT NULL,
    amount INT NOT NULL,
    order_refund_id INT,
    payer_id INT,
    shipper_payee_id INT,
    publisher_payee VARCHAR(20),
    PRIMARY KEY (account_type, account_date)
);

-- Create shipper table
CREATE TABLE shipper (
    shipper_id INT PRIMARY KEY NOT NULL,
    live_location VARCHAR(20) NOT NULL,
    date_of_delivery DATE NOT NULL,
    order_id INT NOT NULL,
    cust_to_ship INT 
);

-- Create book table
CREATE TABLE book (
    ISBN INT PRIMARY KEY NOT NULL,
    status VARCHAR(20) NOT NULL,
    availability VARCHAR(20) NOT NULL,
    edition INT NOT NULL,
    language VARCHAR(20) NOT NULL,
    title VARCHAR(20) NOT NULL,
    rating VARCHAR(20) NOT NULL DEFAULT '0',
    publisher_name VARCHAR(20) NOT NULL,
    cart_cust_id INT,
    date DATE,
    time TIME,
    author_id INT NOT NULL,
    price INT DEFAULT 100,
    number_of_copies INT DEFAULT 5
);

ALTER TABLE book 
MODIFY title VARCHAR(50);

-- Create table Book_genre
CREATE TABLE book_genre (
	ISBN INT,
    type VARCHAR(20),
    PRIMARY KEY (ISBN, type)
);

-- Create search_view_rate table
CREATE TABLE search_view_rate (
    cust_id INT,
    ISBN INT,
    PRIMARY KEY (cust_id, ISBN)
);

-- Create table reviews
CREATE TABLE reviews (
	book_isbn INT,
    date DATE,
    time TIME,
    description VARCHAR(50),
    PRIMARY KEY (book_isbn, date, time)
);

-- Create author table
CREATE TABLE author (
    login_id VARCHAR(20) PRIMARY KEY NOT NULL,
    password VARCHAR(20) NOT NULL DEFAULT 'password',
    name VARCHAR(20) NOT NULL ,
    status VARCHAR(20) NOT NULL DEFAULT 'Active'
);

ALTER TABLE author 
MODIFY login_id INT ;

-- Create publisher table
CREATE TABLE publisher (
    company_name VARCHAR(20) PRIMARY KEY NOT NULL,
    warehouse_zip INT NOT NULL,
    agrrement_terms VARCHAR(20) NOT NULL DEFAULT 'Standard'
);

-- Create Royalty table
CREATE TABLE royalty (
	ISBN INT PRIMARY KEY,
    author_id INT NOT NULL,
    account_type VARCHAR(20),
    account_date VARCHAR(20)
);

ALTER TABLE royalty
MODIFY account_date DATE;

SHOW TABLES;
-- Add foreign key constraints using ALTER TABLE

ALTER TABLE customer_phone
ADD FOREIGN KEY (cust_user_id) REFERENCES customer(user_id);

ALTER TABLE gifts
ADD FOREIGN KEY (send_user_id) REFERENCES customer(user_id),
ADD FOREIGN KEY (recv_user_id) REFERENCES customer(user_id);

ALTER TABLE apply
ADD FOREIGN KEY (cust_id) REFERENCES customer(user_id),
ADD FOREIGN KEY (offer_id) REFERENCES offers(offer_id);

ALTER TABLE cart
ADD FOREIGN KEY (cust_cart_id) REFERENCES customer(user_id) ON DELETE CASCADE;

ALTER TABLE history
ADD FOREIGN KEY (cust_viewed) REFERENCES customer(user_id),
ADD FOREIGN KEY (cart_id, date, time) REFERENCES cart(cust_cart_id, date, time);

ALTER TABLE shipper
ADD FOREIGN KEY (order_id) REFERENCES history(transaction_id),
ADD FOREIGN KEY (cust_to_ship) REFERENCES customer(user_id);

ALTER TABLE accounts
ADD FOREIGN KEY (order_refund_id) REFERENCES history(transaction_id),
ADD FOREIGN KEY (payer_id) REFERENCES customer(user_id),
ADD FOREIGN KEY (shipper_payee_id) REFERENCES shipper(shipper_id),
ADD FOREIGN KEY (publisher_payee) REFERENCES publisher(company_name);

ALTER TABLE book
ADD FOREIGN KEY (cart_cust_id, date, time) REFERENCES cart(cust_cart_id, date, time),
ADD FOREIGN KEY (publisher_name) REFERENCES publisher(company_name),
ADD FOREIGN KEY (author_id) REFERENCES author(login_id);

ALTER TABLE search_view_rate
ADD FOREIGN KEY (cust_id) REFERENCES customer(user_id),
ADD FOREIGN KEY (ISBN) REFERENCES book(ISBN);

ALTER TABLE book_genre
ADD FOREIGN KEY (ISBN) REFERENCES book(ISBN);

ALTER TABLE reviews
ADD FOREIGN KEY (book_isbn) REFERENCES book(ISBN);

ALTER TABLE royalty
ADD FOREIGN KEY (ISBN) REFERENCES book(ISBN),
ADD FOREIGN KEY (author_id) REFERENCES author(login_id),
ADD FOREIGN KEY (account_type, account_date) REFERENCES accounts(account_type, account_date);

-- POPULATING THE DATABASE

-- Insert data into customer table
USE BOOKSTORE;
INSERT INTO customer (username, password, first_name, last_name, house_num, street, city, country, age, gender, login_status, wallet, customer_status)
VALUES
('john_doe', 'password1', 'John', 'Doe', 101, 'Main St', 'New York', 'USA', 30, 'Male', 'Inactive', 150.50, 'Regular'),
('jane_smith', 'password2', 'Jane', 'Smith', 102, 'Oak St', 'Los Angeles', 'USA', 25, 'Female', 'Inactive', 200.75, 'Premium'),
('alice_w', 'password3', 'Alice', 'White', 103, 'Pine St', 'Chicago', 'USA', 27, 'Female', 'Inactive', 50.00, 'Regular'),
('bob_j', 'password4', 'Bob', 'Johnson', 104, 'Elm St', 'Houston', 'USA', 35, 'Male', 'Inactive', 300.00, 'Premium'),
('charlie_b', 'password5', 'Charlie', 'Brown', 105, 'Ash St', 'Phoenix', 'USA', 28, 'Male', 'Inactive', 120.00, 'Regular'),
('daisy_m', 'password6', 'Daisy', 'Miller', 106, 'Cedar St', 'Philadelphia', 'USA', 22, 'Female', 'Inactive', 80.25, 'Regular'),
('eric_k', 'password7', 'Eric', 'King', 107, 'Birch St', 'San Diego', 'USA', 40, 'Male', 'Inactive', 175.00, 'Premium'),
('fiona_g', 'password8', 'Fiona', 'Green', 108, 'Maple St', 'Dallas', 'USA', 32, 'Female', 'Inactive', 220.30, 'Premium'),
('george_p', 'password9', 'George', 'Parker', 109, 'Spruce St', 'Austin', 'USA', 36, 'Male', 'Inactive', 180.90, 'Regular'),
('helen_t', 'password10', 'Helen', 'Taylor', 110, 'Willow St', 'San Jose', 'USA', 29, 'Female', 'Inactive', 90.00, 'Regular');

-- Insert data into customer_phone table
INSERT INTO customer_phone (cust_user_id, phone_num)
VALUES
(1, 1234567890),
(2, 2345678901),
(3, 3456789012),
(4, 4567890123),
(5, 5678901234),
(6, 6789012345),
(7, 7890123456),
(8, 8901234567),
(9, 9012345678),
(10, 9123456789);

-- Insert data into gifts table
INSERT INTO gifts (send_user_id, recv_user_id)
VALUES
(1, 2),
(2, 3),
(3, 4),
(4, 5),
(5, 6),
(6, 7),
(7, 8),
(8, 9),
(9, 10),
(10, 1);

-- Insert data into offers table
INSERT INTO offers (offer_id, description)
VALUES
(1, '10% off on first purchase'),
(2, 'Buy 2 Get 1 Free'),
(3, 'Free shipping on orders over $50'),
(4, '20% off on next purchase'),
(5, 'Loyalty points offer'),
(6, 'Black Friday Sale'),
(7, 'Cyber Monday Discount'),
(8, 'Holiday Special Discount'),
(9, 'Student Discount'),
(10, 'Exclusive Premium Offer');

-- Insert data into apply table
INSERT INTO apply (cust_id, offer_id)
VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(10, 10);

-- Insert data into cart table
INSERT INTO cart (cust_cart_id, date, time, num_items, total_amount)
VALUES
(1, '2024-11-01', '10:00:00', 3, 45.75),
(2, '2024-11-02', '11:15:00', 2, 30.50),
(3, '2024-11-03', '14:30:00', 1, 15.00),
(4, '2024-11-04', '16:45:00', 4, 60.00),
(5, '2024-11-05', '18:00:00', 5, 75.25),
(6, '2024-11-06', '19:15:00', 2, 40.00),
(7, '2024-11-07', '20:30:00', 6, 100.00),
(8, '2024-11-08', '21:45:00', 3, 50.00),
(9, '2024-11-09', '22:00:00', 4, 85.00),
(10, '2024-11-10', '23:15:00', 7, 120.50);

-- Insert data into history table
INSERT INTO history (transaction_id, cart_id, date, time, cust_viewed)
VALUES
(1, 1, '2024-11-01', '10:00:00', 1),
(2, 2, '2024-11-02', '11:15:00', 2),
(3, 3, '2024-11-03', '14:30:00', 3),
(4, 4, '2024-11-04', '16:45:00', 4),
(5, 5, '2024-11-05', '18:00:00', 5),
(6, 6, '2024-11-06', '19:15:00', 6),
(7, 7, '2024-11-07', '20:30:00', 7),
(8, 8, '2024-11-08', '21:45:00', 8),
(9, 9, '2024-11-09', '22:00:00', 9),
(10, 10, '2024-11-10', '23:15:00', 10);

-- Insert data into shipper table
INSERT INTO shipper (shipper_id, live_location, date_of_delivery, order_id, cust_to_ship)
VALUES
(1, 'New York', '2024-11-02', 1, 1),
(2, 'Los Angeles', '2024-11-03', 2, 2),
(3, 'Chicago', '2024-11-04', 3, 3),
(4, 'Houston', '2024-11-05', 4, 4),
(5, 'Phoenix', '2024-11-06', 5, 5),
(6, 'Philadelphia', '2024-11-07', 6, 6),
(7, 'San Diego', '2024-11-08', 7, 7),
(8, 'Dallas', '2024-11-09', 8, 8),
(9, 'Austin', '2024-11-10', 9, 9),
(10, 'San Jose', '2024-11-11', 10, 10);

-- Insert data into publisher table
INSERT INTO publisher (company_name, warehouse_zip, agrrement_terms)
VALUES
('Pearson', 10001, 'Standard'),
('McGrawHill', 90001, 'Premium'),
('OReilly', 60601, 'Standard'),
('Packt', 77001, 'Standard'),
('Manning', 85001, 'Premium'),
('Wiley', 19101, 'Standard'),
('Springer', 92101, 'Premium'),
('NoStarch', 75201, 'Standard');

-- Insert data into accounts table
INSERT INTO accounts (account_type, account_date, amount, order_refund_id, payer_id, shipper_payee_id, publisher_payee)
VALUES
('Order Payment', '2024-11-01', 100, 1, 1, 1, 'Pearson'),
('Order Refund', '2024-11-02', 50, 2, 2, 2, 'McGrawHill'),
('Shipper Payment', '2024-11-03', 75, 3, 3, 3, 'OReilly'),
('Order Payment', '2024-11-04', 150, 4, 4, 4, 'Packt'),
('Order Refund', '2024-11-05', 80, 5, 5, 5, 'Manning'),
('Shipper Payment', '2024-11-06', 90, 6, 6, 6, 'Wiley'),
('Order Payment', '2024-11-07', 120, 7, 7, 7, 'Springer'),
('Order Refund', '2024-11-08', 60, 8, 8, 8, 'NoStarch'),
('Shipper Payment', '2024-11-09', 110, 9, 9, 9, 'OReilly'),
('Order Payment', '2024-11-10', 140, 10, 10, 10, 'Packt');

-- Insert data into accounts table with 'Royalty' and other columns as NULL
INSERT INTO accounts (account_type, account_date, amount, order_refund_id, payer_id, shipper_payee_id, publisher_payee)
VALUES
('Royalty', '2024-11-11', 200, NULL, NULL, NULL, NULL),
('Royalty', '2024-11-12', 250, NULL, NULL, NULL, NULL),
('Royalty', '2024-11-13', 300, NULL, NULL, NULL, NULL),
('Royalty', '2024-11-14', 350, NULL, NULL, NULL, NULL),
('Royalty', '2024-11-15', 400, NULL, NULL, NULL, NULL),
('Royalty', '2024-11-16', 450, NULL, NULL, NULL, NULL),
('Royalty', '2024-11-17', 500, NULL, NULL, NULL, NULL),
('Royalty', '2024-11-18', 550, NULL, NULL, NULL, NULL),
('Royalty', '2024-11-19', 600, NULL, NULL, NULL, NULL),
('Royalty', '2024-11-20', 650, NULL, NULL, NULL, NULL);

-- Insert data into author table
INSERT INTO author (login_id, password, name, status)
VALUES
(1, 'auth1pass', 'C. J. Date', 'Active'),
(2, 'auth2pass', 'Andrew S. Tanenbaum', 'Active'),
(3, 'auth3pass', 'Ian Goodfellow', 'Active'),
(4, 'auth4pass', 'Yann LeCun', 'Active'),
(5, 'auth5pass', 'Stuart Russell', 'Active'),
(6, 'auth6pass', 'Kurose Ross', 'Inactive'),
(7, 'auth7pass', 'John Hennessy', 'Active'),
(8, 'auth8pass', 'Rajkumar Buyya', 'Active'),
(9, 'auth9pass', 'Satoshi Nakamoto', 'Inactive'),
(10, 'auth10pass', 'Bruce Schneier', 'Active');

-- Insert data into book table
INSERT INTO book (ISBN, status, availability, edition, language, title, rating, publisher_name, cart_cust_id, date, time, author_id, price)
VALUES
(101, 'New', 'Available', 1, 'English', 'Database Systems', '4.5', 'Pearson', 1, '2024-11-01', '10:00:00', 1, 100),
(102, 'Used', 'Available', 2, 'English', 'Operating Systems', '4.0', 'McGrawHill', 2, '2024-11-02', '11:15:00', 2, 150),
(103, 'New', 'Available', 3, 'French', 'Machine Learning', '4.8', 'OReilly', 3, '2024-11-03', '14:30:00', 3, 200),
(104, 'Used', 'Available', 4, 'Spanish', 'Deep Learning', '4.7', 'Packt', 4, '2024-11-04', '16:45:00', 4, 500 ),
(105, 'New', 'Available', 5, 'English', 'Artificial Intelligence', '4.9', 'Manning', 5, '2024-11-05', '18:00:00', 5, 400),
(106, 'New', 'Available', 6, 'German', 'Networks', '4.3', 'Wiley', 6, '2024-11-06', '19:15:00', 6, 600),
(107, 'Used', 'Available', 7, 'English', 'Computer Architecture', '4.6', 'Springer', 7, '2024-11-07', '20:30:00', 7, 1000),
(108, 'New', 'Available', 8, 'English', 'Cloud Computing', '4.4', 'NoStarch', 8, '2024-11-08', '21:45:00', 8, 400),
(109, 'New', 'Available', 9, 'English', 'Blockchain Basics', '4.2', 'Packt', 9, '2024-11-09', '22:00:00', 9, 800),
(110, 'Used', 'Available', 10, 'English', 'Cryptography', '4.1', 'Pearson', 10, '2024-11-10', '23:15:00', 10, 900);

-- Insert data into book_genre table
INSERT INTO book_genre (ISBN, type)
VALUES
(101, 'Educational'),
(102, 'Technical'),
(103, 'AI'),
(104, 'AI'),
(105, 'AI'),
(106, 'Networking'),
(107, 'Hardware'),
(108, 'Cloud'),
(109, 'Blockchain'),
(110, 'Security');

-- Insert data into search_view_rate table
INSERT INTO search_view_rate (cust_id, ISBN)
VALUES
(1, 101),
(2, 102),
(3, 103),
(4, 104),
(5, 105),
(6, 106),
(7, 107),
(8, 108),
(9, 109),
(10, 110);

-- Insert data into reviews table
INSERT INTO reviews (book_isbn, date, time, description)
VALUES
(101, '2024-11-01', '10:15:00', 'Excellent book on databases!'),
(102, '2024-11-02', '11:45:00', 'Very helpful for OS concepts.'),
(103, '2024-11-03', '14:50:00', 'Great introduction to ML.'),
(104, '2024-11-04', '17:00:00', 'Informative on DL topics.'),
(105, '2024-11-05', '18:30:00', 'Comprehensive coverage on AI.'),
(106, '2024-11-06', '19:45:00', 'Networking explained clearly.'),
(107, '2024-11-07', '20:50:00', 'Detailed architecture concepts.'),
(108, '2024-11-08', '22:00:00', 'Cloud technologies demystified.'),
(109, '2024-11-09', '22:30:00', 'Basic guide to blockchain.'),
(110, '2024-11-10', '23:30:00', 'Useful for cryptography beginners.');

-- Insert data into royalty table
-- INSERT INTO royalty (ISBN, author_id, account_type, account_date)
-- VALUES
-- (101, 1, 'Royalty', '2024-11-11'),  -- C. J. Date, Database Systems
-- (102, 2, 'Royalty', '2024-11-12'),  -- Andrew S. Tanenbaum, Operating Systems
-- (103, 3, 'Royalty', '2024-11-13'),  -- Ian Goodfellow, Machine Learning
-- (104, 4, 'Royalty', '2024-11-14'),  -- Yann LeCun, Deep Learning
-- (105, 5, 'Royalty', '2024-11-15'),  -- Stuart Russell, Artificial Intelligence
-- (106, 6, 'Royalty', '2024-11-16'),  -- Kurose Ross, Networks
-- (107, 7, 'Royalty', '2024-11-17'),  -- John Hennessy, Computer Architecture
-- (108, 8, 'Royalty', '2024-11-18'),  -- Rajkumar Buyya, Cloud Computing
-- (109, 9, 'Royalty', '2024-11-19'),  -- Satoshi Nakamoto, Blockchain Basics
-- (110, 10, 'Royalty', '2024-11-20');  -- Bruce Schneier, Cryptography

SELECT * FROM CUSTOMER;
SELECT * FROM BOOK;	
SELECT * FROM PUBLISHER;
SELECT * FROM AUTHOR;
select * from search_view_rate;
select * from cart;
select * from history;
select * from royalty;

DELETE FROM rentals;
DELETE FROM books;
DELETE FROM users;

ALTER SEQUENCE rentals_id_seq RESTART WITH 1;
ALTER SEQUENCE books_id_seq RESTART WITH 1;
ALTER SEQUENCE users_id_seq RESTART WITH 1;

INSERT INTO users(name, email, created_at)
VALUES
('Kim', 'kim@test.com', CURRENT_TIMESTAMP),
('Lee', 'lee@test.com', CURRENT_TIMESTAMP),
('Park', 'park@test.com', CURRENT_TIMESTAMP);

INSERT INTO books(title, author, stock, created_at)
VALUES
('Database', 'Hong', 3, CURRENT_TIMESTAMP),
('Operating System', 'Kim', 5, CURRENT_TIMESTAMP),
('Computer Network', 'Andrew Tanenbaum', 4, CURRENT_TIMESTAMP),
('Data Structure', 'Mark Allen Weiss', 2, CURRENT_TIMESTAMP),
('Algorithm', 'Thomas Cormen', 3, CURRENT_TIMESTAMP);

INSERT INTO rentals(user_id, book_id, rental_date, return_date, status)
VALUES
(
    1,
    1,
    CURRENT_TIMESTAMP - INTERVAL '10 days',
    CURRENT_TIMESTAMP - INTERVAL '7 days',
    'RETURNED'
),
(
    2,
    3,
    CURRENT_TIMESTAMP - INTERVAL '5 days',
    NULL,
    'RENTED'
),
(
    3,
    5,
    CURRENT_TIMESTAMP - INTERVAL '2 days',
    NULL,
    'RENTED'
);
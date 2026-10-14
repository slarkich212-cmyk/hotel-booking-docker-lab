CREATE TABLE reservations (
    id SERIAL PRIMARY KEY,
    guest_name VARCHAR(100),
    check_in DATE,
    check_out DATE,
    room_number INT,
    price_per_night NUMERIC(10, 2)
);

INSERT INTO reservations (guest_name, check_in, check_out, room_number, price_per_night)
VALUES 
('Иван Иванов', '2026-10-10', '2026-10-15', 101, 5000.00),
('Мария Петрова', '2026-11-01', '2026-11-05', 202, 7500.00),
('Алексей Смирнов', '2026-12-20', '2026-12-25', 305, 10000.00);
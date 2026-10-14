from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST', 'db'),
        database=os.environ.get('DB_NAME', 'hoteldb'),
        user=os.environ.get('DB_USER', 'postgres'),
        password=os.environ.get('DB_PASSWORD', 'postgres')
    )
    return conn

@app.route('/api/reservations')
def get_reservations():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, guest_name, check_in, check_out, room_number, price_per_night FROM reservations;')
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    reservations_list = []
    for row in rows:
        reservations_list.append({
            'id': row[0],
            'guest_name': row[1],
            'check_in': str(row[2]),
            'check_out': str(row[3]),
            'room_number': row[4],
            'price_per_night': float(row[5])
        })
    return jsonify(reservations_list)

@app.route('/api/calculate/<int:reservation_id>')
def calculate_price(reservation_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        'SELECT check_in, check_out, price_per_night FROM reservations WHERE id = %s;',
        (reservation_id,)
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    
    if not row:
        return jsonify({'error': 'Бронирование не найдено'}), 404
    
    check_in = row[0]
    check_out = row[1]
    price_per_night = float(row[2])
    
    nights = (check_out - check_in).days
    total_price = nights * price_per_night
    
    return jsonify({
        'reservation_id': reservation_id,
        'check_in': str(check_in),
        'check_out': str(check_out),
        'nights': nights,
        'price_per_night': price_per_night,
        'total_price': total_price
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
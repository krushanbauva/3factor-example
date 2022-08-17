from flask import Flask, request, jsonify
import psycopg2
import json
import random
import os

app = Flask(__name__)

def get_db_connection():
  connection_string = os.environ["PSQL_CONN_STR"]
  conn = psycopg2.connect(connection_string)
  return conn

def restaurant_approval(cur, order_id):
  sql = "UPDATE orders SET approved = %s WHERE order_id = %s"
  cur.execute(sql, (True, order_id))

def assign_driver(cur, order_id):
  drivers = [95, 96, 97, 98, 99]
  driver_id = random.choice(drivers)
  sql1 = "INSERT INTO assignment (order_id, driver_id) VALUES (%s, %s)"
  cur.execute(sql1, (order_id, driver_id))
  sql2 = "UPDATE orders SET driver_assigned = %s WHERE order_id = %s"
  cur.execute(sql2, (True, order_id))

@app.route('/driverAssignment', methods=['POST'])
def driverAssignment():
  json_data = request.get_json()
  order_id = json_data["event"]["data"]["old"]["order_id"]
  payment_status = json_data["event"]["data"]["new"]["payment_valid"]
  conn = get_db_connection()
  cur = conn.cursor()
  if payment_status:
    restaurant_approval(cur, order_id)
    assign_driver(cur, order_id)
  cur.close()
  conn.commit()
  conn.close()
  return order_id

if __name__ == '__main__':
  app.run(debug = True, host = '0.0.0.0')
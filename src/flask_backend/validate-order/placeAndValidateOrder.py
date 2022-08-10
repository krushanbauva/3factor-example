from ast import arg
from re import I
from placeAndValidateOrderTypes import placeAndValidateOrderArgs, validatedResponse
from flask import Flask, request, jsonify
import uuid
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
  connection_string = os.environ["PSQL_CONN_STR"]
  conn = psycopg2.connect(connection_string)
  return conn

def build_menu_items_list(cur):
  menu_items = []
  cur.execute('SELECT name FROM menu_items')
  menu = cur.fetchall()
  for item in menu:
    menu_items.append(item[0])
  return menu_items

def valid_order(item_list, menu_items):
  for item in item_list:
    if item not in menu_items:
      return False
  return True

def place_order(cur, user_id, item_list):
  order_id = uuid.uuid1()
  sql = "INSERT INTO orders (order_id, user_id, restaurant_id, address, placed, order_valid) VALUES (%s, %s, %s, %s, %s, %s)"
  val = (str(order_id), user_id, 1, "my-address", True, True)
  cur.execute(sql, val)
  for item in item_list:
    cur.execute("INSERT INTO items (order_id, item) VALUES (%s, %s)", (str(order_id), item))
  return order_id

@app.route('/placeAndValidateOrder', methods=['POST'])
def placeAndValidateOrderHandler():
  args = placeAndValidateOrderArgs.from_request(request.get_json())
  item_list = args.item_list
  user_id = args.user_id

  conn = get_db_connection()
  cur = conn.cursor()

  menu_items = build_menu_items_list(cur)
  
  order_id = -1
  order_valid = False
  
  print(valid_order(item_list, menu_items))
  
  if valid_order(item_list, menu_items):
    order_id = place_order(cur, user_id, item_list)
    order_valid = True
  
  print(order_id)
  
  cur.close()
  conn.commit()
  conn.close()

  return validatedResponse(order_id=str(order_id), order_valid=order_valid).to_json()

if __name__ == '__main__':
  app.run(debug = True, host = '0.0.0.0')
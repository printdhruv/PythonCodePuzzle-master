import itertools
import sqlite3
from flask import Flask, jsonify, request
import re

app = Flask(__name__)

staples_summary = [];
staples_unit_price_dollars = 0;
staples_merchant_discount_dollars = 0;
staples_discount_dollars = 0;
connection = sqlite3.connect('staples.db')
cursor_reference = connection.cursor()
cursor_reference.execute('''DROP TABLE IF EXISTS staples_data_metadata''')
cursor_reference.execute('''DROP TABLE IF EXISTS external_data_metadata''')
cursor_reference.execute('''CREATE TABLE staples_data_metadata(Order_ID INTEGER,Unit_Price_Dollars REAL,Merchant_Discount_Cents REAL,
          Staples_Discount_Cents REAL,Session_Type TEXT )''')
cursor_reference.execute('''CREATE TABLE external_data_metadata(Order_ID INTEGER,Unit_Price_Dollars REAL,Staples_Discount_Dollars REAL,
          Merchant_Discount_Dollars REAL,Session_Type TEXT)''')
file = open(
    'C:\\Users\\print\\Downloads\\PythonCodePuzzle-master\\PythonCodePuzzle-master\\resources\\staples_data'
    '.csv', 'r');
for line in itertools.islice(file,1, None):
    staples_data_list = []
    for pattern in re.finditer('(\d)+|[A-z]+', line):
        staples_data_list.append(pattern.group(0));
    cursor_reference.execute('''INSERT INTO staples_data_metadata(Order_ID,Unit_Price_Dollars,Merchant_Discount_Cents,
              Staples_Discount_Cents,Session_Type )VALUES (?,?,?,?,?)''',
              (staples_data_list[0],float((staples_data_list[1]))/100,float((staples_data_list[2]))/100,
              float((staples_data_list[3]))/100,staples_data_list[4].lower()))
    staples_unit_price_dollars += float(staples_data_list[1])/100
    staples_merchant_discount_dollars += float(staples_data_list[2])/100
    staples_discount_dollars += float(staples_data_list[3])/100

staples_summary.append(('unit-price-dollars',staples_unit_price_dollars
                        ,'merchant-discount-dollars',staples_merchant_discount_dollars
                        ,'staples-discount-dollars',staples_discount_dollars));

merchant_summary = [];
merchant_unit_price_dollars = 0;
merchant_discount_dollars = 0;
merchant_staples_discount_dollars = 0;

file = open(
    'C:\\Users\\print\\Downloads\\PythonCodePuzzle-master\\PythonCodePuzzle-master\\resources\\external_data'
    '.psv', 'r');
for line in itertools.islice(file, 1, None):
    external_data_list=[]
    for pattern in re.finditer('([0-9]+[.]*[0-9]*[^\s\D])|[A-z][^\s]*', line):
        external_data_list.append(pattern.group(0));
    cursor_reference.execute('''INSERT INTO external_data_metadata(Order_ID,Unit_Price_Dollars,Staples_Discount_Dollars,
              Merchant_Discount_Dollars,Session_Type) VALUES(?,?,?,?,?)''',
              (external_data_list[0],float(external_data_list[1]),float(external_data_list[2]),
               float(external_data_list[3]),external_data_list[4].lower()))
    merchant_unit_price_dollars += float(external_data_list[1])
    merchant_discount_dollars += float(external_data_list[3])
    merchant_staples_discount_dollars += float(external_data_list[2])
connection.commit()
connection.close()
merchant_summary.append(('unit-price-dollars',merchant_unit_price_dollars
                         ,'merchant-discount-dollars',merchant_discount_dollars
                         ,'staples-discount-dollars',merchant_staples_discount_dollars));


@app.route('/', methods=['POST', 'GET'])
def hello_world():
    connection_default = sqlite3.connect('staples.db')
    cursor_reference_1 = connection_default.cursor()
    cursor_reference_1.close()
    connection_default.commit()
    connection_default.close()
    return "OK"


@app.route('/analytics/report', methods=['GET'])
def session_desc():
    constraint = request.args.get('order_by')
    column = ""
    if "session-type" in constraint:
        column="Session_Type"
    if "order-id" in constraint:
        column="Order_ID "
    if "unit-price-dollars" in constraint:
        column="Unit_Price_Dollars"
    if "desc" in constraint:
        column += " DESC"
    if "asc" in constraint:
        column += " ASC"
    connection_for_query = sqlite3.connect('staples.db')
    cursor_reference_2 = connection_for_query.cursor()
    cursor_reference_2.execute('''SELECT * FROM staples_data_metadata ORDER BY %s''' % (column,))
    staples_info = []
    for i in cursor_reference_2.fetchall() :
        staples_info.append(("unit-price-dollars:", i[1]
        ,"merchant-discount-dollars:", i[2]
        ,"staples-discount-dollars:", i[3]
        ,"session-type:", i[4]
        ,"order-id:", i[0]))
    cursor_reference_2.execute('''SELECT * FROM external_data_metadata ORDER BY %s''' % (column,))
    external_info = []
    for j in cursor_reference_2.fetchall() :
        external_info.append(("unit-price-dollars:", j[1]
                  ,"merchant-discount-dollars:", j[3]
                  ,"staples-discount-dollars:", j[2]
                  ,"session-type:", j[4]
                  ,"order-id:", j[0]))

    orders = [('summaries', ('staples-summary', staples_summary, 'merchant-summary', merchant_summary,)), 'orders']
    for i, j in zip(staples_info,external_info):
            orders.append(["staples-data", i,"merchant-data", j])
    cursor_reference_2.close()
    connection_for_query.commit()
    connection_for_query.close()
    return jsonify(orders)


if __name__ == '__main__':
    app.run(port=5001)
    app.debug(True)

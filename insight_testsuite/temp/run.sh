#!/bin/bash
#
# Use this shell script to compile (if necessary) your code and then execute it. Below is an example of what might be found in this file if your program was written in Python
#
#python ./src/purchase_analytics.py ./input/order_products.csv ./input/products.csv ./output/report.csv
python ./src/purchase_analytics.py --orders_file ./input/order_products.csv --products_file ./input/products.csv --output_file ./output/report.csv

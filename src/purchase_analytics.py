import sys, csv, argparse

from collections import defaultdict



if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Insight Data Engineering, Purchase Analytics - Di (Sherry) Shao")
	parser.add_argument('--products_file', default="./input/products.csv", help="(default: ./input/products.csv)")
	parser.add_argument('--orders_file', default="./input/order_products.csv", help="(default: ./input/order_products.csv)")
	parser.add_argument('--output_file', default="./output/report.csv", help="Output File Path. (default: ./output/report.csv)")
	args = parser.parse_args()


	# 1. Process products.csv and write to HashMap(product_id: department_id)
	products_by_department = {}		
	with open(args.products_file, 'r') as products:
		reader = csv.reader(products, quotechar='"', delimiter=',')
		product_header = next(reader)	
		for product_line in reader:
			# print("Processing product line..", product_line)
			product_id = product_line[0]
			department_id = product_line[3]	
			products_by_department[product_id] = department_id

	# 2. Process order_products.csv and write to report map
	report = defaultdict(dict)
	with open(args.orders_file, 'r') as order_products:
		next(order_products)	# Skip header
		for order_line in order_products:
			# print("Processing order line: ", order_line)
			order = order_line.rstrip("\n").split(',')	
			product_id = order[1]
			reordered = order[3]
			
			# Ignore the line if department_id is not found for this product_id			
			if product_id not in products_by_department:	
			 	continue
			
			# Add number_of_orders
			department_id = products_by_department[product_id]
			report[department_id]['number_of_orders'] = report[department_id].get("number_of_orders", 0) + 1
	
			# Add number_of_first_orders
			if reordered == '0':
				report[department_id]['number_of_first_orders'] = report[department_id].get('number_of_first_orders', 0) + 1
			else:
				report[department_id]['number_of_first_orders'] = report[department_id].get('number_of_first_orders', 0)
			
			# Add percentage
			number_of_orders = report[department_id]['number_of_orders']
			number_of_first_orders = report[department_id]['number_of_first_orders']
			report[department_id]['percentage'] = "{0:.2f}".format(number_of_first_orders / number_of_orders)
	
	
	# 3. Write to output
	OUTPUT_HEADER = "department_id,number_of_orders,number_of_first_orders,percentage\n"	
	
	with open(args.output_file, 'w') as f:
		f.write(OUTPUT_HEADER)
		sorted_report = sorted(report.items(), key=lambda x: int(x[0]))
		for department_id, row in sorted_report:
			line = department_id + "," + str(row["number_of_orders"]) + "," + str(row["number_of_first_orders"]) + "," + row['percentage'] + "\n"
			f.write(line)	
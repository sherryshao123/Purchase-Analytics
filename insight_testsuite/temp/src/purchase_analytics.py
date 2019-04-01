import sys, csv, argparse

from collections import defaultdict


# Function to validate fields and type
def validate(line, desired_length=None, cols_type=None):
	# print(line, desired_length, cols_type)
	if not isinstance(line, list):	return False
	if desired_length and len(line) != desired_length: return False
	
	for i, col_type in cols_type.items():
		if col_type == "str_digit":
			if not isinstance(line[i], str) or not line[i].isdigit(): return False
		else:
			if not isinstance(line[i], col_type): return False
			
	return True

def process_products(input):
	products_by_department = {}
	
	with open(args.products_file, 'r') as products:
		reader = csv.reader(products, quotechar='"', delimiter=',')
		product_header = next(reader)

		for product_line in reader:
			# print("Processing product line..", product_line)
			schema = { 0: "str_digit", 1: str, 2: "str_digit", 3: "str_digit"}
			if not validate(product_line, desired_length=4, cols_type=schema):
				print("line validation failed. Skipping line: ", product_line)
				continue
				
			product_id, department_id = product_line[0], product_line[3]
			products_by_department[product_id] = department_id	
		
	return products_by_department
	
def process_orders(input):
	report = defaultdict(dict)
	
	with open(input, 'r') as order_products:
		next(order_products)	# Skip header
		
		for order_line in order_products:
			# print("Processing order line: ", order_line)
			order = order_line.rstrip("\n").split(',')	
			schema = { 0: "str_digit", 1: "str_digit", 2: "str_digit", 3: "str_digit"}
			if not validate(order, desired_length=4, cols_type=schema):
				print("line validation failed. Skipping line: ", line)
				continue
				
			product_id, reordered = order[1], order[3]
			
			if product_id not in products_by_department: continue	# Skip if not finding product_id
			
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
			
	return report


def write_report(output):
	OUTPUT_HEADER = "department_id,number_of_orders,number_of_first_orders,percentage\n"	
	
	with open(args.output_file, 'w') as f:
		f.write(OUTPUT_HEADER)
		sorted_report = sorted(report.items(), key=lambda x: int(x[0]))
		for department_id, row in sorted_report:
			line = department_id + "," + str(row["number_of_orders"]) + "," + str(row["number_of_first_orders"]) + "," + row['percentage'] + "\n"
			f.write(line)	


if __name__ == "__main__":
	# Prepare
	parser = argparse.ArgumentParser(description="Insight Data Engineering, Purchase Analytics - Di (Sherry) Shao")
	parser.add_argument('--products_file', default="./input/products.csv", help="(default: ./input/products.csv)")
	parser.add_argument('--orders_file', default="./input/order_products.csv", help="(default: ./input/order_products.csv)")
	parser.add_argument('--output_file', default="./output/report.csv", help="Output File Path. (default: ./output/report.csv)")
	args = parser.parse_args()

	# MAIN
	# 1. Process products.csv and write to HashMap(product_id: department_id)
	products_by_department = process_products(args.products_file)

	# 2. Process order_products.csv and write to report map
	report = process_orders(args.orders_file)
		
	# 3. Write to output
	write_report(args.output_file)
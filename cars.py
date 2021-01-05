#!/usr/bin/env python3
import json, sys, locale, os, reports, emails

def load_data(filename):

  with open(filename) as json_file:
    data = json.load(json_file)
    
  return data

def format_car(car):
  return "{} {} ({})".format(car["car_make"], car["car_model"], car["car_year"])

def process_data(data):

  locale.setlocale(locale.LC_ALL, 'en_US.UTF8')

  max_revenue = {"revenue": 0}
  max_sales = {"Sale": 0}
  car_year_sale = collections.defaultdict(data)

  for item in data:

    item_price = locale.atof(item["price"].strip("$"))
    item_revenue = item["total_sales"] * item_price
    item_sales = item['total_sales']

    if item_revenue > max_revenue["revenue"]:
      item["revenue"] = item_revenue
      max_revenue = item

    if item_sales > max_sales["Sale"]:
      item["Sale"] = item_sales
      max_sales = item

    car_year_sale[item['car']['car_year']] += item['total_sales']
  max_year_sale = (0,0)

  for year, sales in car_year_sale.items():
    if sales > max_year_sale[1]:
      max_year_sale = (year,sales)
      
  summary = [
    "The {} generated the most revenue: ${}".format(format_car(max_revenue["car"]), max_revenue["revenue"]),
    "The {} had the most sales: {}".format(format_car(max_sales["car"]), max_sales["Sale"]),
    "The most popular year was {} with {} sales.".format(max_year_sale[0], max_year_sale[1])
            ]
  return summary

def cars_dict_to_table(car_data):

  table_data = [["ID", "Car", "Price", "Total Sales"]]

  for item in car_data:
    table_data.append([item["id"], format_car(item["car"]), item["price"], item["total_sales"]])

  return table_data

def main(argv):
  
  directory_path = r''

  data = load_data(directory + '/' + "car_sales.json")
  summary = process_data(data)

  report = reports.generate('save-location','title', "<br/>".join(summary), cars_dict_to_table(data))

  message = emails.generate('sender-address','receiver-address', 'title', '\n'.join(summary), 'save-location')
  emails.send(message)

if __name__ == "__main__":
  main(sys.argv)

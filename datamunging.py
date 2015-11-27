from __future__ import absolute_import, division, print_function
import pandas as pd
from grade import Grading

class DataMunging:

    def __init__(self, sales_file, item_file, category):
        self.sales_file = sales_file
        self.item_file = item_file
        self.category = category
        self.item_data= pd.DataFrame
        self.sales_data = pd.DataFrame

    def readData(self):
        self.sales_data = pd.DataFrame.from_csv(self.sales_file, index_col=None)
        self.item_data = pd.DataFrame.from_csv(self.item_file, index_col=None)

    def cleanData(self):
        self.sales_data = self.sales_data[self.sales_data.SALES > 0 ]

    def aggregateData(self):
        merged_data = self.sales_data.merge(self.item_data)
        merged_data = merged_data[merged_data.CATEGORY == self.category]
        total_sales = merged_data.groupby('STOREID').sum().reset_index(level=None)
        total_sales = total_sales.drop('WEEKID', 1)
        return total_sales

# if __name__ == "__main__":
#     sales_file = "C:/Users/1020382/Documents/Work/StoreClustering/grading/testData/sales.txt"
#     item_file = "C:/Users/1020382/Documents/Work/StoreClustering/grading/testData/item.txt"
#     dm = DataMunging(sales_file, item_file, "B")
#     dm.readData()
#     dm.cleanData()
#     data = dm.aggregateData()
#     gd = Grading()
#     bin_size = []
#     num_grade = int(raw_input("Enter Number of Grade"))
#     for i in range(num_grade - 1):
#         print("Upper Limit of bin ", i)
#         bin_size.append(int(raw_input()))
#     gd.percentage_of_average(data, 4, "C:/Users/1020382/Documents/Work/StoreClustering/grading/testData")
# #     gd.equalWidth(data, 4, "C:/Users/1020382/Documents/Work/StoreClustering/grading/testResult")
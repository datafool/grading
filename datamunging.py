__author__ = 'pawan'

import pandas as pd

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
        weekly_sales = merged_data.groupby(['STOREID', 'WEEKID']).sum().reset_index(level=None)
        total_sales = weekly_sales.groupby('STOREID').sum().reset_index(level=None)
        week_count = weekly_sales.groupby('STOREID').size().reset_index(level=None)
        week_count.columns=['STOREID', 'Freq']
        average_sales = total_sales.merge(week_count)
        average_sales['Average Sales'] = average_sales.SALES/average_sales.Freq
        average_sales = average_sales.drop('WEEKID',1)
        return average_sales

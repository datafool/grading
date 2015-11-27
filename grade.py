from __future__ import absolute_import, division, print_function
import datetime
from time import time
import pandas as pd
import numpy as np


class Grading:

    # Equal Width Method for Channel Clustering
    def equal_width(self, data, num_grade, out_file_loc, sd_range=3):
        data = self.mark_outlier(data, sd_range)
        max_sales = np.max(data[data.Outlier == 0]).SALES
        min_sales = np.min(data[data.Outlier == 0]).SALES
        bin_size = (max_sales - min_sales)/num_grade
        data['Grade'] = np.ceil((data['SALES'] - min_sales)/bin_size)
        data['FinalGrade'] = np.where(data['Grade'] <= 0, 1, data['Grade'])
        data = data.drop(['Outlier', 'Grade'], axis=1)
        data['FinalGrade'] = np.where(data['FinalGrade'] >= num_grade, num_grade, data['FinalGrade'])
        data['FinalGrade'] = num_grade + 1 - data['FinalGrade']
        summary = self.create_summary(data, num_grade)
        store_stat = self.detail_store_stats(data, num_grade)
        ts = time()
        st = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H-%M-%S")
        grade_file = out_file_loc+"/EqualWidthGrading_"+st+"_.csv"
        summary_file = out_file_loc+"/EqualWidthSummary_"+st+"_.csv"
        store_file = out_file_loc+"/EqualWidthStoreStats_"+st+"_.csv"
        data.to_csv(grade_file, sep=",", index=False)
        summary.to_csv(summary_file, sep=",", index=False)
        store_stat.to_csv(store_file, sep =",", index=False)
        return [data, summary, store_stat]

    # Percentage of Average method for channel clustering
    def percentage_of_average(self, data, num_grade, out_file_loc, bin_size):
        print("Enter upper percentage limit for each bin. Enter 30, if upper limit of bin is 30%")

        average = np.mean(data.SALES)
        data['PercentageOfAverage'] = (data.SALES / average)*100
        data['FinalGrade'] = None
        for i in range(len(bin_size)-1, -1, -1):
            data['FinalGrade'] = np.where(data['PercentageOfAverage'] < bin_size[i], num_grade - i, data['FinalGrade'])
        data['FinalGrade'] = np.where(data.Grade.isnull(), 1, data['FinalGrade'])
        summary = self.create_summary(data, num_grade)
        store_stat = self.detail_store_stats(data, num_grade)
        ts = time()
        st = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H-%M-%S")
        grade_file = out_file_loc+"/PercentageOfAverage_"+st+"_.csv"
        summary_file = out_file_loc+"/PercentageOfAverage_"+st+"_.csv"
        store_file = out_file_loc+"/PercentageOfAverage_"+st+"_.csv"
        data.to_csv(grade_file, sep=",", index=False)
        summary.to_csv(summary_file, sep=",", index=False)
        store_stat.to_csv(store_file, sep=",", index=False)
        return [data, summary, store_stat]

    # Method to mark the outlier in data which will not be considered in for binSize Calculation
    @staticmethod
    def mark_outlier(data, sd_range=3):
        # data = data.copy()
        avg = np.mean(data['SALES'])
        std = np.std(data['SALES'])
        data['Outlier'] = np.where(np.abs(data.SALES - avg)/std <= sd_range, 0, 1)
        return data

    # Method which creates summary
    @staticmethod
    def create_summary(data, num_grade):
        # Creating a data frame which contains the some extra information about each grade
        summary = pd.DataFrame(columns=('Grade', 'LowerBound', 'UpperBound', 'Range', 'NumberOfStores',
                                        'PercentageOfStore', 'TotalSales', 'PercentageSales'))
        overall_sales = np.sum(data).SALES
        overall_count = len(data)
        for i in range(1, num_grade+1):
            lower = np.min(data[data.FinalGrade == i]).SALES
            upper = np.max(data[data.FinalGrade == i]).SALES
            tot_count = len(data[data.FinalGrade == i])
            tot_sales = np.sum(data[data.FinalGrade == i]).SALES
            summary.loc[i] = [i, lower, upper, upper - lower, tot_count, tot_count*1.0/overall_count,
                              tot_sales, tot_sales*1.0/overall_sales]
        return summary

    @staticmethod
    def detail_store_stats(data, num_grade):
        # data = data.copy()
        # distance = (StoreSales - AverageGradeSales)/AverageGradeSale
        # z-score = (StoreSales - AverageGradeSales)/StandardDeviationOfGradeSales
        data['Distance'] = None
        data['Z-score'] = None
        for i in range(1, num_grade+1):
            avg_grade_sales = np.mean(data[data.FinalGrade == i]).SALES
            std_grade_sales = np.std(data[data.FinalGrade == i]).SALES
            data['Distance'] = np.where(data.FinalGrade == i, (data.SALES - avg_grade_sales)/avg_grade_sales,
                                        data['FinalGrade'])
            data['Z-score'] = np.where(data.FinalGrade == i, (data.SALES - avg_grade_sales)/std_grade_sales,
                                       data['FinalGrade'])
        return data
from __future__ import absolute_import, division, print_function
from datamunging import  DataMunging
from grade import Grading

if __name__ == "__main__":
    pos_data = raw_input("POS Data on which grading will be done")
    item_data = raw_input("Data which gives the category, department etc. of a product")
    grade_type = int(raw_input(''' Type of Grading Algorithm to be run
                                   1. Equal Width Grading, or
                                   2. Percentage of Average Grading, or
                                   3. Manual Grading'''))
    num_grade = int(raw_input('''Number of Grades to be created'''))
    out_file = raw_input("Location where output would be written")
    if grade_type == 1:
        sd = int(raw_input('Value of Standard Deviaiton using which outlier will be removed'))
        dm = DataMunging(pos_data, item_data, "B")
        dm.readData()
        dm.cleanData()
        data = dm.aggregateData()
        gd = Grading()
        gd.equal_width(data, num_grade, out_file, sd)
    elif grade_type == 2:
        bin_size = []
        print("Enter the upper bound for bin, if upper bound is 30%, input should be 30")
        for i in range(num_grade - 1):
            print("Upper Limit of bin ", i + 1)
            bin_size.append(int(raw_input()))
        dm = DataMunging(pos_data, item_data, "B")
        dm.readData()
        dm.cleanData()
        data = dm.aggregateData()
        gd = Grading()
        gd.percentage_of_average(data, num_grade, out_file, bin_size)
    elif grade_type == 3:
        print("Sorry, Method under implementation")
    else:
        print("Sorry, we like to provide multiple algorithm but we are not God")
import csv
import re

with open("results", 'r') as results_f:
    with open('results.csv', 'w') as results_csv:
        csv_writer = csv.writer(results_csv, delimiter=',')

        i = 0
        nums = []
        for line in results_f:
            num = re.findall("\\d+\\.*\\d*", line)
            nums.append(num[0])

            i += 1

            if i == 4:
                print(nums)
                csv_writer.writerow(nums)
                i = 0
                nums = []

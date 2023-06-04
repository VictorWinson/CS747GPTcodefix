import re
import csv
import timeit
import matplotlib.pyplot as plt
import tempfile
import subprocess
import os
import sqlite3
import matplotlib.pyplot as plt
import numpy as np

csv_file_path = "./with-runtime.csv"
liErrors = []
zeros = 0
sScores = []
fScores = []
sRuntimes = []
fRuntimes = []
sScoresChanged = []
fScoresChanged = []
sRuntimesChanged = []
fRuntimesChanged = []

with open(csv_file_path, "r") as file:
    reader = csv.reader(file)
    for row in reader:
        #print(row)
        DiError = {}
        DiError['id'] = row[0]
        DiError['filename'] = row[1]
        DiError['sourceScore'] = float(row[2])
        DiError['fixedScore'] = float(row[3])
        DiError['sRuntime'] = float(row[4])
        DiError['fRuntime'] = float(row[5])
        DiError['source'] = row[6]
        DiError['fixedCode'] = row[7]
        DiError['testCase'] = row[8]
        liErrors.append(DiError)
        sScores.append(DiError['sourceScore'])
        fScores.append(DiError['fixedScore'])
        sRuntimes.append(DiError['sRuntime'])
        fRuntimes.append(DiError['fRuntime'])
        if DiError['sourceScore'] != DiError['fixedScore']:
            sScoresChanged.append(DiError['sourceScore'])
            fScoresChanged.append(DiError['fixedScore'])
            sRuntimesChanged.append(DiError['sRuntime'])
            fRuntimesChanged.append(DiError['fRuntime'])
    print("data imported")
    print(len(liErrors))

print(sScores)
print(fScores)
print(sRuntimes)
print(fRuntimes)

scores = sScores
runtime = sRuntimes

scores_group1 = sScores
runtime_group1 = sRuntimes
scores_group2 = fScores
runtime_group2 = fRuntimes

# Define the score ranges
score_ranges = np.arange(0, 101, 10)

# Compute the average runtime for each score range for Group 1
avg_runtime_group1 = []
for score_range in score_ranges:
    filtered_runtime = [rt for sc, rt in zip(scores_group1, runtime_group1) if score_range <= sc < score_range + 10]
    if filtered_runtime:
        avg_runtime_group1.append(np.mean(filtered_runtime))
    else:
        avg_runtime_group1.append(0)

# Compute the average runtime for each score range for Group 2
avg_runtime_group2 = []
for score_range in score_ranges:
    filtered_runtime = [rt for sc, rt in zip(scores_group2, runtime_group2) if score_range <= sc < score_range + 10]
    if filtered_runtime:
        avg_runtime_group2.append(np.mean(filtered_runtime))
    else:
        avg_runtime_group2.append(0)
"""
# Plotting the line graph for Group 1
#plt.plot(score_ranges, avg_runtime_group1, marker='o', label='sourceCode')

# Plotting the line graph for Group 2
plt.plot(score_ranges, avg_runtime_group2, marker='o', label='fixedCode')

# Adding labels and title
plt.xlabel('Score Ranges')
plt.ylabel('Average Runtime (ms)')
plt.title('Score Ranges vs Average Runtime')

# Adding legend
plt.legend()

# Display the graph
plt.show()
"""

# Sample data for two lists of scores
list1_scores = sScoresChanged
list2_scores = fScoresChanged

# Define the range and number of bins
num_bins = 10
bin_range = range(0, 101, 10)

# Calculate the histogram for each list of scores
list1_hist, _ = np.histogram(list1_scores, bins=num_bins, range=(0, 100))
list2_hist, _ = np.histogram(list2_scores, bins=num_bins, range=(0, 100))

# Create the bar chart
plt.figure(figsize=(10, 6))
bar_width = 0.35
opacity = 0.8

index = np.arange(num_bins)
#plt.bar(index, list1_hist, bar_width, alpha=opacity, color='b', label='sourceCode')
plt.bar(index + bar_width, list2_hist, bar_width, alpha=opacity, color='g', label='fixedCode')

plt.xlabel('Score Range')
plt.ylabel('Frequency')
plt.title('Scores Distribution for test score changed fixes')
plt.xticks(index + bar_width, [f'{start}-{end}' for start, end in zip(bin_range, bin_range[1:])])
plt.legend()

plt.tight_layout()
plt.show()

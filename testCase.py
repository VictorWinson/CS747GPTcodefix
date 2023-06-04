import re
import csv
import timeit
import matplotlib.pyplot as plt
import tempfile
import subprocess
import os
import sqlite3
import sys
from io import StringIO

# Store the original sys.stdout for later restoration
original_stdout = sys.stdout

# Create a new StringIO object to capture the output
output_buffer = StringIO()

csv_file_path = "result.csv"
liErrors = []
zeros = 0

conn = sqlite3.connect('errors.db')
c = conn.cursor()


with open(csv_file_path, "r") as file:
    reader = csv.reader(file)
    for row in reader:
        #print(row)
        DiError = {}
        DiError['id'] = row[0]
        DiError['filename'] = row[1]
        DiError['sourceScore'] = 0#float(re.findall(r'\d+\.?\d?', row[2])[0])
        DiError['fixedScore'] = 0 #float(re.findall(r'\d+\.?\d?', row[3])[0])
        DiError['source'] = row[4].replace('""', '"')
        DiError['fixedCode'] = row[5].replace('""', '"')
        liErrors.append(DiError)
        #print(DiError['source'], DiError['fixedCode'])
    print("data imported")

#print(liErrors)
sScores = []
fScores = []

def run_testcase(source_code, testcase, problem_id):
    # Write the source code to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.py') as temp:
        source_temp_path = temp.name
        temp.write(source_code)

    # Modify the testcase to print the result

    # Write the testcase to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.py') as temp:
        temp.write(testcase.replace(problem_id + ".py", source_temp_path))
        testcase_temp_path = temp.name

    try:
        #把路径改成你的python编译器路径
        result = subprocess.run(['/usr/local/bin/python', testcase_temp_path], stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, timeout=60)


        print('Error:', result.stderr)
    except Exception as e:
        print(f'Error while executing testcase: {e}')
        return None

    # Delete the temporary files
    os.remove(source_temp_path)
    os.remove(testcase_temp_path)

    return result.stdout

"""
def timed_function():
    try:
        sys.stdout = output_buffer
        source = run_testcase(DiError['source'], DiError['testCase'], DiError['filename'])
    except Exception as e:
        if e == "FileNotFoundError":
            pass
        else:
            print(e)
    finally:
        DiError['sourceScore'] = float(re.findall(r"Unit Test Returned: (\d*\.\d+|\d+)", source.decode('utf-8'))[0])  # 正则表达式提取分数
        sys.stdout = original_stdout
        print("source:", DiError['sourceScore'])
    #run_testcase(DiError['source'], DiError['testCase'], DiError['filename'])

def timed_function2():
    try:
        sys.stdout = output_buffer
        source = run_testcase(DiError['source'], DiError['testCase'], DiError['filename'])
    except Exception as e:
        if e == "FileNotFoundError":
            pass
        else:
            print(e)
    finally:
        sys.stdout = original_stdout
        DiError['fixedScore'] = float(re.findall(r"Unit Test Returned: (\d*\.\d+|\d+)", source.decode('utf-8'))[0])  # 正则表达式提取分数
        print("fixed:", DiError['fixedScore'])
    #run_testcase(DiError['fixedCode'], DiError['testCase'], DiError['filename'])
"""

def timed_function():
    try:
        sys.stdout = output_buffer
        source = run_testcase(DiError['source'], DiError['testCase'], DiError['filename'])
    except Exception as e:
        if e == "FileNotFoundError":
            pass
        else:
            print(e)
    finally:
        if source is not None:
            DiError['sourceScore'] = float(re.findall(r"Unit Test Returned: (\d*\.\d+|\d+)", source.decode('utf-8'))[0])
        else:
            DiError['sourceScore'] = 0
        sys.stdout = original_stdout
        print("source:", DiError['sourceScore'])

def timed_function2():
    try:
        sys.stdout = output_buffer
        source = run_testcase(DiError['fixedCode'], DiError['testCase'], DiError['filename'])
    except Exception as e:
        if e == "FileNotFoundError":
            pass
        else:
            print(e)
    finally:
        if source is not None:
            DiError['fixedScore'] = float(re.findall(r"Unit Test Returned: (\d*\.\d+|\d+)", source.decode('utf-8'))[0])
        else:
            DiError['fixedScore'] = 0
        sys.stdout = original_stdout
        print("fixed:", DiError['fixedScore'])

for DiError in liErrors[565:]:
    #if DiError['sourceScore'] == 0 and zeros > 5:
    #    print("more than 5 zeros, pass")
    #    continue
    #elif DiError['sourceScore'] == 0 and DiError['fixedScore'] == 0:
    #    zeros += 1

    sScores.append(DiError['sourceScore'])
    fScores.append(DiError['fixedScore'])

    res = c.execute("SELECT \
    problemtestcase \
    FROM errors \
    WHERE _id == '{id}' \
    ".format(id = DiError['id']))
    selectResult = res.fetchall()
    DiError['testCase'] = selectResult[0][0]

    # Measure the runtime
    print(f"start runtime test for {DiError['id']}")
    runtime = timeit.timeit(timed_function, number=3)
    DiError['sRuntime'] = runtime
    print(f"sRuntime: {runtime} seconds")

    runtime = timeit.timeit(timed_function2, number=3)
    DiError['fRuntime'] = runtime
    print(f"fRuntime: {runtime} seconds")

    result = (DiError['id'], DiError['filename'], DiError['sourceScore'], DiError['fixedScore'], DiError['sRuntime'], DiError['fRuntime'], DiError['source'], DiError['fixedCode'], DiError['testCase'])
    with open('with-runtime.csv', mode='a', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(result)
    print(DiError["id"], ": result writen", "\n==========\n")


"""
#bar chart
# Define the range boundaries
range_labels = ['0-20', '20-40', '40-60', '60-80', '80-100']
range_values = [0, 20, 40, 60, 80, 100]

# Count the number of scores falling into each range
counts = [0] * (len(range_values) - 1)
for score in fScores:
    for i in range(len(range_values) - 1):
        if range_values[i] <= score < range_values[i+1]:
            counts[i] += 1
            break

# Plot the bar chart
plt.bar(range(len(counts)), counts)
plt.xlabel('Range')
plt.ylabel('Count')
plt.xticks(range(len(counts)), range_labels)
plt.title('Score Distribution')
plt.show()
"""

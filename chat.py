import os
import sqlite3
import openai
import sys
from io import StringIO
import subprocess
import tempfile
import csv
import re

openai.api_key = ""

conn = sqlite3.connect('errors.db')
c = conn.cursor()

# Store the original sys.stdout for later restoration
original_stdout = sys.stdout

# Create a new StringIO object to capture the output
output_buffer = StringIO()

# liErrors include a list of dictionary DiError
liErrors = []
# DiError include useful value of a error record
DiError = dict()

#responds = []

res = c.execute("SELECT \
_id, samplesource_code, problemtestcase, \
problemmax_score, problemid \
FROM errors \
WHERE problemid == 'lsn13_cargocapacity' OR problemid == 'Lists2_100m' \
LIMIT {limit} \
OFFSET {offset} \
".format(limit=int(sys.argv[1]), offset=int(sys.argv[2])))

selectResult = res.fetchall()

for i in selectResult:
    DiError = {}
    DiError['id'] = i[0]
    DiError['source'] = i[1]
    DiError['testCase'] = i[2]
    DiError['maxScore'] = i[3]
    DiError['filename'] = i[4]
    DiError['fixedScore'] = None
    liErrors.append(DiError)


#print(liErrors[1])


#print(liErrors[:10])

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
                                stderr=subprocess.PIPE, timeout=10)


        print('Error:', result.stderr)
    except Exception as e:
        print(f'Error while executing testcase: {e}')
        return None

    # Delete the temporary files
    os.remove(source_temp_path)
    os.remove(testcase_temp_path)

    return result.stdout


def get_completion(prompt, model = "gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model = model,
        messages = messages,
        temperature = 0,
    )
    return response.choices[0].message["content"]


for DiError in liErrors:
    # sourceScore calculation
    """
    try:
        exec(DiError['source'])
    except Exception as e:
        DiError['errorType'] = e
    """

    try:
        sys.stdout = output_buffer
        source = run_testcase(DiError['source'], DiError['testCase'], DiError['filename'])
    except Exception as e:
        if e == "FileNotFoundError":
            pass
        else:
            print(e)
    finally:
        DiError['sourceScore'] = re.findall(r"Unit Test Returned: (\d*\.\d+|\d+)", source.decode('utf-8'))  # 正则表达式提取分数
        sys.stdout = original_stdout

    # gpt fix & fixedScore calculation
    if DiError['sourceScore'] == None:
        DiError['fixedScore'] == None
        continue
    print(DiError["id"], ": getting result")
    result = get_completion("Here is a buggy code, try to fix it for me.\
{sourceCode}".format(sourceCode = DiError['source']))
    print(DiError["id"], ": result received")
    DiError['fixedCode'] = result
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
        DiError['fixedScore'] = re.findall(r"Unit Test Returned: (\d*\.\d+|\d+)", source.decode('utf-8'))  # 正则表达式提取分数
        print(source)

    result = (DiError['id'], DiError['filename'], DiError['sourceScore'], DiError['fixedScore'], DiError['source'], DiError['fixedCode'])
    with open('result.csv', mode='a', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(result)
    print(DiError["id"], ": result writen", "\n==========\n")

"""
for key in DiError:
    print("\n=========================================\n")
    print("{key}: {value}\n".format(key=key, value=DiError[key]))
"""

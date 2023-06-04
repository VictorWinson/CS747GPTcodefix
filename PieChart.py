import csv

csv_file_path = "./with-runtime.csv"
liErrors = []
zeros = 0

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
    print("data imported")
    print(len(liErrors))

Unchanged = 0
USlower = 0
UFaster = 0
USameSpeed = 0

Increased = 0
ISlower = 0
IFaster = 0
ISameSpeed = 0

Decreased = 0
DSlower = 0
DFaster = 0
DSameSpeed = 0

for DiError in liErrors:
    if DiError['fixedScore'] == DiError['sourceScore']:
        Unchanged += 1
        if DiError['sRuntime'] > DiError['fRuntime']:
            UFaster += 1
        elif DiError['sRuntime'] < DiError['fRuntime']:
            USlower += 1
        else:
            USameSpeed += 1
    elif DiError['fixedScore'] > DiError['sourceScore']:
        Increased += 1
        if DiError['sRuntime'] > DiError['fRuntime']:
            IFaster += 1
        elif DiError['sRuntime'] < DiError['fRuntime']:
            ISlower += 1
        else:
            ISameSpeed += 1
    else:
        Decreased += 1
        if DiError['sRuntime'] > DiError['fRuntime']:
            DFaster += 1
        elif DiError['sRuntime'] < DiError['fRuntime']:
            DSlower += 1
        else:
            DSameSpeed += 1


print(f"Unchanged:{Unchanged}")
print(f"USlower:{USlower}")
print(f"UFaster:{UFaster}")
print(f"USameSpeed:{USameSpeed}")

print(f"Increased:{Increased}")
print(f"ISlower:{ISlower}")
print(f"IFaster:{IFaster}")
print(f"ISameSpeed:{ISameSpeed}")

print(f"Decreased:{Decreased}")
print(f"DSlower:{DSlower}")
print(f"DFaster:{DFaster}")
print(f"DSameSpeed:{DSameSpeed}")

# pie chart for Increased data
import matplotlib.pyplot as plt

# Data for the pie chart
categories = ['Slower', 'Faster', 'Same speed']
values = [ISlower, IFaster, ISameSpeed]

# Create a pie chart
plt.pie(values, labels=categories, autopct='%1.1f%%')

# Add a title
plt.title('the runtime changes for all fixes getting higher mark in test')

# Display the chart
plt.show()


# pie chart for how many have changed
# Data for the pie chart
categories = ['Increased', 'Decreased', 'Unchanged']
values = [Increased, Decreased, Unchanged]

# Create a pie chart
plt.pie(values, labels=categories, autopct='%1.1f%%')

# Add a title
plt.title('how many have changed after one promt')

# Display the chart
plt.show()

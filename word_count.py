import json
import matplotlib.pyplot as plt
import numpy as np

SIDE_EFFECT = 'side effect'
OMNICRON = 'omicron'
BOOSTER = 'booster'
VACCINE = 'vaccine'

WORD_COUNT = {
    SIDE_EFFECT: 0,
    OMNICRON: 0,
    BOOSTER: 0,
    VACCINE: 0
}

with open('booster_omicron.json', 'r') as f:
    json_data = f.read()

title_list = json.loads(json_data)

for title in title_list:
    norm_title = title.lower()
    for key, value in WORD_COUNT.items():
        if key in norm_title:
            WORD_COUNT[key] = value + 1

print(WORD_COUNT)

y_axis = np.array(WORD_COUNT.values())

x_labels = np.array(WORD_COUNT.keys(), dtype='|S16')
width = 0.2
nitems = len(y_axis)
x_axis = np.arange(0, nitems * width, width)

fig, ax = plt.subplots(1)
ax.bar(x_axis, y_axis, width=width, align='center', color='g')
ax.set_xticks(x_axis);
ax.set_xticklabels(x_labels, rotation=90)
plt.show()

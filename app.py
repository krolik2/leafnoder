from fuzzywuzzy import fuzz, process
import pandas as pd
from tqdm import tqdm
from datetime import datetime

nodesDF = pd.read_csv('nodes.csv')
titlesDF = pd.read_csv('testing.csv', encoding="utf8")

titlesList = titlesDF.values.tolist()

# alternative way of matching, with full tree path, excluding prefix (prefix is all text before ":")
# def getWholeTextExcludingPrefix(string):
#     return string.replace("/", " ").split(':')[1].strip()


def getTextAfterLastSlash(string):
    return string.split('/', -1)[-1]


nodesDF.NODE_TRAVERSED_PATH = nodesDF.NODE_TRAVERSED_PATH.apply(
    getTextAfterLastSlash)

nodeList = nodesDF.values.tolist()

titlesDF["item_name"].fillna("missing name", inplace=True)

# matching options:
# fuzz.ratio
# fuzz.partial_ratio
# fuzz.token_sort_ratio
# fuzz.token_set_ratio


def match_term(term, nodes_list, min_score):
    max_score = -1
    item_name = ""
    item_id = ""
    for term2 in nodes_list:
        score = fuzz.token_set_ratio(term2[1], term)
        if (score > min_score) & (score > max_score):
            item_name = term2[1]
            item_id = term2[0]
            max_score = score
    return (item_id, item_name, max_score)


dict_list = []

for name in tqdm(titlesList):
    match = match_term(name[1], nodeList, 75)

    dict_ = {}
    dict_.update({"product_name": name[1]})
    dict_.update({"asin": name[0]})
    dict_.update({"node_id": match[0]})
    dict_.update({"node_name": match[1]})
    dict_.update({"score": match[2]})
    dict_list.append(dict_)

now = datetime.now()
currentTime = now.strftime("%H_%M_%S")
output = pd.DataFrame(dict_list)
output.to_excel(f'test - {currentTime}.xlsx')
print('done')


# import tkinter as tk
# from tkinter import filedialog, Text
# import os

# root = tk.Tk()

# def addFile():
#     filename= filedialog.askopenfilename(initialdir="/", title="select file",
#     filetypes=(("spreadsheet", "*.xlsx"), ("all files", "*.*")))

# canvas = tk.Canvas(root, height=480, width=480, bg="#18191a")
# canvas.pack()

# frame = tk.Frame(root, bg="white")
# frame.place(relwidth=0.8, relheight=0.6, relx=0.1, rely=0.1)

# openFile = tk.Button(root, text="open file", padx=10, pady=5, command=addFile)
# openFile.pack()

# runApp = tk.Button(root, text="run app", padx=10, pady=5)
# runApp.pack()

# root.mainloop()

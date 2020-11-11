from fuzzywuzzy import fuzz, process
import pandas as pd

nodesDF = pd.read_excel('nodesv2.xlsx')
titlesDF = pd.read_excel('titels.xlsx')

nodeList = nodesDF.values.tolist()
titlesList = titlesDF.values.tolist()


def match_term(term, nodes_list, min_score):
    max_score = -1
    item_name = ""
    item_id = ""
    for term2 in nodes_list:
        score = fuzz.partial_ratio(term2[1], term)
        if (score > min_score) & (score > max_score):
            item_name = term2[1]
            item_id = term2[0]

            max_score = score
    return (item_id, item_name, max_score)

dict_list = []

# partial 70 wyglada niezle

for name in titlesList:
    match = match_term(name[0], nodeList, 70)
    
    dict_ = {}
    dict_.update({"product_name" : name[0]})
    dict_.update({"asin" : name[1]})
    dict_.update({"node_id" : match[0]})
    dict_.update({"node_name" : match[1]})
    dict_.update({"score" : match[2]})
    dict_list.append(dict_)


output = pd.DataFrame(dict_list)
output.to_excel('test6v2partial70.xlsx')
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




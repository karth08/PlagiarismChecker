from tkinter import *
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfile
import os
from matplotlib import pyplot as plt
from numpy import vectorize 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path
#for the comparison table
from prettytable import PrettyTable

#Red colour converter
def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)


# Create an instance of tkinter frame
win = Tk()
def extract_data():
    print(text_box.get('1.0', 'end'))

# Set the geometry of tkinter frame
win.title("File Selector for Plagiarism Checker")
win.geometry("400x500")
win.config(bg='#84BF04')

global list1
list1 = []

message ='''
Welcome to THE PLAGIARISM CHECKER!
    -developed by students of CSE-1

Before you upload any files to cross-verify for plagiarism, here are the steps you should follow:

1.Upload your sample files to cross-check

2.A Graphical Display will give you info on the plagiarised text above a threshold

3.Input the file you would like to gain information about.

4.You are all good to go!

'''
text_box = Text(
    win,
    height=21,
    width=40,
    wrap ='word'
)
text_box.pack(expand=True)
text_box.insert('end', message)

def open_file():
   file = filedialog.askopenfile(mode='r', filetypes=[('Text Files', '*.txt')])
   if file:
      filepath = os.path.abspath(file.name)
      Label(win, text="The File is located at : " + str(filepath), font=('Calibri',9,"italic")).pack()
      list1.append(filepath)
    
def close():
   #win.destroy()
   win.quit()

# Create a Button to call close()
Button(win, text= "Close the Window", font=("Calibri",9,"bold"), command=close).pack(side=TOP)
      
# Add a Label widget
label = Label(win, text="Click the 'Browse' Button to browse the Files")
label.pack(pady=5)

# Create a Button
ttk.Button(win, text="Browse", command=open_file).pack(side = BOTTOM)

win.mainloop()
#print(list1)

 
sample_files = [doc for doc in list1 if doc.endswith('.txt')]
sample_contents = [open(File).read() for File in sample_files]
 
vectorize = lambda Text: TfidfVectorizer().fit_transform(Text).toarray()
similarity = lambda doc1, doc2: cosine_similarity([doc1, doc2])
 
vectors = vectorize(sample_contents)
s_vectors = list(zip(sample_files, vectors))
 
def check_plagiarism():
    results = set()
    global numerical_scores
    numerical_scores = []
    global s_vectors, sample_pair, sim_score
    for sample_a, text_vector_a in s_vectors:
        new_vectors = s_vectors.copy()
        current_index = new_vectors.index((sample_a, text_vector_a))
        del new_vectors[current_index]
        for sample_b, text_vector_b in new_vectors:
            sim_score = similarity(text_vector_a, text_vector_b)[0][1]
            sample_pair = sorted((sample_a, sample_b))
            score = sample_pair[0], sample_pair[1], format(sim_score*100, ".3f")
            results.add(score)
    return results

x_label_names = [Path(i).stem for i in sample_files]
#revised_x_label_names = [f'{x_label_names[i]} VS {x_label_names[i+1]}' for i in range(x_label_names)]
y1 = [Path(data[0]).stem for data in check_plagiarism()]
    
y2 = [Path(data[1]).stem for data in check_plagiarism()]

y1y2 = [f"{i} VS {j}" for i,j in zip(y1,y2)]



y_label_names1 = [float(data[-1]) for data in check_plagiarism()]
y_label_names2 = [100-j for j in y_label_names1]
plt.close("all")
plt.figure(figsize=(10, 10)) 

plt.bar(range(len(y_label_names1)),y_label_names1, label = 'Plagiarised Percentage of the Text')

plt.bar(range(len(y_label_names1)),y_label_names2, bottom =y_label_names1, label = 'Original Percentage of the Text' )

ax = plt.subplot()
ax.set_xticks(range(len(y_label_names1)))
ax.set_xticklabels(y1y2, rotation = 45)

plt.legend()

plt.xlabel('File Names')
plt.ylabel("Percentage of file's text")
plt.title('Comparison of files to determine extent of Plagiarism')

plt.show()
plt.savefig("plagiarised_files.png") 
#for data in check_plagiarism():
#    print(data)    

while True:
    print('\033[1m' + "To gain specific information, we require a base file as a reference!")
    print()
    print("-------------------------------")
    base_file = input("Enter the name of the file you like to consider: ")
    if base_file not in x_label_names:
          print("This base file doesn't exist within your selected file list!")
          base_file = input("Re-enter your base file: ")
    else:
          filenames = []
          filenames_values = []
          for data in check_plagiarism():
                if Path(data[0]).stem == base_file:
                    filenames.append(Path(data[1]).stem)
                    if float(data[-1]) > 30:
                        filenames_values.append(colored(255, 0, 0, str(data[-1])))
                    else:
                        filenames_values.append(str(data[-1]))
    #                 if float(data[-1]) > 30:
    #                     data[-1] = str(data[-1])
    #                     data[-1] = colored(255, 0, 0, str(data[-1]))

                elif Path(data[1]).stem == base_file:
                    filenames.append(Path(data[0]).stem)
                    if float(data[-1]) > 30:
                        filenames_values.append(colored(255, 0, 0, str(data[-1])))
                    else:
                        filenames_values.append(str(data[-1]))
    #                 if float(data[-1]) > 30:
    #                     data[-1] = str(data[-1])
    #                     data[-1] = colored(255, 0, 0, str(data[-1]))
          myTable = PrettyTable(["File Name", f"Plagiarism Percentage against {base_file}"])

          # Add rows
          for i in range(len(filenames)):
                 myTable.add_row([f"{filenames[i]}", f"{filenames_values[i]}"])
          print(myTable)

          print("-------------------------------")
          print('\033[1m' + "In the above table, the red plagiarism percentages, if any, indicate that the plagiarism threshold of 30% has been exceeded!")
          print("Thus, those files are plagiarised")
          print()
          print()
          selection = input("Do you wish to use another file as the base file? y/n: ").lower()
          if selection == "n":
                print("Thank you for using our plagiarism checker!")
                break
          elif selection == "y":
                continue

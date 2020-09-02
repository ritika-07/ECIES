# Core Packages
import tkinter as tk
from tkinter import *
from tkinter import ttk #for tab creation using tkinter
from tkinter.scrolledtext import *
import tkinter.filedialog

# Other pkg
import time
timestr = time.strftime("%Y%m%d-%H%M%S")

# NLP Pkgs
from spacy_summarization import text_summarizer
from gensim.summarization import summarize
from nltk_summarization import nltk_summarizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

# Web Scraping Pkg
from bs4 import BeautifulSoup
from urllib.request import urlopen

#packages for ECIES
from ecies.utils import generate_eth_key
from ecies import encrypt, decrypt
import binascii

def sumy_summary(docx):
	parser = PlaintextParser.from_string(docx, Tokenizer("english"))
	lex_summarizer = LexRankSummarizer()
	summary = lex_summarizer(parser.document, 3)
	summary_list = [str(sentence) for sentence in summary]
	result=''.join(summary_list)
	return result

# Structure and Layout
window = Tk()
window.title("Encryption/Decryption using ECIES")
window.geometry("900x600")
window.config(background='black')

style = ttk.Style(window)
style.configure('lefttab.TNotebook', tabposition='wn') #tabs positioned west-north


# TAB LAYOUT
tab_control = ttk.Notebook(window,style='lefttab.TNotebook')
 
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab3 = ttk.Frame(tab_control)
tab4 = ttk.Frame(tab_control)
tab5 = ttk.Frame(tab_control)
tab6 = ttk.Frame(tab_control)

# ADD TABS TO NOTEBOOK
tab_control.add(tab1, text=f'{"Home":^40s}')
tab_control.add(tab3, text=f'{"Plain Text":^30s}')
tab_control.add(tab4, text=f'{"File Upload":^37s}')
tab_control.add(tab5, text=f'{"URL analysis":^33s}')
tab_control.add(tab6, text=f'{"Alternate Algorithms":^32s}')

label1 = Label(tab1, text= 'About',padx=5, pady=5)
label1.grid(column=1, row=0, pady=5)

label3 = Label(tab3, text= 'Plain text summarisation and Ecryption/Decryption',padx=5, pady=5)
label3.grid(column=1, row=0, pady=5)

label4 = Label(tab4, text= 'File summarisation and Ecryption/Decryption',padx=5, pady=5)
label4.grid(column=1, row=0, pady=5)

label5 = Label(tab5, text= 'URL summarisation and Ecryption/Decryption',padx=5, pady=5)
label5.grid(column=1, row=0, pady=5)

label6 = Label(tab6, text= 'Multi-Algorithm Comparison',padx=5, pady=5)
label6.grid(column=1, row=0, pady=5)

tab_control.pack(expand=1, fill='both')

######
# Functions for candidate information tab
def get_summary():
	raw_text = str(entry.get('1.0',tk.END))
	final_text = text_summarizer(raw_text)
	print(final_text)
	result = '\nSummary:{}'.format(final_text)
	tab3_display.insert(tk.END,result)

def clear_text():
	entry.delete('1.0',END)

def clear_display_result():
	tab3_display.delete('1.0',END)

def save_summary():
	raw_text = str(entry.get('1.0',tk.END))
	final_text = text_summarizer(raw_text)
	file_name = 'CandidateInfo_'+ timestr + '.txt'
	with open(file_name, 'w') as f:
		f.write(final_text)
	result = '\nName of file: {}'.format(file_name)
	tab3_display.insert(tk.END,result)
############################################ fml
def encrypt_text():
	raw_text = str(entry.get('1.0',tk.END))
	raw_text= bytes(raw_text,'utf-8')
	privKey = generate_eth_key()
	privKeyHex = privKey.to_hex()
	pubKeyHex = privKey.public_key.to_hex()
	encrypted = encrypt(pubKeyHex, raw_text)
	encrypted = binascii.hexlify(encrypted)
	result = '\nEncrypted text:{}'.format(encrypted)
	tab3_display.insert(tk.END,result)
	result1 = '\nDecryption private key:{}'.format(privKeyHex)
	tab3_display1.insert(tk.END,result1)

def decrypt_text():
	encrypted = str(entry.get('1.0',tk.END))
	encrypted= bytes(encrypted,'utf-8').strip()
	encrypted = binascii.unhexlify(encrypted)
	privKeyHex= str(tab3_display1.get('1.0',tk.END)).strip()
	decrypted = decrypt(privKeyHex, encrypted)
	result = '\nDecrypted text:{}'.format(decrypted)
	tab3_display.insert(tk.END,result)


#####
#Functions for candidate file tab
def openfiles():
	file1 = tkinter.filedialog.askopenfilename(filetypes=(("Text Files",".txt"),("All files","*")))
	read_text = open(file1).read()
	displayed_file.insert(tk.END,read_text)

# for reset button
def clear_text_file():
	displayed_file.delete('1.0',END)

# Clear Result of Functions
def clear_text_result():
	tab4_display_text.delete('1.0',END)

def get_file_summary():
	raw_text = displayed_file.get('1.0',tk.END)
	final_text = text_summarizer(raw_text)
	result = '\nSummary:{}'.format(final_text)
	tab4_display_text.insert(tk.END,result)

#####
#Functions for Candidate URL TAB
def clear_url_entry():
	url_entry.delete(0,END)

def clear_url_display():
	tab5_display_text.delete('1.0',END)

# Fetch Text From Url
def get_text():
	raw_text = str(url_entry.get())
	page = urlopen(raw_text)
	soup = BeautifulSoup(page)
	fetched_text = ' '.join(map(lambda p:p.text,soup.find_all('p')))
	url_display.insert(tk.END,fetched_text)

def get_url_summary():
	raw_text = url_display.get('1.0',tk.END)
	final_text = text_summarizer(raw_text)
	result = '\nSummary:{}'.format(final_text)
	tab5_display_text.insert(tk.END,result)	

#####
# COMPARER FUNCTIONS
def clear_compare_text():
	entry1.delete('1.0',END)

def clear_compare_display_result():
	tab6_display.delete('1.0',END)

def use_spacy():
	raw_text = str(entry1.get('1.0',tk.END))
	final_text = text_summarizer(raw_text)
	print(final_text)
	result = '\nSpacy Summary:\n{}\n'.format(final_text)
	tab6_display.insert(tk.END,result)

def use_nltk():
	raw_text = str(entry1.get('1.0',tk.END))
	final_text = nltk_summarizer(raw_text)
	print(final_text)
	result = '\nNLTK Summary:\n{}\n'.format(final_text)
	tab6_display.insert(tk.END,result)

def use_gensim():
	raw_text = str(entry1.get('1.0',tk.END))
	final_text = summarize(raw_text)
	print(final_text)
	result = '\nGensim Summary:\n{}\n'.format(final_text)
	tab6_display.insert(tk.END,result)

def use_sumy():
	raw_text = str(entry1.get('1.0',tk.END))
	final_text = sumy_summary(raw_text)
	print(final_text)
	result = '\nSumy Summary:\n{}\n'.format(final_text)
	tab6_display.insert(tk.END,result)
		

# Home tab
about_label = Label(tab1,text="Our Project:\n\nEncryption/Decryption using ECIES",pady=5,padx=5)
about_label.grid(column=1,row=1, pady=5)
about_label = Label(tab1,text="Made By:\n1. Ritika Kayal - 18BCE2518\n2. Srinivas\n3. Amritanshi",pady=5,padx=5)
about_label.grid(column=1,row=2, pady=5)

#BUTTONS
b0=Button(tab1,text="Close", width=12,command=window.destroy)
b0.grid(row=4,column=1,padx=10,pady=10)

# Plain text Tab
l1=Label(tab3,text="Enter Text")
l1.grid(row=2,column=1)

entry=ScrolledText(tab3,height=10)
entry.grid(row=3,column=0,columnspan=3,padx=5,pady=5)

# BUTTONS
button1=Button(tab3,text="Reset",command=clear_text, width=12)
button1.grid(row=5,column=0,padx=10,pady=10)

button2=Button(tab3,text="Summarize",command=get_summary, width=12)
button2.grid(row=5,column=1,padx=10,pady=10)

button3=Button(tab3,text="Clear Result", command=clear_display_result, width=12)
button3.grid(row=5,column=2,padx=10,pady=10)

button4=Button(tab3,text="Save", command=save_summary, width=12)
button4.grid(row=6,column=1,padx=10,pady=10)

button5=Button(tab3,text="Encrypt", command=encrypt_text, width=12)
button5.grid(row=7,column=0,padx=10,pady=10)

button6=Button(tab3,text="Decrypt", command=decrypt_text, width=12)
button6.grid(row=7,column=2,padx=10,pady=10)

# Display Screen For Result
tab3_display = ScrolledText(tab3, height=10)
tab3_display.grid(row=8,column=0, columnspan=3,padx=5,pady=5)

tab3_display1 = ScrolledText(tab3, height=5)
tab3_display1.grid(row=9,column=0, columnspan=3,padx=5,pady=5)


#Candidate file processing tab
l1=Label(tab4,text="Open File To Summarize")
l1.grid(row=1,column=1)

displayed_file = ScrolledText(tab4,height=10)
displayed_file.grid(row=2,column=0, columnspan=3,padx=5,pady=5)

# BUTTONS FOR SECOND TAB/FILE READING TAB
b0=Button(tab4,text="Open File", width=12, command=openfiles)
b0.grid(row=4,column=0,padx=10,pady=10)

b1=Button(tab4,text="Reset", width=12,command=clear_text_file)
b1.grid(row=4,column=1,padx=10,pady=10)

b2=Button(tab4,text="Summarize", width=12,command=get_file_summary)
b2.grid(row=5,column=1,padx=10,pady=10)

b3=Button(tab4,text="Clear Result", width=12,command=clear_text_result)
b3.grid(row=4,column=2,padx=10,pady=10)

# Display Screen
tab4_display_text = ScrolledText(tab4,height=10)
tab4_display_text.grid(row=7,column=0, columnspan=3,padx=5,pady=5)

# Allows you to edit
tab4_display_text.config(state=NORMAL)


# Candidate URL TAB
l1=Label(tab5,text="Enter URL To Summarize")
l1.grid(row=1,column=0)

raw_entry=StringVar()
url_entry=Entry(tab5,textvariable=raw_entry,width=30)
url_entry.grid(row=1,column=1)

# BUTTONS
button1=Button(tab5,text="Reset",command=clear_url_entry, width=12,bg='#03A9F4')
button1.grid(row=4,column=0,padx=10,pady=10)

button2=Button(tab5,text="Get Text",command=get_text, width=12,bg='#03A9F4')
button2.grid(row=4,column=1,padx=10,pady=10)

button3=Button(tab5,text="Clear Result", command=clear_url_display,width=12,bg='#03A9F4')
button3.grid(row=4,column=2,padx=10,pady=10)

button4=Button(tab5,text="Summarize",command=get_url_summary, width=12,bg='#03A9F4')
button4.grid(row=5,column=1,padx=10,pady=10)

# Display Screen For Result
url_display = ScrolledText(tab5,height=10)
url_display.grid(row=7,column=0, columnspan=3,padx=5,pady=5)


tab5_display_text = ScrolledText(tab5,height=10)
tab5_display_text.grid(row=10,column=0, columnspan=3,padx=5,pady=5)


# Alternate algorithms tab
l1=Label(tab6,text="Enter Text To Summarize")
l1.grid(row=1,column=1)

entry1=ScrolledText(tab6,height=10)
entry1.grid(row=2,column=0,columnspan=3,padx=5,pady=5)

# BUTTONS
button1=Button(tab6,text="Reset",command=clear_compare_text, width=12,bg='#03A9F4')
button1.grid(row=4,column=0,padx=10,pady=10)

button2=Button(tab6,text="SpaCy",command=use_spacy, width=12,bg='red')
button2.grid(row=4,column=1,padx=10,pady=10)

button3=Button(tab6,text="Clear Result", command=clear_compare_display_result,width=12,bg='#03A9F4')
button3.grid(row=5,column=0,padx=10,pady=10)

button4=Button(tab6,text="NLTK",command=use_nltk, width=12,bg='#03A9F4')
button4.grid(row=4,column=2,padx=10,pady=10)

button4=Button(tab6,text="Gensim",command=use_gensim, width=12,bg='#03A9F4')
button4.grid(row=5,column=1,padx=10,pady=10)

button4=Button(tab6,text="Sumy",command=use_sumy, width=12,bg='#03A9F4')
button4.grid(row=5,column=2,padx=10,pady=10)


# Display Screen For Result
tab6_display = ScrolledText(tab6,height=10)
tab6_display.grid(row=7,column=0, columnspan=3,padx=5,pady=5)


window.mainloop()
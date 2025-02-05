import sqlite3
import re
import unicodedata
import codecs
import os

# Different bible translation in Downloads folder
#conn = sqlite3.connect(r'C:\Users\jcasallas\Downloads\RVR60.SQLite3')
#conn = sqlite3.connect(r'C:\Users\jcasallas\Downloads\NVI1984.SQLite3')
#conn = sqlite3.connect(r'C:\Users\jcasallas\Downloads\DHHD.SQLite3')
conn = sqlite3.connect(r'C:\Users\jcasallas\Downloads\NTV.SQLite3')

cursor = conn.cursor()
sql_books = 'select * from books'

books_tup = cursor.execute(sql_books)


line1 = "var bible_data = [\n"
last_line = "]"
ari = "\"ari\": "
name = "\"name\": "
verse = "\"verse\": "



bk_idx = 0
bkr= [10,20]
bk_num = []
bk_name = []
for bk in books_tup:
    bk_num.append(bk[0])
    bk_name.append(bk[3]) # RV60 and NTV
    #bk_name.append(bk[2]) #dhh and nvi name is pos 2

#f =  codecs.open("es_rvr.js", "w","utf-8")
#f =  codecs.open("es_dhhd.js", "w","utf-8")
#f =  codecs.open("es_nvi.js", "w","utf-8")
f =  codecs.open("es_ntv.js", "w","utf-8")
f.write(line1)
# reading thru books 
for bk in bk_num:
    print("Book: ", bk_idx, " bk = ", bk)
    sql_verses = "select * from verses where book_number =" + str(bk)
    print(sql_verses)
    verses = cursor.execute(sql_verses)
    
    # loop through each book, verses and chapters
    for v in verses:
        f.write("{\n")
        ari_val = ari + "\"" + str(bk_idx) + ":" + str(v[1]) + ":" + str(v[2]) + "\",\n"
        f.write(ari_val)
        verse_clean  = re.sub("[<[].*?[]>]","", v[3])
        verse_clean = re.sub("\"","",verse_clean)
        name_val = name + "\"" + bk_name[bk_idx] + " " + str(v[1]) + ":" + str(v[2]) + "\",\n"
        f.write(name_val)
        verse_val =   verse + "\"" + verse_clean + "\"\n"
        f.write(verse_val)
        f.write("},\n")
    bk_idx += 1

f.seek(-2,os.SEEK_END)  
f.write("\n]")

f.close()

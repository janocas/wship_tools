import sqlite3
import re
import unicodedata
import codecs
import os

# connecting with DBs located in Downloads
conn = sqlite3.connect(r'C:\Users\jcasallas\Downloads\RVR60.SQLite3')
#conn = sqlite3.connect(r'C:\Users\jcasallas\Downloads\NVI1984.SQLite3')
#conn = sqlite3.connect(r'C:\Users\jcasallas\Downloads\DHHD.SQLite3')
#conn = sqlite3.connect(r'C:\Users\jcasallas\Downloads\NTV.SQLite3')

cursor = conn.cursor()
sql_books = 'select * from books'
books_tup = cursor.execute(sql_books)

# UTF-8 is accepted widely than latin
line1 = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
#line1 = "<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>\n"

line2 = "<bible>\n"
last_line = "</bible>"

bk_idx = 0
bk_num = []
bk_name = []
for bk in books_tup:
    bk_num.append(bk[0])
    bk_name.append(bk[3]) # RV60 and NTV
    #bk_name.append(bk[2]) #dhh and nvi name is pos 2


f =  codecs.open("RVR60", "w","utf-8")
#f =  codecs.open("DHH", "w","utf-8")
#f =  codecs.open("NTV", "w","utf-8")
f.write(line1)
f.write(line2)


for bk in bk_num:
    print("Book: ", bk_idx, " bk = ", bk)
    sql_verses = "select * from verses where book_number =" + str(bk)
    print(sql_verses)
    bk_xml_name = "<b n=\"" + bk_name[bk_idx] + "\">\n"
    f.write(bk_xml_name)
    verses = cursor.execute(sql_verses)
    chap_idx = 1 # temp vairable holding current chapter
    chap_xml = "<c n=\"" + str(chap_idx) + "\">\n"
    f.write(chap_xml)
    
    for v in verses: 
        # Print verse if chapter has not changed
        if (v[1] == chap_idx):
            verse_clean  = re.sub("[<[].*?[]>]","", v[3])
            verse_to_wrt = "<v n=\"" + str(v[2]) + "\">" + verse_clean + "</v>\n"
            f.write(verse_to_wrt)
        # if there is new chapter close previous chapter xml and, open chapter xml and  print the 1st verse of next chapter.
        else:
            f.write("</c>\n")
            chap_xml = "<c n=\"" + str(v[1]) + "\">\n"
            f.write(chap_xml)
            verse_clean  = re.sub("[<[].*?[]>]","", v[3])
            verse_to_wrt = "<v n=\"" + str(v[2]) + "\">" + verse_clean + "</v>\n"
            f.write(verse_to_wrt)
        chap_idx = v[1]
    #After each book print ends parents xmls
    f.write("</c>\n")
    f.write("</b>\n")
    bk_idx += 1
f.write(last_line)

f.close()

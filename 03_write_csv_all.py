#!/usr/bin/python3
import csv,json
import sqlite3
import sys

########################################
# Вывод  информации в CSV ANSI кодировки
########################################
conn = sqlite3.connect("./db/all_fields.db") # или :memory: чтобы сохранить в RAM

if(sys.platform == 'linux'):
    encoding = 'utf-8'
else:
    encoding = 'cp1251'

csvfile = open('./csv/data.csv', 'w', encoding='cp1251', errors='replace', newline='')

fields={}
fields["id"] = 'ID'
fields["f0"] = 'Вид документа'
fields["f1"] = 'Фамилия'
fields["f2"] = 'Имя'
fields["f3"] = 'Отчество'
fields["f4"] = 'Дата рождения/Возраст'
fields["f5"] = 'Место рождения'
fields["f6"] = 'Дата и место призыва'
fields["f7"] = 'Последнее место службы'
fields["f8"] = 'Воинское звание'
fields["f9"] = 'Причина выбытия'
fields["f10"] = 'Дата выбытия'

cursor = conn.cursor()

cursor.execute("SELECT count(*) FROM search_ids")
count_row = cursor.fetchone()[0]
print(count_row)

cur = conn.execute('select * from search_ids  where flag=1 limit 1')
names = list(map(lambda x: x[0], cur.description))
print(names)
header = ''
for field in fields:
    header += '"'+fields[field]+'";'
csvfile.write(header+'\n')

# Для больших объемов информации перевел на дискретную обработку

limit=50000
count=0
offset=0
while offset <  count_row:
	print(limit,offset)
	#offset+=limit
	str_cmd = "SELECT * FROM search_ids where flag=1 limit {} offset {}".format(limit,offset)
	cursor.execute(str_cmd)
	for i in cursor.fetchall():
		print ('{} из {}'.format(count,count_row))
		f_str = ''
		for y in range(0,12):
			if(str(i[y])=="None"):
				f_str += '"";'
			else:
        			f_str += '"'+str(i[y])+'";'
		csvfile.write(f_str+'\n')
		count+=1
	offset+=limit

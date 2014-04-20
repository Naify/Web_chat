#!/usr/bin/python
# -*- coding: utf-8 -*-


import os
import sys
import subprocess
import csv
import time
import cgi
import cgitb

cgitb.enable()
# Извлечение данных о запросе
data = cgi.FieldStorage()

# Извлечение полей запроса
action = data.getvalue("action") 
name = data.getvalue("name") 
message = data.getvalue("message")
row = data.getvalue("row")

def outdiv():
	# Вывод сообщения и добавление его в историю
	f = open("hist.csv","a")
	writer = csv.writer(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	# Запись в фаил
	writer.writerow([name,message])
	# Увеличение числа рядов в файле
	rowW = int(row) + 1
	# Json ответ
	print "Content-type:application/json\r\n" 
	print '{actions: {name:" %s ",message:" %s "}, row:" %d "}' % (name,message,rowW)
	f.close()

def outhis(row):
	# Вывод истории
	print "Content-type:application/json\r\n"
	print '{actions: ['
	f = open("hist.csv","r")
	reader = csv.reader(f, delimiter=' ', quotechar='|')
	# Формирование двумерного массива из reader
	lines = list(reader)
	rowFile = len(lines) # Количество рядов в файле
	rowInOut = int(row)  # № ряда присланный от клиента
	count = 0
	
	for rows in lines:
		count += 1
		if count > rowInOut:
			print  '{name:"' + rows[0] + '",message:"' + rows[1] + '"},'
			rowInOut += 1
	
	print ']'
	print ',row:" %d "}' % (rowInOut)
	
	f.close()

def newchaty(row):
	#Функция для вывода последних только 10 строк истории при оскрытии чата
	print "Content-type:application/json\r\n"
	print '{actions: ['
	f = open("hist.csv","r")	
	reader = csv.reader(f, delimiter=' ', quotechar='|')
	lines = list(reader)
	rowFile = len(lines)
	rowInOut = int(row)
	count = 0
	count2 = 0	
	for rows in lines:
		count += 1
		if count > rowInOut:			
			if rowFile - count2 <= 10:
				print  '{name:"' + rows[0] + '",message:"' + rows[1] + '"},'
			rowInOut += 1
			count2 += 1
	print ']'
	print ',row:" %d "}' % (rowInOut)	
	f.close()

	
def json_answer():
	if action == "sendmsg" :
		# Вывод сообщения и добавление его в историю
		outdiv()
	elif action == "sendhis" :
		# Вывод истории
		outhis(row)
	elif action == "newchat":
		# Вывод последних 10 строк истории
		newchaty(row)

json_answer()

sys.exit(0)
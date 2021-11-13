#!/bin/bash

LOG_FILE="access.log"
RES_FILE="res.txt"

#Общее количество запросов
echo "Общее количество запросов:" > $RES_FILE
wc -l $LOG_FILE | awk '{print $1}' >> $RES_FILE
echo "--------------------------------------------" >> $RES_FILE

#Общее количество запросов по типу
echo "Общее количество запросов по типу:" >> $RES_FILE
cat $LOG_FILE | awk '{print $6}' | cut -c 2- | sort | uniq -c |
while read line; do
	echo "Тип запроса:" >> $RES_FILE
	echo $line | awk '{print $2}' >> $RES_FILE
	echo "Число запросов:" >> $RES_FILE
	echo $line | awk '{print $1}' >> $RES_FILE
	echo >> $RES_FILE
done
echo "--------------------------------------------" >> $RES_FILE


#Топ 10 самых частых запросов
echo "Топ 10 самых частых запросов:" >> $RES_FILE
cat $LOG_FILE | awk '{print $7}' | sort | uniq -c | sort -rnk1 | head | 
while read line; do
	echo "url:" >> $RES_FILE
	echo $line | awk '{print $2}' >> $RES_FILE
	echo "Число запросов:" >> $RES_FILE
	echo $line | awk '{print $1}' >> $RES_FILE
	echo >> $RES_FILE
done
echo "--------------------------------------------" >> $RES_FILE

#Топ 5 самых больших по размеру запросов, которые завершились клиентской (4ХХ) ошибкой
echo "Топ 5 самых больших по размеру запросов, которые завершились клиентской (4ХХ) ошибкой:" >> $RES_FILE
cat $LOG_FILE | awk '$9 ~ /4[0-9]{2}/' | sort -rnk10 | head -n 5 |
while read line; do
	echo "url:" >> $RES_FILE
	echo $line | awk '{print $7}' >> $RES_FILE
	echo "Статус код:">> $RES_FILE
	echo $line | awk '{print $9}' >> $RES_FILE
	echo "Размер запроса:" >> $RES_FILE
	echo $line | awk '{print $10}' >> $RES_FILE
	echo "IP адрес:" >> $RES_FILE
	echo $line | awk '{print $1}' >> $RES_FILE
	echo >> $RES_FILE
done
echo "--------------------------------------------" >> $RES_FILE

#Топ 5 пользователей по количеству запросов, которые завершились серверной (5ХХ) ошибкой
echo "Топ 5 пользователей по количеству запросов, которые завершились серверной (5ХХ) ошибкой:" >> $RES_FILE
# Забавно - у меня здесь sort -rn отрабатывает некорректно, видимо, наткнулся на баг macos
# В linux вроде все ок
cat $LOG_FILE | awk '{if ($9 ~ /5../) print $1}' | sort | uniq -c | sort -rn | head -n 5 |  
while read line; do
	echo "ip:" >> $RES_FILE
	echo $line | awk '{print $2}' >> $RES_FILE
	echo "Число запросов:" >> $RES_FILE
	echo $line | awk '{print $1}' >> $RES_FILE
	echo >> $RES_FILE
done

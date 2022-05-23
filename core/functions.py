import os
import cv2
import random
import numpy as np
import tensorflow as tf
import pytesseract
from core.utils import read_class_names
from core.config import cfg
import pygame

import mysql.connector
import datetime
import openpyxl
import pandas as pd


def sound_s(key):
    print("sound:",key)
    # from playsound import playsound
    file_1 = "1.mp3"
    file_2 = "2.mp3"
    if key=="NoMask":
        pygame.mixer.init()
        if pygame.mixer.music.get_pos() == -1 :
            pygame.mixer.music.load(file_1)
            pygame.mixer.music.play()
        else:
            pass

    elif key=="Wearing incorrectly":
        pygame.mixer.init()
        if pygame.mixer.music.get_pos() == -1 :
            pygame.mixer.music.load(file_2)
            pygame.mixer.music.play()
        else:
            pass
        
# ฟังก์ชันนับจำนวนอ็อบเจ็กต์ สามารถคืนค่าจำนวนคลาสทั้งหมดหรือนับต่อคลาสได้
def count_objects(data, by_class = False, allowed_classes = list(read_class_names(cfg.YOLO.CLASSES).values())):
    boxes, scores, classes, num_objects = data

    #create dictionary to hold count of objects
    counts = dict()
    
    # ถ้า by_class = True ให้นับวัตถุต่อคลาส
    if by_class:
        class_names = read_class_names(cfg.YOLO.CLASSES)
        # print("classname",class_names) #classname {0: 'NoMask', 1: 'KN95', 2: 'Cloth', 3: 'Surgical', 4: 'Wearing incorrectly'}
        # วนซ้ำตามจำนวนวัตถุทั้งหมดที่พบ
        for i in range(num_objects):
            # แปลงเป็นชื่อคลาสที่เกี่ยวข้อง
            class_index = int(classes[i])
            class_name = class_names[class_index]
            
            # print("sssss",class_name,allowed_classes)
            if class_name in allowed_classes:
                counts[class_name] = counts.get(class_name, 0) + 1 
            else:
                continue
            
    # อื่น ๆ นับรวมวัตถุที่พบ
    else:
        counts['total object'] = num_objects
    
    return counts
try:
    mydb = mysql.connector.connect(
        host="us-cdbr-east-05.cleardb.net",
        user="bee2562bca911c",
        password="41039f7c",
        database="heroku_c24e1a9450f3bbd"
        )
    mycursor = mydb.cursor()
    print("connect mysql successfully")
except:
    print("connect mysql error")

def save_data_(img, data, allowed_classes):
    boxes, scores, classes, num_objects = data
    class_names = read_class_names(cfg.YOLO.CLASSES)
    # print("class_names",classes)
    
    counts = dict()
    # print("allowed_classes",allowed_classes)
    date_now = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")
    time_now = datetime.datetime.strftime(datetime.datetime.now(), "%H:%M:%S")
    # จัดเตรียมลำดับของจำนวนเต็มตามอาร์กิวเมนต์ของฟังก์ชัน
    for i in range(num_objects):
        # get count of class for part of image name
        class_index = int(classes[i])
        class_name = class_names[class_index]
        # print("Classname detection",class_name)
        if class_name in allowed_classes:
            counts[class_name] = counts.get(class_name, 0) + 1
            # print("counts",counts) #counts {'NoMask': 1}
            for key, value in counts.items():
                # print("xxxxxx:",key,value)
                if len(key) != 0 & value != None: 
                    # df = pd.read_excel('detections2.xlsx', engine='openpyxl',)
                    # df = df.append({"จำนวน": value ,"ประเภทหน้ากาก": key, "วันที่": date_now, "เวลา" : time_now }, ignore_index=True)
                    # df.to_excel("detections2.xlsx",index=False)
                    try:
                        sql = "INSERT INTO datamask (masktype, amount, date_d, time_t) VALUES (%s, %s, %s, %s)"
                        val = (key, value, date_now, time_now)
                        mycursor.execute(sql, val)
                        mydb.commit()
                        print("connect mysql successfully")
                    except:
                        print("connect mysql error")
                
        else:
            continue

# CREATE TABLE `heroku_c24e1a9450f3bbd`.`datamask` (
# id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
# masktype VARCHAR(50) NOT NULL,
# amount int(30) NOT NULL,
# date_d date,
# time_t time)
# ENGINE = InnoDB
# DEFAULT CHARACTER SET = utf8;
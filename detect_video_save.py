from fileinput import filename
import os

from django.urls import path
# comment out below line to enable tensorflow outputs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import time
import tensorflow as tf
physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
from absl import app
import core.utils as utils
from core.functions import *
from tensorflow.python.saved_model import tag_constants
import cv2
import numpy as np
from tensorflow.compat.v1 import ConfigProto
import datetime 
import random
import string


def main(_argv):
    config = ConfigProto() #ใช้ ConfigProto() เพื่อกำหนดค่าเซสชัน
    config.gpu_options.allow_growth = True #จัดสรรหน่วยความจำให้กับเซสชันเท่าที่จำเป็นเท่านั้น
    input_size = 416
    video_path = 0
    
    
    saved_model_loaded = tf.saved_model.load('./checkpoints/yolov4-tiny-416', tags=[tag_constants.SERVING])
    infer = saved_model_loaded.signatures['serving_default']

    # begin video capture
    try:
        vid = cv2.VideoCapture(int(video_path))
    except:
        vid = cv2.VideoCapture(video_path)

    out = None

    videoname = string.ascii_uppercase
    vname = ''.join(random.choice(videoname) for i in range(10))
    path_vdo = "./detections/"
    
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(str(path_vdo+vname+".avi"),fourcc, 15, (640,480))         


    frame_num = 0
    while True:
        return_value, frame = vid.read()
        if return_value:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cv2.normalize(frame, frame, 0, 255, cv2.NORM_MINMAX)
            frame = cv2.flip(frame,1)
            frame_num += 1
        else:
            print('Video has ended or failed, try a different video format!')
            break

        image_data = cv2.resize(frame, (input_size, input_size))
        image_data = image_data / 255.
        image_data = image_data[np.newaxis, ...].astype(np.float32)
        
        start_time = time.time()


        batch_data = tf.constant(image_data)
        # print("batch data",batch_data) #การเปรียบเทียบความถูกต้องของ filter cnn กับ image_data
        pred_bbox = infer(batch_data) #การบอกเส้น box การตรวจจับ
        # print("pred bbox",pred_bbox)
        for key, value in pred_bbox.items():
            boxes = value[:, :, 0:4]
            # print("key",key)
            # print("value",value) #ค่าความมั่นใจของการเปรียบเทียบ
            pred_conf = value[:, :, 4:]
            # print("pred_conf",pred_conf)


        boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
            boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
            scores=tf.reshape(
                pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
            max_output_size_per_class=50,
            max_total_size=50,
            iou_threshold=0.20,
            score_threshold=0.60
        )

        # รูปแบบกล่องขอบเขตจาก ymin ปกติ, xmin, ymax, xmax ---> xmin, ymin, xmax, ymax
        original_h, original_w, _ = frame.shape
        bboxes = utils.format_boxes(boxes.numpy()[0], original_h, original_w)
        # print("bboxes",bboxes)
        pred_bbox = [bboxes, scores.numpy()[0], classes.numpy()[0], valid_detections.numpy()[0]]
        # print("pred_bbx",pred_bbox) #ค่าความมั่นใจการตรวจจับ

        # อ่านชื่อคลาสทั้งหมดจาก config
        class_names = utils.read_class_names(cfg.YOLO.CLASSES)
        # print(class_names)

        # โดยค่าเริ่มต้น อนุญาตให้คลาสทั้งหมดใน .names file
        allowed_classes = list(class_names.values())
        # print(allowed_classes)

        # บันทึกข้อมูลการตรวจจับทุก
        save_rate = 40 #บันทึกทุก ๆ เฟรม (เช่น บันทึกข้อมูลทุกๆ 10 เฟรม)
        # xxx = frame_num % save_rate
        # print(xxx)
        if frame_num % save_rate == 0:
            save_data_(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), pred_bbox, allowed_classes)
        else:
            pass

        # print(pred_bbox)
        # นับวัตถุที่พบ
        counted_classes = count_objects(pred_bbox, by_class = True, allowed_classes=allowed_classes)
        # วนซ้ำผ่าน dict และ print
        for key, value in counted_classes.items():
            print("Number of {}s: {}".format(key, value))
            sound_s(key)
        
        image = utils.draw_bbox(frame, pred_bbox, False, counted_classes, allowed_classes=allowed_classes, read_plate=False)

        time_ref = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
        fps = 10 / (time.time() - start_time)
        # print(fps)
        #ฟังก์ชั่นถูกใช้เมื่อเราต้องการแปลงอินพุตเป็นอาร์เรย์ อินพุตสามารถเป็น
        print("FPS: %.2f" % fps,time_ref)
        result = np.asarray(image)
        # cv2.namedWindow("Detect TypeMask", cv2.WINDOW_AUTOSIZE)
        cv2.namedWindow("Detect TypeMask", cv2.WND_PROP_FULLSCREEN)
        # cv2.setWindowProperty("Detect TypeMask",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        result = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        

        cv2.imshow("Detect TypeMask", result)
        
        out.write(result)
        if cv2.waitKey(1) & 0xFF == ord('q'): break

    cv2.destroyAllWindows()

    

if __name__ == '__main__':
    try:
        app.run(main)    
    except SystemExit:
        pass

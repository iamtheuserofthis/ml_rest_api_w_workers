import cv2
import numpy as np
import os
import math
import tensorflow as tf
from tensorflow import keras
from tensorflow.python.keras.backend import set_session
import tensorflow.python.keras.backend  as K



class GenderDetect():
    # model_path =
    def __init__(self, image_dir,
                 model_path='/models/gender_class4.h5',
                 cascade_classifier_xml_path='/models/haarcascade_frontalface_default.xml'):
        self.face_cascade_classifier = cv2.CascadeClassifier(cascade_classifier_xml_path)
        self.image_dir = image_dir
        self.class_labels = {0: "Female", 1: "Male"}

        self.sess = tf.Session()
        self.graph = tf.get_default_graph()
        set_session(self.sess)
        self.model_gender = keras.models.load_model(model_path)
        self.model_gender._make_predict_function()

    def face_detect_preprocess(self, img_id):
        """

        Parameters
        ----------
        img_id - Id of the image, which is a uuid generated value
        img_path - The path of the directory where the image has been uploaded to

        Returns
        -------
            dict with the following keys
            - face

            key-type: str
            A key for the detail of the face detected

            value-type: dict
                A dictionary with following info:
                    `face_coord` - Array of the image coordinates.
                    `processed_img` - The cropped preprocessed image
        """
        complete_img_path = os.path.join(self.image_dir, img_id)
        img = cv2.imread(complete_img_path)

        if img is None:
            raise ValueError("Image %s Does not exist" % complete_img_path)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        rects = self.face_cascade_classifier.detectMultiScale3(img, 1.1, 8, outputRejectLevels=True)
        cropped_res = {}
        for i, roi in enumerate(rects[0]):
            x, y, w, h = roi
            padding_y = math.floor(h / 5)
            padding_x = math.floor(w / 6)
            crop_img = img[y - padding_y:y + h, x - padding_x:x + w + padding_x]

            if crop_img is None:
                raise ValueError("None type image")
            if crop_img.shape[0] == 0 | crop_img.shape[1] == 0:
                raise ValueError("bad image")
            processed_img = cv2.equalizeHist(cv2.resize(crop_img, (150, 150)))
            img_test_padded = cv2.cvtColor(processed_img, cv2.COLOR_GRAY2RGB)
            norm_img = img_test_padded / 255
            test_set = np.expand_dims(norm_img, 0)
            curr_index = 'face' + str(i)
            cropped_res[curr_index] = {}
            cropped_res[curr_index]['face_coord'] = roi.tolist()
            cropped_res[curr_index]['processed_img'] = test_set
        return cropped_res

    def gender_detect_one(self, image_id):
        """
             Returns:
                 dict of image results for all the detected faces in the image

             -------
             Processes the images from the image queue using the following steps
             1. Creates a new K.session() for the keras processing.

            todo - Make the method of accessing the image directory generalised
            """
        res_record = {}
        with self.graph.as_default():
            set_session(self.sess)

            cropped_preprocessed_img = self.face_detect_preprocess(image_id)
            for i in cropped_preprocessed_img.keys():
                res_record[i] = {}
                res_record[i]['face_coord'] = cropped_preprocessed_img[i]['face_coord']
                res_record[i]['gender'] = self.class_labels[
                    self.model_gender.predict_classes(cropped_preprocessed_img[i]['processed_img'])[0][0]]
                res_record[i]['confidence'] = float(
                    self.model_gender.predict_proba(cropped_preprocessed_img[i]['processed_img'])[0][0])
        return res_record

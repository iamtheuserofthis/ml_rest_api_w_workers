import cv2

import os
class FaceDetectModel:
    #fix the model path,
    def __init__(self, model_path='/models/haarcascade_frontalface_default.xml'):
        print('work_dir',os.getcwd())
        self.haar_cascade_classifier = cv2.CascadeClassifier(model_path)

    def face_detect(self, filePath):
        numFaces, numNonFace, res_detect = 0, 0, []
        try:
            img = cv2.imread(filePath)
            if img is not None:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                rects = self.haar_cascade_classifier.detectMultiScale3(gray, 1.1, 8, outputRejectLevels=True)
                for i in rects[0]:
                    res_detect.append(i.tolist())
                numFaces = len(res_detect)
                numNonFace = 0 if (numFaces >= 1) else 1
                print('IMAGE PROCESS RES', numFaces, numNonFace)
            else:
                raise FileNotFoundError("%s NOT FOUND" % filePath)
        except Exception as e:
            raise e
        return {'faces': numFaces, 'non-faces': numNonFace, 'face_list': res_detect}


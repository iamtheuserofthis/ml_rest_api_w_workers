from mrcnn import config
import mrcnn.model as modellib
import skimage
import uuid
import os, time
import json


class PredictConfig(config.Config):
    BACKBONE = "resnet50"
    NAME = 'eval_fingers'
    NUM_CLASSES = 4 + 1
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
    IMAGE_MIN_DIM = 512
    IMAGE_MAX_DIM = 512
    BATCH_SIZE = 1


class ElementDetectionMrcnn:
    def __init__(self, log_dir, model_path):
        cfg = PredictConfig()
        self.model_finger_sign = modellib.MaskRCNN(mode='inference',
                                              model_dir=os.path.join(log_dir, str(uuid.uuid4())),
                                              config=cfg)
        self.model_finger_sign.load_weights(model_path, by_name=True)
        self.model_finger_sign.keras_model._make_predict_function()

    def detect_image(self, path):
        class_name = ['none', 'thumb', 'sign', 'photograph', 'marksbox']
        img = skimage.io.imread(path)
        img = img if (img.shape[2] <= 3) else img[:, :, :3]
        print(img.shape)
        # model_finger_sign._make_predict_function()
        res = self.model_finger_sign.detect([img], verbose=1)

        return list(map(lambda x: {class_name[x[0]]: str(x[1])}, zip(res[0]['class_ids'], res[0]['scores'])))


if __name__ == '__main__':
    edm = ElementDetectionMrcnn('/home/iamtheuserofthis/python_workspace/iaf_image_process/models/log_files', '/home/iamtheuserofthis/python_workspace/iaf_image_process/models/weights_for_fin_v3.h5')
    dir_path = '/home/iamtheuserofthis/untagged_data/thumb2'
    for i in os.listdir(dir_path)[:10]:
        x = edm.detect_image(os.path.join(dir_path, i))
        print(json.dumps(x))
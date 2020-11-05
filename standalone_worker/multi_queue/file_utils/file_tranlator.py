import base64
import os
import uuid
import json


def image_to_json(applicant_cred_id, img_bytes, fin_task):
    x = []
    img_id = str(uuid.uuid4())
    x.append(str(applicant_cred_id))
    x.append(fin_task)
    x.append(img_id)
    x.append(base64.b64encode(img_bytes).decode('utf-8'))
    if len(x) == 0:
        raise ValueError("Image Could not be encrypted")
    return img_id, json.dumps(x)


def decode_img_tag_json(json_img_s):
    """

    Parameters
    ----------
    json_img_s

    Returns
    -------
    Tuple containing:
        - applicant_cred_id
        - image_id
        - base64enc image
    """
    img_arr = json.loads(json_img_s)
    base64_img = base64.b64decode(img_arr[3])
    return img_arr[0], img_arr[1], img_arr[2], base64_img


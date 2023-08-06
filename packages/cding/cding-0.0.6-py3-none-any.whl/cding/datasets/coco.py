import random
from tqdm import tqdm
from pycocotools.coco import COCO 
from pycocotools.cocoeval import COCOeval 


def init_dict(class_name='pole'):
    dataset = {
        "info":{},
        "licenses":[],
        "categories":[{
            "id": 1, 
            "name": class_name,
            "supercategory": 'target'
            }],
        "images":[],
        "annotations":[]
        }
    return dataset

def init_images(file_name, image_id):
    return {
        "file_name": file_name,
        "id": image_id,
        "width": 1920,
        "height": 1080
        }, image_id + 1

def initAnnos(x, y, w, h, image_id, category_id):
    return {'segmentation':[[x,y,x+w,y,x+w,y+h,x,y+h]],
            "area": w*h,
            "bbox": [x,y,w,h], 
            "category_id": 1, 
            "image_id": image_id,
            "id": category_id,
            'iscrowd': 0,}, category_id+1


def gen_whole_dataset(file_names, bboxes):
    """
    file_names: list of str
    bboxes: list of xywh lists, [[[x1,y1,w1,h1], [x2,y2,w2,h2], ...], [], ...], same length of file_names
    """
    image_id, category_id = 0, 0
    dataset = init_dict()
    for i in tqdm(range(len(file_names))):
        one_image, image_id = init_images(file_names[i], image_id)
        dataset['images'].append(one_image)
        for x, y, w, h in bboxes[i]:
            one_anno, category_id = initAnnos(x, y, w, h, image_id-1, category_id)
            dataset['annotations'].append(one_anno)
    return dataset

def random_split_dataset(file_names, bboxes, percent=20, seed=666):
    """
    file_names: list of str
    bboxes: list of xywh lists, [[[x1,y1,w1,h1], [x2,y2,w2,h2], ...], [], ...], same length of file_names
    percent: percent of validation set, 20, int/float
    seed: random seed to split, 666
    return: dict of train_dataset, val_dataset, trainval_dataset
    """
    random.seed(seed)
    random.shuffle(file_names)
    random.seed(seed)
    random.shuffle(bboxes)
    sep = int(len(file_names)*percent/100)
    file_names_val, file_names_train, file_names_trainval = file_names[:sep], file_names[sep:], file_names
    bboxes_val, bboxes_train, bboxes_trainval = bboxes[:sep], bboxes[sep:], bboxes
    train_dataset, val_dataset, trainval_dataset = gen_whole_dataset(file_names_train, bboxes_train), gen_whole_dataset(file_names_val, bboxes_val), gen_whole_dataset(file_names_trainval, bboxes_trainval)
    return train_dataset, val_dataset, trainval_dataset


def eval_coco(res, anno, iou_thresh=[0.5,0,0.5], max_dets=[100,300,1000], area_range=[512, 512]):
    """
    res: result json from model
    anno: annotation json
    iou_thresh: [start, step, end], [0.5, 0, 0.5]
    max_dets: thresholds on max detections per image, [100, 300, 1000]
    area_range: area_range to seperate small, (medium,) large, [512, 512]
    """
    cocoGt = COCO(anno)
    cocoDt = cocoGt.loadRes(res)
    cocoEval = COCOeval(cocoGt, cocoDt, "bbox")
    cocoEval.params.iouThrs=iou_thresh
    cocoEval.params.maxDets=max_dets
    cocoEval.params.areaRng= [[0 ** 2, 1e5 ** 2], [0 ** 2, area_range[0]], [0 ** 2, area_range[0]], [area_range[1], 1e5 ** 2]]
    cocoEval.evaluate()
    cocoEval.accumulate()
    cocoEval.summarize()
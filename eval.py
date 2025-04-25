# from faster_coco_eval.core import COCO
# from fast_coco_api import COCOeval_faster

import coco_eval

# Replace pycocotools with faster_coco_eval
coco_eval.init_as_pycocotools()

from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval

import time
import os
import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description='Evaluate the result of yolo_cwdet_v8248'
    )
    parser.add_argument(
        '--gt_json',
        type=str,
        default='det_dataset/DOTD/coco_json/test_coco_start_1.json',
        help='path to ground truth json file',
    )
    parser.add_argument(
        '--dt_json',
        type=str,
        default='xxx/predictions.json',
        help='path to detection result json file',
    )
    args = parser.parse_args()
    return args


def evaluate(gt_json, dt_json):
    # check file exists
    assert os.path.exists(gt_json), f'{gt_json} not exists'
    assert os.path.exists(dt_json), f'{dt_json} not exists'
    
    coco_gt = COCO(gt_json)
    coco_dt = coco_gt.loadRes(dt_json)
    time1 = time.time()
    print(f'{gt_json} has loaded')
    cocoEval = COCOeval(cocoGt=coco_gt, cocoDt=coco_dt, iouType='bbox')
    cocoEval.evaluate()
    cocoEval.accumulate()
    cocoEval.summarize()
    time2 = time.time()
    print(f'time: {time2-time1} s')
    stats = cocoEval.stats
    return stats


if __name__ == '__main__':
    args = parse_args()
    stats = evaluate(args.gt_json, args.dt_json)
    print(stats)

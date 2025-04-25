# 适用于DTOD、AITOD等遥感数据集的快速coco eval工具
## 0. 说明

该工具基于[faster_coco_eval](https://github.com/MiXaiLL76/faster_coco_eval)
适用于DTOD、AITOD等遥感数据集的快速coco eval工具，可以快速验证预测结果json
实测DTOD数量众多的数据集，测试时间将从2小时缩短至5-10秒
提供coco格式相关的多个小工具

## 1. 安装

```shell
pip install -r requirements.txt
```

## 2. 生成coco格式的真值标注json

先生成coco格式的真值标注json，之后运行eval.py测试coco格式的预测结果
值得注意的是，注意line104行可以对clsid的起始序号进行修改，修改该处选择是否从1开始，如果计算结果出现异常，尝试从0开始
```shell
python yolo2coco.py -i {测试集图片} -l {测试集标签} -s {生成的coco格式的真值标注json位置}
```

## 3. 验证预测结果json

```shell
python eval.py -dt_json {预测结果json} -gt_json {真值标注json}
```
结果包含DTOD指标和AITOD指标
自定义指标的方式：
修改`coco_eval/coco_eval_base.py`中Params类的setDetParams方法可指定待评测目标的`maxdet`以及`areaRng`
修改COCOeval类的summarize方法中的子方法_summarizeDets，可指定不同的指标，_summarize第一个参数如果是1则测评AP，如果是0测评AR，按需增减，同时记得修改_count

## 4. 小工具
- `yolo2coco.py`：将yolo格式的标签转换为coco格式的标签json
- `yolo_dataset_to_coco_format.py`：将yolo格式的数据集重命名，符合coco的06d格式命名，最后转出来的仍是yolo数据集格式
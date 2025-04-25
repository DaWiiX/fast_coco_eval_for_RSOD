# 适用于DTOD、AITOD等遥感数据集的coco eval工具
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
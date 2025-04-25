import os
import shutil
import argparse
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

img_extensions = ['.png', '.jpg', '.jpeg', '.JPG', '.PNG', '.JPEG', '.tif', '.tiff']

def parse_args():
    parser = argparse.ArgumentParser(description='Convert YOLO dataset to COCO format.')
    parser.add_argument('--img_dir', '-i', type=str, required=True, help='Directory of images.')
    parser.add_argument('--label_dir','-l', type=str, required=True, help='Directory of labels.')
    parser.add_argument('--output_path','-o', type=str, required=True, help='Output directory.')
    parser.add_argument('--workers','-w', type=int, default=8, help='Number of worker threads')
    return parser.parse_args()

def process_file(args, label_txt, index):
    """处理单个文件的线程任务"""
    base_name = os.path.splitext(label_txt)[0]
    
    # 查找匹配的图片文件
    img_file = None
    now_ext = None
    for ext in img_extensions:
        candidate = os.path.join(args.img_dir, base_name + ext)
        if os.path.exists(candidate):
            img_file = candidate
            now_ext = ext
            break
    
    if not img_file:
        raise FileNotFoundError(f"No image found for {label_txt}")

    # 生成新文件名
    new_img_name = f"{index:06d}{now_ext}"
    new_img_path = os.path.join(args.output_img_dir, new_img_name)
    new_label_name = f"{index:06d}.txt"
    new_label_path = os.path.join(args.output_label_dir, new_label_name)

    # 执行文件复制操作
    shutil.copy(img_file, new_img_path)
    shutil.copy(os.path.join(args.label_dir, label_txt), new_label_path)
    
    return index  # 返回处理完成的索引

def yolo_dataset_to_coco(args):
    # 创建输出目录
    args.output_label_dir = os.path.join(args.output_path, 'labels')
    args.output_img_dir = os.path.join(args.output_path, 'images')
    os.makedirs(args.output_label_dir, exist_ok=True)
    os.makedirs(args.output_img_dir, exist_ok=True)

    # 获取并排序标签文件列表（确保跨平台一致性）
    label_files = sorted([f for f in os.listdir(args.label_dir) if f.endswith('.txt')])
    
    # 预先生成任务参数（保持顺序）
    tasks = [(label_file, idx) for idx, label_file in enumerate(label_files)]

    # 使用线程池处理
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = []
        for label_file, idx in tasks:
            future = executor.submit(
                process_file, 
                args,
                label_file,
                idx
            )
            futures.append(future)
        
        # 进度条监控
        completed = 0
        progress = tqdm(total=len(futures), desc="Processing", ncols=100)
        for future in as_completed(futures):
            try:
                future.result()
                completed += 1
                progress.update(1)
            except Exception as e:
                progress.close()
                raise RuntimeError(f"Error processing task: {e}") from e
        progress.close()

    print(f"Convert {len(label_files)} label files to COCO format.")

if __name__ == '__main__':
    args = parse_args()
    yolo_dataset_to_coco(args)
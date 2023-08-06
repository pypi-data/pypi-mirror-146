#!/usr/bin/env python
# encoding=utf-8

import re
import random
import exifread

from .logger import *


# 支持的图片后缀
image_exts = {'jpg', 'bmp', 'png', 'jpeg', 'rgb', 'tif', 'heic'}


# 相关说明
def rename_tips():
    print_info(f'## 图标说明')
    print_info()
    print_info(f'> 🈚️ 表示路径不存在')
    print_info(f'> 📁 表示文件夹')
    print_info(f'> 🏞  表示图片')
    print_info(f'> ⏭️  表示跳过，例如该文件名称 无需重命名')
    print_info(f'> ✅ 表示处理成功')
    print_info()


# 将文件重命名
def rename_with_date(path):
    if path is None:
        print_error(f'❌ 请输入 path')
        print_info()
        parser.print_help()
        print_info()
        parser.exit()

    print_info(f'## 开始重命名')
    print_info()
    _rename_with_date(path)


# 将照片重命名
def _rename_with_date(path):
    # 异常处理
    if path is None or not os.path.exists(path):
        print_error(f'🈚️ {path}')
        return

    # 目录，则遍历其下的文件
    if os.path.isdir(path):
        for home, dirs, files in os.walk(path):
            print_verbose()
            print_verbose(f'📁 {home}')
            print_debug(f' ┣━ home = {home}')
            print_debug(f' ┣━ dirs = {dirs}')
            print_debug(f' ┗━ files = {files if len(files) < 20 else len(files)}个')
            for file in files:
                if file == '.DS_Store': continue
                ext = file.split('.')[-1]
                if ext.lower() not in image_exts:
                    print_verbose()
                    print_verbose(f'❓ {home}/{file}')
                    continue
                _rename_with_date(f'{home}/{file}')
        return

    # 图片文件：若文件名 符合目标的命名格式，则跳过
    print_verbose()
    print_verbose(f'🏞  {path}')
    already_renamed = re.match(r'\d{8,}\.\d{3}\.\w+', os.path.basename(path), re.M | re.I)
    if already_renamed:
        print_info(f'⏭️  {path}')
        return

    # 图片文件：读取拍摄时间（用创建时间 兜底）
    img_read = open(path, 'rb')
    img_exif = exifread.process_file(img_read)
    take_date_time = img_exif.get('EXIF DateTimeDigitized')
    print_verbose(f' ┣━ 拍摄日期：{take_date_time}')
    modifi_time = os.path.getmtime(path)
    print_verbose(f' ┣━ 修改日期：{time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(modifi_time))}')
    create_time = os.path.getctime(path)
    print_verbose(f' ┣━ 创建日期：{time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(create_time))}')
    if take_date_time is not None:
        take_time = time.strptime(str(take_date_time), "%Y:%m:%d %H:%M:%S")
    else:
        take_time = time.localtime(create_time)

    # 准备变量
    dir = '/'.join(path.split('/')[:-1])
    name = path.split('/')[-1]
    ext = name.split('.')[-1]
    take_time_str = time.strftime('%Y%m%d%H%M', take_time)
    new_path = f'{dir}/{take_time_str}.{random.randint(100, 999)}.{ext}'
    while os.path.isfile(new_path):
        new_path = f'{dir}/{take_time_str}.{random.randint(100, 999)}.{ext}'
        print_verbose(f'\t文件已存在，重新生成文件名：{new_path}')

    print_success(f'{" ┗━ " if args.verbose else "✅ "}{path} => {new_path}')

    # 执行重命名
    if args.list is False:
        os.rename(path, new_path)


def main():
    print_info(f'# 用文件日期将文件重命名')
    print_info()
    rename_tips()
    rename_with_date(args.path)
    print_success()
    print_success(f'## 完成')
    print_success()


if __name__ == '__main__':
    main()

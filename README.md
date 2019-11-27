# ImageToMask

├── mask-png
│   ├── mask.py
│   ├── shpimage
│   │   ├── gh.png
│   │   └── shp_test.png
│   ├── shpmask
│   │   └── shp_mask.png
│   ├── shpmasked
│   │   └── shp_test.png
│   └── tiff+shp
│       ├── guigang_iamge.tif
│       └── shp
│           ├── 111.dbf
│           ├── 111.ebb
│           ├── 111.ed1
│           ├── 111.eq1
│           ├── 111.prj
│           ├── 111.shp
│           ├── 111.shp.qtr
│           └── 111.shx

程序中有4个文件夹分别:shpimage 存放待处理的原图路径
                     :shpmask 存放生成的mask图像
                     :shpmasked 存放的生成结果图

                     :tiff+shp 存放的tiff图像以及shp数据


运行：python mask.py


--------------------------------

功能：可以处理shp转换边缘点，在图像上绘制
      针对不同图像，扣取图像，其余部分生成mask==255像素值





#coding:utf-8
import os
import scipy
from scipy import misc
import PIL
import cv2
import numpy as np
import gdal
import shapefile
from PIL import Image, ImageDraw
import PIL.ImageOps
from sympy.physics.quantum.circuitplot import matplotlib

class TiffToMask(object):


    def topix(in_tif,coor_data ):
        """
        由shp文件中列表信息中的经纬度转化为图像的行列号信息
        :param in_tif: 原图路径（主要是从原图中获取六元素坐标信息）
        :param coor_data: shp中的经纬度数据
        :return:          对应的行列号信息
        """
        img = gdal.Open(in_tif)
        geo_trans = img.GetGeoTransform()
        #经纬度转为行列号
        a = np.array([[geo_trans[1], geo_trans[2]], [geo_trans[4], geo_trans[5]]])
        b = np.array([coor_data[0] - geo_trans[0], coor_data[1] - geo_trans[3]])
        result = np.linalg.solve(a, b)  # 使用numpy的linalg.solve进行二元一次方程的求解
        return list(result)

    '''
    将shp数据转换
    '''
    def pix(tif_path,shp_data):
        pix_data= []
        for i in range(len(shp_data)):
             geo = shp_data[i]
             row = []
             for j in range(len(geo)):
                 pix = TiffToMask.topix(tif_path,geo[j])
                 row.append(tuple(pix))
             pix_data.append(row)
        return  pix_data

    def read_shp(shp_path):
        """ 读取shp文件的类型和点坐标信息
        Args:
            shp_path: shp文件的绝对路径
        Return:
            type: shp文件的类型
            coordinates: 图像的点坐标串,是一个二维数组形式。
        """
        try:
            file = shapefile.Reader(shp_path)
            print(file)
            print(shp_path)
            # 读取图像的类型
            type = file.shapeTypeName.capitalize()
            print(type)
            # 读取shp图像的所有点坐标
            shapes = file.shapes()
            result = dict()
            result["geometry"] = []

            for geometry in shapes:
                temp = dict()
                temp["type"] = type
                temp["coordinates"] = list()
                temp["coordinates"].append([list(point) for point in geometry.points])
                result["geometry"].append(temp)

            return result
        except Exception as e:
            print(e)
            return False, None

    def rd(data):
        """
        准备shp文件中列表数据
        :param data:  输入从shp中解析出的数据
        :return:   返回包含的列表信息
        """
        ge_data =[]
        geo_data =data['geometry']
        for i in range(len(geo_data)):
            geo = geo_data[i]['coordinates']
            ge_data.append(geo[0])
        return  ge_data

    '''
    将tiff转换成mask图像
    '''
    def tiff_to_mask(tif_path,shp_data):
        '''
        :param tif_path: 图像原图路径
        :param shp_data: shp数据路径
        :function read_shp: 将读取shp数据
        :function rd ：将shp中数据字段解析
        :return:
        '''

        tif = gdal.Open(tif_path)

        nXSize = tif.RasterXSize #列数
        nYSize = tif.RasterYSize #行数

        im_width = tif.RasterXSize
        im_heigth = tif.RasterYSize

        im_data = tif.ReadAsArray(0, 0, im_width, im_heigth)
        im_redData = im_data[0, :, :]
        im_greedData = im_data[1, :, :]
        im_blueData = im_data[2, :, :]
        tif = np.dstack((im_redData, im_greedData, im_blueData))
        shp_image = os.path.join('./shpimage/','shp_test.png')
        scipy.misc.imsave(shp_image, tif)

        newImg = Image.new("RGB", (nXSize, nYSize), (255, 255, 255))
        draw = ImageDraw.Draw(newImg)

        shp_data =TiffToMask.read_shp(shp_data)
        shp_data= TiffToMask.rd(shp_data)

        pix_data = TiffToMask.pix(tif_path, shp_data)
        for row in pix_data:
            draw.polygon(row ,outline='red',fill = (0, 0, 0))

        newImg = newImg.convert('L')
        newImg = np.array(newImg)
        shp_mask = os.path.join('./shpmask/', 'shp_mask.png')
        cv2.imwrite(shp_mask,newImg)

        image_fan = Image.open(shp_mask)
        inverted_image = PIL.ImageOps.invert(image_fan)
        # 保存图片
        inverted_image.save(shp_mask)
        TiffToMask.add_mask2image_binary(shp_image,shp_mask)


    def add_mask2image_binary(shp_image_path,shp_mask_path):
    # Add binary masks to images

        mask = cv2.imread(shp_mask_path, cv2.IMREAD_GRAYSCALE)  # 将彩色mask以二值图像形式读取
        image = cv2.imread(shp_image_path)

        masked = cv2.add(image, np.zeros(np.shape(image), dtype=np.uint8), mask=mask)  #将image的相素值和mask像素值相加得到结果
        maksed_path = os.path.join('./shpmasked/','shp_test.png')
        cv2.imwrite(maksed_path,masked)
        print('-----------')



if __name__=="__main__":
    '''
    input_image;输入tiff图像
    input_shp:输入shp文件
    '''
    input_image = os.path.join('./tiff+shp/','guigang_iamge.tif')
    input_shp = os.path.join('./tiff+shp/shp/', '111.shp')

    TiffToMask.tiff_to_mask(input_image,input_shp)

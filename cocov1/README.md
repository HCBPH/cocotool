## COCOTOOL

### 1.结构

- cocotool
  - coco.py                 核心类
  - txt2coco.py
  - swedish2txt.py
  - data                      源数据目录
  - coco                      导出目录



### 2.流程

1. 针对不同数据集，先提取出coco需要的数据，存放到txt文件中，格式如下：

   ```
   file_name.jpg,height,width,category,bx,by,bh,bw
   ```

   ​		bx,by,bh,bw是bbox的左上角点和框的长宽

   还需要一个category的映射：

   ```
   PROHIBITORY:1
   MANDATORY:0
   WARNING:2
   
   key值根据具体数据集中标签而定
   ```

2. 调用txt2coco.py脚本

   ```
   必要的参数：
   	--txt_path：上一步生成的txt文件
   	--coco_path：coco的根目录
   	--cat：swedish数据集中分的类别的映射
   
   可选参数：
   	--appending：是否追加到之前的coco annotation中，默认不开启
   	--old_ann_path：如果开启了追加，就一定要指定之前的annotaion.json文件
   	--copy：是否将当前数据集的图片复制到coco文件夹下，默认不开启
   	--img_path：如果开启了，一定要指定源数据集的图片路径
   ```

   



### 3.用例

以swedish数据集为例，

![image-20220325171636133](C:\Users\53059\AppData\Roaming\Typora\typora-user-images\image-20220325171636133.png)

swedish数据集中包含set1-part0中的图片和annotations.txt标签文件，annotation文件格式如下图：

![image-20220325180439072](C:\Users\53059\AppData\Roaming\Typora\typora-user-images\image-20220325180439072.png)



- 文件名、bbox和类别是生成coco数据集需要的，运行swedish2txt.py，提取数据。

```shell
PS E:\Project\cv\cocotool> python .\swedish2txt.py
```

![image-20220325180616231](C:\Users\53059\AppData\Roaming\Typora\typora-user-images\image-20220325180616231.png)

新生成的txt文件需要包含：文件名、图片高宽、图片类型、bbox。



- 再运行txt2coco.py, 就能将提取后的数据转为coco格式的数据

  ![image-20220325180024250](C:\Users\53059\AppData\Roaming\Typora\typora-user-images\image-20220325180024250.png)

```shell
python .\txt2coco.py --txt_path ./data/swedish/new.txt --coco_path ./coco --cat ./data/swedish/category.txt	
```






## COCOTOOL

### 1.结构

- cocotool
  - coco.py                 核心类
  - swedish2txt.py    从swedish标签提取出必要元素到txt文件，需要根据不同类型数据集修改
  - txt2coco.py          txt文件中数据的格式统一，脚本可以自动转为coco
  - data                      源数据目录
  - coco                      导出目录
    - annotations
      - instances_train2017.json
      - instances_val2017.json
      - instances_test2017.json
    - images
      - train2017
      - val2017
      - test2017



### 2.流程

1. 针对不同数据集，先提取出coco需要的数据，存放到txt文件中，格式如下：

   ```
   file_name.jpg,height,width,category,bx,by,bh,bw,category,bx,by,bh,bw,category,bx,by,bh,bw.............
   file_name.jpg,height,width,category,............
   file_name.jpg,height,width,category,............
   一行一张图片，多个标签
   bx,by,bh,bw是bbox的左上角点和框的长宽
   ```

   还需要一个category的映射：

   ```
   PROHIBITORY:1
   MANDATORY:0
   WARNING:2
   ```

   注意：上面的key（例如PROHIBITORY）是根据标签在具体数据集中的名称，关键是value（例如1）要和之前或者之后插入的数据集标签的映射一致。

2. 调用txt2coco.py脚本

   ```
   必要的参数：
   	--txt_path：上一步生成的txt文件
   	--coco_path：coco的根目录
   	--img_path：源图片目录
   	--cat：数据集中分的类别的映射
   
   可选参数：
   	--appending：是否追加到之前的coco annotation中，默认不开启
   	--old_ann_path：如果开启了追加，就一定要指定之前的annotaion.json文件
   	--logging：源图复制到coco目录，会进行重命名和shuffle，开启日志记录其映射历史
   ```

   



### 3.用例

以swedish数据集为例：

![](https://raw.githubusercontent.com/HCBPH/picgo/main/img/image-20220325171636133.png)

swedish数据集中包含set1-part0中的图片和annotations.txt标签文件，annotation文件格式如下图：

![](https://raw.githubusercontent.com/HCBPH/picgo/main/img/image-20220325180439072.png)



- 图片文件名、bbox和类别是生成coco数据集需要的，运行swedish2txt.py，提取数据。

```shell
PS E:\Project\cv\cocotool> python .\swedish2txt.py
```

​	得到new.txt文件

![](https://raw.githubusercontent.com/HCBPH/picgo/main/img/20220327212711.png)

​	new.txt文件内容如下：

![](https://raw.githubusercontent.com/HCBPH/picgo/main/img/image-20220325180616231.png)

​	新生成的txt文件需要包含：文件名、图片高宽、图片类型、bbox。



- 再运行txt2coco.py, 就能将提取后的数据new.txt转为coco格式的数据，要指定txt的路径，指定coco路径，指定源图片的路径，还有类别映射的文件路径。
  - 注意：对于首次导入到coco文件，会读取--cat指定文件中的类别映射，对于追加导入的数据，将读取之前annotation中的类别映射。



```shell
python .\txt2coco.py --txt_path ./data/swedish/new.txt --coco_path ./coco --img_path E:\Data\dataset\swedish\set1-part0 --cat ./data/swedish/category.txt --logging --split 0.6,0.1,0.3
```

​	产生的coco数据如下：

![](https://raw.githubusercontent.com/HCBPH/picgo/main/img/20220327213040.png)

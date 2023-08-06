# heatmapanimation

Python package for generating heatmap animation with given data and geojson.

<p align='center'>
<b>English</b> | <a href="https://github.com/zhushaohz/heatmapanimation/blob/master/README.zh-CN.md">简体中文</a>
</p>

## Introduction

If you want to generate a heatmap animation with given data and geojson file or url,
you can use this package.
You can also type the region name or code replacing the geojson file. 

Use [高德地图地理/逆地理编码](https://lbs.amap.com/api/webservice/guide/api/georegeo)
get the region code.

Use [阿里云数据可视化平台](http://datav.aliyun.com/portal/school/atlas/area_selector?spm=a2crr.b71357980.atlas.10.780426c0KhXFQp)
get the geojson file.

    Note: Currently, the region name must be in Chinese.
## Install

    pip install heatmapanimation
## Usage

    import heatmapanimation as hma
    
    heatmap = hma.Heatmap() # create a heatmap object

    # set the configuration
    heatmap.region = '北京'
    heatmap.datafile = './data/data.csv'
    heatmap.run_x() # run the animation

## API Reference

### *class* heatmapanimation.Heatmap()

    You must set a region and datafile before run the animation.

+ **region**

    The region name you want to generate the heatmap animation.
Must be type Chinese region in Chinese.

+ **region_code**

    The region code you want to generate the heatmap animation. 
Must be type Chinese region code.

+ **region_url**

  The url of the geojson file.Or the geojson file path.

+ **datafile**

  The data file path.

+ **data**

  The data you want to generate the heatmap animation.

  Options: dict or list or json or pandas.DataFrame.

+ **output_format**

  The output format of the animation.

  Options: 'gif' or 'mp4'.

+ **fig_name**

  The name of the output file.

  Note: If you don't set the fig_name, the output file will be named as the region name.

+ **color_map**

  The colormap of the heatmap.

  Options: 'Blues', 'BuGn', 'BuPu', 'GnBu', 'Greens', 'Greys', 'Oranges', 'OrRd', 'PuBu'.
  
  All the colormaps are in [matplotlib](https://matplotlib.org/stable/tutorials/colors/colormaps.html).

  Default: 'Reds'

+ **isLegend**

  Whether to show the legend.

  Options: True or False.

  Default: False.

+ **legend_label**

  The label of the legend.

  Options: str.

  Default: 'Temperature'.

+ **legend_location**

  The location of the legend.

  Options: 'right' or 'right'.

  Default: 'right'.

+ **legend_min**

  The min value of the legend.

  Options: int or float.

  Default: the minimum of the data.

+ **legend_max**

  The max value of the legend.

  Options: int or float.

  Default: the maximum of the data.

+ **run_x()**

  Run the animation and generate frame image and synthetic GIF. Currently,
  the output format is only 'gif'.

+ **run()**

  Run the animation with another method which can not show the legend. But the output format
  is gif, mp4, jshtml and html5.
## License

[MIT](https://github.com/zhushaohz/heatmapanimation/blob/master/LICENSE)

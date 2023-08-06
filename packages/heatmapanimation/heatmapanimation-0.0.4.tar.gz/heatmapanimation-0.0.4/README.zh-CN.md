# heatmapanimation

用于使用给定数据和 geojson 生成热力地图动画的 Python 包。

<p align='center'>
<b>English</b> | <a href="https://github.com/zhushaohz/heatmapanimation/master/blob/README.zh-CN.md">简体中文</a>
</p>

## 介绍

如果你想用给定的数据和geojson文件或url生成热力地图动画，你可以使用这个包。
您还可以使用区域名称或代码来替代 geojson 文件。

    注意: 目前，区域名称必须选择中国的省或市。
## 安装

    pip install heatmapanimation
## 用法

    import heatmapanimation as hma
    
    heatmap = hma.Heatmap() # create a heatmap object

    # set the configuration
    heatmap.region = '北京'
    heatmap.datafile = './data/data.csv'
    heatmap.run_x() # run the animation

## License

[MIT](https://github.com/zhushaohz/heatmapanimation/blob/master/LICENSE)

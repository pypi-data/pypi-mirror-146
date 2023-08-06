import heatmapanimation as hma

heatmap = hma.Heatmap()
# heatmap-animation.url = 'https://geo.datav.aliyun.com/areas_v3/bound/geojson?code=110000_full'
heatmap.region = '北京'
# heatmap-animation.region_code = '120000'
heatmap.datafile = './data/data.csv'
# heatmap-animation.data = {
#     'name': ['东城区', '西城区', '朝阳区', '丰台区', '石景山区', '海淀区', '门头沟区', '房山区', '通州区', '顺义区', '昌平区', '大兴区', '怀柔区', '平谷区', '密云县', '延庆县'],
#     'data': [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
#     'data1': [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
# }
# heatmap-animation.data = [
#     ['东城区', 3, 20],
#     ['西城区', 4, 21],
#     ['朝阳区', 5, 12],
#     ['丰台区', 6, 13],
#     ['石景山区', 7, 14],
#     ['海淀区', 8, 15],
#     ['门头沟区', 9, 16],
#     ['房山区', 10, 17],
#     ['通州区', 11, 18],
#     ['顺义区', 12, 19],
#     ['昌平区', 13, 20],
#     ['大兴区', 14, 21],
#     ['怀柔区', 15, 22],
#     ['平谷区', 16, 23],
#     ['密云县', 17, 24],
#     ['延庆县', 18, 25]
# ]
heatmap.output_format = 'gif'
heatmap.fig_name = '我是图片名称'
heatmap.isLegend = True
heatmap.legend_label = '温度'
heatmap.legend_min = 0
heatmap.legend_max = 50
heatmap.run_x()

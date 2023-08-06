# coding: utf-8
import sys
import os
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import requests
import urllib.error
import json
import datetime as dt
import imageio
from mpl_toolkits.axes_grid1 import make_axes_locatable


class Heatmap:
    def __init__(self):
        """
        初始化变量
        --------------------------------------------------
        __region: 地区名称，中文
        __region_code: 地区编码
        __url: 地区网址
        fig: 图像
        ax: 坐标轴
        __data: 数据
        """
        self.__legend_location = "right"
        self.__legend_label = 'Temperature'
        self.__chosen_map = None
        self.__region = None
        self.__region_code = None
        self.__url = 'https://geo.datav.aliyun.com/areas_v3/bound/geojson?code=110000_full'
        self.fig = plt.figure(figsize=(10, 10))
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.fig.subplots_adjust(wspace=0.1)
        self.__data = None
        self.__datafile = None
        self.__frame_output_path = None
        self.__output_format = 'gif'
        # 图的细节配置
        self.__fig_name = None
        self.__fig_color = None
        self.__colormap = 'Reds'
        self.isLegend = False
        self.__run_method = None
        self.__legend_min = None
        self.__legend_max = None
        plt.rcParams['font.sans-serif'] = ['Heiti TC']
        plt.rcParams['axes.unicode_minus'] = False

    def run(self):
        """
        启动程序
        --------------------------------------------------
        """
        self.__run_method = 'run'
        if self.__region is not None:
            self.__region, self.__region_code = self.geturl(self.__region)
            print('当前选择：' + self.__region)
        if self.__region_code is not None:
            self.__url = 'https://geo.datav.aliyun.com/areas_v3/bound/geojson?code=' + self.__region_code + '_full'
            print('当前选择：' + self.__url)

        # 读取数据
        try:
            self.__chosen_map = gpd.read_file(self.__url)
        except urllib.error.HTTPError:
            print('URL Entered Error. 网址输入错误或数据格式不正确,请输入geojson格式的网址')
            sys.exit(0)
        if self.__datafile is not None:
            # 这里加载文件格式可以分为三种，一种是csv，一种是json，一种是excel
            if self.__datafile.endswith('.csv'):
                self.__data = pd.read_csv(self.__datafile)
            elif self.__datafile.endswith('.json'):
                self.__data = pd.read_json(self.__datafile)
            elif self.__datafile.endswith('.xlsx'):
                self.__data = pd.read_excel(self.__datafile)
            else:
                print('文件格式不正确，请输入正确的文件格式，支持csv,json,xlsx')
                sys.exit(0)
            # self.__data = pd.read_csv(self.__datafile)
        elif self.__data is None:
            if not os.path.exists('data/data.csv'):
                # print('data/data.csv not exists')
                if not os.path.exists('data'):
                    os.mkdir('data')

                dataframe = pd.DataFrame({'name': self.__chosen_map['name'], 'data': [0] * len(self.__chosen_map)})
                dataframe.to_csv('data/data.csv', index=False)
                # print('data.csv created')
                print('请在data/data.csv中填入数据')
            self.__datafile = 'data/data.csv'
            self.__data = pd.read_csv(self.__datafile)

        len_data = len(self.__data.columns) - 1
        now = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        self.__frame_output_path = 'frame_output_' + now
        os.mkdir(self.__frame_output_path)

        if len_data <= 0:
            print('数据错误或没有数据')
        elif len_data == 1:
            # print('只有一个时间点，无法生成动画，将生成单帧图像')
            self.draw(0)
            plt.savefig('heatmap-animation.png')
        else:
            try:
                animator = animation.FuncAnimation(self.fig, func=self.draw, frames=range(0, len_data), interval=500)
                if self.__output_format == 'gif':
                    animator.save('heatmap-animation.gif', dpi=300)
                elif self.__output_format == 'mp4':
                    animator.save('heatmap-animation.mp4', writer='ffmpeg')
                elif self.__output_format == 'html':
                    with open('output.html', 'w') as f:
                        f.write(animator.to_jshtml())
                elif self.__output_format == 'html5':
                    with open('output.html', 'w') as f:
                        f.write(animator.to_html5_video())
                else:
                    print('暂不支持该格式')
                    animator.save('heatmap-animation.gif')
            except SystemExit:
                print('生成动画错误，请检查数据是否正确')
                sys.exit()
        print('Done')

    def run_x(self):
        # without using animation module
        self.__run_method = 'run_x'
        if self.__region is not None:
            self.__region, self.__region_code = self.geturl(self.__region)
            print('当前选择：' + self.__region)
        if self.__region_code is not None:
            self.__url = 'https://geo.datav.aliyun.com/areas_v3/bound/geojson?code=' + self.__region_code + '_full'
            print('当前选择：' + self.__url)

        # 读取数据
        try:
            self.__chosen_map = gpd.read_file(self.__url)
        except urllib.error.HTTPError:
            print('URL Entered Error. 网址输入错误或数据格式不正确,请输入geojson格式的网址')
            sys.exit(0)
        if self.__datafile is not None:
            # 这里加载文件格式可以分为三种，一种是csv，一种是json，一种是excel
            if self.__datafile.endswith('.csv'):
                self.__data = pd.read_csv(self.__datafile)
            elif self.__datafile.endswith('.json'):
                self.__data = pd.read_json(self.__datafile)
            elif self.__datafile.endswith('.xlsx'):
                self.__data = pd.read_excel(self.__datafile)
            else:
                print('文件格式不正确，请输入正确的文件格式，支持csv,json,xlsx')
                sys.exit(0)
            # self.__data = pd.read_csv(self.__datafile)
        elif self.__data is None:
            if not os.path.exists('data/data.csv'):
                # print('data/data.csv not exists')
                if not os.path.exists('data'):
                    os.mkdir('data')

                dataframe = pd.DataFrame({'name': self.__chosen_map['name'], 'data': [0] * len(self.__chosen_map)})
                dataframe.to_csv('data/data.csv', index=False)
                # print('data.csv created')
                print('请在data/data.csv中填入数据')
            self.__datafile = 'data/data.csv'
            self.__data = pd.read_csv(self.__datafile)

        len_data = len(self.__data.columns) - 1
        now = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        self.__frame_output_path = 'frame_output_' + now
        os.mkdir(self.__frame_output_path)

        if len_data <= 0:
            print('数据错误或没有数据')
        elif len_data == 1:
            # print('只有一个时间点，无法生成动画，将生成单帧图像')
            self.draw(0)
            plt.savefig('heatmap-animation.png')
        else:
            try:
                for i in range(0, len_data):
                    self.draw(i)
            except SystemExit:
                print('生成动画错误，请检查数据是否正确')
                sys.exit()
            # 图片合成动画
            if self.__output_format == 'gif':
                self.compose_gif()
            elif self.__output_format == 'mp4':
                # 合成mp4
                print('合成mp4待开发')
                # self.compose_mp4()
            else:
                print('暂不支持该格式')
        print('Done')

    def draw(self, time):
        """
        绘制热力图
        """
        chosen_map = self.__chosen_map
        data = self.__data
        temp_time = data.columns.tolist()
        reg = pd.merge(chosen_map, data[['name', temp_time[time + 1]]], on='name')
        if self.isLegend:
            if time == 0:
                if self.__run_method == 'run':
                    fig = reg.plot(ax=self.ax, column=temp_time[time + 1], cmap=self.__colormap,
                                   vmin=self.__legend_min, vmax=self.__legend_max)
                else:
                    divider = make_axes_locatable(plt.gca())
                    cax = divider.append_axes(self.__legend_location, size="3%", pad="1%")
                    fig = reg.plot(ax=self.ax, column=temp_time[time + 1], cmap=self.__colormap,
                                   vmin=self.__legend_min, vmax=self.__legend_max, legend=True, cax=cax,
                                   legend_kwds={'label': self.__legend_label})
            else:
                fig = reg.plot(ax=self.ax, column=temp_time[time + 1], cmap=self.__colormap,
                               vmin=self.__legend_min, vmax=self.__legend_max)
        else:
            fig = reg.plot(ax=self.ax, column=temp_time[time + 1], cmap=self.__colormap,
                           vmin=self.__legend_min, vmax=self.__legend_max)
        if self.__run_method == 'run_x':
            plt.sca(self.ax)
        if self.__fig_name is not None:
            plt.title(self.__fig_name + str(time))
        else:
            plt.title('热力图')
        # plt.title('Time: ' + str(time))
        plt.savefig(self.__frame_output_path + '/frame' + str(time) + '.png', dpi=300)
        return fig

    def geturl(self, region):
        """
        获取地区编码
        --------------------------------------------------
        :param region:
        :return: region_code
        """
        session = requests.Session()
        url = 'https://restapi.amap.com/v3/config/district'
        params = {
            'key': '6175db72a9451d0cc6b0e7568b6b8824',
            'subdistrict': '0',
            'extensions': 'base',
            'keywords': region
        }
        response = session.get(url, params=params)
        region_name = response.json()['districts'][0]['name']
        region_code = response.json()['districts'][0]['adcode']
        return region_name, region_code

    def compose_gif(self):
        """
        将生成的图片合成为gif
        """
        images = []
        for i in range(0, len(self.__data.columns) - 1):
            images.append(imageio.imread(self.__frame_output_path + '/frame' + str(i) + '.png'))
        imageio.mimsave('heatmapx.gif', images, fps=2)
        print('Gif Saved')
    # --------------------------------------------------------------------------
    # Setter & getter
    # --------------------------------------------------------------------------
    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, url):
        self.__url = url

    @property
    def region(self):
        return self.__region

    @region.setter
    def region(self, value):
        self.__region = value

    @property
    def region_code(self):
        return self.__region

    @region_code.setter
    def region_code(self, value):
        self.__region_code = value

    @property
    def datafile(self):
        return self.__region

    @datafile.setter
    def datafile(self, value):
        self.__datafile = value

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, value):
        # print(type(value))
        if type(value) is dict:
            df = pd.DataFrame(value)
            self.__data = df
            # print(self.__data)
        elif check_json(value):
            df = pd.DataFrame(value)
            self.__data = df
            # print(self.__data)
        elif type(value) is list:
            df = pd.DataFrame(value, columns=['name', 'data', 'time'])
            self.__data = df
            # print(self.__data)

    @property
    def output_format(self):
        return self.__output_format

    @output_format.setter
    def output_format(self, value):
        self.__output_format = value

    @property
    def fig_name(self):
        return self.__fig_name

    @fig_name.setter
    def fig_name(self, value):
        self.__fig_name = value

    @property
    def color_map(self):
        return self.__colormap

    @color_map.setter
    def color_map(self, value):
        # 可选颜色列表，详见：https://matplotlib.org/stable/tutorials/colors/colormaps.html
        color_list = [
            # 感知均匀的顺序颜色映射
            'viridis', 'plasma', 'inferno', 'magma', 'cividis',
            # 顺序颜色映射
            'Blues', 'BuGn', 'BuPu', 'GnBu', 'Greens', 'Greys', 'Oranges', 'OrRd', 'PuBu',
            'PuBuGn', 'PuRd', 'Purples', 'RdPu', 'Reds', 'YlGn', 'YlGnBu', 'YlOrBr', 'YlOrRd',
            'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink', 'spring', 'summer', 'autumn',
            'cool', 'Wistia', 'hot', 'afmhot', 'gist_heat', 'copper',
            # 发散颜色映射
            'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu', 'RdYlBu', 'RdYlGn', 'Spectral',
            'coolwarm', 'bwr', 'seismic',
            # 循环颜色映射
            'twilight', 'twilight_shifted', 'hsv',
            # 定性颜色映射
            'Pastel1', 'Pastel2', 'Paired', 'Accent', 'Dark2', 'Set1', 'Set2', 'Set3',
            'tab10', 'tab20', 'tab20b', 'tab20c',
            # 杂项颜色映射
            'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern', 'gnuplot',
            'gnuplot2', 'CMRmap', 'cubehelix', 'brg', 'gist_rainbow', 'rainbow', 'jet',
            'turbo', 'nipy_spectral', 'gist_ncar',
        ]
        if value in color_list:
            self.__colormap = value
        else:
            print('请输入正确的颜色名称')

    @property
    def legend_label(self):
        return self.__legend_label

    @legend_label.setter
    def legend_label(self, value):
        self.__legend_label = value

    @property
    def legend_location(self):
        return self.__legend_location

    @legend_location.setter
    def legend_location(self, value):
        # 可选位置列表： left, right
        self.__legend_location = value

    @property
    def legend_min(self):
        return self.__legend_min

    @legend_min.setter
    def legend_min(self, value):
        self.__legend_min = float(value)

    @property
    def legend_max(self):
        return self.__legend_max

    @legend_max.setter
    def legend_max(self, value):
        self.__legend_max = float(value)


def check_json(json_file):
    try:
        json.loads(json_file)
        return True
    except:
        return False

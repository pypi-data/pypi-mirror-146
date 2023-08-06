#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2021
# @Author :  GitOPEN
# @Email  :  gitopen@gmail.com
# @Date   :  2021-05-22 17:08:35
# @Description :  一些画图的相关工具函数


__version__ = "0.4.3"


from matplotlib import ticker
from matplotlib.axes import Axes
from matplotlib.offsetbox import AnchoredText
import matplotlib.pyplot as plt


def set_legend_outside(ax: Axes, loc: int = 3, ncol: int = 1, alpha: float = 1.0):
    """把图例放到图片的右下角；也可以调整一些参数，例如透明度，列数。"""
    ax.legend_.remove()
    legend = ax.legend(bbox_to_anchor=(1.05, 0), loc=loc, ncol=ncol, borderaxespad=0)
    legend.get_frame().set_alpha(alpha)


def set_axis_tick(ax: Axes, axis: str = "y", format="%.2f"):
    """
    横轴或者纵轴的刻度标签的格式，例如，%.2f 表示两位小数；
    %.2e 科学计数法
    """
    if axis == "x":
        ax.xaxis.set_major_formatter(ticker.FormatStrFormatter(format))
    if axis == "y":
        ax.yaxis.set_major_formatter(ticker.FormatStrFormatter(format))


def legend_text(
    ax: Axes, text: str, loc=2, fontsize: int = 10, fontcolor: str = "black"
):
    """
    在ax上添加一个仅包含文本的legend

    Args:
        ax (Axes): 子图的轴
        text (str): 要显示的文字内容
        loc (int): legend的位置，1表示右上角，2表示左上角，3表示左下角，4表示右下角
        fontsize (int): 字体大小
        fontcolor (str): 字体颜色

    Returns:
        AnchoredText: 返回AnchoredText实例
    """
    at = AnchoredText(
        text, prop=dict(size=fontsize, color=fontcolor), frameon=True, loc=loc
    )
    at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
    ax.add_artist(at)
    return at


def set_font(fname: str = "SimHei", fsize: int = 12):
    """
    设置字体

    Args:
        fname (str): 字体的名称。
        fsize (int): 字体的大小。

    Returns:
        None
    """
    # 用来正常显示中文标签
    plt.rcParams["font.sans-serif"].insert(0, fname)
    # 用来设置字体大小
    plt.rcParams["font.size"] = fsize
    # 用来正常显示负号
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["mathtext.fontset"] = "cm"

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""

import xml.etree.ElementTree as ET
import re
from typing import Tuple, List, Union
import colorsys


class ColorParser:
    # 颜色名称到RGB值的映射
    COLOR_NAMES = {
        'red': '#FF0000',
        'green': '#00FF00',
        'blue': '#0000FF',
        # 可以添加更多颜色名称映射
    }

    @staticmethod
    def normalize_color(color: str) -> str:
        """
        将各种格式的颜色值标准化为6位十六进制格式
        支持以下格式：
        - 颜色名称: red, blue 等
        - 十六进制: #RGB, #RRGGBB
        - RGB: rgb(255, 0, 0)
        - RGBA: rgba(255, 0, 0, 1)
        - HSL: hsl(0, 100%, 50%)
        """
        color = color.strip().lower()

        # 处理颜色名称
        if color in ColorParser.COLOR_NAMES:
            return ColorParser.COLOR_NAMES[color]

        # 处理十六进制格式
        if color.startswith('#'):
            if len(color) == 4:  # #RGB 格式
                r, g, b = color[1], color[2], color[3]
                return f'#{r}{r}{g}{g}{b}{b}'.upper()
            return color.upper()

        # 处理rgb/rgba格式
        rgb_match = re.match(r'rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*[\d.]+)?\)', color)
        if rgb_match:
            r, g, b = map(int, rgb_match.groups())
            return f'#{r:02x}{g:02x}{b:02x}'.upper()

        # 处理hsl格式
        hsl_match = re.match(r'hsl\((\d+),\s*(\d+)%,\s*(\d+)%\)', color)
        if hsl_match:
            h, s, l = map(float, hsl_match.groups())
            h /= 360
            s /= 100
            l /= 100
            r, g, b = colorsys.hls_to_rgb(h, l, s)
            return f'#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}'.upper()

        return color.upper()

    @staticmethod
    def colors_are_similar(color1: str, color2: str, threshold: float = 0.1) -> bool:
        """
        比较两个颜色是否相似
        :param threshold: 相似度阈值 (0-1)
        """

        def hex_to_rgb(hex_color: str) -> Tuple[float, float, float]:
            hex_color = hex_color.lstrip('#')
            r = int(hex_color[0:2], 16) / 255.0
            g = int(hex_color[2:4], 16) / 255.0
            b = int(hex_color[4:6], 16) / 255.0
            return (r, g, b)

        if color1.startswith('#') and color2.startswith('#'):
            rgb1 = hex_to_rgb(color1)
            rgb2 = hex_to_rgb(color2)

            diff = sum(abs(a - b) for a, b in zip(rgb1, rgb2)) / 3
            return diff <= threshold

        return ColorParser.normalize_color(color1) == ColorParser.normalize_color(color2)


class SVGParser:
    def __init__(self, svg_file: str):
        ET.register_namespace("", "http://www.w3.org/2000/svg")
        self.svg_file = svg_file
        self.tree = ET.parse(svg_file)
        self.root = self.tree.getroot()
        self.ns = {"svg": "http://www.w3.org/2000/svg"}
        self.color_parser = ColorParser()

    def get_color_attributes(self, elem: ET.Element) -> List[Tuple[str, str]]:
        """获取元素的所有颜色属性"""
        color_attrs = []

        # 直接属性
        for attr in ['fill', 'stroke']:
            value = elem.get(attr)
            if value and value != 'none':
                color_attrs.append((attr, value))

        # style 属性中的颜色
        style = elem.get('style')
        if style:
            for prop in style.split(';'):
                if ':' in prop:
                    name, value = prop.split(':')
                    name = name.strip()
                    if name in ['fill', 'stroke'] and value.strip() != 'none':
                        color_attrs.append((f'style-{name}', value.strip()))

        return color_attrs

    def smart_change_color(self, new_color: str) -> int:
        """
        智能替换SVG中的主要颜色
        :param new_color: 新的颜色值
        :return: 修改的元素数量
        """
        # 收集所有颜色及其使用次数
        color_usage = {}
        for elem in self.root.iter():
            for attr, value in self.get_color_attributes(elem):
                norm_color = self.color_parser.normalize_color(value)
                color_usage[norm_color] = color_usage.get(norm_color, 0) + 1

        # 找出使用最多的颜色
        if not color_usage:
            return 0

        most_used_color = max(color_usage.items(), key=lambda x: x[1])[0]
        return self.change_color(most_used_color, new_color)

    def change_color(self, old_color: str, new_color: str) -> int:
        """
        替换特定颜色
        :param old_color: 原始颜色
        :param new_color: 新颜色
        :return: 修改的元素数量
        """
        count = 0
        normalized_old = self.color_parser.normalize_color(old_color)
        normalized_new = self.color_parser.normalize_color(new_color)

        for elem in self.root.iter():
            # 处理直接属性
            for attr in ['fill', 'stroke']:
                value = elem.get(attr)
                if value and value != 'none':
                    if self.color_parser.colors_are_similar(value, normalized_old):
                        elem.set(attr, normalized_new)
                        count += 1

            # 处理style属性
            style = elem.get('style')
            if style:
                new_style_parts = []
                modified = False

                for prop in style.split(';'):
                    if ':' in prop:
                        name, value = prop.split(':')
                        name = name.strip()
                        value = value.strip()

                        if name in ['fill', 'stroke'] and value != 'none':
                            if self.color_parser.colors_are_similar(value, normalized_old):
                                value = normalized_new
                                modified = True

                        new_style_parts.append(f"{name}:{value}")

                if modified:
                    elem.set('style', ';'.join(new_style_parts))
                    count += 1

        return count

    def save(self, output_file: str = None):
        """保存修改后的SVG文件"""
        if output_file is None:
            output_file = self.svg_file
        self.tree.write(output_file, encoding='utf-8', xml_declaration=True)

    def tostring(self):
        return ET.tostring(self.root, encoding="unicode")


# 使用示例
def main():
    svg_file = "example.svg"
    parser = SVGParser(svg_file)

    # 智能替换主要颜色
    changed = parser.smart_change_color("#00FF00")
    print(f"自动替换了 {changed} 个颜色")

    # 保存修改后的文件
    parser.save("output.svg")


if __name__ == "__main__":
    main()

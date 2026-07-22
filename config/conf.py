#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os

from utils.times import dt_strftime


class ConfigManager(object):
    # 项目目录
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # 输出目录
    OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

    # 日志目录
    LOG_DIR = os.path.join(OUTPUT_DIR, 'logs')

    # 报告目录
    REPORT_DIR = os.path.join(OUTPUT_DIR, 'allure-results')

    # 页面元素目录
    ELEMENT_PATH = os.path.join(BASE_DIR, 'yaml')

    # 报告文件
    REPORT_FILE = os.path.join(REPORT_DIR, 'reports.html')

    # 邮件信息
    EMAIL_INFO = {
        'username': '',  # 切换成你自己的地址
        'password': '',
        'smtp_host': '测试',
        'smtp_port': 465
    }

    # 收件人
    ADDRESSEE = [
        '2222224647@qq.com',
    ]

    @property
    def log_file(self):
        """日志文件路径"""
        if not os.path.exists(self.LOG_DIR):
            os.makedirs(self.LOG_DIR)
        return os.path.join(self.LOG_DIR, '{}.log'.format(dt_strftime()))

    @property
    def report_dir(self):
        """报告目录"""
        if not os.path.exists(self.REPORT_DIR):
            os.makedirs(self.REPORT_DIR)
        return self.REPORT_DIR

    @property
    def ini_file(self):
        """配置文件"""
        ini_file = os.path.join(self.BASE_DIR, 'config', 'config.ini')
        if not os.path.exists(ini_file):
            raise FileNotFoundError("配置文件%s不存在！" % ini_file)
        return ini_file


cm = ConfigManager()
if __name__ == '__main__':
    print(f"项目目录: {cm.BASE_DIR}")
    print(f"输出目录: {cm.OUTPUT_DIR}")
    print(f"日志目录: {cm.LOG_DIR}")
    print(f"报告目录: {cm.REPORT_DIR}")
    print(f"日志文件: {cm.log_file}")
    print(f"报告文件: {cm.REPORT_FILE}")


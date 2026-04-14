# 运行所有测试用例
pytest testcases/ -v -s

# 运行并生成allure结果
pytest testcases/ --alluredir=./allure-results -v -s

# 生成allure报告
allure generate ./allure-results -o ./allure-report --clean

# 或生成HTML报告
pytest testcases/ --html=report.html --self-contained-html

# 打开allure报告
allure open ./allure-report

# 或直接在浏览器中打开HTML报告
# 使用浏览器打开 report.html 文件

import subprocess
import sys
import webbrowser
import os

# 执行测试并生成报告
subprocess.run([sys.executable, '-m', 'pytest', 'testcases/', '--alluredir=./allure-results', '-v', '-s'])

# 生成allure报告
subprocess.run(['allure', 'generate', './allure-results', '-o', './allure-report', '--clean'])

# 打开报告
report_path = os.path.abspath('./allure-report/index.html')
webbrowser.open(f'file://{report_path}')

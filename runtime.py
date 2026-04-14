import subprocess
import sys
import webbrowser
import os
from datetime import datetime

# 生成带时间戳的目录名
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
allure_results_dir = f'./allure-results/{timestamp}'
allure_report_dir = f'./allure-report/{timestamp}'

# 确保目录存在且有写权限
os.makedirs(allure_results_dir, exist_ok=True)
os.makedirs(allure_report_dir, exist_ok=True)

print(f"测试结果目录: {allure_results_dir}")
print(f"报告目录: {allure_report_dir}")

# 执行测试并生成报告（无论成功失败都要生成报告）
print("开始执行测试...")
test_result = subprocess.run(
    [sys.executable, '-m', 'pytest', 'testcases/', f'--alluredir={allure_results_dir}', '-v', '-s'])

print(f"测试执行完成，返回码: {test_result.returncode}")

# 检查测试结果目录
if os.path.exists(allure_results_dir):
    result_files = os.listdir(allure_results_dir)
    print(f"生成了 {len(result_files)} 个测试结果文件")

    # 即使测试失败也生成报告
    allure_path = r"E:\allure-2.33.0\bin\allure.bat"
    print("正在生成报告...")
    generate_result = subprocess.run([allure_path, 'generate', allure_results_dir, '-o', allure_report_dir, '--clean'])

    if generate_result.returncode == 0:
        print("报告生成完成")
        # 打开报告
        report_path = os.path.abspath(f'{allure_report_dir}/index.html')
        if os.path.exists(report_path):
            webbrowser.open(f'file://{report_path}')
            print(f"已打开报告: {report_path}")
        else:
            print("报告文件未找到")
    else:
        print("报告生成失败")
else:
    print("未找到测试结果目录")

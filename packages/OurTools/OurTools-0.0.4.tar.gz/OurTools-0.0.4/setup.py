from setuptools import setup, find_packages

setup(
    # 以下为必需参数
    name='OurTools',  # 模块名
    version='0.0.4',  # 当前版本
    description='A Tool Project by CHIANDYAO',  # 简短描述
    py_modules=["ourtools"], # import的名字，并且需要和文件名对应
    # ckages=find_packages(exclude=['contrib', 'docs', 'tests']),  # 多文件模块写法
    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires=['pytorch', 'numpy', 'line_profiler'], # 依赖模块
)
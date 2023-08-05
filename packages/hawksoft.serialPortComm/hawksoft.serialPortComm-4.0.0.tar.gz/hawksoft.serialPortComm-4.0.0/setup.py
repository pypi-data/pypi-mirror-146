from setuptools import setup, find_packages

setup(name='hawksoft.serialPortComm',
      version='4.0.0',
      packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # 多文件模块写法
      author="xingyongkang",
      author_email="xingyongkang@cqu.edu.cn",
      description="Provides a thread which send and receive bytes from serial port.",
      long_description=open('./README.md', encoding='utf-8').read(),
      long_description_content_type = "text/markdown",
      #long_description="http://gitee.comg/xingyongkang",
      license="MIT",
      url = "https://gitee.com/xingyongkang/serialportcomm",
      include_package_data=True,
      platforms="any",
      install_requires=['pyserial','pyknow'],
      keywords='serial port comm'
)
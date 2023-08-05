'''
      下面打包选项的说明：
      name : 打包后包的文件名
      version : 版本号
      author : 作者
      author_email : 作者的邮箱
      py_modules : 要打包的.py文件
      packages: 打包的python文件夹
      include_package_data : 项目里会有一些非py文件,比如html和js等,这时候就要靠include_package_data 和 package_data 来指定了。package_data:一般写成{‘your_package_name’: [“files”]}, include_package_data还没完,还需要修改MANIFEST.in文件.MANIFEST.in文件的语法为: include xxx/xxx/xxx/.ini/(所有以.ini结尾的文件,也可以直接指定文件名)
      license : 支持的开源协议
      description : 对项目简短的一个形容
      ext_modules : 是一个包含Extension实例的列表,Extension的定义也有一些参数。
      ext_package : 定义extension的相对路径
      requires : 定义依赖哪些模块
      provides : 定义可以为哪些模块提供依赖
      data_files :指定其他的一些文件(如配置文件),规定了哪些文件被安装到哪些目录中。如果目录名
'''
import os
import sys

PACKAGE_CFG = {
    "name":"zhangsan12345abc",
    "version":"0.1.5",
    "description":"上传自定义包",
    "author":"zhangsan12345",
    "author_email":"zhangsan12345@qq.com",

    #是否：build命令，真使用：Build命令，否则使
    #     用一般的方式
    "blIsBuildWay":True
}

from setuptools import setup,find_packages,Command
from shutil import rmtree

here = os.path.abspath(os.path.dirname(__file__))

class UploadCommand(Command):
    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
            rmtree(os.path.join(here, 'build'))
            rmtree(os.path.join(here, PACKAGE_CFG.get("name") + '.egg-info'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')

        # 目前两种方式均支持，但如果Build方式需要
        #    安装build即pip inistall build
        blIsBuildWay = PACKAGE_CFG.get("blIsBuildWay")

        if blIsBuildWay:
            os.system('{0} -m build'.format(
                sys.executable))
        else:
            os.system('{0} setup.py sdist bdist_wheel --universal'.format(
                sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')

        sys.exit()


setup(name=PACKAGE_CFG.get("name"),
      version=PACKAGE_CFG.get("version"),
      description=PACKAGE_CFG.get("description"),
      author=PACKAGE_CFG.get("author"),
      author_email=PACKAGE_CFG.get("author_email"),

      # 定义依赖哪些模块
      requires= [],
      install_requires=[],
      include_package_data=True,

      # 系统自动从当前目录开始找包
      packages=find_packages(),
      # 如果有的文件不用打包，则只能指定需要打包的文件
      #packages=['代码1','代码2','__init__']  #指定目录中需要打包的py文件，注意不要.py后缀

      license='MIT',
      classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        "Programming Language :: Python :: 3"
      ],

      # 上传后的处理：属扩展增强功能，可选，本示例是发布时删除
      #   前一个版本生成的内容
      cmdclass={
        'upload': UploadCommand
      }
)

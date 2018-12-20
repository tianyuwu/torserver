# torserver-基于tornado的web开发工具包

## Python3环境搭建
### pipenv搭建
安装pipenv
```git
brew install pipenv
```
进入项目目录，运行命令创建py3开发虚拟环境
```git
pipenv --python 3.7
```
进入虚拟环境
```git
pipenv shell
```
查看虚拟环境py解释器位置
```git
pipenv --py
```
查看安装的依赖及其版本
```git
pipenv run pip freeze 
```
### Docker容器搭建
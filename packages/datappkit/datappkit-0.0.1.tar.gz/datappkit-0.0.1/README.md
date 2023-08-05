# datappkit

## 简介

datappkit 是一个对数据操作的SDK，为接入方提供对标注和统计等平台沟通的接口

工程结构：
```
.
├── README.md
├── datappkit #核心代码包
│   ├── __init__.py
│   ├── common #通用基础包
│   │   ├── __init__.py
│   │   └── quota_manager.py #配额管理
│   │   └── ...
│   ├── controller #控制层，接收事件并转发给service
│   │   ├── __init__.py
│   │   └── requirement_controller.py
│   │   └── ...
│   ├── datapp.py #SDK唯一入口，接收事件并转发给响应业务的controller
│   ├── services #核心业务包
│   │   ├── __init__.py
│   │   └── requirement_service.py
│   │   └── ...
│   ├── utils #工具包
│   │   └── __init__.py
│   │   └── ...
│   └── version.py #版本信息
├── docs #包的参考文档
│   └── conf.py
│   └── ...
├── main.py
├── requirements.txt #开发依赖
├── setup.py #打包和发布管理模块
├── tests
│   ├── __init__.py
│   └── test_basic.py
│   └── ...
└── venv
```

## 安装

普通用户安装：

``` shell
pip install datappkit
```

开发者：

``` shell
git clone git@git-core.megvii-inc.com:brain/label/infrastructure/data-service-sdk.git
cd data-service-sdk
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

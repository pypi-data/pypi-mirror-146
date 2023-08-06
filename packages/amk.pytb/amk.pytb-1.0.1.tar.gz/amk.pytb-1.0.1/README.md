# PythonToolbox - Python 工具箱

## 安装

```bash
pip install amk.pytb
```



## 使用

### pip 相关

#### 新建 package

```bash
pytb create <pkg_name>
```



#### 发布 package


* 发布测试包：`pytb publish <-t/--test>`
* 发布正式包：`pytb publish`



#### 安装/更新 package

* 安装 测试包：`pytb install <pkg_name> [version] -t`，例如：`pytb install ampt2 0.0.1 -t`
* 安装 正式包：`pytb install <pkg_name> [version]`，例如：`pytb install ampt2 `
* 更新 测试包：`pytb install <pkg_name> -ut`，例如：`pytb install ampt2 0.0.2 -ut`
* 更新 正式包：`pytb install <pkg_name> -u`，例如：`pytb install ampt2 0.0.2 -u`



## 更新记录


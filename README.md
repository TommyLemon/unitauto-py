# unitauto-py 
**UnitAuto Python 库，可通过 pip 仓库等远程依赖。** <br />
**UnitAuto Python Library for remote dependencies with pip, etc.** <br />

同步纯函数：<br />
Sync pure function: <br />
https://github.com/TommyLemon/unitauto-py/blob/main/unitauto/test/testutil.py#L39-L40
<img width="1217" alt="image" src="https://github.com/TommyLemon/unitauto-py/assets/5738175/9ce1a1d1-883b-40be-bc77-7ed7da6f9ff6">

class 内成员函数：<br />
class member function: <br />
https://github.com/TommyLemon/unitauto-py/blob/main/unitauto/test/testutil.py#L111-L112
<img width="1279" alt="image" src="https://github.com/TommyLemon/unitauto-py/assets/5738175/2436b0d2-54f4-4c5a-be9c-c9618a258df2">

async & await 协程异步函数：<br />
async & await function: <br />
https://github.com/TommyLemon/unitauto-py/blob/main/unitauto/test/testutil.py#L63-L67
<img width="1280" alt="image" src="https://github.com/TommyLemon/unitauto-py/assets/5738175/100a6605-2c37-4c51-92ea-a6ae080c0ab4">

异步回调函数：<br />
thread callback function: <br />
https://github.com/TommyLemon/unitauto-py/blob/main/unitauto/test/testutil.py#L70-L83
<img width="1281" alt="image" src="https://github.com/TommyLemon/unitauto-py/assets/5738175/101c3736-93bc-409c-8f9f-b189e13cb06b">
<img width="1496" alt="image" src="https://github.com/TommyLemon/unitauto-py/assets/5738175/3e7ed198-29bb-4094-ab40-e32c7650cf8b">

代码覆盖率统计：<br />
Code coverage: <br />
<img width="1495" alt="image" src="https://github.com/TommyLemon/unitauto-py/assets/5738175/13e7ae6c-1384-4fdc-a7b0-79693895ec6a">
<img width="1495" alt="image" src="https://github.com/TommyLemon/unitauto-py/assets/5738175/054b46c8-e32c-4e45-ad6c-173bc63d5a9c">

<br />

## 使用
## Usage

#### 1. 在你的项目中添加依赖
#### 1. Add dependency to your project
```sh
	pip install unitauto
```
如果执行以上命令未成功，则将 pip 换成 pip3 试试：<br />
if you cannot run the command successfully, try pip3:
```sh
	pip3 install unitauto
```

<br />

#### 2. 启动单元测试服务
#### 2. Start unit testing server

添加以下代码到你的项目的 main.py <br />
Add the code below in main.py of your project <br />
https://github.com/TommyLemon/unitauto-py/blob/main/main.py#L3-L13
```py
import unitauto

if __name__ == '__main__':
    unitauto.server.start()
```

用 PyCharm 等 IDE 运行按钮来运行 main.py 或执行以下命令 <br />
Run main.py with PyCharm or execute command below <br />
```sh
	python main.py
```
如果执行以上命令未成功，则将 python 换成 python3 试试：<br />
if you cannot run the command successfully, try python3:
```sh
	python3 main.py
```

<br />

#### 3. 参考主项目文档来测试
#### 3. Test by following the main repo

https://github.com/TommyLemon/UnitAuto

<br />

### 4. 关于作者
### 4. Author
[https://github.com/TommyLemon](https://github.com/TommyLemon)<br />
<img width="1280" src="https://github.com/TommyLemon/unitauto-py/assets/5738175/e8ed6021-5f70-46bf-8d61-08c0d4d4dd9e">

如果有什么问题或建议可以 [去 APIAuto 提 issue](https://github.com/TommyLemon/APIAuto/issues)，交流技术，分享经验。<br >
如果你解决了某些 bug，或者新增了一些功能，欢迎 [提 PR 贡献代码](https://github.com/Tencent/APIJSON/blob/master/CONTRIBUTING.md)，感激不尽。
<br />
If you have any questions or suggestions, you can [create an issue](https://github.com/TommyLemon/APIAuto/issues). <br >
If you can added a feature or fixed a bug, please [create a pull request](https://github.com/TommyLemon/unitauto-py/pulls), thank you~

<br />

### 5. 其它项目
### 5. Link
创作不易、坚持更难，右上角点量 ⭐ Star 支持下吧，谢谢 ^\_^  <br />
Please ⭐ Star the repos that you like ^\_^  <br />

[UnitAuto](https://github.com/TommyLemon/UnitAuto) 机器学习零代码单元测试平台，零代码、全方位、自动化 测试 方法/函数 的正确性、可用性和性能

[unitauto-go](https://github.com/TommyLemon/unitauto-go) UnitAuto Go 库，可通过 GitHub 仓库等远程依赖

[APIJSON](https://github.com/Tencent/APIJSON) 🚀 腾讯零代码、全功能、强安全 ORM 库 🏆 后端接口和文档零代码，前端(客户端) 定制返回 JSON 的数据和结构

[uliweb-apijson](https://github.com/zhangchunlin/uliweb-apijson) Python 版 APIJSON，支持 MySQL, PostgreSQL, SQL Server, Oracle, SQLite 等

[APIAuto](https://github.com/TommyLemon/APIAuto) 敏捷开发最强大易用的 HTTP 接口工具，机器学习零代码测试、生成代码与静态检查、生成文档与光标悬浮注释，集 文档、测试、Mock、调试、管理 于一体的一站式体验

[SQLAuto](https://github.com/TommyLemon/SQLAuto) 智能零代码自动化测试 SQL 语句执行结果的数据库工具，任意增删改查、任意 SQL 模板变量、一键批量生成参数组合、快速构造大量测试数据

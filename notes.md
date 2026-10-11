## 1. 环境
- 系统：Ubuntu
- Python：3.10
- 虚拟环境：.venv
- PaddlePaddle：2.6.2，CPU 版
- PaddleDetection：release/2.9

激活环境：
source .venv/bin/activate

## 1.安装
 -## 二、环境选择

- 系统：Ubuntu Linux
- Python：3.10.12
- 虚拟环境：项目根目录下的 `.venv`
- PaddlePaddle：2.6.2，CPU 版
- PaddleDetection：官方 `release/2.9` 分支
- PaddleDetection 提交号：`b25522a0f4bde8c80603f3ba5e3472059972e3b5`
- NumPy：1.26.4
- setuptools：80.9.0

默认 Python 为 3.13，系统同时已有 Python 3.10。本次选择 Python 3.10，以配合所选 PaddlePaddle 版本和 PaddleDetection 工具。

创建独立环境可以隔离依赖，避免影响其他项目。选择 CPU 版是为了先完成基本图片推理，减少 CUDA、cuDNN 和 GPU 环境配置工作。

## 三、安装过程



作业仓库根目录为 `/home/charmaine/git demo/BaiduSmartCar2027-Training`

```bash
cd "/home/charmaine/git demo/BaiduSmartCar2027-Training"
```

### 1. 创建虚拟环境

```bash
uv venv --python /usr/bin/python3.10 .venv
```

使用系统已有的 Python 3.10 创建 `.venv`

激活环境：

```bash
source .venv/bin/activate
```



### 2. 安装 PaddlePaddle

```bash
uv pip install --python .venv/bin/python \
  'paddlepaddle==2.6.2' 'numpy<2'
```

`--python` 指定安装目标环境；`==` 固定版本；`numpy<2` 限制使用 NumPy 1.x，符合 PaddleDetection 的依赖要求。

### 3. 下载 PaddleDetection

```bash
git clone --depth 1 --branch release/2.9 \
  https://github.com/PaddlePaddle/PaddleDetection.git \
  .tools/PaddleDetection
```

下载官方发布分支到本地工具目录。`--depth 1` 减少 Git 历史下载量。

### 4. 安装依赖和源码包

```bash
cd .tools/PaddleDetection

uv pip install --python ../../.venv/bin/python \
  -r requirements.txt -e .
```

`-r requirements.txt` 指定当前目录的依赖清单，安装其中列出的包。

`-e .` 以可编辑方式安装当前目录的源码，使该环境可以通过 `import ppdet` 使用 PaddleDetection。


## 四、安装中遇到的问题

### 1. 缺少 setuptools

第一次检查时出现：

```text
ModuleNotFoundError: No module named 'setuptools'
```

当时 PaddleDetection 依赖尚未安装完毕。官方依赖清单包含 setuptools，完成依赖安装后补齐。

### 2. 缺少 pkg_resources

之后导入 PaddleDetection 时出现：

```text
ModuleNotFoundError: No module named 'pkg_resources'
```

排查发现，安装到的 setuptools 84.0.0 已移除该模块，而此版本 PaddleDetection 仍使用它。

在 PaddleDetection 目录执行：

```bash
uv pip install --python ../../.venv/bin/python \
  'setuptools==80.9.0'
```



## 五、安装验证

激活 `.venv` 后，我执行检查命令了：

```bash
python -c "import paddle; print(paddle.__version__); paddle.utils.run_check()"
```

关键输出：

```text
2.6.2
PaddlePaddle works well on 1 CPU.
PaddlePaddle is installed successfully! Let's start deep learning with PaddlePaddle now.
```

说明 PaddlePaddle 可以正常执行 CPU 计算。

随后执行：

```bash
python -c "import ppdet; print(ppdet.__file__)"
```

成功输出项目中 `.tools/PaddleDetection/ppdet/__init__.py` 的路径，说明 PaddleDetection 导入成功。

AI 另外完成了模型配置读取、推理命令帮助信息和依赖兼容性检查，均通过。上述检查验证的是安装状态，不能替代实际模型推理测试。

## 六、为什么使用 uv 和 .venv，而没有使用 Conda

Conda 同样可以完成本任务，本次选择 uv 是因为系统已有合适的 Python 3.10 和 uv，所需依赖可以通过 Python 包安装完成。

- pip 主要负责安装 Python 包，本身不创建环境。
- uv 可以创建虚拟环境，本次通过 `uv pip` 安装包。
- Conda 可以管理环境、Python 版本以及许多非 Python 依赖。



## 七、环境激活时的学习记录

`source .venv/bin/activate` 使用相对路径，需要在项目根目录执行。若已经进入 PaddleDetection 目录，激活脚本的相对路径应为 `../../.venv/bin/activate`。

如果终端位于其他目录，可以使用完整路径：

```bash
source "/home/charmaine/git demo/BaiduSmartCar2027-Training/.venv/bin/activate"
```

使用以下命令确认 Python 来源：

```bash
which python
```

路径应为 `/home/charmaine/git demo/BaiduSmartCar2027-Training/.venv/bin/python`。

## 八、AI 协助与个人学习

环境创建、依赖安装和安装期间的兼容问题由 AI 协助处理。我手动执行了 PaddlePaddle 自检和 PaddleDetection 导入结果。


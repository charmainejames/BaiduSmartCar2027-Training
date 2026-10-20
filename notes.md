## 1. 环境
- 系统：Ubuntu
- Python：3.10
- 虚拟环境：.venv
- PaddlePaddle：2.6.2，CPU 版
- PaddleDetection：release/2.9

激活环境：

```bash
source .venv/bin/activate
```

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
uv venv \
  --python /usr/bin/python3.10 \
  .venv
```

使用系统已有的 Python 3.10 创建 `.venv`

激活环境：

```bash
source .venv/bin/activate
```



### 2. 安装 PaddlePaddle

```bash
uv pip install \
  --python .venv/bin/python \
  paddlepaddle==2.6.2 \
  'numpy<2'
```

`--python` 指定安装目标环境；`==` 固定版本；`numpy<2` 限制使用 NumPy 1.x，符合 PaddleDetection 的依赖要求。

### 3. 下载 PaddleDetection

```bash
git clone \
  --depth 1 \
  --branch release/2.9 \
  https://github.com/PaddlePaddle/PaddleDetection.git \
  .tools/PaddleDetection
```

下载官方发布分支到本地工具目录。`--depth 1` 减少 Git 历史下载量。

### 4. 安装依赖和源码包

```bash
cd .tools/PaddleDetection

uv pip install \
  --python ../../.venv/bin/python \
  -r requirements.txt \
  -e .
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
uv pip install \
  --python ../../.venv/bin/python \
  setuptools==80.9.0
```



## 五、安装验证

激活 `.venv` 后，我执行检查命令了：

```bash
python \
  -c 'import paddle; print(paddle.__version__); paddle.utils.run_check()'
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
python \
  -c 'import ppdet; print(ppdet.__file__)'
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

环境创建、依赖安装和安装期间的兼容问题由 AI 协助处理。我在终端手动执行 PaddlePaddle 自检和 PaddleDetection 导入检查，查看输出并向 AI 提供结果。我针对 Python 版本、虚拟环境激活、uv 与 Conda 的区别、安装命令的参数和路径、官方自检命令来源等问题持续提问，并整理学习笔记。通过这些操作，我逐步理解了环境隔离、版本选择和安装验证的作用。

## 九、第一张图片检测

### 1. 第一张图片识别

使用官方预训练模型检测 `data/img_1.jpg`，确认单张图片的推理流程，看误检、漏检

模型为 PP-YOLOE-s，使用官方 COCO 预训练权重。选择较小的模型先跑通 CPU 推理。当前任务只有五张图片，用 CPU 因为可以减少 GPU 驱动、CUDA 等配置工作。
### 2. 执行命令、来源与参数

根据官方源码中的 `docs/tutorials/GETTING_STARTED_cn.md`、`configs/ppyoloe/README_legacy.md` 和 `tools/infer.py` 整理命令，选择配套的配置与权重，并填写本项目的输入、输出位置。

第一次执行的命令：
```bash
python tools/infer.py \
  -c configs/ppyoloe/ppyoloe_crn_s_300e_coco.yml \
  -o \
    use_gpu=False \
    weights=https://paddledet.bj.bcebos.com/models/ppyoloe_crn_s_300e_coco.pdparams \
  --infer_img=../../data/img_1.jpg \
  --output_dir=../../output/first_image \
  --draw_threshold=0.5 \
  --save_results=True
```
然后报错了
```bash
FileNotFoundError: [Errno 2] No such file or directory: 'dataset/coco/annotations/instances_val2017.json'
```
尝试读取默认的 COCO 标注文件，但本机没有这个文件。

我就把默认的标注路径改成空了TestDataset.anno_path=null

中间还有一次跑不出来，我手动中断了，结果其实是我热点没连网断了

这次运行被我按 Ctrl+C 中断，最后显示：

```text
KeyboardInterrupt
```


随后再次运行，出现 SSL 连接错误：

```text
ssl.SSLEOFError: [SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol (_ssl.c:1007)
```

这表示 HTTPS 连接在握手阶段意外断开，最终异常为 `requests.exceptions.SSLError`。

结果其实是我热点没连网断了


增加标注路径覆盖后，最终使用重试成功的命令：

```bash
python tools/infer.py \
  -c configs/ppyoloe/ppyoloe_crn_s_300e_coco.yml \
  -o \
    use_gpu=False \
    TestDataset.anno_path=null \
    weights=https://paddledet.bj.bcebos.com/models/ppyoloe_crn_s_300e_coco.pdparams \
  --infer_img=../../data/img_1.jpg \
  --output_dir=../../output/first_image \
  --draw_threshold=0.5 \
  --save_results=True
```
跑通了之后查看结果图片，左侧的人检测出来多了一个框是bird

### 6. 结果观察与数据核对
跑通了之后查看结果图片，右侧为 `person 0.90`，左侧的人被标为 `bird 0.5372`，存在错误的 bird 预测。运行成功不代表识别完全正确。

编写notes时检查当前磁盘上的 `bbox.json`，发现三个分数达到 0.5 的预测：

| 类别 | COCO category_id | 分数（约） |
|---|---|---|
| person | 1 | 0.8958 |
| person | 1 | 0.7211 |
| bird | 16 | 0.5273 |

#


### 7.  AI 协助




AI 协助完成初始环境安装和兼容问题处理，查阅官方源码、拟定推理命令、整理我的口述笔记。


## 十、五张图片检测与结果整理

### 1. 执行命令

单图跑通后，我在已激活 `.venv` 的 PaddleDetection 目录下运行五图检测：

```bash
python tools/infer.py \
  -c configs/ppyoloe/ppyoloe_crn_s_300e_coco.yml \
  -o \
    use_gpu=False \
    TestDataset.anno_path=null \
    weights=/home/charmaine/.cache/paddle/weights/ppyoloe_crn_s_300e_coco.pdparams \
  --infer_dir=../../data \
  --output_dir=../../output/all_images \
  --draw_threshold=0.5 \
  --save_threshold=0.5 \
  --save_results=True
```

相比单图命令，这次有四处调整：

| 调整 | 理由 |
|---|---|
| `weights=` 使用本地缓存文件路径 | 权重已经下载，直接加载同一官方权重，避免网址引发的联网校验 |
| `--infer_img` 改为 `--infer_dir` | 处理 `data/` 中全部五张指定图片 |
| 输出到 `../../output/all_images` | 与之前的单图试运行分开保存 |
| 增加 `--save_threshold=0.5` | JSON 保存和画框使用相同分数阈值，便于汇总 |

`weights=` 后面是绝对文件路径；`../../data` 和 `../../output/all_images` 是相对目录路径，均以当前 PaddleDetection 目录为起点。

### 2. 尝试过程和实际结果

我执行命令后查看终端输出，确认程序发现五张图片并完成 `5/5`。这次没有出现阻止运行的异常，不需要重新安装或下载权重。已有的 numba 警告没有阻止推理，默认 COCO 类别提示与空标注路径设置一致。

关键日志：

```text
Found 5 inference images in total.
The bbox result is saved to ../../output/all_images/bbox.json and do not evaluate the mAP.
Detection bbox results save in ../../output/all_images/img_1.jpg
Detection bbox results save in ../../output/all_images/img_2.jpg
Detection bbox results save in ../../output/all_images/img_4.jpg
Detection bbox results save in ../../output/all_images/img_3.jpg
Detection bbox results save in ../../output/all_images/img_5.jpg
```

随后我打开五张图片，将可视化结果提供给 AI 一起分析。

### 3. 检测效果和分类数量

以下数量按 `output/all_images/bbox.json` 中分数达到 0.5 的预测统计，是模型输出框的数量

| 图片 | 模型输出 | 最高分数（约） | 图片观察 |
|---|---|---|---|
| img_1 | person 2 个、bird 1 个 | person 0.8958；bird 0.5273 | 图片中是两个人；左侧还出现错误的 bird 预测，重叠标签使图片上的数量不易直接判断 |
| img_2 | cow 2 个 | 0.5636 | 其他可见的牛没有框，存在漏检；有的框包含不止一头牛 |
| img_3 | sheep 17 个 | 0.9294 | 羊群很密集且有遮挡，没有全部检出；框|
| img_4 | motorcycle 1 个、truck 1 个 | motorcycle 0.6767；truck 0.6435 | 实际是拖拉机，同一目标出现两种预测，分类不准确 |
| img_5 | banana 1 个 | 0.9482 | 类别正确，但模型用一个大框覆盖整串香蕉，没有逐根检测 |



### 6. 本地校验

在作业仓库根目录执行：

```bash
python3 tools/validate.py
```

输出：

```text
✓ 自动校验通过！请在验收日前准备现场演示与追问。
```


### 7. AI 协助

AI 提供命令和参数解释，，核对原始 JSON 与类别映射，生成汇总及规定命名的图片。帮助总结我的口头笔记


## 十一、完整命令

以下是演示操作清单，不代表已经完成新的实验。使用官方推理程序，按步骤手动运行，不依赖自写脚本。

### 1. 进入项目并激活环境

```bash
cd "/home/charmaine/git demo/BaiduSmartCar2027-Training"
source .venv/bin/activate
```

查看实际使用的 Python 和飞桨版本：

```bash
which python
python --version
python -c "import paddle; print(paddle.__version__)"
```

需要展示官方 CPU 自检时执行：

```bash
python -c "import paddle; paddle.utils.run_check()"
```

### 2. 现场重新检测五张图片

```bash
cd .tools/PaddleDetection

python tools/infer.py \
  -c configs/ppyoloe/ppyoloe_crn_s_300e_coco.yml \
  -o \
    use_gpu=False \
    TestDataset.anno_path=null \
    weights=/home/charmaine/.cache/paddle/weights/ppyoloe_crn_s_300e_coco.pdparams \
  --infer_dir=../../data \
  --output_dir=../../output/acceptance_demo \
  --draw_threshold=0.5 \
  --save_threshold=0.5 \
  --save_results=True \
  --rtn_im_file=True
```

新结果保存到 `output/acceptance_demo/`




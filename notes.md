# 任务二：文字识别学习记录

## 一、任务目标与进度

复用任务一的运行环境，使用 PaddleOCR 识别 `data/` 中十张指定图片，完成至少一次后处理对比实验，并整理 `results.json` 和笔记。实验时一次只改一个变量，保留处理前后的数据，最后执行校验并提交。

目前完成了环境检查、PaddleOCR 安装和第一张图片识别。批量识别、原始结果文件保存、后处理实验和最终提交尚未完成。

## 二、环境准备

- Python：3.10.12，复用项目根目录下的 `.venv`。
- PaddlePaddle：2.6.2，CPU 版。
- PaddleOCR：2.9.1。
- NumPy：1.26.4。
- OCR 模型：PP-OCRv4。

任务要求复用环境，因此没有重新创建环境。选择 PaddleOCR 2.x 路线，并固定已有 PaddlePaddle 和 NumPy 版本，减少依赖升级带来的兼容性变化。使用 CPU 完成小规模图片推理，不需要重新配置 GPU 环境。

以下命令均在项目根目录执行。

### 1. 激活并检查环境

```bash
source .venv/bin/activate
```

`.venv/bin/activate` 是激活脚本的相对路径。激活只对当前终端生效，新终端需要重新执行。

```bash
python -c "import sys, paddle; print(sys.executable); print(paddle.__version__)"
```

检查结果：Python 来自项目的 `.venv/bin/python`，PaddlePaddle 版本为 `2.6.2`，导入正常。

### 2. 安装和验证 PaddleOCR

```bash
uv pip install --python .venv/bin/python \
  "paddleocr==2.9.1" \
  "paddlepaddle==2.6.2" \
  "numpy==1.26.4"
```

- `uv pip install`：安装 Python 包，沿用任务一的安装工具。
- `--python .venv/bin/python`：指定目标环境，其中 `.venv/bin/python` 是 Python 可执行文件的相对路径。
- `==`：固定版本；后两项固定已有依赖。
- 行末的 `\`：表示同一条命令在下一行继续。

检查命令：

```bash
python -c "from paddleocr import PaddleOCR; import importlib.metadata as m; print(m.version('paddleocr'))"
```

实际输出 `2.9.1`，说明安装完成且能够导入，还需要实际图片推理验证。

## 三、第一张图片识别

### 1. 执行命令

```bash
python - <<'PY'
from paddleocr import PaddleOCR

ocr = PaddleOCR(
    use_gpu=False,
    lang="ch",
    ocr_version="PP-OCRv4",
    use_angle_cls=True,
    drop_score=0.0,
)

result = ocr.ocr("data/sign_1.jpg", cls=True)

for page in result:
    if page is None:
        print("未识别到文字")
        continue
    for box, (text, score) in page:
        print(f"文字：{text!r}，置信度：{score:.4f}")
        print(f"位置：{box}")
PY
```

`python - <<'PY'` 到最后单独一行的 `PY`，表示将中间代码交给 Python 执行，没有创建脚本文件。`data/sign_1.jpg` 是输入图片的相对路径。

### 2. 参数与选择理由

| 参数 | 含义和选择理由 |
| --- | --- |
| `use_gpu=False` | 使用 CPU，沿用已有环境 |
| `lang="ch"` | 使用中文识别配置，也支持英文和数字 |
| `ocr_version="PP-OCRv4"` | 明确模型版本，方便复现 |
| `use_angle_cls=True`、`cls=True` | 启用文字方向分类，主要区分正向与倒置，不是任意角度矫正 |
| `drop_score=0.0` | 暂时不按识别置信度丢弃结果，保留低分文字供后处理对比 |

`drop_score=0.0` 不代表关闭所有过滤。文字检测阶段仍有自己的阈值，图片上的所有文字不一定都能进入识别阶段。

### 3. 运行结果

本次下载和推理成功，没有报错。共检测到八个文字区域，完成方向分类并返回八条识别结果。

### 4. 实际识别结果

以下文字来自本次终端输出，分数保留四位小数，未进行纠错或额外的置信度过滤。

| 识别文字 | 置信度 |
| --- | --- |
| 雅都美妆 | 0.9993 |
| 公交站点 | 0.9958 |
| 化妆品 | 0.9987 |
| 康洋综业连销 | 0.6563 |
| KANGZE | 0.9850 |
| 红荔园 | 0.9984 |
| 原雅芳店 | 0.9938 |
| 本站名： | 0.9756 |

对照原图，大字如“雅都美妆”“公交站点”能够正确识别；右上角招牌被识别为“康洋综业连销”，存在错字，需要进一步人工核对。站牌上的线路数字和大量小字未出现在输出中，存在漏检或漏识，尚未定位到具体阶段。




## 四、十张图片基线与人工核对

### 1. 当前进度与文件用途

十张指定图片的基线识别，并保存到 `output/ocr_baseline.json`

- `output/ocr_baseline.json`：模型实际返回的文字、完整置信度和文字框坐标
- `output/ocr_review/sign_1_review.jpg` 至 `sign_10_review.jpg`：AI 根据已有坐标生成的核对图，左侧框号对应右侧文字；没有重新识别。编号与每张图片的基线条目顺序一致。
- `notes.md`：记录人工核对、无法确认的内容、实验理由和前后对比分析。
- 后处理实验 JSON：后续另存各组程序处理结果；最终再按任务格式整理根目录的 `results.json`。本阶段尚未生成。

十张图片共返回 102 条结果，其中四条为空文字：第 7 张第 14 条、第 8 张第 33 条、第 10 张第 4、6 条。第 2 张返回零条，仍保留图片记录。结果条数不等于正确文字条数。

### 2. 核对方式与判定原则

AI 先对照原图和编号框给出候选问题，我再查看图片并确认、纠正或标记无法看清的部分。以下为联合人工核对记录

分开记录错字、漏识、图案误检和无法确认；无法看清的内容不直接算作确定正确或确定错误。简繁差异与真正错字分开判断。被遮挡的文字不凭常见词语补全。

### 3. 各图片的问题记录

| 图片 | 核对结果 |
| --- | --- |
| `sign_1.jpg` | 第 4 条“康洋综业连销”对应的招牌原文看不清，无法确认。站牌线路数字 1、18、20、31、32、40、104 未出现在结果中；其他主要大字基本正确。 |
| `sign_2.jpg` | 图中没有清晰可辨的文字，零条结果目前合理。 |
| `sign_3.jpg` | 第 3 条“雪主咖啡”应为“雪王咖啡”；第 2 条“H”对应雪人图案，属于误检。第 18 条“果茶爪”、第 20 条“夏日救”存在错字或内容不完整；完整原文仍需逐字核实。顶部饮品名和右侧招聘文字有漏识。 |
| `sign_4.jpg` | 第 1 条“杨提”应为“杨堤”；第 3 条“保持水土、人人”内容不完整。第 4 条英文 `resouree` 对照原图应为 `resources`，第 5 条 `obligatin` 应为 `obligation`。竖排楹联未完整识别。 |
| `sign_5.jpg` | 第 1 条“#福器”将中心“福”字与附近内容混合识别。对联末尾人工核对为“事事顺”“方方利”，OCR 分别输出“事事气”“方方部”。 |
| `sign_6.jpg` | `TIMBANG` 与原图一致，暂未发现明显问题，可作为正确识别对照。 |
| `sign_7.jpg` | 具体记录见下表。顶部禁烟横幅大部分未返回；底部英文被拆成两段。 |
| `sign_8.jpg` | 第 1、32 条将叶片装饰识别成文字，第 25 条 `SS` 对应箭头图案，属于误检；第 33 条为空文字。多处店名存在误识，典型例子见下表。部分店名、左侧标志和时间戳未完整返回。 |
| `sign_9.jpg` | 第 2 条“工神極喷”的末字应为“峻”，牌匾按右向左的传统顺序读为“峻極神工”，同时存在错字与阅读顺序问题。第 1 条“春四十一年五月端陽日”开头的年号未确认，不凭历史常识补全。小字题款未完整返回。 |
| `sign_10.jpg` | 第 1 条“家”和第 2 条 `U` 对应游乐设施装饰，属于误检。地面书法大部分未识别，第 4、6 条为空文字。第 3 条 `adTalk` 为招牌可见部分，开头受树遮挡，不补猜被遮住的文字。第 5、7 条尚未逐字确认。 |

### 4. 第 7 张的重点核对

| 框号 | OCR 原文 | 人工核对 |
| --- | --- | --- |
| 4 | 鼠患問题自然行 | 末字应为“冇”（，即“鼠患問題自然冇” |
| 6 | 肉飞 | 对应逃生标识图案，不是这两个文字，属于图案误检。 |
| 7、8、9、10 | 福；衣药酶牛；的0；格地节 | 太模糊，无法确认原文，不直接判对错。 |
| 13 | 電泉 | 原文为“電騙”（电骗）。 |
| 14 | 空文字 | 保留为空结果的事实，不补写文字。 |
| 16 | 不准放鞋物 | 原文为“不准放雜物”（不准放杂物）。 |
| 18 | 进者會被检控 | 首字应为“違”，AI 初查发现，用户认可该项，其他字仍以原图为准。 |
| 19 | 1872 | 看不清，无法确认。 |
| 21 | Kong Cleo | 末尾可见字母为 `Clea`，不是 `Cleo` |

### 5. 第 8 张的典型错字



| 框号 | OCR 原文 | 人工核对文字 |
| --- | --- | --- |
| 3 | 總宝 | 總覽 |
| 7 | 卓兴西房有限公司 | 卓興西餅房有限公司 |
| 14 | 海怡專菜洗衣店 | 海怡專業洗衣店 |
| 17 | 金旺食品题级市 | 金旺食品超級市場 |
| 24 | 香港饭信鞋锁店 | 香港恆信鞋鎖店 |
| 31 | 佳骏水電冷氧维修 | 佳駿水電冷氣維修 |

### 6. 下一步如何使用这些记录

先保持模型、基线文件和十张图片不变，仅改变后处理置信度阈值，拟比较 0.5 与 0.8 两组。各组另存结果，检查删除了哪些明确错误、图案误检和空文字，以及是否误删正确结果



## 五、后处理实验：比较置信度阈值

### 1. 实验方法和结果

读取同一份 `output/ocr_baseline.json`，不重新运行模型，只改变识别置信度阈值。统一使用 `score >= threshold` 作为保留条件，对全部十张图应用相同规则。不替换文字，也不额外添加空字符串过滤规则。

| 识别置信度阈值 | 保留条数 | 删除条数 |
| --- | ---: | ---: |
| 0.0（基线） | 102 | 0 |
| 0.5 | 78 | 24 |
| 0.8 | 56 | 46 |

结果文件位于 `output/ocr_threshold_experiment/`：`threshold_0_5.json`、`threshold_0_8.json` 为保留结果；`removed_0_5.json`、`removed_0_8.json` 为删除清单，包含基线框号；`comparison.md` 为对照表，`summary.json` 为数量汇总。

实际执行的过滤核心如下，其余辅助代码负责保存文件和生成对照表：

```python
for threshold in [0.5, 0.8]:
    for image in baseline["images"]:
        kept = []
        removed = []
        for item in image["texts"]:
            if item["score"] >= threshold:
                kept.append(item)
            else:
                removed.append(item)
```

### 2. 我对结果的判断与选择

检查删除清单后发现0.8 过高，删除了不少只有部分文字错误、其余内容仍可用的整条结果。例如“出入平安事事气”（0.7673）虽然末字有误，但整句删除会丢失前面的正确信息。

0.5 删除了四条空文字，以及逃生标识被误识成的“肉飞”、箭头被误识成的 `SS` 等。0.5 更适合当前保留可用信息的目标，后续优先使用这一过滤阈值。这是基于当前图片及人工核对的选择，未计算完整准确率，不能认定它对所有新图片都最好。

过滤只能删除结果，不能修正错字或补回漏识。高分错误仍会保留，例如“不准放鞋物”（0.8533）和“工神極喷”（0.8218）。无法看清的原文不强行判对错。

## 六、检测尺寸实验：960 与 1536

### 1. 修改内容与理由

为尝试找回小字，将 `det_limit_side_len` 从默认 960 提高为 1536，保持 `det_limit_type="max"`。十张图统一设置，模型、语言、CPU、方向分类及其他检测参数不变。

这个参数限制送入检测模型的最长边，提高上限可减少原图被缩小的程度

两组原始识别均保留 `drop_score=0.0`，对比时再统一应用 0.5 后处理，避免同时改变两个变量。实际模型初始化代码：

```python
ocr = PaddleOCR(
    use_gpu=False,
    lang="ch",
    ocr_version="PP-OCRv4",
    use_angle_cls=True,
    drop_score=0.0,
    show_log=False,
    det_limit_side_len=1536,
    det_limit_type="max",
)
```

使用 `ocr.ocr(str(image_path), cls=True)` 依次识别 `sign_1.jpg` 至 `sign_10.jpg`，保存文字、分数及坐标；过滤条件仍为 `item["score"] >= 0.5`。代码由 AI 根据 PaddleOCR 接口和任务需要编写，不是整段复制官方文档。

### 2. 保存文件与数量对比

- `output/ocr_size_1536/raw.json`：1536 设置下未经识别置信度过滤的结果。
- `output/ocr_size_1536/filtered_0_5.json`：统一应用 0.5 过滤后的结果。
- `output/ocr_size_1536/comparison.json`：每张图的结果数量对比及本次推理耗时。
- `output/ocr_size_1536/change_review/`：两组均经过 0.5 过滤后的异色核对图；`matching.json` 保存近似框匹配记录。

异色图中，蓝色表示匹配区域文字未变，红色表示文字变化，绿色表示新结果未匹配旧框，橙色虚线表示旧结果未匹配新框。颜色不代表正确或错误。框拆分或合并可能影响匹配，需要人工核对。N 为本次新结果编号，O 为本次旧结果编号，不能直接套用最初基线核对图的编号。

| 图片 | 960 原始条数 | 1536 原始条数 | 960 经 0.5 过滤 | 1536 经 0.5 过滤 |
| --- | ---: | ---: | ---: | ---: |
| sign_1.jpg | 8 | 14 | 8 | 14 |
| sign_2.jpg | 0 | 2 | 0 | 0 |
| sign_3.jpg | 21 | 33 | 13 | 18 |
| sign_4.jpg | 5 | 7 | 4 | 5 |
| sign_5.jpg | 3 | 3 | 3 | 2 |
| sign_6.jpg | 1 | 1 | 1 | 1 |
| sign_7.jpg | 22 | 25 | 17 | 16 |
| sign_8.jpg | 33 | 64 | 28 | 57 |
| sign_9.jpg | 2 | 3 | 2 | 2 |
| sign_10.jpg | 7 | 8 | 2 | 2 |
| 合计 | 102 | 160 | 78 | 117 |


### 3. 逐图分析与我的补充核对

AI 先查看对比图给出初步判断，我再核对并修正。以下以我的最新核对为准；看不清的内容继续保留不确定，不回填到模型原始结果中。

| 图片 | 对比与核对结论 |
| --- | --- |
| `sign_1.jpg` | 过滤后从 8 条增加到 14 条，找到了更多站牌小字。N11 的站名拼音我确认正确，图中 `i` 难以辨认，撤回 AI 对其“拼写错误”的初判，不擅自修改 JSON 拼音。N10 原文为“停靠路线”，OCR 为“本路线”；N12 原文为“医保定点”，OCR 为“保定点”，均不完整。N13 受遮挡，无法确认。N14 将线路 18 识别为 8，其他线路数字仍未完整找回。右上招牌仍无法确认原文。 |
| `sign_2.jpg` | 两组过滤后均为空，原图没有清晰可辨的文字，目前结果合理。 |
| `sign_3.jpg` | 找到更多饮品文字和电话号码。N3 原文确认为“椰椰拿铁”，OCR“御柳拿铁·”有误；N14 电话号码 `1738955887` 我确认正确。顶部“葡萄冰美式”与价格数字 6 合并输出；价格 8 增加货币符号。原先正确的“奋斗一杯”未保留，“雪主咖啡”等错字仍在。因此有新增可用内容，也有退步。 |
| `sign_4.jpg` | 整体偏退步：“杨提”变为“杨提！”，仍错且多符号；“保持水土、人人”变成“保特水土”，新增错字且内容减少。新增楹联结果仍混乱，两行英文拼写错误也未解决。 |
| `sign_5.jpg` | 没有明确改善：“出入平安事事气”变成“出入平安事事”，虽然去掉错误末字，但正确末字“顺”仍未读出；“方方部”仍未修正为“方方利”。顶部“福”字区域不再保留结果，不能把错误条目减少等同于读对了。 |
| `sign_6.jpg` | 两组均正确识别 `TIMBANG`，文字结果不变。分数下降不等于文字识别变错。 |
| `sign_7.jpg` | 有得有失：新结果“電骗”正确；热线 1823 单独识别正确，但“查詢”变为“查鹤”，出现退步。底部英文合为一句，末尾仍为 `Cleo`，与我此前确认的 `Clea` 不符。“自然行”“放鞋物”仍错，“进者被检控”还漏了原来的“會”。海报底部数字仍看不清，不判定哪版正确。 |
| `sign_8.jpg` | 收益最明显，过滤后由 28 条增加到 57 条，找到更多店名、编号及时间戳。“杏花工程有限公司”“金旺食品超级市场”“富记蔬菜”、编号 38-39 比旧结果改善；新增“德利美食”“元记豆腐”“有貨到”和时间戳初步可用。N48“川奇蛋”中的“蛋”我确认正确，撤回 AI 关于该字可能错误的初判。N38 将 31B 识别为 318，叶片装饰误检及“總宝”等错字仍在，不能认定所有新增结果都正确。 |
| `sign_9.jpg` | 大字从“工神極喷”变成“工神喷”，漏了“極”，阅读顺序仍错，属于退步。年号开头仍未完整识别，虽然删除了旧版错误的“春”，也不能认为原文已正确读出。 |
| `sign_10.jpg` | 两组文字基本不变，地面书法仍大面积漏识。我确认 N2 对应的实际文字是“俭”，OCR 仍输出“容”，属于错字，分数提高不代表纠正成功。 |



### 4. 当前结论与实验局限

我选择 0.5 作为当前优先的后处理阈值；1536 对第 8 张的小字有明显收益，对第 1、3、7 张有得有失，第 4、9 张有退步，第 10 张倾斜书法没有解决。


## 七、AI 协助、我的工作与后续安排

生成方便复核的图，撰写笔记

## 八、补充诊断：人工裁剪与检测框阈值

本节更新前面的阶段记录：此后已完成两次人工裁剪诊断，以及全图检测框阈值 0.6、0.3、0.1 的对比。新增 OCR 实验由我在终端运行，AI 提供命令、分析已有文件并生成核对图。

### 1. 第 1 张站牌裁剪

为检查小字漏识，使用原图坐标 `(580, 250, 790, 590)` 裁出站牌。坐标顺序为左、上、右、下；保持检测尺寸上限 1536、检测框阈值默认 0.6、`drop_score=0.0`，没有额外放大。

输出在 `output/ocr_sign1_crop/`，包含 `sign_1_crop.png` 和 `raw.json`。共返回六条：

| 识别文字 | 识别置信度 |
| --- | ---: |
| 2 | 0.3508 |
| 红荔园 | 0.9954 |
| 本站名： | 0.9806 |
| 体靠路线 | 0.7492 |
| Hongllyuan | 0.9640 |
| 1 | 0.0502 |

线路数字没有被完整找回；“停靠路线”读成“体靠路线”。两条数字均低于后处理阈值 0.5。这个实验没有达到预期，保留结果而不覆盖。

裁剪减少背景，但没有增加字本身的像素；相比已使用 1536 上限的整图，不是裁剪就等于把小字放大。

### 2. 第 7 张黄色横幅裁剪

按原图宽度的 50% 至 100%、高度的 0% 至 27% 选取横幅区域，本图实际裁剪框为 `(640, 0, 1280, 259)`。保持与上面相同的 OCR 设置，输出在 `output/ocr_sign7_banner_crop/`。

仅返回“禁”（0.9750）、“2”（0.0496）、“Oa”（0.1673），没有找回主要横幅文字。裁剪图可见范围内的主要内容仍在，但横幅右端本来就超出原图，不能恢复画面外的文字。

随后只把检测框阈值从 0.6 降到 0.3，使用同一张裁剪图，输出在 `output/ocr_sign7_banner_box_0_3/raw.json`。本次返回八条，新增“此街市室内凰厅”（0.9286）、`fience $1,500`（0.8472）、`Fixed penaly正oking`（0.8116）等片段。说明降低框保留阈值能找回一些候选区域，但识别仍有错字和缺失，不能等同于横幅识别正确。


## 九、全图检测框阈值对比与参数选择



### 2. 实验设置与命令要点

不使用手动裁剪，统一识别十张原图；固定 PP-OCRv4、中文配置、CPU、方向分类、检测最长边上限 1536、原始输出 `drop_score=0.0`，只比较检测框阈值 0.6、0.3、0.1。各组另存原始结果，之后都按识别分数 0.5 过滤。

在项目根目录激活环境后，通过 `python - <<'PY'` 方式执行 多行 Python 命令。初始化的关键设置如下，分别将 `det_db_box_thresh` 设为 0.3、0.1 运行，输出目录也分别指定，不覆盖上一组：

```python
ocr = PaddleOCR(
    use_gpu=False,
    lang="ch",
    ocr_version="PP-OCRv4",
    use_angle_cls=True,
    drop_score=0.0,
    show_log=False,
    det_limit_side_len=1536,
    det_limit_type="max",
    det_db_box_thresh=0.3,
)
```

识别调用仍是 `ocr.ocr(str(path), cls=True)`。默认 0.6 组为此前 `output/ocr_size_1536/` 的结果，0.3 组保存在 `output/ocr_size_1536_box_0_3/`，0.1 组保存在 `output/ocr_size_1536_box_0_1/`。每组的 `raw.json` 保留全部返回结果，`filtered_0_5.json` 保存识别分数不低于 0.5 的条目。

0.3、0.1 组各自的 `change_review/` 中保存与上一组的异色核对图、`comparison.md` 和 `matching.json`。颜色用于标记变化，不代表对错；N/O 编号仅属于对应轮次。

### 3. 数量对比

| 图片 | 0.6 过滤后 | 0.3 过滤后 | 0.1 过滤后 |
| --- | ---: | ---: | ---: |
| sign_1.jpg | 14 | 14 | 14 |
| sign_2.jpg | 0 | 0 | 0 |
| sign_3.jpg | 18 | 19 | 19 |
| sign_4.jpg | 5 | 5 | 5 |
| sign_5.jpg | 2 | 2 | 2 |
| sign_6.jpg | 1 | 1 | 1 |
| sign_7.jpg | 16 | 20 | 23 |
| sign_8.jpg | 57 | 57 | 57 |
| sign_9.jpg | 2 | 2 | 2 |
| sign_10.jpg | 2 | 3 | 3 |
| 合计 | 117 | 123 | 126 |

三组原始结果分别为 160、189、192 条。以上条数包含错字和误检，不等于正确文字数量，不能据此计算准确率或认定阈值越低越好。

### 4. 人工核对与取舍

| 图片 | 对比结论 |
| --- | --- |
| 第 1 张 | 三组过滤后均为 14 条，文字未变，线路数字漏识没有解决。 |
| 第 2 张 | 三组过滤后均为空；没有保留下来的新增误检。 |
| 第 3 张 | 从 0.6 降至 0.3 后找回“奋斗一杯！”（0.8965），有可用收益；再降至 0.1 无新增收益。其他旧错字仍在。 |
| 第 4、5、6、9 张 | 过滤后文字未变；已有的错字、漏识或正确结果基本保持。 |
| 第 7 张 | 0.3 找回黄色横幅的部分中文和罚款英文片段，我认为这一变化有价值；但仍有错字，新增“地”“禁地节”也不完整。0.1 又增加三个结果，但我确认新框有跨行、重叠，新内容不算有用信息。 |
| 第 8 张 | 从 0.6 到 0.3，英文 `the fresh oneMARKET` 恢复为 `the fresh one MARKET`；装饰误识文字也有变化。0.1 与 0.3 的过滤后文字相同，既有错字与装饰误检未解决。 |
| 第 10 张 | 0.3 和 0.1 均新增 `14`（0.5548），我确认原图对应的是书法文字，不是数字，属于新增误识。“俭”读成“容”的错误也仍然存在。 |

第 7 张中，从 0.3 降到 0.1 后：新增“冀例街市室内航凰”
|“例吸定频s1.500”
|“Fixed penalyo正moking”。对照框图可见跨行与重叠，判断这些新增结果不可用，不计为有效收益。原有中文主句从“此街市室内園厅”变为“此街市室内園藏”，并未更正确；“进者被检控”补回“會”，但首字仍错，仅是局部变化。

### 5. 当前优先配置及理由

当前优先选择统一配置：

```text
检测最长边上限：1536
检测框阈值：0.3
识别结果后处理：保留 score >= 0.5
```

选择 1536 是为了保留更多小字细节，接受部分图片退步；选择检测框阈值 0.3，是因为相比 0.6 找回了第 3 张标语和第 7 张部分横幅，而继续降至 0.1 的新增内容经我核对没有可用收益。0.3 也增加了第 10 张误识的 `14`，这个代价明确保留在记录中，不手动删除特定图片的条目来美化结果。

识别分数 0.5 则来自此前后处理对比，避免 0.8 整条删除过多部分正确的内容。

## 十、最终产物与验收复现

### 1. 最终结果来源

采用统一配置：PP-OCRv4、中文配置、CPU、文字方向分类、检测最长边上限1536、检测框阈值0.3、识别结果过滤0.5。没有逐张设置参数，也没有使用人工裁剪作为最终流程。

根目录 `results.json` 从 `output/ocr_size_1536_box_0_3/filtered_0_5.json` 整理，按任务示例保存 `engine`、十张图的 `images` 和 `postprocess`；每条仅提取原有 `text`、`score`，不改变文字或分数。实验文件继续保留文字框坐标。

共123条结果，第2张保留空列表。第10张误识的 `14` 仍如实保留，不手工删掉特定图片的错误来美化结果。现有文件和文件夹名称保持不变。

### 2. 当前环境与命令来源

复用任务一的 `.venv`，Python 3.10.12、PaddlePaddle 2.6.2、PaddleOCR 2.9.1、NumPy 1.26.4、setuptools 80.9.0。当前安装的 OpenCV 包为 opencv-python 4.5.5.64 和 opencv-contrib-python 4.11.0.86，Pillow 12.3.0。此处记录实际环境，不代表已经在全新环境验证全部复现。

PaddleOCR接口及参数来自工具用法，批量循环、结果保存、对比及可视化代码由AI根据任务编写。初始基线由我执行；识别分数过滤和首次1536实验由AI执行；后续裁剪和检测框阈值实验由我按命令执行。我核对原图、指出0.8过度过滤、确认0.1新增内容不可用，并选择当前方案。

### 3. 十张原图现场复现命令

以下在项目根目录执行，创建独立演示输出，不改历史实验和根目录最终结果。本次整理笔记没有执行下面的新推理。

```bash
source .venv/bin/activate
```

```bash
python - <<'PY'
import json
from pathlib import Path
from paddleocr import PaddleOCR

output_dir = Path("output/acceptance_demo")
if output_dir.exists():
    raise SystemExit("演示目录已存在，请改用新的目录名。")

paths = [Path("data") / f"sign_{i}.jpg" for i in range(1, 11)]
for path in paths:
    if not path.is_file():
        raise FileNotFoundError(path)

ocr = PaddleOCR(
    use_gpu=False,
    lang="ch",
    ocr_version="PP-OCRv4",
    use_angle_cls=True,
    drop_score=0.0,
    show_log=False,
    det_limit_side_len=1536,
    det_limit_type="max",
    det_db_box_thresh=0.3,
)

images = []
for path in paths:
    texts = []
    result = ocr.ocr(str(path), cls=True)
    for page in result:
        for box, (text, score) in page or []:
            texts.append({"text": text, "score": float(score), "box": box})
    images.append({"file": path.name, "texts": texts})
    print(f"{path.name}：{len(texts)} 条原始结果")

raw = {
    "engine": "PP-OCRv4",
    "settings": {
        "use_gpu": False,
        "lang": "ch",
        "ocr_version": "PP-OCRv4",
        "use_angle_cls": True,
        "drop_score": 0.0,
        "det_limit_side_len": 1536,
        "det_limit_type": "max",
        "det_db_box_thresh": 0.3,
    },
    "images": images,
}
output_dir.mkdir(parents=True)
with (output_dir / "raw.json").open("x", encoding="utf-8") as file:
    json.dump(raw, file, ensure_ascii=False, indent=2)

# 同一份原始输出分别进行识别分数过滤，不重新运行模型。
for threshold in [0.5, 0.8]:
    kept_images = []
    removed = []
    for image in images:
        kept = []
        for index, item in enumerate(image["texts"], 1):
            if item["score"] >= threshold:
                kept.append({"text": item["text"], "score": item["score"]})
            else:
                removed.append({
                    "file": image["file"],
                    "baseline_index": index,
                    **item,
                })
        kept_images.append({"file": image["file"], "texts": kept})
    filtered = {
        "engine": "PP-OCRv4",
        "images": kept_images,
        "postprocess": {
            "score_threshold": threshold,
            "description": f"保留识别分数不低于{threshold}的结果，未纠错。",
        },
    }
    tag = str(threshold).replace(".", "_")
    for filename, content in [
        (f"results_score_{tag}.json", filtered),
        (f"removed_score_{tag}.json", removed),
    ]:
        with (output_dir / filename).open("x", encoding="utf-8") as file:
            json.dump(content, file, ensure_ascii=False, indent=2)
    count = sum(len(image["texts"]) for image in kept_images)
    print(f"识别分数阈值 {threshold}：保留 {count} 条，删除 {len(removed)} 条")

print(f"演示结果已保存到：{output_dir}")
PY
```

# C-Value: A method for reasonable measurement of nested terms

![](https://img.shields.io/badge/language-python-blue.svg)
![](https://img.shields.io/badge/license-Apache_2.0-green.svg)

-----

术语自动抽取方法C-Value方法的Python实现版本，支持CLI方式对语料文本直接进行术语抽取。分词技术采用工业界和学术界高度认可的`HanLP`自然语言处理工具包。

CValue提供一下功能：

* 支持多种语料输入，包括
    * CSV、TXT
* 候选术语C-value快速计算
* 候选术语集合快速排序
* 候选术语集合多文件格式导出，包括：
    * CSV、TXT、JSON

### 环境配置

-----

具体的操作视操作者当前操作系统下的真实情况而定，如果系统默认的python版本就是`python3`可以直接按下面的命令操作，如果系统有多个版本可以直接见下面命令里的`python`改为`python3`。

```shell
pip install virtualenv
python -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 命令行执行

-----

INPUT_CORPUS_FILE_PATH: 需要进行术语抽取的语料的文件路径 OUTPUT_TERMS_FILE_PATH: 需要导出候选术语集合的文件路径

```shell
python cvalue.py INPUT_CORPUS_FILE_PATH OUTPUT_TERMS_FILE_PATH
```

### API执行

-----

```python
from cvalue import CValue

input_path = None
output_path = None

# 候选术语抽取
candidate_terms_dict = CValue(input_path, output_path).terms_extraction()

# 候选术语集合导出
CValue(input_path, output_path).terms_export()
```
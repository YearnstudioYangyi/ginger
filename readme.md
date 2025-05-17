# Ginger

Ginger 是一个将自然语言描述的代码逻辑翻译为可执行代码的工具。

## 功能

- 支持将自然语言逐行翻译为指定编程语言的代码。
- 自动检测语法错误并返回详细的错误信息。
- 支持多种编程语言的代码生成。
- 输出 JSON 格式的翻译结果。

## 安装

1. 克隆项目到本地：

   ```bash
   git clone <repository-url>
   cd ginger
   ```

2. 安装依赖：

   ```bash
   pip install -r requirements.txt
   ```

## 使用方法

1. 准备一个包含自然语言代码描述的输入文件，例如 `input.txt`。
2. 运行以下命令：

   ```bash
   python ginger.py --key <your-api-key> -f input.txt -l <language> -t <traceback-language> -i <indentation>
   ```

   参数说明：
   - `--key`：必填，API密钥，从[智谱AI开放平台](https://bigmodel.cn)获取。
   - `-f`：输入文件路径，默认为 `input.txt`。
   - `-l`：目标编程语言，默认为 `Python`。
   - `-t`：错误信息语言，默认为 `en-US`。
   - `-i`：代码缩进空格数，默认为 `4`。

3. 翻译结果将保存为 `<输入文件名>.<目标语言扩展名>`，或在有语法错误时打印错误信息。

## 示例

输入文件内容：

```txt
声明一个名为“加法”的函数，声明两个参数名为a和b，类型都是整数，实现如下：
    返回两个参数的和
```

运行命令：

```bash
python ginger.py --key <your-api-key> -f input.txt -l Python
```

输出文件内容：

```python
def 加法(a: int, b: int):
    return a + b
```

## 注意事项

- 确保输入文件内容符合自然语言描述的代码逻辑。
- 如果遇到语法错误，工具会返回详细的错误信息。

## 许可证

本项目使用 MIT 许可证。
> Readme written by GPT-4o

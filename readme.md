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

### 指定单文件

1. 准备一个包含自然语言代码描述的输入文件，例如 `input.txt`。
2. 运行以下命令：

   ```bash
   python ginger.py [options]
   ```

   参数说明：
   - `--key`：必填，API密钥，从[智谱AI开放平台](https://bigmodel.cn)获取。
   - `-f`：输入文件路径，与 `-c` 互斥。
   - `-c`：配置文件路径，与 `-f` 互斥。
   - `-l`：目标编程语言，默认为 `Python`。
   - `-t`：错误信息语言，默认为 `en-US`。
   - `-i`：代码缩进空格数，默认为 `4`。
   - `-o`：输出文件路径。
   - `-m`：使用的编译器模型，默认为 `ChatGLM`。
   - `-p`：是否展示已格式化后的AI提示词，默认为否。
   - `-w`：是否监听文件的变化，默认为否。

### 使用配置文件

创建配置文件（JSON），例如 `config.json`，内容如下：

```json
{
    "includes": [],
    "common": {}
}
```

其中，`includes` 是一个数组，每个元素是一个实现了如下接口的对象，`common` 也是。如果某个配置项在 `common` 中定义了，那么所有 `includes` 中的配置项都会继承这个配置项的值。

```ts
interface ConfigIncludes {
    input?: string; // 输入文件
    language?: string; // 目标语言
    output?: string; // 输出文件
    traceback?: string; // 错误信息语言
    indent?: number; // 缩进
    show_prompt?: boolean; // 是否显示已格式化后的提示词
    watch?: boolean; // 是否监视文件变化
    model?: string; // 模型
    common: ConfigIncludes; // 当前配置的通用配置
}
```

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

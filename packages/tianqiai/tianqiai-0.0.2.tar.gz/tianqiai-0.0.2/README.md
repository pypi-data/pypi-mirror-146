# tianqiai Python Library

The tianqiai Python library provides convenient access to the tianqiai API
from applications written in the Python language. It includes a
pre-defined set of classes for API resources that initialize
themselves dynamically from API responses which makes it compatible
with a wide range of versions of the tianqiai API.

## Documentation

See the [tianqiai API docs](https://wudao.aminer.cn/dev_doc_v2/zh-CN/document/get_started/developer_quickstart).

## Installation

You don't need this source code unless you want to modify the package. If you just
want to use the package, just run:

```sh
pip install --upgrade tianqiai
```

Install from source with:

```sh
python setup.py install
```

## Usage

The library needs to be configured with your account's secret key which is available on the [website](https://beta.tianqiai.com/account/api-keys). Either set it as the `tianqiai_API_KEY` environment variable before using the library:

```bash
export TIANQIAI_API_KEY='sk-...'
```

Or set `tianqiai.api_key` to its value:

```python
import tianqiai
tianqiai.api_key = "sk-..."

# print the first engine's id
print(engines.data[0].id)

# create a completion
completion = tianqiai.Completion.create(model="glm", prompt="Hello world")

# print the completion
print(completion.choices[0].text)
```

### Command-line interface

This library additionally provides an tianqiai command-line utility which makes it easy to interact with the API from your terminal. Run tianqiai api completions.create -h for usage.
```
tianqiai api completions.create -p "问题：冬天，中国哪座城市最适合避寒？问题描述：能推荐一些国内适合冬天避寒的城市吗？回答用户：旅游爱好者 回答：" -ip "冬天，中国哪座城市最适合避寒？" -l "zh-CN" -m "glm" -M 200
```

## Example code

Coming soon

## Requirements

- Python 3.7.1+

In general we want to support the versions of Python that our
customers are using, so if you run into issues with any version
issues, please let us know at support@tianqiai.com.

## Credit

This library is forked from the [Stripe Python Library](https://github.com/stripe/stripe-python).

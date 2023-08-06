<p align="center">
  <img src="https://img.shields.io/pypi/v/waifus?style=flat-square" </a>
  <img src="https://img.shields.io/pypi/l/waifus?style=flat-square" </a>
  <img src="https://img.shields.io/pypi/dm/waifus?style=flat-square" </a>
</p>

---

### Code example

Example of how you can use [waifus](https://pypi.org/project/waifus/) <br>
- possible options [`only_link`, `custom_path`, `displaying`, `count`, `meow`, `nsfw`, `sleeping_time`, `deleting`]

### installing it

```shell
python -m pip install waifus
```

### executing it (for example)

```python
import waifus

waifus.module(count = 5, sleeping_time = 1)
```

### getting only a link out [`https://api.waifu.pics/sfw/neko`, `https://api.waifu.pics/nsfw/neko`, `https://api.waifu.pics/sfw/waifu`, `https://api.waifu.pics/nsfw/waifu`]

```python
import waifus

waifus.getting_url("https://api.waifu.pics/sfw/waifu")
```
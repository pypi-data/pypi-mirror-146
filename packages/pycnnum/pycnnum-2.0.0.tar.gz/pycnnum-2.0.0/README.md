Copied from my git repo https://github.com/zcold/pycnnum.

## Usage

This package exposes two methods for conversion between Chinese string and `int`/`float` number.

### Chinese string to number `cn2num`

```python
>>> from pycnnum import cn2num
>>> cn2num("一百八")
180
>>> cn2num("十五")
15
>>> cn2num("负十五")
-15
>>> cn2num("一百八十")
180
>>> cn2num("一百八点五六七")
180.567
>>> cn2num("两千万一百八十")
20000180
```

### Number to Chinese string `num2cn`

```python
from pycnnum import num2cn
>>> num2cn('023232.005184132423423423300', numbering_type="high", alt_two=True, capitalize=False, traditional=True)
'兩萬三仟兩佰三拾二點零零五一八四一三二四二三四二三四二三三'
>>> num2cn('023232.005184132423423423300', numbering_type="high", alt_two=False, capitalize=False, traditional=True)
'二萬三仟二佰三拾二點零零五一八四一三二四二三四二三四二三三'
>>> num2cn(111180000)
'一亿一千一百一十八万'
>>> num2cn(1821010)
'一百八十二万一千零一十'
>>> num2cn(182.1)
'一百八十二点一'
>>> num2cn('3.4')
'三点四'
>>> num2cn(16)
'十六'
>>> num2cn(10600)
'一万零六百'
>>> num2cn(110)
'一百一'
>>> num2cn(1600)
'一千六'
```

## Development

1. Create a virtual env `venv`
2. Activate the virtual env
3. Run `python -m pip install .[dev]`

- `VSCode` task for creating API document is in `.vscode/tasks.json`.
- `VSCode` debugger configuration for fixing issues with `pytest-cov` is in `.vscode/launch.json`.

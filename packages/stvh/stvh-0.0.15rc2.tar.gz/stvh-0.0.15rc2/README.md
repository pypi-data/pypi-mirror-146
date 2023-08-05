# stvh

A collection of useful tools.

## Build status

<table>
  <tr>
    <th>build</th>
    <th>status</th>
  </tr>
  <tr>
    <td>misc</td>
    <td>
      <a href="https://builds.sr.ht/~stvhuang/stvh.py/commits/main/misc.yml">
        <img src="https://builds.sr.ht/~stvhuang/stvh.py/commits/main/misc.yml.svg"></td>
      </a>
    </td>
  </tr>
  <tr>
    <td>sklearn</td>
    <td>
      <a href="https://builds.sr.ht/~stvhuang/stvh.py/commits/main/sklearn.yml">
        <img src="https://builds.sr.ht/~stvhuang/stvh.py/commits/main/sklearn.yml.svg"></td>
      </a>
  </tr>
  <tr>
    <td>torch</td>
    <td>
      <a href="https://builds.sr.ht/~stvhuang/stvh.py/commits/main/torch.yml">
        <img src="https://builds.sr.ht/~stvhuang/stvh.py/commits/main/torch.yml.svg">
      </a>
    </td>
  </tr>
</table>

## Package building and uploading

Build package, requiring [build](https://pypa-build.readthedocs.io/en/stable/):

```sh
python -m build
```

Upload package to PyPI, requiring [Twine](https://twine.readthedocs.io/en/stable/):

```py
twine upload dist/*
```

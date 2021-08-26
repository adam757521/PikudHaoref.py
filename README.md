<h1 align="center">PikudHaoref.py</h1>

<p align="center">
  <a href="https://www.codefactor.io/repository/github/adam757521/pikudhaoref.py"><img src="https://img.shields.io/codefactor/grade/github/adam757521/PikudHaoref.py?style=flat-square" /></a>
  <a href="https://pepy.tech/project/PikudHaoref.py"><img src="https://img.shields.io/pypi/dm/PikudHaoref.py?color=green&style=flat-square" /></a>
  <a href="https://pypi.org/project/PikudHaoref.py/"><img src="https://img.shields.io/pypi/v/PikudHaoref.py?style=flat-square" /></a>
  <a href=""><img src="https://img.shields.io/pypi/l/PikudHaoref.py?style=flat-square" /></a>
  <br></br>
  <a href="#">Documentation</a>
</p>

<p align="center">
   An API wrapper for Pikud Haoref's unofficial rocket API written in python.
</p>

Features
-------------

- Very easy to use and user friendly.
- Object Oriented.
- Detect sirens in real time.
(MORE COMING SOON)

Installation
--------------

Installing discordSuperUtils is very easy.

```sh
python -m pip install pikudhaoref.py
```

Examples
--------------

### Siren detector example ###

```py
import pikudhaoref


client = pikudhaoref.Client(update_interval=2)
print(client.history())  # client.history returns sirens that happened in the last 24 hours.
print(client.get_current_sirens())  # Returns the current sirens


@client.event()
def on_siren(sirens):
    print(f"Siren alert! started sirens: {sirens}")


@client.event()
def on_siren_end(sirens):
    print(f"Sirens {sirens} have ended.")
```

Known Issues
--------------

- Currently, None!

**Incase you do find bugs, please create an issue or a PR.**

Support
--------------

- **[Documentation](#)**

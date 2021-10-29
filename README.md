<h1 align="center">PikudHaoref.py</h1>

<p align="center">
  <a href="https://www.codefactor.io/repository/github/adam757521/pikudhaoref.py"><img src="https://img.shields.io/codefactor/grade/github/adam757521/PikudHaoref.py?style=flat-square" /></a>
  <a href="https://pepy.tech/project/PikudHaoref.py"><img src="https://img.shields.io/pypi/dm/PikudHaoref.py?color=green&style=flat-square" /></a>
  <a href="https://pypi.org/project/PikudHaoref.py/"><img src="https://img.shields.io/pypi/v/PikudHaoref.py?style=flat-square" /></a>
  <a href=""><img src="https://img.shields.io/pypi/l/PikudHaoref.py?style=flat-square" /></a>
    <br/>
  <a href="#">Documentation</a>
</p>

<p align="center">
   An unofficial API wrapper for Pikud Haoref's rocket API written in python.
    <br/>
  <b>The documentation is not done yet.</b>
</p>

Credits
-------------
- [HoshenKadosh](https://github.com/HoshenKadosh/) for pikudhaoref API help.

Features
-------------

- Very easy to use and user-friendly.
- Object Oriented.
- Detect sirens in real time.
(MORE COMING SOON)

**The pikudhaoref API is only accessible from Israel.**

Installation
--------------

Installing pikudhaoref.py is very easy.

```sh
python -m pip install pikudhaoref.py
```

Examples
--------------

### Siren detector example ###

```py
from datetime import datetime

import pikudhaoref


client = pikudhaoref.SyncClient(update_interval=2)

history_range = client.get_history(
    date_range=pikudhaoref.Range(datetime(year=2014, month=7, day=24), datetime.now())
)
history_month = client.get_history(mode=pikudhaoref.HistoryMode.LAST_MONTH)

print(history_month)
print(history_range)
# The get_history method does not create a city object as it might take a long time.
# In case you need the city information, you can use the get_city method.

print(client.current_sirens)
# The current_sirens property returns the list of current sirens, and gets the city automatically.


@client.event()
def on_siren(sirens):
    print(f"Siren alert! started sirens: {sirens}")


@client.event()
def on_siren_end(sirens):
    print(f"Sirens {sirens} have ended.")


while True:
    pass  # To make sure the script doesnt stop
```

TODO
--------------

- None

Known Issues
--------------

- Currently, None!

**Incase you do find bugs, please create an issue or a PR.**

Support
--------------

- **[Documentation](#)**

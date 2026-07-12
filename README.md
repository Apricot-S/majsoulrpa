# MajsoulRPA

A Robotic Process Automation (RPA) framework for Mahjong Soul (雀魂)

This project is a fork of **[Cryolite's majsoul-rpa](https://github.com/Cryolite/majsoul-rpa)**, but has been completely redesigned based on the proactor pattern.
While some internal ideas and major class names were borrowed, the architecture and codebase are entirely new.

> [!NOTE]
> This framework is intended to enable the participation of bots in friendly matches and tournaments where bot participation is agreed upon by all players involved.
>
> This framework does not support the functionality to enter bots into open matches (including, but not limited to, ranked matches and special rooms within tournament matches). Furthermore, there is no intention to introduce such functionality in the future.

> [!WARNING]
> Users of this framework accept full responsibility for its use. The authors shall bear no liability whatsoever for any damages resulting from utilization of this framework, including, but not limited to, account suspension or legal repercussions.

> 🚧 **Work in Progress**
>
> MajsoulRPA is currently in active development and not usable yet.

## Key differences from the original project

- ✅ Requires **Python 3.12** or later
- 🗑️ Removed dependencies on **Docker** and **Redis**
- 🖥️ Supports moving browser window position after launch
- 🖱️ Mouse can be used freely even while RPA is running
- 📐 Supports browser viewport sizes other than **1920 × 1080**
- 🀄 Supports **three-player mahjong**

## Implementation concept diagram

![implementation-concept-diagram](docs/implementation-concept-diagram.png)

## Installation

### Remote browser host (the machine that will run the browser)

```sh
majsoulrpa$ pip install .[browser]
# Install Chromium browser binaries on the browser host
majsoulrpa$ playwright install chromium --with-deps
```

### RPA client host (the machine running the RPA client which performs automation)

```sh
majsoulrpa$ pip install .[client]
```

### Combined setup (browser and client on the same host)

```sh
majsoulrpa$ pip install .[browser,client]
```

### Optional: fetch verification emails from AWS S3

```sh
majsoulrpa$ pip install .[email-s3]
```

Make AWS credentials available using one of the following methods:

- Save them in `~/.aws/credentials`
- Set them via environment variables:

    ```sh
    export AWS_ACCESS_KEY_ID=...
    export AWS_SECRET_ACCESS_KEY=...
    export AWS_REGION=...
    ```

## Usage

### 🌐 Remote browser

You can launch the remote browser directly from the command line:

```sh
majsoulrpa-browser
```

It can also be invoked from Python code:

```python
from majsoulrpa.browser.server.runtime import run_browser_server

config = ...
option = ...
run_browser_server(config, option)
```

See [examples/](examples/) for detailed configurations and scenarios.

### 🤖 RPA client

The RPA client is used from Python code. A typical flow looks like this:

```python
import asyncio
from typing import Any
from majsoulrpa.presentation.home import HomePresentation
from majsoulrpa.presentation.login import LoginPresentation
from majsoulrpa.rpa_client import RPAClient

rpa = RPAClient()

@rpa.on(LoginPresentation)
async def on_login(p: LoginPresentation, data: Any) -> Any:
    ...
    return ...

@rpa.on(HomePresentation)
async def on_home(p: HomePresentation, data: Any) -> Any:
    ...
    return ...

config = ...
data = ...  # You can set any value here; it will be carried through the client
asyncio.run(rpa.run(config, data))
```

- Register callbacks with `@rpa.on(Presentation)`
- Only the registered Presentations are subject to detection; unregistered ones are ignored
- `data` can hold arbitrary values and is passed along within the client
- Call `rpa.run(...)` to start execution

See [examples/](examples/) for complete implementations.

> [!IMPORTANT]
> The email address you use must be linked to your Yostar ID.

## License

Licensed under the [MIT license](LICENSE).

# MajsoulRPA

A Robotic Process Automation (RPA) framework for Mahjong Soul (雀魂)

This is fork of **[Cryolite's majsoul-rpa](https://github.com/Cryolite/majsoul-rpa)** with following changes.

- Requires Python 3.12 or later
- Removed dependencies on Docker and Redis
- Supports moving browser position after launch
- Mouse can be used freely even while RPA is running
- Supports browser viewport sizes other than 1920 x 1080
- Supports three-player mahjong

> [!NOTE]
> This framework is intended to enable the participation of bots in friendly matches and tournaments where bot participation is explicitly allowed.
>
> This framework does not support the functionality to enter bots into open matches (including, but not limited to, ranked matches and special rooms within tournament matches). Furthermore, there is no intention to introduce such functionality in the future.

> [!WARNING]
> Users of this framework accept full responsibility for its use. The authors shall bear no liability whatsoever for any damages resulting from utilization of this framework, including, but not limited to, account suspension or legal repercussions.

## Implementation concept diagram

TODO

## Installation

```sh
majsoulrpa$ pip install .
majsoulrpa$ playwright install --with-deps chromium
```

## License

Licensed under the [MIT license](LICENSE).

# MajsoulRPA

MajsoulRPA v3 is a redesign branch for a Mahjong Soul (雀魂) RPA framework.

This branch intentionally starts from a minimal package skeleton. The public API
will be rebuilt from the v3 design documents under `docs/agents/`.

## Current Status

Implementation is in the initial skeleton phase. The package can be imported,
but browser automation, screen detection, and WebSocket capture are not
implemented yet.

```python
import majsoulrpa

print(majsoulrpa.__version__)
```

## Safety Scope

This project is intended for agreed friendly matches and tournaments only. It
does not support entering bots into open matches, ranked matches, or any match
where bot participation has not been agreed by all involved players.

## License

Licensed under the [MIT license](LICENSE).

# Examples

## fetch_log.py

Repeatedly prompts for a game record ID, navigates to the corresponding Mahjong Soul game record URL, and saves the response from `.lq.Lobby.fetchGameRecord` to `game-records/<game-record-id>.bin`.

Enter a blank line to stop fetching records.

First, start the client example:

```console
python examples/fetch_log.py
```

After the client begins waiting for the browser host, start the browser host in another terminal:

```console
majsoulrpa-browser
```

Starting them in this order reduces the chance of missing the initial WebSocket communication, even when `LoginScreen` is skipped because saved cookies are available.

Enter your email address and verification code if required, then enter a game record ID at the prompt.

The saved data is not decoded JSON. It consists of the raw response bytes obtained from the captured request/response event.

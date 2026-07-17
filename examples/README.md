# Examples

A configuration file template is available at `examples/config.example.toml`. Create `examples/config.toml` from it as needed and load it from both the browser host and the client.

Local configuration and generated game records must not be committed. `examples/.gitignore` excludes `examples/config.toml` and `examples/game-records/`.

## yostar_email_s3.py

Requests a Yostar verification email during login, waits for AWS SES to receive and store it in AWS S3, extracts its verification code, and uses it to log in. After reaching the Home screen, the example waits for two seconds and stops both the browser host and the RPA client.

Install the S3 optional dependency:

```console
pip install ".[s3]"
```

Create `examples/config.toml` based on `examples/config.example.toml`, then configure the `[yostar_email]` and `[yostar_email.s3]` sections.

AWS credentials are resolved through boto3's normal credential provider chain. Do not place AWS access keys in `config.toml`.

First, start the RPA client:

```console
python examples/yostar_email_s3.py
```

After the client begins waiting, start the browser host in another terminal with the same configuration:

```console
majsoulrpa-browser --config examples/config.toml
```

## fetch_id.py

Opens the spectating screen from Home, switches through the Gold, Jade, and Throne Room
four-player East and South lists, and prints the unique game record IDs from
`.lq.Lobby.fetchGameLiveList` in observation order.

This example uses only fixed `Region` values for the spectating screen.
It does not use screenshot templates or heartbeat monitoring.

First, start the client example:

```console
python examples/fetch_id.py
```

After the client begins waiting for the browser host, start the browser host in another terminal:

```console
majsoulrpa-browser
```

Enter your email address and verification code if required.

The collected IDs are printed one per line.

## fetch_log.py

Repeatedly prompts for a game record ID, navigates to the corresponding Mahjong Soul game record URL, and saves the response from `.lq.Lobby.fetchGameRecord` to `examples/game-records/<game-record-id>.bin`.

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

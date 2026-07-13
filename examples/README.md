# Examples

A configuration file template is available at `config.example.toml`. Copy it as needed and load it from both the browser host and the client.

Local `config.toml` files and the `game-records` output directory are ignored by Git.

## yostar_email_s3.py

Retrieves a Yostar verification email stored in Amazon S3, extracts its verification code, and uses it to log in. After reaching the Home screen, the example waits for two seconds and stops both the browser host and the RPA client.

Install the S3 optional dependency:

```console
pip install "majsoulrpa[s3]"
```

Copy the configuration template to `config.toml` and configure the `[yostar_email]` and `[yostar_email.s3]` sections. Use placeholder-free local values only in `config.toml`; do not commit email addresses or AWS settings.

```console
copy examples\config.example.toml config.toml
```

AWS credentials are resolved through boto3's normal credential provider chain. Do not place AWS access keys in `config.toml`.

First, start the RPA client:

```console
python examples/yostar_email_s3.py
```

After the client begins waiting, start the browser host in another terminal with the same configuration:

```console
majsoulrpa-browser --config config.toml
```

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

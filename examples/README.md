# Examples

Run these examples from the repository root. A configuration template is available at `examples/config.example.toml`; copy it to `examples/config.toml` when an example requires configuration.

Do not commit local configuration or generated data. The examples' `.gitignore` excludes:

- `examples/config.toml`
- `examples/game-ids/`
- `examples/game-records/`

For every example, start the RPA client before the browser host. This reduces the chance of missing initial WebSocket messages when saved cookies allow Mahjong Soul to skip `LoginScreen`.

## random_action.py

### Purpose

Creates a one-game friendly room, fills every available seat with an AI player, and, after confirmation, plays the match by randomly selecting from the legal operation candidates reported by `MatchScreen`. After the match, the example stops the browser host and RPA client.

### Preparation

No additional configuration is required.

### Run

1. Start the RPA client:

   ```console
   python examples/random_action.py
   ```

2. After the client begins waiting, start the browser host in another terminal:

   ```console
   majsoulrpa-browser
   ```

### Runtime input and output

If `LoginScreen` appears, enter the email address and verification code when prompted.

After the room is filled with AI players, enter `y` at `Start match? [y/N]:` to start the match. Any other input leaves the room without starting a match.

The example does not create an output file.

## yostar_email_s3.py

### Purpose

Logs in using a Yostar verification email delivered by AWS SES to S3. The example extracts the verification code, completes login, waits two seconds after reaching Home, and stops the browser host and RPA client.

### Preparation

Install the S3 optional dependency:

```console
pip install ".[s3]"
```

Copy `examples/config.example.toml` to `examples/config.toml`, then configure the `[yostar_email]` and `[yostar_email.s3]` sections. AWS credentials are resolved through boto3's normal credential provider chain. Do not put AWS access keys in `config.toml`.

### Run

1. Start the RPA client:

   ```console
   python examples/yostar_email_s3.py
   ```

2. After the client begins waiting, start the browser host in another terminal with the same configuration:

   ```console
   majsoulrpa-browser --config examples/config.toml
   ```

### Runtime input and output

No terminal input is required. The verification code is obtained from S3. This example does not create an output file.

## fetch_id.py

### Purpose

Opens the spectating screen from Home and visits the Gold, Jade, and Throne Room lists for four-player and three-player East and South games. It obtains game record IDs from `.lq.Lobby.fetchGameLiveList`.

### Preparation

No additional configuration is required. Generated ID files are written under the ignored `examples/game-ids/` directory.

### Run

1. Start the RPA client:

   ```console
   python examples/fetch_id.py
   ```

2. After the client begins waiting, start the browser host in another terminal:

   ```console
   majsoulrpa-browser
   ```

### Runtime input and output

If `LoginScreen` appears, enter the email address and verification code when prompted.

After one fetch completes, the example displays `Fetch again? [y/N]:`. Enter `y` to fetch again. Press Enter or enter `N` to finish.

IDs are printed to the terminal and appended as UTF-8 text, one ID per line, to files named:

```text
examples/game-ids/<4|3>-<east|south>-<gold|jade|throne>.txt
```

## fetch_log.py

### Purpose

Prompts for game record IDs, opens each corresponding Mahjong Soul game record URL, and captures the `.lq.Lobby.fetchGameRecord` response.

### Preparation

No additional configuration is required. Generated records are written under the ignored `examples/game-records/` directory.

### Run

1. Start the RPA client:

   ```console
   python examples/fetch_log.py
   ```

2. After the client begins waiting, start the browser host in another terminal:

   ```console
   majsoulrpa-browser
   ```

### Runtime input and output

If `LoginScreen` appears, enter the email address and verification code when prompted. Then enter a game record ID at each `Log ID` prompt. Enter a blank line to finish.

Each response is saved to:

```text
examples/game-records/<game-record-id>.bin
```

The `.bin` file contains raw response bytes from the captured request/response event; it is not decoded JSON.

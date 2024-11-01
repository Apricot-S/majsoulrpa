from majsoulrpa.common import Player


def test_player() -> None:
    account_id = 0
    name = ""
    player = Player(account_id, name)

    assert player.account_id == account_id
    assert player.name == name

    account_id = 123456789
    name = "あいうえおかき"
    player = Player(account_id, name)

    assert player.account_id == account_id
    assert player.name == name

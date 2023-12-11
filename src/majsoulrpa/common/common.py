import datetime
from typing import TypeAlias

TimeoutType: TypeAlias = int | float | datetime.timedelta


def to_timedelta(seconds: TimeoutType) -> datetime.timedelta:
    if isinstance(seconds, datetime.timedelta):
        return seconds
    if isinstance(seconds, int | float):
        return datetime.timedelta(seconds=seconds)
    raise TypeError


def timeout_to_deadline(timeout: TimeoutType) -> datetime.datetime:
    return datetime.datetime.now(datetime.UTC) + to_timedelta(timeout)


class Player:

    def __init__(self, account_id: int, name: str) -> None:
        self._account_id = account_id
        self._name = name

    @property
    def account_id(self) -> int:
        return self._account_id

    @property
    def name(self) -> str:
        return self._name


_LEVEL_ID_MAP = {
    10101: "初心1",
    10102: "初心2",
    10103: "初心3",
    10201: "雀士1",
    10202: "雀士2",
    10203: "雀士3",
    10301: "雀傑1",
    10302: "雀傑2",
    10303: "雀傑3",
    10401: "雀豪1",
    10402: "雀豪2",
    10403: "雀豪3",
    10501: "雀聖1",
    10502: "雀聖2",
    10503: "雀聖3",
    #10601: "魂天", before Soul Points introduction
    10701: "魂天Lv1",
    10702: "魂天Lv2",
    10703: "魂天Lv3",
    10704: "魂天Lv4",
    10705: "魂天Lv5",
    10706: "魂天Lv6",
    10707: "魂天Lv7",
    10708: "魂天Lv8",
    10709: "魂天Lv9",
    10710: "魂天Lv10",
    10711: "魂天Lv11",
    10712: "魂天Lv12",
    10713: "魂天Lv13",
    10714: "魂天Lv14",
    10715: "魂天Lv15",
    10716: "魂天Lv16",
    10717: "魂天Lv17",
    10718: "魂天Lv18",
    10719: "魂天Lv19",
    10720: "魂天Lv20",
    20101: "初心1",
    20102: "初心2",
    20103: "初心3",
    20201: "雀士1",
    20202: "雀士2",
    20203: "雀士3",
    20301: "雀傑1",
    20302: "雀傑2",
    20303: "雀傑3",
    20401: "雀豪1",
    20402: "雀豪2",
    20403: "雀豪3",
    20501: "雀聖1",
    20502: "雀聖2",
    20503: "雀聖3",
    #20601: "魂天", before Soul Points introduction
    20701: "魂天Lv1",
    20702: "魂天Lv2",
    20703: "魂天Lv3",
    20704: "魂天Lv4",
    20705: "魂天Lv5",
    20706: "魂天Lv6",
    20707: "魂天Lv7",
    20708: "魂天Lv8",
    20709: "魂天Lv9",
    20710: "魂天Lv10",
    20711: "魂天Lv11",
    20712: "魂天Lv12",
    20713: "魂天Lv13",
    20714: "魂天Lv14",
    20715: "魂天Lv15",
    20716: "魂天Lv16",
    20717: "魂天Lv17",
    20718: "魂天Lv18",
    20719: "魂天Lv19",
    20720: "魂天Lv20",
}


def id_to_level(level_id: int) -> str:
    return _LEVEL_ID_MAP[level_id]


_CHARACTER_ID_MAP = {
    200001: "一姫",
    200002: "二階堂美樹",
    200003: "藤田佳奈",
    200004: "三上千織",
    200005: "相原舞",
    200006: "撫子",
    200007: "八木唯",
    200008: "九条璃雨",
    200009: "ジニア",
    200010: "カーヴィ",
    200011: "四宮夏生",
    200012: "ワン次郎",
    200013: "一ノ瀬空",
    200014: "明智英樹",
    200015: "軽庫娘",
    200016: "サラ",
    200017: "二之宮花",
    200018: "白石奈々",
    200019: "小鳥遊雛田",
    200020: "五十嵐陽菜",
    200021: "涼宮杏樹",
    200022: "ジョセフ",
    200023: "斎藤治",
    200024: "北見紗和子",
    200025: "エイン",
    200026: "雛桃",
    200027: "月見山",
    200028: "藤本キララ",
    200029: "かぐや姫",
    200030: "如月蓮",
    200031: "石原碓海",
    200032: "エリサ",
    200033: "寺崎千穂理",
    200034: "宮永咲",
    200035: "原村和",
    200036: "天江衣",
    200037: "宮永照",
    200038: "福姫",
    200039: "七夕",
    200040: "蛇喰夢子",
    200041: "早乙女芽亜里",
    200042: "生志摩妄",
    200043: "桃喰綺羅莉",
    200044: "七海礼奈",
    200045: "A-37",
    200046: "姫川響",
    200047: "ライアン",
    200048: "森川綾子",
    200049: "滝川夏彦",
    200050: "赤木しげる",
    200051: "鷲巣巌",
    200052: "西園寺一羽",
    200053: "小野寺七羽",
    200054: "サミール",
    200055: "四宮かぐや",
    200056: "白銀御行",
    200057: "早坂愛",
    200058: "白銀圭",
    200059: "ゆず",
    200060: "ゼクス",
}


def id_to_character(character_id: int) -> str:
    return _CHARACTER_ID_MAP[character_id]

from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GamePlayerState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    NULL: _ClassVar[GamePlayerState]
    AUTH: _ClassVar[GamePlayerState]
    SYNCING: _ClassVar[GamePlayerState]
    READY: _ClassVar[GamePlayerState]
NULL: GamePlayerState
AUTH: GamePlayerState
SYNCING: GamePlayerState
READY: GamePlayerState

class NotifyCaptcha(_message.Message):
    __slots__ = ["check_id", "start_time", "random_str", "type"]
    CHECK_ID_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    RANDOM_STR_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    check_id: int
    start_time: int
    random_str: str
    type: int
    def __init__(self, check_id: _Optional[int] = ..., start_time: _Optional[int] = ..., random_str: _Optional[str] = ..., type: _Optional[int] = ...) -> None: ...

class NotifyRoomGameStart(_message.Message):
    __slots__ = ["game_url", "connect_token", "game_uuid", "location"]
    GAME_URL_FIELD_NUMBER: _ClassVar[int]
    CONNECT_TOKEN_FIELD_NUMBER: _ClassVar[int]
    GAME_UUID_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    game_url: str
    connect_token: str
    game_uuid: str
    location: str
    def __init__(self, game_url: _Optional[str] = ..., connect_token: _Optional[str] = ..., game_uuid: _Optional[str] = ..., location: _Optional[str] = ...) -> None: ...

class NotifyMatchGameStart(_message.Message):
    __slots__ = ["game_url", "connect_token", "game_uuid", "match_mode_id", "location"]
    GAME_URL_FIELD_NUMBER: _ClassVar[int]
    CONNECT_TOKEN_FIELD_NUMBER: _ClassVar[int]
    GAME_UUID_FIELD_NUMBER: _ClassVar[int]
    MATCH_MODE_ID_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    game_url: str
    connect_token: str
    game_uuid: str
    match_mode_id: int
    location: str
    def __init__(self, game_url: _Optional[str] = ..., connect_token: _Optional[str] = ..., game_uuid: _Optional[str] = ..., match_mode_id: _Optional[int] = ..., location: _Optional[str] = ...) -> None: ...

class NotifyRoomPlayerReady(_message.Message):
    __slots__ = ["account_id", "ready", "account_list", "seq"]
    class AccountReadyState(_message.Message):
        __slots__ = ["account_id", "ready"]
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        READY_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        ready: bool
        def __init__(self, account_id: _Optional[int] = ..., ready: bool = ...) -> None: ...
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    READY_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_LIST_FIELD_NUMBER: _ClassVar[int]
    SEQ_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    ready: bool
    account_list: NotifyRoomPlayerReady.AccountReadyState
    seq: int
    def __init__(self, account_id: _Optional[int] = ..., ready: bool = ..., account_list: _Optional[_Union[NotifyRoomPlayerReady.AccountReadyState, _Mapping]] = ..., seq: _Optional[int] = ...) -> None: ...

class NotifyRoomPlayerDressing(_message.Message):
    __slots__ = ["account_id", "dressing", "account_list", "seq"]
    class AccountDressingState(_message.Message):
        __slots__ = ["account_id", "dressing"]
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        DRESSING_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        dressing: bool
        def __init__(self, account_id: _Optional[int] = ..., dressing: bool = ...) -> None: ...
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    DRESSING_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_LIST_FIELD_NUMBER: _ClassVar[int]
    SEQ_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    dressing: bool
    account_list: NotifyRoomPlayerDressing.AccountDressingState
    seq: int
    def __init__(self, account_id: _Optional[int] = ..., dressing: bool = ..., account_list: _Optional[_Union[NotifyRoomPlayerDressing.AccountDressingState, _Mapping]] = ..., seq: _Optional[int] = ...) -> None: ...

class NotifyRoomPlayerUpdate(_message.Message):
    __slots__ = ["update_list", "remove_list", "owner_id", "robot_count", "player_list", "seq"]
    UPDATE_LIST_FIELD_NUMBER: _ClassVar[int]
    REMOVE_LIST_FIELD_NUMBER: _ClassVar[int]
    OWNER_ID_FIELD_NUMBER: _ClassVar[int]
    ROBOT_COUNT_FIELD_NUMBER: _ClassVar[int]
    PLAYER_LIST_FIELD_NUMBER: _ClassVar[int]
    SEQ_FIELD_NUMBER: _ClassVar[int]
    update_list: _containers.RepeatedCompositeFieldContainer[PlayerBaseView]
    remove_list: _containers.RepeatedScalarFieldContainer[int]
    owner_id: int
    robot_count: int
    player_list: _containers.RepeatedCompositeFieldContainer[PlayerBaseView]
    seq: int
    def __init__(self, update_list: _Optional[_Iterable[_Union[PlayerBaseView, _Mapping]]] = ..., remove_list: _Optional[_Iterable[int]] = ..., owner_id: _Optional[int] = ..., robot_count: _Optional[int] = ..., player_list: _Optional[_Iterable[_Union[PlayerBaseView, _Mapping]]] = ..., seq: _Optional[int] = ...) -> None: ...

class NotifyRoomKickOut(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class NotifyFriendStateChange(_message.Message):
    __slots__ = ["target_id", "active_state"]
    TARGET_ID_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_STATE_FIELD_NUMBER: _ClassVar[int]
    target_id: int
    active_state: AccountActiveState
    def __init__(self, target_id: _Optional[int] = ..., active_state: _Optional[_Union[AccountActiveState, _Mapping]] = ...) -> None: ...

class NotifyFriendViewChange(_message.Message):
    __slots__ = ["target_id", "base"]
    TARGET_ID_FIELD_NUMBER: _ClassVar[int]
    BASE_FIELD_NUMBER: _ClassVar[int]
    target_id: int
    base: PlayerBaseView
    def __init__(self, target_id: _Optional[int] = ..., base: _Optional[_Union[PlayerBaseView, _Mapping]] = ...) -> None: ...

class NotifyFriendChange(_message.Message):
    __slots__ = ["account_id", "type", "friend"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    FRIEND_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    type: int
    friend: Friend
    def __init__(self, account_id: _Optional[int] = ..., type: _Optional[int] = ..., friend: _Optional[_Union[Friend, _Mapping]] = ...) -> None: ...

class NotifyNewFriendApply(_message.Message):
    __slots__ = ["account_id", "apply_time", "removed_id"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    APPLY_TIME_FIELD_NUMBER: _ClassVar[int]
    REMOVED_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    apply_time: int
    removed_id: int
    def __init__(self, account_id: _Optional[int] = ..., apply_time: _Optional[int] = ..., removed_id: _Optional[int] = ...) -> None: ...

class NotifyClientMessage(_message.Message):
    __slots__ = ["sender", "type", "content"]
    SENDER_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    sender: PlayerBaseView
    type: int
    content: str
    def __init__(self, sender: _Optional[_Union[PlayerBaseView, _Mapping]] = ..., type: _Optional[int] = ..., content: _Optional[str] = ...) -> None: ...

class NotifyAccountUpdate(_message.Message):
    __slots__ = ["update"]
    UPDATE_FIELD_NUMBER: _ClassVar[int]
    update: AccountUpdate
    def __init__(self, update: _Optional[_Union[AccountUpdate, _Mapping]] = ...) -> None: ...

class NotifyAnotherLogin(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class NotifyAccountLogout(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class NotifyAnnouncementUpdate(_message.Message):
    __slots__ = ["update_list"]
    class AnnouncementUpdate(_message.Message):
        __slots__ = ["lang", "platform"]
        LANG_FIELD_NUMBER: _ClassVar[int]
        PLATFORM_FIELD_NUMBER: _ClassVar[int]
        lang: str
        platform: str
        def __init__(self, lang: _Optional[str] = ..., platform: _Optional[str] = ...) -> None: ...
    UPDATE_LIST_FIELD_NUMBER: _ClassVar[int]
    update_list: _containers.RepeatedCompositeFieldContainer[NotifyAnnouncementUpdate.AnnouncementUpdate]
    def __init__(self, update_list: _Optional[_Iterable[_Union[NotifyAnnouncementUpdate.AnnouncementUpdate, _Mapping]]] = ...) -> None: ...

class NotifyNewMail(_message.Message):
    __slots__ = ["mail"]
    MAIL_FIELD_NUMBER: _ClassVar[int]
    mail: Mail
    def __init__(self, mail: _Optional[_Union[Mail, _Mapping]] = ...) -> None: ...

class NotifyDeleteMail(_message.Message):
    __slots__ = ["mail_id_list"]
    MAIL_ID_LIST_FIELD_NUMBER: _ClassVar[int]
    mail_id_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, mail_id_list: _Optional[_Iterable[int]] = ...) -> None: ...

class NotifyReviveCoinUpdate(_message.Message):
    __slots__ = ["has_gained"]
    HAS_GAINED_FIELD_NUMBER: _ClassVar[int]
    has_gained: bool
    def __init__(self, has_gained: bool = ...) -> None: ...

class NotifyDailyTaskUpdate(_message.Message):
    __slots__ = ["progresses", "max_daily_task_count", "refresh_count"]
    PROGRESSES_FIELD_NUMBER: _ClassVar[int]
    MAX_DAILY_TASK_COUNT_FIELD_NUMBER: _ClassVar[int]
    REFRESH_COUNT_FIELD_NUMBER: _ClassVar[int]
    progresses: _containers.RepeatedCompositeFieldContainer[TaskProgress]
    max_daily_task_count: int
    refresh_count: int
    def __init__(self, progresses: _Optional[_Iterable[_Union[TaskProgress, _Mapping]]] = ..., max_daily_task_count: _Optional[int] = ..., refresh_count: _Optional[int] = ...) -> None: ...

class NotifyActivityTaskUpdate(_message.Message):
    __slots__ = ["progresses"]
    PROGRESSES_FIELD_NUMBER: _ClassVar[int]
    progresses: _containers.RepeatedCompositeFieldContainer[TaskProgress]
    def __init__(self, progresses: _Optional[_Iterable[_Union[TaskProgress, _Mapping]]] = ...) -> None: ...

class NotifyActivityPeriodTaskUpdate(_message.Message):
    __slots__ = ["progresses"]
    PROGRESSES_FIELD_NUMBER: _ClassVar[int]
    progresses: _containers.RepeatedCompositeFieldContainer[TaskProgress]
    def __init__(self, progresses: _Optional[_Iterable[_Union[TaskProgress, _Mapping]]] = ...) -> None: ...

class NotifyAccountRandomTaskUpdate(_message.Message):
    __slots__ = ["progresses"]
    PROGRESSES_FIELD_NUMBER: _ClassVar[int]
    progresses: _containers.RepeatedCompositeFieldContainer[TaskProgress]
    def __init__(self, progresses: _Optional[_Iterable[_Union[TaskProgress, _Mapping]]] = ...) -> None: ...

class NotifyActivitySegmentTaskUpdate(_message.Message):
    __slots__ = ["progresses"]
    PROGRESSES_FIELD_NUMBER: _ClassVar[int]
    progresses: _containers.RepeatedCompositeFieldContainer[SegmentTaskProgress]
    def __init__(self, progresses: _Optional[_Iterable[_Union[SegmentTaskProgress, _Mapping]]] = ...) -> None: ...

class NotifyActivityUpdate(_message.Message):
    __slots__ = ["list"]
    class FeedActivityData(_message.Message):
        __slots__ = ["activity_id", "feed_count", "friend_receive_data", "friend_send_data", "gift_inbox"]
        class CountWithTimeData(_message.Message):
            __slots__ = ["count", "last_update_time"]
            COUNT_FIELD_NUMBER: _ClassVar[int]
            LAST_UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
            count: int
            last_update_time: int
            def __init__(self, count: _Optional[int] = ..., last_update_time: _Optional[int] = ...) -> None: ...
        class GiftBoxData(_message.Message):
            __slots__ = ["id", "item_id", "count", "from_account_id", "time", "received"]
            ID_FIELD_NUMBER: _ClassVar[int]
            ITEM_ID_FIELD_NUMBER: _ClassVar[int]
            COUNT_FIELD_NUMBER: _ClassVar[int]
            FROM_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
            TIME_FIELD_NUMBER: _ClassVar[int]
            RECEIVED_FIELD_NUMBER: _ClassVar[int]
            id: int
            item_id: int
            count: int
            from_account_id: int
            time: int
            received: int
            def __init__(self, id: _Optional[int] = ..., item_id: _Optional[int] = ..., count: _Optional[int] = ..., from_account_id: _Optional[int] = ..., time: _Optional[int] = ..., received: _Optional[int] = ...) -> None: ...
        ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
        FEED_COUNT_FIELD_NUMBER: _ClassVar[int]
        FRIEND_RECEIVE_DATA_FIELD_NUMBER: _ClassVar[int]
        FRIEND_SEND_DATA_FIELD_NUMBER: _ClassVar[int]
        GIFT_INBOX_FIELD_NUMBER: _ClassVar[int]
        activity_id: int
        feed_count: int
        friend_receive_data: NotifyActivityUpdate.FeedActivityData.CountWithTimeData
        friend_send_data: NotifyActivityUpdate.FeedActivityData.CountWithTimeData
        gift_inbox: _containers.RepeatedCompositeFieldContainer[NotifyActivityUpdate.FeedActivityData.GiftBoxData]
        def __init__(self, activity_id: _Optional[int] = ..., feed_count: _Optional[int] = ..., friend_receive_data: _Optional[_Union[NotifyActivityUpdate.FeedActivityData.CountWithTimeData, _Mapping]] = ..., friend_send_data: _Optional[_Union[NotifyActivityUpdate.FeedActivityData.CountWithTimeData, _Mapping]] = ..., gift_inbox: _Optional[_Iterable[_Union[NotifyActivityUpdate.FeedActivityData.GiftBoxData, _Mapping]]] = ...) -> None: ...
    LIST_FIELD_NUMBER: _ClassVar[int]
    list: _containers.RepeatedCompositeFieldContainer[NotifyActivityUpdate.FeedActivityData]
    def __init__(self, list: _Optional[_Iterable[_Union[NotifyActivityUpdate.FeedActivityData, _Mapping]]] = ...) -> None: ...

class NotifyAccountChallengeTaskUpdate(_message.Message):
    __slots__ = ["progresses", "level", "refresh_count", "match_count", "ticket_id", "rewarded_season"]
    PROGRESSES_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    REFRESH_COUNT_FIELD_NUMBER: _ClassVar[int]
    MATCH_COUNT_FIELD_NUMBER: _ClassVar[int]
    TICKET_ID_FIELD_NUMBER: _ClassVar[int]
    REWARDED_SEASON_FIELD_NUMBER: _ClassVar[int]
    progresses: _containers.RepeatedCompositeFieldContainer[TaskProgress]
    level: int
    refresh_count: int
    match_count: int
    ticket_id: int
    rewarded_season: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, progresses: _Optional[_Iterable[_Union[TaskProgress, _Mapping]]] = ..., level: _Optional[int] = ..., refresh_count: _Optional[int] = ..., match_count: _Optional[int] = ..., ticket_id: _Optional[int] = ..., rewarded_season: _Optional[_Iterable[int]] = ...) -> None: ...

class NotifyNewComment(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class NotifyRollingNotice(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class NotifyMaintainNotice(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class NotifyGiftSendRefresh(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class NotifyShopUpdate(_message.Message):
    __slots__ = ["shop_info"]
    SHOP_INFO_FIELD_NUMBER: _ClassVar[int]
    shop_info: ShopInfo
    def __init__(self, shop_info: _Optional[_Union[ShopInfo, _Mapping]] = ...) -> None: ...

class NotifyIntervalUpdate(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class NotifyVipLevelChange(_message.Message):
    __slots__ = ["gift_limit", "friend_max_count", "zhp_free_refresh_limit", "zhp_cost_refresh_limit", "buddy_bonus", "record_collect_limit"]
    GIFT_LIMIT_FIELD_NUMBER: _ClassVar[int]
    FRIEND_MAX_COUNT_FIELD_NUMBER: _ClassVar[int]
    ZHP_FREE_REFRESH_LIMIT_FIELD_NUMBER: _ClassVar[int]
    ZHP_COST_REFRESH_LIMIT_FIELD_NUMBER: _ClassVar[int]
    BUDDY_BONUS_FIELD_NUMBER: _ClassVar[int]
    RECORD_COLLECT_LIMIT_FIELD_NUMBER: _ClassVar[int]
    gift_limit: int
    friend_max_count: int
    zhp_free_refresh_limit: int
    zhp_cost_refresh_limit: int
    buddy_bonus: float
    record_collect_limit: int
    def __init__(self, gift_limit: _Optional[int] = ..., friend_max_count: _Optional[int] = ..., zhp_free_refresh_limit: _Optional[int] = ..., zhp_cost_refresh_limit: _Optional[int] = ..., buddy_bonus: _Optional[float] = ..., record_collect_limit: _Optional[int] = ...) -> None: ...

class NotifyServerSetting(_message.Message):
    __slots__ = ["settings"]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    settings: ServerSettings
    def __init__(self, settings: _Optional[_Union[ServerSettings, _Mapping]] = ...) -> None: ...

class NotifyPayResult(_message.Message):
    __slots__ = ["pay_result", "order_id", "goods_id", "new_month_ticket", "resource_modify"]
    class ResourceModify(_message.Message):
        __slots__ = ["id", "count", "final"]
        ID_FIELD_NUMBER: _ClassVar[int]
        COUNT_FIELD_NUMBER: _ClassVar[int]
        FINAL_FIELD_NUMBER: _ClassVar[int]
        id: int
        count: int
        final: int
        def __init__(self, id: _Optional[int] = ..., count: _Optional[int] = ..., final: _Optional[int] = ...) -> None: ...
    PAY_RESULT_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    GOODS_ID_FIELD_NUMBER: _ClassVar[int]
    NEW_MONTH_TICKET_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_MODIFY_FIELD_NUMBER: _ClassVar[int]
    pay_result: int
    order_id: str
    goods_id: int
    new_month_ticket: int
    resource_modify: _containers.RepeatedCompositeFieldContainer[NotifyPayResult.ResourceModify]
    def __init__(self, pay_result: _Optional[int] = ..., order_id: _Optional[str] = ..., goods_id: _Optional[int] = ..., new_month_ticket: _Optional[int] = ..., resource_modify: _Optional[_Iterable[_Union[NotifyPayResult.ResourceModify, _Mapping]]] = ...) -> None: ...

class NotifyCustomContestAccountMsg(_message.Message):
    __slots__ = ["unique_id", "account_id", "sender", "content", "verified"]
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    SENDER_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    VERIFIED_FIELD_NUMBER: _ClassVar[int]
    unique_id: int
    account_id: int
    sender: str
    content: str
    verified: int
    def __init__(self, unique_id: _Optional[int] = ..., account_id: _Optional[int] = ..., sender: _Optional[str] = ..., content: _Optional[str] = ..., verified: _Optional[int] = ...) -> None: ...

class NotifyCustomContestSystemMsg(_message.Message):
    __slots__ = ["unique_id", "type", "uuid", "game_start", "game_end"]
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    GAME_START_FIELD_NUMBER: _ClassVar[int]
    GAME_END_FIELD_NUMBER: _ClassVar[int]
    unique_id: int
    type: int
    uuid: str
    game_start: CustomizedContestGameStart
    game_end: CustomizedContestGameEnd
    def __init__(self, unique_id: _Optional[int] = ..., type: _Optional[int] = ..., uuid: _Optional[str] = ..., game_start: _Optional[_Union[CustomizedContestGameStart, _Mapping]] = ..., game_end: _Optional[_Union[CustomizedContestGameEnd, _Mapping]] = ...) -> None: ...

class NotifyMatchTimeout(_message.Message):
    __slots__ = ["sid"]
    SID_FIELD_NUMBER: _ClassVar[int]
    sid: str
    def __init__(self, sid: _Optional[str] = ...) -> None: ...

class NotifyMatchFailed(_message.Message):
    __slots__ = ["sid"]
    SID_FIELD_NUMBER: _ClassVar[int]
    sid: str
    def __init__(self, sid: _Optional[str] = ...) -> None: ...

class NotifyCustomContestState(_message.Message):
    __slots__ = ["unique_id", "state"]
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    unique_id: int
    state: int
    def __init__(self, unique_id: _Optional[int] = ..., state: _Optional[int] = ...) -> None: ...

class NotifyActivityChange(_message.Message):
    __slots__ = ["new_activities", "end_activities"]
    NEW_ACTIVITIES_FIELD_NUMBER: _ClassVar[int]
    END_ACTIVITIES_FIELD_NUMBER: _ClassVar[int]
    new_activities: _containers.RepeatedCompositeFieldContainer[Activity]
    end_activities: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, new_activities: _Optional[_Iterable[_Union[Activity, _Mapping]]] = ..., end_activities: _Optional[_Iterable[int]] = ...) -> None: ...

class NotifyAFKResult(_message.Message):
    __slots__ = ["type", "ban_end_time", "game_uuid"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    BAN_END_TIME_FIELD_NUMBER: _ClassVar[int]
    GAME_UUID_FIELD_NUMBER: _ClassVar[int]
    type: int
    ban_end_time: int
    game_uuid: str
    def __init__(self, type: _Optional[int] = ..., ban_end_time: _Optional[int] = ..., game_uuid: _Optional[str] = ...) -> None: ...

class NotifyLoginQueueFinished(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class NotifyGameFinishRewardV2(_message.Message):
    __slots__ = ["mode_id", "level_change", "match_chest", "main_character", "character_gift"]
    class LevelChange(_message.Message):
        __slots__ = ["origin", "final", "type"]
        ORIGIN_FIELD_NUMBER: _ClassVar[int]
        FINAL_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        origin: AccountLevel
        final: AccountLevel
        type: int
        def __init__(self, origin: _Optional[_Union[AccountLevel, _Mapping]] = ..., final: _Optional[_Union[AccountLevel, _Mapping]] = ..., type: _Optional[int] = ...) -> None: ...
    class MatchChest(_message.Message):
        __slots__ = ["chest_id", "origin", "final", "is_graded", "rewards"]
        CHEST_ID_FIELD_NUMBER: _ClassVar[int]
        ORIGIN_FIELD_NUMBER: _ClassVar[int]
        FINAL_FIELD_NUMBER: _ClassVar[int]
        IS_GRADED_FIELD_NUMBER: _ClassVar[int]
        REWARDS_FIELD_NUMBER: _ClassVar[int]
        chest_id: int
        origin: int
        final: int
        is_graded: bool
        rewards: _containers.RepeatedCompositeFieldContainer[RewardSlot]
        def __init__(self, chest_id: _Optional[int] = ..., origin: _Optional[int] = ..., final: _Optional[int] = ..., is_graded: bool = ..., rewards: _Optional[_Iterable[_Union[RewardSlot, _Mapping]]] = ...) -> None: ...
    class MainCharacter(_message.Message):
        __slots__ = ["level", "exp", "add"]
        LEVEL_FIELD_NUMBER: _ClassVar[int]
        EXP_FIELD_NUMBER: _ClassVar[int]
        ADD_FIELD_NUMBER: _ClassVar[int]
        level: int
        exp: int
        add: int
        def __init__(self, level: _Optional[int] = ..., exp: _Optional[int] = ..., add: _Optional[int] = ...) -> None: ...
    class CharacterGift(_message.Message):
        __slots__ = ["origin", "final", "add", "is_graded"]
        ORIGIN_FIELD_NUMBER: _ClassVar[int]
        FINAL_FIELD_NUMBER: _ClassVar[int]
        ADD_FIELD_NUMBER: _ClassVar[int]
        IS_GRADED_FIELD_NUMBER: _ClassVar[int]
        origin: int
        final: int
        add: int
        is_graded: bool
        def __init__(self, origin: _Optional[int] = ..., final: _Optional[int] = ..., add: _Optional[int] = ..., is_graded: bool = ...) -> None: ...
    MODE_ID_FIELD_NUMBER: _ClassVar[int]
    LEVEL_CHANGE_FIELD_NUMBER: _ClassVar[int]
    MATCH_CHEST_FIELD_NUMBER: _ClassVar[int]
    MAIN_CHARACTER_FIELD_NUMBER: _ClassVar[int]
    CHARACTER_GIFT_FIELD_NUMBER: _ClassVar[int]
    mode_id: int
    level_change: NotifyGameFinishRewardV2.LevelChange
    match_chest: NotifyGameFinishRewardV2.MatchChest
    main_character: NotifyGameFinishRewardV2.MainCharacter
    character_gift: NotifyGameFinishRewardV2.CharacterGift
    def __init__(self, mode_id: _Optional[int] = ..., level_change: _Optional[_Union[NotifyGameFinishRewardV2.LevelChange, _Mapping]] = ..., match_chest: _Optional[_Union[NotifyGameFinishRewardV2.MatchChest, _Mapping]] = ..., main_character: _Optional[_Union[NotifyGameFinishRewardV2.MainCharacter, _Mapping]] = ..., character_gift: _Optional[_Union[NotifyGameFinishRewardV2.CharacterGift, _Mapping]] = ...) -> None: ...

class NotifyActivityRewardV2(_message.Message):
    __slots__ = ["activity_reward"]
    class ActivityReward(_message.Message):
        __slots__ = ["activity_id", "rewards"]
        ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
        REWARDS_FIELD_NUMBER: _ClassVar[int]
        activity_id: int
        rewards: _containers.RepeatedCompositeFieldContainer[RewardSlot]
        def __init__(self, activity_id: _Optional[int] = ..., rewards: _Optional[_Iterable[_Union[RewardSlot, _Mapping]]] = ...) -> None: ...
    ACTIVITY_REWARD_FIELD_NUMBER: _ClassVar[int]
    activity_reward: _containers.RepeatedCompositeFieldContainer[NotifyActivityRewardV2.ActivityReward]
    def __init__(self, activity_reward: _Optional[_Iterable[_Union[NotifyActivityRewardV2.ActivityReward, _Mapping]]] = ...) -> None: ...

class NotifyActivityPointV2(_message.Message):
    __slots__ = ["activity_points"]
    class ActivityPoint(_message.Message):
        __slots__ = ["activity_id", "point"]
        ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
        POINT_FIELD_NUMBER: _ClassVar[int]
        activity_id: int
        point: int
        def __init__(self, activity_id: _Optional[int] = ..., point: _Optional[int] = ...) -> None: ...
    ACTIVITY_POINTS_FIELD_NUMBER: _ClassVar[int]
    activity_points: _containers.RepeatedCompositeFieldContainer[NotifyActivityPointV2.ActivityPoint]
    def __init__(self, activity_points: _Optional[_Iterable[_Union[NotifyActivityPointV2.ActivityPoint, _Mapping]]] = ...) -> None: ...

class NotifyLeaderboardPointV2(_message.Message):
    __slots__ = ["leaderboard_points"]
    class LeaderboardPoint(_message.Message):
        __slots__ = ["leaderboard_id", "point"]
        LEADERBOARD_ID_FIELD_NUMBER: _ClassVar[int]
        POINT_FIELD_NUMBER: _ClassVar[int]
        leaderboard_id: int
        point: int
        def __init__(self, leaderboard_id: _Optional[int] = ..., point: _Optional[int] = ...) -> None: ...
    LEADERBOARD_POINTS_FIELD_NUMBER: _ClassVar[int]
    leaderboard_points: _containers.RepeatedCompositeFieldContainer[NotifyLeaderboardPointV2.LeaderboardPoint]
    def __init__(self, leaderboard_points: _Optional[_Iterable[_Union[NotifyLeaderboardPointV2.LeaderboardPoint, _Mapping]]] = ...) -> None: ...

class Error(_message.Message):
    __slots__ = ["code", "u32_params", "str_params", "json_param"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    U32_PARAMS_FIELD_NUMBER: _ClassVar[int]
    STR_PARAMS_FIELD_NUMBER: _ClassVar[int]
    JSON_PARAM_FIELD_NUMBER: _ClassVar[int]
    code: int
    u32_params: _containers.RepeatedScalarFieldContainer[int]
    str_params: _containers.RepeatedScalarFieldContainer[str]
    json_param: str
    def __init__(self, code: _Optional[int] = ..., u32_params: _Optional[_Iterable[int]] = ..., str_params: _Optional[_Iterable[str]] = ..., json_param: _Optional[str] = ...) -> None: ...

class Wrapper(_message.Message):
    __slots__ = ["name", "data"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    name: str
    data: bytes
    def __init__(self, name: _Optional[str] = ..., data: _Optional[bytes] = ...) -> None: ...

class NetworkEndpoint(_message.Message):
    __slots__ = ["family", "address", "port"]
    FAMILY_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    family: str
    address: str
    port: int
    def __init__(self, family: _Optional[str] = ..., address: _Optional[str] = ..., port: _Optional[int] = ...) -> None: ...

class ReqCommon(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ResCommon(_message.Message):
    __slots__ = ["error"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    error: Error
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class ResAccountUpdate(_message.Message):
    __slots__ = ["error", "update"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    UPDATE_FIELD_NUMBER: _ClassVar[int]
    error: Error
    update: AccountUpdate
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., update: _Optional[_Union[AccountUpdate, _Mapping]] = ...) -> None: ...

class AntiAddiction(_message.Message):
    __slots__ = ["online_duration"]
    ONLINE_DURATION_FIELD_NUMBER: _ClassVar[int]
    online_duration: int
    def __init__(self, online_duration: _Optional[int] = ...) -> None: ...

class AccountMahjongStatistic(_message.Message):
    __slots__ = ["final_position_counts", "recent_round", "recent_hu", "highest_hu", "recent_20_hu_summary", "recent_10_hu_summary", "recent_10_game_result"]
    class RoundSummary(_message.Message):
        __slots__ = ["total_count", "rong_count", "zimo_count", "fangchong_count"]
        TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
        RONG_COUNT_FIELD_NUMBER: _ClassVar[int]
        ZIMO_COUNT_FIELD_NUMBER: _ClassVar[int]
        FANGCHONG_COUNT_FIELD_NUMBER: _ClassVar[int]
        total_count: int
        rong_count: int
        zimo_count: int
        fangchong_count: int
        def __init__(self, total_count: _Optional[int] = ..., rong_count: _Optional[int] = ..., zimo_count: _Optional[int] = ..., fangchong_count: _Optional[int] = ...) -> None: ...
    class HuSummary(_message.Message):
        __slots__ = ["total_count", "dora_round_count", "total_fan"]
        TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
        DORA_ROUND_COUNT_FIELD_NUMBER: _ClassVar[int]
        TOTAL_FAN_FIELD_NUMBER: _ClassVar[int]
        total_count: int
        dora_round_count: int
        total_fan: int
        def __init__(self, total_count: _Optional[int] = ..., dora_round_count: _Optional[int] = ..., total_fan: _Optional[int] = ...) -> None: ...
    class HighestHuRecord(_message.Message):
        __slots__ = ["fanshu", "doranum", "title", "hands", "ming", "hupai", "title_id"]
        FANSHU_FIELD_NUMBER: _ClassVar[int]
        DORANUM_FIELD_NUMBER: _ClassVar[int]
        TITLE_FIELD_NUMBER: _ClassVar[int]
        HANDS_FIELD_NUMBER: _ClassVar[int]
        MING_FIELD_NUMBER: _ClassVar[int]
        HUPAI_FIELD_NUMBER: _ClassVar[int]
        TITLE_ID_FIELD_NUMBER: _ClassVar[int]
        fanshu: int
        doranum: int
        title: str
        hands: _containers.RepeatedScalarFieldContainer[str]
        ming: _containers.RepeatedScalarFieldContainer[str]
        hupai: str
        title_id: int
        def __init__(self, fanshu: _Optional[int] = ..., doranum: _Optional[int] = ..., title: _Optional[str] = ..., hands: _Optional[_Iterable[str]] = ..., ming: _Optional[_Iterable[str]] = ..., hupai: _Optional[str] = ..., title_id: _Optional[int] = ...) -> None: ...
    class Liqi20Summary(_message.Message):
        __slots__ = ["total_count", "total_lidora_count", "average_hu_point"]
        TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
        TOTAL_LIDORA_COUNT_FIELD_NUMBER: _ClassVar[int]
        AVERAGE_HU_POINT_FIELD_NUMBER: _ClassVar[int]
        total_count: int
        total_lidora_count: int
        average_hu_point: int
        def __init__(self, total_count: _Optional[int] = ..., total_lidora_count: _Optional[int] = ..., average_hu_point: _Optional[int] = ...) -> None: ...
    class LiQi10Summary(_message.Message):
        __slots__ = ["total_xuanshang", "total_fanshu"]
        TOTAL_XUANSHANG_FIELD_NUMBER: _ClassVar[int]
        TOTAL_FANSHU_FIELD_NUMBER: _ClassVar[int]
        total_xuanshang: int
        total_fanshu: int
        def __init__(self, total_xuanshang: _Optional[int] = ..., total_fanshu: _Optional[int] = ...) -> None: ...
    class GameResult(_message.Message):
        __slots__ = ["rank", "final_point"]
        RANK_FIELD_NUMBER: _ClassVar[int]
        FINAL_POINT_FIELD_NUMBER: _ClassVar[int]
        rank: int
        final_point: int
        def __init__(self, rank: _Optional[int] = ..., final_point: _Optional[int] = ...) -> None: ...
    FINAL_POSITION_COUNTS_FIELD_NUMBER: _ClassVar[int]
    RECENT_ROUND_FIELD_NUMBER: _ClassVar[int]
    RECENT_HU_FIELD_NUMBER: _ClassVar[int]
    HIGHEST_HU_FIELD_NUMBER: _ClassVar[int]
    RECENT_20_HU_SUMMARY_FIELD_NUMBER: _ClassVar[int]
    RECENT_10_HU_SUMMARY_FIELD_NUMBER: _ClassVar[int]
    RECENT_10_GAME_RESULT_FIELD_NUMBER: _ClassVar[int]
    final_position_counts: _containers.RepeatedScalarFieldContainer[int]
    recent_round: AccountMahjongStatistic.RoundSummary
    recent_hu: AccountMahjongStatistic.HuSummary
    highest_hu: AccountMahjongStatistic.HighestHuRecord
    recent_20_hu_summary: AccountMahjongStatistic.Liqi20Summary
    recent_10_hu_summary: AccountMahjongStatistic.LiQi10Summary
    recent_10_game_result: _containers.RepeatedCompositeFieldContainer[AccountMahjongStatistic.GameResult]
    def __init__(self, final_position_counts: _Optional[_Iterable[int]] = ..., recent_round: _Optional[_Union[AccountMahjongStatistic.RoundSummary, _Mapping]] = ..., recent_hu: _Optional[_Union[AccountMahjongStatistic.HuSummary, _Mapping]] = ..., highest_hu: _Optional[_Union[AccountMahjongStatistic.HighestHuRecord, _Mapping]] = ..., recent_20_hu_summary: _Optional[_Union[AccountMahjongStatistic.Liqi20Summary, _Mapping]] = ..., recent_10_hu_summary: _Optional[_Union[AccountMahjongStatistic.LiQi10Summary, _Mapping]] = ..., recent_10_game_result: _Optional[_Iterable[_Union[AccountMahjongStatistic.GameResult, _Mapping]]] = ...) -> None: ...

class AccountStatisticData(_message.Message):
    __slots__ = ["mahjong_category", "game_category", "statistic", "game_type"]
    MAHJONG_CATEGORY_FIELD_NUMBER: _ClassVar[int]
    GAME_CATEGORY_FIELD_NUMBER: _ClassVar[int]
    STATISTIC_FIELD_NUMBER: _ClassVar[int]
    GAME_TYPE_FIELD_NUMBER: _ClassVar[int]
    mahjong_category: int
    game_category: int
    statistic: AccountMahjongStatistic
    game_type: int
    def __init__(self, mahjong_category: _Optional[int] = ..., game_category: _Optional[int] = ..., statistic: _Optional[_Union[AccountMahjongStatistic, _Mapping]] = ..., game_type: _Optional[int] = ...) -> None: ...

class AccountLevel(_message.Message):
    __slots__ = ["id", "score"]
    ID_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    id: int
    score: int
    def __init__(self, id: _Optional[int] = ..., score: _Optional[int] = ...) -> None: ...

class ViewSlot(_message.Message):
    __slots__ = ["slot", "item_id", "type", "item_id_list"]
    SLOT_FIELD_NUMBER: _ClassVar[int]
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ITEM_ID_LIST_FIELD_NUMBER: _ClassVar[int]
    slot: int
    item_id: int
    type: int
    item_id_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, slot: _Optional[int] = ..., item_id: _Optional[int] = ..., type: _Optional[int] = ..., item_id_list: _Optional[_Iterable[int]] = ...) -> None: ...

class Account(_message.Message):
    __slots__ = ["account_id", "nickname", "login_time", "logout_time", "room_id", "anti_addiction", "title", "signature", "email", "email_verify", "gold", "diamond", "avatar_id", "vip", "birthday", "phone", "phone_verify", "platform_diamond", "level", "level3", "avatar_frame", "skin_ticket", "platform_skin_ticket", "verified", "challenge_levels", "achievement_count", "frozen_state", "loading_image"]
    class PlatformDiamond(_message.Message):
        __slots__ = ["id", "count"]
        ID_FIELD_NUMBER: _ClassVar[int]
        COUNT_FIELD_NUMBER: _ClassVar[int]
        id: int
        count: int
        def __init__(self, id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...
    class PlatformSkinTicket(_message.Message):
        __slots__ = ["id", "count"]
        ID_FIELD_NUMBER: _ClassVar[int]
        COUNT_FIELD_NUMBER: _ClassVar[int]
        id: int
        count: int
        def __init__(self, id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...
    class ChallengeLevel(_message.Message):
        __slots__ = ["season", "level", "rank"]
        SEASON_FIELD_NUMBER: _ClassVar[int]
        LEVEL_FIELD_NUMBER: _ClassVar[int]
        RANK_FIELD_NUMBER: _ClassVar[int]
        season: int
        level: int
        rank: int
        def __init__(self, season: _Optional[int] = ..., level: _Optional[int] = ..., rank: _Optional[int] = ...) -> None: ...
    class AchievementCount(_message.Message):
        __slots__ = ["rare", "count"]
        RARE_FIELD_NUMBER: _ClassVar[int]
        COUNT_FIELD_NUMBER: _ClassVar[int]
        rare: int
        count: int
        def __init__(self, rare: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    NICKNAME_FIELD_NUMBER: _ClassVar[int]
    LOGIN_TIME_FIELD_NUMBER: _ClassVar[int]
    LOGOUT_TIME_FIELD_NUMBER: _ClassVar[int]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    ANTI_ADDICTION_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    EMAIL_VERIFY_FIELD_NUMBER: _ClassVar[int]
    GOLD_FIELD_NUMBER: _ClassVar[int]
    DIAMOND_FIELD_NUMBER: _ClassVar[int]
    AVATAR_ID_FIELD_NUMBER: _ClassVar[int]
    VIP_FIELD_NUMBER: _ClassVar[int]
    BIRTHDAY_FIELD_NUMBER: _ClassVar[int]
    PHONE_FIELD_NUMBER: _ClassVar[int]
    PHONE_VERIFY_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_DIAMOND_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    LEVEL3_FIELD_NUMBER: _ClassVar[int]
    AVATAR_FRAME_FIELD_NUMBER: _ClassVar[int]
    SKIN_TICKET_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_SKIN_TICKET_FIELD_NUMBER: _ClassVar[int]
    VERIFIED_FIELD_NUMBER: _ClassVar[int]
    CHALLENGE_LEVELS_FIELD_NUMBER: _ClassVar[int]
    ACHIEVEMENT_COUNT_FIELD_NUMBER: _ClassVar[int]
    FROZEN_STATE_FIELD_NUMBER: _ClassVar[int]
    LOADING_IMAGE_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    nickname: str
    login_time: int
    logout_time: int
    room_id: int
    anti_addiction: AntiAddiction
    title: int
    signature: str
    email: str
    email_verify: int
    gold: int
    diamond: int
    avatar_id: int
    vip: int
    birthday: int
    phone: str
    phone_verify: int
    platform_diamond: _containers.RepeatedCompositeFieldContainer[Account.PlatformDiamond]
    level: AccountLevel
    level3: AccountLevel
    avatar_frame: int
    skin_ticket: int
    platform_skin_ticket: _containers.RepeatedCompositeFieldContainer[Account.PlatformSkinTicket]
    verified: int
    challenge_levels: _containers.RepeatedCompositeFieldContainer[Account.ChallengeLevel]
    achievement_count: _containers.RepeatedCompositeFieldContainer[Account.AchievementCount]
    frozen_state: int
    loading_image: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, account_id: _Optional[int] = ..., nickname: _Optional[str] = ..., login_time: _Optional[int] = ..., logout_time: _Optional[int] = ..., room_id: _Optional[int] = ..., anti_addiction: _Optional[_Union[AntiAddiction, _Mapping]] = ..., title: _Optional[int] = ..., signature: _Optional[str] = ..., email: _Optional[str] = ..., email_verify: _Optional[int] = ..., gold: _Optional[int] = ..., diamond: _Optional[int] = ..., avatar_id: _Optional[int] = ..., vip: _Optional[int] = ..., birthday: _Optional[int] = ..., phone: _Optional[str] = ..., phone_verify: _Optional[int] = ..., platform_diamond: _Optional[_Iterable[_Union[Account.PlatformDiamond, _Mapping]]] = ..., level: _Optional[_Union[AccountLevel, _Mapping]] = ..., level3: _Optional[_Union[AccountLevel, _Mapping]] = ..., avatar_frame: _Optional[int] = ..., skin_ticket: _Optional[int] = ..., platform_skin_ticket: _Optional[_Iterable[_Union[Account.PlatformSkinTicket, _Mapping]]] = ..., verified: _Optional[int] = ..., challenge_levels: _Optional[_Iterable[_Union[Account.ChallengeLevel, _Mapping]]] = ..., achievement_count: _Optional[_Iterable[_Union[Account.AchievementCount, _Mapping]]] = ..., frozen_state: _Optional[int] = ..., loading_image: _Optional[_Iterable[int]] = ...) -> None: ...

class AccountOwnerData(_message.Message):
    __slots__ = ["unlock_characters"]
    UNLOCK_CHARACTERS_FIELD_NUMBER: _ClassVar[int]
    unlock_characters: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, unlock_characters: _Optional[_Iterable[int]] = ...) -> None: ...

class AccountUpdate(_message.Message):
    __slots__ = ["numerical", "character", "bag", "achievement", "shilian", "daily_task", "title", "new_recharged_list", "activity_task", "activity_flip_task", "activity_period_task", "activity_random_task", "challenge", "ab_match", "activity", "activity_segment_task", "month_ticket"]
    class NumericalUpdate(_message.Message):
        __slots__ = ["id", "final"]
        ID_FIELD_NUMBER: _ClassVar[int]
        FINAL_FIELD_NUMBER: _ClassVar[int]
        id: int
        final: int
        def __init__(self, id: _Optional[int] = ..., final: _Optional[int] = ...) -> None: ...
    class CharacterUpdate(_message.Message):
        __slots__ = ["characters", "skins", "finished_endings", "rewarded_endings"]
        CHARACTERS_FIELD_NUMBER: _ClassVar[int]
        SKINS_FIELD_NUMBER: _ClassVar[int]
        FINISHED_ENDINGS_FIELD_NUMBER: _ClassVar[int]
        REWARDED_ENDINGS_FIELD_NUMBER: _ClassVar[int]
        characters: _containers.RepeatedCompositeFieldContainer[Character]
        skins: _containers.RepeatedScalarFieldContainer[int]
        finished_endings: _containers.RepeatedScalarFieldContainer[int]
        rewarded_endings: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, characters: _Optional[_Iterable[_Union[Character, _Mapping]]] = ..., skins: _Optional[_Iterable[int]] = ..., finished_endings: _Optional[_Iterable[int]] = ..., rewarded_endings: _Optional[_Iterable[int]] = ...) -> None: ...
    class AchievementUpdate(_message.Message):
        __slots__ = ["progresses", "rewarded_group"]
        PROGRESSES_FIELD_NUMBER: _ClassVar[int]
        REWARDED_GROUP_FIELD_NUMBER: _ClassVar[int]
        progresses: _containers.RepeatedCompositeFieldContainer[AchievementProgress]
        rewarded_group: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, progresses: _Optional[_Iterable[_Union[AchievementProgress, _Mapping]]] = ..., rewarded_group: _Optional[_Iterable[int]] = ...) -> None: ...
    class DailyTaskUpdate(_message.Message):
        __slots__ = ["progresses", "task_list"]
        PROGRESSES_FIELD_NUMBER: _ClassVar[int]
        TASK_LIST_FIELD_NUMBER: _ClassVar[int]
        progresses: _containers.RepeatedCompositeFieldContainer[TaskProgress]
        task_list: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, progresses: _Optional[_Iterable[_Union[TaskProgress, _Mapping]]] = ..., task_list: _Optional[_Iterable[int]] = ...) -> None: ...
    class TitleUpdate(_message.Message):
        __slots__ = ["new_titles", "remove_titles"]
        NEW_TITLES_FIELD_NUMBER: _ClassVar[int]
        REMOVE_TITLES_FIELD_NUMBER: _ClassVar[int]
        new_titles: _containers.RepeatedScalarFieldContainer[int]
        remove_titles: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, new_titles: _Optional[_Iterable[int]] = ..., remove_titles: _Optional[_Iterable[int]] = ...) -> None: ...
    class TaskUpdate(_message.Message):
        __slots__ = ["progresses", "task_list"]
        PROGRESSES_FIELD_NUMBER: _ClassVar[int]
        TASK_LIST_FIELD_NUMBER: _ClassVar[int]
        progresses: _containers.RepeatedCompositeFieldContainer[TaskProgress]
        task_list: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, progresses: _Optional[_Iterable[_Union[TaskProgress, _Mapping]]] = ..., task_list: _Optional[_Iterable[int]] = ...) -> None: ...
    class AccountChallengeUpdate(_message.Message):
        __slots__ = ["progresses", "level", "refresh_count", "match_count", "ticket_id", "task_list", "rewarded_season"]
        PROGRESSES_FIELD_NUMBER: _ClassVar[int]
        LEVEL_FIELD_NUMBER: _ClassVar[int]
        REFRESH_COUNT_FIELD_NUMBER: _ClassVar[int]
        MATCH_COUNT_FIELD_NUMBER: _ClassVar[int]
        TICKET_ID_FIELD_NUMBER: _ClassVar[int]
        TASK_LIST_FIELD_NUMBER: _ClassVar[int]
        REWARDED_SEASON_FIELD_NUMBER: _ClassVar[int]
        progresses: _containers.RepeatedCompositeFieldContainer[TaskProgress]
        level: int
        refresh_count: int
        match_count: int
        ticket_id: int
        task_list: _containers.RepeatedScalarFieldContainer[int]
        rewarded_season: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, progresses: _Optional[_Iterable[_Union[TaskProgress, _Mapping]]] = ..., level: _Optional[int] = ..., refresh_count: _Optional[int] = ..., match_count: _Optional[int] = ..., ticket_id: _Optional[int] = ..., task_list: _Optional[_Iterable[int]] = ..., rewarded_season: _Optional[_Iterable[int]] = ...) -> None: ...
    class AccountABMatchUpdate(_message.Message):
        __slots__ = ["match_id", "match_count", "buy_in_count", "point", "rewarded", "match_max_point", "quit"]
        class MatchPoint(_message.Message):
            __slots__ = ["match_id", "point"]
            MATCH_ID_FIELD_NUMBER: _ClassVar[int]
            POINT_FIELD_NUMBER: _ClassVar[int]
            match_id: int
            point: int
            def __init__(self, match_id: _Optional[int] = ..., point: _Optional[int] = ...) -> None: ...
        MATCH_ID_FIELD_NUMBER: _ClassVar[int]
        MATCH_COUNT_FIELD_NUMBER: _ClassVar[int]
        BUY_IN_COUNT_FIELD_NUMBER: _ClassVar[int]
        POINT_FIELD_NUMBER: _ClassVar[int]
        REWARDED_FIELD_NUMBER: _ClassVar[int]
        MATCH_MAX_POINT_FIELD_NUMBER: _ClassVar[int]
        QUIT_FIELD_NUMBER: _ClassVar[int]
        match_id: int
        match_count: int
        buy_in_count: int
        point: int
        rewarded: bool
        match_max_point: _containers.RepeatedCompositeFieldContainer[AccountUpdate.AccountABMatchUpdate.MatchPoint]
        quit: bool
        def __init__(self, match_id: _Optional[int] = ..., match_count: _Optional[int] = ..., buy_in_count: _Optional[int] = ..., point: _Optional[int] = ..., rewarded: bool = ..., match_max_point: _Optional[_Iterable[_Union[AccountUpdate.AccountABMatchUpdate.MatchPoint, _Mapping]]] = ..., quit: bool = ...) -> None: ...
    class SegmentTaskUpdate(_message.Message):
        __slots__ = ["progresses", "task_list"]
        PROGRESSES_FIELD_NUMBER: _ClassVar[int]
        TASK_LIST_FIELD_NUMBER: _ClassVar[int]
        progresses: _containers.RepeatedCompositeFieldContainer[SegmentTaskProgress]
        task_list: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, progresses: _Optional[_Iterable[_Union[SegmentTaskProgress, _Mapping]]] = ..., task_list: _Optional[_Iterable[int]] = ...) -> None: ...
    class MonthTicketUpdate(_message.Message):
        __slots__ = ["end_time", "last_pay_time"]
        END_TIME_FIELD_NUMBER: _ClassVar[int]
        LAST_PAY_TIME_FIELD_NUMBER: _ClassVar[int]
        end_time: int
        last_pay_time: int
        def __init__(self, end_time: _Optional[int] = ..., last_pay_time: _Optional[int] = ...) -> None: ...
    NUMERICAL_FIELD_NUMBER: _ClassVar[int]
    CHARACTER_FIELD_NUMBER: _ClassVar[int]
    BAG_FIELD_NUMBER: _ClassVar[int]
    ACHIEVEMENT_FIELD_NUMBER: _ClassVar[int]
    SHILIAN_FIELD_NUMBER: _ClassVar[int]
    DAILY_TASK_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    NEW_RECHARGED_LIST_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_TASK_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_FLIP_TASK_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_PERIOD_TASK_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_RANDOM_TASK_FIELD_NUMBER: _ClassVar[int]
    CHALLENGE_FIELD_NUMBER: _ClassVar[int]
    AB_MATCH_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_SEGMENT_TASK_FIELD_NUMBER: _ClassVar[int]
    MONTH_TICKET_FIELD_NUMBER: _ClassVar[int]
    numerical: _containers.RepeatedCompositeFieldContainer[AccountUpdate.NumericalUpdate]
    character: AccountUpdate.CharacterUpdate
    bag: BagUpdate
    achievement: AccountUpdate.AchievementUpdate
    shilian: AccountShiLian
    daily_task: AccountUpdate.DailyTaskUpdate
    title: AccountUpdate.TitleUpdate
    new_recharged_list: _containers.RepeatedScalarFieldContainer[int]
    activity_task: AccountUpdate.TaskUpdate
    activity_flip_task: AccountUpdate.TaskUpdate
    activity_period_task: AccountUpdate.TaskUpdate
    activity_random_task: AccountUpdate.TaskUpdate
    challenge: AccountUpdate.AccountChallengeUpdate
    ab_match: AccountUpdate.AccountABMatchUpdate
    activity: AccountActivityUpdate
    activity_segment_task: AccountUpdate.SegmentTaskUpdate
    month_ticket: AccountUpdate.MonthTicketUpdate
    def __init__(self, numerical: _Optional[_Iterable[_Union[AccountUpdate.NumericalUpdate, _Mapping]]] = ..., character: _Optional[_Union[AccountUpdate.CharacterUpdate, _Mapping]] = ..., bag: _Optional[_Union[BagUpdate, _Mapping]] = ..., achievement: _Optional[_Union[AccountUpdate.AchievementUpdate, _Mapping]] = ..., shilian: _Optional[_Union[AccountShiLian, _Mapping]] = ..., daily_task: _Optional[_Union[AccountUpdate.DailyTaskUpdate, _Mapping]] = ..., title: _Optional[_Union[AccountUpdate.TitleUpdate, _Mapping]] = ..., new_recharged_list: _Optional[_Iterable[int]] = ..., activity_task: _Optional[_Union[AccountUpdate.TaskUpdate, _Mapping]] = ..., activity_flip_task: _Optional[_Union[AccountUpdate.TaskUpdate, _Mapping]] = ..., activity_period_task: _Optional[_Union[AccountUpdate.TaskUpdate, _Mapping]] = ..., activity_random_task: _Optional[_Union[AccountUpdate.TaskUpdate, _Mapping]] = ..., challenge: _Optional[_Union[AccountUpdate.AccountChallengeUpdate, _Mapping]] = ..., ab_match: _Optional[_Union[AccountUpdate.AccountABMatchUpdate, _Mapping]] = ..., activity: _Optional[_Union[AccountActivityUpdate, _Mapping]] = ..., activity_segment_task: _Optional[_Union[AccountUpdate.SegmentTaskUpdate, _Mapping]] = ..., month_ticket: _Optional[_Union[AccountUpdate.MonthTicketUpdate, _Mapping]] = ...) -> None: ...

class GameMetaData(_message.Message):
    __slots__ = ["room_id", "mode_id", "contest_uid"]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    MODE_ID_FIELD_NUMBER: _ClassVar[int]
    CONTEST_UID_FIELD_NUMBER: _ClassVar[int]
    room_id: int
    mode_id: int
    contest_uid: int
    def __init__(self, room_id: _Optional[int] = ..., mode_id: _Optional[int] = ..., contest_uid: _Optional[int] = ...) -> None: ...

class AccountPlayingGame(_message.Message):
    __slots__ = ["game_uuid", "category", "meta"]
    GAME_UUID_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    META_FIELD_NUMBER: _ClassVar[int]
    game_uuid: str
    category: int
    meta: GameMetaData
    def __init__(self, game_uuid: _Optional[str] = ..., category: _Optional[int] = ..., meta: _Optional[_Union[GameMetaData, _Mapping]] = ...) -> None: ...

class AccountCacheView(_message.Message):
    __slots__ = ["cache_version", "account_id", "nickname", "login_time", "logout_time", "is_online", "room_id", "title", "avatar_id", "vip", "level", "playing_game", "level3", "avatar_frame", "verified", "ban_deadline", "comment_ban", "ban_state"]
    CACHE_VERSION_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    NICKNAME_FIELD_NUMBER: _ClassVar[int]
    LOGIN_TIME_FIELD_NUMBER: _ClassVar[int]
    LOGOUT_TIME_FIELD_NUMBER: _ClassVar[int]
    IS_ONLINE_FIELD_NUMBER: _ClassVar[int]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    AVATAR_ID_FIELD_NUMBER: _ClassVar[int]
    VIP_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    PLAYING_GAME_FIELD_NUMBER: _ClassVar[int]
    LEVEL3_FIELD_NUMBER: _ClassVar[int]
    AVATAR_FRAME_FIELD_NUMBER: _ClassVar[int]
    VERIFIED_FIELD_NUMBER: _ClassVar[int]
    BAN_DEADLINE_FIELD_NUMBER: _ClassVar[int]
    COMMENT_BAN_FIELD_NUMBER: _ClassVar[int]
    BAN_STATE_FIELD_NUMBER: _ClassVar[int]
    cache_version: int
    account_id: int
    nickname: str
    login_time: int
    logout_time: int
    is_online: bool
    room_id: int
    title: int
    avatar_id: int
    vip: int
    level: AccountLevel
    playing_game: AccountPlayingGame
    level3: AccountLevel
    avatar_frame: int
    verified: int
    ban_deadline: int
    comment_ban: int
    ban_state: int
    def __init__(self, cache_version: _Optional[int] = ..., account_id: _Optional[int] = ..., nickname: _Optional[str] = ..., login_time: _Optional[int] = ..., logout_time: _Optional[int] = ..., is_online: bool = ..., room_id: _Optional[int] = ..., title: _Optional[int] = ..., avatar_id: _Optional[int] = ..., vip: _Optional[int] = ..., level: _Optional[_Union[AccountLevel, _Mapping]] = ..., playing_game: _Optional[_Union[AccountPlayingGame, _Mapping]] = ..., level3: _Optional[_Union[AccountLevel, _Mapping]] = ..., avatar_frame: _Optional[int] = ..., verified: _Optional[int] = ..., ban_deadline: _Optional[int] = ..., comment_ban: _Optional[int] = ..., ban_state: _Optional[int] = ...) -> None: ...

class PlayerBaseView(_message.Message):
    __slots__ = ["account_id", "avatar_id", "title", "nickname", "level", "level3", "avatar_frame", "verified", "is_banned"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    AVATAR_ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    NICKNAME_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    LEVEL3_FIELD_NUMBER: _ClassVar[int]
    AVATAR_FRAME_FIELD_NUMBER: _ClassVar[int]
    VERIFIED_FIELD_NUMBER: _ClassVar[int]
    IS_BANNED_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    avatar_id: int
    title: int
    nickname: str
    level: AccountLevel
    level3: AccountLevel
    avatar_frame: int
    verified: int
    is_banned: int
    def __init__(self, account_id: _Optional[int] = ..., avatar_id: _Optional[int] = ..., title: _Optional[int] = ..., nickname: _Optional[str] = ..., level: _Optional[_Union[AccountLevel, _Mapping]] = ..., level3: _Optional[_Union[AccountLevel, _Mapping]] = ..., avatar_frame: _Optional[int] = ..., verified: _Optional[int] = ..., is_banned: _Optional[int] = ...) -> None: ...

class PlayerGameView(_message.Message):
    __slots__ = ["account_id", "avatar_id", "title", "nickname", "level", "character", "level3", "avatar_frame", "verified", "views"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    AVATAR_ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    NICKNAME_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    CHARACTER_FIELD_NUMBER: _ClassVar[int]
    LEVEL3_FIELD_NUMBER: _ClassVar[int]
    AVATAR_FRAME_FIELD_NUMBER: _ClassVar[int]
    VERIFIED_FIELD_NUMBER: _ClassVar[int]
    VIEWS_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    avatar_id: int
    title: int
    nickname: str
    level: AccountLevel
    character: Character
    level3: AccountLevel
    avatar_frame: int
    verified: int
    views: _containers.RepeatedCompositeFieldContainer[ViewSlot]
    def __init__(self, account_id: _Optional[int] = ..., avatar_id: _Optional[int] = ..., title: _Optional[int] = ..., nickname: _Optional[str] = ..., level: _Optional[_Union[AccountLevel, _Mapping]] = ..., character: _Optional[_Union[Character, _Mapping]] = ..., level3: _Optional[_Union[AccountLevel, _Mapping]] = ..., avatar_frame: _Optional[int] = ..., verified: _Optional[int] = ..., views: _Optional[_Iterable[_Union[ViewSlot, _Mapping]]] = ...) -> None: ...

class GameSetting(_message.Message):
    __slots__ = ["emoji_switch"]
    EMOJI_SWITCH_FIELD_NUMBER: _ClassVar[int]
    emoji_switch: int
    def __init__(self, emoji_switch: _Optional[int] = ...) -> None: ...

class GameMode(_message.Message):
    __slots__ = ["mode", "ai", "extendinfo", "detail_rule", "testing_environment", "game_setting"]
    MODE_FIELD_NUMBER: _ClassVar[int]
    AI_FIELD_NUMBER: _ClassVar[int]
    EXTENDINFO_FIELD_NUMBER: _ClassVar[int]
    DETAIL_RULE_FIELD_NUMBER: _ClassVar[int]
    TESTING_ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    GAME_SETTING_FIELD_NUMBER: _ClassVar[int]
    mode: int
    ai: bool
    extendinfo: str
    detail_rule: GameDetailRule
    testing_environment: GameTestingEnvironmentSet
    game_setting: GameSetting
    def __init__(self, mode: _Optional[int] = ..., ai: bool = ..., extendinfo: _Optional[str] = ..., detail_rule: _Optional[_Union[GameDetailRule, _Mapping]] = ..., testing_environment: _Optional[_Union[GameTestingEnvironmentSet, _Mapping]] = ..., game_setting: _Optional[_Union[GameSetting, _Mapping]] = ...) -> None: ...

class GameTestingEnvironmentSet(_message.Message):
    __slots__ = ["paixing", "left_count", "field_spell_var"]
    PAIXING_FIELD_NUMBER: _ClassVar[int]
    LEFT_COUNT_FIELD_NUMBER: _ClassVar[int]
    FIELD_SPELL_VAR_FIELD_NUMBER: _ClassVar[int]
    paixing: int
    left_count: int
    field_spell_var: int
    def __init__(self, paixing: _Optional[int] = ..., left_count: _Optional[int] = ..., field_spell_var: _Optional[int] = ...) -> None: ...

class GameDetailRule(_message.Message):
    __slots__ = ["time_fixed", "time_add", "dora_count", "shiduan", "init_point", "fandian", "can_jifei", "tianbian_value", "liqibang_value", "changbang_value", "noting_fafu_1", "noting_fafu_2", "noting_fafu_3", "have_liujumanguan", "have_qieshangmanguan", "have_biao_dora", "have_gang_biao_dora", "ming_dora_immediately_open", "have_li_dora", "have_gang_li_dora", "have_sifenglianda", "have_sigangsanle", "have_sijializhi", "have_jiuzhongjiupai", "have_sanjiahele", "have_toutiao", "have_helelianzhuang", "have_helezhongju", "have_tingpailianzhuang", "have_tingpaizhongju", "have_yifa", "have_nanruxiru", "jingsuanyuandian", "shunweima_2", "shunweima_3", "shunweima_4", "bianjietishi", "ai_level", "have_zimosun", "disable_multi_yukaman", "fanfu", "guyi_mode", "dora3_mode", "begin_open_mode", "jiuchao_mode", "muyu_mode", "open_hand", "xuezhandaodi", "huansanzhang", "chuanma", "reveal_discard", "field_spell_mode", "zhanxing", "tianming_mode", "disable_leijiyiman", "disable_double_yakuman", "disable_composite_yakuman", "enable_shiti", "enable_nontsumo_liqi", "disable_double_wind_four_fu", "disable_angang_guoshi", "enable_renhe", "enable_baopai_extend_settings", "yongchang_mode", "hunzhiyiji_mode"]
    TIME_FIXED_FIELD_NUMBER: _ClassVar[int]
    TIME_ADD_FIELD_NUMBER: _ClassVar[int]
    DORA_COUNT_FIELD_NUMBER: _ClassVar[int]
    SHIDUAN_FIELD_NUMBER: _ClassVar[int]
    INIT_POINT_FIELD_NUMBER: _ClassVar[int]
    FANDIAN_FIELD_NUMBER: _ClassVar[int]
    CAN_JIFEI_FIELD_NUMBER: _ClassVar[int]
    TIANBIAN_VALUE_FIELD_NUMBER: _ClassVar[int]
    LIQIBANG_VALUE_FIELD_NUMBER: _ClassVar[int]
    CHANGBANG_VALUE_FIELD_NUMBER: _ClassVar[int]
    NOTING_FAFU_1_FIELD_NUMBER: _ClassVar[int]
    NOTING_FAFU_2_FIELD_NUMBER: _ClassVar[int]
    NOTING_FAFU_3_FIELD_NUMBER: _ClassVar[int]
    HAVE_LIUJUMANGUAN_FIELD_NUMBER: _ClassVar[int]
    HAVE_QIESHANGMANGUAN_FIELD_NUMBER: _ClassVar[int]
    HAVE_BIAO_DORA_FIELD_NUMBER: _ClassVar[int]
    HAVE_GANG_BIAO_DORA_FIELD_NUMBER: _ClassVar[int]
    MING_DORA_IMMEDIATELY_OPEN_FIELD_NUMBER: _ClassVar[int]
    HAVE_LI_DORA_FIELD_NUMBER: _ClassVar[int]
    HAVE_GANG_LI_DORA_FIELD_NUMBER: _ClassVar[int]
    HAVE_SIFENGLIANDA_FIELD_NUMBER: _ClassVar[int]
    HAVE_SIGANGSANLE_FIELD_NUMBER: _ClassVar[int]
    HAVE_SIJIALIZHI_FIELD_NUMBER: _ClassVar[int]
    HAVE_JIUZHONGJIUPAI_FIELD_NUMBER: _ClassVar[int]
    HAVE_SANJIAHELE_FIELD_NUMBER: _ClassVar[int]
    HAVE_TOUTIAO_FIELD_NUMBER: _ClassVar[int]
    HAVE_HELELIANZHUANG_FIELD_NUMBER: _ClassVar[int]
    HAVE_HELEZHONGJU_FIELD_NUMBER: _ClassVar[int]
    HAVE_TINGPAILIANZHUANG_FIELD_NUMBER: _ClassVar[int]
    HAVE_TINGPAIZHONGJU_FIELD_NUMBER: _ClassVar[int]
    HAVE_YIFA_FIELD_NUMBER: _ClassVar[int]
    HAVE_NANRUXIRU_FIELD_NUMBER: _ClassVar[int]
    JINGSUANYUANDIAN_FIELD_NUMBER: _ClassVar[int]
    SHUNWEIMA_2_FIELD_NUMBER: _ClassVar[int]
    SHUNWEIMA_3_FIELD_NUMBER: _ClassVar[int]
    SHUNWEIMA_4_FIELD_NUMBER: _ClassVar[int]
    BIANJIETISHI_FIELD_NUMBER: _ClassVar[int]
    AI_LEVEL_FIELD_NUMBER: _ClassVar[int]
    HAVE_ZIMOSUN_FIELD_NUMBER: _ClassVar[int]
    DISABLE_MULTI_YUKAMAN_FIELD_NUMBER: _ClassVar[int]
    FANFU_FIELD_NUMBER: _ClassVar[int]
    GUYI_MODE_FIELD_NUMBER: _ClassVar[int]
    DORA3_MODE_FIELD_NUMBER: _ClassVar[int]
    BEGIN_OPEN_MODE_FIELD_NUMBER: _ClassVar[int]
    JIUCHAO_MODE_FIELD_NUMBER: _ClassVar[int]
    MUYU_MODE_FIELD_NUMBER: _ClassVar[int]
    OPEN_HAND_FIELD_NUMBER: _ClassVar[int]
    XUEZHANDAODI_FIELD_NUMBER: _ClassVar[int]
    HUANSANZHANG_FIELD_NUMBER: _ClassVar[int]
    CHUANMA_FIELD_NUMBER: _ClassVar[int]
    REVEAL_DISCARD_FIELD_NUMBER: _ClassVar[int]
    FIELD_SPELL_MODE_FIELD_NUMBER: _ClassVar[int]
    ZHANXING_FIELD_NUMBER: _ClassVar[int]
    TIANMING_MODE_FIELD_NUMBER: _ClassVar[int]
    DISABLE_LEIJIYIMAN_FIELD_NUMBER: _ClassVar[int]
    DISABLE_DOUBLE_YAKUMAN_FIELD_NUMBER: _ClassVar[int]
    DISABLE_COMPOSITE_YAKUMAN_FIELD_NUMBER: _ClassVar[int]
    ENABLE_SHITI_FIELD_NUMBER: _ClassVar[int]
    ENABLE_NONTSUMO_LIQI_FIELD_NUMBER: _ClassVar[int]
    DISABLE_DOUBLE_WIND_FOUR_FU_FIELD_NUMBER: _ClassVar[int]
    DISABLE_ANGANG_GUOSHI_FIELD_NUMBER: _ClassVar[int]
    ENABLE_RENHE_FIELD_NUMBER: _ClassVar[int]
    ENABLE_BAOPAI_EXTEND_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    YONGCHANG_MODE_FIELD_NUMBER: _ClassVar[int]
    HUNZHIYIJI_MODE_FIELD_NUMBER: _ClassVar[int]
    time_fixed: int
    time_add: int
    dora_count: int
    shiduan: int
    init_point: int
    fandian: int
    can_jifei: bool
    tianbian_value: int
    liqibang_value: int
    changbang_value: int
    noting_fafu_1: int
    noting_fafu_2: int
    noting_fafu_3: int
    have_liujumanguan: bool
    have_qieshangmanguan: bool
    have_biao_dora: bool
    have_gang_biao_dora: bool
    ming_dora_immediately_open: bool
    have_li_dora: bool
    have_gang_li_dora: bool
    have_sifenglianda: bool
    have_sigangsanle: bool
    have_sijializhi: bool
    have_jiuzhongjiupai: bool
    have_sanjiahele: bool
    have_toutiao: bool
    have_helelianzhuang: bool
    have_helezhongju: bool
    have_tingpailianzhuang: bool
    have_tingpaizhongju: bool
    have_yifa: bool
    have_nanruxiru: bool
    jingsuanyuandian: int
    shunweima_2: int
    shunweima_3: int
    shunweima_4: int
    bianjietishi: bool
    ai_level: int
    have_zimosun: bool
    disable_multi_yukaman: bool
    fanfu: int
    guyi_mode: int
    dora3_mode: int
    begin_open_mode: int
    jiuchao_mode: int
    muyu_mode: int
    open_hand: int
    xuezhandaodi: int
    huansanzhang: int
    chuanma: int
    reveal_discard: int
    field_spell_mode: int
    zhanxing: int
    tianming_mode: int
    disable_leijiyiman: bool
    disable_double_yakuman: int
    disable_composite_yakuman: int
    enable_shiti: int
    enable_nontsumo_liqi: int
    disable_double_wind_four_fu: int
    disable_angang_guoshi: int
    enable_renhe: int
    enable_baopai_extend_settings: int
    yongchang_mode: int
    hunzhiyiji_mode: int
    def __init__(self, time_fixed: _Optional[int] = ..., time_add: _Optional[int] = ..., dora_count: _Optional[int] = ..., shiduan: _Optional[int] = ..., init_point: _Optional[int] = ..., fandian: _Optional[int] = ..., can_jifei: bool = ..., tianbian_value: _Optional[int] = ..., liqibang_value: _Optional[int] = ..., changbang_value: _Optional[int] = ..., noting_fafu_1: _Optional[int] = ..., noting_fafu_2: _Optional[int] = ..., noting_fafu_3: _Optional[int] = ..., have_liujumanguan: bool = ..., have_qieshangmanguan: bool = ..., have_biao_dora: bool = ..., have_gang_biao_dora: bool = ..., ming_dora_immediately_open: bool = ..., have_li_dora: bool = ..., have_gang_li_dora: bool = ..., have_sifenglianda: bool = ..., have_sigangsanle: bool = ..., have_sijializhi: bool = ..., have_jiuzhongjiupai: bool = ..., have_sanjiahele: bool = ..., have_toutiao: bool = ..., have_helelianzhuang: bool = ..., have_helezhongju: bool = ..., have_tingpailianzhuang: bool = ..., have_tingpaizhongju: bool = ..., have_yifa: bool = ..., have_nanruxiru: bool = ..., jingsuanyuandian: _Optional[int] = ..., shunweima_2: _Optional[int] = ..., shunweima_3: _Optional[int] = ..., shunweima_4: _Optional[int] = ..., bianjietishi: bool = ..., ai_level: _Optional[int] = ..., have_zimosun: bool = ..., disable_multi_yukaman: bool = ..., fanfu: _Optional[int] = ..., guyi_mode: _Optional[int] = ..., dora3_mode: _Optional[int] = ..., begin_open_mode: _Optional[int] = ..., jiuchao_mode: _Optional[int] = ..., muyu_mode: _Optional[int] = ..., open_hand: _Optional[int] = ..., xuezhandaodi: _Optional[int] = ..., huansanzhang: _Optional[int] = ..., chuanma: _Optional[int] = ..., reveal_discard: _Optional[int] = ..., field_spell_mode: _Optional[int] = ..., zhanxing: _Optional[int] = ..., tianming_mode: _Optional[int] = ..., disable_leijiyiman: bool = ..., disable_double_yakuman: _Optional[int] = ..., disable_composite_yakuman: _Optional[int] = ..., enable_shiti: _Optional[int] = ..., enable_nontsumo_liqi: _Optional[int] = ..., disable_double_wind_four_fu: _Optional[int] = ..., disable_angang_guoshi: _Optional[int] = ..., enable_renhe: _Optional[int] = ..., enable_baopai_extend_settings: _Optional[int] = ..., yongchang_mode: _Optional[int] = ..., hunzhiyiji_mode: _Optional[int] = ...) -> None: ...

class Room(_message.Message):
    __slots__ = ["room_id", "owner_id", "mode", "max_player_count", "persons", "ready_list", "is_playing", "public_live", "robot_count", "tournament_id", "seq", "pre_rule"]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    OWNER_ID_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    MAX_PLAYER_COUNT_FIELD_NUMBER: _ClassVar[int]
    PERSONS_FIELD_NUMBER: _ClassVar[int]
    READY_LIST_FIELD_NUMBER: _ClassVar[int]
    IS_PLAYING_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_LIVE_FIELD_NUMBER: _ClassVar[int]
    ROBOT_COUNT_FIELD_NUMBER: _ClassVar[int]
    TOURNAMENT_ID_FIELD_NUMBER: _ClassVar[int]
    SEQ_FIELD_NUMBER: _ClassVar[int]
    PRE_RULE_FIELD_NUMBER: _ClassVar[int]
    room_id: int
    owner_id: int
    mode: GameMode
    max_player_count: int
    persons: _containers.RepeatedCompositeFieldContainer[PlayerGameView]
    ready_list: _containers.RepeatedScalarFieldContainer[int]
    is_playing: bool
    public_live: bool
    robot_count: int
    tournament_id: int
    seq: int
    pre_rule: str
    def __init__(self, room_id: _Optional[int] = ..., owner_id: _Optional[int] = ..., mode: _Optional[_Union[GameMode, _Mapping]] = ..., max_player_count: _Optional[int] = ..., persons: _Optional[_Iterable[_Union[PlayerGameView, _Mapping]]] = ..., ready_list: _Optional[_Iterable[int]] = ..., is_playing: bool = ..., public_live: bool = ..., robot_count: _Optional[int] = ..., tournament_id: _Optional[int] = ..., seq: _Optional[int] = ..., pre_rule: _Optional[str] = ...) -> None: ...

class GameEndResult(_message.Message):
    __slots__ = ["players"]
    class PlayerItem(_message.Message):
        __slots__ = ["seat", "total_point", "part_point_1", "part_point_2", "grading_score", "gold"]
        SEAT_FIELD_NUMBER: _ClassVar[int]
        TOTAL_POINT_FIELD_NUMBER: _ClassVar[int]
        PART_POINT_1_FIELD_NUMBER: _ClassVar[int]
        PART_POINT_2_FIELD_NUMBER: _ClassVar[int]
        GRADING_SCORE_FIELD_NUMBER: _ClassVar[int]
        GOLD_FIELD_NUMBER: _ClassVar[int]
        seat: int
        total_point: int
        part_point_1: int
        part_point_2: int
        grading_score: int
        gold: int
        def __init__(self, seat: _Optional[int] = ..., total_point: _Optional[int] = ..., part_point_1: _Optional[int] = ..., part_point_2: _Optional[int] = ..., grading_score: _Optional[int] = ..., gold: _Optional[int] = ...) -> None: ...
    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    players: _containers.RepeatedCompositeFieldContainer[GameEndResult.PlayerItem]
    def __init__(self, players: _Optional[_Iterable[_Union[GameEndResult.PlayerItem, _Mapping]]] = ...) -> None: ...

class GameConnectInfo(_message.Message):
    __slots__ = ["connect_token", "game_uuid", "location"]
    CONNECT_TOKEN_FIELD_NUMBER: _ClassVar[int]
    GAME_UUID_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    connect_token: str
    game_uuid: str
    location: str
    def __init__(self, connect_token: _Optional[str] = ..., game_uuid: _Optional[str] = ..., location: _Optional[str] = ...) -> None: ...

class ItemGainRecord(_message.Message):
    __slots__ = ["item_id", "count"]
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    item_id: int
    count: int
    def __init__(self, item_id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class ItemGainRecords(_message.Message):
    __slots__ = ["record_time", "limit_source_id", "records"]
    RECORD_TIME_FIELD_NUMBER: _ClassVar[int]
    LIMIT_SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    RECORDS_FIELD_NUMBER: _ClassVar[int]
    record_time: int
    limit_source_id: int
    records: _containers.RepeatedCompositeFieldContainer[ItemGainRecord]
    def __init__(self, record_time: _Optional[int] = ..., limit_source_id: _Optional[int] = ..., records: _Optional[_Iterable[_Union[ItemGainRecord, _Mapping]]] = ...) -> None: ...

class FakeRandomRecords(_message.Message):
    __slots__ = ["item_id", "special_item_id", "gain_count", "gain_history"]
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    SPECIAL_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    GAIN_COUNT_FIELD_NUMBER: _ClassVar[int]
    GAIN_HISTORY_FIELD_NUMBER: _ClassVar[int]
    item_id: int
    special_item_id: int
    gain_count: int
    gain_history: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, item_id: _Optional[int] = ..., special_item_id: _Optional[int] = ..., gain_count: _Optional[int] = ..., gain_history: _Optional[_Iterable[int]] = ...) -> None: ...

class Item(_message.Message):
    __slots__ = ["item_id", "stack"]
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    STACK_FIELD_NUMBER: _ClassVar[int]
    item_id: int
    stack: int
    def __init__(self, item_id: _Optional[int] = ..., stack: _Optional[int] = ...) -> None: ...

class Bag(_message.Message):
    __slots__ = ["items", "daily_gain_record"]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    DAILY_GAIN_RECORD_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[Item]
    daily_gain_record: _containers.RepeatedCompositeFieldContainer[ItemGainRecords]
    def __init__(self, items: _Optional[_Iterable[_Union[Item, _Mapping]]] = ..., daily_gain_record: _Optional[_Iterable[_Union[ItemGainRecords, _Mapping]]] = ...) -> None: ...

class BagUpdate(_message.Message):
    __slots__ = ["update_items", "update_daily_gain_record"]
    UPDATE_ITEMS_FIELD_NUMBER: _ClassVar[int]
    UPDATE_DAILY_GAIN_RECORD_FIELD_NUMBER: _ClassVar[int]
    update_items: _containers.RepeatedCompositeFieldContainer[Item]
    update_daily_gain_record: _containers.RepeatedCompositeFieldContainer[ItemGainRecords]
    def __init__(self, update_items: _Optional[_Iterable[_Union[Item, _Mapping]]] = ..., update_daily_gain_record: _Optional[_Iterable[_Union[ItemGainRecords, _Mapping]]] = ...) -> None: ...

class RewardSlot(_message.Message):
    __slots__ = ["id", "count"]
    ID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    id: int
    count: int
    def __init__(self, id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class OpenResult(_message.Message):
    __slots__ = ["reward", "replace"]
    REWARD_FIELD_NUMBER: _ClassVar[int]
    REPLACE_FIELD_NUMBER: _ClassVar[int]
    reward: RewardSlot
    replace: RewardSlot
    def __init__(self, reward: _Optional[_Union[RewardSlot, _Mapping]] = ..., replace: _Optional[_Union[RewardSlot, _Mapping]] = ...) -> None: ...

class RewardPlusResult(_message.Message):
    __slots__ = ["id", "count", "exchange"]
    class Exchange(_message.Message):
        __slots__ = ["id", "count", "exchange"]
        ID_FIELD_NUMBER: _ClassVar[int]
        COUNT_FIELD_NUMBER: _ClassVar[int]
        EXCHANGE_FIELD_NUMBER: _ClassVar[int]
        id: int
        count: int
        exchange: int
        def __init__(self, id: _Optional[int] = ..., count: _Optional[int] = ..., exchange: _Optional[int] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    EXCHANGE_FIELD_NUMBER: _ClassVar[int]
    id: int
    count: int
    exchange: RewardPlusResult.Exchange
    def __init__(self, id: _Optional[int] = ..., count: _Optional[int] = ..., exchange: _Optional[_Union[RewardPlusResult.Exchange, _Mapping]] = ...) -> None: ...

class ExecuteReward(_message.Message):
    __slots__ = ["reward", "replace", "replace_count"]
    REWARD_FIELD_NUMBER: _ClassVar[int]
    REPLACE_FIELD_NUMBER: _ClassVar[int]
    REPLACE_COUNT_FIELD_NUMBER: _ClassVar[int]
    reward: RewardSlot
    replace: RewardSlot
    replace_count: int
    def __init__(self, reward: _Optional[_Union[RewardSlot, _Mapping]] = ..., replace: _Optional[_Union[RewardSlot, _Mapping]] = ..., replace_count: _Optional[int] = ...) -> None: ...

class ExecuteResult(_message.Message):
    __slots__ = ["id", "count"]
    ID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    id: int
    count: int
    def __init__(self, id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class I18nContext(_message.Message):
    __slots__ = ["lang", "context"]
    LANG_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    lang: str
    context: str
    def __init__(self, lang: _Optional[str] = ..., context: _Optional[str] = ...) -> None: ...

class Mail(_message.Message):
    __slots__ = ["mail_id", "state", "take_attachment", "title", "content", "attachments", "create_time", "expire_time", "reference_id", "title_i18n", "content_i18n", "template_id"]
    MAIL_ID_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    TAKE_ATTACHMENT_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    ATTACHMENTS_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    EXPIRE_TIME_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_I18N_FIELD_NUMBER: _ClassVar[int]
    CONTENT_I18N_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    mail_id: int
    state: int
    take_attachment: bool
    title: str
    content: str
    attachments: _containers.RepeatedCompositeFieldContainer[RewardSlot]
    create_time: int
    expire_time: int
    reference_id: int
    title_i18n: _containers.RepeatedCompositeFieldContainer[I18nContext]
    content_i18n: _containers.RepeatedCompositeFieldContainer[I18nContext]
    template_id: int
    def __init__(self, mail_id: _Optional[int] = ..., state: _Optional[int] = ..., take_attachment: bool = ..., title: _Optional[str] = ..., content: _Optional[str] = ..., attachments: _Optional[_Iterable[_Union[RewardSlot, _Mapping]]] = ..., create_time: _Optional[int] = ..., expire_time: _Optional[int] = ..., reference_id: _Optional[int] = ..., title_i18n: _Optional[_Iterable[_Union[I18nContext, _Mapping]]] = ..., content_i18n: _Optional[_Iterable[_Union[I18nContext, _Mapping]]] = ..., template_id: _Optional[int] = ...) -> None: ...

class AchievementProgress(_message.Message):
    __slots__ = ["id", "counter", "achieved", "rewarded", "achieved_time"]
    ID_FIELD_NUMBER: _ClassVar[int]
    COUNTER_FIELD_NUMBER: _ClassVar[int]
    ACHIEVED_FIELD_NUMBER: _ClassVar[int]
    REWARDED_FIELD_NUMBER: _ClassVar[int]
    ACHIEVED_TIME_FIELD_NUMBER: _ClassVar[int]
    id: int
    counter: int
    achieved: bool
    rewarded: bool
    achieved_time: int
    def __init__(self, id: _Optional[int] = ..., counter: _Optional[int] = ..., achieved: bool = ..., rewarded: bool = ..., achieved_time: _Optional[int] = ...) -> None: ...

class AccountStatisticByGameMode(_message.Message):
    __slots__ = ["mode", "game_count_sum", "game_final_position", "fly_count", "gold_earn_sum", "round_count_sum", "dadian_sum", "round_end", "ming_count_sum", "liqi_count_sum", "xun_count_sum", "highest_lianzhuang", "score_earn_sum", "rank_score"]
    class RoundEndData(_message.Message):
        __slots__ = ["type", "sum"]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        SUM_FIELD_NUMBER: _ClassVar[int]
        type: int
        sum: int
        def __init__(self, type: _Optional[int] = ..., sum: _Optional[int] = ...) -> None: ...
    class RankScore(_message.Message):
        __slots__ = ["rank", "score_sum", "count"]
        RANK_FIELD_NUMBER: _ClassVar[int]
        SCORE_SUM_FIELD_NUMBER: _ClassVar[int]
        COUNT_FIELD_NUMBER: _ClassVar[int]
        rank: int
        score_sum: int
        count: int
        def __init__(self, rank: _Optional[int] = ..., score_sum: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...
    MODE_FIELD_NUMBER: _ClassVar[int]
    GAME_COUNT_SUM_FIELD_NUMBER: _ClassVar[int]
    GAME_FINAL_POSITION_FIELD_NUMBER: _ClassVar[int]
    FLY_COUNT_FIELD_NUMBER: _ClassVar[int]
    GOLD_EARN_SUM_FIELD_NUMBER: _ClassVar[int]
    ROUND_COUNT_SUM_FIELD_NUMBER: _ClassVar[int]
    DADIAN_SUM_FIELD_NUMBER: _ClassVar[int]
    ROUND_END_FIELD_NUMBER: _ClassVar[int]
    MING_COUNT_SUM_FIELD_NUMBER: _ClassVar[int]
    LIQI_COUNT_SUM_FIELD_NUMBER: _ClassVar[int]
    XUN_COUNT_SUM_FIELD_NUMBER: _ClassVar[int]
    HIGHEST_LIANZHUANG_FIELD_NUMBER: _ClassVar[int]
    SCORE_EARN_SUM_FIELD_NUMBER: _ClassVar[int]
    RANK_SCORE_FIELD_NUMBER: _ClassVar[int]
    mode: int
    game_count_sum: int
    game_final_position: _containers.RepeatedScalarFieldContainer[int]
    fly_count: int
    gold_earn_sum: float
    round_count_sum: int
    dadian_sum: float
    round_end: _containers.RepeatedCompositeFieldContainer[AccountStatisticByGameMode.RoundEndData]
    ming_count_sum: int
    liqi_count_sum: int
    xun_count_sum: int
    highest_lianzhuang: int
    score_earn_sum: int
    rank_score: _containers.RepeatedCompositeFieldContainer[AccountStatisticByGameMode.RankScore]
    def __init__(self, mode: _Optional[int] = ..., game_count_sum: _Optional[int] = ..., game_final_position: _Optional[_Iterable[int]] = ..., fly_count: _Optional[int] = ..., gold_earn_sum: _Optional[float] = ..., round_count_sum: _Optional[int] = ..., dadian_sum: _Optional[float] = ..., round_end: _Optional[_Iterable[_Union[AccountStatisticByGameMode.RoundEndData, _Mapping]]] = ..., ming_count_sum: _Optional[int] = ..., liqi_count_sum: _Optional[int] = ..., xun_count_sum: _Optional[int] = ..., highest_lianzhuang: _Optional[int] = ..., score_earn_sum: _Optional[int] = ..., rank_score: _Optional[_Iterable[_Union[AccountStatisticByGameMode.RankScore, _Mapping]]] = ...) -> None: ...

class AccountStatisticByFan(_message.Message):
    __slots__ = ["fan_id", "sum"]
    FAN_ID_FIELD_NUMBER: _ClassVar[int]
    SUM_FIELD_NUMBER: _ClassVar[int]
    fan_id: int
    sum: int
    def __init__(self, fan_id: _Optional[int] = ..., sum: _Optional[int] = ...) -> None: ...

class AccountFanAchieved(_message.Message):
    __slots__ = ["mahjong_category", "fan", "liujumanguan"]
    MAHJONG_CATEGORY_FIELD_NUMBER: _ClassVar[int]
    FAN_FIELD_NUMBER: _ClassVar[int]
    LIUJUMANGUAN_FIELD_NUMBER: _ClassVar[int]
    mahjong_category: int
    fan: _containers.RepeatedCompositeFieldContainer[AccountStatisticByFan]
    liujumanguan: int
    def __init__(self, mahjong_category: _Optional[int] = ..., fan: _Optional[_Iterable[_Union[AccountStatisticByFan, _Mapping]]] = ..., liujumanguan: _Optional[int] = ...) -> None: ...

class AccountDetailStatistic(_message.Message):
    __slots__ = ["game_mode", "fan", "liujumanguan", "fan_achieved"]
    GAME_MODE_FIELD_NUMBER: _ClassVar[int]
    FAN_FIELD_NUMBER: _ClassVar[int]
    LIUJUMANGUAN_FIELD_NUMBER: _ClassVar[int]
    FAN_ACHIEVED_FIELD_NUMBER: _ClassVar[int]
    game_mode: _containers.RepeatedCompositeFieldContainer[AccountStatisticByGameMode]
    fan: _containers.RepeatedCompositeFieldContainer[AccountStatisticByFan]
    liujumanguan: int
    fan_achieved: _containers.RepeatedCompositeFieldContainer[AccountFanAchieved]
    def __init__(self, game_mode: _Optional[_Iterable[_Union[AccountStatisticByGameMode, _Mapping]]] = ..., fan: _Optional[_Iterable[_Union[AccountStatisticByFan, _Mapping]]] = ..., liujumanguan: _Optional[int] = ..., fan_achieved: _Optional[_Iterable[_Union[AccountFanAchieved, _Mapping]]] = ...) -> None: ...

class AccountDetailStatisticByCategory(_message.Message):
    __slots__ = ["category", "detail_statistic"]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    DETAIL_STATISTIC_FIELD_NUMBER: _ClassVar[int]
    category: int
    detail_statistic: AccountDetailStatistic
    def __init__(self, category: _Optional[int] = ..., detail_statistic: _Optional[_Union[AccountDetailStatistic, _Mapping]] = ...) -> None: ...

class AccountDetailStatisticV2(_message.Message):
    __slots__ = ["friend_room_statistic", "rank_statistic", "customized_contest_statistic", "leisure_match_statistic", "challenge_match_statistic", "activity_match_statistic", "ab_match_statistic"]
    class RankStatistic(_message.Message):
        __slots__ = ["total_statistic", "month_statistic", "month_refresh_time"]
        class RankData(_message.Message):
            __slots__ = ["all_level_statistic", "level_data_list"]
            class RankLevelData(_message.Message):
                __slots__ = ["rank_level", "statistic"]
                RANK_LEVEL_FIELD_NUMBER: _ClassVar[int]
                STATISTIC_FIELD_NUMBER: _ClassVar[int]
                rank_level: int
                statistic: AccountDetailStatistic
                def __init__(self, rank_level: _Optional[int] = ..., statistic: _Optional[_Union[AccountDetailStatistic, _Mapping]] = ...) -> None: ...
            ALL_LEVEL_STATISTIC_FIELD_NUMBER: _ClassVar[int]
            LEVEL_DATA_LIST_FIELD_NUMBER: _ClassVar[int]
            all_level_statistic: AccountDetailStatistic
            level_data_list: _containers.RepeatedCompositeFieldContainer[AccountDetailStatisticV2.RankStatistic.RankData.RankLevelData]
            def __init__(self, all_level_statistic: _Optional[_Union[AccountDetailStatistic, _Mapping]] = ..., level_data_list: _Optional[_Iterable[_Union[AccountDetailStatisticV2.RankStatistic.RankData.RankLevelData, _Mapping]]] = ...) -> None: ...
        TOTAL_STATISTIC_FIELD_NUMBER: _ClassVar[int]
        MONTH_STATISTIC_FIELD_NUMBER: _ClassVar[int]
        MONTH_REFRESH_TIME_FIELD_NUMBER: _ClassVar[int]
        total_statistic: AccountDetailStatisticV2.RankStatistic.RankData
        month_statistic: AccountDetailStatisticV2.RankStatistic.RankData
        month_refresh_time: int
        def __init__(self, total_statistic: _Optional[_Union[AccountDetailStatisticV2.RankStatistic.RankData, _Mapping]] = ..., month_statistic: _Optional[_Union[AccountDetailStatisticV2.RankStatistic.RankData, _Mapping]] = ..., month_refresh_time: _Optional[int] = ...) -> None: ...
    class CustomizedContestStatistic(_message.Message):
        __slots__ = ["total_statistic", "month_statistic", "month_refresh_time"]
        TOTAL_STATISTIC_FIELD_NUMBER: _ClassVar[int]
        MONTH_STATISTIC_FIELD_NUMBER: _ClassVar[int]
        MONTH_REFRESH_TIME_FIELD_NUMBER: _ClassVar[int]
        total_statistic: AccountDetailStatistic
        month_statistic: AccountDetailStatistic
        month_refresh_time: int
        def __init__(self, total_statistic: _Optional[_Union[AccountDetailStatistic, _Mapping]] = ..., month_statistic: _Optional[_Union[AccountDetailStatistic, _Mapping]] = ..., month_refresh_time: _Optional[int] = ...) -> None: ...
    class ChallengeStatistic(_message.Message):
        __slots__ = ["all_season", "season_data_list"]
        class SeasonData(_message.Message):
            __slots__ = ["season_id", "statistic"]
            SEASON_ID_FIELD_NUMBER: _ClassVar[int]
            STATISTIC_FIELD_NUMBER: _ClassVar[int]
            season_id: int
            statistic: AccountDetailStatistic
            def __init__(self, season_id: _Optional[int] = ..., statistic: _Optional[_Union[AccountDetailStatistic, _Mapping]] = ...) -> None: ...
        ALL_SEASON_FIELD_NUMBER: _ClassVar[int]
        SEASON_DATA_LIST_FIELD_NUMBER: _ClassVar[int]
        all_season: AccountDetailStatistic
        season_data_list: _containers.RepeatedCompositeFieldContainer[AccountDetailStatisticV2.ChallengeStatistic.SeasonData]
        def __init__(self, all_season: _Optional[_Union[AccountDetailStatistic, _Mapping]] = ..., season_data_list: _Optional[_Iterable[_Union[AccountDetailStatisticV2.ChallengeStatistic.SeasonData, _Mapping]]] = ...) -> None: ...
    FRIEND_ROOM_STATISTIC_FIELD_NUMBER: _ClassVar[int]
    RANK_STATISTIC_FIELD_NUMBER: _ClassVar[int]
    CUSTOMIZED_CONTEST_STATISTIC_FIELD_NUMBER: _ClassVar[int]
    LEISURE_MATCH_STATISTIC_FIELD_NUMBER: _ClassVar[int]
    CHALLENGE_MATCH_STATISTIC_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_MATCH_STATISTIC_FIELD_NUMBER: _ClassVar[int]
    AB_MATCH_STATISTIC_FIELD_NUMBER: _ClassVar[int]
    friend_room_statistic: AccountDetailStatistic
    rank_statistic: AccountDetailStatisticV2.RankStatistic
    customized_contest_statistic: AccountDetailStatisticV2.CustomizedContestStatistic
    leisure_match_statistic: AccountDetailStatistic
    challenge_match_statistic: AccountDetailStatisticV2.ChallengeStatistic
    activity_match_statistic: AccountDetailStatistic
    ab_match_statistic: AccountDetailStatistic
    def __init__(self, friend_room_statistic: _Optional[_Union[AccountDetailStatistic, _Mapping]] = ..., rank_statistic: _Optional[_Union[AccountDetailStatisticV2.RankStatistic, _Mapping]] = ..., customized_contest_statistic: _Optional[_Union[AccountDetailStatisticV2.CustomizedContestStatistic, _Mapping]] = ..., leisure_match_statistic: _Optional[_Union[AccountDetailStatistic, _Mapping]] = ..., challenge_match_statistic: _Optional[_Union[AccountDetailStatisticV2.ChallengeStatistic, _Mapping]] = ..., activity_match_statistic: _Optional[_Union[AccountDetailStatistic, _Mapping]] = ..., ab_match_statistic: _Optional[_Union[AccountDetailStatistic, _Mapping]] = ...) -> None: ...

class AccountShiLian(_message.Message):
    __slots__ = ["step", "state"]
    STEP_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    step: int
    state: int
    def __init__(self, step: _Optional[int] = ..., state: _Optional[int] = ...) -> None: ...

class ClientDeviceInfo(_message.Message):
    __slots__ = ["platform", "hardware", "os", "os_version", "is_browser", "software", "sale_platform", "hardware_vendor", "model_number", "screen_width", "screen_height"]
    PLATFORM_FIELD_NUMBER: _ClassVar[int]
    HARDWARE_FIELD_NUMBER: _ClassVar[int]
    OS_FIELD_NUMBER: _ClassVar[int]
    OS_VERSION_FIELD_NUMBER: _ClassVar[int]
    IS_BROWSER_FIELD_NUMBER: _ClassVar[int]
    SOFTWARE_FIELD_NUMBER: _ClassVar[int]
    SALE_PLATFORM_FIELD_NUMBER: _ClassVar[int]
    HARDWARE_VENDOR_FIELD_NUMBER: _ClassVar[int]
    MODEL_NUMBER_FIELD_NUMBER: _ClassVar[int]
    SCREEN_WIDTH_FIELD_NUMBER: _ClassVar[int]
    SCREEN_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    platform: str
    hardware: str
    os: str
    os_version: str
    is_browser: bool
    software: str
    sale_platform: str
    hardware_vendor: str
    model_number: str
    screen_width: int
    screen_height: int
    def __init__(self, platform: _Optional[str] = ..., hardware: _Optional[str] = ..., os: _Optional[str] = ..., os_version: _Optional[str] = ..., is_browser: bool = ..., software: _Optional[str] = ..., sale_platform: _Optional[str] = ..., hardware_vendor: _Optional[str] = ..., model_number: _Optional[str] = ..., screen_width: _Optional[int] = ..., screen_height: _Optional[int] = ...) -> None: ...

class ClientVersionInfo(_message.Message):
    __slots__ = ["resource", "package"]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    PACKAGE_FIELD_NUMBER: _ClassVar[int]
    resource: str
    package: str
    def __init__(self, resource: _Optional[str] = ..., package: _Optional[str] = ...) -> None: ...

class Announcement(_message.Message):
    __slots__ = ["id", "title", "content", "header_image"]
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    HEADER_IMAGE_FIELD_NUMBER: _ClassVar[int]
    id: int
    title: str
    content: str
    header_image: str
    def __init__(self, id: _Optional[int] = ..., title: _Optional[str] = ..., content: _Optional[str] = ..., header_image: _Optional[str] = ...) -> None: ...

class TaskProgress(_message.Message):
    __slots__ = ["id", "counter", "achieved", "rewarded", "failed", "rewarded_time"]
    ID_FIELD_NUMBER: _ClassVar[int]
    COUNTER_FIELD_NUMBER: _ClassVar[int]
    ACHIEVED_FIELD_NUMBER: _ClassVar[int]
    REWARDED_FIELD_NUMBER: _ClassVar[int]
    FAILED_FIELD_NUMBER: _ClassVar[int]
    REWARDED_TIME_FIELD_NUMBER: _ClassVar[int]
    id: int
    counter: int
    achieved: bool
    rewarded: bool
    failed: bool
    rewarded_time: int
    def __init__(self, id: _Optional[int] = ..., counter: _Optional[int] = ..., achieved: bool = ..., rewarded: bool = ..., failed: bool = ..., rewarded_time: _Optional[int] = ...) -> None: ...

class GameConfig(_message.Message):
    __slots__ = ["category", "mode", "meta"]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    META_FIELD_NUMBER: _ClassVar[int]
    category: int
    mode: GameMode
    meta: GameMetaData
    def __init__(self, category: _Optional[int] = ..., mode: _Optional[_Union[GameMode, _Mapping]] = ..., meta: _Optional[_Union[GameMetaData, _Mapping]] = ...) -> None: ...

class RPGState(_message.Message):
    __slots__ = ["player_damaged", "monster_damaged", "monster_seq"]
    PLAYER_DAMAGED_FIELD_NUMBER: _ClassVar[int]
    MONSTER_DAMAGED_FIELD_NUMBER: _ClassVar[int]
    MONSTER_SEQ_FIELD_NUMBER: _ClassVar[int]
    player_damaged: int
    monster_damaged: int
    monster_seq: int
    def __init__(self, player_damaged: _Optional[int] = ..., monster_damaged: _Optional[int] = ..., monster_seq: _Optional[int] = ...) -> None: ...

class RPGActivity(_message.Message):
    __slots__ = ["activity_id", "last_show_uuid", "last_played_uuid", "current_state", "last_show_state", "received_rewards", "last_show_id"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_SHOW_UUID_FIELD_NUMBER: _ClassVar[int]
    LAST_PLAYED_UUID_FIELD_NUMBER: _ClassVar[int]
    CURRENT_STATE_FIELD_NUMBER: _ClassVar[int]
    LAST_SHOW_STATE_FIELD_NUMBER: _ClassVar[int]
    RECEIVED_REWARDS_FIELD_NUMBER: _ClassVar[int]
    LAST_SHOW_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    last_show_uuid: str
    last_played_uuid: str
    current_state: RPGState
    last_show_state: RPGState
    received_rewards: _containers.RepeatedScalarFieldContainer[int]
    last_show_id: int
    def __init__(self, activity_id: _Optional[int] = ..., last_show_uuid: _Optional[str] = ..., last_played_uuid: _Optional[str] = ..., current_state: _Optional[_Union[RPGState, _Mapping]] = ..., last_show_state: _Optional[_Union[RPGState, _Mapping]] = ..., received_rewards: _Optional[_Iterable[int]] = ..., last_show_id: _Optional[int] = ...) -> None: ...

class ActivityArenaData(_message.Message):
    __slots__ = ["win_count", "lose_count", "activity_id", "enter_time", "daily_enter_count", "daily_enter_time", "max_win_count", "total_win_count"]
    WIN_COUNT_FIELD_NUMBER: _ClassVar[int]
    LOSE_COUNT_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    ENTER_TIME_FIELD_NUMBER: _ClassVar[int]
    DAILY_ENTER_COUNT_FIELD_NUMBER: _ClassVar[int]
    DAILY_ENTER_TIME_FIELD_NUMBER: _ClassVar[int]
    MAX_WIN_COUNT_FIELD_NUMBER: _ClassVar[int]
    TOTAL_WIN_COUNT_FIELD_NUMBER: _ClassVar[int]
    win_count: int
    lose_count: int
    activity_id: int
    enter_time: int
    daily_enter_count: int
    daily_enter_time: int
    max_win_count: int
    total_win_count: int
    def __init__(self, win_count: _Optional[int] = ..., lose_count: _Optional[int] = ..., activity_id: _Optional[int] = ..., enter_time: _Optional[int] = ..., daily_enter_count: _Optional[int] = ..., daily_enter_time: _Optional[int] = ..., max_win_count: _Optional[int] = ..., total_win_count: _Optional[int] = ...) -> None: ...

class FeedActivityData(_message.Message):
    __slots__ = ["activity_id", "feed_count", "friend_receive_data", "friend_send_data", "gift_inbox"]
    class CountWithTimeData(_message.Message):
        __slots__ = ["count", "last_update_time"]
        COUNT_FIELD_NUMBER: _ClassVar[int]
        LAST_UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
        count: int
        last_update_time: int
        def __init__(self, count: _Optional[int] = ..., last_update_time: _Optional[int] = ...) -> None: ...
    class GiftBoxData(_message.Message):
        __slots__ = ["id", "item_id", "count", "from_account_id", "time", "received"]
        ID_FIELD_NUMBER: _ClassVar[int]
        ITEM_ID_FIELD_NUMBER: _ClassVar[int]
        COUNT_FIELD_NUMBER: _ClassVar[int]
        FROM_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        TIME_FIELD_NUMBER: _ClassVar[int]
        RECEIVED_FIELD_NUMBER: _ClassVar[int]
        id: int
        item_id: int
        count: int
        from_account_id: int
        time: int
        received: int
        def __init__(self, id: _Optional[int] = ..., item_id: _Optional[int] = ..., count: _Optional[int] = ..., from_account_id: _Optional[int] = ..., time: _Optional[int] = ..., received: _Optional[int] = ...) -> None: ...
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    FEED_COUNT_FIELD_NUMBER: _ClassVar[int]
    FRIEND_RECEIVE_DATA_FIELD_NUMBER: _ClassVar[int]
    FRIEND_SEND_DATA_FIELD_NUMBER: _ClassVar[int]
    GIFT_INBOX_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    feed_count: int
    friend_receive_data: FeedActivityData.CountWithTimeData
    friend_send_data: FeedActivityData.CountWithTimeData
    gift_inbox: _containers.RepeatedCompositeFieldContainer[FeedActivityData.GiftBoxData]
    def __init__(self, activity_id: _Optional[int] = ..., feed_count: _Optional[int] = ..., friend_receive_data: _Optional[_Union[FeedActivityData.CountWithTimeData, _Mapping]] = ..., friend_send_data: _Optional[_Union[FeedActivityData.CountWithTimeData, _Mapping]] = ..., gift_inbox: _Optional[_Iterable[_Union[FeedActivityData.GiftBoxData, _Mapping]]] = ...) -> None: ...

class SegmentTaskProgress(_message.Message):
    __slots__ = ["id", "counter", "achieved", "rewarded", "failed", "reward_count", "achieved_count"]
    ID_FIELD_NUMBER: _ClassVar[int]
    COUNTER_FIELD_NUMBER: _ClassVar[int]
    ACHIEVED_FIELD_NUMBER: _ClassVar[int]
    REWARDED_FIELD_NUMBER: _ClassVar[int]
    FAILED_FIELD_NUMBER: _ClassVar[int]
    REWARD_COUNT_FIELD_NUMBER: _ClassVar[int]
    ACHIEVED_COUNT_FIELD_NUMBER: _ClassVar[int]
    id: int
    counter: int
    achieved: bool
    rewarded: bool
    failed: bool
    reward_count: int
    achieved_count: int
    def __init__(self, id: _Optional[int] = ..., counter: _Optional[int] = ..., achieved: bool = ..., rewarded: bool = ..., failed: bool = ..., reward_count: _Optional[int] = ..., achieved_count: _Optional[int] = ...) -> None: ...

class MineActivityData(_message.Message):
    __slots__ = ["dig_point", "map", "id"]
    DIG_POINT_FIELD_NUMBER: _ClassVar[int]
    MAP_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    dig_point: _containers.RepeatedCompositeFieldContainer[Point]
    map: _containers.RepeatedCompositeFieldContainer[MineReward]
    id: int
    def __init__(self, dig_point: _Optional[_Iterable[_Union[Point, _Mapping]]] = ..., map: _Optional[_Iterable[_Union[MineReward, _Mapping]]] = ..., id: _Optional[int] = ...) -> None: ...

class AccountActivityUpdate(_message.Message):
    __slots__ = ["mine_data", "rpg_data", "feed_data", "spot_data", "friend_gift_data", "upgrade_data", "gacha_data", "simulation_data", "combining_data", "village_data", "festival_data", "island_data", "amulet_data", "story_data"]
    MINE_DATA_FIELD_NUMBER: _ClassVar[int]
    RPG_DATA_FIELD_NUMBER: _ClassVar[int]
    FEED_DATA_FIELD_NUMBER: _ClassVar[int]
    SPOT_DATA_FIELD_NUMBER: _ClassVar[int]
    FRIEND_GIFT_DATA_FIELD_NUMBER: _ClassVar[int]
    UPGRADE_DATA_FIELD_NUMBER: _ClassVar[int]
    GACHA_DATA_FIELD_NUMBER: _ClassVar[int]
    SIMULATION_DATA_FIELD_NUMBER: _ClassVar[int]
    COMBINING_DATA_FIELD_NUMBER: _ClassVar[int]
    VILLAGE_DATA_FIELD_NUMBER: _ClassVar[int]
    FESTIVAL_DATA_FIELD_NUMBER: _ClassVar[int]
    ISLAND_DATA_FIELD_NUMBER: _ClassVar[int]
    AMULET_DATA_FIELD_NUMBER: _ClassVar[int]
    STORY_DATA_FIELD_NUMBER: _ClassVar[int]
    mine_data: _containers.RepeatedCompositeFieldContainer[MineActivityData]
    rpg_data: _containers.RepeatedCompositeFieldContainer[RPGActivity]
    feed_data: _containers.RepeatedCompositeFieldContainer[ActivityFeedData]
    spot_data: _containers.RepeatedCompositeFieldContainer[ActivitySpotData]
    friend_gift_data: _containers.RepeatedCompositeFieldContainer[ActivityFriendGiftData]
    upgrade_data: _containers.RepeatedCompositeFieldContainer[ActivityUpgradeData]
    gacha_data: _containers.RepeatedCompositeFieldContainer[ActivityGachaUpdateData]
    simulation_data: _containers.RepeatedCompositeFieldContainer[ActivitySimulationData]
    combining_data: _containers.RepeatedCompositeFieldContainer[ActivityCombiningLQData]
    village_data: _containers.RepeatedCompositeFieldContainer[ActivityVillageData]
    festival_data: _containers.RepeatedCompositeFieldContainer[ActivityFestivalData]
    island_data: _containers.RepeatedCompositeFieldContainer[ActivityIslandData]
    amulet_data: _containers.RepeatedCompositeFieldContainer[ActivityAmuletData]
    story_data: _containers.RepeatedCompositeFieldContainer[ActivityStoryData]
    def __init__(self, mine_data: _Optional[_Iterable[_Union[MineActivityData, _Mapping]]] = ..., rpg_data: _Optional[_Iterable[_Union[RPGActivity, _Mapping]]] = ..., feed_data: _Optional[_Iterable[_Union[ActivityFeedData, _Mapping]]] = ..., spot_data: _Optional[_Iterable[_Union[ActivitySpotData, _Mapping]]] = ..., friend_gift_data: _Optional[_Iterable[_Union[ActivityFriendGiftData, _Mapping]]] = ..., upgrade_data: _Optional[_Iterable[_Union[ActivityUpgradeData, _Mapping]]] = ..., gacha_data: _Optional[_Iterable[_Union[ActivityGachaUpdateData, _Mapping]]] = ..., simulation_data: _Optional[_Iterable[_Union[ActivitySimulationData, _Mapping]]] = ..., combining_data: _Optional[_Iterable[_Union[ActivityCombiningLQData, _Mapping]]] = ..., village_data: _Optional[_Iterable[_Union[ActivityVillageData, _Mapping]]] = ..., festival_data: _Optional[_Iterable[_Union[ActivityFestivalData, _Mapping]]] = ..., island_data: _Optional[_Iterable[_Union[ActivityIslandData, _Mapping]]] = ..., amulet_data: _Optional[_Iterable[_Union[ActivityAmuletData, _Mapping]]] = ..., story_data: _Optional[_Iterable[_Union[ActivityStoryData, _Mapping]]] = ...) -> None: ...

class ActivityCombiningWorkbench(_message.Message):
    __slots__ = ["craft_id", "pos"]
    CRAFT_ID_FIELD_NUMBER: _ClassVar[int]
    POS_FIELD_NUMBER: _ClassVar[int]
    craft_id: int
    pos: int
    def __init__(self, craft_id: _Optional[int] = ..., pos: _Optional[int] = ...) -> None: ...

class ActivityCombiningMenuData(_message.Message):
    __slots__ = ["menu_group", "generated"]
    class MenuRequire(_message.Message):
        __slots__ = ["level", "count"]
        LEVEL_FIELD_NUMBER: _ClassVar[int]
        COUNT_FIELD_NUMBER: _ClassVar[int]
        level: int
        count: int
        def __init__(self, level: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...
    MENU_GROUP_FIELD_NUMBER: _ClassVar[int]
    GENERATED_FIELD_NUMBER: _ClassVar[int]
    menu_group: int
    generated: _containers.RepeatedCompositeFieldContainer[ActivityCombiningMenuData.MenuRequire]
    def __init__(self, menu_group: _Optional[int] = ..., generated: _Optional[_Iterable[_Union[ActivityCombiningMenuData.MenuRequire, _Mapping]]] = ...) -> None: ...

class ActivityCombiningOrderData(_message.Message):
    __slots__ = ["id", "pos", "craft_id", "unlock_day"]
    ID_FIELD_NUMBER: _ClassVar[int]
    POS_FIELD_NUMBER: _ClassVar[int]
    CRAFT_ID_FIELD_NUMBER: _ClassVar[int]
    UNLOCK_DAY_FIELD_NUMBER: _ClassVar[int]
    id: int
    pos: int
    craft_id: int
    unlock_day: int
    def __init__(self, id: _Optional[int] = ..., pos: _Optional[int] = ..., craft_id: _Optional[int] = ..., unlock_day: _Optional[int] = ...) -> None: ...

class ActivityCombiningLQData(_message.Message):
    __slots__ = ["activity_id", "workbench", "orders", "recycle_bin", "unlocked_craft"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    WORKBENCH_FIELD_NUMBER: _ClassVar[int]
    ORDERS_FIELD_NUMBER: _ClassVar[int]
    RECYCLE_BIN_FIELD_NUMBER: _ClassVar[int]
    UNLOCKED_CRAFT_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    workbench: _containers.RepeatedCompositeFieldContainer[ActivityCombiningWorkbench]
    orders: _containers.RepeatedCompositeFieldContainer[ActivityCombiningOrderData]
    recycle_bin: ActivityCombiningWorkbench
    unlocked_craft: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, activity_id: _Optional[int] = ..., workbench: _Optional[_Iterable[_Union[ActivityCombiningWorkbench, _Mapping]]] = ..., orders: _Optional[_Iterable[_Union[ActivityCombiningOrderData, _Mapping]]] = ..., recycle_bin: _Optional[_Union[ActivityCombiningWorkbench, _Mapping]] = ..., unlocked_craft: _Optional[_Iterable[int]] = ...) -> None: ...

class ActivityCombiningPoolData(_message.Message):
    __slots__ = ["group", "count"]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    group: int
    count: int
    def __init__(self, group: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class ActivityCombiningData(_message.Message):
    __slots__ = ["activity_id", "workbench", "orders", "recycle_bin", "menu", "current_order_id", "bonus", "unlocked_craft", "craft_pool", "order_pool"]
    class BonusData(_message.Message):
        __slots__ = ["count", "update_time"]
        COUNT_FIELD_NUMBER: _ClassVar[int]
        UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
        count: int
        update_time: int
        def __init__(self, count: _Optional[int] = ..., update_time: _Optional[int] = ...) -> None: ...
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    WORKBENCH_FIELD_NUMBER: _ClassVar[int]
    ORDERS_FIELD_NUMBER: _ClassVar[int]
    RECYCLE_BIN_FIELD_NUMBER: _ClassVar[int]
    MENU_FIELD_NUMBER: _ClassVar[int]
    CURRENT_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    BONUS_FIELD_NUMBER: _ClassVar[int]
    UNLOCKED_CRAFT_FIELD_NUMBER: _ClassVar[int]
    CRAFT_POOL_FIELD_NUMBER: _ClassVar[int]
    ORDER_POOL_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    workbench: _containers.RepeatedCompositeFieldContainer[ActivityCombiningWorkbench]
    orders: _containers.RepeatedCompositeFieldContainer[ActivityCombiningOrderData]
    recycle_bin: ActivityCombiningWorkbench
    menu: ActivityCombiningMenuData
    current_order_id: int
    bonus: ActivityCombiningData.BonusData
    unlocked_craft: _containers.RepeatedScalarFieldContainer[int]
    craft_pool: _containers.RepeatedCompositeFieldContainer[ActivityCombiningPoolData]
    order_pool: _containers.RepeatedCompositeFieldContainer[ActivityCombiningPoolData]
    def __init__(self, activity_id: _Optional[int] = ..., workbench: _Optional[_Iterable[_Union[ActivityCombiningWorkbench, _Mapping]]] = ..., orders: _Optional[_Iterable[_Union[ActivityCombiningOrderData, _Mapping]]] = ..., recycle_bin: _Optional[_Union[ActivityCombiningWorkbench, _Mapping]] = ..., menu: _Optional[_Union[ActivityCombiningMenuData, _Mapping]] = ..., current_order_id: _Optional[int] = ..., bonus: _Optional[_Union[ActivityCombiningData.BonusData, _Mapping]] = ..., unlocked_craft: _Optional[_Iterable[int]] = ..., craft_pool: _Optional[_Iterable[_Union[ActivityCombiningPoolData, _Mapping]]] = ..., order_pool: _Optional[_Iterable[_Union[ActivityCombiningPoolData, _Mapping]]] = ...) -> None: ...

class VillageReward(_message.Message):
    __slots__ = ["id", "count"]
    ID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    id: int
    count: int
    def __init__(self, id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class VillageBuildingData(_message.Message):
    __slots__ = ["id", "reward", "workers"]
    ID_FIELD_NUMBER: _ClassVar[int]
    REWARD_FIELD_NUMBER: _ClassVar[int]
    WORKERS_FIELD_NUMBER: _ClassVar[int]
    id: int
    reward: _containers.RepeatedCompositeFieldContainer[VillageReward]
    workers: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, id: _Optional[int] = ..., reward: _Optional[_Iterable[_Union[VillageReward, _Mapping]]] = ..., workers: _Optional[_Iterable[int]] = ...) -> None: ...

class VillageTripData(_message.Message):
    __slots__ = ["start_round", "dest_id", "reward", "level", "info"]
    START_ROUND_FIELD_NUMBER: _ClassVar[int]
    DEST_ID_FIELD_NUMBER: _ClassVar[int]
    REWARD_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    start_round: int
    dest_id: int
    reward: _containers.RepeatedCompositeFieldContainer[VillageReward]
    level: int
    info: VillageTargetInfo
    def __init__(self, start_round: _Optional[int] = ..., dest_id: _Optional[int] = ..., reward: _Optional[_Iterable[_Union[VillageReward, _Mapping]]] = ..., level: _Optional[int] = ..., info: _Optional[_Union[VillageTargetInfo, _Mapping]] = ...) -> None: ...

class VillageTaskData(_message.Message):
    __slots__ = ["id", "completed_count"]
    ID_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_COUNT_FIELD_NUMBER: _ClassVar[int]
    id: int
    completed_count: int
    def __init__(self, id: _Optional[int] = ..., completed_count: _Optional[int] = ...) -> None: ...

class VillageTargetInfo(_message.Message):
    __slots__ = ["nickname", "avatar", "avatar_frame", "title", "verified"]
    NICKNAME_FIELD_NUMBER: _ClassVar[int]
    AVATAR_FIELD_NUMBER: _ClassVar[int]
    AVATAR_FRAME_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    VERIFIED_FIELD_NUMBER: _ClassVar[int]
    nickname: str
    avatar: int
    avatar_frame: int
    title: int
    verified: int
    def __init__(self, nickname: _Optional[str] = ..., avatar: _Optional[int] = ..., avatar_frame: _Optional[int] = ..., title: _Optional[int] = ..., verified: _Optional[int] = ...) -> None: ...

class ActivityVillageData(_message.Message):
    __slots__ = ["activity_id", "buildings", "trip", "tasks", "round"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    BUILDINGS_FIELD_NUMBER: _ClassVar[int]
    TRIP_FIELD_NUMBER: _ClassVar[int]
    TASKS_FIELD_NUMBER: _ClassVar[int]
    ROUND_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    buildings: _containers.RepeatedCompositeFieldContainer[VillageBuildingData]
    trip: _containers.RepeatedCompositeFieldContainer[VillageTripData]
    tasks: _containers.RepeatedCompositeFieldContainer[VillageTaskData]
    round: int
    def __init__(self, activity_id: _Optional[int] = ..., buildings: _Optional[_Iterable[_Union[VillageBuildingData, _Mapping]]] = ..., trip: _Optional[_Iterable[_Union[VillageTripData, _Mapping]]] = ..., tasks: _Optional[_Iterable[_Union[VillageTaskData, _Mapping]]] = ..., round: _Optional[int] = ...) -> None: ...

class TimeCounterData(_message.Message):
    __slots__ = ["count", "update_time"]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    count: int
    update_time: int
    def __init__(self, count: _Optional[int] = ..., update_time: _Optional[int] = ...) -> None: ...

class SignedTimeCounterData(_message.Message):
    __slots__ = ["count", "update_time"]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    count: int
    update_time: int
    def __init__(self, count: _Optional[int] = ..., update_time: _Optional[int] = ...) -> None: ...

class FestivalProposalData(_message.Message):
    __slots__ = ["id", "proposal_id", "pos"]
    ID_FIELD_NUMBER: _ClassVar[int]
    PROPOSAL_ID_FIELD_NUMBER: _ClassVar[int]
    POS_FIELD_NUMBER: _ClassVar[int]
    id: int
    proposal_id: int
    pos: int
    def __init__(self, id: _Optional[int] = ..., proposal_id: _Optional[int] = ..., pos: _Optional[int] = ...) -> None: ...

class ActivityFestivalData(_message.Message):
    __slots__ = ["activity_id", "level", "proposal_list", "event_list", "buy_record"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    PROPOSAL_LIST_FIELD_NUMBER: _ClassVar[int]
    EVENT_LIST_FIELD_NUMBER: _ClassVar[int]
    BUY_RECORD_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    level: int
    proposal_list: _containers.RepeatedCompositeFieldContainer[FestivalProposalData]
    event_list: _containers.RepeatedScalarFieldContainer[int]
    buy_record: SignedTimeCounterData
    def __init__(self, activity_id: _Optional[int] = ..., level: _Optional[int] = ..., proposal_list: _Optional[_Iterable[_Union[FestivalProposalData, _Mapping]]] = ..., event_list: _Optional[_Iterable[int]] = ..., buy_record: _Optional[_Union[SignedTimeCounterData, _Mapping]] = ...) -> None: ...

class IslandBagItemData(_message.Message):
    __slots__ = ["id", "pos", "rotate", "goods_id", "price"]
    ID_FIELD_NUMBER: _ClassVar[int]
    POS_FIELD_NUMBER: _ClassVar[int]
    ROTATE_FIELD_NUMBER: _ClassVar[int]
    GOODS_ID_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    id: int
    pos: _containers.RepeatedScalarFieldContainer[int]
    rotate: int
    goods_id: int
    price: int
    def __init__(self, id: _Optional[int] = ..., pos: _Optional[_Iterable[int]] = ..., rotate: _Optional[int] = ..., goods_id: _Optional[int] = ..., price: _Optional[int] = ...) -> None: ...

class IslandBagData(_message.Message):
    __slots__ = ["id", "matrix", "items"]
    ID_FIELD_NUMBER: _ClassVar[int]
    MATRIX_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    id: int
    matrix: str
    items: _containers.RepeatedCompositeFieldContainer[IslandBagItemData]
    def __init__(self, id: _Optional[int] = ..., matrix: _Optional[str] = ..., items: _Optional[_Iterable[_Union[IslandBagItemData, _Mapping]]] = ...) -> None: ...

class IslandGoodsData(_message.Message):
    __slots__ = ["goods_id", "count", "update_time"]
    GOODS_ID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    goods_id: int
    count: int
    update_time: int
    def __init__(self, goods_id: _Optional[int] = ..., count: _Optional[int] = ..., update_time: _Optional[int] = ...) -> None: ...

class IslandZoneData(_message.Message):
    __slots__ = ["id", "currency_used", "goods_records"]
    ID_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_USED_FIELD_NUMBER: _ClassVar[int]
    GOODS_RECORDS_FIELD_NUMBER: _ClassVar[int]
    id: int
    currency_used: SignedTimeCounterData
    goods_records: _containers.RepeatedCompositeFieldContainer[IslandGoodsData]
    def __init__(self, id: _Optional[int] = ..., currency_used: _Optional[_Union[SignedTimeCounterData, _Mapping]] = ..., goods_records: _Optional[_Iterable[_Union[IslandGoodsData, _Mapping]]] = ...) -> None: ...

class ActivityIslandData(_message.Message):
    __slots__ = ["activity_id", "zone", "bags", "zones"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    ZONE_FIELD_NUMBER: _ClassVar[int]
    BAGS_FIELD_NUMBER: _ClassVar[int]
    ZONES_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    zone: int
    bags: _containers.RepeatedCompositeFieldContainer[IslandBagData]
    zones: _containers.RepeatedCompositeFieldContainer[IslandZoneData]
    def __init__(self, activity_id: _Optional[int] = ..., zone: _Optional[int] = ..., bags: _Optional[_Iterable[_Union[IslandBagData, _Mapping]]] = ..., zones: _Optional[_Iterable[_Union[IslandZoneData, _Mapping]]] = ...) -> None: ...

class AmuletEffectData(_message.Message):
    __slots__ = ["id", "uid", "store"]
    ID_FIELD_NUMBER: _ClassVar[int]
    UID_FIELD_NUMBER: _ClassVar[int]
    STORE_FIELD_NUMBER: _ClassVar[int]
    id: int
    uid: int
    store: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, id: _Optional[int] = ..., uid: _Optional[int] = ..., store: _Optional[_Iterable[int]] = ...) -> None: ...

class AmuletBuffData(_message.Message):
    __slots__ = ["id", "store"]
    ID_FIELD_NUMBER: _ClassVar[int]
    STORE_FIELD_NUMBER: _ClassVar[int]
    id: int
    store: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, id: _Optional[int] = ..., store: _Optional[_Iterable[int]] = ...) -> None: ...

class AmuletGameShopGoods(_message.Message):
    __slots__ = ["id", "sold", "goods_id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    SOLD_FIELD_NUMBER: _ClassVar[int]
    GOODS_ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    sold: bool
    goods_id: int
    def __init__(self, id: _Optional[int] = ..., sold: bool = ..., goods_id: _Optional[int] = ...) -> None: ...

class AmuletActivityTingInfo(_message.Message):
    __slots__ = ["tile", "fan", "ting_tile"]
    TILE_FIELD_NUMBER: _ClassVar[int]
    FAN_FIELD_NUMBER: _ClassVar[int]
    TING_TILE_FIELD_NUMBER: _ClassVar[int]
    tile: str
    fan: int
    ting_tile: str
    def __init__(self, tile: _Optional[str] = ..., fan: _Optional[int] = ..., ting_tile: _Optional[str] = ...) -> None: ...

class AmuletShowDesktopTileData(_message.Message):
    __slots__ = ["id", "pos"]
    ID_FIELD_NUMBER: _ClassVar[int]
    POS_FIELD_NUMBER: _ClassVar[int]
    id: int
    pos: int
    def __init__(self, id: _Optional[int] = ..., pos: _Optional[int] = ...) -> None: ...

class AmuletGameOperation(_message.Message):
    __slots__ = ["type", "gang", "effect_id"]
    class GangTiles(_message.Message):
        __slots__ = ["tiles"]
        TILES_FIELD_NUMBER: _ClassVar[int]
        tiles: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, tiles: _Optional[_Iterable[int]] = ...) -> None: ...
    TYPE_FIELD_NUMBER: _ClassVar[int]
    GANG_FIELD_NUMBER: _ClassVar[int]
    EFFECT_ID_FIELD_NUMBER: _ClassVar[int]
    type: int
    gang: _containers.RepeatedCompositeFieldContainer[AmuletGameOperation.GangTiles]
    effect_id: int
    def __init__(self, type: _Optional[int] = ..., gang: _Optional[_Iterable[_Union[AmuletGameOperation.GangTiles, _Mapping]]] = ..., effect_id: _Optional[int] = ...) -> None: ...

class AmuletGameShopData(_message.Message):
    __slots__ = ["goods", "effect_list", "shop_refresh_count", "refresh_price"]
    GOODS_FIELD_NUMBER: _ClassVar[int]
    EFFECT_LIST_FIELD_NUMBER: _ClassVar[int]
    SHOP_REFRESH_COUNT_FIELD_NUMBER: _ClassVar[int]
    REFRESH_PRICE_FIELD_NUMBER: _ClassVar[int]
    goods: _containers.RepeatedCompositeFieldContainer[AmuletGameShopGoods]
    effect_list: _containers.RepeatedScalarFieldContainer[int]
    shop_refresh_count: int
    refresh_price: int
    def __init__(self, goods: _Optional[_Iterable[_Union[AmuletGameShopGoods, _Mapping]]] = ..., effect_list: _Optional[_Iterable[int]] = ..., shop_refresh_count: _Optional[int] = ..., refresh_price: _Optional[int] = ...) -> None: ...

class AmuletGameUpdateData(_message.Message):
    __slots__ = ["tile_replace", "tian_dora", "dora", "hands", "ming", "effect_list", "buff_list", "point", "coin", "stage", "desktop_remain", "show_desktop_tiles", "ting_list", "next_operation", "used_desktop", "highest_hu", "records"]
    TILE_REPLACE_FIELD_NUMBER: _ClassVar[int]
    TIAN_DORA_FIELD_NUMBER: _ClassVar[int]
    DORA_FIELD_NUMBER: _ClassVar[int]
    HANDS_FIELD_NUMBER: _ClassVar[int]
    MING_FIELD_NUMBER: _ClassVar[int]
    EFFECT_LIST_FIELD_NUMBER: _ClassVar[int]
    BUFF_LIST_FIELD_NUMBER: _ClassVar[int]
    POINT_FIELD_NUMBER: _ClassVar[int]
    COIN_FIELD_NUMBER: _ClassVar[int]
    STAGE_FIELD_NUMBER: _ClassVar[int]
    DESKTOP_REMAIN_FIELD_NUMBER: _ClassVar[int]
    SHOW_DESKTOP_TILES_FIELD_NUMBER: _ClassVar[int]
    TING_LIST_FIELD_NUMBER: _ClassVar[int]
    NEXT_OPERATION_FIELD_NUMBER: _ClassVar[int]
    USED_DESKTOP_FIELD_NUMBER: _ClassVar[int]
    HIGHEST_HU_FIELD_NUMBER: _ClassVar[int]
    RECORDS_FIELD_NUMBER: _ClassVar[int]
    tile_replace: _containers.RepeatedCompositeFieldContainer[AmuletTile]
    tian_dora: _containers.RepeatedScalarFieldContainer[str]
    dora: _containers.RepeatedScalarFieldContainer[int]
    hands: _containers.RepeatedScalarFieldContainer[int]
    ming: _containers.RepeatedCompositeFieldContainer[AmuletMingInfo]
    effect_list: _containers.RepeatedCompositeFieldContainer[AmuletEffectData]
    buff_list: _containers.RepeatedCompositeFieldContainer[AmuletEffectData]
    point: str
    coin: int
    stage: int
    desktop_remain: int
    show_desktop_tiles: _containers.RepeatedCompositeFieldContainer[AmuletShowDesktopTileData]
    ting_list: _containers.RepeatedCompositeFieldContainer[AmuletActivityTingInfo]
    next_operation: _containers.RepeatedCompositeFieldContainer[AmuletGameOperation]
    used_desktop: _containers.RepeatedScalarFieldContainer[int]
    highest_hu: ActivityAmuletHuRecord
    records: ActivityAmuletRecord
    def __init__(self, tile_replace: _Optional[_Iterable[_Union[AmuletTile, _Mapping]]] = ..., tian_dora: _Optional[_Iterable[str]] = ..., dora: _Optional[_Iterable[int]] = ..., hands: _Optional[_Iterable[int]] = ..., ming: _Optional[_Iterable[_Union[AmuletMingInfo, _Mapping]]] = ..., effect_list: _Optional[_Iterable[_Union[AmuletEffectData, _Mapping]]] = ..., buff_list: _Optional[_Iterable[_Union[AmuletEffectData, _Mapping]]] = ..., point: _Optional[str] = ..., coin: _Optional[int] = ..., stage: _Optional[int] = ..., desktop_remain: _Optional[int] = ..., show_desktop_tiles: _Optional[_Iterable[_Union[AmuletShowDesktopTileData, _Mapping]]] = ..., ting_list: _Optional[_Iterable[_Union[AmuletActivityTingInfo, _Mapping]]] = ..., next_operation: _Optional[_Iterable[_Union[AmuletGameOperation, _Mapping]]] = ..., used_desktop: _Optional[_Iterable[int]] = ..., highest_hu: _Optional[_Union[ActivityAmuletHuRecord, _Mapping]] = ..., records: _Optional[_Union[ActivityAmuletRecord, _Mapping]] = ...) -> None: ...

class AmuletGameRecordData(_message.Message):
    __slots__ = ["key", "int_value", "str_value", "int_arr_value"]
    KEY_FIELD_NUMBER: _ClassVar[int]
    INT_VALUE_FIELD_NUMBER: _ClassVar[int]
    STR_VALUE_FIELD_NUMBER: _ClassVar[int]
    INT_ARR_VALUE_FIELD_NUMBER: _ClassVar[int]
    key: int
    int_value: int
    str_value: str
    int_arr_value: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, key: _Optional[int] = ..., int_value: _Optional[int] = ..., str_value: _Optional[str] = ..., int_arr_value: _Optional[_Iterable[int]] = ...) -> None: ...

class AmuletGameData(_message.Message):
    __slots__ = ["pool", "tile_replace", "tian_dora", "mountain", "dora", "hands", "ming", "effect_list", "buff_list", "level", "point", "coin", "shop", "used", "boss_buff", "stage", "desktop", "show_desktop", "desktop_remain", "free_effect_list", "show_desktop_tiles", "change_tile_count", "ting_list", "next_operation", "shop_buff_list", "remain_change_tile_count", "used_desktop", "after_gang", "record_data", "skill_buff_list", "max_effect_count", "highest_hu", "total_consumed_coin", "boss_buff_id"]
    POOL_FIELD_NUMBER: _ClassVar[int]
    TILE_REPLACE_FIELD_NUMBER: _ClassVar[int]
    TIAN_DORA_FIELD_NUMBER: _ClassVar[int]
    MOUNTAIN_FIELD_NUMBER: _ClassVar[int]
    DORA_FIELD_NUMBER: _ClassVar[int]
    HANDS_FIELD_NUMBER: _ClassVar[int]
    MING_FIELD_NUMBER: _ClassVar[int]
    EFFECT_LIST_FIELD_NUMBER: _ClassVar[int]
    BUFF_LIST_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    POINT_FIELD_NUMBER: _ClassVar[int]
    COIN_FIELD_NUMBER: _ClassVar[int]
    SHOP_FIELD_NUMBER: _ClassVar[int]
    USED_FIELD_NUMBER: _ClassVar[int]
    BOSS_BUFF_FIELD_NUMBER: _ClassVar[int]
    STAGE_FIELD_NUMBER: _ClassVar[int]
    DESKTOP_FIELD_NUMBER: _ClassVar[int]
    SHOW_DESKTOP_FIELD_NUMBER: _ClassVar[int]
    DESKTOP_REMAIN_FIELD_NUMBER: _ClassVar[int]
    FREE_EFFECT_LIST_FIELD_NUMBER: _ClassVar[int]
    SHOW_DESKTOP_TILES_FIELD_NUMBER: _ClassVar[int]
    CHANGE_TILE_COUNT_FIELD_NUMBER: _ClassVar[int]
    TING_LIST_FIELD_NUMBER: _ClassVar[int]
    NEXT_OPERATION_FIELD_NUMBER: _ClassVar[int]
    SHOP_BUFF_LIST_FIELD_NUMBER: _ClassVar[int]
    REMAIN_CHANGE_TILE_COUNT_FIELD_NUMBER: _ClassVar[int]
    USED_DESKTOP_FIELD_NUMBER: _ClassVar[int]
    AFTER_GANG_FIELD_NUMBER: _ClassVar[int]
    RECORD_DATA_FIELD_NUMBER: _ClassVar[int]
    SKILL_BUFF_LIST_FIELD_NUMBER: _ClassVar[int]
    MAX_EFFECT_COUNT_FIELD_NUMBER: _ClassVar[int]
    HIGHEST_HU_FIELD_NUMBER: _ClassVar[int]
    TOTAL_CONSUMED_COIN_FIELD_NUMBER: _ClassVar[int]
    BOSS_BUFF_ID_FIELD_NUMBER: _ClassVar[int]
    pool: _containers.RepeatedCompositeFieldContainer[AmuletTile]
    tile_replace: _containers.RepeatedCompositeFieldContainer[AmuletTile]
    tian_dora: _containers.RepeatedScalarFieldContainer[str]
    mountain: _containers.RepeatedScalarFieldContainer[int]
    dora: _containers.RepeatedScalarFieldContainer[int]
    hands: _containers.RepeatedScalarFieldContainer[int]
    ming: _containers.RepeatedCompositeFieldContainer[AmuletMingInfo]
    effect_list: _containers.RepeatedCompositeFieldContainer[AmuletEffectData]
    buff_list: _containers.RepeatedCompositeFieldContainer[AmuletBuffData]
    level: int
    point: str
    coin: int
    shop: AmuletGameShopData
    used: _containers.RepeatedScalarFieldContainer[int]
    boss_buff: _containers.RepeatedScalarFieldContainer[int]
    stage: int
    desktop: _containers.RepeatedScalarFieldContainer[int]
    show_desktop: _containers.RepeatedScalarFieldContainer[int]
    desktop_remain: int
    free_effect_list: _containers.RepeatedScalarFieldContainer[int]
    show_desktop_tiles: _containers.RepeatedCompositeFieldContainer[AmuletShowDesktopTileData]
    change_tile_count: int
    ting_list: _containers.RepeatedCompositeFieldContainer[AmuletActivityTingInfo]
    next_operation: _containers.RepeatedCompositeFieldContainer[AmuletGameOperation]
    shop_buff_list: _containers.RepeatedCompositeFieldContainer[AmuletBuffData]
    remain_change_tile_count: int
    used_desktop: _containers.RepeatedScalarFieldContainer[int]
    after_gang: int
    record_data: _containers.RepeatedCompositeFieldContainer[AmuletGameRecordData]
    skill_buff_list: _containers.RepeatedCompositeFieldContainer[AmuletBuffData]
    max_effect_count: int
    highest_hu: ActivityAmuletHuRecord
    total_consumed_coin: int
    boss_buff_id: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, pool: _Optional[_Iterable[_Union[AmuletTile, _Mapping]]] = ..., tile_replace: _Optional[_Iterable[_Union[AmuletTile, _Mapping]]] = ..., tian_dora: _Optional[_Iterable[str]] = ..., mountain: _Optional[_Iterable[int]] = ..., dora: _Optional[_Iterable[int]] = ..., hands: _Optional[_Iterable[int]] = ..., ming: _Optional[_Iterable[_Union[AmuletMingInfo, _Mapping]]] = ..., effect_list: _Optional[_Iterable[_Union[AmuletEffectData, _Mapping]]] = ..., buff_list: _Optional[_Iterable[_Union[AmuletBuffData, _Mapping]]] = ..., level: _Optional[int] = ..., point: _Optional[str] = ..., coin: _Optional[int] = ..., shop: _Optional[_Union[AmuletGameShopData, _Mapping]] = ..., used: _Optional[_Iterable[int]] = ..., boss_buff: _Optional[_Iterable[int]] = ..., stage: _Optional[int] = ..., desktop: _Optional[_Iterable[int]] = ..., show_desktop: _Optional[_Iterable[int]] = ..., desktop_remain: _Optional[int] = ..., free_effect_list: _Optional[_Iterable[int]] = ..., show_desktop_tiles: _Optional[_Iterable[_Union[AmuletShowDesktopTileData, _Mapping]]] = ..., change_tile_count: _Optional[int] = ..., ting_list: _Optional[_Iterable[_Union[AmuletActivityTingInfo, _Mapping]]] = ..., next_operation: _Optional[_Iterable[_Union[AmuletGameOperation, _Mapping]]] = ..., shop_buff_list: _Optional[_Iterable[_Union[AmuletBuffData, _Mapping]]] = ..., remain_change_tile_count: _Optional[int] = ..., used_desktop: _Optional[_Iterable[int]] = ..., after_gang: _Optional[int] = ..., record_data: _Optional[_Iterable[_Union[AmuletGameRecordData, _Mapping]]] = ..., skill_buff_list: _Optional[_Iterable[_Union[AmuletBuffData, _Mapping]]] = ..., max_effect_count: _Optional[int] = ..., highest_hu: _Optional[_Union[ActivityAmuletHuRecord, _Mapping]] = ..., total_consumed_coin: _Optional[int] = ..., boss_buff_id: _Optional[_Iterable[int]] = ...) -> None: ...

class ActivityAmuletUpdateData(_message.Message):
    __slots__ = ["activity_id", "game_update", "game_empty"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    GAME_UPDATE_FIELD_NUMBER: _ClassVar[int]
    GAME_EMPTY_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    game_update: AmuletGameUpdateData
    game_empty: bool
    def __init__(self, activity_id: _Optional[int] = ..., game_update: _Optional[_Union[AmuletGameUpdateData, _Mapping]] = ..., game_empty: bool = ...) -> None: ...

class AmuletSkillData(_message.Message):
    __slots__ = ["id", "level"]
    ID_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    id: int
    level: int
    def __init__(self, id: _Optional[int] = ..., level: _Optional[int] = ...) -> None: ...

class ActivityAmuletUpgradeData(_message.Message):
    __slots__ = ["skill"]
    SKILL_FIELD_NUMBER: _ClassVar[int]
    skill: _containers.RepeatedCompositeFieldContainer[AmuletSkillData]
    def __init__(self, skill: _Optional[_Iterable[_Union[AmuletSkillData, _Mapping]]] = ...) -> None: ...

class ActivityAmuletRecord(_message.Message):
    __slots__ = ["effect_gain_count", "hu_count"]
    EFFECT_GAIN_COUNT_FIELD_NUMBER: _ClassVar[int]
    HU_COUNT_FIELD_NUMBER: _ClassVar[int]
    effect_gain_count: int
    hu_count: int
    def __init__(self, effect_gain_count: _Optional[int] = ..., hu_count: _Optional[int] = ...) -> None: ...

class ActivityAmuletHuRecord(_message.Message):
    __slots__ = ["point", "pai", "fan", "base"]
    POINT_FIELD_NUMBER: _ClassVar[int]
    PAI_FIELD_NUMBER: _ClassVar[int]
    FAN_FIELD_NUMBER: _ClassVar[int]
    BASE_FIELD_NUMBER: _ClassVar[int]
    point: str
    pai: str
    fan: int
    base: int
    def __init__(self, point: _Optional[str] = ..., pai: _Optional[str] = ..., fan: _Optional[int] = ..., base: _Optional[int] = ...) -> None: ...

class ActivityAmuletIllustratedBookData(_message.Message):
    __slots__ = ["effect_collection", "highest_hu", "highest_level"]
    EFFECT_COLLECTION_FIELD_NUMBER: _ClassVar[int]
    HIGHEST_HU_FIELD_NUMBER: _ClassVar[int]
    HIGHEST_LEVEL_FIELD_NUMBER: _ClassVar[int]
    effect_collection: _containers.RepeatedScalarFieldContainer[int]
    highest_hu: ActivityAmuletHuRecord
    highest_level: int
    def __init__(self, effect_collection: _Optional[_Iterable[int]] = ..., highest_hu: _Optional[_Union[ActivityAmuletHuRecord, _Mapping]] = ..., highest_level: _Optional[int] = ...) -> None: ...

class ActivityAmuletData(_message.Message):
    __slots__ = ["activity_id", "game", "version", "upgrade", "illustrated_book"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    GAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    UPGRADE_FIELD_NUMBER: _ClassVar[int]
    ILLUSTRATED_BOOK_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    game: AmuletGameData
    version: int
    upgrade: ActivityAmuletUpgradeData
    illustrated_book: ActivityAmuletIllustratedBookData
    def __init__(self, activity_id: _Optional[int] = ..., game: _Optional[_Union[AmuletGameData, _Mapping]] = ..., version: _Optional[int] = ..., upgrade: _Optional[_Union[ActivityAmuletUpgradeData, _Mapping]] = ..., illustrated_book: _Optional[_Union[ActivityAmuletIllustratedBookData, _Mapping]] = ...) -> None: ...

class ActivityFeedData(_message.Message):
    __slots__ = ["activity_id", "feed_count", "friend_receive_data", "friend_send_data", "gift_inbox", "max_inbox_id"]
    class CountWithTimeData(_message.Message):
        __slots__ = ["count", "last_update_time"]
        COUNT_FIELD_NUMBER: _ClassVar[int]
        LAST_UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
        count: int
        last_update_time: int
        def __init__(self, count: _Optional[int] = ..., last_update_time: _Optional[int] = ...) -> None: ...
    class GiftBoxData(_message.Message):
        __slots__ = ["id", "item_id", "count", "from_account_id", "time", "received"]
        ID_FIELD_NUMBER: _ClassVar[int]
        ITEM_ID_FIELD_NUMBER: _ClassVar[int]
        COUNT_FIELD_NUMBER: _ClassVar[int]
        FROM_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        TIME_FIELD_NUMBER: _ClassVar[int]
        RECEIVED_FIELD_NUMBER: _ClassVar[int]
        id: int
        item_id: int
        count: int
        from_account_id: int
        time: int
        received: int
        def __init__(self, id: _Optional[int] = ..., item_id: _Optional[int] = ..., count: _Optional[int] = ..., from_account_id: _Optional[int] = ..., time: _Optional[int] = ..., received: _Optional[int] = ...) -> None: ...
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    FEED_COUNT_FIELD_NUMBER: _ClassVar[int]
    FRIEND_RECEIVE_DATA_FIELD_NUMBER: _ClassVar[int]
    FRIEND_SEND_DATA_FIELD_NUMBER: _ClassVar[int]
    GIFT_INBOX_FIELD_NUMBER: _ClassVar[int]
    MAX_INBOX_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    feed_count: int
    friend_receive_data: ActivityFeedData.CountWithTimeData
    friend_send_data: ActivityFeedData.CountWithTimeData
    gift_inbox: _containers.RepeatedCompositeFieldContainer[ActivityFeedData.GiftBoxData]
    max_inbox_id: int
    def __init__(self, activity_id: _Optional[int] = ..., feed_count: _Optional[int] = ..., friend_receive_data: _Optional[_Union[ActivityFeedData.CountWithTimeData, _Mapping]] = ..., friend_send_data: _Optional[_Union[ActivityFeedData.CountWithTimeData, _Mapping]] = ..., gift_inbox: _Optional[_Iterable[_Union[ActivityFeedData.GiftBoxData, _Mapping]]] = ..., max_inbox_id: _Optional[int] = ...) -> None: ...

class UnlockedStoryData(_message.Message):
    __slots__ = ["story_id", "finished_ending", "rewarded_ending", "finish_rewarded", "all_finish_rewarded"]
    STORY_ID_FIELD_NUMBER: _ClassVar[int]
    FINISHED_ENDING_FIELD_NUMBER: _ClassVar[int]
    REWARDED_ENDING_FIELD_NUMBER: _ClassVar[int]
    FINISH_REWARDED_FIELD_NUMBER: _ClassVar[int]
    ALL_FINISH_REWARDED_FIELD_NUMBER: _ClassVar[int]
    story_id: int
    finished_ending: _containers.RepeatedScalarFieldContainer[int]
    rewarded_ending: _containers.RepeatedScalarFieldContainer[int]
    finish_rewarded: int
    all_finish_rewarded: int
    def __init__(self, story_id: _Optional[int] = ..., finished_ending: _Optional[_Iterable[int]] = ..., rewarded_ending: _Optional[_Iterable[int]] = ..., finish_rewarded: _Optional[int] = ..., all_finish_rewarded: _Optional[int] = ...) -> None: ...

class ActivityStoryData(_message.Message):
    __slots__ = ["activity_id", "unlocked_story"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    UNLOCKED_STORY_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    unlocked_story: _containers.RepeatedCompositeFieldContainer[UnlockedStoryData]
    def __init__(self, activity_id: _Optional[int] = ..., unlocked_story: _Optional[_Iterable[_Union[UnlockedStoryData, _Mapping]]] = ...) -> None: ...

class ActivityFriendGiftData(_message.Message):
    __slots__ = ["activity_id", "max_inbox_id", "receive_data", "send_data", "gift_inbox"]
    class CountWithTimeData(_message.Message):
        __slots__ = ["count", "last_update_time", "send_friend_id"]
        COUNT_FIELD_NUMBER: _ClassVar[int]
        LAST_UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
        SEND_FRIEND_ID_FIELD_NUMBER: _ClassVar[int]
        count: int
        last_update_time: int
        send_friend_id: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, count: _Optional[int] = ..., last_update_time: _Optional[int] = ..., send_friend_id: _Optional[_Iterable[int]] = ...) -> None: ...
    class GiftBoxData(_message.Message):
        __slots__ = ["id", "item_id", "count", "from_account_id", "time", "received"]
        ID_FIELD_NUMBER: _ClassVar[int]
        ITEM_ID_FIELD_NUMBER: _ClassVar[int]
        COUNT_FIELD_NUMBER: _ClassVar[int]
        FROM_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        TIME_FIELD_NUMBER: _ClassVar[int]
        RECEIVED_FIELD_NUMBER: _ClassVar[int]
        id: int
        item_id: int
        count: int
        from_account_id: int
        time: int
        received: int
        def __init__(self, id: _Optional[int] = ..., item_id: _Optional[int] = ..., count: _Optional[int] = ..., from_account_id: _Optional[int] = ..., time: _Optional[int] = ..., received: _Optional[int] = ...) -> None: ...
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    MAX_INBOX_ID_FIELD_NUMBER: _ClassVar[int]
    RECEIVE_DATA_FIELD_NUMBER: _ClassVar[int]
    SEND_DATA_FIELD_NUMBER: _ClassVar[int]
    GIFT_INBOX_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    max_inbox_id: int
    receive_data: ActivityFriendGiftData.CountWithTimeData
    send_data: ActivityFriendGiftData.CountWithTimeData
    gift_inbox: _containers.RepeatedCompositeFieldContainer[ActivityFriendGiftData.GiftBoxData]
    def __init__(self, activity_id: _Optional[int] = ..., max_inbox_id: _Optional[int] = ..., receive_data: _Optional[_Union[ActivityFriendGiftData.CountWithTimeData, _Mapping]] = ..., send_data: _Optional[_Union[ActivityFriendGiftData.CountWithTimeData, _Mapping]] = ..., gift_inbox: _Optional[_Iterable[_Union[ActivityFriendGiftData.GiftBoxData, _Mapping]]] = ...) -> None: ...

class ActivityUpgradeData(_message.Message):
    __slots__ = ["activity_id", "groups", "received_level"]
    class LevelGroup(_message.Message):
        __slots__ = ["group_id", "level"]
        GROUP_ID_FIELD_NUMBER: _ClassVar[int]
        LEVEL_FIELD_NUMBER: _ClassVar[int]
        group_id: int
        level: int
        def __init__(self, group_id: _Optional[int] = ..., level: _Optional[int] = ...) -> None: ...
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    RECEIVED_LEVEL_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    groups: _containers.RepeatedCompositeFieldContainer[ActivityUpgradeData.LevelGroup]
    received_level: int
    def __init__(self, activity_id: _Optional[int] = ..., groups: _Optional[_Iterable[_Union[ActivityUpgradeData.LevelGroup, _Mapping]]] = ..., received_level: _Optional[int] = ...) -> None: ...

class GachaRecord(_message.Message):
    __slots__ = ["id", "count"]
    ID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    id: int
    count: int
    def __init__(self, id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class ActivityGachaData(_message.Message):
    __slots__ = ["activity_id", "gained"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    GAINED_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    gained: _containers.RepeatedCompositeFieldContainer[GachaRecord]
    def __init__(self, activity_id: _Optional[int] = ..., gained: _Optional[_Iterable[_Union[GachaRecord, _Mapping]]] = ...) -> None: ...

class ActivityGachaUpdateData(_message.Message):
    __slots__ = ["activity_id", "gained", "remain_count"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    GAINED_FIELD_NUMBER: _ClassVar[int]
    REMAIN_COUNT_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    gained: _containers.RepeatedCompositeFieldContainer[GachaRecord]
    remain_count: int
    def __init__(self, activity_id: _Optional[int] = ..., gained: _Optional[_Iterable[_Union[GachaRecord, _Mapping]]] = ..., remain_count: _Optional[int] = ...) -> None: ...

class ActivitySimulationGameRecordMessage(_message.Message):
    __slots__ = ["type", "args", "xun"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    XUN_FIELD_NUMBER: _ClassVar[int]
    type: int
    args: _containers.RepeatedScalarFieldContainer[int]
    xun: int
    def __init__(self, type: _Optional[int] = ..., args: _Optional[_Iterable[int]] = ..., xun: _Optional[int] = ...) -> None: ...

class ActivitySimulationGameRecord(_message.Message):
    __slots__ = ["round", "seats", "uuid", "start_time", "scores", "messages"]
    ROUND_FIELD_NUMBER: _ClassVar[int]
    SEATS_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    SCORES_FIELD_NUMBER: _ClassVar[int]
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    round: int
    seats: _containers.RepeatedScalarFieldContainer[int]
    uuid: str
    start_time: int
    scores: _containers.RepeatedScalarFieldContainer[int]
    messages: _containers.RepeatedCompositeFieldContainer[ActivitySimulationGameRecordMessage]
    def __init__(self, round: _Optional[int] = ..., seats: _Optional[_Iterable[int]] = ..., uuid: _Optional[str] = ..., start_time: _Optional[int] = ..., scores: _Optional[_Iterable[int]] = ..., messages: _Optional[_Iterable[_Union[ActivitySimulationGameRecordMessage, _Mapping]]] = ...) -> None: ...

class ActivitySimulationDailyContest(_message.Message):
    __slots__ = ["day", "characters", "records", "round"]
    DAY_FIELD_NUMBER: _ClassVar[int]
    CHARACTERS_FIELD_NUMBER: _ClassVar[int]
    RECORDS_FIELD_NUMBER: _ClassVar[int]
    ROUND_FIELD_NUMBER: _ClassVar[int]
    day: int
    characters: _containers.RepeatedScalarFieldContainer[int]
    records: _containers.RepeatedCompositeFieldContainer[ActivitySimulationGameRecord]
    round: int
    def __init__(self, day: _Optional[int] = ..., characters: _Optional[_Iterable[int]] = ..., records: _Optional[_Iterable[_Union[ActivitySimulationGameRecord, _Mapping]]] = ..., round: _Optional[int] = ...) -> None: ...

class ActivitySimulationTrainRecord(_message.Message):
    __slots__ = ["time", "modify_stats", "final_stats", "type"]
    TIME_FIELD_NUMBER: _ClassVar[int]
    MODIFY_STATS_FIELD_NUMBER: _ClassVar[int]
    FINAL_STATS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    time: int
    modify_stats: _containers.RepeatedScalarFieldContainer[int]
    final_stats: _containers.RepeatedScalarFieldContainer[int]
    type: int
    def __init__(self, time: _Optional[int] = ..., modify_stats: _Optional[_Iterable[int]] = ..., final_stats: _Optional[_Iterable[int]] = ..., type: _Optional[int] = ...) -> None: ...

class ActivitySimulationData(_message.Message):
    __slots__ = ["activity_id", "stats", "stamina_update_time", "daily_contest", "train_records"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    STATS_FIELD_NUMBER: _ClassVar[int]
    STAMINA_UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    DAILY_CONTEST_FIELD_NUMBER: _ClassVar[int]
    TRAIN_RECORDS_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    stats: _containers.RepeatedScalarFieldContainer[int]
    stamina_update_time: int
    daily_contest: _containers.RepeatedCompositeFieldContainer[ActivitySimulationDailyContest]
    train_records: _containers.RepeatedCompositeFieldContainer[ActivitySimulationTrainRecord]
    def __init__(self, activity_id: _Optional[int] = ..., stats: _Optional[_Iterable[int]] = ..., stamina_update_time: _Optional[int] = ..., daily_contest: _Optional[_Iterable[_Union[ActivitySimulationDailyContest, _Mapping]]] = ..., train_records: _Optional[_Iterable[_Union[ActivitySimulationTrainRecord, _Mapping]]] = ...) -> None: ...

class ActivitySpotData(_message.Message):
    __slots__ = ["activity_id", "spots"]
    class SpotData(_message.Message):
        __slots__ = ["unique_id", "rewarded", "unlocked_ending", "unlocked"]
        UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
        REWARDED_FIELD_NUMBER: _ClassVar[int]
        UNLOCKED_ENDING_FIELD_NUMBER: _ClassVar[int]
        UNLOCKED_FIELD_NUMBER: _ClassVar[int]
        unique_id: int
        rewarded: int
        unlocked_ending: _containers.RepeatedScalarFieldContainer[int]
        unlocked: int
        def __init__(self, unique_id: _Optional[int] = ..., rewarded: _Optional[int] = ..., unlocked_ending: _Optional[_Iterable[int]] = ..., unlocked: _Optional[int] = ...) -> None: ...
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    SPOTS_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    spots: _containers.RepeatedCompositeFieldContainer[ActivitySpotData.SpotData]
    def __init__(self, activity_id: _Optional[int] = ..., spots: _Optional[_Iterable[_Union[ActivitySpotData.SpotData, _Mapping]]] = ...) -> None: ...

class AccountActiveState(_message.Message):
    __slots__ = ["account_id", "login_time", "logout_time", "is_online", "playing"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    LOGIN_TIME_FIELD_NUMBER: _ClassVar[int]
    LOGOUT_TIME_FIELD_NUMBER: _ClassVar[int]
    IS_ONLINE_FIELD_NUMBER: _ClassVar[int]
    PLAYING_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    login_time: int
    logout_time: int
    is_online: bool
    playing: AccountPlayingGame
    def __init__(self, account_id: _Optional[int] = ..., login_time: _Optional[int] = ..., logout_time: _Optional[int] = ..., is_online: bool = ..., playing: _Optional[_Union[AccountPlayingGame, _Mapping]] = ...) -> None: ...

class Friend(_message.Message):
    __slots__ = ["base", "state"]
    BASE_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    base: PlayerBaseView
    state: AccountActiveState
    def __init__(self, base: _Optional[_Union[PlayerBaseView, _Mapping]] = ..., state: _Optional[_Union[AccountActiveState, _Mapping]] = ...) -> None: ...

class Point(_message.Message):
    __slots__ = ["x", "y"]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    x: int
    y: int
    def __init__(self, x: _Optional[int] = ..., y: _Optional[int] = ...) -> None: ...

class MineReward(_message.Message):
    __slots__ = ["point", "reward_id", "received"]
    POINT_FIELD_NUMBER: _ClassVar[int]
    REWARD_ID_FIELD_NUMBER: _ClassVar[int]
    RECEIVED_FIELD_NUMBER: _ClassVar[int]
    point: Point
    reward_id: int
    received: bool
    def __init__(self, point: _Optional[_Union[Point, _Mapping]] = ..., reward_id: _Optional[int] = ..., received: bool = ...) -> None: ...

class GameLiveUnit(_message.Message):
    __slots__ = ["timestamp", "action_category", "action_data"]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    ACTION_CATEGORY_FIELD_NUMBER: _ClassVar[int]
    ACTION_DATA_FIELD_NUMBER: _ClassVar[int]
    timestamp: int
    action_category: int
    action_data: bytes
    def __init__(self, timestamp: _Optional[int] = ..., action_category: _Optional[int] = ..., action_data: _Optional[bytes] = ...) -> None: ...

class GameLiveSegment(_message.Message):
    __slots__ = ["actions"]
    ACTIONS_FIELD_NUMBER: _ClassVar[int]
    actions: _containers.RepeatedCompositeFieldContainer[GameLiveUnit]
    def __init__(self, actions: _Optional[_Iterable[_Union[GameLiveUnit, _Mapping]]] = ...) -> None: ...

class GameLiveSegmentUri(_message.Message):
    __slots__ = ["segment_id", "segment_uri"]
    SEGMENT_ID_FIELD_NUMBER: _ClassVar[int]
    SEGMENT_URI_FIELD_NUMBER: _ClassVar[int]
    segment_id: int
    segment_uri: str
    def __init__(self, segment_id: _Optional[int] = ..., segment_uri: _Optional[str] = ...) -> None: ...

class GameLiveHead(_message.Message):
    __slots__ = ["uuid", "start_time", "game_config", "players", "seat_list"]
    UUID_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    GAME_CONFIG_FIELD_NUMBER: _ClassVar[int]
    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    SEAT_LIST_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    start_time: int
    game_config: GameConfig
    players: _containers.RepeatedCompositeFieldContainer[PlayerGameView]
    seat_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, uuid: _Optional[str] = ..., start_time: _Optional[int] = ..., game_config: _Optional[_Union[GameConfig, _Mapping]] = ..., players: _Optional[_Iterable[_Union[PlayerGameView, _Mapping]]] = ..., seat_list: _Optional[_Iterable[int]] = ...) -> None: ...

class GameNewRoundState(_message.Message):
    __slots__ = ["seat_states"]
    SEAT_STATES_FIELD_NUMBER: _ClassVar[int]
    seat_states: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, seat_states: _Optional[_Iterable[int]] = ...) -> None: ...

class GameEndAction(_message.Message):
    __slots__ = ["state"]
    STATE_FIELD_NUMBER: _ClassVar[int]
    state: int
    def __init__(self, state: _Optional[int] = ...) -> None: ...

class GameNoopAction(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class CommentItem(_message.Message):
    __slots__ = ["comment_id", "timestamp", "commenter", "content", "is_banned"]
    COMMENT_ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    COMMENTER_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    IS_BANNED_FIELD_NUMBER: _ClassVar[int]
    comment_id: int
    timestamp: int
    commenter: PlayerBaseView
    content: str
    is_banned: int
    def __init__(self, comment_id: _Optional[int] = ..., timestamp: _Optional[int] = ..., commenter: _Optional[_Union[PlayerBaseView, _Mapping]] = ..., content: _Optional[str] = ..., is_banned: _Optional[int] = ...) -> None: ...

class RollingNotice(_message.Message):
    __slots__ = ["content", "start_time", "end_time", "repeat_interval", "repeat_time", "repeat_type"]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    REPEAT_INTERVAL_FIELD_NUMBER: _ClassVar[int]
    REPEAT_TIME_FIELD_NUMBER: _ClassVar[int]
    REPEAT_TYPE_FIELD_NUMBER: _ClassVar[int]
    content: str
    start_time: int
    end_time: int
    repeat_interval: int
    repeat_time: _containers.RepeatedScalarFieldContainer[int]
    repeat_type: int
    def __init__(self, content: _Optional[str] = ..., start_time: _Optional[int] = ..., end_time: _Optional[int] = ..., repeat_interval: _Optional[int] = ..., repeat_time: _Optional[_Iterable[int]] = ..., repeat_type: _Optional[int] = ...) -> None: ...

class MaintainNotice(_message.Message):
    __slots__ = ["maintain_time"]
    MAINTAIN_TIME_FIELD_NUMBER: _ClassVar[int]
    maintain_time: int
    def __init__(self, maintain_time: _Optional[int] = ...) -> None: ...

class BillingGoods(_message.Message):
    __slots__ = ["id", "name", "desc", "icon", "resource_id", "resource_count"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESC_FIELD_NUMBER: _ClassVar[int]
    ICON_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_COUNT_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    desc: str
    icon: str
    resource_id: int
    resource_count: int
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., desc: _Optional[str] = ..., icon: _Optional[str] = ..., resource_id: _Optional[int] = ..., resource_count: _Optional[int] = ...) -> None: ...

class BillShortcut(_message.Message):
    __slots__ = ["id", "count", "dealPrice"]
    ID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    DEALPRICE_FIELD_NUMBER: _ClassVar[int]
    id: int
    count: int
    dealPrice: int
    def __init__(self, id: _Optional[int] = ..., count: _Optional[int] = ..., dealPrice: _Optional[int] = ...) -> None: ...

class BillingProduct(_message.Message):
    __slots__ = ["goods", "currency_code", "currency_price", "sort_weight"]
    GOODS_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_CODE_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_PRICE_FIELD_NUMBER: _ClassVar[int]
    SORT_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    goods: BillingGoods
    currency_code: str
    currency_price: int
    sort_weight: int
    def __init__(self, goods: _Optional[_Union[BillingGoods, _Mapping]] = ..., currency_code: _Optional[str] = ..., currency_price: _Optional[int] = ..., sort_weight: _Optional[int] = ...) -> None: ...

class Character(_message.Message):
    __slots__ = ["charid", "level", "exp", "views", "skin", "is_upgraded", "extra_emoji", "rewarded_level"]
    CHARID_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    EXP_FIELD_NUMBER: _ClassVar[int]
    VIEWS_FIELD_NUMBER: _ClassVar[int]
    SKIN_FIELD_NUMBER: _ClassVar[int]
    IS_UPGRADED_FIELD_NUMBER: _ClassVar[int]
    EXTRA_EMOJI_FIELD_NUMBER: _ClassVar[int]
    REWARDED_LEVEL_FIELD_NUMBER: _ClassVar[int]
    charid: int
    level: int
    exp: int
    views: _containers.RepeatedCompositeFieldContainer[ViewSlot]
    skin: int
    is_upgraded: bool
    extra_emoji: _containers.RepeatedScalarFieldContainer[int]
    rewarded_level: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, charid: _Optional[int] = ..., level: _Optional[int] = ..., exp: _Optional[int] = ..., views: _Optional[_Iterable[_Union[ViewSlot, _Mapping]]] = ..., skin: _Optional[int] = ..., is_upgraded: bool = ..., extra_emoji: _Optional[_Iterable[int]] = ..., rewarded_level: _Optional[_Iterable[int]] = ...) -> None: ...

class BuyRecord(_message.Message):
    __slots__ = ["id", "count"]
    ID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    id: int
    count: int
    def __init__(self, id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class ZHPShop(_message.Message):
    __slots__ = ["goods", "buy_records", "free_refresh", "cost_refresh"]
    class RefreshCount(_message.Message):
        __slots__ = ["count", "limit"]
        COUNT_FIELD_NUMBER: _ClassVar[int]
        LIMIT_FIELD_NUMBER: _ClassVar[int]
        count: int
        limit: int
        def __init__(self, count: _Optional[int] = ..., limit: _Optional[int] = ...) -> None: ...
    GOODS_FIELD_NUMBER: _ClassVar[int]
    BUY_RECORDS_FIELD_NUMBER: _ClassVar[int]
    FREE_REFRESH_FIELD_NUMBER: _ClassVar[int]
    COST_REFRESH_FIELD_NUMBER: _ClassVar[int]
    goods: _containers.RepeatedScalarFieldContainer[int]
    buy_records: _containers.RepeatedCompositeFieldContainer[BuyRecord]
    free_refresh: ZHPShop.RefreshCount
    cost_refresh: ZHPShop.RefreshCount
    def __init__(self, goods: _Optional[_Iterable[int]] = ..., buy_records: _Optional[_Iterable[_Union[BuyRecord, _Mapping]]] = ..., free_refresh: _Optional[_Union[ZHPShop.RefreshCount, _Mapping]] = ..., cost_refresh: _Optional[_Union[ZHPShop.RefreshCount, _Mapping]] = ...) -> None: ...

class MonthTicketInfo(_message.Message):
    __slots__ = ["id", "end_time", "last_pay_time"]
    ID_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    LAST_PAY_TIME_FIELD_NUMBER: _ClassVar[int]
    id: int
    end_time: int
    last_pay_time: int
    def __init__(self, id: _Optional[int] = ..., end_time: _Optional[int] = ..., last_pay_time: _Optional[int] = ...) -> None: ...

class ShopInfo(_message.Message):
    __slots__ = ["zhp", "buy_records", "last_refresh_time"]
    ZHP_FIELD_NUMBER: _ClassVar[int]
    BUY_RECORDS_FIELD_NUMBER: _ClassVar[int]
    LAST_REFRESH_TIME_FIELD_NUMBER: _ClassVar[int]
    zhp: ZHPShop
    buy_records: _containers.RepeatedCompositeFieldContainer[BuyRecord]
    last_refresh_time: int
    def __init__(self, zhp: _Optional[_Union[ZHPShop, _Mapping]] = ..., buy_records: _Optional[_Iterable[_Union[BuyRecord, _Mapping]]] = ..., last_refresh_time: _Optional[int] = ...) -> None: ...

class ChangeNicknameRecord(_message.Message):
    __slots__ = ["to", "time"]
    FROM_FIELD_NUMBER: _ClassVar[int]
    TO_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    to: str
    time: int
    def __init__(self, to: _Optional[str] = ..., time: _Optional[int] = ..., **kwargs) -> None: ...

class ServerSettings(_message.Message):
    __slots__ = ["payment_setting", "payment_setting_v2", "nickname_setting"]
    PAYMENT_SETTING_FIELD_NUMBER: _ClassVar[int]
    PAYMENT_SETTING_V2_FIELD_NUMBER: _ClassVar[int]
    NICKNAME_SETTING_FIELD_NUMBER: _ClassVar[int]
    payment_setting: PaymentSetting
    payment_setting_v2: PaymentSettingV2
    nickname_setting: NicknameSetting
    def __init__(self, payment_setting: _Optional[_Union[PaymentSetting, _Mapping]] = ..., payment_setting_v2: _Optional[_Union[PaymentSettingV2, _Mapping]] = ..., nickname_setting: _Optional[_Union[NicknameSetting, _Mapping]] = ...) -> None: ...

class NicknameSetting(_message.Message):
    __slots__ = ["enable", "nicknames"]
    ENABLE_FIELD_NUMBER: _ClassVar[int]
    NICKNAMES_FIELD_NUMBER: _ClassVar[int]
    enable: int
    nicknames: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, enable: _Optional[int] = ..., nicknames: _Optional[_Iterable[str]] = ...) -> None: ...

class PaymentSettingV2(_message.Message):
    __slots__ = ["open_payment", "payment_platforms"]
    class PaymentMaintain(_message.Message):
        __slots__ = ["start_time", "end_time", "goods_click_action", "goods_click_text", "enabled_channel"]
        START_TIME_FIELD_NUMBER: _ClassVar[int]
        END_TIME_FIELD_NUMBER: _ClassVar[int]
        GOODS_CLICK_ACTION_FIELD_NUMBER: _ClassVar[int]
        GOODS_CLICK_TEXT_FIELD_NUMBER: _ClassVar[int]
        ENABLED_CHANNEL_FIELD_NUMBER: _ClassVar[int]
        start_time: int
        end_time: int
        goods_click_action: int
        goods_click_text: str
        enabled_channel: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, start_time: _Optional[int] = ..., end_time: _Optional[int] = ..., goods_click_action: _Optional[int] = ..., goods_click_text: _Optional[str] = ..., enabled_channel: _Optional[_Iterable[str]] = ...) -> None: ...
    class PaymentSettingUnit(_message.Message):
        __slots__ = ["platform", "is_show", "goods_click_action", "goods_click_text", "maintain", "enable_for_frozen_account", "extra_data", "enabled_channel"]
        PLATFORM_FIELD_NUMBER: _ClassVar[int]
        IS_SHOW_FIELD_NUMBER: _ClassVar[int]
        GOODS_CLICK_ACTION_FIELD_NUMBER: _ClassVar[int]
        GOODS_CLICK_TEXT_FIELD_NUMBER: _ClassVar[int]
        MAINTAIN_FIELD_NUMBER: _ClassVar[int]
        ENABLE_FOR_FROZEN_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
        EXTRA_DATA_FIELD_NUMBER: _ClassVar[int]
        ENABLED_CHANNEL_FIELD_NUMBER: _ClassVar[int]
        platform: str
        is_show: bool
        goods_click_action: int
        goods_click_text: str
        maintain: PaymentSettingV2.PaymentMaintain
        enable_for_frozen_account: bool
        extra_data: str
        enabled_channel: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, platform: _Optional[str] = ..., is_show: bool = ..., goods_click_action: _Optional[int] = ..., goods_click_text: _Optional[str] = ..., maintain: _Optional[_Union[PaymentSettingV2.PaymentMaintain, _Mapping]] = ..., enable_for_frozen_account: bool = ..., extra_data: _Optional[str] = ..., enabled_channel: _Optional[_Iterable[str]] = ...) -> None: ...
    OPEN_PAYMENT_FIELD_NUMBER: _ClassVar[int]
    PAYMENT_PLATFORMS_FIELD_NUMBER: _ClassVar[int]
    open_payment: int
    payment_platforms: _containers.RepeatedCompositeFieldContainer[PaymentSettingV2.PaymentSettingUnit]
    def __init__(self, open_payment: _Optional[int] = ..., payment_platforms: _Optional[_Iterable[_Union[PaymentSettingV2.PaymentSettingUnit, _Mapping]]] = ...) -> None: ...

class PaymentSetting(_message.Message):
    __slots__ = ["open_payment", "payment_info_show_type", "payment_info", "wechat", "alipay"]
    class WechatData(_message.Message):
        __slots__ = ["disable_create", "payment_source_platform", "enable_credit"]
        DISABLE_CREATE_FIELD_NUMBER: _ClassVar[int]
        PAYMENT_SOURCE_PLATFORM_FIELD_NUMBER: _ClassVar[int]
        ENABLE_CREDIT_FIELD_NUMBER: _ClassVar[int]
        disable_create: bool
        payment_source_platform: int
        enable_credit: bool
        def __init__(self, disable_create: bool = ..., payment_source_platform: _Optional[int] = ..., enable_credit: bool = ...) -> None: ...
    class AlipayData(_message.Message):
        __slots__ = ["disable_create", "payment_source_platform"]
        DISABLE_CREATE_FIELD_NUMBER: _ClassVar[int]
        PAYMENT_SOURCE_PLATFORM_FIELD_NUMBER: _ClassVar[int]
        disable_create: bool
        payment_source_platform: int
        def __init__(self, disable_create: bool = ..., payment_source_platform: _Optional[int] = ...) -> None: ...
    OPEN_PAYMENT_FIELD_NUMBER: _ClassVar[int]
    PAYMENT_INFO_SHOW_TYPE_FIELD_NUMBER: _ClassVar[int]
    PAYMENT_INFO_FIELD_NUMBER: _ClassVar[int]
    WECHAT_FIELD_NUMBER: _ClassVar[int]
    ALIPAY_FIELD_NUMBER: _ClassVar[int]
    open_payment: int
    payment_info_show_type: int
    payment_info: str
    wechat: PaymentSetting.WechatData
    alipay: PaymentSetting.AlipayData
    def __init__(self, open_payment: _Optional[int] = ..., payment_info_show_type: _Optional[int] = ..., payment_info: _Optional[str] = ..., wechat: _Optional[_Union[PaymentSetting.WechatData, _Mapping]] = ..., alipay: _Optional[_Union[PaymentSetting.AlipayData, _Mapping]] = ...) -> None: ...

class AccountSetting(_message.Message):
    __slots__ = ["key", "value"]
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: int
    value: int
    def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...

class ChestData(_message.Message):
    __slots__ = ["chest_id", "total_open_count", "consume_count", "face_black_count"]
    CHEST_ID_FIELD_NUMBER: _ClassVar[int]
    TOTAL_OPEN_COUNT_FIELD_NUMBER: _ClassVar[int]
    CONSUME_COUNT_FIELD_NUMBER: _ClassVar[int]
    FACE_BLACK_COUNT_FIELD_NUMBER: _ClassVar[int]
    chest_id: int
    total_open_count: int
    consume_count: int
    face_black_count: int
    def __init__(self, chest_id: _Optional[int] = ..., total_open_count: _Optional[int] = ..., consume_count: _Optional[int] = ..., face_black_count: _Optional[int] = ...) -> None: ...

class ChestDataV2(_message.Message):
    __slots__ = ["chest_id", "total_open_count", "face_black_count", "ticket_face_black_count"]
    CHEST_ID_FIELD_NUMBER: _ClassVar[int]
    TOTAL_OPEN_COUNT_FIELD_NUMBER: _ClassVar[int]
    FACE_BLACK_COUNT_FIELD_NUMBER: _ClassVar[int]
    TICKET_FACE_BLACK_COUNT_FIELD_NUMBER: _ClassVar[int]
    chest_id: int
    total_open_count: int
    face_black_count: int
    ticket_face_black_count: int
    def __init__(self, chest_id: _Optional[int] = ..., total_open_count: _Optional[int] = ..., face_black_count: _Optional[int] = ..., ticket_face_black_count: _Optional[int] = ...) -> None: ...

class FaithData(_message.Message):
    __slots__ = ["faith_id", "total_open_count", "consume_count", "modify_count"]
    FAITH_ID_FIELD_NUMBER: _ClassVar[int]
    TOTAL_OPEN_COUNT_FIELD_NUMBER: _ClassVar[int]
    CONSUME_COUNT_FIELD_NUMBER: _ClassVar[int]
    MODIFY_COUNT_FIELD_NUMBER: _ClassVar[int]
    faith_id: int
    total_open_count: int
    consume_count: int
    modify_count: int
    def __init__(self, faith_id: _Optional[int] = ..., total_open_count: _Optional[int] = ..., consume_count: _Optional[int] = ..., modify_count: _Optional[int] = ...) -> None: ...

class CustomizedContestBase(_message.Message):
    __slots__ = ["unique_id", "contest_id", "contest_name", "state", "creator_id", "create_time", "start_time", "finish_time", "open", "contest_type", "public_notice", "check_state", "checking_name"]
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    CONTEST_ID_FIELD_NUMBER: _ClassVar[int]
    CONTEST_NAME_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    CREATOR_ID_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    FINISH_TIME_FIELD_NUMBER: _ClassVar[int]
    OPEN_FIELD_NUMBER: _ClassVar[int]
    CONTEST_TYPE_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_NOTICE_FIELD_NUMBER: _ClassVar[int]
    CHECK_STATE_FIELD_NUMBER: _ClassVar[int]
    CHECKING_NAME_FIELD_NUMBER: _ClassVar[int]
    unique_id: int
    contest_id: int
    contest_name: str
    state: int
    creator_id: int
    create_time: int
    start_time: int
    finish_time: int
    open: bool
    contest_type: int
    public_notice: str
    check_state: int
    checking_name: str
    def __init__(self, unique_id: _Optional[int] = ..., contest_id: _Optional[int] = ..., contest_name: _Optional[str] = ..., state: _Optional[int] = ..., creator_id: _Optional[int] = ..., create_time: _Optional[int] = ..., start_time: _Optional[int] = ..., finish_time: _Optional[int] = ..., open: bool = ..., contest_type: _Optional[int] = ..., public_notice: _Optional[str] = ..., check_state: _Optional[int] = ..., checking_name: _Optional[str] = ...) -> None: ...

class CustomizedContestExtend(_message.Message):
    __slots__ = ["unique_id", "public_notice"]
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_NOTICE_FIELD_NUMBER: _ClassVar[int]
    unique_id: int
    public_notice: str
    def __init__(self, unique_id: _Optional[int] = ..., public_notice: _Optional[str] = ...) -> None: ...

class CustomizedContestAbstract(_message.Message):
    __slots__ = ["unique_id", "contest_id", "contest_name", "state", "creator_id", "create_time", "start_time", "finish_time", "open", "public_notice", "contest_type"]
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    CONTEST_ID_FIELD_NUMBER: _ClassVar[int]
    CONTEST_NAME_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    CREATOR_ID_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    FINISH_TIME_FIELD_NUMBER: _ClassVar[int]
    OPEN_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_NOTICE_FIELD_NUMBER: _ClassVar[int]
    CONTEST_TYPE_FIELD_NUMBER: _ClassVar[int]
    unique_id: int
    contest_id: int
    contest_name: str
    state: int
    creator_id: int
    create_time: int
    start_time: int
    finish_time: int
    open: bool
    public_notice: str
    contest_type: int
    def __init__(self, unique_id: _Optional[int] = ..., contest_id: _Optional[int] = ..., contest_name: _Optional[str] = ..., state: _Optional[int] = ..., creator_id: _Optional[int] = ..., create_time: _Optional[int] = ..., start_time: _Optional[int] = ..., finish_time: _Optional[int] = ..., open: bool = ..., public_notice: _Optional[str] = ..., contest_type: _Optional[int] = ...) -> None: ...

class CustomizedContestDetail(_message.Message):
    __slots__ = ["unique_id", "contest_id", "contest_name", "state", "creator_id", "create_time", "start_time", "finish_time", "open", "rank_rule", "game_mode", "private_notice", "observer_switch", "emoji_switch", "contest_type", "disable_broadcast", "signup_start_time", "signup_end_time", "signup_type", "auto_match"]
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    CONTEST_ID_FIELD_NUMBER: _ClassVar[int]
    CONTEST_NAME_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    CREATOR_ID_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    FINISH_TIME_FIELD_NUMBER: _ClassVar[int]
    OPEN_FIELD_NUMBER: _ClassVar[int]
    RANK_RULE_FIELD_NUMBER: _ClassVar[int]
    GAME_MODE_FIELD_NUMBER: _ClassVar[int]
    PRIVATE_NOTICE_FIELD_NUMBER: _ClassVar[int]
    OBSERVER_SWITCH_FIELD_NUMBER: _ClassVar[int]
    EMOJI_SWITCH_FIELD_NUMBER: _ClassVar[int]
    CONTEST_TYPE_FIELD_NUMBER: _ClassVar[int]
    DISABLE_BROADCAST_FIELD_NUMBER: _ClassVar[int]
    SIGNUP_START_TIME_FIELD_NUMBER: _ClassVar[int]
    SIGNUP_END_TIME_FIELD_NUMBER: _ClassVar[int]
    SIGNUP_TYPE_FIELD_NUMBER: _ClassVar[int]
    AUTO_MATCH_FIELD_NUMBER: _ClassVar[int]
    unique_id: int
    contest_id: int
    contest_name: str
    state: int
    creator_id: int
    create_time: int
    start_time: int
    finish_time: int
    open: bool
    rank_rule: int
    game_mode: GameMode
    private_notice: str
    observer_switch: int
    emoji_switch: int
    contest_type: int
    disable_broadcast: int
    signup_start_time: int
    signup_end_time: int
    signup_type: int
    auto_match: int
    def __init__(self, unique_id: _Optional[int] = ..., contest_id: _Optional[int] = ..., contest_name: _Optional[str] = ..., state: _Optional[int] = ..., creator_id: _Optional[int] = ..., create_time: _Optional[int] = ..., start_time: _Optional[int] = ..., finish_time: _Optional[int] = ..., open: bool = ..., rank_rule: _Optional[int] = ..., game_mode: _Optional[_Union[GameMode, _Mapping]] = ..., private_notice: _Optional[str] = ..., observer_switch: _Optional[int] = ..., emoji_switch: _Optional[int] = ..., contest_type: _Optional[int] = ..., disable_broadcast: _Optional[int] = ..., signup_start_time: _Optional[int] = ..., signup_end_time: _Optional[int] = ..., signup_type: _Optional[int] = ..., auto_match: _Optional[int] = ...) -> None: ...

class CustomizedContestPlayerReport(_message.Message):
    __slots__ = ["rank_rule", "rank", "point", "game_ranks", "total_game_count"]
    RANK_RULE_FIELD_NUMBER: _ClassVar[int]
    RANK_FIELD_NUMBER: _ClassVar[int]
    POINT_FIELD_NUMBER: _ClassVar[int]
    GAME_RANKS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_GAME_COUNT_FIELD_NUMBER: _ClassVar[int]
    rank_rule: int
    rank: int
    point: int
    game_ranks: _containers.RepeatedScalarFieldContainer[int]
    total_game_count: int
    def __init__(self, rank_rule: _Optional[int] = ..., rank: _Optional[int] = ..., point: _Optional[int] = ..., game_ranks: _Optional[_Iterable[int]] = ..., total_game_count: _Optional[int] = ...) -> None: ...

class RecordGame(_message.Message):
    __slots__ = ["uuid", "start_time", "end_time", "config", "accounts", "result"]
    class AccountInfo(_message.Message):
        __slots__ = ["account_id", "seat", "nickname", "avatar_id", "character", "title", "level", "level3", "avatar_frame", "verified", "views"]
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        SEAT_FIELD_NUMBER: _ClassVar[int]
        NICKNAME_FIELD_NUMBER: _ClassVar[int]
        AVATAR_ID_FIELD_NUMBER: _ClassVar[int]
        CHARACTER_FIELD_NUMBER: _ClassVar[int]
        TITLE_FIELD_NUMBER: _ClassVar[int]
        LEVEL_FIELD_NUMBER: _ClassVar[int]
        LEVEL3_FIELD_NUMBER: _ClassVar[int]
        AVATAR_FRAME_FIELD_NUMBER: _ClassVar[int]
        VERIFIED_FIELD_NUMBER: _ClassVar[int]
        VIEWS_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        seat: int
        nickname: str
        avatar_id: int
        character: Character
        title: int
        level: AccountLevel
        level3: AccountLevel
        avatar_frame: int
        verified: int
        views: _containers.RepeatedCompositeFieldContainer[ViewSlot]
        def __init__(self, account_id: _Optional[int] = ..., seat: _Optional[int] = ..., nickname: _Optional[str] = ..., avatar_id: _Optional[int] = ..., character: _Optional[_Union[Character, _Mapping]] = ..., title: _Optional[int] = ..., level: _Optional[_Union[AccountLevel, _Mapping]] = ..., level3: _Optional[_Union[AccountLevel, _Mapping]] = ..., avatar_frame: _Optional[int] = ..., verified: _Optional[int] = ..., views: _Optional[_Iterable[_Union[ViewSlot, _Mapping]]] = ...) -> None: ...
    UUID_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    ACCOUNTS_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    start_time: int
    end_time: int
    config: GameConfig
    accounts: _containers.RepeatedCompositeFieldContainer[RecordGame.AccountInfo]
    result: GameEndResult
    def __init__(self, uuid: _Optional[str] = ..., start_time: _Optional[int] = ..., end_time: _Optional[int] = ..., config: _Optional[_Union[GameConfig, _Mapping]] = ..., accounts: _Optional[_Iterable[_Union[RecordGame.AccountInfo, _Mapping]]] = ..., result: _Optional[_Union[GameEndResult, _Mapping]] = ...) -> None: ...

class RecordListEntry(_message.Message):
    __slots__ = ["version", "uuid", "start_time", "end_time", "tag", "subtag", "players"]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    SUBTAG_FIELD_NUMBER: _ClassVar[int]
    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    version: int
    uuid: str
    start_time: int
    end_time: int
    tag: int
    subtag: int
    players: _containers.RepeatedCompositeFieldContainer[RecordPlayerResult]
    def __init__(self, version: _Optional[int] = ..., uuid: _Optional[str] = ..., start_time: _Optional[int] = ..., end_time: _Optional[int] = ..., tag: _Optional[int] = ..., subtag: _Optional[int] = ..., players: _Optional[_Iterable[_Union[RecordPlayerResult, _Mapping]]] = ...) -> None: ...

class RecordPlayerResult(_message.Message):
    __slots__ = ["rank", "account_id", "nickname", "level", "level3", "pt", "point", "max_hu_type", "action_liqi", "action_rong", "action_zimo", "action_chong", "verified"]
    RANK_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    NICKNAME_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    LEVEL3_FIELD_NUMBER: _ClassVar[int]
    PT_FIELD_NUMBER: _ClassVar[int]
    POINT_FIELD_NUMBER: _ClassVar[int]
    MAX_HU_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACTION_LIQI_FIELD_NUMBER: _ClassVar[int]
    ACTION_RONG_FIELD_NUMBER: _ClassVar[int]
    ACTION_ZIMO_FIELD_NUMBER: _ClassVar[int]
    ACTION_CHONG_FIELD_NUMBER: _ClassVar[int]
    VERIFIED_FIELD_NUMBER: _ClassVar[int]
    rank: int
    account_id: int
    nickname: str
    level: AccountLevel
    level3: AccountLevel
    pt: int
    point: int
    max_hu_type: int
    action_liqi: int
    action_rong: int
    action_zimo: int
    action_chong: int
    verified: int
    def __init__(self, rank: _Optional[int] = ..., account_id: _Optional[int] = ..., nickname: _Optional[str] = ..., level: _Optional[_Union[AccountLevel, _Mapping]] = ..., level3: _Optional[_Union[AccountLevel, _Mapping]] = ..., pt: _Optional[int] = ..., point: _Optional[int] = ..., max_hu_type: _Optional[int] = ..., action_liqi: _Optional[int] = ..., action_rong: _Optional[int] = ..., action_zimo: _Optional[int] = ..., action_chong: _Optional[int] = ..., verified: _Optional[int] = ...) -> None: ...

class CustomizedContestGameStart(_message.Message):
    __slots__ = ["players"]
    class Item(_message.Message):
        __slots__ = ["account_id", "nickname"]
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        NICKNAME_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        nickname: str
        def __init__(self, account_id: _Optional[int] = ..., nickname: _Optional[str] = ...) -> None: ...
    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    players: _containers.RepeatedCompositeFieldContainer[CustomizedContestGameStart.Item]
    def __init__(self, players: _Optional[_Iterable[_Union[CustomizedContestGameStart.Item, _Mapping]]] = ...) -> None: ...

class CustomizedContestGameEnd(_message.Message):
    __slots__ = ["players"]
    class Item(_message.Message):
        __slots__ = ["account_id", "nickname", "total_point"]
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        NICKNAME_FIELD_NUMBER: _ClassVar[int]
        TOTAL_POINT_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        nickname: str
        total_point: int
        def __init__(self, account_id: _Optional[int] = ..., nickname: _Optional[str] = ..., total_point: _Optional[int] = ...) -> None: ...
    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    players: _containers.RepeatedCompositeFieldContainer[CustomizedContestGameEnd.Item]
    def __init__(self, players: _Optional[_Iterable[_Union[CustomizedContestGameEnd.Item, _Mapping]]] = ...) -> None: ...

class Activity(_message.Message):
    __slots__ = ["activity_id", "start_time", "end_time", "type"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    start_time: int
    end_time: int
    type: str
    def __init__(self, activity_id: _Optional[int] = ..., start_time: _Optional[int] = ..., end_time: _Optional[int] = ..., type: _Optional[str] = ...) -> None: ...

class ExchangeRecord(_message.Message):
    __slots__ = ["exchange_id", "count"]
    EXCHANGE_ID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    exchange_id: int
    count: int
    def __init__(self, exchange_id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class ActivityAccumulatedPointData(_message.Message):
    __slots__ = ["activity_id", "point", "gained_reward_list"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    POINT_FIELD_NUMBER: _ClassVar[int]
    GAINED_REWARD_LIST_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    point: int
    gained_reward_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, activity_id: _Optional[int] = ..., point: _Optional[int] = ..., gained_reward_list: _Optional[_Iterable[int]] = ...) -> None: ...

class ActivityRankPointData(_message.Message):
    __slots__ = ["leaderboard_id", "point", "gained_reward", "gainable_time"]
    LEADERBOARD_ID_FIELD_NUMBER: _ClassVar[int]
    POINT_FIELD_NUMBER: _ClassVar[int]
    GAINED_REWARD_FIELD_NUMBER: _ClassVar[int]
    GAINABLE_TIME_FIELD_NUMBER: _ClassVar[int]
    leaderboard_id: int
    point: int
    gained_reward: bool
    gainable_time: int
    def __init__(self, leaderboard_id: _Optional[int] = ..., point: _Optional[int] = ..., gained_reward: bool = ..., gainable_time: _Optional[int] = ...) -> None: ...

class GameRoundHuData(_message.Message):
    __slots__ = ["hupai", "fans", "score", "xun", "title_id", "fan_sum", "fu_sum", "yakuman_count", "biao_dora_count", "red_dora_count", "li_dora_count", "babei_count", "xuan_shang_count"]
    class HuPai(_message.Message):
        __slots__ = ["tile", "seat", "liqi"]
        TILE_FIELD_NUMBER: _ClassVar[int]
        SEAT_FIELD_NUMBER: _ClassVar[int]
        LIQI_FIELD_NUMBER: _ClassVar[int]
        tile: str
        seat: int
        liqi: int
        def __init__(self, tile: _Optional[str] = ..., seat: _Optional[int] = ..., liqi: _Optional[int] = ...) -> None: ...
    class Fan(_message.Message):
        __slots__ = ["id", "count", "fan"]
        ID_FIELD_NUMBER: _ClassVar[int]
        COUNT_FIELD_NUMBER: _ClassVar[int]
        FAN_FIELD_NUMBER: _ClassVar[int]
        id: int
        count: int
        fan: int
        def __init__(self, id: _Optional[int] = ..., count: _Optional[int] = ..., fan: _Optional[int] = ...) -> None: ...
    HUPAI_FIELD_NUMBER: _ClassVar[int]
    FANS_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    XUN_FIELD_NUMBER: _ClassVar[int]
    TITLE_ID_FIELD_NUMBER: _ClassVar[int]
    FAN_SUM_FIELD_NUMBER: _ClassVar[int]
    FU_SUM_FIELD_NUMBER: _ClassVar[int]
    YAKUMAN_COUNT_FIELD_NUMBER: _ClassVar[int]
    BIAO_DORA_COUNT_FIELD_NUMBER: _ClassVar[int]
    RED_DORA_COUNT_FIELD_NUMBER: _ClassVar[int]
    LI_DORA_COUNT_FIELD_NUMBER: _ClassVar[int]
    BABEI_COUNT_FIELD_NUMBER: _ClassVar[int]
    XUAN_SHANG_COUNT_FIELD_NUMBER: _ClassVar[int]
    hupai: GameRoundHuData.HuPai
    fans: _containers.RepeatedCompositeFieldContainer[GameRoundHuData.Fan]
    score: int
    xun: int
    title_id: int
    fan_sum: int
    fu_sum: int
    yakuman_count: int
    biao_dora_count: int
    red_dora_count: int
    li_dora_count: int
    babei_count: int
    xuan_shang_count: int
    def __init__(self, hupai: _Optional[_Union[GameRoundHuData.HuPai, _Mapping]] = ..., fans: _Optional[_Iterable[_Union[GameRoundHuData.Fan, _Mapping]]] = ..., score: _Optional[int] = ..., xun: _Optional[int] = ..., title_id: _Optional[int] = ..., fan_sum: _Optional[int] = ..., fu_sum: _Optional[int] = ..., yakuman_count: _Optional[int] = ..., biao_dora_count: _Optional[int] = ..., red_dora_count: _Optional[int] = ..., li_dora_count: _Optional[int] = ..., babei_count: _Optional[int] = ..., xuan_shang_count: _Optional[int] = ...) -> None: ...

class GameRoundPlayerResult(_message.Message):
    __slots__ = ["type", "hands", "ming", "liqi_type", "is_fulu", "is_liujumanguan", "lian_zhuang", "hu"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    HANDS_FIELD_NUMBER: _ClassVar[int]
    MING_FIELD_NUMBER: _ClassVar[int]
    LIQI_TYPE_FIELD_NUMBER: _ClassVar[int]
    IS_FULU_FIELD_NUMBER: _ClassVar[int]
    IS_LIUJUMANGUAN_FIELD_NUMBER: _ClassVar[int]
    LIAN_ZHUANG_FIELD_NUMBER: _ClassVar[int]
    HU_FIELD_NUMBER: _ClassVar[int]
    type: int
    hands: _containers.RepeatedScalarFieldContainer[str]
    ming: _containers.RepeatedScalarFieldContainer[str]
    liqi_type: int
    is_fulu: bool
    is_liujumanguan: bool
    lian_zhuang: int
    hu: GameRoundHuData
    def __init__(self, type: _Optional[int] = ..., hands: _Optional[_Iterable[str]] = ..., ming: _Optional[_Iterable[str]] = ..., liqi_type: _Optional[int] = ..., is_fulu: bool = ..., is_liujumanguan: bool = ..., lian_zhuang: _Optional[int] = ..., hu: _Optional[_Union[GameRoundHuData, _Mapping]] = ...) -> None: ...

class GameRoundPlayer(_message.Message):
    __slots__ = ["score", "rank", "result"]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    RANK_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    score: int
    rank: int
    result: GameRoundPlayerResult
    def __init__(self, score: _Optional[int] = ..., rank: _Optional[int] = ..., result: _Optional[_Union[GameRoundPlayerResult, _Mapping]] = ...) -> None: ...

class GameRoundSnapshot(_message.Message):
    __slots__ = ["ju", "ben", "players"]
    JU_FIELD_NUMBER: _ClassVar[int]
    BEN_FIELD_NUMBER: _ClassVar[int]
    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    ju: int
    ben: int
    players: _containers.RepeatedCompositeFieldContainer[GameRoundPlayer]
    def __init__(self, ju: _Optional[int] = ..., ben: _Optional[int] = ..., players: _Optional[_Iterable[_Union[GameRoundPlayer, _Mapping]]] = ...) -> None: ...

class GameFinalSnapshot(_message.Message):
    __slots__ = ["uuid", "state", "category", "mode", "meta", "calculate_param", "create_time", "start_time", "finish_time", "seats", "rounds", "account_views", "final_players", "afk_info"]
    class CalculateParam(_message.Message):
        __slots__ = ["init_point", "jingsuanyuandian", "rank_points"]
        INIT_POINT_FIELD_NUMBER: _ClassVar[int]
        JINGSUANYUANDIAN_FIELD_NUMBER: _ClassVar[int]
        RANK_POINTS_FIELD_NUMBER: _ClassVar[int]
        init_point: int
        jingsuanyuandian: int
        rank_points: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, init_point: _Optional[int] = ..., jingsuanyuandian: _Optional[int] = ..., rank_points: _Optional[_Iterable[int]] = ...) -> None: ...
    class GameSeat(_message.Message):
        __slots__ = ["type", "account_id", "notify_endpoint", "client_address", "is_connected"]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        NOTIFY_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
        CLIENT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
        IS_CONNECTED_FIELD_NUMBER: _ClassVar[int]
        type: int
        account_id: int
        notify_endpoint: NetworkEndpoint
        client_address: str
        is_connected: bool
        def __init__(self, type: _Optional[int] = ..., account_id: _Optional[int] = ..., notify_endpoint: _Optional[_Union[NetworkEndpoint, _Mapping]] = ..., client_address: _Optional[str] = ..., is_connected: bool = ...) -> None: ...
    class FinalPlayer(_message.Message):
        __slots__ = ["seat", "total_point", "part_point_1", "part_point_2", "grading_score", "gold"]
        SEAT_FIELD_NUMBER: _ClassVar[int]
        TOTAL_POINT_FIELD_NUMBER: _ClassVar[int]
        PART_POINT_1_FIELD_NUMBER: _ClassVar[int]
        PART_POINT_2_FIELD_NUMBER: _ClassVar[int]
        GRADING_SCORE_FIELD_NUMBER: _ClassVar[int]
        GOLD_FIELD_NUMBER: _ClassVar[int]
        seat: int
        total_point: int
        part_point_1: int
        part_point_2: int
        grading_score: int
        gold: int
        def __init__(self, seat: _Optional[int] = ..., total_point: _Optional[int] = ..., part_point_1: _Optional[int] = ..., part_point_2: _Optional[int] = ..., grading_score: _Optional[int] = ..., gold: _Optional[int] = ...) -> None: ...
    class AFKInfo(_message.Message):
        __slots__ = ["deal_tile_count", "moqie_count", "seat"]
        DEAL_TILE_COUNT_FIELD_NUMBER: _ClassVar[int]
        MOQIE_COUNT_FIELD_NUMBER: _ClassVar[int]
        SEAT_FIELD_NUMBER: _ClassVar[int]
        deal_tile_count: int
        moqie_count: int
        seat: int
        def __init__(self, deal_tile_count: _Optional[int] = ..., moqie_count: _Optional[int] = ..., seat: _Optional[int] = ...) -> None: ...
    UUID_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    META_FIELD_NUMBER: _ClassVar[int]
    CALCULATE_PARAM_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    FINISH_TIME_FIELD_NUMBER: _ClassVar[int]
    SEATS_FIELD_NUMBER: _ClassVar[int]
    ROUNDS_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_VIEWS_FIELD_NUMBER: _ClassVar[int]
    FINAL_PLAYERS_FIELD_NUMBER: _ClassVar[int]
    AFK_INFO_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    state: int
    category: int
    mode: GameMode
    meta: GameMetaData
    calculate_param: GameFinalSnapshot.CalculateParam
    create_time: int
    start_time: int
    finish_time: int
    seats: _containers.RepeatedCompositeFieldContainer[GameFinalSnapshot.GameSeat]
    rounds: _containers.RepeatedCompositeFieldContainer[GameRoundSnapshot]
    account_views: _containers.RepeatedCompositeFieldContainer[PlayerGameView]
    final_players: _containers.RepeatedCompositeFieldContainer[GameFinalSnapshot.FinalPlayer]
    afk_info: _containers.RepeatedCompositeFieldContainer[GameFinalSnapshot.AFKInfo]
    def __init__(self, uuid: _Optional[str] = ..., state: _Optional[int] = ..., category: _Optional[int] = ..., mode: _Optional[_Union[GameMode, _Mapping]] = ..., meta: _Optional[_Union[GameMetaData, _Mapping]] = ..., calculate_param: _Optional[_Union[GameFinalSnapshot.CalculateParam, _Mapping]] = ..., create_time: _Optional[int] = ..., start_time: _Optional[int] = ..., finish_time: _Optional[int] = ..., seats: _Optional[_Iterable[_Union[GameFinalSnapshot.GameSeat, _Mapping]]] = ..., rounds: _Optional[_Iterable[_Union[GameRoundSnapshot, _Mapping]]] = ..., account_views: _Optional[_Iterable[_Union[PlayerGameView, _Mapping]]] = ..., final_players: _Optional[_Iterable[_Union[GameFinalSnapshot.FinalPlayer, _Mapping]]] = ..., afk_info: _Optional[_Iterable[_Union[GameFinalSnapshot.AFKInfo, _Mapping]]] = ...) -> None: ...

class RecordCollectedData(_message.Message):
    __slots__ = ["uuid", "remarks", "start_time", "end_time"]
    UUID_FIELD_NUMBER: _ClassVar[int]
    REMARKS_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    remarks: str
    start_time: int
    end_time: int
    def __init__(self, uuid: _Optional[str] = ..., remarks: _Optional[str] = ..., start_time: _Optional[int] = ..., end_time: _Optional[int] = ...) -> None: ...

class ContestDetailRule(_message.Message):
    __slots__ = ["init_point", "fandian", "can_jifei", "tianbian_value", "liqibang_value", "changbang_value", "noting_fafu_1", "noting_fafu_2", "noting_fafu_3", "have_liujumanguan", "have_qieshangmanguan", "have_biao_dora", "have_gang_biao_dora", "ming_dora_immediately_open", "have_li_dora", "have_gang_li_dora", "have_sifenglianda", "have_sigangsanle", "have_sijializhi", "have_jiuzhongjiupai", "have_sanjiahele", "have_toutiao", "have_helelianzhuang", "have_helezhongju", "have_tingpailianzhuang", "have_tingpaizhongju", "have_yifa", "have_nanruxiru", "jingsuanyuandian", "shunweima_2", "shunweima_3", "shunweima_4", "bianjietishi", "ai_level", "have_zimosun", "disable_multi_yukaman", "guyi_mode", "disable_leijiyiman", "dora3_mode", "xuezhandaodi", "huansanzhang", "chuanma", "disable_double_yakuman", "disable_composite_yakuman", "enable_shiti", "enable_nontsumo_liqi", "disable_double_wind_four_fu", "disable_angang_guoshi", "enable_renhe", "enable_baopai_extend_settings", "fanfu"]
    INIT_POINT_FIELD_NUMBER: _ClassVar[int]
    FANDIAN_FIELD_NUMBER: _ClassVar[int]
    CAN_JIFEI_FIELD_NUMBER: _ClassVar[int]
    TIANBIAN_VALUE_FIELD_NUMBER: _ClassVar[int]
    LIQIBANG_VALUE_FIELD_NUMBER: _ClassVar[int]
    CHANGBANG_VALUE_FIELD_NUMBER: _ClassVar[int]
    NOTING_FAFU_1_FIELD_NUMBER: _ClassVar[int]
    NOTING_FAFU_2_FIELD_NUMBER: _ClassVar[int]
    NOTING_FAFU_3_FIELD_NUMBER: _ClassVar[int]
    HAVE_LIUJUMANGUAN_FIELD_NUMBER: _ClassVar[int]
    HAVE_QIESHANGMANGUAN_FIELD_NUMBER: _ClassVar[int]
    HAVE_BIAO_DORA_FIELD_NUMBER: _ClassVar[int]
    HAVE_GANG_BIAO_DORA_FIELD_NUMBER: _ClassVar[int]
    MING_DORA_IMMEDIATELY_OPEN_FIELD_NUMBER: _ClassVar[int]
    HAVE_LI_DORA_FIELD_NUMBER: _ClassVar[int]
    HAVE_GANG_LI_DORA_FIELD_NUMBER: _ClassVar[int]
    HAVE_SIFENGLIANDA_FIELD_NUMBER: _ClassVar[int]
    HAVE_SIGANGSANLE_FIELD_NUMBER: _ClassVar[int]
    HAVE_SIJIALIZHI_FIELD_NUMBER: _ClassVar[int]
    HAVE_JIUZHONGJIUPAI_FIELD_NUMBER: _ClassVar[int]
    HAVE_SANJIAHELE_FIELD_NUMBER: _ClassVar[int]
    HAVE_TOUTIAO_FIELD_NUMBER: _ClassVar[int]
    HAVE_HELELIANZHUANG_FIELD_NUMBER: _ClassVar[int]
    HAVE_HELEZHONGJU_FIELD_NUMBER: _ClassVar[int]
    HAVE_TINGPAILIANZHUANG_FIELD_NUMBER: _ClassVar[int]
    HAVE_TINGPAIZHONGJU_FIELD_NUMBER: _ClassVar[int]
    HAVE_YIFA_FIELD_NUMBER: _ClassVar[int]
    HAVE_NANRUXIRU_FIELD_NUMBER: _ClassVar[int]
    JINGSUANYUANDIAN_FIELD_NUMBER: _ClassVar[int]
    SHUNWEIMA_2_FIELD_NUMBER: _ClassVar[int]
    SHUNWEIMA_3_FIELD_NUMBER: _ClassVar[int]
    SHUNWEIMA_4_FIELD_NUMBER: _ClassVar[int]
    BIANJIETISHI_FIELD_NUMBER: _ClassVar[int]
    AI_LEVEL_FIELD_NUMBER: _ClassVar[int]
    HAVE_ZIMOSUN_FIELD_NUMBER: _ClassVar[int]
    DISABLE_MULTI_YUKAMAN_FIELD_NUMBER: _ClassVar[int]
    GUYI_MODE_FIELD_NUMBER: _ClassVar[int]
    DISABLE_LEIJIYIMAN_FIELD_NUMBER: _ClassVar[int]
    DORA3_MODE_FIELD_NUMBER: _ClassVar[int]
    XUEZHANDAODI_FIELD_NUMBER: _ClassVar[int]
    HUANSANZHANG_FIELD_NUMBER: _ClassVar[int]
    CHUANMA_FIELD_NUMBER: _ClassVar[int]
    DISABLE_DOUBLE_YAKUMAN_FIELD_NUMBER: _ClassVar[int]
    DISABLE_COMPOSITE_YAKUMAN_FIELD_NUMBER: _ClassVar[int]
    ENABLE_SHITI_FIELD_NUMBER: _ClassVar[int]
    ENABLE_NONTSUMO_LIQI_FIELD_NUMBER: _ClassVar[int]
    DISABLE_DOUBLE_WIND_FOUR_FU_FIELD_NUMBER: _ClassVar[int]
    DISABLE_ANGANG_GUOSHI_FIELD_NUMBER: _ClassVar[int]
    ENABLE_RENHE_FIELD_NUMBER: _ClassVar[int]
    ENABLE_BAOPAI_EXTEND_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    FANFU_FIELD_NUMBER: _ClassVar[int]
    init_point: int
    fandian: int
    can_jifei: bool
    tianbian_value: int
    liqibang_value: int
    changbang_value: int
    noting_fafu_1: int
    noting_fafu_2: int
    noting_fafu_3: int
    have_liujumanguan: bool
    have_qieshangmanguan: bool
    have_biao_dora: bool
    have_gang_biao_dora: bool
    ming_dora_immediately_open: bool
    have_li_dora: bool
    have_gang_li_dora: bool
    have_sifenglianda: bool
    have_sigangsanle: bool
    have_sijializhi: bool
    have_jiuzhongjiupai: bool
    have_sanjiahele: bool
    have_toutiao: bool
    have_helelianzhuang: bool
    have_helezhongju: bool
    have_tingpailianzhuang: bool
    have_tingpaizhongju: bool
    have_yifa: bool
    have_nanruxiru: bool
    jingsuanyuandian: int
    shunweima_2: int
    shunweima_3: int
    shunweima_4: int
    bianjietishi: bool
    ai_level: int
    have_zimosun: bool
    disable_multi_yukaman: bool
    guyi_mode: int
    disable_leijiyiman: bool
    dora3_mode: int
    xuezhandaodi: int
    huansanzhang: int
    chuanma: int
    disable_double_yakuman: int
    disable_composite_yakuman: int
    enable_shiti: int
    enable_nontsumo_liqi: int
    disable_double_wind_four_fu: int
    disable_angang_guoshi: int
    enable_renhe: int
    enable_baopai_extend_settings: int
    fanfu: int
    def __init__(self, init_point: _Optional[int] = ..., fandian: _Optional[int] = ..., can_jifei: bool = ..., tianbian_value: _Optional[int] = ..., liqibang_value: _Optional[int] = ..., changbang_value: _Optional[int] = ..., noting_fafu_1: _Optional[int] = ..., noting_fafu_2: _Optional[int] = ..., noting_fafu_3: _Optional[int] = ..., have_liujumanguan: bool = ..., have_qieshangmanguan: bool = ..., have_biao_dora: bool = ..., have_gang_biao_dora: bool = ..., ming_dora_immediately_open: bool = ..., have_li_dora: bool = ..., have_gang_li_dora: bool = ..., have_sifenglianda: bool = ..., have_sigangsanle: bool = ..., have_sijializhi: bool = ..., have_jiuzhongjiupai: bool = ..., have_sanjiahele: bool = ..., have_toutiao: bool = ..., have_helelianzhuang: bool = ..., have_helezhongju: bool = ..., have_tingpailianzhuang: bool = ..., have_tingpaizhongju: bool = ..., have_yifa: bool = ..., have_nanruxiru: bool = ..., jingsuanyuandian: _Optional[int] = ..., shunweima_2: _Optional[int] = ..., shunweima_3: _Optional[int] = ..., shunweima_4: _Optional[int] = ..., bianjietishi: bool = ..., ai_level: _Optional[int] = ..., have_zimosun: bool = ..., disable_multi_yukaman: bool = ..., guyi_mode: _Optional[int] = ..., disable_leijiyiman: bool = ..., dora3_mode: _Optional[int] = ..., xuezhandaodi: _Optional[int] = ..., huansanzhang: _Optional[int] = ..., chuanma: _Optional[int] = ..., disable_double_yakuman: _Optional[int] = ..., disable_composite_yakuman: _Optional[int] = ..., enable_shiti: _Optional[int] = ..., enable_nontsumo_liqi: _Optional[int] = ..., disable_double_wind_four_fu: _Optional[int] = ..., disable_angang_guoshi: _Optional[int] = ..., enable_renhe: _Optional[int] = ..., enable_baopai_extend_settings: _Optional[int] = ..., fanfu: _Optional[int] = ...) -> None: ...

class ContestDetailRuleV2(_message.Message):
    __slots__ = ["game_rule", "extra_rule"]
    class ExtraRule(_message.Message):
        __slots__ = ["required_level", "max_game_count"]
        REQUIRED_LEVEL_FIELD_NUMBER: _ClassVar[int]
        MAX_GAME_COUNT_FIELD_NUMBER: _ClassVar[int]
        required_level: int
        max_game_count: int
        def __init__(self, required_level: _Optional[int] = ..., max_game_count: _Optional[int] = ...) -> None: ...
    GAME_RULE_FIELD_NUMBER: _ClassVar[int]
    EXTRA_RULE_FIELD_NUMBER: _ClassVar[int]
    game_rule: ContestDetailRule
    extra_rule: ContestDetailRuleV2.ExtraRule
    def __init__(self, game_rule: _Optional[_Union[ContestDetailRule, _Mapping]] = ..., extra_rule: _Optional[_Union[ContestDetailRuleV2.ExtraRule, _Mapping]] = ...) -> None: ...

class GameRuleSetting(_message.Message):
    __slots__ = ["round_type", "shiduan", "dora_count", "thinking_type", "use_detail_rule", "detail_rule_v2"]
    ROUND_TYPE_FIELD_NUMBER: _ClassVar[int]
    SHIDUAN_FIELD_NUMBER: _ClassVar[int]
    DORA_COUNT_FIELD_NUMBER: _ClassVar[int]
    THINKING_TYPE_FIELD_NUMBER: _ClassVar[int]
    USE_DETAIL_RULE_FIELD_NUMBER: _ClassVar[int]
    DETAIL_RULE_V2_FIELD_NUMBER: _ClassVar[int]
    round_type: int
    shiduan: bool
    dora_count: int
    thinking_type: int
    use_detail_rule: bool
    detail_rule_v2: ContestDetailRuleV2
    def __init__(self, round_type: _Optional[int] = ..., shiduan: bool = ..., dora_count: _Optional[int] = ..., thinking_type: _Optional[int] = ..., use_detail_rule: bool = ..., detail_rule_v2: _Optional[_Union[ContestDetailRuleV2, _Mapping]] = ...) -> None: ...

class RecordTingPaiInfo(_message.Message):
    __slots__ = ["tile", "haveyi", "yiman", "count", "fu", "biao_dora_count", "yiman_zimo", "count_zimo", "fu_zimo"]
    TILE_FIELD_NUMBER: _ClassVar[int]
    HAVEYI_FIELD_NUMBER: _ClassVar[int]
    YIMAN_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    FU_FIELD_NUMBER: _ClassVar[int]
    BIAO_DORA_COUNT_FIELD_NUMBER: _ClassVar[int]
    YIMAN_ZIMO_FIELD_NUMBER: _ClassVar[int]
    COUNT_ZIMO_FIELD_NUMBER: _ClassVar[int]
    FU_ZIMO_FIELD_NUMBER: _ClassVar[int]
    tile: str
    haveyi: bool
    yiman: bool
    count: int
    fu: int
    biao_dora_count: int
    yiman_zimo: bool
    count_zimo: int
    fu_zimo: int
    def __init__(self, tile: _Optional[str] = ..., haveyi: bool = ..., yiman: bool = ..., count: _Optional[int] = ..., fu: _Optional[int] = ..., biao_dora_count: _Optional[int] = ..., yiman_zimo: bool = ..., count_zimo: _Optional[int] = ..., fu_zimo: _Optional[int] = ...) -> None: ...

class RecordNoTilePlayerInfo(_message.Message):
    __slots__ = ["tingpai", "hand", "tings", "liuman"]
    TINGPAI_FIELD_NUMBER: _ClassVar[int]
    HAND_FIELD_NUMBER: _ClassVar[int]
    TINGS_FIELD_NUMBER: _ClassVar[int]
    LIUMAN_FIELD_NUMBER: _ClassVar[int]
    tingpai: bool
    hand: _containers.RepeatedScalarFieldContainer[str]
    tings: _containers.RepeatedCompositeFieldContainer[RecordTingPaiInfo]
    liuman: bool
    def __init__(self, tingpai: bool = ..., hand: _Optional[_Iterable[str]] = ..., tings: _Optional[_Iterable[_Union[RecordTingPaiInfo, _Mapping]]] = ..., liuman: bool = ...) -> None: ...

class RecordHuleInfo(_message.Message):
    __slots__ = ["hand", "ming", "hu_tile", "seat", "zimo", "qinjia", "liqi", "doras", "li_doras", "yiman", "count", "fans", "fu", "point_zimo_qin", "point_zimo_xian", "title_id", "point_sum", "dadian", "is_jue_zhang", "xun", "ting_type", "ting_mian"]
    class RecordFanInfo(_message.Message):
        __slots__ = ["val", "id"]
        VAL_FIELD_NUMBER: _ClassVar[int]
        ID_FIELD_NUMBER: _ClassVar[int]
        val: int
        id: int
        def __init__(self, val: _Optional[int] = ..., id: _Optional[int] = ...) -> None: ...
    HAND_FIELD_NUMBER: _ClassVar[int]
    MING_FIELD_NUMBER: _ClassVar[int]
    HU_TILE_FIELD_NUMBER: _ClassVar[int]
    SEAT_FIELD_NUMBER: _ClassVar[int]
    ZIMO_FIELD_NUMBER: _ClassVar[int]
    QINJIA_FIELD_NUMBER: _ClassVar[int]
    LIQI_FIELD_NUMBER: _ClassVar[int]
    DORAS_FIELD_NUMBER: _ClassVar[int]
    LI_DORAS_FIELD_NUMBER: _ClassVar[int]
    YIMAN_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    FANS_FIELD_NUMBER: _ClassVar[int]
    FU_FIELD_NUMBER: _ClassVar[int]
    POINT_ZIMO_QIN_FIELD_NUMBER: _ClassVar[int]
    POINT_ZIMO_XIAN_FIELD_NUMBER: _ClassVar[int]
    TITLE_ID_FIELD_NUMBER: _ClassVar[int]
    POINT_SUM_FIELD_NUMBER: _ClassVar[int]
    DADIAN_FIELD_NUMBER: _ClassVar[int]
    IS_JUE_ZHANG_FIELD_NUMBER: _ClassVar[int]
    XUN_FIELD_NUMBER: _ClassVar[int]
    TING_TYPE_FIELD_NUMBER: _ClassVar[int]
    TING_MIAN_FIELD_NUMBER: _ClassVar[int]
    hand: _containers.RepeatedScalarFieldContainer[str]
    ming: _containers.RepeatedScalarFieldContainer[str]
    hu_tile: str
    seat: int
    zimo: bool
    qinjia: bool
    liqi: bool
    doras: _containers.RepeatedScalarFieldContainer[str]
    li_doras: _containers.RepeatedScalarFieldContainer[str]
    yiman: bool
    count: int
    fans: _containers.RepeatedCompositeFieldContainer[RecordHuleInfo.RecordFanInfo]
    fu: int
    point_zimo_qin: int
    point_zimo_xian: int
    title_id: int
    point_sum: int
    dadian: int
    is_jue_zhang: bool
    xun: int
    ting_type: int
    ting_mian: int
    def __init__(self, hand: _Optional[_Iterable[str]] = ..., ming: _Optional[_Iterable[str]] = ..., hu_tile: _Optional[str] = ..., seat: _Optional[int] = ..., zimo: bool = ..., qinjia: bool = ..., liqi: bool = ..., doras: _Optional[_Iterable[str]] = ..., li_doras: _Optional[_Iterable[str]] = ..., yiman: bool = ..., count: _Optional[int] = ..., fans: _Optional[_Iterable[_Union[RecordHuleInfo.RecordFanInfo, _Mapping]]] = ..., fu: _Optional[int] = ..., point_zimo_qin: _Optional[int] = ..., point_zimo_xian: _Optional[int] = ..., title_id: _Optional[int] = ..., point_sum: _Optional[int] = ..., dadian: _Optional[int] = ..., is_jue_zhang: bool = ..., xun: _Optional[int] = ..., ting_type: _Optional[int] = ..., ting_mian: _Optional[int] = ...) -> None: ...

class RecordHulesInfo(_message.Message):
    __slots__ = ["seat", "hules"]
    SEAT_FIELD_NUMBER: _ClassVar[int]
    HULES_FIELD_NUMBER: _ClassVar[int]
    seat: int
    hules: _containers.RepeatedCompositeFieldContainer[RecordHuleInfo]
    def __init__(self, seat: _Optional[int] = ..., hules: _Optional[_Iterable[_Union[RecordHuleInfo, _Mapping]]] = ...) -> None: ...

class RecordLiujuInfo(_message.Message):
    __slots__ = ["seat", "type"]
    SEAT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    seat: int
    type: int
    def __init__(self, seat: _Optional[int] = ..., type: _Optional[int] = ...) -> None: ...

class RecordNoTileInfo(_message.Message):
    __slots__ = ["liujumanguan", "players"]
    LIUJUMANGUAN_FIELD_NUMBER: _ClassVar[int]
    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    liujumanguan: bool
    players: _containers.RepeatedCompositeFieldContainer[RecordNoTilePlayerInfo]
    def __init__(self, liujumanguan: bool = ..., players: _Optional[_Iterable[_Union[RecordNoTilePlayerInfo, _Mapping]]] = ...) -> None: ...

class RecordLiqiInfo(_message.Message):
    __slots__ = ["seat", "score", "is_w", "is_zhen_ting", "xun", "is_success"]
    SEAT_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    IS_W_FIELD_NUMBER: _ClassVar[int]
    IS_ZHEN_TING_FIELD_NUMBER: _ClassVar[int]
    XUN_FIELD_NUMBER: _ClassVar[int]
    IS_SUCCESS_FIELD_NUMBER: _ClassVar[int]
    seat: int
    score: int
    is_w: bool
    is_zhen_ting: bool
    xun: int
    is_success: bool
    def __init__(self, seat: _Optional[int] = ..., score: _Optional[int] = ..., is_w: bool = ..., is_zhen_ting: bool = ..., xun: _Optional[int] = ..., is_success: bool = ...) -> None: ...

class RecordGangInfo(_message.Message):
    __slots__ = ["seat", "type", "pai", "is_dora", "xun"]
    SEAT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    PAI_FIELD_NUMBER: _ClassVar[int]
    IS_DORA_FIELD_NUMBER: _ClassVar[int]
    XUN_FIELD_NUMBER: _ClassVar[int]
    seat: int
    type: int
    pai: str
    is_dora: bool
    xun: int
    def __init__(self, seat: _Optional[int] = ..., type: _Optional[int] = ..., pai: _Optional[str] = ..., is_dora: bool = ..., xun: _Optional[int] = ...) -> None: ...

class RecordBaBeiInfo(_message.Message):
    __slots__ = ["seat", "is_zi_mo", "is_chong", "is_bei"]
    SEAT_FIELD_NUMBER: _ClassVar[int]
    IS_ZI_MO_FIELD_NUMBER: _ClassVar[int]
    IS_CHONG_FIELD_NUMBER: _ClassVar[int]
    IS_BEI_FIELD_NUMBER: _ClassVar[int]
    seat: int
    is_zi_mo: bool
    is_chong: bool
    is_bei: bool
    def __init__(self, seat: _Optional[int] = ..., is_zi_mo: bool = ..., is_chong: bool = ..., is_bei: bool = ...) -> None: ...

class RecordPeiPaiInfo(_message.Message):
    __slots__ = ["dora_count", "r_dora_count", "bei_count"]
    DORA_COUNT_FIELD_NUMBER: _ClassVar[int]
    R_DORA_COUNT_FIELD_NUMBER: _ClassVar[int]
    BEI_COUNT_FIELD_NUMBER: _ClassVar[int]
    dora_count: int
    r_dora_count: int
    bei_count: int
    def __init__(self, dora_count: _Optional[int] = ..., r_dora_count: _Optional[int] = ..., bei_count: _Optional[int] = ...) -> None: ...

class RecordRoundInfo(_message.Message):
    __slots__ = ["name", "chang", "ju", "ben", "scores", "liqi_infos", "gang_infos", "peipai_infos", "babai_infos", "hules_info", "liuju_info", "no_tile_info"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CHANG_FIELD_NUMBER: _ClassVar[int]
    JU_FIELD_NUMBER: _ClassVar[int]
    BEN_FIELD_NUMBER: _ClassVar[int]
    SCORES_FIELD_NUMBER: _ClassVar[int]
    LIQI_INFOS_FIELD_NUMBER: _ClassVar[int]
    GANG_INFOS_FIELD_NUMBER: _ClassVar[int]
    PEIPAI_INFOS_FIELD_NUMBER: _ClassVar[int]
    BABAI_INFOS_FIELD_NUMBER: _ClassVar[int]
    HULES_INFO_FIELD_NUMBER: _ClassVar[int]
    LIUJU_INFO_FIELD_NUMBER: _ClassVar[int]
    NO_TILE_INFO_FIELD_NUMBER: _ClassVar[int]
    name: str
    chang: int
    ju: int
    ben: int
    scores: _containers.RepeatedScalarFieldContainer[int]
    liqi_infos: _containers.RepeatedCompositeFieldContainer[RecordLiqiInfo]
    gang_infos: _containers.RepeatedCompositeFieldContainer[RecordGangInfo]
    peipai_infos: _containers.RepeatedCompositeFieldContainer[RecordPeiPaiInfo]
    babai_infos: _containers.RepeatedCompositeFieldContainer[RecordBaBeiInfo]
    hules_info: RecordHulesInfo
    liuju_info: RecordLiujuInfo
    no_tile_info: RecordNoTileInfo
    def __init__(self, name: _Optional[str] = ..., chang: _Optional[int] = ..., ju: _Optional[int] = ..., ben: _Optional[int] = ..., scores: _Optional[_Iterable[int]] = ..., liqi_infos: _Optional[_Iterable[_Union[RecordLiqiInfo, _Mapping]]] = ..., gang_infos: _Optional[_Iterable[_Union[RecordGangInfo, _Mapping]]] = ..., peipai_infos: _Optional[_Iterable[_Union[RecordPeiPaiInfo, _Mapping]]] = ..., babai_infos: _Optional[_Iterable[_Union[RecordBaBeiInfo, _Mapping]]] = ..., hules_info: _Optional[_Union[RecordHulesInfo, _Mapping]] = ..., liuju_info: _Optional[_Union[RecordLiujuInfo, _Mapping]] = ..., no_tile_info: _Optional[_Union[RecordNoTileInfo, _Mapping]] = ...) -> None: ...

class RecordAnalysisedData(_message.Message):
    __slots__ = ["round_infos"]
    ROUND_INFOS_FIELD_NUMBER: _ClassVar[int]
    round_infos: _containers.RepeatedCompositeFieldContainer[RecordRoundInfo]
    def __init__(self, round_infos: _Optional[_Iterable[_Union[RecordRoundInfo, _Mapping]]] = ...) -> None: ...

class VoteData(_message.Message):
    __slots__ = ["activity_id", "vote", "count"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    VOTE_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    vote: int
    count: int
    def __init__(self, activity_id: _Optional[int] = ..., vote: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class ActivityBuffData(_message.Message):
    __slots__ = ["buff_id", "level"]
    BUFF_ID_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    buff_id: int
    level: int
    def __init__(self, buff_id: _Optional[int] = ..., level: _Optional[int] = ...) -> None: ...

class AccountResourceSnapshot(_message.Message):
    __slots__ = ["bag_item", "currency", "title", "used_title", "currency_convert"]
    class BagItemSnapshot(_message.Message):
        __slots__ = ["resource_id", "resource_count", "resource_version"]
        RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
        RESOURCE_COUNT_FIELD_NUMBER: _ClassVar[int]
        RESOURCE_VERSION_FIELD_NUMBER: _ClassVar[int]
        resource_id: int
        resource_count: int
        resource_version: int
        def __init__(self, resource_id: _Optional[int] = ..., resource_count: _Optional[int] = ..., resource_version: _Optional[int] = ...) -> None: ...
    class CurrencySnapshot(_message.Message):
        __slots__ = ["currency_id", "currency_count"]
        CURRENCY_ID_FIELD_NUMBER: _ClassVar[int]
        CURRENCY_COUNT_FIELD_NUMBER: _ClassVar[int]
        currency_id: int
        currency_count: int
        def __init__(self, currency_id: _Optional[int] = ..., currency_count: _Optional[int] = ...) -> None: ...
    class TitleSnapshot(_message.Message):
        __slots__ = ["title_list"]
        TITLE_LIST_FIELD_NUMBER: _ClassVar[int]
        title_list: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, title_list: _Optional[_Iterable[int]] = ...) -> None: ...
    class UsedTitleSnapshot(_message.Message):
        __slots__ = ["title_id"]
        TITLE_ID_FIELD_NUMBER: _ClassVar[int]
        title_id: int
        def __init__(self, title_id: _Optional[int] = ...) -> None: ...
    BAG_ITEM_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    USED_TITLE_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_CONVERT_FIELD_NUMBER: _ClassVar[int]
    bag_item: _containers.RepeatedCompositeFieldContainer[AccountResourceSnapshot.BagItemSnapshot]
    currency: _containers.RepeatedCompositeFieldContainer[AccountResourceSnapshot.CurrencySnapshot]
    title: AccountResourceSnapshot.TitleSnapshot
    used_title: AccountResourceSnapshot.UsedTitleSnapshot
    currency_convert: int
    def __init__(self, bag_item: _Optional[_Iterable[_Union[AccountResourceSnapshot.BagItemSnapshot, _Mapping]]] = ..., currency: _Optional[_Iterable[_Union[AccountResourceSnapshot.CurrencySnapshot, _Mapping]]] = ..., title: _Optional[_Union[AccountResourceSnapshot.TitleSnapshot, _Mapping]] = ..., used_title: _Optional[_Union[AccountResourceSnapshot.UsedTitleSnapshot, _Mapping]] = ..., currency_convert: _Optional[int] = ...) -> None: ...

class AccountCharacterSnapshot(_message.Message):
    __slots__ = ["created_characters", "removed_characters", "modified_characters", "main_character", "skins", "hidden_characters"]
    class MainCharacterSnapshot(_message.Message):
        __slots__ = ["character_id"]
        CHARACTER_ID_FIELD_NUMBER: _ClassVar[int]
        character_id: int
        def __init__(self, character_id: _Optional[int] = ...) -> None: ...
    class SkinsSnapshot(_message.Message):
        __slots__ = ["skin_list"]
        SKIN_LIST_FIELD_NUMBER: _ClassVar[int]
        skin_list: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, skin_list: _Optional[_Iterable[int]] = ...) -> None: ...
    class HiddenCharacter(_message.Message):
        __slots__ = ["hidden_list"]
        HIDDEN_LIST_FIELD_NUMBER: _ClassVar[int]
        hidden_list: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, hidden_list: _Optional[_Iterable[int]] = ...) -> None: ...
    CREATED_CHARACTERS_FIELD_NUMBER: _ClassVar[int]
    REMOVED_CHARACTERS_FIELD_NUMBER: _ClassVar[int]
    MODIFIED_CHARACTERS_FIELD_NUMBER: _ClassVar[int]
    MAIN_CHARACTER_FIELD_NUMBER: _ClassVar[int]
    SKINS_FIELD_NUMBER: _ClassVar[int]
    HIDDEN_CHARACTERS_FIELD_NUMBER: _ClassVar[int]
    created_characters: _containers.RepeatedScalarFieldContainer[int]
    removed_characters: _containers.RepeatedCompositeFieldContainer[Character]
    modified_characters: _containers.RepeatedCompositeFieldContainer[Character]
    main_character: AccountCharacterSnapshot.MainCharacterSnapshot
    skins: AccountCharacterSnapshot.SkinsSnapshot
    hidden_characters: AccountCharacterSnapshot.HiddenCharacter
    def __init__(self, created_characters: _Optional[_Iterable[int]] = ..., removed_characters: _Optional[_Iterable[_Union[Character, _Mapping]]] = ..., modified_characters: _Optional[_Iterable[_Union[Character, _Mapping]]] = ..., main_character: _Optional[_Union[AccountCharacterSnapshot.MainCharacterSnapshot, _Mapping]] = ..., skins: _Optional[_Union[AccountCharacterSnapshot.SkinsSnapshot, _Mapping]] = ..., hidden_characters: _Optional[_Union[AccountCharacterSnapshot.HiddenCharacter, _Mapping]] = ...) -> None: ...

class AccountMailRecord(_message.Message):
    __slots__ = ["created_mails", "removed_mails", "modified_mails"]
    class MailSnapshot(_message.Message):
        __slots__ = ["mail_id", "reference_id", "create_time", "expire_time", "take_attachment", "attachments"]
        MAIL_ID_FIELD_NUMBER: _ClassVar[int]
        REFERENCE_ID_FIELD_NUMBER: _ClassVar[int]
        CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
        EXPIRE_TIME_FIELD_NUMBER: _ClassVar[int]
        TAKE_ATTACHMENT_FIELD_NUMBER: _ClassVar[int]
        ATTACHMENTS_FIELD_NUMBER: _ClassVar[int]
        mail_id: int
        reference_id: int
        create_time: int
        expire_time: int
        take_attachment: int
        attachments: _containers.RepeatedCompositeFieldContainer[RewardSlot]
        def __init__(self, mail_id: _Optional[int] = ..., reference_id: _Optional[int] = ..., create_time: _Optional[int] = ..., expire_time: _Optional[int] = ..., take_attachment: _Optional[int] = ..., attachments: _Optional[_Iterable[_Union[RewardSlot, _Mapping]]] = ...) -> None: ...
    CREATED_MAILS_FIELD_NUMBER: _ClassVar[int]
    REMOVED_MAILS_FIELD_NUMBER: _ClassVar[int]
    MODIFIED_MAILS_FIELD_NUMBER: _ClassVar[int]
    created_mails: _containers.RepeatedScalarFieldContainer[int]
    removed_mails: _containers.RepeatedCompositeFieldContainer[AccountMailRecord.MailSnapshot]
    modified_mails: _containers.RepeatedCompositeFieldContainer[AccountMailRecord.MailSnapshot]
    def __init__(self, created_mails: _Optional[_Iterable[int]] = ..., removed_mails: _Optional[_Iterable[_Union[AccountMailRecord.MailSnapshot, _Mapping]]] = ..., modified_mails: _Optional[_Iterable[_Union[AccountMailRecord.MailSnapshot, _Mapping]]] = ...) -> None: ...

class AccountAchievementSnapshot(_message.Message):
    __slots__ = ["achievements", "rewarded_group", "version"]
    class RewardedGroupSnapshot(_message.Message):
        __slots__ = ["rewarded_id"]
        REWARDED_ID_FIELD_NUMBER: _ClassVar[int]
        rewarded_id: int
        def __init__(self, rewarded_id: _Optional[int] = ...) -> None: ...
    class AchievementVersion(_message.Message):
        __slots__ = ["version"]
        VERSION_FIELD_NUMBER: _ClassVar[int]
        version: int
        def __init__(self, version: _Optional[int] = ...) -> None: ...
    ACHIEVEMENTS_FIELD_NUMBER: _ClassVar[int]
    REWARDED_GROUP_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    achievements: _containers.RepeatedCompositeFieldContainer[AchievementProgress]
    rewarded_group: AccountAchievementSnapshot.RewardedGroupSnapshot
    version: AccountAchievementSnapshot.AchievementVersion
    def __init__(self, achievements: _Optional[_Iterable[_Union[AchievementProgress, _Mapping]]] = ..., rewarded_group: _Optional[_Union[AccountAchievementSnapshot.RewardedGroupSnapshot, _Mapping]] = ..., version: _Optional[_Union[AccountAchievementSnapshot.AchievementVersion, _Mapping]] = ...) -> None: ...

class AccountMiscSnapshot(_message.Message):
    __slots__ = ["faith_data", "vip_reward_gained", "vip", "shop_info", "month_ticket", "recharged", "month_ticket_v2"]
    class AccountVIPRewardSnapshot(_message.Message):
        __slots__ = ["rewarded"]
        REWARDED_FIELD_NUMBER: _ClassVar[int]
        rewarded: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, rewarded: _Optional[_Iterable[int]] = ...) -> None: ...
    class MonthTicketInfo(_message.Message):
        __slots__ = ["id", "end_time", "last_pay_time", "record_start_time", "history"]
        ID_FIELD_NUMBER: _ClassVar[int]
        END_TIME_FIELD_NUMBER: _ClassVar[int]
        LAST_PAY_TIME_FIELD_NUMBER: _ClassVar[int]
        RECORD_START_TIME_FIELD_NUMBER: _ClassVar[int]
        HISTORY_FIELD_NUMBER: _ClassVar[int]
        id: int
        end_time: int
        last_pay_time: int
        record_start_time: int
        history: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, id: _Optional[int] = ..., end_time: _Optional[int] = ..., last_pay_time: _Optional[int] = ..., record_start_time: _Optional[int] = ..., history: _Optional[_Iterable[int]] = ...) -> None: ...
    class AccountMonthTicketSnapshot(_message.Message):
        __slots__ = ["tickets"]
        TICKETS_FIELD_NUMBER: _ClassVar[int]
        tickets: _containers.RepeatedCompositeFieldContainer[AccountMiscSnapshot.MonthTicketInfo]
        def __init__(self, tickets: _Optional[_Iterable[_Union[AccountMiscSnapshot.MonthTicketInfo, _Mapping]]] = ...) -> None: ...
    class AccountVIP(_message.Message):
        __slots__ = ["vip"]
        VIP_FIELD_NUMBER: _ClassVar[int]
        vip: int
        def __init__(self, vip: _Optional[int] = ...) -> None: ...
    class AccountRechargeInfo(_message.Message):
        __slots__ = ["records", "has_data"]
        class RechargeRecord(_message.Message):
            __slots__ = ["level", "recharge_time"]
            LEVEL_FIELD_NUMBER: _ClassVar[int]
            RECHARGE_TIME_FIELD_NUMBER: _ClassVar[int]
            level: int
            recharge_time: int
            def __init__(self, level: _Optional[int] = ..., recharge_time: _Optional[int] = ...) -> None: ...
        RECORDS_FIELD_NUMBER: _ClassVar[int]
        HAS_DATA_FIELD_NUMBER: _ClassVar[int]
        records: _containers.RepeatedCompositeFieldContainer[AccountMiscSnapshot.AccountRechargeInfo.RechargeRecord]
        has_data: int
        def __init__(self, records: _Optional[_Iterable[_Union[AccountMiscSnapshot.AccountRechargeInfo.RechargeRecord, _Mapping]]] = ..., has_data: _Optional[int] = ...) -> None: ...
    class AccountMonthTicketSnapshotV2(_message.Message):
        __slots__ = ["end_time", "last_pay_time", "record_start_time", "history"]
        END_TIME_FIELD_NUMBER: _ClassVar[int]
        LAST_PAY_TIME_FIELD_NUMBER: _ClassVar[int]
        RECORD_START_TIME_FIELD_NUMBER: _ClassVar[int]
        HISTORY_FIELD_NUMBER: _ClassVar[int]
        end_time: int
        last_pay_time: int
        record_start_time: int
        history: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, end_time: _Optional[int] = ..., last_pay_time: _Optional[int] = ..., record_start_time: _Optional[int] = ..., history: _Optional[_Iterable[int]] = ...) -> None: ...
    FAITH_DATA_FIELD_NUMBER: _ClassVar[int]
    VIP_REWARD_GAINED_FIELD_NUMBER: _ClassVar[int]
    VIP_FIELD_NUMBER: _ClassVar[int]
    SHOP_INFO_FIELD_NUMBER: _ClassVar[int]
    MONTH_TICKET_FIELD_NUMBER: _ClassVar[int]
    RECHARGED_FIELD_NUMBER: _ClassVar[int]
    MONTH_TICKET_V2_FIELD_NUMBER: _ClassVar[int]
    faith_data: FaithData
    vip_reward_gained: AccountMiscSnapshot.AccountVIPRewardSnapshot
    vip: AccountMiscSnapshot.AccountVIP
    shop_info: ShopInfo
    month_ticket: AccountMiscSnapshot.AccountMonthTicketSnapshot
    recharged: AccountMiscSnapshot.AccountRechargeInfo
    month_ticket_v2: AccountMiscSnapshot.AccountMonthTicketSnapshotV2
    def __init__(self, faith_data: _Optional[_Union[FaithData, _Mapping]] = ..., vip_reward_gained: _Optional[_Union[AccountMiscSnapshot.AccountVIPRewardSnapshot, _Mapping]] = ..., vip: _Optional[_Union[AccountMiscSnapshot.AccountVIP, _Mapping]] = ..., shop_info: _Optional[_Union[ShopInfo, _Mapping]] = ..., month_ticket: _Optional[_Union[AccountMiscSnapshot.AccountMonthTicketSnapshot, _Mapping]] = ..., recharged: _Optional[_Union[AccountMiscSnapshot.AccountRechargeInfo, _Mapping]] = ..., month_ticket_v2: _Optional[_Union[AccountMiscSnapshot.AccountMonthTicketSnapshotV2, _Mapping]] = ...) -> None: ...

class AccountGiftCodeRecord(_message.Message):
    __slots__ = ["used_gift_code"]
    USED_GIFT_CODE_FIELD_NUMBER: _ClassVar[int]
    used_gift_code: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, used_gift_code: _Optional[_Iterable[str]] = ...) -> None: ...

class AccSn(_message.Message):
    __slots__ = ["resource", "character", "mail", "achievement", "misc", "gift_code"]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    CHARACTER_FIELD_NUMBER: _ClassVar[int]
    MAIL_FIELD_NUMBER: _ClassVar[int]
    ACHIEVEMENT_FIELD_NUMBER: _ClassVar[int]
    MISC_FIELD_NUMBER: _ClassVar[int]
    GIFT_CODE_FIELD_NUMBER: _ClassVar[int]
    resource: AccountResourceSnapshot
    character: AccountCharacterSnapshot
    mail: AccountMailRecord
    achievement: AccountAchievementSnapshot
    misc: AccountMiscSnapshot
    gift_code: AccountGiftCodeRecord
    def __init__(self, resource: _Optional[_Union[AccountResourceSnapshot, _Mapping]] = ..., character: _Optional[_Union[AccountCharacterSnapshot, _Mapping]] = ..., mail: _Optional[_Union[AccountMailRecord, _Mapping]] = ..., achievement: _Optional[_Union[AccountAchievementSnapshot, _Mapping]] = ..., misc: _Optional[_Union[AccountMiscSnapshot, _Mapping]] = ..., gift_code: _Optional[_Union[AccountGiftCodeRecord, _Mapping]] = ...) -> None: ...

class AccSnDa(_message.Message):
    __slots__ = ["account_id", "time", "snapshot"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    time: int
    snapshot: bytes
    def __init__(self, account_id: _Optional[int] = ..., time: _Optional[int] = ..., snapshot: _Optional[bytes] = ...) -> None: ...

class TransparentData(_message.Message):
    __slots__ = ["method", "data", "session", "remote"]
    METHOD_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    SESSION_FIELD_NUMBER: _ClassVar[int]
    REMOTE_FIELD_NUMBER: _ClassVar[int]
    method: str
    data: bytes
    session: str
    remote: NetworkEndpoint
    def __init__(self, method: _Optional[str] = ..., data: _Optional[bytes] = ..., session: _Optional[str] = ..., remote: _Optional[_Union[NetworkEndpoint, _Mapping]] = ...) -> None: ...

class AmuletTile(_message.Message):
    __slots__ = ["id", "tile"]
    ID_FIELD_NUMBER: _ClassVar[int]
    TILE_FIELD_NUMBER: _ClassVar[int]
    id: int
    tile: str
    def __init__(self, id: _Optional[int] = ..., tile: _Optional[str] = ...) -> None: ...

class AmuletFan(_message.Message):
    __slots__ = ["id", "val", "count", "yiman"]
    ID_FIELD_NUMBER: _ClassVar[int]
    VAL_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    YIMAN_FIELD_NUMBER: _ClassVar[int]
    id: int
    val: int
    count: int
    yiman: bool
    def __init__(self, id: _Optional[int] = ..., val: _Optional[int] = ..., count: _Optional[int] = ..., yiman: bool = ...) -> None: ...

class AmuletReplace(_message.Message):
    __slots__ = ["id", "tile"]
    ID_FIELD_NUMBER: _ClassVar[int]
    TILE_FIELD_NUMBER: _ClassVar[int]
    id: int
    tile: str
    def __init__(self, id: _Optional[int] = ..., tile: _Optional[str] = ...) -> None: ...

class AmuletMingInfo(_message.Message):
    __slots__ = ["type", "tile_list"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TILE_LIST_FIELD_NUMBER: _ClassVar[int]
    type: int
    tile_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, type: _Optional[int] = ..., tile_list: _Optional[_Iterable[int]] = ...) -> None: ...

class AmuletActivityHookEffect(_message.Message):
    __slots__ = ["add_dora", "add_tian_dora", "add_effect", "remove_effect", "add_buff", "remove_buff", "add_coin", "tile_replace", "add_fan", "add_base", "modify_fan", "id", "modify_dora", "uid", "add_show_tile", "add_dora_count"]
    ADD_DORA_FIELD_NUMBER: _ClassVar[int]
    ADD_TIAN_DORA_FIELD_NUMBER: _ClassVar[int]
    ADD_EFFECT_FIELD_NUMBER: _ClassVar[int]
    REMOVE_EFFECT_FIELD_NUMBER: _ClassVar[int]
    ADD_BUFF_FIELD_NUMBER: _ClassVar[int]
    REMOVE_BUFF_FIELD_NUMBER: _ClassVar[int]
    ADD_COIN_FIELD_NUMBER: _ClassVar[int]
    TILE_REPLACE_FIELD_NUMBER: _ClassVar[int]
    ADD_FAN_FIELD_NUMBER: _ClassVar[int]
    ADD_BASE_FIELD_NUMBER: _ClassVar[int]
    MODIFY_FAN_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    MODIFY_DORA_FIELD_NUMBER: _ClassVar[int]
    UID_FIELD_NUMBER: _ClassVar[int]
    ADD_SHOW_TILE_FIELD_NUMBER: _ClassVar[int]
    ADD_DORA_COUNT_FIELD_NUMBER: _ClassVar[int]
    add_dora: _containers.RepeatedScalarFieldContainer[int]
    add_tian_dora: _containers.RepeatedScalarFieldContainer[str]
    add_effect: _containers.RepeatedScalarFieldContainer[int]
    remove_effect: _containers.RepeatedScalarFieldContainer[int]
    add_buff: _containers.RepeatedScalarFieldContainer[int]
    remove_buff: _containers.RepeatedScalarFieldContainer[int]
    add_coin: int
    tile_replace: _containers.RepeatedCompositeFieldContainer[AmuletReplace]
    add_fan: int
    add_base: int
    modify_fan: _containers.RepeatedCompositeFieldContainer[AmuletFan]
    id: int
    modify_dora: bool
    uid: int
    add_show_tile: _containers.RepeatedScalarFieldContainer[int]
    add_dora_count: int
    def __init__(self, add_dora: _Optional[_Iterable[int]] = ..., add_tian_dora: _Optional[_Iterable[str]] = ..., add_effect: _Optional[_Iterable[int]] = ..., remove_effect: _Optional[_Iterable[int]] = ..., add_buff: _Optional[_Iterable[int]] = ..., remove_buff: _Optional[_Iterable[int]] = ..., add_coin: _Optional[int] = ..., tile_replace: _Optional[_Iterable[_Union[AmuletReplace, _Mapping]]] = ..., add_fan: _Optional[int] = ..., add_base: _Optional[int] = ..., modify_fan: _Optional[_Iterable[_Union[AmuletFan, _Mapping]]] = ..., id: _Optional[int] = ..., modify_dora: bool = ..., uid: _Optional[int] = ..., add_show_tile: _Optional[_Iterable[int]] = ..., add_dora_count: _Optional[int] = ...) -> None: ...

class AmuletHuleInfo(_message.Message):
    __slots__ = ["tile", "fan_list", "fan", "point", "base"]
    TILE_FIELD_NUMBER: _ClassVar[int]
    FAN_LIST_FIELD_NUMBER: _ClassVar[int]
    FAN_FIELD_NUMBER: _ClassVar[int]
    POINT_FIELD_NUMBER: _ClassVar[int]
    BASE_FIELD_NUMBER: _ClassVar[int]
    tile: int
    fan_list: _containers.RepeatedCompositeFieldContainer[AmuletFan]
    fan: int
    point: str
    base: int
    def __init__(self, tile: _Optional[int] = ..., fan_list: _Optional[_Iterable[_Union[AmuletFan, _Mapping]]] = ..., fan: _Optional[int] = ..., point: _Optional[str] = ..., base: _Optional[int] = ...) -> None: ...

class AmuletHuleOperateResult(_message.Message):
    __slots__ = ["hu_final", "hu_base", "hook_effect"]
    HU_FINAL_FIELD_NUMBER: _ClassVar[int]
    HU_BASE_FIELD_NUMBER: _ClassVar[int]
    HOOK_EFFECT_FIELD_NUMBER: _ClassVar[int]
    hu_final: AmuletHuleInfo
    hu_base: AmuletHuleInfo
    hook_effect: _containers.RepeatedCompositeFieldContainer[AmuletActivityHookEffect]
    def __init__(self, hu_final: _Optional[_Union[AmuletHuleInfo, _Mapping]] = ..., hu_base: _Optional[_Union[AmuletHuleInfo, _Mapping]] = ..., hook_effect: _Optional[_Iterable[_Union[AmuletActivityHookEffect, _Mapping]]] = ...) -> None: ...

class AmuletGangOperateResult(_message.Message):
    __slots__ = ["new_dora", "hook_effect"]
    NEW_DORA_FIELD_NUMBER: _ClassVar[int]
    HOOK_EFFECT_FIELD_NUMBER: _ClassVar[int]
    new_dora: _containers.RepeatedScalarFieldContainer[int]
    hook_effect: _containers.RepeatedCompositeFieldContainer[AmuletActivityHookEffect]
    def __init__(self, new_dora: _Optional[_Iterable[int]] = ..., hook_effect: _Optional[_Iterable[_Union[AmuletActivityHookEffect, _Mapping]]] = ...) -> None: ...

class AmuletDealTileResult(_message.Message):
    __slots__ = ["tile", "hook_effect"]
    TILE_FIELD_NUMBER: _ClassVar[int]
    HOOK_EFFECT_FIELD_NUMBER: _ClassVar[int]
    tile: int
    hook_effect: _containers.RepeatedCompositeFieldContainer[AmuletActivityHookEffect]
    def __init__(self, tile: _Optional[int] = ..., hook_effect: _Optional[_Iterable[_Union[AmuletActivityHookEffect, _Mapping]]] = ...) -> None: ...

class AmuletRoundResult(_message.Message):
    __slots__ = ["hu_result", "deal_result"]
    HU_RESULT_FIELD_NUMBER: _ClassVar[int]
    DEAL_RESULT_FIELD_NUMBER: _ClassVar[int]
    hu_result: AmuletHuleOperateResult
    deal_result: AmuletDealTileResult
    def __init__(self, hu_result: _Optional[_Union[AmuletHuleOperateResult, _Mapping]] = ..., deal_result: _Optional[_Union[AmuletDealTileResult, _Mapping]] = ...) -> None: ...

class AmuletUpgradeResult(_message.Message):
    __slots__ = ["remain_rounds", "point_coin", "level_coin", "shop", "hook_effect"]
    REMAIN_ROUNDS_FIELD_NUMBER: _ClassVar[int]
    POINT_COIN_FIELD_NUMBER: _ClassVar[int]
    LEVEL_COIN_FIELD_NUMBER: _ClassVar[int]
    SHOP_FIELD_NUMBER: _ClassVar[int]
    HOOK_EFFECT_FIELD_NUMBER: _ClassVar[int]
    remain_rounds: _containers.RepeatedCompositeFieldContainer[AmuletRoundResult]
    point_coin: int
    level_coin: int
    shop: AmuletGameShopData
    hook_effect: _containers.RepeatedCompositeFieldContainer[AmuletActivityHookEffect]
    def __init__(self, remain_rounds: _Optional[_Iterable[_Union[AmuletRoundResult, _Mapping]]] = ..., point_coin: _Optional[int] = ..., level_coin: _Optional[int] = ..., shop: _Optional[_Union[AmuletGameShopData, _Mapping]] = ..., hook_effect: _Optional[_Iterable[_Union[AmuletActivityHookEffect, _Mapping]]] = ...) -> None: ...

class QuestionnaireReward(_message.Message):
    __slots__ = ["resource_id", "count"]
    RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    resource_id: int
    count: int
    def __init__(self, resource_id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class QuestionnaireDetail(_message.Message):
    __slots__ = ["id", "version_id", "effective_time_start", "effective_time_end", "rewards", "banner_title", "title", "announcement_title", "announcement_content", "final_text", "questions"]
    ID_FIELD_NUMBER: _ClassVar[int]
    VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    EFFECTIVE_TIME_START_FIELD_NUMBER: _ClassVar[int]
    EFFECTIVE_TIME_END_FIELD_NUMBER: _ClassVar[int]
    REWARDS_FIELD_NUMBER: _ClassVar[int]
    BANNER_TITLE_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    ANNOUNCEMENT_TITLE_FIELD_NUMBER: _ClassVar[int]
    ANNOUNCEMENT_CONTENT_FIELD_NUMBER: _ClassVar[int]
    FINAL_TEXT_FIELD_NUMBER: _ClassVar[int]
    QUESTIONS_FIELD_NUMBER: _ClassVar[int]
    id: int
    version_id: int
    effective_time_start: int
    effective_time_end: int
    rewards: _containers.RepeatedCompositeFieldContainer[QuestionnaireReward]
    banner_title: str
    title: str
    announcement_title: str
    announcement_content: str
    final_text: str
    questions: _containers.RepeatedCompositeFieldContainer[QuestionnaireQuestion]
    def __init__(self, id: _Optional[int] = ..., version_id: _Optional[int] = ..., effective_time_start: _Optional[int] = ..., effective_time_end: _Optional[int] = ..., rewards: _Optional[_Iterable[_Union[QuestionnaireReward, _Mapping]]] = ..., banner_title: _Optional[str] = ..., title: _Optional[str] = ..., announcement_title: _Optional[str] = ..., announcement_content: _Optional[str] = ..., final_text: _Optional[str] = ..., questions: _Optional[_Iterable[_Union[QuestionnaireQuestion, _Mapping]]] = ...) -> None: ...

class QuestionnaireQuestion(_message.Message):
    __slots__ = ["id", "title", "describe", "type", "sub_type", "options", "option_random_sort", "require", "max_choice", "next_question", "matrix_row"]
    class QuestionOption(_message.Message):
        __slots__ = ["label", "value", "allow_input"]
        LABEL_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        ALLOW_INPUT_FIELD_NUMBER: _ClassVar[int]
        label: str
        value: str
        allow_input: bool
        def __init__(self, label: _Optional[str] = ..., value: _Optional[str] = ..., allow_input: bool = ...) -> None: ...
    class NextQuestionData(_message.Message):
        __slots__ = ["target_question_id", "conditions"]
        class QuestionCondition(_message.Message):
            __slots__ = ["question_id", "op", "values"]
            QUESTION_ID_FIELD_NUMBER: _ClassVar[int]
            OP_FIELD_NUMBER: _ClassVar[int]
            VALUES_FIELD_NUMBER: _ClassVar[int]
            question_id: int
            op: str
            values: _containers.RepeatedScalarFieldContainer[str]
            def __init__(self, question_id: _Optional[int] = ..., op: _Optional[str] = ..., values: _Optional[_Iterable[str]] = ...) -> None: ...
        class QuestionconditionWrapper(_message.Message):
            __slots__ = ["conditions"]
            CONDITIONS_FIELD_NUMBER: _ClassVar[int]
            conditions: _containers.RepeatedCompositeFieldContainer[QuestionnaireQuestion.NextQuestionData.QuestionCondition]
            def __init__(self, conditions: _Optional[_Iterable[_Union[QuestionnaireQuestion.NextQuestionData.QuestionCondition, _Mapping]]] = ...) -> None: ...
        TARGET_QUESTION_ID_FIELD_NUMBER: _ClassVar[int]
        CONDITIONS_FIELD_NUMBER: _ClassVar[int]
        target_question_id: int
        conditions: _containers.RepeatedCompositeFieldContainer[QuestionnaireQuestion.NextQuestionData.QuestionconditionWrapper]
        def __init__(self, target_question_id: _Optional[int] = ..., conditions: _Optional[_Iterable[_Union[QuestionnaireQuestion.NextQuestionData.QuestionconditionWrapper, _Mapping]]] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIBE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    SUB_TYPE_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    OPTION_RANDOM_SORT_FIELD_NUMBER: _ClassVar[int]
    REQUIRE_FIELD_NUMBER: _ClassVar[int]
    MAX_CHOICE_FIELD_NUMBER: _ClassVar[int]
    NEXT_QUESTION_FIELD_NUMBER: _ClassVar[int]
    MATRIX_ROW_FIELD_NUMBER: _ClassVar[int]
    id: int
    title: str
    describe: str
    type: str
    sub_type: str
    options: _containers.RepeatedCompositeFieldContainer[QuestionnaireQuestion.QuestionOption]
    option_random_sort: bool
    require: bool
    max_choice: int
    next_question: _containers.RepeatedCompositeFieldContainer[QuestionnaireQuestion.NextQuestionData]
    matrix_row: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[int] = ..., title: _Optional[str] = ..., describe: _Optional[str] = ..., type: _Optional[str] = ..., sub_type: _Optional[str] = ..., options: _Optional[_Iterable[_Union[QuestionnaireQuestion.QuestionOption, _Mapping]]] = ..., option_random_sort: bool = ..., require: bool = ..., max_choice: _Optional[int] = ..., next_question: _Optional[_Iterable[_Union[QuestionnaireQuestion.NextQuestionData, _Mapping]]] = ..., matrix_row: _Optional[_Iterable[str]] = ...) -> None: ...

class QuestionnaireBrief(_message.Message):
    __slots__ = ["id", "version_id", "effective_time_start", "effective_time_end", "rewards", "banner_title", "title"]
    ID_FIELD_NUMBER: _ClassVar[int]
    VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    EFFECTIVE_TIME_START_FIELD_NUMBER: _ClassVar[int]
    EFFECTIVE_TIME_END_FIELD_NUMBER: _ClassVar[int]
    REWARDS_FIELD_NUMBER: _ClassVar[int]
    BANNER_TITLE_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    id: int
    version_id: int
    effective_time_start: int
    effective_time_end: int
    rewards: _containers.RepeatedCompositeFieldContainer[QuestionnaireReward]
    banner_title: str
    title: str
    def __init__(self, id: _Optional[int] = ..., version_id: _Optional[int] = ..., effective_time_start: _Optional[int] = ..., effective_time_end: _Optional[int] = ..., rewards: _Optional[_Iterable[_Union[QuestionnaireReward, _Mapping]]] = ..., banner_title: _Optional[str] = ..., title: _Optional[str] = ...) -> None: ...

class ResConnectionInfo(_message.Message):
    __slots__ = ["error", "client_endpoint"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    error: Error
    client_endpoint: NetworkEndpoint
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., client_endpoint: _Optional[_Union[NetworkEndpoint, _Mapping]] = ...) -> None: ...

class ResFetchQueueInfo(_message.Message):
    __slots__ = ["error", "remain", "rank"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    REMAIN_FIELD_NUMBER: _ClassVar[int]
    RANK_FIELD_NUMBER: _ClassVar[int]
    error: Error
    remain: int
    rank: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., remain: _Optional[int] = ..., rank: _Optional[int] = ...) -> None: ...

class ReqOpenidCheck(_message.Message):
    __slots__ = ["type", "token"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    type: int
    token: str
    def __init__(self, type: _Optional[int] = ..., token: _Optional[str] = ...) -> None: ...

class ReqSignupAccount(_message.Message):
    __slots__ = ["account", "password", "code", "type", "device", "client_version_string", "tag"]
    ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    DEVICE_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    account: str
    password: str
    code: str
    type: int
    device: ClientDeviceInfo
    client_version_string: str
    tag: str
    def __init__(self, account: _Optional[str] = ..., password: _Optional[str] = ..., code: _Optional[str] = ..., type: _Optional[int] = ..., device: _Optional[_Union[ClientDeviceInfo, _Mapping]] = ..., client_version_string: _Optional[str] = ..., tag: _Optional[str] = ...) -> None: ...

class ResSignupAccount(_message.Message):
    __slots__ = ["error"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    error: Error
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class ReqLogin(_message.Message):
    __slots__ = ["account", "password", "reconnect", "device", "random_key", "client_version", "gen_access_token", "currency_platforms", "type", "version", "client_version_string", "tag"]
    ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    RECONNECT_FIELD_NUMBER: _ClassVar[int]
    DEVICE_FIELD_NUMBER: _ClassVar[int]
    RANDOM_KEY_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_FIELD_NUMBER: _ClassVar[int]
    GEN_ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_PLATFORMS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    account: str
    password: str
    reconnect: bool
    device: ClientDeviceInfo
    random_key: str
    client_version: ClientVersionInfo
    gen_access_token: bool
    currency_platforms: _containers.RepeatedScalarFieldContainer[int]
    type: int
    version: int
    client_version_string: str
    tag: str
    def __init__(self, account: _Optional[str] = ..., password: _Optional[str] = ..., reconnect: bool = ..., device: _Optional[_Union[ClientDeviceInfo, _Mapping]] = ..., random_key: _Optional[str] = ..., client_version: _Optional[_Union[ClientVersionInfo, _Mapping]] = ..., gen_access_token: bool = ..., currency_platforms: _Optional[_Iterable[int]] = ..., type: _Optional[int] = ..., version: _Optional[int] = ..., client_version_string: _Optional[str] = ..., tag: _Optional[str] = ...) -> None: ...

class ResLogin(_message.Message):
    __slots__ = ["error", "account_id", "account", "game_info", "has_unread_announcement", "access_token", "signup_time", "is_id_card_authed", "country", "logined_version", "rewarded_version"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    GAME_INFO_FIELD_NUMBER: _ClassVar[int]
    HAS_UNREAD_ANNOUNCEMENT_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    SIGNUP_TIME_FIELD_NUMBER: _ClassVar[int]
    IS_ID_CARD_AUTHED_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_FIELD_NUMBER: _ClassVar[int]
    LOGINED_VERSION_FIELD_NUMBER: _ClassVar[int]
    REWARDED_VERSION_FIELD_NUMBER: _ClassVar[int]
    error: Error
    account_id: int
    account: Account
    game_info: GameConnectInfo
    has_unread_announcement: bool
    access_token: str
    signup_time: int
    is_id_card_authed: bool
    country: str
    logined_version: _containers.RepeatedScalarFieldContainer[int]
    rewarded_version: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., account_id: _Optional[int] = ..., account: _Optional[_Union[Account, _Mapping]] = ..., game_info: _Optional[_Union[GameConnectInfo, _Mapping]] = ..., has_unread_announcement: bool = ..., access_token: _Optional[str] = ..., signup_time: _Optional[int] = ..., is_id_card_authed: bool = ..., country: _Optional[str] = ..., logined_version: _Optional[_Iterable[int]] = ..., rewarded_version: _Optional[_Iterable[int]] = ...) -> None: ...

class ReqEmailLogin(_message.Message):
    __slots__ = ["email", "password", "reconnect", "device", "random_key", "client_version", "gen_access_token", "currency_platforms"]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    RECONNECT_FIELD_NUMBER: _ClassVar[int]
    DEVICE_FIELD_NUMBER: _ClassVar[int]
    RANDOM_KEY_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_FIELD_NUMBER: _ClassVar[int]
    GEN_ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_PLATFORMS_FIELD_NUMBER: _ClassVar[int]
    email: str
    password: str
    reconnect: bool
    device: ClientDeviceInfo
    random_key: str
    client_version: str
    gen_access_token: bool
    currency_platforms: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, email: _Optional[str] = ..., password: _Optional[str] = ..., reconnect: bool = ..., device: _Optional[_Union[ClientDeviceInfo, _Mapping]] = ..., random_key: _Optional[str] = ..., client_version: _Optional[str] = ..., gen_access_token: bool = ..., currency_platforms: _Optional[_Iterable[int]] = ...) -> None: ...

class ReqBindAccount(_message.Message):
    __slots__ = ["account", "password"]
    ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    account: str
    password: str
    def __init__(self, account: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class ReqCreatePhoneVerifyCode(_message.Message):
    __slots__ = ["phone", "usage"]
    PHONE_FIELD_NUMBER: _ClassVar[int]
    USAGE_FIELD_NUMBER: _ClassVar[int]
    phone: str
    usage: int
    def __init__(self, phone: _Optional[str] = ..., usage: _Optional[int] = ...) -> None: ...

class ReqCreateEmailVerifyCode(_message.Message):
    __slots__ = ["email", "usage"]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    USAGE_FIELD_NUMBER: _ClassVar[int]
    email: str
    usage: int
    def __init__(self, email: _Optional[str] = ..., usage: _Optional[int] = ...) -> None: ...

class ReqVerifyCodeForSecure(_message.Message):
    __slots__ = ["code", "operation"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    code: str
    operation: int
    def __init__(self, code: _Optional[str] = ..., operation: _Optional[int] = ...) -> None: ...

class ResVerfiyCodeForSecure(_message.Message):
    __slots__ = ["error", "secure_token"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    SECURE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    error: Error
    secure_token: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., secure_token: _Optional[str] = ...) -> None: ...

class ReqBindPhoneNumber(_message.Message):
    __slots__ = ["code", "phone", "password", "multi_bind_version"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    PHONE_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    MULTI_BIND_VERSION_FIELD_NUMBER: _ClassVar[int]
    code: str
    phone: str
    password: str
    multi_bind_version: bool
    def __init__(self, code: _Optional[str] = ..., phone: _Optional[str] = ..., password: _Optional[str] = ..., multi_bind_version: bool = ...) -> None: ...

class ReqUnbindPhoneNumber(_message.Message):
    __slots__ = ["code", "phone", "password"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    PHONE_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    code: str
    phone: str
    password: str
    def __init__(self, code: _Optional[str] = ..., phone: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class ResFetchPhoneLoginBind(_message.Message):
    __slots__ = ["error", "phone_login"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    PHONE_LOGIN_FIELD_NUMBER: _ClassVar[int]
    error: Error
    phone_login: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., phone_login: _Optional[int] = ...) -> None: ...

class ReqCreatePhoneLoginBind(_message.Message):
    __slots__ = ["password"]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    password: str
    def __init__(self, password: _Optional[str] = ...) -> None: ...

class ReqBindEmail(_message.Message):
    __slots__ = ["email", "code", "password"]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    email: str
    code: str
    password: str
    def __init__(self, email: _Optional[str] = ..., code: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class ReqModifyPassword(_message.Message):
    __slots__ = ["new_password", "old_password", "secure_token"]
    NEW_PASSWORD_FIELD_NUMBER: _ClassVar[int]
    OLD_PASSWORD_FIELD_NUMBER: _ClassVar[int]
    SECURE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    new_password: str
    old_password: str
    secure_token: str
    def __init__(self, new_password: _Optional[str] = ..., old_password: _Optional[str] = ..., secure_token: _Optional[str] = ...) -> None: ...

class ReqOauth2Auth(_message.Message):
    __slots__ = ["type", "code", "uid", "client_version_string"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    UID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    type: int
    code: str
    uid: str
    client_version_string: str
    def __init__(self, type: _Optional[int] = ..., code: _Optional[str] = ..., uid: _Optional[str] = ..., client_version_string: _Optional[str] = ...) -> None: ...

class ResOauth2Auth(_message.Message):
    __slots__ = ["error", "access_token"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    error: Error
    access_token: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., access_token: _Optional[str] = ...) -> None: ...

class ReqOauth2Check(_message.Message):
    __slots__ = ["type", "access_token"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    type: int
    access_token: str
    def __init__(self, type: _Optional[int] = ..., access_token: _Optional[str] = ...) -> None: ...

class ResOauth2Check(_message.Message):
    __slots__ = ["error", "has_account"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    HAS_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    error: Error
    has_account: bool
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., has_account: bool = ...) -> None: ...

class ReqOauth2Signup(_message.Message):
    __slots__ = ["type", "access_token", "email", "advertise_str", "device", "client_version", "client_version_string", "tag"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    ADVERTISE_STR_FIELD_NUMBER: _ClassVar[int]
    DEVICE_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    type: int
    access_token: str
    email: str
    advertise_str: str
    device: ClientDeviceInfo
    client_version: ClientVersionInfo
    client_version_string: str
    tag: str
    def __init__(self, type: _Optional[int] = ..., access_token: _Optional[str] = ..., email: _Optional[str] = ..., advertise_str: _Optional[str] = ..., device: _Optional[_Union[ClientDeviceInfo, _Mapping]] = ..., client_version: _Optional[_Union[ClientVersionInfo, _Mapping]] = ..., client_version_string: _Optional[str] = ..., tag: _Optional[str] = ...) -> None: ...

class ResOauth2Signup(_message.Message):
    __slots__ = ["error"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    error: Error
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class ReqOauth2Login(_message.Message):
    __slots__ = ["type", "access_token", "reconnect", "device", "random_key", "client_version", "gen_access_token", "currency_platforms", "version", "client_version_string", "tag"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    RECONNECT_FIELD_NUMBER: _ClassVar[int]
    DEVICE_FIELD_NUMBER: _ClassVar[int]
    RANDOM_KEY_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_FIELD_NUMBER: _ClassVar[int]
    GEN_ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_PLATFORMS_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    type: int
    access_token: str
    reconnect: bool
    device: ClientDeviceInfo
    random_key: str
    client_version: ClientVersionInfo
    gen_access_token: bool
    currency_platforms: _containers.RepeatedScalarFieldContainer[int]
    version: int
    client_version_string: str
    tag: str
    def __init__(self, type: _Optional[int] = ..., access_token: _Optional[str] = ..., reconnect: bool = ..., device: _Optional[_Union[ClientDeviceInfo, _Mapping]] = ..., random_key: _Optional[str] = ..., client_version: _Optional[_Union[ClientVersionInfo, _Mapping]] = ..., gen_access_token: bool = ..., currency_platforms: _Optional[_Iterable[int]] = ..., version: _Optional[int] = ..., client_version_string: _Optional[str] = ..., tag: _Optional[str] = ...) -> None: ...

class ReqDMMPreLogin(_message.Message):
    __slots__ = ["finish_url"]
    FINISH_URL_FIELD_NUMBER: _ClassVar[int]
    finish_url: str
    def __init__(self, finish_url: _Optional[str] = ...) -> None: ...

class ResDMMPreLogin(_message.Message):
    __slots__ = ["error", "parameter"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    PARAMETER_FIELD_NUMBER: _ClassVar[int]
    error: Error
    parameter: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., parameter: _Optional[str] = ...) -> None: ...

class ReqLogout(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ResLogout(_message.Message):
    __slots__ = ["error"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    error: Error
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class ReqHeatBeat(_message.Message):
    __slots__ = ["no_operation_counter"]
    NO_OPERATION_COUNTER_FIELD_NUMBER: _ClassVar[int]
    no_operation_counter: int
    def __init__(self, no_operation_counter: _Optional[int] = ...) -> None: ...

class ReqLoginBeat(_message.Message):
    __slots__ = ["contract"]
    CONTRACT_FIELD_NUMBER: _ClassVar[int]
    contract: str
    def __init__(self, contract: _Optional[str] = ...) -> None: ...

class ReqJoinMatchQueue(_message.Message):
    __slots__ = ["match_mode", "client_version_string"]
    MATCH_MODE_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    match_mode: int
    client_version_string: str
    def __init__(self, match_mode: _Optional[int] = ..., client_version_string: _Optional[str] = ...) -> None: ...

class ReqCancelMatchQueue(_message.Message):
    __slots__ = ["match_mode"]
    MATCH_MODE_FIELD_NUMBER: _ClassVar[int]
    match_mode: int
    def __init__(self, match_mode: _Optional[int] = ...) -> None: ...

class ReqAccountInfo(_message.Message):
    __slots__ = ["account_id"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    def __init__(self, account_id: _Optional[int] = ...) -> None: ...

class ResAccountInfo(_message.Message):
    __slots__ = ["error", "account", "room"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    ROOM_FIELD_NUMBER: _ClassVar[int]
    error: Error
    account: Account
    room: Room
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., account: _Optional[_Union[Account, _Mapping]] = ..., room: _Optional[_Union[Room, _Mapping]] = ...) -> None: ...

class ReqCreateNickname(_message.Message):
    __slots__ = ["nickname", "advertise_str", "tag"]
    NICKNAME_FIELD_NUMBER: _ClassVar[int]
    ADVERTISE_STR_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    nickname: str
    advertise_str: str
    tag: str
    def __init__(self, nickname: _Optional[str] = ..., advertise_str: _Optional[str] = ..., tag: _Optional[str] = ...) -> None: ...

class ReqModifyNickname(_message.Message):
    __slots__ = ["nickname", "use_item_id"]
    NICKNAME_FIELD_NUMBER: _ClassVar[int]
    USE_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    nickname: str
    use_item_id: int
    def __init__(self, nickname: _Optional[str] = ..., use_item_id: _Optional[int] = ...) -> None: ...

class ReqModifyBirthday(_message.Message):
    __slots__ = ["birthday"]
    BIRTHDAY_FIELD_NUMBER: _ClassVar[int]
    birthday: int
    def __init__(self, birthday: _Optional[int] = ...) -> None: ...

class ResSelfRoom(_message.Message):
    __slots__ = ["error", "room"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ROOM_FIELD_NUMBER: _ClassVar[int]
    error: Error
    room: Room
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., room: _Optional[_Union[Room, _Mapping]] = ...) -> None: ...

class ResFetchGamingInfo(_message.Message):
    __slots__ = ["error", "game_info"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    GAME_INFO_FIELD_NUMBER: _ClassVar[int]
    error: Error
    game_info: GameConnectInfo
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., game_info: _Optional[_Union[GameConnectInfo, _Mapping]] = ...) -> None: ...

class ReqCreateRoom(_message.Message):
    __slots__ = ["player_count", "mode", "public_live", "client_version_string", "pre_rule"]
    PLAYER_COUNT_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_LIVE_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    PRE_RULE_FIELD_NUMBER: _ClassVar[int]
    player_count: int
    mode: GameMode
    public_live: bool
    client_version_string: str
    pre_rule: str
    def __init__(self, player_count: _Optional[int] = ..., mode: _Optional[_Union[GameMode, _Mapping]] = ..., public_live: bool = ..., client_version_string: _Optional[str] = ..., pre_rule: _Optional[str] = ...) -> None: ...

class ResCreateRoom(_message.Message):
    __slots__ = ["error", "room"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ROOM_FIELD_NUMBER: _ClassVar[int]
    error: Error
    room: Room
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., room: _Optional[_Union[Room, _Mapping]] = ...) -> None: ...

class ReqJoinRoom(_message.Message):
    __slots__ = ["room_id", "client_version_string"]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    room_id: int
    client_version_string: str
    def __init__(self, room_id: _Optional[int] = ..., client_version_string: _Optional[str] = ...) -> None: ...

class ResJoinRoom(_message.Message):
    __slots__ = ["error", "room"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ROOM_FIELD_NUMBER: _ClassVar[int]
    error: Error
    room: Room
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., room: _Optional[_Union[Room, _Mapping]] = ...) -> None: ...

class ReqRoomReady(_message.Message):
    __slots__ = ["ready"]
    READY_FIELD_NUMBER: _ClassVar[int]
    ready: bool
    def __init__(self, ready: bool = ...) -> None: ...

class ReqRoomDressing(_message.Message):
    __slots__ = ["dressing"]
    DRESSING_FIELD_NUMBER: _ClassVar[int]
    dressing: bool
    def __init__(self, dressing: bool = ...) -> None: ...

class ReqRoomStart(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ReqRoomKick(_message.Message):
    __slots__ = ["account_id"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    def __init__(self, account_id: _Optional[int] = ...) -> None: ...

class ReqModifyRoom(_message.Message):
    __slots__ = ["robot_count"]
    ROBOT_COUNT_FIELD_NUMBER: _ClassVar[int]
    robot_count: int
    def __init__(self, robot_count: _Optional[int] = ...) -> None: ...

class ReqChangeAvatar(_message.Message):
    __slots__ = ["avatar_id"]
    AVATAR_ID_FIELD_NUMBER: _ClassVar[int]
    avatar_id: int
    def __init__(self, avatar_id: _Optional[int] = ...) -> None: ...

class ReqAccountStatisticInfo(_message.Message):
    __slots__ = ["account_id"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    def __init__(self, account_id: _Optional[int] = ...) -> None: ...

class ResAccountStatisticInfo(_message.Message):
    __slots__ = ["error", "statistic_data", "detail_data"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    STATISTIC_DATA_FIELD_NUMBER: _ClassVar[int]
    DETAIL_DATA_FIELD_NUMBER: _ClassVar[int]
    error: Error
    statistic_data: _containers.RepeatedCompositeFieldContainer[AccountStatisticData]
    detail_data: AccountDetailStatisticV2
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., statistic_data: _Optional[_Iterable[_Union[AccountStatisticData, _Mapping]]] = ..., detail_data: _Optional[_Union[AccountDetailStatisticV2, _Mapping]] = ...) -> None: ...

class ResAccountChallengeRankInfo(_message.Message):
    __slots__ = ["error", "season_info"]
    class ChallengeRank(_message.Message):
        __slots__ = ["season", "rank", "level"]
        SEASON_FIELD_NUMBER: _ClassVar[int]
        RANK_FIELD_NUMBER: _ClassVar[int]
        LEVEL_FIELD_NUMBER: _ClassVar[int]
        season: int
        rank: int
        level: int
        def __init__(self, season: _Optional[int] = ..., rank: _Optional[int] = ..., level: _Optional[int] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    SEASON_INFO_FIELD_NUMBER: _ClassVar[int]
    error: Error
    season_info: _containers.RepeatedCompositeFieldContainer[ResAccountChallengeRankInfo.ChallengeRank]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., season_info: _Optional[_Iterable[_Union[ResAccountChallengeRankInfo.ChallengeRank, _Mapping]]] = ...) -> None: ...

class ResAccountCharacterInfo(_message.Message):
    __slots__ = ["error", "unlock_list"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    UNLOCK_LIST_FIELD_NUMBER: _ClassVar[int]
    error: Error
    unlock_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., unlock_list: _Optional[_Iterable[int]] = ...) -> None: ...

class ReqShopPurchase(_message.Message):
    __slots__ = ["type", "id"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    type: str
    id: int
    def __init__(self, type: _Optional[str] = ..., id: _Optional[int] = ...) -> None: ...

class ResShopPurchase(_message.Message):
    __slots__ = ["error", "update"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    UPDATE_FIELD_NUMBER: _ClassVar[int]
    error: Error
    update: AccountUpdate
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., update: _Optional[_Union[AccountUpdate, _Mapping]] = ...) -> None: ...

class ReqGameRecord(_message.Message):
    __slots__ = ["game_uuid", "client_version_string"]
    GAME_UUID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    game_uuid: str
    client_version_string: str
    def __init__(self, game_uuid: _Optional[str] = ..., client_version_string: _Optional[str] = ...) -> None: ...

class ResGameRecord(_message.Message):
    __slots__ = ["error", "head", "data", "data_url"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    HEAD_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    DATA_URL_FIELD_NUMBER: _ClassVar[int]
    error: Error
    head: RecordGame
    data: bytes
    data_url: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., head: _Optional[_Union[RecordGame, _Mapping]] = ..., data: _Optional[bytes] = ..., data_url: _Optional[str] = ...) -> None: ...

class ReqGameRecordList(_message.Message):
    __slots__ = ["start", "count", "type"]
    START_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    start: int
    count: int
    type: int
    def __init__(self, start: _Optional[int] = ..., count: _Optional[int] = ..., type: _Optional[int] = ...) -> None: ...

class ResGameRecordList(_message.Message):
    __slots__ = ["error", "total_count", "record_list"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    RECORD_LIST_FIELD_NUMBER: _ClassVar[int]
    error: Error
    total_count: int
    record_list: _containers.RepeatedCompositeFieldContainer[RecordGame]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., total_count: _Optional[int] = ..., record_list: _Optional[_Iterable[_Union[RecordGame, _Mapping]]] = ...) -> None: ...

class ReqGameRecordListV2(_message.Message):
    __slots__ = ["tag", "begin_time", "end_time", "ranks", "modes", "max_hu_type", "level_mode"]
    TAG_FIELD_NUMBER: _ClassVar[int]
    BEGIN_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    RANKS_FIELD_NUMBER: _ClassVar[int]
    MODES_FIELD_NUMBER: _ClassVar[int]
    MAX_HU_TYPE_FIELD_NUMBER: _ClassVar[int]
    LEVEL_MODE_FIELD_NUMBER: _ClassVar[int]
    tag: int
    begin_time: int
    end_time: int
    ranks: _containers.RepeatedScalarFieldContainer[int]
    modes: _containers.RepeatedScalarFieldContainer[int]
    max_hu_type: int
    level_mode: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, tag: _Optional[int] = ..., begin_time: _Optional[int] = ..., end_time: _Optional[int] = ..., ranks: _Optional[_Iterable[int]] = ..., modes: _Optional[_Iterable[int]] = ..., max_hu_type: _Optional[int] = ..., level_mode: _Optional[_Iterable[int]] = ...) -> None: ...

class ResGameRecordListV2(_message.Message):
    __slots__ = ["error", "iterator", "iterator_expire", "actual_begin_time", "actual_end_time"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ITERATOR_FIELD_NUMBER: _ClassVar[int]
    ITERATOR_EXPIRE_FIELD_NUMBER: _ClassVar[int]
    ACTUAL_BEGIN_TIME_FIELD_NUMBER: _ClassVar[int]
    ACTUAL_END_TIME_FIELD_NUMBER: _ClassVar[int]
    error: Error
    iterator: str
    iterator_expire: int
    actual_begin_time: int
    actual_end_time: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., iterator: _Optional[str] = ..., iterator_expire: _Optional[int] = ..., actual_begin_time: _Optional[int] = ..., actual_end_time: _Optional[int] = ...) -> None: ...

class ReqNextGameRecordList(_message.Message):
    __slots__ = ["iterator", "count"]
    ITERATOR_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    iterator: str
    count: int
    def __init__(self, iterator: _Optional[str] = ..., count: _Optional[int] = ...) -> None: ...

class ResNextGameRecordList(_message.Message):
    __slots__ = ["error", "next", "entries", "iterator_expire", "next_end_time"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    NEXT_FIELD_NUMBER: _ClassVar[int]
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    ITERATOR_EXPIRE_FIELD_NUMBER: _ClassVar[int]
    NEXT_END_TIME_FIELD_NUMBER: _ClassVar[int]
    error: Error
    next: bool
    entries: _containers.RepeatedCompositeFieldContainer[RecordListEntry]
    iterator_expire: int
    next_end_time: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., next: bool = ..., entries: _Optional[_Iterable[_Union[RecordListEntry, _Mapping]]] = ..., iterator_expire: _Optional[int] = ..., next_end_time: _Optional[int] = ...) -> None: ...

class ResCollectedGameRecordList(_message.Message):
    __slots__ = ["error", "record_list", "record_collect_limit"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    RECORD_LIST_FIELD_NUMBER: _ClassVar[int]
    RECORD_COLLECT_LIMIT_FIELD_NUMBER: _ClassVar[int]
    error: Error
    record_list: _containers.RepeatedCompositeFieldContainer[RecordCollectedData]
    record_collect_limit: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., record_list: _Optional[_Iterable[_Union[RecordCollectedData, _Mapping]]] = ..., record_collect_limit: _Optional[int] = ...) -> None: ...

class ReqGameRecordsDetail(_message.Message):
    __slots__ = ["uuid_list"]
    UUID_LIST_FIELD_NUMBER: _ClassVar[int]
    uuid_list: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, uuid_list: _Optional[_Iterable[str]] = ...) -> None: ...

class ResGameRecordsDetail(_message.Message):
    __slots__ = ["error", "record_list"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    RECORD_LIST_FIELD_NUMBER: _ClassVar[int]
    error: Error
    record_list: _containers.RepeatedCompositeFieldContainer[RecordGame]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., record_list: _Optional[_Iterable[_Union[RecordGame, _Mapping]]] = ...) -> None: ...

class ReqGameRecordsDetailV2(_message.Message):
    __slots__ = ["uuid_list"]
    UUID_LIST_FIELD_NUMBER: _ClassVar[int]
    uuid_list: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, uuid_list: _Optional[_Iterable[str]] = ...) -> None: ...

class ResGameRecordsDetailV2(_message.Message):
    __slots__ = ["error", "entries"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    error: Error
    entries: _containers.RepeatedCompositeFieldContainer[RecordListEntry]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., entries: _Optional[_Iterable[_Union[RecordListEntry, _Mapping]]] = ...) -> None: ...

class ReqAddCollectedGameRecord(_message.Message):
    __slots__ = ["uuid", "remarks", "start_time", "end_time"]
    UUID_FIELD_NUMBER: _ClassVar[int]
    REMARKS_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    remarks: str
    start_time: int
    end_time: int
    def __init__(self, uuid: _Optional[str] = ..., remarks: _Optional[str] = ..., start_time: _Optional[int] = ..., end_time: _Optional[int] = ...) -> None: ...

class ResAddCollectedGameRecord(_message.Message):
    __slots__ = ["error"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    error: Error
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class ReqRemoveCollectedGameRecord(_message.Message):
    __slots__ = ["uuid"]
    UUID_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    def __init__(self, uuid: _Optional[str] = ...) -> None: ...

class ResRemoveCollectedGameRecord(_message.Message):
    __slots__ = ["error"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    error: Error
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class ReqChangeCollectedGameRecordRemarks(_message.Message):
    __slots__ = ["uuid", "remarks"]
    UUID_FIELD_NUMBER: _ClassVar[int]
    REMARKS_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    remarks: str
    def __init__(self, uuid: _Optional[str] = ..., remarks: _Optional[str] = ...) -> None: ...

class ResChangeCollectedGameRecordRemarks(_message.Message):
    __slots__ = ["error"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    error: Error
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class ReqLevelLeaderboard(_message.Message):
    __slots__ = ["type"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    type: int
    def __init__(self, type: _Optional[int] = ...) -> None: ...

class ResLevelLeaderboard(_message.Message):
    __slots__ = ["error", "items", "self_rank"]
    class Item(_message.Message):
        __slots__ = ["account_id", "level"]
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        LEVEL_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        level: AccountLevel
        def __init__(self, account_id: _Optional[int] = ..., level: _Optional[_Union[AccountLevel, _Mapping]] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    SELF_RANK_FIELD_NUMBER: _ClassVar[int]
    error: Error
    items: _containers.RepeatedCompositeFieldContainer[ResLevelLeaderboard.Item]
    self_rank: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., items: _Optional[_Iterable[_Union[ResLevelLeaderboard.Item, _Mapping]]] = ..., self_rank: _Optional[int] = ...) -> None: ...

class ReqChallangeLeaderboard(_message.Message):
    __slots__ = ["season"]
    SEASON_FIELD_NUMBER: _ClassVar[int]
    season: int
    def __init__(self, season: _Optional[int] = ...) -> None: ...

class ResChallengeLeaderboard(_message.Message):
    __slots__ = ["error", "items", "self_rank"]
    class Item(_message.Message):
        __slots__ = ["account_id", "level", "nickname"]
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        LEVEL_FIELD_NUMBER: _ClassVar[int]
        NICKNAME_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        level: int
        nickname: str
        def __init__(self, account_id: _Optional[int] = ..., level: _Optional[int] = ..., nickname: _Optional[str] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    SELF_RANK_FIELD_NUMBER: _ClassVar[int]
    error: Error
    items: _containers.RepeatedCompositeFieldContainer[ResChallengeLeaderboard.Item]
    self_rank: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., items: _Optional[_Iterable[_Union[ResChallengeLeaderboard.Item, _Mapping]]] = ..., self_rank: _Optional[int] = ...) -> None: ...

class ReqMutiChallengeLevel(_message.Message):
    __slots__ = ["account_id_list", "season"]
    ACCOUNT_ID_LIST_FIELD_NUMBER: _ClassVar[int]
    SEASON_FIELD_NUMBER: _ClassVar[int]
    account_id_list: _containers.RepeatedScalarFieldContainer[int]
    season: int
    def __init__(self, account_id_list: _Optional[_Iterable[int]] = ..., season: _Optional[int] = ...) -> None: ...

class ResMutiChallengeLevel(_message.Message):
    __slots__ = ["error", "items"]
    class Item(_message.Message):
        __slots__ = ["account_id", "level"]
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        LEVEL_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        level: int
        def __init__(self, account_id: _Optional[int] = ..., level: _Optional[int] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    items: _containers.RepeatedCompositeFieldContainer[ResMutiChallengeLevel.Item]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., items: _Optional[_Iterable[_Union[ResMutiChallengeLevel.Item, _Mapping]]] = ...) -> None: ...

class ReqMultiAccountId(_message.Message):
    __slots__ = ["account_id_list"]
    ACCOUNT_ID_LIST_FIELD_NUMBER: _ClassVar[int]
    account_id_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, account_id_list: _Optional[_Iterable[int]] = ...) -> None: ...

class ResMultiAccountBrief(_message.Message):
    __slots__ = ["error", "players"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    players: _containers.RepeatedCompositeFieldContainer[PlayerBaseView]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., players: _Optional[_Iterable[_Union[PlayerBaseView, _Mapping]]] = ...) -> None: ...

class ResFriendList(_message.Message):
    __slots__ = ["error", "friends", "friend_max_count", "friend_count"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    FRIENDS_FIELD_NUMBER: _ClassVar[int]
    FRIEND_MAX_COUNT_FIELD_NUMBER: _ClassVar[int]
    FRIEND_COUNT_FIELD_NUMBER: _ClassVar[int]
    error: Error
    friends: _containers.RepeatedCompositeFieldContainer[Friend]
    friend_max_count: int
    friend_count: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., friends: _Optional[_Iterable[_Union[Friend, _Mapping]]] = ..., friend_max_count: _Optional[int] = ..., friend_count: _Optional[int] = ...) -> None: ...

class ResFriendApplyList(_message.Message):
    __slots__ = ["error", "applies"]
    class FriendApply(_message.Message):
        __slots__ = ["account_id", "apply_time"]
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        APPLY_TIME_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        apply_time: int
        def __init__(self, account_id: _Optional[int] = ..., apply_time: _Optional[int] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    APPLIES_FIELD_NUMBER: _ClassVar[int]
    error: Error
    applies: _containers.RepeatedCompositeFieldContainer[ResFriendApplyList.FriendApply]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., applies: _Optional[_Iterable[_Union[ResFriendApplyList.FriendApply, _Mapping]]] = ...) -> None: ...

class ReqApplyFriend(_message.Message):
    __slots__ = ["target_id"]
    TARGET_ID_FIELD_NUMBER: _ClassVar[int]
    target_id: int
    def __init__(self, target_id: _Optional[int] = ...) -> None: ...

class ReqHandleFriendApply(_message.Message):
    __slots__ = ["target_id", "method"]
    TARGET_ID_FIELD_NUMBER: _ClassVar[int]
    METHOD_FIELD_NUMBER: _ClassVar[int]
    target_id: int
    method: int
    def __init__(self, target_id: _Optional[int] = ..., method: _Optional[int] = ...) -> None: ...

class ReqRemoveFriend(_message.Message):
    __slots__ = ["target_id"]
    TARGET_ID_FIELD_NUMBER: _ClassVar[int]
    target_id: int
    def __init__(self, target_id: _Optional[int] = ...) -> None: ...

class ReqSearchAccountByPattern(_message.Message):
    __slots__ = ["search_next", "pattern"]
    SEARCH_NEXT_FIELD_NUMBER: _ClassVar[int]
    PATTERN_FIELD_NUMBER: _ClassVar[int]
    search_next: bool
    pattern: str
    def __init__(self, search_next: bool = ..., pattern: _Optional[str] = ...) -> None: ...

class ResSearchAccountByPattern(_message.Message):
    __slots__ = ["error", "is_finished", "match_accounts", "decode_id"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    IS_FINISHED_FIELD_NUMBER: _ClassVar[int]
    MATCH_ACCOUNTS_FIELD_NUMBER: _ClassVar[int]
    DECODE_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    is_finished: bool
    match_accounts: _containers.RepeatedScalarFieldContainer[int]
    decode_id: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., is_finished: bool = ..., match_accounts: _Optional[_Iterable[int]] = ..., decode_id: _Optional[int] = ...) -> None: ...

class ReqAccountList(_message.Message):
    __slots__ = ["account_id_list"]
    ACCOUNT_ID_LIST_FIELD_NUMBER: _ClassVar[int]
    account_id_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, account_id_list: _Optional[_Iterable[int]] = ...) -> None: ...

class ResAccountStates(_message.Message):
    __slots__ = ["error", "states"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    STATES_FIELD_NUMBER: _ClassVar[int]
    error: Error
    states: _containers.RepeatedCompositeFieldContainer[AccountActiveState]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., states: _Optional[_Iterable[_Union[AccountActiveState, _Mapping]]] = ...) -> None: ...

class ReqSearchAccountById(_message.Message):
    __slots__ = ["account_id"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    def __init__(self, account_id: _Optional[int] = ...) -> None: ...

class ResSearchAccountById(_message.Message):
    __slots__ = ["error", "player"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    PLAYER_FIELD_NUMBER: _ClassVar[int]
    error: Error
    player: PlayerBaseView
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., player: _Optional[_Union[PlayerBaseView, _Mapping]] = ...) -> None: ...

class ResBagInfo(_message.Message):
    __slots__ = ["error", "bag"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    BAG_FIELD_NUMBER: _ClassVar[int]
    error: Error
    bag: Bag
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., bag: _Optional[_Union[Bag, _Mapping]] = ...) -> None: ...

class ReqUseBagItem(_message.Message):
    __slots__ = ["item_id"]
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    item_id: int
    def __init__(self, item_id: _Optional[int] = ...) -> None: ...

class ReqOpenManualItem(_message.Message):
    __slots__ = ["item_id", "count", "select_id"]
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    SELECT_ID_FIELD_NUMBER: _ClassVar[int]
    item_id: int
    count: int
    select_id: int
    def __init__(self, item_id: _Optional[int] = ..., count: _Optional[int] = ..., select_id: _Optional[int] = ...) -> None: ...

class ReqOpenRandomRewardItem(_message.Message):
    __slots__ = ["item_id"]
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    item_id: int
    def __init__(self, item_id: _Optional[int] = ...) -> None: ...

class ResOpenRandomRewardItem(_message.Message):
    __slots__ = ["error", "results"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    results: _containers.RepeatedCompositeFieldContainer[OpenResult]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., results: _Optional[_Iterable[_Union[OpenResult, _Mapping]]] = ...) -> None: ...

class ReqOpenAllRewardItem(_message.Message):
    __slots__ = ["item_id"]
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    item_id: int
    def __init__(self, item_id: _Optional[int] = ...) -> None: ...

class ResOpenAllRewardItem(_message.Message):
    __slots__ = ["error", "results"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    results: _containers.RepeatedCompositeFieldContainer[OpenResult]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., results: _Optional[_Iterable[_Union[OpenResult, _Mapping]]] = ...) -> None: ...

class ReqComposeShard(_message.Message):
    __slots__ = ["item_id"]
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    item_id: int
    def __init__(self, item_id: _Optional[int] = ...) -> None: ...

class ReqFetchAnnouncement(_message.Message):
    __slots__ = ["lang", "platform"]
    LANG_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_FIELD_NUMBER: _ClassVar[int]
    lang: str
    platform: str
    def __init__(self, lang: _Optional[str] = ..., platform: _Optional[str] = ...) -> None: ...

class ResAnnouncement(_message.Message):
    __slots__ = ["error", "announcements", "sort", "read_list"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ANNOUNCEMENTS_FIELD_NUMBER: _ClassVar[int]
    SORT_FIELD_NUMBER: _ClassVar[int]
    READ_LIST_FIELD_NUMBER: _ClassVar[int]
    error: Error
    announcements: _containers.RepeatedCompositeFieldContainer[Announcement]
    sort: _containers.RepeatedScalarFieldContainer[int]
    read_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., announcements: _Optional[_Iterable[_Union[Announcement, _Mapping]]] = ..., sort: _Optional[_Iterable[int]] = ..., read_list: _Optional[_Iterable[int]] = ...) -> None: ...

class ResMailInfo(_message.Message):
    __slots__ = ["error", "mails"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    MAILS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    mails: _containers.RepeatedCompositeFieldContainer[Mail]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., mails: _Optional[_Iterable[_Union[Mail, _Mapping]]] = ...) -> None: ...

class ReqReadMail(_message.Message):
    __slots__ = ["mail_id"]
    MAIL_ID_FIELD_NUMBER: _ClassVar[int]
    mail_id: int
    def __init__(self, mail_id: _Optional[int] = ...) -> None: ...

class ReqDeleteMail(_message.Message):
    __slots__ = ["mail_id"]
    MAIL_ID_FIELD_NUMBER: _ClassVar[int]
    mail_id: int
    def __init__(self, mail_id: _Optional[int] = ...) -> None: ...

class ReqTakeAttachment(_message.Message):
    __slots__ = ["mail_id"]
    MAIL_ID_FIELD_NUMBER: _ClassVar[int]
    mail_id: int
    def __init__(self, mail_id: _Optional[int] = ...) -> None: ...

class ReqReceiveAchievementGroupReward(_message.Message):
    __slots__ = ["group_id"]
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    group_id: int
    def __init__(self, group_id: _Optional[int] = ...) -> None: ...

class ResReceiveAchievementGroupReward(_message.Message):
    __slots__ = ["error", "execute_reward"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    EXECUTE_REWARD_FIELD_NUMBER: _ClassVar[int]
    error: Error
    execute_reward: _containers.RepeatedCompositeFieldContainer[ExecuteReward]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., execute_reward: _Optional[_Iterable[_Union[ExecuteReward, _Mapping]]] = ...) -> None: ...

class ReqReceiveAchievementReward(_message.Message):
    __slots__ = ["achievement_id"]
    ACHIEVEMENT_ID_FIELD_NUMBER: _ClassVar[int]
    achievement_id: int
    def __init__(self, achievement_id: _Optional[int] = ...) -> None: ...

class ResReceiveAchievementReward(_message.Message):
    __slots__ = ["error", "execute_reward"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    EXECUTE_REWARD_FIELD_NUMBER: _ClassVar[int]
    error: Error
    execute_reward: _containers.RepeatedCompositeFieldContainer[ExecuteReward]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., execute_reward: _Optional[_Iterable[_Union[ExecuteReward, _Mapping]]] = ...) -> None: ...

class ResFetchAchievementRate(_message.Message):
    __slots__ = ["error", "rate"]
    class AchievementRate(_message.Message):
        __slots__ = ["id", "rate"]
        ID_FIELD_NUMBER: _ClassVar[int]
        RATE_FIELD_NUMBER: _ClassVar[int]
        id: int
        rate: int
        def __init__(self, id: _Optional[int] = ..., rate: _Optional[int] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    RATE_FIELD_NUMBER: _ClassVar[int]
    error: Error
    rate: _containers.RepeatedCompositeFieldContainer[ResFetchAchievementRate.AchievementRate]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., rate: _Optional[_Iterable[_Union[ResFetchAchievementRate.AchievementRate, _Mapping]]] = ...) -> None: ...

class ResAchievement(_message.Message):
    __slots__ = ["error", "progresses", "rewarded_group"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    PROGRESSES_FIELD_NUMBER: _ClassVar[int]
    REWARDED_GROUP_FIELD_NUMBER: _ClassVar[int]
    error: Error
    progresses: _containers.RepeatedCompositeFieldContainer[AchievementProgress]
    rewarded_group: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., progresses: _Optional[_Iterable[_Union[AchievementProgress, _Mapping]]] = ..., rewarded_group: _Optional[_Iterable[int]] = ...) -> None: ...

class ResTitleList(_message.Message):
    __slots__ = ["error", "title_list"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    TITLE_LIST_FIELD_NUMBER: _ClassVar[int]
    error: Error
    title_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., title_list: _Optional[_Iterable[int]] = ...) -> None: ...

class ReqUseTitle(_message.Message):
    __slots__ = ["title"]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    title: int
    def __init__(self, title: _Optional[int] = ...) -> None: ...

class ReqBuyShiLian(_message.Message):
    __slots__ = ["type"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    type: int
    def __init__(self, type: _Optional[int] = ...) -> None: ...

class ReqUpdateClientValue(_message.Message):
    __slots__ = ["key", "value"]
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: int
    value: int
    def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...

class ResClientValue(_message.Message):
    __slots__ = ["error", "datas", "recharged_count"]
    class Value(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    DATAS_FIELD_NUMBER: _ClassVar[int]
    RECHARGED_COUNT_FIELD_NUMBER: _ClassVar[int]
    error: Error
    datas: _containers.RepeatedCompositeFieldContainer[ResClientValue.Value]
    recharged_count: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., datas: _Optional[_Iterable[_Union[ResClientValue.Value, _Mapping]]] = ..., recharged_count: _Optional[int] = ...) -> None: ...

class ReqClientMessage(_message.Message):
    __slots__ = ["timestamp", "message"]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    timestamp: int
    message: str
    def __init__(self, timestamp: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...

class ReqCurrentMatchInfo(_message.Message):
    __slots__ = ["mode_list"]
    MODE_LIST_FIELD_NUMBER: _ClassVar[int]
    mode_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, mode_list: _Optional[_Iterable[int]] = ...) -> None: ...

class ResCurrentMatchInfo(_message.Message):
    __slots__ = ["error", "matches"]
    class CurrentMatchInfo(_message.Message):
        __slots__ = ["mode_id", "playing_count"]
        MODE_ID_FIELD_NUMBER: _ClassVar[int]
        PLAYING_COUNT_FIELD_NUMBER: _ClassVar[int]
        mode_id: int
        playing_count: int
        def __init__(self, mode_id: _Optional[int] = ..., playing_count: _Optional[int] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    MATCHES_FIELD_NUMBER: _ClassVar[int]
    error: Error
    matches: _containers.RepeatedCompositeFieldContainer[ResCurrentMatchInfo.CurrentMatchInfo]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., matches: _Optional[_Iterable[_Union[ResCurrentMatchInfo.CurrentMatchInfo, _Mapping]]] = ...) -> None: ...

class ReqUserComplain(_message.Message):
    __slots__ = ["target_id", "type", "content", "game_uuid", "round_info"]
    class GameRoundInfo(_message.Message):
        __slots__ = ["chang", "ju", "ben", "seat", "xun"]
        CHANG_FIELD_NUMBER: _ClassVar[int]
        JU_FIELD_NUMBER: _ClassVar[int]
        BEN_FIELD_NUMBER: _ClassVar[int]
        SEAT_FIELD_NUMBER: _ClassVar[int]
        XUN_FIELD_NUMBER: _ClassVar[int]
        chang: int
        ju: int
        ben: int
        seat: int
        xun: int
        def __init__(self, chang: _Optional[int] = ..., ju: _Optional[int] = ..., ben: _Optional[int] = ..., seat: _Optional[int] = ..., xun: _Optional[int] = ...) -> None: ...
    TARGET_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    GAME_UUID_FIELD_NUMBER: _ClassVar[int]
    ROUND_INFO_FIELD_NUMBER: _ClassVar[int]
    target_id: int
    type: int
    content: str
    game_uuid: str
    round_info: ReqUserComplain.GameRoundInfo
    def __init__(self, target_id: _Optional[int] = ..., type: _Optional[int] = ..., content: _Optional[str] = ..., game_uuid: _Optional[str] = ..., round_info: _Optional[_Union[ReqUserComplain.GameRoundInfo, _Mapping]] = ...) -> None: ...

class ReqReadAnnouncement(_message.Message):
    __slots__ = ["announcement_id", "announcement_list"]
    ANNOUNCEMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ANNOUNCEMENT_LIST_FIELD_NUMBER: _ClassVar[int]
    announcement_id: int
    announcement_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, announcement_id: _Optional[int] = ..., announcement_list: _Optional[_Iterable[int]] = ...) -> None: ...

class ResReviveCoinInfo(_message.Message):
    __slots__ = ["error", "has_gained"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    HAS_GAINED_FIELD_NUMBER: _ClassVar[int]
    error: Error
    has_gained: bool
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., has_gained: bool = ...) -> None: ...

class ResDailyTask(_message.Message):
    __slots__ = ["error", "progresses", "has_refresh_count", "max_daily_task_count", "refresh_count"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    PROGRESSES_FIELD_NUMBER: _ClassVar[int]
    HAS_REFRESH_COUNT_FIELD_NUMBER: _ClassVar[int]
    MAX_DAILY_TASK_COUNT_FIELD_NUMBER: _ClassVar[int]
    REFRESH_COUNT_FIELD_NUMBER: _ClassVar[int]
    error: Error
    progresses: _containers.RepeatedCompositeFieldContainer[TaskProgress]
    has_refresh_count: bool
    max_daily_task_count: int
    refresh_count: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., progresses: _Optional[_Iterable[_Union[TaskProgress, _Mapping]]] = ..., has_refresh_count: bool = ..., max_daily_task_count: _Optional[int] = ..., refresh_count: _Optional[int] = ...) -> None: ...

class ReqRefreshDailyTask(_message.Message):
    __slots__ = ["task_id"]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    task_id: int
    def __init__(self, task_id: _Optional[int] = ...) -> None: ...

class ResRefreshDailyTask(_message.Message):
    __slots__ = ["error", "progress", "refresh_count"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    REFRESH_COUNT_FIELD_NUMBER: _ClassVar[int]
    error: Error
    progress: TaskProgress
    refresh_count: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., progress: _Optional[_Union[TaskProgress, _Mapping]] = ..., refresh_count: _Optional[int] = ...) -> None: ...

class ReqUseGiftCode(_message.Message):
    __slots__ = ["code"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    code: str
    def __init__(self, code: _Optional[str] = ...) -> None: ...

class ResUseGiftCode(_message.Message):
    __slots__ = ["error", "rewards"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    REWARDS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    rewards: _containers.RepeatedCompositeFieldContainer[RewardSlot]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., rewards: _Optional[_Iterable[_Union[RewardSlot, _Mapping]]] = ...) -> None: ...

class ResUseSpecialGiftCode(_message.Message):
    __slots__ = ["error", "rewards"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    REWARDS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    rewards: _containers.RepeatedCompositeFieldContainer[ExecuteReward]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., rewards: _Optional[_Iterable[_Union[ExecuteReward, _Mapping]]] = ...) -> None: ...

class ReqSendClientMessage(_message.Message):
    __slots__ = ["target_id", "type", "content"]
    TARGET_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    target_id: int
    type: int
    content: str
    def __init__(self, target_id: _Optional[int] = ..., type: _Optional[int] = ..., content: _Optional[str] = ...) -> None: ...

class ReqGameLiveInfo(_message.Message):
    __slots__ = ["game_uuid"]
    GAME_UUID_FIELD_NUMBER: _ClassVar[int]
    game_uuid: str
    def __init__(self, game_uuid: _Optional[str] = ...) -> None: ...

class ResGameLiveInfo(_message.Message):
    __slots__ = ["error", "left_start_seconds", "live_head", "segments", "now_millisecond"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    LEFT_START_SECONDS_FIELD_NUMBER: _ClassVar[int]
    LIVE_HEAD_FIELD_NUMBER: _ClassVar[int]
    SEGMENTS_FIELD_NUMBER: _ClassVar[int]
    NOW_MILLISECOND_FIELD_NUMBER: _ClassVar[int]
    error: Error
    left_start_seconds: int
    live_head: GameLiveHead
    segments: _containers.RepeatedCompositeFieldContainer[GameLiveSegmentUri]
    now_millisecond: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., left_start_seconds: _Optional[int] = ..., live_head: _Optional[_Union[GameLiveHead, _Mapping]] = ..., segments: _Optional[_Iterable[_Union[GameLiveSegmentUri, _Mapping]]] = ..., now_millisecond: _Optional[int] = ...) -> None: ...

class ReqGameLiveLeftSegment(_message.Message):
    __slots__ = ["game_uuid", "last_segment_id"]
    GAME_UUID_FIELD_NUMBER: _ClassVar[int]
    LAST_SEGMENT_ID_FIELD_NUMBER: _ClassVar[int]
    game_uuid: str
    last_segment_id: int
    def __init__(self, game_uuid: _Optional[str] = ..., last_segment_id: _Optional[int] = ...) -> None: ...

class ResGameLiveLeftSegment(_message.Message):
    __slots__ = ["error", "live_state", "segments", "now_millisecond", "segment_end_millisecond"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    LIVE_STATE_FIELD_NUMBER: _ClassVar[int]
    SEGMENTS_FIELD_NUMBER: _ClassVar[int]
    NOW_MILLISECOND_FIELD_NUMBER: _ClassVar[int]
    SEGMENT_END_MILLISECOND_FIELD_NUMBER: _ClassVar[int]
    error: Error
    live_state: int
    segments: _containers.RepeatedCompositeFieldContainer[GameLiveSegmentUri]
    now_millisecond: int
    segment_end_millisecond: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., live_state: _Optional[int] = ..., segments: _Optional[_Iterable[_Union[GameLiveSegmentUri, _Mapping]]] = ..., now_millisecond: _Optional[int] = ..., segment_end_millisecond: _Optional[int] = ...) -> None: ...

class ReqGameLiveList(_message.Message):
    __slots__ = ["filter_id"]
    FILTER_ID_FIELD_NUMBER: _ClassVar[int]
    filter_id: int
    def __init__(self, filter_id: _Optional[int] = ...) -> None: ...

class ResGameLiveList(_message.Message):
    __slots__ = ["error", "live_list"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    LIVE_LIST_FIELD_NUMBER: _ClassVar[int]
    error: Error
    live_list: _containers.RepeatedCompositeFieldContainer[GameLiveHead]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., live_list: _Optional[_Iterable[_Union[GameLiveHead, _Mapping]]] = ...) -> None: ...

class ResCommentSetting(_message.Message):
    __slots__ = ["error", "comment_allow"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    COMMENT_ALLOW_FIELD_NUMBER: _ClassVar[int]
    error: Error
    comment_allow: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., comment_allow: _Optional[int] = ...) -> None: ...

class ReqUpdateCommentSetting(_message.Message):
    __slots__ = ["comment_allow"]
    COMMENT_ALLOW_FIELD_NUMBER: _ClassVar[int]
    comment_allow: int
    def __init__(self, comment_allow: _Optional[int] = ...) -> None: ...

class ReqFetchCommentList(_message.Message):
    __slots__ = ["target_id"]
    TARGET_ID_FIELD_NUMBER: _ClassVar[int]
    target_id: int
    def __init__(self, target_id: _Optional[int] = ...) -> None: ...

class ResFetchCommentList(_message.Message):
    __slots__ = ["error", "comment_allow", "comment_id_list", "last_read_id"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    COMMENT_ALLOW_FIELD_NUMBER: _ClassVar[int]
    COMMENT_ID_LIST_FIELD_NUMBER: _ClassVar[int]
    LAST_READ_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    comment_allow: int
    comment_id_list: _containers.RepeatedScalarFieldContainer[int]
    last_read_id: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., comment_allow: _Optional[int] = ..., comment_id_list: _Optional[_Iterable[int]] = ..., last_read_id: _Optional[int] = ...) -> None: ...

class ReqFetchCommentContent(_message.Message):
    __slots__ = ["target_id", "comment_id_list"]
    TARGET_ID_FIELD_NUMBER: _ClassVar[int]
    COMMENT_ID_LIST_FIELD_NUMBER: _ClassVar[int]
    target_id: int
    comment_id_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, target_id: _Optional[int] = ..., comment_id_list: _Optional[_Iterable[int]] = ...) -> None: ...

class ResFetchCommentContent(_message.Message):
    __slots__ = ["error", "comments"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    COMMENTS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    comments: _containers.RepeatedCompositeFieldContainer[CommentItem]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., comments: _Optional[_Iterable[_Union[CommentItem, _Mapping]]] = ...) -> None: ...

class ReqLeaveComment(_message.Message):
    __slots__ = ["target_id", "content"]
    TARGET_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    target_id: int
    content: str
    def __init__(self, target_id: _Optional[int] = ..., content: _Optional[str] = ...) -> None: ...

class ReqDeleteComment(_message.Message):
    __slots__ = ["target_id", "delete_list"]
    TARGET_ID_FIELD_NUMBER: _ClassVar[int]
    DELETE_LIST_FIELD_NUMBER: _ClassVar[int]
    target_id: int
    delete_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, target_id: _Optional[int] = ..., delete_list: _Optional[_Iterable[int]] = ...) -> None: ...

class ReqUpdateReadComment(_message.Message):
    __slots__ = ["read_id"]
    READ_ID_FIELD_NUMBER: _ClassVar[int]
    read_id: int
    def __init__(self, read_id: _Optional[int] = ...) -> None: ...

class ResFetchRollingNotice(_message.Message):
    __slots__ = ["error", "notice"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    NOTICE_FIELD_NUMBER: _ClassVar[int]
    error: Error
    notice: RollingNotice
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., notice: _Optional[_Union[RollingNotice, _Mapping]] = ...) -> None: ...

class ResFetchMaintainNotice(_message.Message):
    __slots__ = ["error", "notice"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    NOTICE_FIELD_NUMBER: _ClassVar[int]
    error: Error
    notice: MaintainNotice
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., notice: _Optional[_Union[MaintainNotice, _Mapping]] = ...) -> None: ...

class ReqFetchRollingNotice(_message.Message):
    __slots__ = ["lang"]
    LANG_FIELD_NUMBER: _ClassVar[int]
    lang: str
    def __init__(self, lang: _Optional[str] = ...) -> None: ...

class ResServerTime(_message.Message):
    __slots__ = ["server_time", "error"]
    SERVER_TIME_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    server_time: int
    error: Error
    def __init__(self, server_time: _Optional[int] = ..., error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class ReqPlatformBillingProducts(_message.Message):
    __slots__ = ["shelves_id"]
    SHELVES_ID_FIELD_NUMBER: _ClassVar[int]
    shelves_id: int
    def __init__(self, shelves_id: _Optional[int] = ...) -> None: ...

class ResPlatformBillingProducts(_message.Message):
    __slots__ = ["error", "products"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    PRODUCTS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    products: _containers.RepeatedCompositeFieldContainer[BillingProduct]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., products: _Optional[_Iterable[_Union[BillingProduct, _Mapping]]] = ...) -> None: ...

class ReqCreateBillingOrder(_message.Message):
    __slots__ = ["goods_id", "payment_platform", "client_type", "account_id", "client_version_string"]
    GOODS_ID_FIELD_NUMBER: _ClassVar[int]
    PAYMENT_PLATFORM_FIELD_NUMBER: _ClassVar[int]
    CLIENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    goods_id: int
    payment_platform: int
    client_type: int
    account_id: int
    client_version_string: str
    def __init__(self, goods_id: _Optional[int] = ..., payment_platform: _Optional[int] = ..., client_type: _Optional[int] = ..., account_id: _Optional[int] = ..., client_version_string: _Optional[str] = ...) -> None: ...

class ResCreateBillingOrder(_message.Message):
    __slots__ = ["error", "order_id"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    order_id: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., order_id: _Optional[str] = ...) -> None: ...

class ReqSolveGooglePlayOrder(_message.Message):
    __slots__ = ["inapp_purchase_data", "inapp_data_signature"]
    INAPP_PURCHASE_DATA_FIELD_NUMBER: _ClassVar[int]
    INAPP_DATA_SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    inapp_purchase_data: str
    inapp_data_signature: str
    def __init__(self, inapp_purchase_data: _Optional[str] = ..., inapp_data_signature: _Optional[str] = ...) -> None: ...

class ReqSolveGooglePlayOrderV3(_message.Message):
    __slots__ = ["order_id", "transaction_id", "token", "account_id"]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    TRANSACTION_ID_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    transaction_id: str
    token: str
    account_id: int
    def __init__(self, order_id: _Optional[str] = ..., transaction_id: _Optional[str] = ..., token: _Optional[str] = ..., account_id: _Optional[int] = ...) -> None: ...

class ReqCancelGooglePlayOrder(_message.Message):
    __slots__ = ["order_id"]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    def __init__(self, order_id: _Optional[str] = ...) -> None: ...

class ReqCreateWechatNativeOrder(_message.Message):
    __slots__ = ["goods_id", "client_type", "account_id", "account_ip", "client_version_string"]
    GOODS_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_IP_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    goods_id: int
    client_type: int
    account_id: int
    account_ip: str
    client_version_string: str
    def __init__(self, goods_id: _Optional[int] = ..., client_type: _Optional[int] = ..., account_id: _Optional[int] = ..., account_ip: _Optional[str] = ..., client_version_string: _Optional[str] = ...) -> None: ...

class ResCreateWechatNativeOrder(_message.Message):
    __slots__ = ["error", "qrcode_buffer", "order_id"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    QRCODE_BUFFER_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    qrcode_buffer: str
    order_id: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., qrcode_buffer: _Optional[str] = ..., order_id: _Optional[str] = ...) -> None: ...

class ReqCreateWechatAppOrder(_message.Message):
    __slots__ = ["goods_id", "client_type", "account_id", "account_ip", "client_version_string"]
    GOODS_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_IP_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    goods_id: int
    client_type: int
    account_id: int
    account_ip: str
    client_version_string: str
    def __init__(self, goods_id: _Optional[int] = ..., client_type: _Optional[int] = ..., account_id: _Optional[int] = ..., account_ip: _Optional[str] = ..., client_version_string: _Optional[str] = ...) -> None: ...

class ResCreateWechatAppOrder(_message.Message):
    __slots__ = ["error", "call_wechat_app_param"]
    class CallWechatAppParam(_message.Message):
        __slots__ = ["appid", "partnerid", "prepayid", "package", "noncestr", "timestamp", "sign"]
        APPID_FIELD_NUMBER: _ClassVar[int]
        PARTNERID_FIELD_NUMBER: _ClassVar[int]
        PREPAYID_FIELD_NUMBER: _ClassVar[int]
        PACKAGE_FIELD_NUMBER: _ClassVar[int]
        NONCESTR_FIELD_NUMBER: _ClassVar[int]
        TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        SIGN_FIELD_NUMBER: _ClassVar[int]
        appid: str
        partnerid: str
        prepayid: str
        package: str
        noncestr: str
        timestamp: str
        sign: str
        def __init__(self, appid: _Optional[str] = ..., partnerid: _Optional[str] = ..., prepayid: _Optional[str] = ..., package: _Optional[str] = ..., noncestr: _Optional[str] = ..., timestamp: _Optional[str] = ..., sign: _Optional[str] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    CALL_WECHAT_APP_PARAM_FIELD_NUMBER: _ClassVar[int]
    error: Error
    call_wechat_app_param: ResCreateWechatAppOrder.CallWechatAppParam
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., call_wechat_app_param: _Optional[_Union[ResCreateWechatAppOrder.CallWechatAppParam, _Mapping]] = ...) -> None: ...

class ReqCreateAlipayOrder(_message.Message):
    __slots__ = ["goods_id", "client_type", "account_id", "alipay_trade_type", "return_url", "client_version_string"]
    GOODS_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ALIPAY_TRADE_TYPE_FIELD_NUMBER: _ClassVar[int]
    RETURN_URL_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    goods_id: int
    client_type: int
    account_id: int
    alipay_trade_type: str
    return_url: str
    client_version_string: str
    def __init__(self, goods_id: _Optional[int] = ..., client_type: _Optional[int] = ..., account_id: _Optional[int] = ..., alipay_trade_type: _Optional[str] = ..., return_url: _Optional[str] = ..., client_version_string: _Optional[str] = ...) -> None: ...

class ResCreateAlipayOrder(_message.Message):
    __slots__ = ["error", "alipay_url"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ALIPAY_URL_FIELD_NUMBER: _ClassVar[int]
    error: Error
    alipay_url: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., alipay_url: _Optional[str] = ...) -> None: ...

class ReqCreateAlipayScanOrder(_message.Message):
    __slots__ = ["goods_id", "client_type", "account_id", "client_version_string"]
    GOODS_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    goods_id: int
    client_type: int
    account_id: int
    client_version_string: str
    def __init__(self, goods_id: _Optional[int] = ..., client_type: _Optional[int] = ..., account_id: _Optional[int] = ..., client_version_string: _Optional[str] = ...) -> None: ...

class ResCreateAlipayScanOrder(_message.Message):
    __slots__ = ["error", "qrcode_buffer", "order_id", "qr_code"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    QRCODE_BUFFER_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    QR_CODE_FIELD_NUMBER: _ClassVar[int]
    error: Error
    qrcode_buffer: str
    order_id: str
    qr_code: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., qrcode_buffer: _Optional[str] = ..., order_id: _Optional[str] = ..., qr_code: _Optional[str] = ...) -> None: ...

class ReqCreateAlipayAppOrder(_message.Message):
    __slots__ = ["goods_id", "client_type", "account_id", "client_version_string"]
    GOODS_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    goods_id: int
    client_type: int
    account_id: int
    client_version_string: str
    def __init__(self, goods_id: _Optional[int] = ..., client_type: _Optional[int] = ..., account_id: _Optional[int] = ..., client_version_string: _Optional[str] = ...) -> None: ...

class ResCreateAlipayAppOrder(_message.Message):
    __slots__ = ["error", "alipay_url"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ALIPAY_URL_FIELD_NUMBER: _ClassVar[int]
    error: Error
    alipay_url: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., alipay_url: _Optional[str] = ...) -> None: ...

class ReqCreateJPCreditCardOrder(_message.Message):
    __slots__ = ["goods_id", "client_type", "account_id", "return_url", "access_token", "client_version_string"]
    GOODS_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    RETURN_URL_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    goods_id: int
    client_type: int
    account_id: int
    return_url: str
    access_token: str
    client_version_string: str
    def __init__(self, goods_id: _Optional[int] = ..., client_type: _Optional[int] = ..., account_id: _Optional[int] = ..., return_url: _Optional[str] = ..., access_token: _Optional[str] = ..., client_version_string: _Optional[str] = ...) -> None: ...

class ResCreateJPCreditCardOrder(_message.Message):
    __slots__ = ["error", "order_id"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    order_id: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., order_id: _Optional[str] = ...) -> None: ...

class ReqCreateJPPaypalOrder(_message.Message):
    __slots__ = ["goods_id", "client_type", "account_id", "return_url", "access_token", "client_version_string"]
    GOODS_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    RETURN_URL_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    goods_id: int
    client_type: int
    account_id: int
    return_url: str
    access_token: str
    client_version_string: str
    def __init__(self, goods_id: _Optional[int] = ..., client_type: _Optional[int] = ..., account_id: _Optional[int] = ..., return_url: _Optional[str] = ..., access_token: _Optional[str] = ..., client_version_string: _Optional[str] = ...) -> None: ...

class ResCreateJPPaypalOrder(_message.Message):
    __slots__ = ["error", "order_id"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    order_id: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., order_id: _Optional[str] = ...) -> None: ...

class ReqCreateJPAuOrder(_message.Message):
    __slots__ = ["goods_id", "client_type", "account_id", "return_url", "access_token", "client_version_string"]
    GOODS_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    RETURN_URL_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    goods_id: int
    client_type: int
    account_id: int
    return_url: str
    access_token: str
    client_version_string: str
    def __init__(self, goods_id: _Optional[int] = ..., client_type: _Optional[int] = ..., account_id: _Optional[int] = ..., return_url: _Optional[str] = ..., access_token: _Optional[str] = ..., client_version_string: _Optional[str] = ...) -> None: ...

class ResCreateJPAuOrder(_message.Message):
    __slots__ = ["error", "order_id"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    order_id: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., order_id: _Optional[str] = ...) -> None: ...

class ReqCreateJPDocomoOrder(_message.Message):
    __slots__ = ["goods_id", "client_type", "account_id", "return_url", "access_token", "client_version_string"]
    GOODS_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    RETURN_URL_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    goods_id: int
    client_type: int
    account_id: int
    return_url: str
    access_token: str
    client_version_string: str
    def __init__(self, goods_id: _Optional[int] = ..., client_type: _Optional[int] = ..., account_id: _Optional[int] = ..., return_url: _Optional[str] = ..., access_token: _Optional[str] = ..., client_version_string: _Optional[str] = ...) -> None: ...

class ResCreateJPDocomoOrder(_message.Message):
    __slots__ = ["error", "order_id"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    order_id: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., order_id: _Optional[str] = ...) -> None: ...

class ReqCreateJPWebMoneyOrder(_message.Message):
    __slots__ = ["goods_id", "client_type", "account_id", "return_url", "access_token", "client_version_string"]
    GOODS_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    RETURN_URL_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    goods_id: int
    client_type: int
    account_id: int
    return_url: str
    access_token: str
    client_version_string: str
    def __init__(self, goods_id: _Optional[int] = ..., client_type: _Optional[int] = ..., account_id: _Optional[int] = ..., return_url: _Optional[str] = ..., access_token: _Optional[str] = ..., client_version_string: _Optional[str] = ...) -> None: ...

class ResCreateJPWebMoneyOrder(_message.Message):
    __slots__ = ["error", "order_id"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    order_id: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., order_id: _Optional[str] = ...) -> None: ...

class ReqCreateJPSoftbankOrder(_message.Message):
    __slots__ = ["goods_id", "client_type", "account_id", "return_url", "access_token", "client_version_string"]
    GOODS_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    RETURN_URL_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    goods_id: int
    client_type: int
    account_id: int
    return_url: str
    access_token: str
    client_version_string: str
    def __init__(self, goods_id: _Optional[int] = ..., client_type: _Optional[int] = ..., account_id: _Optional[int] = ..., return_url: _Optional[str] = ..., access_token: _Optional[str] = ..., client_version_string: _Optional[str] = ...) -> None: ...

class ResCreateJPSoftbankOrder(_message.Message):
    __slots__ = ["error", "order_id"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    order_id: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., order_id: _Optional[str] = ...) -> None: ...

class ReqCreateJPPayPayOrder(_message.Message):
    __slots__ = ["goods_id", "client_type", "account_id", "return_url", "access_token", "client_version_string"]
    GOODS_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    RETURN_URL_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    goods_id: int
    client_type: int
    account_id: int
    return_url: str
    access_token: str
    client_version_string: str
    def __init__(self, goods_id: _Optional[int] = ..., client_type: _Optional[int] = ..., account_id: _Optional[int] = ..., return_url: _Optional[str] = ..., access_token: _Optional[str] = ..., client_version_string: _Optional[str] = ...) -> None: ...

class ResCreateJPPayPayOrder(_message.Message):
    __slots__ = ["error", "order_id"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    order_id: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., order_id: _Optional[str] = ...) -> None: ...

class ReqFetchJPCommonCreditCardOrder(_message.Message):
    __slots__ = ["order_id", "account_id"]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    account_id: int
    def __init__(self, order_id: _Optional[str] = ..., account_id: _Optional[int] = ...) -> None: ...

class ResFetchJPCommonCreditCardOrder(_message.Message):
    __slots__ = ["error"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    error: Error
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class ReqCreateJPGMOOrder(_message.Message):
    __slots__ = ["goods_id", "client_type", "account_id", "return_url", "access_token", "client_version_string"]
    GOODS_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    RETURN_URL_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    goods_id: int
    client_type: int
    account_id: int
    return_url: str
    access_token: str
    client_version_string: str
    def __init__(self, goods_id: _Optional[int] = ..., client_type: _Optional[int] = ..., account_id: _Optional[int] = ..., return_url: _Optional[str] = ..., access_token: _Optional[str] = ..., client_version_string: _Optional[str] = ...) -> None: ...

class ResCreateJPGMOOrder(_message.Message):
    __slots__ = ["error", "order_id"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    order_id: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., order_id: _Optional[str] = ...) -> None: ...

class ReqCreateYostarOrder(_message.Message):
    __slots__ = ["goods_id", "client_type", "account_id", "order_type", "client_version_string"]
    GOODS_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ORDER_TYPE_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    goods_id: int
    client_type: int
    account_id: int
    order_type: int
    client_version_string: str
    def __init__(self, goods_id: _Optional[int] = ..., client_type: _Optional[int] = ..., account_id: _Optional[int] = ..., order_type: _Optional[int] = ..., client_version_string: _Optional[str] = ...) -> None: ...

class ResCreateYostarOrder(_message.Message):
    __slots__ = ["error", "order_id"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    order_id: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., order_id: _Optional[str] = ...) -> None: ...

class ReqCreateENPaypalOrder(_message.Message):
    __slots__ = ["goods_id", "client_type", "account_id", "return_url", "access_token", "client_version_string"]
    GOODS_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    RETURN_URL_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    goods_id: int
    client_type: int
    account_id: int
    return_url: str
    access_token: str
    client_version_string: str
    def __init__(self, goods_id: _Optional[int] = ..., client_type: _Optional[int] = ..., account_id: _Optional[int] = ..., return_url: _Optional[str] = ..., access_token: _Optional[str] = ..., client_version_string: _Optional[str] = ...) -> None: ...

class ResCreateENPaypalOrder(_message.Message):
    __slots__ = ["error", "order_id"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    order_id: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., order_id: _Optional[str] = ...) -> None: ...

class ReqCreateENJCBOrder(_message.Message):
    __slots__ = ["goods_id", "client_type", "account_id", "return_url", "access_token", "client_version_string"]
    GOODS_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    RETURN_URL_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    goods_id: int
    client_type: int
    account_id: int
    return_url: str
    access_token: str
    client_version_string: str
    def __init__(self, goods_id: _Optional[int] = ..., client_type: _Optional[int] = ..., account_id: _Optional[int] = ..., return_url: _Optional[str] = ..., access_token: _Optional[str] = ..., client_version_string: _Optional[str] = ...) -> None: ...

class ResCreateENJCBOrder(_message.Message):
    __slots__ = ["error", "order_id"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    order_id: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., order_id: _Optional[str] = ...) -> None: ...

class ReqCreateENMasterCardOrder(_message.Message):
    __slots__ = ["goods_id", "client_type", "account_id", "return_url", "access_token", "client_version_string"]
    GOODS_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    RETURN_URL_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    goods_id: int
    client_type: int
    account_id: int
    return_url: str
    access_token: str
    client_version_string: str
    def __init__(self, goods_id: _Optional[int] = ..., client_type: _Optional[int] = ..., account_id: _Optional[int] = ..., return_url: _Optional[str] = ..., access_token: _Optional[str] = ..., client_version_string: _Optional[str] = ...) -> None: ...

class ResCreateENMasterCardOrder(_message.Message):
    __slots__ = ["error", "order_id"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    order_id: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., order_id: _Optional[str] = ...) -> None: ...

class ReqCreateENVisaOrder(_message.Message):
    __slots__ = ["goods_id", "client_type", "account_id", "return_url", "access_token", "client_version_string"]
    GOODS_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    RETURN_URL_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    goods_id: int
    client_type: int
    account_id: int
    return_url: str
    access_token: str
    client_version_string: str
    def __init__(self, goods_id: _Optional[int] = ..., client_type: _Optional[int] = ..., account_id: _Optional[int] = ..., return_url: _Optional[str] = ..., access_token: _Optional[str] = ..., client_version_string: _Optional[str] = ...) -> None: ...

class ResCreateENVisaOrder(_message.Message):
    __slots__ = ["error", "order_id"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    order_id: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., order_id: _Optional[str] = ...) -> None: ...

class ReqCreateENAlipayOrder(_message.Message):
    __slots__ = ["goods_id", "client_type", "account_id", "return_url", "access_token", "client_version_string"]
    GOODS_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    RETURN_URL_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    goods_id: int
    client_type: int
    account_id: int
    return_url: str
    access_token: str
    client_version_string: str
    def __init__(self, goods_id: _Optional[int] = ..., client_type: _Optional[int] = ..., account_id: _Optional[int] = ..., return_url: _Optional[str] = ..., access_token: _Optional[str] = ..., client_version_string: _Optional[str] = ...) -> None: ...

class ResCreateENAlipayOrder(_message.Message):
    __slots__ = ["error", "order_id"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    order_id: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., order_id: _Optional[str] = ...) -> None: ...

class ReqCreateKRPaypalOrder(_message.Message):
    __slots__ = ["goods_id", "client_type", "account_id", "return_url", "access_token", "client_version_string"]
    GOODS_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    RETURN_URL_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    goods_id: int
    client_type: int
    account_id: int
    return_url: str
    access_token: str
    client_version_string: str
    def __init__(self, goods_id: _Optional[int] = ..., client_type: _Optional[int] = ..., account_id: _Optional[int] = ..., return_url: _Optional[str] = ..., access_token: _Optional[str] = ..., client_version_string: _Optional[str] = ...) -> None: ...

class ResCreateKRPaypalOrder(_message.Message):
    __slots__ = ["error", "order_id"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    order_id: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., order_id: _Optional[str] = ...) -> None: ...

class ReqCreateKRJCBOrder(_message.Message):
    __slots__ = ["goods_id", "client_type", "account_id", "return_url", "access_token", "client_version_string"]
    GOODS_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    RETURN_URL_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    goods_id: int
    client_type: int
    account_id: int
    return_url: str
    access_token: str
    client_version_string: str
    def __init__(self, goods_id: _Optional[int] = ..., client_type: _Optional[int] = ..., account_id: _Optional[int] = ..., return_url: _Optional[str] = ..., access_token: _Optional[str] = ..., client_version_string: _Optional[str] = ...) -> None: ...

class ResCreateKRJCBOrder(_message.Message):
    __slots__ = ["error", "order_id"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    order_id: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., order_id: _Optional[str] = ...) -> None: ...

class ReqCreateKRMasterCardOrder(_message.Message):
    __slots__ = ["goods_id", "client_type", "account_id", "return_url", "access_token", "client_version_string"]
    GOODS_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    RETURN_URL_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    goods_id: int
    client_type: int
    account_id: int
    return_url: str
    access_token: str
    client_version_string: str
    def __init__(self, goods_id: _Optional[int] = ..., client_type: _Optional[int] = ..., account_id: _Optional[int] = ..., return_url: _Optional[str] = ..., access_token: _Optional[str] = ..., client_version_string: _Optional[str] = ...) -> None: ...

class ResCreateKRMasterCardOrder(_message.Message):
    __slots__ = ["error", "order_id"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    order_id: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., order_id: _Optional[str] = ...) -> None: ...

class ReqCreateKRVisaOrder(_message.Message):
    __slots__ = ["goods_id", "client_type", "account_id", "return_url", "access_token", "client_version_string"]
    GOODS_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    RETURN_URL_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    goods_id: int
    client_type: int
    account_id: int
    return_url: str
    access_token: str
    client_version_string: str
    def __init__(self, goods_id: _Optional[int] = ..., client_type: _Optional[int] = ..., account_id: _Optional[int] = ..., return_url: _Optional[str] = ..., access_token: _Optional[str] = ..., client_version_string: _Optional[str] = ...) -> None: ...

class ResCreateKRVisaOrder(_message.Message):
    __slots__ = ["error", "order_id"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    order_id: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., order_id: _Optional[str] = ...) -> None: ...

class ReqCreateKRAlipayOrder(_message.Message):
    __slots__ = ["goods_id", "client_type", "account_id", "return_url", "access_token", "client_version_string"]
    GOODS_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    RETURN_URL_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    goods_id: int
    client_type: int
    account_id: int
    return_url: str
    access_token: str
    client_version_string: str
    def __init__(self, goods_id: _Optional[int] = ..., client_type: _Optional[int] = ..., account_id: _Optional[int] = ..., return_url: _Optional[str] = ..., access_token: _Optional[str] = ..., client_version_string: _Optional[str] = ...) -> None: ...

class ResCreateKRAlipayOrder(_message.Message):
    __slots__ = ["error", "order_id"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    order_id: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., order_id: _Optional[str] = ...) -> None: ...

class ReqCreateDMMOrder(_message.Message):
    __slots__ = ["goods_id", "account_id", "client_type", "client_version_string"]
    GOODS_ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    goods_id: int
    account_id: int
    client_type: int
    client_version_string: str
    def __init__(self, goods_id: _Optional[int] = ..., account_id: _Optional[int] = ..., client_type: _Optional[int] = ..., client_version_string: _Optional[str] = ...) -> None: ...

class ResCreateDmmOrder(_message.Message):
    __slots__ = ["error", "order_id", "transaction_id", "dmm_user_id", "token", "callback_url", "request_time", "dmm_app_id"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    TRANSACTION_ID_FIELD_NUMBER: _ClassVar[int]
    DMM_USER_ID_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    CALLBACK_URL_FIELD_NUMBER: _ClassVar[int]
    REQUEST_TIME_FIELD_NUMBER: _ClassVar[int]
    DMM_APP_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    order_id: str
    transaction_id: str
    dmm_user_id: str
    token: str
    callback_url: str
    request_time: str
    dmm_app_id: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., order_id: _Optional[str] = ..., transaction_id: _Optional[str] = ..., dmm_user_id: _Optional[str] = ..., token: _Optional[str] = ..., callback_url: _Optional[str] = ..., request_time: _Optional[str] = ..., dmm_app_id: _Optional[str] = ...) -> None: ...

class ReqCreateIAPOrder(_message.Message):
    __slots__ = ["goods_id", "client_type", "account_id", "access_token", "debt_order_id", "client_version_string"]
    GOODS_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    DEBT_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    goods_id: int
    client_type: int
    account_id: int
    access_token: str
    debt_order_id: str
    client_version_string: str
    def __init__(self, goods_id: _Optional[int] = ..., client_type: _Optional[int] = ..., account_id: _Optional[int] = ..., access_token: _Optional[str] = ..., debt_order_id: _Optional[str] = ..., client_version_string: _Optional[str] = ...) -> None: ...

class ResCreateIAPOrder(_message.Message):
    __slots__ = ["error", "order_id"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    order_id: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., order_id: _Optional[str] = ...) -> None: ...

class ReqVerificationIAPOrder(_message.Message):
    __slots__ = ["order_id", "transaction_id", "receipt_data", "account_id"]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    TRANSACTION_ID_FIELD_NUMBER: _ClassVar[int]
    RECEIPT_DATA_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    transaction_id: str
    receipt_data: str
    account_id: int
    def __init__(self, order_id: _Optional[str] = ..., transaction_id: _Optional[str] = ..., receipt_data: _Optional[str] = ..., account_id: _Optional[int] = ...) -> None: ...

class ResVerificationIAPOrder(_message.Message):
    __slots__ = ["error"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    error: Error
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class ReqCreateSteamOrder(_message.Message):
    __slots__ = ["language", "account_id", "client_type", "goods_id", "steam_id", "debt_order_id", "client_version_string"]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    GOODS_ID_FIELD_NUMBER: _ClassVar[int]
    STEAM_ID_FIELD_NUMBER: _ClassVar[int]
    DEBT_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    language: str
    account_id: int
    client_type: int
    goods_id: int
    steam_id: str
    debt_order_id: str
    client_version_string: str
    def __init__(self, language: _Optional[str] = ..., account_id: _Optional[int] = ..., client_type: _Optional[int] = ..., goods_id: _Optional[int] = ..., steam_id: _Optional[str] = ..., debt_order_id: _Optional[str] = ..., client_version_string: _Optional[str] = ...) -> None: ...

class ResCreateSteamOrder(_message.Message):
    __slots__ = ["error", "order_id", "platform_order_id"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    order_id: str
    platform_order_id: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., order_id: _Optional[str] = ..., platform_order_id: _Optional[str] = ...) -> None: ...

class ReqVerifySteamOrder(_message.Message):
    __slots__ = ["order_id", "account_id"]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    account_id: int
    def __init__(self, order_id: _Optional[str] = ..., account_id: _Optional[int] = ...) -> None: ...

class ReqCreateMyCardOrder(_message.Message):
    __slots__ = ["goods_id", "client_type", "account_id", "debt_order_id", "client_version_string"]
    GOODS_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    DEBT_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    goods_id: int
    client_type: int
    account_id: int
    debt_order_id: str
    client_version_string: str
    def __init__(self, goods_id: _Optional[int] = ..., client_type: _Optional[int] = ..., account_id: _Optional[int] = ..., debt_order_id: _Optional[str] = ..., client_version_string: _Optional[str] = ...) -> None: ...

class ResCreateMyCardOrder(_message.Message):
    __slots__ = ["error", "auth_code", "order_id"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    AUTH_CODE_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    auth_code: str
    order_id: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., auth_code: _Optional[str] = ..., order_id: _Optional[str] = ...) -> None: ...

class ReqVerifyMyCardOrder(_message.Message):
    __slots__ = ["order_id", "account_id"]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    account_id: int
    def __init__(self, order_id: _Optional[str] = ..., account_id: _Optional[int] = ...) -> None: ...

class ReqCreatePaypalOrder(_message.Message):
    __slots__ = ["goods_id", "client_type", "account_id", "debt_order_id", "client_version_string"]
    GOODS_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    DEBT_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    goods_id: int
    client_type: int
    account_id: int
    debt_order_id: str
    client_version_string: str
    def __init__(self, goods_id: _Optional[int] = ..., client_type: _Optional[int] = ..., account_id: _Optional[int] = ..., debt_order_id: _Optional[str] = ..., client_version_string: _Optional[str] = ...) -> None: ...

class ResCreatePaypalOrder(_message.Message):
    __slots__ = ["error", "order_id", "url"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    error: Error
    order_id: str
    url: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., order_id: _Optional[str] = ..., url: _Optional[str] = ...) -> None: ...

class ReqCreateXsollaOrder(_message.Message):
    __slots__ = ["goods_id", "client_type", "account_id", "payment_method", "debt_order_id", "client_version_string"]
    GOODS_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    PAYMENT_METHOD_FIELD_NUMBER: _ClassVar[int]
    DEBT_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    goods_id: int
    client_type: int
    account_id: int
    payment_method: int
    debt_order_id: str
    client_version_string: str
    def __init__(self, goods_id: _Optional[int] = ..., client_type: _Optional[int] = ..., account_id: _Optional[int] = ..., payment_method: _Optional[int] = ..., debt_order_id: _Optional[str] = ..., client_version_string: _Optional[str] = ...) -> None: ...

class ResCreateXsollaOrder(_message.Message):
    __slots__ = ["error", "order_id", "url"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    error: Error
    order_id: str
    url: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., order_id: _Optional[str] = ..., url: _Optional[str] = ...) -> None: ...

class ReqDeliverAA32Order(_message.Message):
    __slots__ = ["account_id", "nsa_id", "nsa_token"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    NSA_ID_FIELD_NUMBER: _ClassVar[int]
    NSA_TOKEN_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    nsa_id: str
    nsa_token: str
    def __init__(self, account_id: _Optional[int] = ..., nsa_id: _Optional[str] = ..., nsa_token: _Optional[str] = ...) -> None: ...

class ReqOpenChest(_message.Message):
    __slots__ = ["chest_id", "count", "use_ticket"]
    CHEST_ID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    USE_TICKET_FIELD_NUMBER: _ClassVar[int]
    chest_id: int
    count: int
    use_ticket: bool
    def __init__(self, chest_id: _Optional[int] = ..., count: _Optional[int] = ..., use_ticket: bool = ...) -> None: ...

class ResOpenChest(_message.Message):
    __slots__ = ["error", "results", "total_open_count", "faith_count", "chest_replace_up"]
    class ChestReplaceCountData(_message.Message):
        __slots__ = ["id", "count"]
        ID_FIELD_NUMBER: _ClassVar[int]
        COUNT_FIELD_NUMBER: _ClassVar[int]
        id: int
        count: int
        def __init__(self, id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_OPEN_COUNT_FIELD_NUMBER: _ClassVar[int]
    FAITH_COUNT_FIELD_NUMBER: _ClassVar[int]
    CHEST_REPLACE_UP_FIELD_NUMBER: _ClassVar[int]
    error: Error
    results: _containers.RepeatedCompositeFieldContainer[OpenResult]
    total_open_count: int
    faith_count: int
    chest_replace_up: _containers.RepeatedCompositeFieldContainer[ResOpenChest.ChestReplaceCountData]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., results: _Optional[_Iterable[_Union[OpenResult, _Mapping]]] = ..., total_open_count: _Optional[int] = ..., faith_count: _Optional[int] = ..., chest_replace_up: _Optional[_Iterable[_Union[ResOpenChest.ChestReplaceCountData, _Mapping]]] = ...) -> None: ...

class ReqBuyFromChestShop(_message.Message):
    __slots__ = ["goods_id", "count"]
    GOODS_ID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    goods_id: int
    count: int
    def __init__(self, goods_id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class ResBuyFromChestShop(_message.Message):
    __slots__ = ["error", "chest_id", "consume_count", "faith_count"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    CHEST_ID_FIELD_NUMBER: _ClassVar[int]
    CONSUME_COUNT_FIELD_NUMBER: _ClassVar[int]
    FAITH_COUNT_FIELD_NUMBER: _ClassVar[int]
    error: Error
    chest_id: int
    consume_count: int
    faith_count: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., chest_id: _Optional[int] = ..., consume_count: _Optional[int] = ..., faith_count: _Optional[int] = ...) -> None: ...

class ResDailySignInInfo(_message.Message):
    __slots__ = ["error", "sign_in_days"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    SIGN_IN_DAYS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    sign_in_days: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., sign_in_days: _Optional[int] = ...) -> None: ...

class ReqDoActivitySignIn(_message.Message):
    __slots__ = ["activity_id"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ResDoActivitySignIn(_message.Message):
    __slots__ = ["error", "rewards", "sign_in_count"]
    class RewardData(_message.Message):
        __slots__ = ["resource_id", "count"]
        RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
        COUNT_FIELD_NUMBER: _ClassVar[int]
        resource_id: int
        count: int
        def __init__(self, resource_id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    REWARDS_FIELD_NUMBER: _ClassVar[int]
    SIGN_IN_COUNT_FIELD_NUMBER: _ClassVar[int]
    error: Error
    rewards: _containers.RepeatedCompositeFieldContainer[ResDoActivitySignIn.RewardData]
    sign_in_count: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., rewards: _Optional[_Iterable[_Union[ResDoActivitySignIn.RewardData, _Mapping]]] = ..., sign_in_count: _Optional[int] = ...) -> None: ...

class ResCharacterInfo(_message.Message):
    __slots__ = ["error", "characters", "skins", "main_character_id", "send_gift_count", "send_gift_limit", "finished_endings", "rewarded_endings", "character_sort", "hidden_characters"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    CHARACTERS_FIELD_NUMBER: _ClassVar[int]
    SKINS_FIELD_NUMBER: _ClassVar[int]
    MAIN_CHARACTER_ID_FIELD_NUMBER: _ClassVar[int]
    SEND_GIFT_COUNT_FIELD_NUMBER: _ClassVar[int]
    SEND_GIFT_LIMIT_FIELD_NUMBER: _ClassVar[int]
    FINISHED_ENDINGS_FIELD_NUMBER: _ClassVar[int]
    REWARDED_ENDINGS_FIELD_NUMBER: _ClassVar[int]
    CHARACTER_SORT_FIELD_NUMBER: _ClassVar[int]
    HIDDEN_CHARACTERS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    characters: _containers.RepeatedCompositeFieldContainer[Character]
    skins: _containers.RepeatedScalarFieldContainer[int]
    main_character_id: int
    send_gift_count: int
    send_gift_limit: int
    finished_endings: _containers.RepeatedScalarFieldContainer[int]
    rewarded_endings: _containers.RepeatedScalarFieldContainer[int]
    character_sort: _containers.RepeatedScalarFieldContainer[int]
    hidden_characters: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., characters: _Optional[_Iterable[_Union[Character, _Mapping]]] = ..., skins: _Optional[_Iterable[int]] = ..., main_character_id: _Optional[int] = ..., send_gift_count: _Optional[int] = ..., send_gift_limit: _Optional[int] = ..., finished_endings: _Optional[_Iterable[int]] = ..., rewarded_endings: _Optional[_Iterable[int]] = ..., character_sort: _Optional[_Iterable[int]] = ..., hidden_characters: _Optional[_Iterable[int]] = ...) -> None: ...

class ReqUpdateCharacterSort(_message.Message):
    __slots__ = ["sort"]
    SORT_FIELD_NUMBER: _ClassVar[int]
    sort: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, sort: _Optional[_Iterable[int]] = ...) -> None: ...

class ReqChangeMainCharacter(_message.Message):
    __slots__ = ["character_id"]
    CHARACTER_ID_FIELD_NUMBER: _ClassVar[int]
    character_id: int
    def __init__(self, character_id: _Optional[int] = ...) -> None: ...

class ReqChangeCharacterSkin(_message.Message):
    __slots__ = ["character_id", "skin"]
    CHARACTER_ID_FIELD_NUMBER: _ClassVar[int]
    SKIN_FIELD_NUMBER: _ClassVar[int]
    character_id: int
    skin: int
    def __init__(self, character_id: _Optional[int] = ..., skin: _Optional[int] = ...) -> None: ...

class ReqChangeCharacterView(_message.Message):
    __slots__ = ["character_id", "slot", "item_id"]
    CHARACTER_ID_FIELD_NUMBER: _ClassVar[int]
    SLOT_FIELD_NUMBER: _ClassVar[int]
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    character_id: int
    slot: int
    item_id: int
    def __init__(self, character_id: _Optional[int] = ..., slot: _Optional[int] = ..., item_id: _Optional[int] = ...) -> None: ...

class ReqSetHiddenCharacter(_message.Message):
    __slots__ = ["chara_list"]
    CHARA_LIST_FIELD_NUMBER: _ClassVar[int]
    chara_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, chara_list: _Optional[_Iterable[int]] = ...) -> None: ...

class ResSetHiddenCharacter(_message.Message):
    __slots__ = ["error", "hidden_characters"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    HIDDEN_CHARACTERS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    hidden_characters: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., hidden_characters: _Optional[_Iterable[int]] = ...) -> None: ...

class ReqSendGiftToCharacter(_message.Message):
    __slots__ = ["character_id", "gifts"]
    class Gift(_message.Message):
        __slots__ = ["item_id", "count"]
        ITEM_ID_FIELD_NUMBER: _ClassVar[int]
        COUNT_FIELD_NUMBER: _ClassVar[int]
        item_id: int
        count: int
        def __init__(self, item_id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...
    CHARACTER_ID_FIELD_NUMBER: _ClassVar[int]
    GIFTS_FIELD_NUMBER: _ClassVar[int]
    character_id: int
    gifts: _containers.RepeatedCompositeFieldContainer[ReqSendGiftToCharacter.Gift]
    def __init__(self, character_id: _Optional[int] = ..., gifts: _Optional[_Iterable[_Union[ReqSendGiftToCharacter.Gift, _Mapping]]] = ...) -> None: ...

class ResSendGiftToCharacter(_message.Message):
    __slots__ = ["error", "level", "exp"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    EXP_FIELD_NUMBER: _ClassVar[int]
    error: Error
    level: int
    exp: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., level: _Optional[int] = ..., exp: _Optional[int] = ...) -> None: ...

class ReqSellItem(_message.Message):
    __slots__ = ["sells"]
    class Item(_message.Message):
        __slots__ = ["item_id", "count"]
        ITEM_ID_FIELD_NUMBER: _ClassVar[int]
        COUNT_FIELD_NUMBER: _ClassVar[int]
        item_id: int
        count: int
        def __init__(self, item_id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...
    SELLS_FIELD_NUMBER: _ClassVar[int]
    sells: _containers.RepeatedCompositeFieldContainer[ReqSellItem.Item]
    def __init__(self, sells: _Optional[_Iterable[_Union[ReqSellItem.Item, _Mapping]]] = ...) -> None: ...

class ResCommonView(_message.Message):
    __slots__ = ["error", "slots"]
    class Slot(_message.Message):
        __slots__ = ["slot", "value"]
        SLOT_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        slot: int
        value: int
        def __init__(self, slot: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    SLOTS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    slots: _containers.RepeatedCompositeFieldContainer[ResCommonView.Slot]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., slots: _Optional[_Iterable[_Union[ResCommonView.Slot, _Mapping]]] = ...) -> None: ...

class ReqChangeCommonView(_message.Message):
    __slots__ = ["slot", "value"]
    SLOT_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    slot: int
    value: int
    def __init__(self, slot: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...

class ReqSaveCommonViews(_message.Message):
    __slots__ = ["views", "save_index", "is_use"]
    VIEWS_FIELD_NUMBER: _ClassVar[int]
    SAVE_INDEX_FIELD_NUMBER: _ClassVar[int]
    IS_USE_FIELD_NUMBER: _ClassVar[int]
    views: _containers.RepeatedCompositeFieldContainer[ViewSlot]
    save_index: int
    is_use: int
    def __init__(self, views: _Optional[_Iterable[_Union[ViewSlot, _Mapping]]] = ..., save_index: _Optional[int] = ..., is_use: _Optional[int] = ...) -> None: ...

class ReqCommonViews(_message.Message):
    __slots__ = ["index"]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    index: int
    def __init__(self, index: _Optional[int] = ...) -> None: ...

class ResCommonViews(_message.Message):
    __slots__ = ["error", "views"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    VIEWS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    views: _containers.RepeatedCompositeFieldContainer[ViewSlot]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., views: _Optional[_Iterable[_Union[ViewSlot, _Mapping]]] = ...) -> None: ...

class ResAllcommonViews(_message.Message):
    __slots__ = ["views", "use", "error"]
    class Views(_message.Message):
        __slots__ = ["values", "index"]
        VALUES_FIELD_NUMBER: _ClassVar[int]
        INDEX_FIELD_NUMBER: _ClassVar[int]
        values: _containers.RepeatedCompositeFieldContainer[ViewSlot]
        index: int
        def __init__(self, values: _Optional[_Iterable[_Union[ViewSlot, _Mapping]]] = ..., index: _Optional[int] = ...) -> None: ...
    VIEWS_FIELD_NUMBER: _ClassVar[int]
    USE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    views: _containers.RepeatedCompositeFieldContainer[ResAllcommonViews.Views]
    use: int
    error: Error
    def __init__(self, views: _Optional[_Iterable[_Union[ResAllcommonViews.Views, _Mapping]]] = ..., use: _Optional[int] = ..., error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class ReqUseCommonView(_message.Message):
    __slots__ = ["index"]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    index: int
    def __init__(self, index: _Optional[int] = ...) -> None: ...

class ReqUpgradeCharacter(_message.Message):
    __slots__ = ["character_id"]
    CHARACTER_ID_FIELD_NUMBER: _ClassVar[int]
    character_id: int
    def __init__(self, character_id: _Optional[int] = ...) -> None: ...

class ResUpgradeCharacter(_message.Message):
    __slots__ = ["error", "character"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    CHARACTER_FIELD_NUMBER: _ClassVar[int]
    error: Error
    character: Character
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., character: _Optional[_Union[Character, _Mapping]] = ...) -> None: ...

class ReqFinishedEnding(_message.Message):
    __slots__ = ["character_id", "story_id", "ending_id"]
    CHARACTER_ID_FIELD_NUMBER: _ClassVar[int]
    STORY_ID_FIELD_NUMBER: _ClassVar[int]
    ENDING_ID_FIELD_NUMBER: _ClassVar[int]
    character_id: int
    story_id: int
    ending_id: int
    def __init__(self, character_id: _Optional[int] = ..., story_id: _Optional[int] = ..., ending_id: _Optional[int] = ...) -> None: ...

class ReqGMCommand(_message.Message):
    __slots__ = ["command"]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    command: str
    def __init__(self, command: _Optional[str] = ...) -> None: ...

class ResShopInfo(_message.Message):
    __slots__ = ["error", "shop_info"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    SHOP_INFO_FIELD_NUMBER: _ClassVar[int]
    error: Error
    shop_info: ShopInfo
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., shop_info: _Optional[_Union[ShopInfo, _Mapping]] = ...) -> None: ...

class ReqBuyFromShop(_message.Message):
    __slots__ = ["goods_id", "count", "ver_price", "ver_goods"]
    class Item(_message.Message):
        __slots__ = ["id", "count"]
        ID_FIELD_NUMBER: _ClassVar[int]
        COUNT_FIELD_NUMBER: _ClassVar[int]
        id: int
        count: int
        def __init__(self, id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...
    GOODS_ID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    VER_PRICE_FIELD_NUMBER: _ClassVar[int]
    VER_GOODS_FIELD_NUMBER: _ClassVar[int]
    goods_id: int
    count: int
    ver_price: _containers.RepeatedCompositeFieldContainer[ReqBuyFromShop.Item]
    ver_goods: _containers.RepeatedCompositeFieldContainer[ReqBuyFromShop.Item]
    def __init__(self, goods_id: _Optional[int] = ..., count: _Optional[int] = ..., ver_price: _Optional[_Iterable[_Union[ReqBuyFromShop.Item, _Mapping]]] = ..., ver_goods: _Optional[_Iterable[_Union[ReqBuyFromShop.Item, _Mapping]]] = ...) -> None: ...

class ResBuyFromShop(_message.Message):
    __slots__ = ["error", "rewards"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    REWARDS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    rewards: _containers.RepeatedCompositeFieldContainer[RewardSlot]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., rewards: _Optional[_Iterable[_Union[RewardSlot, _Mapping]]] = ...) -> None: ...

class ReqBuyFromZHP(_message.Message):
    __slots__ = ["goods_id", "count"]
    GOODS_ID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    goods_id: int
    count: int
    def __init__(self, goods_id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class ReqPayMonthTicket(_message.Message):
    __slots__ = ["ticket_id"]
    TICKET_ID_FIELD_NUMBER: _ClassVar[int]
    ticket_id: int
    def __init__(self, ticket_id: _Optional[int] = ...) -> None: ...

class ResPayMonthTicket(_message.Message):
    __slots__ = ["error", "resource_id", "resource_count"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_COUNT_FIELD_NUMBER: _ClassVar[int]
    error: Error
    resource_id: int
    resource_count: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., resource_id: _Optional[int] = ..., resource_count: _Optional[int] = ...) -> None: ...

class ReqReshZHPShop(_message.Message):
    __slots__ = ["free_refresh", "cost_refresh"]
    FREE_REFRESH_FIELD_NUMBER: _ClassVar[int]
    COST_REFRESH_FIELD_NUMBER: _ClassVar[int]
    free_refresh: int
    cost_refresh: int
    def __init__(self, free_refresh: _Optional[int] = ..., cost_refresh: _Optional[int] = ...) -> None: ...

class ResRefreshZHPShop(_message.Message):
    __slots__ = ["error", "zhp"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ZHP_FIELD_NUMBER: _ClassVar[int]
    error: Error
    zhp: ZHPShop
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., zhp: _Optional[_Union[ZHPShop, _Mapping]] = ...) -> None: ...

class ResMonthTicketInfo(_message.Message):
    __slots__ = ["error", "month_ticket_info"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    MONTH_TICKET_INFO_FIELD_NUMBER: _ClassVar[int]
    error: Error
    month_ticket_info: MonthTicketInfo
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., month_ticket_info: _Optional[_Union[MonthTicketInfo, _Mapping]] = ...) -> None: ...

class ReqExchangeCurrency(_message.Message):
    __slots__ = ["id", "count"]
    ID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    id: int
    count: int
    def __init__(self, id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class ResServerSettings(_message.Message):
    __slots__ = ["error", "settings"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    settings: ServerSettings
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., settings: _Optional[_Union[ServerSettings, _Mapping]] = ...) -> None: ...

class ResAccountSettings(_message.Message):
    __slots__ = ["error", "settings"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    settings: _containers.RepeatedCompositeFieldContainer[AccountSetting]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., settings: _Optional[_Iterable[_Union[AccountSetting, _Mapping]]] = ...) -> None: ...

class ReqUpdateAccountSettings(_message.Message):
    __slots__ = ["setting"]
    SETTING_FIELD_NUMBER: _ClassVar[int]
    setting: AccountSetting
    def __init__(self, setting: _Optional[_Union[AccountSetting, _Mapping]] = ...) -> None: ...

class ResModNicknameTime(_message.Message):
    __slots__ = ["error", "last_mod_time"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    LAST_MOD_TIME_FIELD_NUMBER: _ClassVar[int]
    error: Error
    last_mod_time: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., last_mod_time: _Optional[int] = ...) -> None: ...

class ResMisc(_message.Message):
    __slots__ = ["error", "recharged_list", "faiths", "verified_hidden", "verified_value"]
    class MiscFaithData(_message.Message):
        __slots__ = ["faith_id", "count"]
        FAITH_ID_FIELD_NUMBER: _ClassVar[int]
        COUNT_FIELD_NUMBER: _ClassVar[int]
        faith_id: int
        count: int
        def __init__(self, faith_id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    RECHARGED_LIST_FIELD_NUMBER: _ClassVar[int]
    FAITHS_FIELD_NUMBER: _ClassVar[int]
    VERIFIED_HIDDEN_FIELD_NUMBER: _ClassVar[int]
    VERIFIED_VALUE_FIELD_NUMBER: _ClassVar[int]
    error: Error
    recharged_list: _containers.RepeatedScalarFieldContainer[int]
    faiths: _containers.RepeatedCompositeFieldContainer[ResMisc.MiscFaithData]
    verified_hidden: int
    verified_value: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., recharged_list: _Optional[_Iterable[int]] = ..., faiths: _Optional[_Iterable[_Union[ResMisc.MiscFaithData, _Mapping]]] = ..., verified_hidden: _Optional[int] = ..., verified_value: _Optional[int] = ...) -> None: ...

class ReqModifySignature(_message.Message):
    __slots__ = ["signature"]
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    signature: str
    def __init__(self, signature: _Optional[str] = ...) -> None: ...

class ResIDCardInfo(_message.Message):
    __slots__ = ["error", "is_authed", "country"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    IS_AUTHED_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_FIELD_NUMBER: _ClassVar[int]
    error: Error
    is_authed: bool
    country: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., is_authed: bool = ..., country: _Optional[str] = ...) -> None: ...

class ReqUpdateIDCardInfo(_message.Message):
    __slots__ = ["fullname", "card_no"]
    FULLNAME_FIELD_NUMBER: _ClassVar[int]
    CARD_NO_FIELD_NUMBER: _ClassVar[int]
    fullname: str
    card_no: str
    def __init__(self, fullname: _Optional[str] = ..., card_no: _Optional[str] = ...) -> None: ...

class ResVipReward(_message.Message):
    __slots__ = ["error", "gained_vip_levels"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    GAINED_VIP_LEVELS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    gained_vip_levels: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., gained_vip_levels: _Optional[_Iterable[int]] = ...) -> None: ...

class ResFetchRefundOrder(_message.Message):
    __slots__ = ["error", "orders", "clear_deadline", "message"]
    class OrderInfo(_message.Message):
        __slots__ = ["success_time", "goods_id", "cleared", "order_id"]
        SUCCESS_TIME_FIELD_NUMBER: _ClassVar[int]
        GOODS_ID_FIELD_NUMBER: _ClassVar[int]
        CLEARED_FIELD_NUMBER: _ClassVar[int]
        ORDER_ID_FIELD_NUMBER: _ClassVar[int]
        success_time: int
        goods_id: int
        cleared: int
        order_id: str
        def __init__(self, success_time: _Optional[int] = ..., goods_id: _Optional[int] = ..., cleared: _Optional[int] = ..., order_id: _Optional[str] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDERS_FIELD_NUMBER: _ClassVar[int]
    CLEAR_DEADLINE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    error: Error
    orders: _containers.RepeatedCompositeFieldContainer[ResFetchRefundOrder.OrderInfo]
    clear_deadline: int
    message: _containers.RepeatedCompositeFieldContainer[I18nContext]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., orders: _Optional[_Iterable[_Union[ResFetchRefundOrder.OrderInfo, _Mapping]]] = ..., clear_deadline: _Optional[int] = ..., message: _Optional[_Iterable[_Union[I18nContext, _Mapping]]] = ...) -> None: ...

class ReqGainVipReward(_message.Message):
    __slots__ = ["vip_level"]
    VIP_LEVEL_FIELD_NUMBER: _ClassVar[int]
    vip_level: int
    def __init__(self, vip_level: _Optional[int] = ...) -> None: ...

class ReqFetchCustomizedContestList(_message.Message):
    __slots__ = ["start", "count", "lang"]
    START_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    LANG_FIELD_NUMBER: _ClassVar[int]
    start: int
    count: int
    lang: str
    def __init__(self, start: _Optional[int] = ..., count: _Optional[int] = ..., lang: _Optional[str] = ...) -> None: ...

class ResFetchCustomizedContestList(_message.Message):
    __slots__ = ["error", "contests", "follow_contests"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    CONTESTS_FIELD_NUMBER: _ClassVar[int]
    FOLLOW_CONTESTS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    contests: _containers.RepeatedCompositeFieldContainer[CustomizedContestBase]
    follow_contests: _containers.RepeatedCompositeFieldContainer[CustomizedContestBase]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., contests: _Optional[_Iterable[_Union[CustomizedContestBase, _Mapping]]] = ..., follow_contests: _Optional[_Iterable[_Union[CustomizedContestBase, _Mapping]]] = ...) -> None: ...

class ReqFetchCustomizedContestAuthInfo(_message.Message):
    __slots__ = ["unique_id"]
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    unique_id: int
    def __init__(self, unique_id: _Optional[int] = ...) -> None: ...

class ResFetchCustomizedContestAuthInfo(_message.Message):
    __slots__ = ["error", "observer_level"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    OBSERVER_LEVEL_FIELD_NUMBER: _ClassVar[int]
    error: Error
    observer_level: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., observer_level: _Optional[int] = ...) -> None: ...

class ReqEnterCustomizedContest(_message.Message):
    __slots__ = ["unique_id", "lang"]
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    LANG_FIELD_NUMBER: _ClassVar[int]
    unique_id: int
    lang: str
    def __init__(self, unique_id: _Optional[int] = ..., lang: _Optional[str] = ...) -> None: ...

class ResEnterCustomizedContest(_message.Message):
    __slots__ = ["error", "detail_info", "player_report", "is_followed", "state", "is_admin"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    DETAIL_INFO_FIELD_NUMBER: _ClassVar[int]
    PLAYER_REPORT_FIELD_NUMBER: _ClassVar[int]
    IS_FOLLOWED_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    IS_ADMIN_FIELD_NUMBER: _ClassVar[int]
    error: Error
    detail_info: CustomizedContestDetail
    player_report: CustomizedContestPlayerReport
    is_followed: bool
    state: int
    is_admin: bool
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., detail_info: _Optional[_Union[CustomizedContestDetail, _Mapping]] = ..., player_report: _Optional[_Union[CustomizedContestPlayerReport, _Mapping]] = ..., is_followed: bool = ..., state: _Optional[int] = ..., is_admin: bool = ...) -> None: ...

class ReqFetchCustomizedContestOnlineInfo(_message.Message):
    __slots__ = ["unique_id"]
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    unique_id: int
    def __init__(self, unique_id: _Optional[int] = ...) -> None: ...

class ResFetchCustomizedContestOnlineInfo(_message.Message):
    __slots__ = ["error", "online_player"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ONLINE_PLAYER_FIELD_NUMBER: _ClassVar[int]
    error: Error
    online_player: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., online_player: _Optional[int] = ...) -> None: ...

class ReqFetchCustomizedContestByContestId(_message.Message):
    __slots__ = ["contest_id", "lang"]
    CONTEST_ID_FIELD_NUMBER: _ClassVar[int]
    LANG_FIELD_NUMBER: _ClassVar[int]
    contest_id: int
    lang: str
    def __init__(self, contest_id: _Optional[int] = ..., lang: _Optional[str] = ...) -> None: ...

class ResFetchCustomizedContestByContestId(_message.Message):
    __slots__ = ["error", "contest_info"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    CONTEST_INFO_FIELD_NUMBER: _ClassVar[int]
    error: Error
    contest_info: CustomizedContestAbstract
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., contest_info: _Optional[_Union[CustomizedContestAbstract, _Mapping]] = ...) -> None: ...

class ReqSignupCustomizedContest(_message.Message):
    __slots__ = ["unique_id", "client_version_string"]
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    unique_id: int
    client_version_string: str
    def __init__(self, unique_id: _Optional[int] = ..., client_version_string: _Optional[str] = ...) -> None: ...

class ResSignupCustomizedContest(_message.Message):
    __slots__ = ["error", "state"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    error: Error
    state: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., state: _Optional[int] = ...) -> None: ...

class ReqStartCustomizedContest(_message.Message):
    __slots__ = ["unique_id", "client_version_string"]
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    unique_id: int
    client_version_string: str
    def __init__(self, unique_id: _Optional[int] = ..., client_version_string: _Optional[str] = ...) -> None: ...

class ReqStopCustomizedContest(_message.Message):
    __slots__ = ["unique_id"]
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    unique_id: int
    def __init__(self, unique_id: _Optional[int] = ...) -> None: ...

class ReqJoinCustomizedContestChatRoom(_message.Message):
    __slots__ = ["unique_id"]
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    unique_id: int
    def __init__(self, unique_id: _Optional[int] = ...) -> None: ...

class ResJoinCustomizedContestChatRoom(_message.Message):
    __slots__ = ["error", "token"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    error: Error
    token: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., token: _Optional[str] = ...) -> None: ...

class ReqSayChatMessage(_message.Message):
    __slots__ = ["content", "unique_id"]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    content: str
    unique_id: int
    def __init__(self, content: _Optional[str] = ..., unique_id: _Optional[int] = ...) -> None: ...

class ReqFetchCustomizedContestGameLiveList(_message.Message):
    __slots__ = ["unique_id"]
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    unique_id: int
    def __init__(self, unique_id: _Optional[int] = ...) -> None: ...

class ResFetchCustomizedContestGameLiveList(_message.Message):
    __slots__ = ["error", "live_list"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    LIVE_LIST_FIELD_NUMBER: _ClassVar[int]
    error: Error
    live_list: _containers.RepeatedCompositeFieldContainer[GameLiveHead]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., live_list: _Optional[_Iterable[_Union[GameLiveHead, _Mapping]]] = ...) -> None: ...

class ReqFetchCustomizedContestGameRecords(_message.Message):
    __slots__ = ["unique_id", "last_index", "season_id"]
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_INDEX_FIELD_NUMBER: _ClassVar[int]
    SEASON_ID_FIELD_NUMBER: _ClassVar[int]
    unique_id: int
    last_index: int
    season_id: int
    def __init__(self, unique_id: _Optional[int] = ..., last_index: _Optional[int] = ..., season_id: _Optional[int] = ...) -> None: ...

class ResFetchCustomizedContestGameRecords(_message.Message):
    __slots__ = ["error", "next_index", "record_list"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    NEXT_INDEX_FIELD_NUMBER: _ClassVar[int]
    RECORD_LIST_FIELD_NUMBER: _ClassVar[int]
    error: Error
    next_index: int
    record_list: _containers.RepeatedCompositeFieldContainer[RecordGame]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., next_index: _Optional[int] = ..., record_list: _Optional[_Iterable[_Union[RecordGame, _Mapping]]] = ...) -> None: ...

class ReqTargetCustomizedContest(_message.Message):
    __slots__ = ["unique_id"]
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    unique_id: int
    def __init__(self, unique_id: _Optional[int] = ...) -> None: ...

class ResActivityList(_message.Message):
    __slots__ = ["error", "activities"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ACTIVITIES_FIELD_NUMBER: _ClassVar[int]
    error: Error
    activities: _containers.RepeatedCompositeFieldContainer[Activity]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., activities: _Optional[_Iterable[_Union[Activity, _Mapping]]] = ...) -> None: ...

class ResAccountActivityData(_message.Message):
    __slots__ = ["error", "exchange_records", "task_progress_list", "accumulated_point_list", "rank_data_list", "flip_task_progress_list", "sign_in_data", "richman_data", "period_task_progress_list", "random_task_progress_list", "chest_up_data", "sns_data", "mine_data", "rpg_data", "arena_data", "feed_data", "segment_task_progress_list", "vote_records", "spot_data", "friend_gift_data", "upgrade_data", "gacha_data", "simulation_data", "combining_data", "village_data", "festival_data", "island_data", "amulet_data", "story_data"]
    class ActivitySignInData(_message.Message):
        __slots__ = ["activity_id", "sign_in_count", "last_sign_in_time"]
        ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
        SIGN_IN_COUNT_FIELD_NUMBER: _ClassVar[int]
        LAST_SIGN_IN_TIME_FIELD_NUMBER: _ClassVar[int]
        activity_id: int
        sign_in_count: int
        last_sign_in_time: int
        def __init__(self, activity_id: _Optional[int] = ..., sign_in_count: _Optional[int] = ..., last_sign_in_time: _Optional[int] = ...) -> None: ...
    class BuffData(_message.Message):
        __slots__ = ["type", "remain", "effect"]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        REMAIN_FIELD_NUMBER: _ClassVar[int]
        EFFECT_FIELD_NUMBER: _ClassVar[int]
        type: int
        remain: int
        effect: int
        def __init__(self, type: _Optional[int] = ..., remain: _Optional[int] = ..., effect: _Optional[int] = ...) -> None: ...
    class ActivityRichmanData(_message.Message):
        __slots__ = ["activity_id", "location", "finished_count", "chest_position", "bank_save", "exp", "buff"]
        ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
        LOCATION_FIELD_NUMBER: _ClassVar[int]
        FINISHED_COUNT_FIELD_NUMBER: _ClassVar[int]
        CHEST_POSITION_FIELD_NUMBER: _ClassVar[int]
        BANK_SAVE_FIELD_NUMBER: _ClassVar[int]
        EXP_FIELD_NUMBER: _ClassVar[int]
        BUFF_FIELD_NUMBER: _ClassVar[int]
        activity_id: int
        location: int
        finished_count: int
        chest_position: int
        bank_save: int
        exp: int
        buff: _containers.RepeatedCompositeFieldContainer[ResAccountActivityData.BuffData]
        def __init__(self, activity_id: _Optional[int] = ..., location: _Optional[int] = ..., finished_count: _Optional[int] = ..., chest_position: _Optional[int] = ..., bank_save: _Optional[int] = ..., exp: _Optional[int] = ..., buff: _Optional[_Iterable[_Union[ResAccountActivityData.BuffData, _Mapping]]] = ...) -> None: ...
    class ChestUpData(_message.Message):
        __slots__ = ["id", "count"]
        ID_FIELD_NUMBER: _ClassVar[int]
        COUNT_FIELD_NUMBER: _ClassVar[int]
        id: int
        count: int
        def __init__(self, id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...
    class ActivitySNSData(_message.Message):
        __slots__ = ["blog", "liked_id", "reply"]
        BLOG_FIELD_NUMBER: _ClassVar[int]
        LIKED_ID_FIELD_NUMBER: _ClassVar[int]
        REPLY_FIELD_NUMBER: _ClassVar[int]
        blog: _containers.RepeatedCompositeFieldContainer[SNSBlog]
        liked_id: _containers.RepeatedScalarFieldContainer[int]
        reply: _containers.RepeatedCompositeFieldContainer[SNSReply]
        def __init__(self, blog: _Optional[_Iterable[_Union[SNSBlog, _Mapping]]] = ..., liked_id: _Optional[_Iterable[int]] = ..., reply: _Optional[_Iterable[_Union[SNSReply, _Mapping]]] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    EXCHANGE_RECORDS_FIELD_NUMBER: _ClassVar[int]
    TASK_PROGRESS_LIST_FIELD_NUMBER: _ClassVar[int]
    ACCUMULATED_POINT_LIST_FIELD_NUMBER: _ClassVar[int]
    RANK_DATA_LIST_FIELD_NUMBER: _ClassVar[int]
    FLIP_TASK_PROGRESS_LIST_FIELD_NUMBER: _ClassVar[int]
    SIGN_IN_DATA_FIELD_NUMBER: _ClassVar[int]
    RICHMAN_DATA_FIELD_NUMBER: _ClassVar[int]
    PERIOD_TASK_PROGRESS_LIST_FIELD_NUMBER: _ClassVar[int]
    RANDOM_TASK_PROGRESS_LIST_FIELD_NUMBER: _ClassVar[int]
    CHEST_UP_DATA_FIELD_NUMBER: _ClassVar[int]
    SNS_DATA_FIELD_NUMBER: _ClassVar[int]
    MINE_DATA_FIELD_NUMBER: _ClassVar[int]
    RPG_DATA_FIELD_NUMBER: _ClassVar[int]
    ARENA_DATA_FIELD_NUMBER: _ClassVar[int]
    FEED_DATA_FIELD_NUMBER: _ClassVar[int]
    SEGMENT_TASK_PROGRESS_LIST_FIELD_NUMBER: _ClassVar[int]
    VOTE_RECORDS_FIELD_NUMBER: _ClassVar[int]
    SPOT_DATA_FIELD_NUMBER: _ClassVar[int]
    FRIEND_GIFT_DATA_FIELD_NUMBER: _ClassVar[int]
    UPGRADE_DATA_FIELD_NUMBER: _ClassVar[int]
    GACHA_DATA_FIELD_NUMBER: _ClassVar[int]
    SIMULATION_DATA_FIELD_NUMBER: _ClassVar[int]
    COMBINING_DATA_FIELD_NUMBER: _ClassVar[int]
    VILLAGE_DATA_FIELD_NUMBER: _ClassVar[int]
    FESTIVAL_DATA_FIELD_NUMBER: _ClassVar[int]
    ISLAND_DATA_FIELD_NUMBER: _ClassVar[int]
    AMULET_DATA_FIELD_NUMBER: _ClassVar[int]
    STORY_DATA_FIELD_NUMBER: _ClassVar[int]
    error: Error
    exchange_records: _containers.RepeatedCompositeFieldContainer[ExchangeRecord]
    task_progress_list: _containers.RepeatedCompositeFieldContainer[TaskProgress]
    accumulated_point_list: _containers.RepeatedCompositeFieldContainer[ActivityAccumulatedPointData]
    rank_data_list: _containers.RepeatedCompositeFieldContainer[ActivityRankPointData]
    flip_task_progress_list: _containers.RepeatedCompositeFieldContainer[TaskProgress]
    sign_in_data: _containers.RepeatedCompositeFieldContainer[ResAccountActivityData.ActivitySignInData]
    richman_data: _containers.RepeatedCompositeFieldContainer[ResAccountActivityData.ActivityRichmanData]
    period_task_progress_list: _containers.RepeatedCompositeFieldContainer[TaskProgress]
    random_task_progress_list: _containers.RepeatedCompositeFieldContainer[TaskProgress]
    chest_up_data: _containers.RepeatedCompositeFieldContainer[ResAccountActivityData.ChestUpData]
    sns_data: ResAccountActivityData.ActivitySNSData
    mine_data: _containers.RepeatedCompositeFieldContainer[MineActivityData]
    rpg_data: _containers.RepeatedCompositeFieldContainer[RPGActivity]
    arena_data: _containers.RepeatedCompositeFieldContainer[ActivityArenaData]
    feed_data: _containers.RepeatedCompositeFieldContainer[FeedActivityData]
    segment_task_progress_list: _containers.RepeatedCompositeFieldContainer[SegmentTaskProgress]
    vote_records: _containers.RepeatedCompositeFieldContainer[VoteData]
    spot_data: _containers.RepeatedCompositeFieldContainer[ActivitySpotData]
    friend_gift_data: _containers.RepeatedCompositeFieldContainer[ActivityFriendGiftData]
    upgrade_data: _containers.RepeatedCompositeFieldContainer[ActivityUpgradeData]
    gacha_data: _containers.RepeatedCompositeFieldContainer[ActivityGachaUpdateData]
    simulation_data: _containers.RepeatedCompositeFieldContainer[ActivitySimulationData]
    combining_data: _containers.RepeatedCompositeFieldContainer[ActivityCombiningLQData]
    village_data: _containers.RepeatedCompositeFieldContainer[ActivityVillageData]
    festival_data: _containers.RepeatedCompositeFieldContainer[ActivityFestivalData]
    island_data: _containers.RepeatedCompositeFieldContainer[ActivityIslandData]
    amulet_data: _containers.RepeatedCompositeFieldContainer[ActivityAmuletData]
    story_data: _containers.RepeatedCompositeFieldContainer[ActivityStoryData]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., exchange_records: _Optional[_Iterable[_Union[ExchangeRecord, _Mapping]]] = ..., task_progress_list: _Optional[_Iterable[_Union[TaskProgress, _Mapping]]] = ..., accumulated_point_list: _Optional[_Iterable[_Union[ActivityAccumulatedPointData, _Mapping]]] = ..., rank_data_list: _Optional[_Iterable[_Union[ActivityRankPointData, _Mapping]]] = ..., flip_task_progress_list: _Optional[_Iterable[_Union[TaskProgress, _Mapping]]] = ..., sign_in_data: _Optional[_Iterable[_Union[ResAccountActivityData.ActivitySignInData, _Mapping]]] = ..., richman_data: _Optional[_Iterable[_Union[ResAccountActivityData.ActivityRichmanData, _Mapping]]] = ..., period_task_progress_list: _Optional[_Iterable[_Union[TaskProgress, _Mapping]]] = ..., random_task_progress_list: _Optional[_Iterable[_Union[TaskProgress, _Mapping]]] = ..., chest_up_data: _Optional[_Iterable[_Union[ResAccountActivityData.ChestUpData, _Mapping]]] = ..., sns_data: _Optional[_Union[ResAccountActivityData.ActivitySNSData, _Mapping]] = ..., mine_data: _Optional[_Iterable[_Union[MineActivityData, _Mapping]]] = ..., rpg_data: _Optional[_Iterable[_Union[RPGActivity, _Mapping]]] = ..., arena_data: _Optional[_Iterable[_Union[ActivityArenaData, _Mapping]]] = ..., feed_data: _Optional[_Iterable[_Union[FeedActivityData, _Mapping]]] = ..., segment_task_progress_list: _Optional[_Iterable[_Union[SegmentTaskProgress, _Mapping]]] = ..., vote_records: _Optional[_Iterable[_Union[VoteData, _Mapping]]] = ..., spot_data: _Optional[_Iterable[_Union[ActivitySpotData, _Mapping]]] = ..., friend_gift_data: _Optional[_Iterable[_Union[ActivityFriendGiftData, _Mapping]]] = ..., upgrade_data: _Optional[_Iterable[_Union[ActivityUpgradeData, _Mapping]]] = ..., gacha_data: _Optional[_Iterable[_Union[ActivityGachaUpdateData, _Mapping]]] = ..., simulation_data: _Optional[_Iterable[_Union[ActivitySimulationData, _Mapping]]] = ..., combining_data: _Optional[_Iterable[_Union[ActivityCombiningLQData, _Mapping]]] = ..., village_data: _Optional[_Iterable[_Union[ActivityVillageData, _Mapping]]] = ..., festival_data: _Optional[_Iterable[_Union[ActivityFestivalData, _Mapping]]] = ..., island_data: _Optional[_Iterable[_Union[ActivityIslandData, _Mapping]]] = ..., amulet_data: _Optional[_Iterable[_Union[ActivityAmuletData, _Mapping]]] = ..., story_data: _Optional[_Iterable[_Union[ActivityStoryData, _Mapping]]] = ...) -> None: ...

class SNSBlog(_message.Message):
    __slots__ = ["id", "read_time"]
    ID_FIELD_NUMBER: _ClassVar[int]
    READ_TIME_FIELD_NUMBER: _ClassVar[int]
    id: int
    read_time: int
    def __init__(self, id: _Optional[int] = ..., read_time: _Optional[int] = ...) -> None: ...

class SNSReply(_message.Message):
    __slots__ = ["id", "reply_time"]
    ID_FIELD_NUMBER: _ClassVar[int]
    REPLY_TIME_FIELD_NUMBER: _ClassVar[int]
    id: int
    reply_time: int
    def __init__(self, id: _Optional[int] = ..., reply_time: _Optional[int] = ...) -> None: ...

class ReqExchangeActivityItem(_message.Message):
    __slots__ = ["exchange_id", "count"]
    EXCHANGE_ID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    exchange_id: int
    count: int
    def __init__(self, exchange_id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class ResExchangeActivityItem(_message.Message):
    __slots__ = ["error", "execute_reward"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    EXECUTE_REWARD_FIELD_NUMBER: _ClassVar[int]
    error: Error
    execute_reward: _containers.RepeatedCompositeFieldContainer[ExecuteReward]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., execute_reward: _Optional[_Iterable[_Union[ExecuteReward, _Mapping]]] = ...) -> None: ...

class ReqCompleteActivityTask(_message.Message):
    __slots__ = ["task_id"]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    task_id: int
    def __init__(self, task_id: _Optional[int] = ...) -> None: ...

class ReqCompleteActivityTaskBatch(_message.Message):
    __slots__ = ["task_list"]
    TASK_LIST_FIELD_NUMBER: _ClassVar[int]
    task_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, task_list: _Optional[_Iterable[int]] = ...) -> None: ...

class ReqCompletePeriodActivityTaskBatch(_message.Message):
    __slots__ = ["task_list"]
    TASK_LIST_FIELD_NUMBER: _ClassVar[int]
    task_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, task_list: _Optional[_Iterable[int]] = ...) -> None: ...

class ReqReceiveActivityFlipTask(_message.Message):
    __slots__ = ["task_id"]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    task_id: int
    def __init__(self, task_id: _Optional[int] = ...) -> None: ...

class ResReceiveActivityFlipTask(_message.Message):
    __slots__ = ["count", "error"]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    count: int
    error: Error
    def __init__(self, count: _Optional[int] = ..., error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class ReqCompleteSegmentTaskReward(_message.Message):
    __slots__ = ["task_id", "count"]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    task_id: int
    count: int
    def __init__(self, task_id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class ResCompleteSegmentTaskReward(_message.Message):
    __slots__ = ["error", "rewards"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    REWARDS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    rewards: _containers.RepeatedCompositeFieldContainer[ExecuteReward]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., rewards: _Optional[_Iterable[_Union[ExecuteReward, _Mapping]]] = ...) -> None: ...

class ReqFetchActivityFlipInfo(_message.Message):
    __slots__ = ["activity_id"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ResFetchActivityFlipInfo(_message.Message):
    __slots__ = ["rewards", "count", "error"]
    REWARDS_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    rewards: _containers.RepeatedScalarFieldContainer[int]
    count: int
    error: Error
    def __init__(self, rewards: _Optional[_Iterable[int]] = ..., count: _Optional[int] = ..., error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class ReqGainAccumulatedPointActivityReward(_message.Message):
    __slots__ = ["activity_id", "reward_id"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    REWARD_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    reward_id: int
    def __init__(self, activity_id: _Optional[int] = ..., reward_id: _Optional[int] = ...) -> None: ...

class ReqGainMultiPointActivityReward(_message.Message):
    __slots__ = ["activity_id", "reward_id_list"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    REWARD_ID_LIST_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    reward_id_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, activity_id: _Optional[int] = ..., reward_id_list: _Optional[_Iterable[int]] = ...) -> None: ...

class ReqFetchRankPointLeaderboard(_message.Message):
    __slots__ = ["leaderboard_id"]
    LEADERBOARD_ID_FIELD_NUMBER: _ClassVar[int]
    leaderboard_id: int
    def __init__(self, leaderboard_id: _Optional[int] = ...) -> None: ...

class ResFetchRankPointLeaderboard(_message.Message):
    __slots__ = ["error", "items", "last_refresh_time"]
    class Item(_message.Message):
        __slots__ = ["account_id", "rank", "view", "point"]
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        RANK_FIELD_NUMBER: _ClassVar[int]
        VIEW_FIELD_NUMBER: _ClassVar[int]
        POINT_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        rank: int
        view: PlayerBaseView
        point: int
        def __init__(self, account_id: _Optional[int] = ..., rank: _Optional[int] = ..., view: _Optional[_Union[PlayerBaseView, _Mapping]] = ..., point: _Optional[int] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    LAST_REFRESH_TIME_FIELD_NUMBER: _ClassVar[int]
    error: Error
    items: _containers.RepeatedCompositeFieldContainer[ResFetchRankPointLeaderboard.Item]
    last_refresh_time: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., items: _Optional[_Iterable[_Union[ResFetchRankPointLeaderboard.Item, _Mapping]]] = ..., last_refresh_time: _Optional[int] = ...) -> None: ...

class ReqGainRankPointReward(_message.Message):
    __slots__ = ["leaderboard_id", "activity_id"]
    LEADERBOARD_ID_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    leaderboard_id: int
    activity_id: int
    def __init__(self, leaderboard_id: _Optional[int] = ..., activity_id: _Optional[int] = ...) -> None: ...

class ReqRichmanNextMove(_message.Message):
    __slots__ = ["activity_id"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ResRichmanNextMove(_message.Message):
    __slots__ = ["paths", "dice", "location", "finished_count", "step", "buff", "bank_save", "chest_position", "exp", "bank_save_add", "error"]
    class RewardData(_message.Message):
        __slots__ = ["resource_id", "count", "origin_count", "type"]
        RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
        COUNT_FIELD_NUMBER: _ClassVar[int]
        ORIGIN_COUNT_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        resource_id: int
        count: int
        origin_count: int
        type: int
        def __init__(self, resource_id: _Optional[int] = ..., count: _Optional[int] = ..., origin_count: _Optional[int] = ..., type: _Optional[int] = ...) -> None: ...
    class PathData(_message.Message):
        __slots__ = ["location", "rewards", "events"]
        LOCATION_FIELD_NUMBER: _ClassVar[int]
        REWARDS_FIELD_NUMBER: _ClassVar[int]
        EVENTS_FIELD_NUMBER: _ClassVar[int]
        location: int
        rewards: _containers.RepeatedCompositeFieldContainer[ResRichmanNextMove.RewardData]
        events: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, location: _Optional[int] = ..., rewards: _Optional[_Iterable[_Union[ResRichmanNextMove.RewardData, _Mapping]]] = ..., events: _Optional[_Iterable[int]] = ...) -> None: ...
    class BuffData(_message.Message):
        __slots__ = ["type", "remain", "effect"]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        REMAIN_FIELD_NUMBER: _ClassVar[int]
        EFFECT_FIELD_NUMBER: _ClassVar[int]
        type: int
        remain: int
        effect: int
        def __init__(self, type: _Optional[int] = ..., remain: _Optional[int] = ..., effect: _Optional[int] = ...) -> None: ...
    PATHS_FIELD_NUMBER: _ClassVar[int]
    DICE_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    FINISHED_COUNT_FIELD_NUMBER: _ClassVar[int]
    STEP_FIELD_NUMBER: _ClassVar[int]
    BUFF_FIELD_NUMBER: _ClassVar[int]
    BANK_SAVE_FIELD_NUMBER: _ClassVar[int]
    CHEST_POSITION_FIELD_NUMBER: _ClassVar[int]
    EXP_FIELD_NUMBER: _ClassVar[int]
    BANK_SAVE_ADD_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    paths: _containers.RepeatedCompositeFieldContainer[ResRichmanNextMove.PathData]
    dice: int
    location: int
    finished_count: int
    step: int
    buff: _containers.RepeatedCompositeFieldContainer[ResRichmanNextMove.BuffData]
    bank_save: int
    chest_position: int
    exp: int
    bank_save_add: int
    error: Error
    def __init__(self, paths: _Optional[_Iterable[_Union[ResRichmanNextMove.PathData, _Mapping]]] = ..., dice: _Optional[int] = ..., location: _Optional[int] = ..., finished_count: _Optional[int] = ..., step: _Optional[int] = ..., buff: _Optional[_Iterable[_Union[ResRichmanNextMove.BuffData, _Mapping]]] = ..., bank_save: _Optional[int] = ..., chest_position: _Optional[int] = ..., exp: _Optional[int] = ..., bank_save_add: _Optional[int] = ..., error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class ReqRichmanSpecialMove(_message.Message):
    __slots__ = ["activity_id", "step"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    STEP_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    step: int
    def __init__(self, activity_id: _Optional[int] = ..., step: _Optional[int] = ...) -> None: ...

class ReqRichmanChestInfo(_message.Message):
    __slots__ = ["activity_id"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ResRichmanChestInfo(_message.Message):
    __slots__ = ["items", "error"]
    class ItemData(_message.Message):
        __slots__ = ["id", "count"]
        ID_FIELD_NUMBER: _ClassVar[int]
        COUNT_FIELD_NUMBER: _ClassVar[int]
        id: int
        count: int
        def __init__(self, id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[ResRichmanChestInfo.ItemData]
    error: Error
    def __init__(self, items: _Optional[_Iterable[_Union[ResRichmanChestInfo.ItemData, _Mapping]]] = ..., error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class ReqCreateGameObserveAuth(_message.Message):
    __slots__ = ["game_uuid"]
    GAME_UUID_FIELD_NUMBER: _ClassVar[int]
    game_uuid: str
    def __init__(self, game_uuid: _Optional[str] = ...) -> None: ...

class ResCreateGameObserveAuth(_message.Message):
    __slots__ = ["error", "token", "location"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    error: Error
    token: str
    location: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., token: _Optional[str] = ..., location: _Optional[str] = ...) -> None: ...

class ReqRefreshGameObserveAuth(_message.Message):
    __slots__ = ["token"]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: str
    def __init__(self, token: _Optional[str] = ...) -> None: ...

class ResRefreshGameObserveAuth(_message.Message):
    __slots__ = ["error", "ttl"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    TTL_FIELD_NUMBER: _ClassVar[int]
    error: Error
    ttl: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., ttl: _Optional[int] = ...) -> None: ...

class ResActivityBuff(_message.Message):
    __slots__ = ["error", "buff_list"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    BUFF_LIST_FIELD_NUMBER: _ClassVar[int]
    error: Error
    buff_list: _containers.RepeatedCompositeFieldContainer[ActivityBuffData]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., buff_list: _Optional[_Iterable[_Union[ActivityBuffData, _Mapping]]] = ...) -> None: ...

class ReqUpgradeActivityBuff(_message.Message):
    __slots__ = ["buff_id"]
    BUFF_ID_FIELD_NUMBER: _ClassVar[int]
    buff_id: int
    def __init__(self, buff_id: _Optional[int] = ...) -> None: ...

class ReqUpgradeActivityLevel(_message.Message):
    __slots__ = ["activity_id", "group", "count"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    group: int
    count: int
    def __init__(self, activity_id: _Optional[int] = ..., group: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class ResUpgradeActivityLevel(_message.Message):
    __slots__ = ["error", "rewards"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    REWARDS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    rewards: _containers.RepeatedCompositeFieldContainer[ExecuteReward]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., rewards: _Optional[_Iterable[_Union[ExecuteReward, _Mapping]]] = ...) -> None: ...

class ReqReceiveUpgradeActivityReward(_message.Message):
    __slots__ = ["activity_id"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ResReceiveUpgradeActivityReward(_message.Message):
    __slots__ = ["error", "rewards"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    REWARDS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    rewards: _containers.RepeatedCompositeFieldContainer[ExecuteReward]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., rewards: _Optional[_Iterable[_Union[ExecuteReward, _Mapping]]] = ...) -> None: ...

class ReqReceiveAllActivityGift(_message.Message):
    __slots__ = ["activity_id"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ResReceiveAllActivityGift(_message.Message):
    __slots__ = ["error", "rewards", "receive_gift"]
    class ReceiveRewards(_message.Message):
        __slots__ = ["id", "from_account_id", "item_id", "count"]
        ID_FIELD_NUMBER: _ClassVar[int]
        FROM_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        ITEM_ID_FIELD_NUMBER: _ClassVar[int]
        COUNT_FIELD_NUMBER: _ClassVar[int]
        id: int
        from_account_id: int
        item_id: int
        count: int
        def __init__(self, id: _Optional[int] = ..., from_account_id: _Optional[int] = ..., item_id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    REWARDS_FIELD_NUMBER: _ClassVar[int]
    RECEIVE_GIFT_FIELD_NUMBER: _ClassVar[int]
    error: Error
    rewards: _containers.RepeatedCompositeFieldContainer[ExecuteReward]
    receive_gift: _containers.RepeatedCompositeFieldContainer[ResReceiveAllActivityGift.ReceiveRewards]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., rewards: _Optional[_Iterable[_Union[ExecuteReward, _Mapping]]] = ..., receive_gift: _Optional[_Iterable[_Union[ResReceiveAllActivityGift.ReceiveRewards, _Mapping]]] = ...) -> None: ...

class ResUpgradeChallenge(_message.Message):
    __slots__ = ["error", "task_progress", "refresh_count", "level", "match_count", "ticket_id"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    TASK_PROGRESS_FIELD_NUMBER: _ClassVar[int]
    REFRESH_COUNT_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    MATCH_COUNT_FIELD_NUMBER: _ClassVar[int]
    TICKET_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    task_progress: _containers.RepeatedCompositeFieldContainer[TaskProgress]
    refresh_count: int
    level: int
    match_count: int
    ticket_id: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., task_progress: _Optional[_Iterable[_Union[TaskProgress, _Mapping]]] = ..., refresh_count: _Optional[int] = ..., level: _Optional[int] = ..., match_count: _Optional[int] = ..., ticket_id: _Optional[int] = ...) -> None: ...

class ResRefreshChallenge(_message.Message):
    __slots__ = ["error", "task_progress", "refresh_count", "level", "match_count", "ticket_id"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    TASK_PROGRESS_FIELD_NUMBER: _ClassVar[int]
    REFRESH_COUNT_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    MATCH_COUNT_FIELD_NUMBER: _ClassVar[int]
    TICKET_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    task_progress: _containers.RepeatedCompositeFieldContainer[TaskProgress]
    refresh_count: int
    level: int
    match_count: int
    ticket_id: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., task_progress: _Optional[_Iterable[_Union[TaskProgress, _Mapping]]] = ..., refresh_count: _Optional[int] = ..., level: _Optional[int] = ..., match_count: _Optional[int] = ..., ticket_id: _Optional[int] = ...) -> None: ...

class ResFetchChallengeInfo(_message.Message):
    __slots__ = ["error", "task_progress", "refresh_count", "level", "match_count", "ticket_id", "rewarded_season"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    TASK_PROGRESS_FIELD_NUMBER: _ClassVar[int]
    REFRESH_COUNT_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    MATCH_COUNT_FIELD_NUMBER: _ClassVar[int]
    TICKET_ID_FIELD_NUMBER: _ClassVar[int]
    REWARDED_SEASON_FIELD_NUMBER: _ClassVar[int]
    error: Error
    task_progress: _containers.RepeatedCompositeFieldContainer[TaskProgress]
    refresh_count: int
    level: int
    match_count: int
    ticket_id: int
    rewarded_season: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., task_progress: _Optional[_Iterable[_Union[TaskProgress, _Mapping]]] = ..., refresh_count: _Optional[int] = ..., level: _Optional[int] = ..., match_count: _Optional[int] = ..., ticket_id: _Optional[int] = ..., rewarded_season: _Optional[_Iterable[int]] = ...) -> None: ...

class ReqForceCompleteChallengeTask(_message.Message):
    __slots__ = ["task_id"]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    task_id: int
    def __init__(self, task_id: _Optional[int] = ...) -> None: ...

class ResFetchABMatch(_message.Message):
    __slots__ = ["error", "match_id", "match_count", "buy_in_count", "point", "rewarded", "match_max_point", "quit"]
    class MatchPoint(_message.Message):
        __slots__ = ["match_id", "point"]
        MATCH_ID_FIELD_NUMBER: _ClassVar[int]
        POINT_FIELD_NUMBER: _ClassVar[int]
        match_id: int
        point: int
        def __init__(self, match_id: _Optional[int] = ..., point: _Optional[int] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    MATCH_COUNT_FIELD_NUMBER: _ClassVar[int]
    BUY_IN_COUNT_FIELD_NUMBER: _ClassVar[int]
    POINT_FIELD_NUMBER: _ClassVar[int]
    REWARDED_FIELD_NUMBER: _ClassVar[int]
    MATCH_MAX_POINT_FIELD_NUMBER: _ClassVar[int]
    QUIT_FIELD_NUMBER: _ClassVar[int]
    error: Error
    match_id: int
    match_count: int
    buy_in_count: int
    point: int
    rewarded: bool
    match_max_point: _containers.RepeatedCompositeFieldContainer[ResFetchABMatch.MatchPoint]
    quit: bool
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., match_id: _Optional[int] = ..., match_count: _Optional[int] = ..., buy_in_count: _Optional[int] = ..., point: _Optional[int] = ..., rewarded: bool = ..., match_max_point: _Optional[_Iterable[_Union[ResFetchABMatch.MatchPoint, _Mapping]]] = ..., quit: bool = ...) -> None: ...

class ReqStartUnifiedMatch(_message.Message):
    __slots__ = ["match_sid", "client_version_string"]
    MATCH_SID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    match_sid: str
    client_version_string: str
    def __init__(self, match_sid: _Optional[str] = ..., client_version_string: _Optional[str] = ...) -> None: ...

class ReqCancelUnifiedMatch(_message.Message):
    __slots__ = ["match_sid"]
    MATCH_SID_FIELD_NUMBER: _ClassVar[int]
    match_sid: str
    def __init__(self, match_sid: _Optional[str] = ...) -> None: ...

class ResChallengeSeasonInfo(_message.Message):
    __slots__ = ["error", "challenge_season_list"]
    class ChallengeInfo(_message.Message):
        __slots__ = ["season_id", "start_time", "end_time", "state"]
        SEASON_ID_FIELD_NUMBER: _ClassVar[int]
        START_TIME_FIELD_NUMBER: _ClassVar[int]
        END_TIME_FIELD_NUMBER: _ClassVar[int]
        STATE_FIELD_NUMBER: _ClassVar[int]
        season_id: int
        start_time: int
        end_time: int
        state: int
        def __init__(self, season_id: _Optional[int] = ..., start_time: _Optional[int] = ..., end_time: _Optional[int] = ..., state: _Optional[int] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    CHALLENGE_SEASON_LIST_FIELD_NUMBER: _ClassVar[int]
    error: Error
    challenge_season_list: _containers.RepeatedCompositeFieldContainer[ResChallengeSeasonInfo.ChallengeInfo]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., challenge_season_list: _Optional[_Iterable[_Union[ResChallengeSeasonInfo.ChallengeInfo, _Mapping]]] = ...) -> None: ...

class ReqReceiveChallengeRankReward(_message.Message):
    __slots__ = ["season_id"]
    SEASON_ID_FIELD_NUMBER: _ClassVar[int]
    season_id: int
    def __init__(self, season_id: _Optional[int] = ...) -> None: ...

class ResReceiveChallengeRankReward(_message.Message):
    __slots__ = ["error", "rewards"]
    class Reward(_message.Message):
        __slots__ = ["resource_id", "count"]
        RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
        COUNT_FIELD_NUMBER: _ClassVar[int]
        resource_id: int
        count: int
        def __init__(self, resource_id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    REWARDS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    rewards: _containers.RepeatedCompositeFieldContainer[ResReceiveChallengeRankReward.Reward]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., rewards: _Optional[_Iterable[_Union[ResReceiveChallengeRankReward.Reward, _Mapping]]] = ...) -> None: ...

class ReqBuyInABMatch(_message.Message):
    __slots__ = ["match_id"]
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    match_id: int
    def __init__(self, match_id: _Optional[int] = ...) -> None: ...

class ReqGamePointRank(_message.Message):
    __slots__ = ["activity_id"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ResGamePointRank(_message.Message):
    __slots__ = ["error", "rank", "self_rank"]
    class RankInfo(_message.Message):
        __slots__ = ["account_id", "point"]
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        POINT_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        point: int
        def __init__(self, account_id: _Optional[int] = ..., point: _Optional[int] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    RANK_FIELD_NUMBER: _ClassVar[int]
    SELF_RANK_FIELD_NUMBER: _ClassVar[int]
    error: Error
    rank: _containers.RepeatedCompositeFieldContainer[ResGamePointRank.RankInfo]
    self_rank: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., rank: _Optional[_Iterable[_Union[ResGamePointRank.RankInfo, _Mapping]]] = ..., self_rank: _Optional[int] = ...) -> None: ...

class ResFetchSelfGamePointRank(_message.Message):
    __slots__ = ["error", "self_rate"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    SELF_RATE_FIELD_NUMBER: _ClassVar[int]
    error: Error
    self_rate: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., self_rate: _Optional[int] = ...) -> None: ...

class ReqReadSNS(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class ResReadSNS(_message.Message):
    __slots__ = ["error", "sns_content"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    SNS_CONTENT_FIELD_NUMBER: _ClassVar[int]
    error: Error
    sns_content: SNSBlog
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., sns_content: _Optional[_Union[SNSBlog, _Mapping]] = ...) -> None: ...

class ReqReplySNS(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class ResReplySNS(_message.Message):
    __slots__ = ["error", "sns_reply"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    SNS_REPLY_FIELD_NUMBER: _ClassVar[int]
    error: Error
    sns_reply: SNSReply
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., sns_reply: _Optional[_Union[SNSReply, _Mapping]] = ...) -> None: ...

class ReqLikeSNS(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class ResLikeSNS(_message.Message):
    __slots__ = ["error", "is_liked"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    IS_LIKED_FIELD_NUMBER: _ClassVar[int]
    error: Error
    is_liked: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., is_liked: _Optional[int] = ...) -> None: ...

class ReqDigMine(_message.Message):
    __slots__ = ["activity_id", "point"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    POINT_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    point: Point
    def __init__(self, activity_id: _Optional[int] = ..., point: _Optional[_Union[Point, _Mapping]] = ...) -> None: ...

class ResDigMine(_message.Message):
    __slots__ = ["error", "map", "reward"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    MAP_FIELD_NUMBER: _ClassVar[int]
    REWARD_FIELD_NUMBER: _ClassVar[int]
    error: Error
    map: _containers.RepeatedCompositeFieldContainer[MineReward]
    reward: _containers.RepeatedCompositeFieldContainer[RewardSlot]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., map: _Optional[_Iterable[_Union[MineReward, _Mapping]]] = ..., reward: _Optional[_Iterable[_Union[RewardSlot, _Mapping]]] = ...) -> None: ...

class ReqFetchLastPrivacy(_message.Message):
    __slots__ = ["type"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    type: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, type: _Optional[_Iterable[int]] = ...) -> None: ...

class ResFetchLastPrivacy(_message.Message):
    __slots__ = ["error", "privacy"]
    class PrivacyInfo(_message.Message):
        __slots__ = ["type", "version"]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        VERSION_FIELD_NUMBER: _ClassVar[int]
        type: int
        version: str
        def __init__(self, type: _Optional[int] = ..., version: _Optional[str] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    PRIVACY_FIELD_NUMBER: _ClassVar[int]
    error: Error
    privacy: _containers.RepeatedCompositeFieldContainer[ResFetchLastPrivacy.PrivacyInfo]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., privacy: _Optional[_Iterable[_Union[ResFetchLastPrivacy.PrivacyInfo, _Mapping]]] = ...) -> None: ...

class ReqCheckPrivacy(_message.Message):
    __slots__ = ["device_type", "versions"]
    class Versions(_message.Message):
        __slots__ = ["version", "type"]
        VERSION_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        version: str
        type: int
        def __init__(self, version: _Optional[str] = ..., type: _Optional[int] = ...) -> None: ...
    DEVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    VERSIONS_FIELD_NUMBER: _ClassVar[int]
    device_type: str
    versions: _containers.RepeatedCompositeFieldContainer[ReqCheckPrivacy.Versions]
    def __init__(self, device_type: _Optional[str] = ..., versions: _Optional[_Iterable[_Union[ReqCheckPrivacy.Versions, _Mapping]]] = ...) -> None: ...

class ReqResponseCaptcha(_message.Message):
    __slots__ = ["check_id", "check_time", "result", "client_version_string", "type"]
    CHECK_ID_FIELD_NUMBER: _ClassVar[int]
    CHECK_TIME_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    check_id: int
    check_time: int
    result: str
    client_version_string: str
    type: int
    def __init__(self, check_id: _Optional[int] = ..., check_time: _Optional[int] = ..., result: _Optional[str] = ..., client_version_string: _Optional[str] = ..., type: _Optional[int] = ...) -> None: ...

class ReqFetchRPGBattleHistory(_message.Message):
    __slots__ = ["activity_id"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ResFetchRPGBattleHistory(_message.Message):
    __slots__ = ["error", "battle_result", "start_state", "current_state"]
    class BattleResult(_message.Message):
        __slots__ = ["uuid", "chang", "ju", "ben", "target", "damage", "heal", "monster_seq", "chain_atk", "killed", "is_luk", "is_dex", "is_extra", "reward", "points", "is_zimo"]
        UUID_FIELD_NUMBER: _ClassVar[int]
        CHANG_FIELD_NUMBER: _ClassVar[int]
        JU_FIELD_NUMBER: _ClassVar[int]
        BEN_FIELD_NUMBER: _ClassVar[int]
        TARGET_FIELD_NUMBER: _ClassVar[int]
        DAMAGE_FIELD_NUMBER: _ClassVar[int]
        HEAL_FIELD_NUMBER: _ClassVar[int]
        MONSTER_SEQ_FIELD_NUMBER: _ClassVar[int]
        CHAIN_ATK_FIELD_NUMBER: _ClassVar[int]
        KILLED_FIELD_NUMBER: _ClassVar[int]
        IS_LUK_FIELD_NUMBER: _ClassVar[int]
        IS_DEX_FIELD_NUMBER: _ClassVar[int]
        IS_EXTRA_FIELD_NUMBER: _ClassVar[int]
        REWARD_FIELD_NUMBER: _ClassVar[int]
        POINTS_FIELD_NUMBER: _ClassVar[int]
        IS_ZIMO_FIELD_NUMBER: _ClassVar[int]
        uuid: str
        chang: int
        ju: int
        ben: int
        target: int
        damage: int
        heal: int
        monster_seq: int
        chain_atk: int
        killed: int
        is_luk: int
        is_dex: int
        is_extra: int
        reward: str
        points: int
        is_zimo: int
        def __init__(self, uuid: _Optional[str] = ..., chang: _Optional[int] = ..., ju: _Optional[int] = ..., ben: _Optional[int] = ..., target: _Optional[int] = ..., damage: _Optional[int] = ..., heal: _Optional[int] = ..., monster_seq: _Optional[int] = ..., chain_atk: _Optional[int] = ..., killed: _Optional[int] = ..., is_luk: _Optional[int] = ..., is_dex: _Optional[int] = ..., is_extra: _Optional[int] = ..., reward: _Optional[str] = ..., points: _Optional[int] = ..., is_zimo: _Optional[int] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    BATTLE_RESULT_FIELD_NUMBER: _ClassVar[int]
    START_STATE_FIELD_NUMBER: _ClassVar[int]
    CURRENT_STATE_FIELD_NUMBER: _ClassVar[int]
    error: Error
    battle_result: _containers.RepeatedCompositeFieldContainer[ResFetchRPGBattleHistory.BattleResult]
    start_state: RPGState
    current_state: RPGState
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., battle_result: _Optional[_Iterable[_Union[ResFetchRPGBattleHistory.BattleResult, _Mapping]]] = ..., start_state: _Optional[_Union[RPGState, _Mapping]] = ..., current_state: _Optional[_Union[RPGState, _Mapping]] = ...) -> None: ...

class ResFetchRPGBattleHistoryV2(_message.Message):
    __slots__ = ["error", "battle_result", "start_state", "current_state", "recent_battle_result"]
    class BattleResultV2(_message.Message):
        __slots__ = ["uuid", "chang", "ju", "ben", "damage", "monster_seq", "killed", "buff", "points"]
        UUID_FIELD_NUMBER: _ClassVar[int]
        CHANG_FIELD_NUMBER: _ClassVar[int]
        JU_FIELD_NUMBER: _ClassVar[int]
        BEN_FIELD_NUMBER: _ClassVar[int]
        DAMAGE_FIELD_NUMBER: _ClassVar[int]
        MONSTER_SEQ_FIELD_NUMBER: _ClassVar[int]
        KILLED_FIELD_NUMBER: _ClassVar[int]
        BUFF_FIELD_NUMBER: _ClassVar[int]
        POINTS_FIELD_NUMBER: _ClassVar[int]
        uuid: str
        chang: int
        ju: int
        ben: int
        damage: int
        monster_seq: int
        killed: int
        buff: _containers.RepeatedCompositeFieldContainer[ActivityBuffData]
        points: int
        def __init__(self, uuid: _Optional[str] = ..., chang: _Optional[int] = ..., ju: _Optional[int] = ..., ben: _Optional[int] = ..., damage: _Optional[int] = ..., monster_seq: _Optional[int] = ..., killed: _Optional[int] = ..., buff: _Optional[_Iterable[_Union[ActivityBuffData, _Mapping]]] = ..., points: _Optional[int] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    BATTLE_RESULT_FIELD_NUMBER: _ClassVar[int]
    START_STATE_FIELD_NUMBER: _ClassVar[int]
    CURRENT_STATE_FIELD_NUMBER: _ClassVar[int]
    RECENT_BATTLE_RESULT_FIELD_NUMBER: _ClassVar[int]
    error: Error
    battle_result: _containers.RepeatedCompositeFieldContainer[ResFetchRPGBattleHistoryV2.BattleResultV2]
    start_state: RPGState
    current_state: RPGState
    recent_battle_result: _containers.RepeatedCompositeFieldContainer[ResFetchRPGBattleHistoryV2.BattleResultV2]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., battle_result: _Optional[_Iterable[_Union[ResFetchRPGBattleHistoryV2.BattleResultV2, _Mapping]]] = ..., start_state: _Optional[_Union[RPGState, _Mapping]] = ..., current_state: _Optional[_Union[RPGState, _Mapping]] = ..., recent_battle_result: _Optional[_Iterable[_Union[ResFetchRPGBattleHistoryV2.BattleResultV2, _Mapping]]] = ...) -> None: ...

class ReqBuyArenaTicket(_message.Message):
    __slots__ = ["activity_id"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ReqArenaReward(_message.Message):
    __slots__ = ["activity_id"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ReqEnterArena(_message.Message):
    __slots__ = ["activity_id"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ResArenaReward(_message.Message):
    __slots__ = ["error", "items"]
    class RewardItem(_message.Message):
        __slots__ = ["id", "count"]
        ID_FIELD_NUMBER: _ClassVar[int]
        COUNT_FIELD_NUMBER: _ClassVar[int]
        id: int
        count: int
        def __init__(self, id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    items: _containers.RepeatedCompositeFieldContainer[ResArenaReward.RewardItem]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., items: _Optional[_Iterable[_Union[ResArenaReward.RewardItem, _Mapping]]] = ...) -> None: ...

class ReqReceiveRPGRewards(_message.Message):
    __slots__ = ["activity_id"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ReqReceiveRPGReward(_message.Message):
    __slots__ = ["activity_id", "monster_seq"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    MONSTER_SEQ_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    monster_seq: int
    def __init__(self, activity_id: _Optional[int] = ..., monster_seq: _Optional[int] = ...) -> None: ...

class ResReceiveRPGRewards(_message.Message):
    __slots__ = ["error", "items"]
    class RewardItem(_message.Message):
        __slots__ = ["id", "count"]
        ID_FIELD_NUMBER: _ClassVar[int]
        COUNT_FIELD_NUMBER: _ClassVar[int]
        id: int
        count: int
        def __init__(self, id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    items: _containers.RepeatedCompositeFieldContainer[ResReceiveRPGRewards.RewardItem]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., items: _Optional[_Iterable[_Union[ResReceiveRPGRewards.RewardItem, _Mapping]]] = ...) -> None: ...

class ReqFetchOBToken(_message.Message):
    __slots__ = ["uuid"]
    UUID_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    def __init__(self, uuid: _Optional[str] = ...) -> None: ...

class ResFetchOBToken(_message.Message):
    __slots__ = ["error", "token", "create_time", "delay", "start_time"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    DELAY_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    error: Error
    token: str
    create_time: int
    delay: int
    start_time: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., token: _Optional[str] = ..., create_time: _Optional[int] = ..., delay: _Optional[int] = ..., start_time: _Optional[int] = ...) -> None: ...

class ReqReceiveCharacterRewards(_message.Message):
    __slots__ = ["character_id", "level"]
    CHARACTER_ID_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    character_id: int
    level: int
    def __init__(self, character_id: _Optional[int] = ..., level: _Optional[int] = ...) -> None: ...

class ResReceiveCharacterRewards(_message.Message):
    __slots__ = ["error", "items"]
    class RewardItem(_message.Message):
        __slots__ = ["id", "count"]
        ID_FIELD_NUMBER: _ClassVar[int]
        COUNT_FIELD_NUMBER: _ClassVar[int]
        id: int
        count: int
        def __init__(self, id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    items: _containers.RepeatedCompositeFieldContainer[ResReceiveCharacterRewards.RewardItem]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., items: _Optional[_Iterable[_Union[ResReceiveCharacterRewards.RewardItem, _Mapping]]] = ...) -> None: ...

class ReqFeedActivityFeed(_message.Message):
    __slots__ = ["activity_id", "count"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    count: int
    def __init__(self, activity_id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class ResFeedActivityFeed(_message.Message):
    __slots__ = ["error", "items", "feed_count"]
    class RewardItem(_message.Message):
        __slots__ = ["id", "count"]
        ID_FIELD_NUMBER: _ClassVar[int]
        COUNT_FIELD_NUMBER: _ClassVar[int]
        id: int
        count: int
        def __init__(self, id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    FEED_COUNT_FIELD_NUMBER: _ClassVar[int]
    error: Error
    items: _containers.RepeatedCompositeFieldContainer[ResFeedActivityFeed.RewardItem]
    feed_count: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., items: _Optional[_Iterable[_Union[ResFeedActivityFeed.RewardItem, _Mapping]]] = ..., feed_count: _Optional[int] = ...) -> None: ...

class ReqSendActivityGiftToFriend(_message.Message):
    __slots__ = ["activity_id", "item_id", "target_id"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    item_id: int
    target_id: int
    def __init__(self, activity_id: _Optional[int] = ..., item_id: _Optional[int] = ..., target_id: _Optional[int] = ...) -> None: ...

class ResSendActivityGiftToFriend(_message.Message):
    __slots__ = ["error", "send_gift_count"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    SEND_GIFT_COUNT_FIELD_NUMBER: _ClassVar[int]
    error: Error
    send_gift_count: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., send_gift_count: _Optional[int] = ...) -> None: ...

class ReqReceiveActivityGift(_message.Message):
    __slots__ = ["activity_id", "id"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    id: int
    def __init__(self, activity_id: _Optional[int] = ..., id: _Optional[int] = ...) -> None: ...

class ReqFetchFriendGiftActivityData(_message.Message):
    __slots__ = ["activity_id", "account_list"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_LIST_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    account_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, activity_id: _Optional[int] = ..., account_list: _Optional[_Iterable[int]] = ...) -> None: ...

class ResFetchFriendGiftActivityData(_message.Message):
    __slots__ = ["error", "list"]
    class ItemCountData(_message.Message):
        __slots__ = ["item", "count"]
        ITEM_FIELD_NUMBER: _ClassVar[int]
        COUNT_FIELD_NUMBER: _ClassVar[int]
        item: int
        count: int
        def __init__(self, item: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...
    class FriendData(_message.Message):
        __slots__ = ["account_id", "items", "receive_count"]
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        ITEMS_FIELD_NUMBER: _ClassVar[int]
        RECEIVE_COUNT_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        items: _containers.RepeatedCompositeFieldContainer[ResFetchFriendGiftActivityData.ItemCountData]
        receive_count: int
        def __init__(self, account_id: _Optional[int] = ..., items: _Optional[_Iterable[_Union[ResFetchFriendGiftActivityData.ItemCountData, _Mapping]]] = ..., receive_count: _Optional[int] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    LIST_FIELD_NUMBER: _ClassVar[int]
    error: Error
    list: _containers.RepeatedCompositeFieldContainer[ResFetchFriendGiftActivityData.FriendData]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., list: _Optional[_Iterable[_Union[ResFetchFriendGiftActivityData.FriendData, _Mapping]]] = ...) -> None: ...

class ReqOpenPreChestItem(_message.Message):
    __slots__ = ["item_id", "pool_id"]
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    item_id: int
    pool_id: int
    def __init__(self, item_id: _Optional[int] = ..., pool_id: _Optional[int] = ...) -> None: ...

class ResOpenPreChestItem(_message.Message):
    __slots__ = ["error", "results"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    results: _containers.RepeatedCompositeFieldContainer[OpenResult]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., results: _Optional[_Iterable[_Union[OpenResult, _Mapping]]] = ...) -> None: ...

class ReqFetchVoteActivity(_message.Message):
    __slots__ = ["activity_id"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ResFetchVoteActivity(_message.Message):
    __slots__ = ["error", "vote_rank", "update_time"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    VOTE_RANK_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    error: Error
    vote_rank: _containers.RepeatedScalarFieldContainer[int]
    update_time: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., vote_rank: _Optional[_Iterable[int]] = ..., update_time: _Optional[int] = ...) -> None: ...

class ReqVoteActivity(_message.Message):
    __slots__ = ["vote", "activity_id"]
    VOTE_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    vote: int
    activity_id: int
    def __init__(self, vote: _Optional[int] = ..., activity_id: _Optional[int] = ...) -> None: ...

class ResVoteActivity(_message.Message):
    __slots__ = ["error", "vote_records"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    VOTE_RECORDS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    vote_records: _containers.RepeatedCompositeFieldContainer[VoteData]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., vote_records: _Optional[_Iterable[_Union[VoteData, _Mapping]]] = ...) -> None: ...

class ReqUnlockActivitySpot(_message.Message):
    __slots__ = ["unique_id"]
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    unique_id: int
    def __init__(self, unique_id: _Optional[int] = ...) -> None: ...

class ReqUnlockActivitySpotEnding(_message.Message):
    __slots__ = ["unique_id", "ending_id"]
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    ENDING_ID_FIELD_NUMBER: _ClassVar[int]
    unique_id: int
    ending_id: int
    def __init__(self, unique_id: _Optional[int] = ..., ending_id: _Optional[int] = ...) -> None: ...

class ReqReceiveActivitySpotReward(_message.Message):
    __slots__ = ["unique_id"]
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    unique_id: int
    def __init__(self, unique_id: _Optional[int] = ...) -> None: ...

class ResReceiveActivitySpotReward(_message.Message):
    __slots__ = ["error", "items"]
    class RewardItem(_message.Message):
        __slots__ = ["id", "count"]
        ID_FIELD_NUMBER: _ClassVar[int]
        COUNT_FIELD_NUMBER: _ClassVar[int]
        id: int
        count: int
        def __init__(self, id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    items: _containers.RepeatedCompositeFieldContainer[ResReceiveActivitySpotReward.RewardItem]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., items: _Optional[_Iterable[_Union[ResReceiveActivitySpotReward.RewardItem, _Mapping]]] = ...) -> None: ...

class ReqLogReport(_message.Message):
    __slots__ = ["success", "failed"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    FAILED_FIELD_NUMBER: _ClassVar[int]
    success: int
    failed: int
    def __init__(self, success: _Optional[int] = ..., failed: _Optional[int] = ...) -> None: ...

class ReqBindOauth2(_message.Message):
    __slots__ = ["type", "token"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    type: int
    token: str
    def __init__(self, type: _Optional[int] = ..., token: _Optional[str] = ...) -> None: ...

class ReqFetchOauth2(_message.Message):
    __slots__ = ["type"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    type: int
    def __init__(self, type: _Optional[int] = ...) -> None: ...

class ResFetchOauth2(_message.Message):
    __slots__ = ["error", "openid"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    OPENID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    openid: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., openid: _Optional[str] = ...) -> None: ...

class ResDeleteAccount(_message.Message):
    __slots__ = ["error", "delete_time"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    DELETE_TIME_FIELD_NUMBER: _ClassVar[int]
    error: Error
    delete_time: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., delete_time: _Optional[int] = ...) -> None: ...

class ReqSetLoadingImage(_message.Message):
    __slots__ = ["images"]
    IMAGES_FIELD_NUMBER: _ClassVar[int]
    images: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, images: _Optional[_Iterable[int]] = ...) -> None: ...

class ResFetchShopInterval(_message.Message):
    __slots__ = ["error", "result"]
    class ShopInterval(_message.Message):
        __slots__ = ["group_id", "interval"]
        GROUP_ID_FIELD_NUMBER: _ClassVar[int]
        INTERVAL_FIELD_NUMBER: _ClassVar[int]
        group_id: int
        interval: int
        def __init__(self, group_id: _Optional[int] = ..., interval: _Optional[int] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    error: Error
    result: _containers.RepeatedCompositeFieldContainer[ResFetchShopInterval.ShopInterval]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., result: _Optional[_Iterable[_Union[ResFetchShopInterval.ShopInterval, _Mapping]]] = ...) -> None: ...

class ResFetchActivityInterval(_message.Message):
    __slots__ = ["error", "result"]
    class ActivityInterval(_message.Message):
        __slots__ = ["activity_id", "interval"]
        ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
        INTERVAL_FIELD_NUMBER: _ClassVar[int]
        activity_id: int
        interval: int
        def __init__(self, activity_id: _Optional[int] = ..., interval: _Optional[int] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    error: Error
    result: _containers.RepeatedCompositeFieldContainer[ResFetchActivityInterval.ActivityInterval]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., result: _Optional[_Iterable[_Union[ResFetchActivityInterval.ActivityInterval, _Mapping]]] = ...) -> None: ...

class ResFetchrecentFriend(_message.Message):
    __slots__ = ["error", "account_list"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_LIST_FIELD_NUMBER: _ClassVar[int]
    error: Error
    account_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., account_list: _Optional[_Iterable[int]] = ...) -> None: ...

class ReqOpenGacha(_message.Message):
    __slots__ = ["activity_id", "count"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    count: int
    def __init__(self, activity_id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class ResOpenGacha(_message.Message):
    __slots__ = ["error", "result_list", "reward_items", "sp_reward_items", "remain_count"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    RESULT_LIST_FIELD_NUMBER: _ClassVar[int]
    REWARD_ITEMS_FIELD_NUMBER: _ClassVar[int]
    SP_REWARD_ITEMS_FIELD_NUMBER: _ClassVar[int]
    REMAIN_COUNT_FIELD_NUMBER: _ClassVar[int]
    error: Error
    result_list: _containers.RepeatedScalarFieldContainer[int]
    reward_items: _containers.RepeatedCompositeFieldContainer[ExecuteReward]
    sp_reward_items: _containers.RepeatedCompositeFieldContainer[ExecuteReward]
    remain_count: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., result_list: _Optional[_Iterable[int]] = ..., reward_items: _Optional[_Iterable[_Union[ExecuteReward, _Mapping]]] = ..., sp_reward_items: _Optional[_Iterable[_Union[ExecuteReward, _Mapping]]] = ..., remain_count: _Optional[int] = ...) -> None: ...

class ReqTaskRequest(_message.Message):
    __slots__ = ["params"]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    params: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, params: _Optional[_Iterable[int]] = ...) -> None: ...

class ReqSimulationActivityTrain(_message.Message):
    __slots__ = ["activity_id", "type"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    type: int
    def __init__(self, activity_id: _Optional[int] = ..., type: _Optional[int] = ...) -> None: ...

class ResSimulationActivityTrain(_message.Message):
    __slots__ = ["error", "result_type", "final_stats"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    RESULT_TYPE_FIELD_NUMBER: _ClassVar[int]
    FINAL_STATS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    result_type: int
    final_stats: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., result_type: _Optional[int] = ..., final_stats: _Optional[_Iterable[int]] = ...) -> None: ...

class ReqFetchSimulationGameRecord(_message.Message):
    __slots__ = ["game_uuid", "activity_id"]
    GAME_UUID_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    game_uuid: str
    activity_id: int
    def __init__(self, game_uuid: _Optional[str] = ..., activity_id: _Optional[int] = ...) -> None: ...

class ResFetchSimulationGameRecord(_message.Message):
    __slots__ = ["error", "messages"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    error: Error
    messages: _containers.RepeatedCompositeFieldContainer[ActivitySimulationGameRecordMessage]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., messages: _Optional[_Iterable[_Union[ActivitySimulationGameRecordMessage, _Mapping]]] = ...) -> None: ...

class ReqStartSimulationActivityGame(_message.Message):
    __slots__ = ["activity_id"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ResStartSimulationActivityGame(_message.Message):
    __slots__ = ["error", "records"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    RECORDS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    records: _containers.RepeatedCompositeFieldContainer[ActivitySimulationGameRecord]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., records: _Optional[_Iterable[_Union[ActivitySimulationGameRecord, _Mapping]]] = ...) -> None: ...

class ReqFetchSimulationGameRank(_message.Message):
    __slots__ = ["activity_id", "day"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    DAY_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    day: int
    def __init__(self, activity_id: _Optional[int] = ..., day: _Optional[int] = ...) -> None: ...

class ResFetchSimulationGameRank(_message.Message):
    __slots__ = ["error", "rank"]
    class RankInfo(_message.Message):
        __slots__ = ["character", "score"]
        CHARACTER_FIELD_NUMBER: _ClassVar[int]
        SCORE_FIELD_NUMBER: _ClassVar[int]
        character: int
        score: float
        def __init__(self, character: _Optional[int] = ..., score: _Optional[float] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    RANK_FIELD_NUMBER: _ClassVar[int]
    error: Error
    rank: _containers.RepeatedCompositeFieldContainer[ResFetchSimulationGameRank.RankInfo]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., rank: _Optional[_Iterable[_Union[ResFetchSimulationGameRank.RankInfo, _Mapping]]] = ...) -> None: ...

class ReqGenerateCombiningCraft(_message.Message):
    __slots__ = ["activity_id", "bin_id"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    BIN_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    bin_id: int
    def __init__(self, activity_id: _Optional[int] = ..., bin_id: _Optional[int] = ...) -> None: ...

class ResGenerateCombiningCraft(_message.Message):
    __slots__ = ["error", "pos", "craft_id"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    POS_FIELD_NUMBER: _ClassVar[int]
    CRAFT_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    pos: int
    craft_id: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., pos: _Optional[int] = ..., craft_id: _Optional[int] = ...) -> None: ...

class ReqMoveCombiningCraft(_message.Message):
    __slots__ = ["activity_id", "to"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    FROM_FIELD_NUMBER: _ClassVar[int]
    TO_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    to: int
    def __init__(self, activity_id: _Optional[int] = ..., to: _Optional[int] = ..., **kwargs) -> None: ...

class ResMoveCombiningCraft(_message.Message):
    __slots__ = ["error", "pos", "combined", "craft_id", "bonus"]
    class BonusData(_message.Message):
        __slots__ = ["craft_id", "pos"]
        CRAFT_ID_FIELD_NUMBER: _ClassVar[int]
        POS_FIELD_NUMBER: _ClassVar[int]
        craft_id: int
        pos: int
        def __init__(self, craft_id: _Optional[int] = ..., pos: _Optional[int] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    POS_FIELD_NUMBER: _ClassVar[int]
    COMBINED_FIELD_NUMBER: _ClassVar[int]
    CRAFT_ID_FIELD_NUMBER: _ClassVar[int]
    BONUS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    pos: int
    combined: int
    craft_id: int
    bonus: ResMoveCombiningCraft.BonusData
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., pos: _Optional[int] = ..., combined: _Optional[int] = ..., craft_id: _Optional[int] = ..., bonus: _Optional[_Union[ResMoveCombiningCraft.BonusData, _Mapping]] = ...) -> None: ...

class ReqCombiningRecycleCraft(_message.Message):
    __slots__ = ["activity_id", "pos"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    POS_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    pos: int
    def __init__(self, activity_id: _Optional[int] = ..., pos: _Optional[int] = ...) -> None: ...

class ResCombiningRecycleCraft(_message.Message):
    __slots__ = ["error", "reward_items"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    REWARD_ITEMS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    reward_items: _containers.RepeatedCompositeFieldContainer[ExecuteReward]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., reward_items: _Optional[_Iterable[_Union[ExecuteReward, _Mapping]]] = ...) -> None: ...

class ReqRecoverCombiningRecycle(_message.Message):
    __slots__ = ["activity_id"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ResRecoverCombiningRecycle(_message.Message):
    __slots__ = ["error", "craft_id", "pos"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    CRAFT_ID_FIELD_NUMBER: _ClassVar[int]
    POS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    craft_id: int
    pos: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., craft_id: _Optional[int] = ..., pos: _Optional[int] = ...) -> None: ...

class ReqFinishCombiningOrder(_message.Message):
    __slots__ = ["activity_id", "craft_pos", "order_pos"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    CRAFT_POS_FIELD_NUMBER: _ClassVar[int]
    ORDER_POS_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    craft_pos: int
    order_pos: int
    def __init__(self, activity_id: _Optional[int] = ..., craft_pos: _Optional[int] = ..., order_pos: _Optional[int] = ...) -> None: ...

class ResFinishCombiningOrder(_message.Message):
    __slots__ = ["error", "reward_items"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    REWARD_ITEMS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    reward_items: _containers.RepeatedCompositeFieldContainer[ExecuteReward]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., reward_items: _Optional[_Iterable[_Union[ExecuteReward, _Mapping]]] = ...) -> None: ...

class ResFetchInfo(_message.Message):
    __slots__ = ["error", "server_time", "server_setting", "client_value", "friend_list", "friend_apply_list", "recent_friend", "mail_info", "receive_coin_info", "title_list", "bag_info", "shop_info", "shop_interval", "activity_data", "activity_interval", "activity_buff", "vip_reward", "month_ticket_info", "achievement", "comment_setting", "account_settings", "mod_nickname_time", "misc", "announcement", "activity_list", "character_info", "all_common_views", "collected_game_record_list", "maintain_notice"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    SERVER_TIME_FIELD_NUMBER: _ClassVar[int]
    SERVER_SETTING_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VALUE_FIELD_NUMBER: _ClassVar[int]
    FRIEND_LIST_FIELD_NUMBER: _ClassVar[int]
    FRIEND_APPLY_LIST_FIELD_NUMBER: _ClassVar[int]
    RECENT_FRIEND_FIELD_NUMBER: _ClassVar[int]
    MAIL_INFO_FIELD_NUMBER: _ClassVar[int]
    RECEIVE_COIN_INFO_FIELD_NUMBER: _ClassVar[int]
    TITLE_LIST_FIELD_NUMBER: _ClassVar[int]
    BAG_INFO_FIELD_NUMBER: _ClassVar[int]
    SHOP_INFO_FIELD_NUMBER: _ClassVar[int]
    SHOP_INTERVAL_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_DATA_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_INTERVAL_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_BUFF_FIELD_NUMBER: _ClassVar[int]
    VIP_REWARD_FIELD_NUMBER: _ClassVar[int]
    MONTH_TICKET_INFO_FIELD_NUMBER: _ClassVar[int]
    ACHIEVEMENT_FIELD_NUMBER: _ClassVar[int]
    COMMENT_SETTING_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    MOD_NICKNAME_TIME_FIELD_NUMBER: _ClassVar[int]
    MISC_FIELD_NUMBER: _ClassVar[int]
    ANNOUNCEMENT_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_LIST_FIELD_NUMBER: _ClassVar[int]
    CHARACTER_INFO_FIELD_NUMBER: _ClassVar[int]
    ALL_COMMON_VIEWS_FIELD_NUMBER: _ClassVar[int]
    COLLECTED_GAME_RECORD_LIST_FIELD_NUMBER: _ClassVar[int]
    MAINTAIN_NOTICE_FIELD_NUMBER: _ClassVar[int]
    error: Error
    server_time: ResServerTime
    server_setting: ResServerSettings
    client_value: ResClientValue
    friend_list: ResFriendList
    friend_apply_list: ResFriendApplyList
    recent_friend: ResFetchrecentFriend
    mail_info: ResMailInfo
    receive_coin_info: ResReviveCoinInfo
    title_list: ResTitleList
    bag_info: ResBagInfo
    shop_info: ResShopInfo
    shop_interval: ResFetchShopInterval
    activity_data: ResAccountActivityData
    activity_interval: ResFetchActivityInterval
    activity_buff: ResActivityBuff
    vip_reward: ResVipReward
    month_ticket_info: ResMonthTicketInfo
    achievement: ResAchievement
    comment_setting: ResCommentSetting
    account_settings: ResAccountSettings
    mod_nickname_time: ResModNicknameTime
    misc: ResMisc
    announcement: ResAnnouncement
    activity_list: ResActivityList
    character_info: ResCharacterInfo
    all_common_views: ResAllcommonViews
    collected_game_record_list: ResCollectedGameRecordList
    maintain_notice: ResFetchMaintainNotice
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., server_time: _Optional[_Union[ResServerTime, _Mapping]] = ..., server_setting: _Optional[_Union[ResServerSettings, _Mapping]] = ..., client_value: _Optional[_Union[ResClientValue, _Mapping]] = ..., friend_list: _Optional[_Union[ResFriendList, _Mapping]] = ..., friend_apply_list: _Optional[_Union[ResFriendApplyList, _Mapping]] = ..., recent_friend: _Optional[_Union[ResFetchrecentFriend, _Mapping]] = ..., mail_info: _Optional[_Union[ResMailInfo, _Mapping]] = ..., receive_coin_info: _Optional[_Union[ResReviveCoinInfo, _Mapping]] = ..., title_list: _Optional[_Union[ResTitleList, _Mapping]] = ..., bag_info: _Optional[_Union[ResBagInfo, _Mapping]] = ..., shop_info: _Optional[_Union[ResShopInfo, _Mapping]] = ..., shop_interval: _Optional[_Union[ResFetchShopInterval, _Mapping]] = ..., activity_data: _Optional[_Union[ResAccountActivityData, _Mapping]] = ..., activity_interval: _Optional[_Union[ResFetchActivityInterval, _Mapping]] = ..., activity_buff: _Optional[_Union[ResActivityBuff, _Mapping]] = ..., vip_reward: _Optional[_Union[ResVipReward, _Mapping]] = ..., month_ticket_info: _Optional[_Union[ResMonthTicketInfo, _Mapping]] = ..., achievement: _Optional[_Union[ResAchievement, _Mapping]] = ..., comment_setting: _Optional[_Union[ResCommentSetting, _Mapping]] = ..., account_settings: _Optional[_Union[ResAccountSettings, _Mapping]] = ..., mod_nickname_time: _Optional[_Union[ResModNicknameTime, _Mapping]] = ..., misc: _Optional[_Union[ResMisc, _Mapping]] = ..., announcement: _Optional[_Union[ResAnnouncement, _Mapping]] = ..., activity_list: _Optional[_Union[ResActivityList, _Mapping]] = ..., character_info: _Optional[_Union[ResCharacterInfo, _Mapping]] = ..., all_common_views: _Optional[_Union[ResAllcommonViews, _Mapping]] = ..., collected_game_record_list: _Optional[_Union[ResCollectedGameRecordList, _Mapping]] = ..., maintain_notice: _Optional[_Union[ResFetchMaintainNotice, _Mapping]] = ...) -> None: ...

class ReqUpgradeVillageBuilding(_message.Message):
    __slots__ = ["building_id", "activity_id"]
    BUILDING_ID_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    building_id: int
    activity_id: int
    def __init__(self, building_id: _Optional[int] = ..., activity_id: _Optional[int] = ...) -> None: ...

class ReqReceiveVillageBuildingReward(_message.Message):
    __slots__ = ["activity_id", "building_id", "rewards"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    BUILDING_ID_FIELD_NUMBER: _ClassVar[int]
    REWARDS_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    building_id: int
    rewards: _containers.RepeatedCompositeFieldContainer[RewardSlot]
    def __init__(self, activity_id: _Optional[int] = ..., building_id: _Optional[int] = ..., rewards: _Optional[_Iterable[_Union[RewardSlot, _Mapping]]] = ...) -> None: ...

class ResReceiveVillageBuildingReward(_message.Message):
    __slots__ = ["error", "reward_items"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    REWARD_ITEMS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    reward_items: _containers.RepeatedCompositeFieldContainer[ExecuteReward]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., reward_items: _Optional[_Iterable[_Union[ExecuteReward, _Mapping]]] = ...) -> None: ...

class ReqStartVillageTrip(_message.Message):
    __slots__ = ["dest", "activity_id"]
    DEST_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    dest: int
    activity_id: int
    def __init__(self, dest: _Optional[int] = ..., activity_id: _Optional[int] = ...) -> None: ...

class ReqReceiveVillageTripReward(_message.Message):
    __slots__ = ["activity_id", "dest_id", "rewards"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    DEST_ID_FIELD_NUMBER: _ClassVar[int]
    REWARDS_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    dest_id: int
    rewards: _containers.RepeatedCompositeFieldContainer[RewardSlot]
    def __init__(self, activity_id: _Optional[int] = ..., dest_id: _Optional[int] = ..., rewards: _Optional[_Iterable[_Union[RewardSlot, _Mapping]]] = ...) -> None: ...

class ResReceiveVillageTripReward(_message.Message):
    __slots__ = ["error", "reward_items"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    REWARD_ITEMS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    reward_items: _containers.RepeatedCompositeFieldContainer[ExecuteReward]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., reward_items: _Optional[_Iterable[_Union[ExecuteReward, _Mapping]]] = ...) -> None: ...

class ReqCompleteVillageTask(_message.Message):
    __slots__ = ["task_id", "activity_id"]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    task_id: int
    activity_id: int
    def __init__(self, task_id: _Optional[int] = ..., activity_id: _Optional[int] = ...) -> None: ...

class ResCompleteVillageTask(_message.Message):
    __slots__ = ["error", "reward_items"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    REWARD_ITEMS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    reward_items: _containers.RepeatedCompositeFieldContainer[ExecuteReward]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., reward_items: _Optional[_Iterable[_Union[ExecuteReward, _Mapping]]] = ...) -> None: ...

class ReqGetFriendVillageData(_message.Message):
    __slots__ = ["account_list", "activity_id"]
    ACCOUNT_LIST_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    account_list: _containers.RepeatedScalarFieldContainer[int]
    activity_id: int
    def __init__(self, account_list: _Optional[_Iterable[int]] = ..., activity_id: _Optional[int] = ...) -> None: ...

class ResGetFriendVillageData(_message.Message):
    __slots__ = ["error", "list"]
    class FriendVillageData(_message.Message):
        __slots__ = ["account_id", "level"]
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        LEVEL_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        level: int
        def __init__(self, account_id: _Optional[int] = ..., level: _Optional[int] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    LIST_FIELD_NUMBER: _ClassVar[int]
    error: Error
    list: _containers.RepeatedCompositeFieldContainer[ResGetFriendVillageData.FriendVillageData]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., list: _Optional[_Iterable[_Union[ResGetFriendVillageData.FriendVillageData, _Mapping]]] = ...) -> None: ...

class ReqSetVillageWorker(_message.Message):
    __slots__ = ["building_id", "worker_pos", "activity_id"]
    BUILDING_ID_FIELD_NUMBER: _ClassVar[int]
    WORKER_POS_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    building_id: int
    worker_pos: int
    activity_id: int
    def __init__(self, building_id: _Optional[int] = ..., worker_pos: _Optional[int] = ..., activity_id: _Optional[int] = ...) -> None: ...

class ResSetVillageWorker(_message.Message):
    __slots__ = ["error", "building", "update_time"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    BUILDING_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    error: Error
    building: VillageBuildingData
    update_time: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., building: _Optional[_Union[VillageBuildingData, _Mapping]] = ..., update_time: _Optional[int] = ...) -> None: ...

class ReqNextRoundVillage(_message.Message):
    __slots__ = ["activity_id"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ResNextRoundVillage(_message.Message):
    __slots__ = ["error", "activity_data"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_DATA_FIELD_NUMBER: _ClassVar[int]
    error: Error
    activity_data: ActivityVillageData
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., activity_data: _Optional[_Union[ActivityVillageData, _Mapping]] = ...) -> None: ...

class ReqResolveFestivalActivityProposal(_message.Message):
    __slots__ = ["activity_id", "id", "select"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    SELECT_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    id: int
    select: int
    def __init__(self, activity_id: _Optional[int] = ..., id: _Optional[int] = ..., select: _Optional[int] = ...) -> None: ...

class ResResolveFestivalActivityProposal(_message.Message):
    __slots__ = ["error", "effected_buff", "result", "reward_items", "level"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    EFFECTED_BUFF_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    REWARD_ITEMS_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    error: Error
    effected_buff: _containers.RepeatedScalarFieldContainer[int]
    result: int
    reward_items: _containers.RepeatedCompositeFieldContainer[ExecuteResult]
    level: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., effected_buff: _Optional[_Iterable[int]] = ..., result: _Optional[int] = ..., reward_items: _Optional[_Iterable[_Union[ExecuteResult, _Mapping]]] = ..., level: _Optional[int] = ...) -> None: ...

class ReqResolveFestivalActivityEvent(_message.Message):
    __slots__ = ["activity_id", "id", "select"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    SELECT_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    id: int
    select: int
    def __init__(self, activity_id: _Optional[int] = ..., id: _Optional[int] = ..., select: _Optional[int] = ...) -> None: ...

class ResResolveFestivalActivityEvent(_message.Message):
    __slots__ = ["error", "effected_buff", "reward_items", "ending_id", "level"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    EFFECTED_BUFF_FIELD_NUMBER: _ClassVar[int]
    REWARD_ITEMS_FIELD_NUMBER: _ClassVar[int]
    ENDING_ID_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    error: Error
    effected_buff: _containers.RepeatedScalarFieldContainer[int]
    reward_items: _containers.RepeatedCompositeFieldContainer[ExecuteResult]
    ending_id: int
    level: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., effected_buff: _Optional[_Iterable[int]] = ..., reward_items: _Optional[_Iterable[_Union[ExecuteResult, _Mapping]]] = ..., ending_id: _Optional[int] = ..., level: _Optional[int] = ...) -> None: ...

class ReqBuyFestivalProposal(_message.Message):
    __slots__ = ["activity_id"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ResBuyFestivalProposal(_message.Message):
    __slots__ = ["error", "new_proposal"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    NEW_PROPOSAL_FIELD_NUMBER: _ClassVar[int]
    error: Error
    new_proposal: FestivalProposalData
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., new_proposal: _Optional[_Union[FestivalProposalData, _Mapping]] = ...) -> None: ...

class ReqIslandActivityMove(_message.Message):
    __slots__ = ["activity_id", "zone_id"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    ZONE_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    zone_id: int
    def __init__(self, activity_id: _Optional[int] = ..., zone_id: _Optional[int] = ...) -> None: ...

class ReqIslandActivityBuy(_message.Message):
    __slots__ = ["activity_id", "items"]
    class BuyItems(_message.Message):
        __slots__ = ["goods_id", "pos", "rotate", "bag_id", "price"]
        GOODS_ID_FIELD_NUMBER: _ClassVar[int]
        POS_FIELD_NUMBER: _ClassVar[int]
        ROTATE_FIELD_NUMBER: _ClassVar[int]
        BAG_ID_FIELD_NUMBER: _ClassVar[int]
        PRICE_FIELD_NUMBER: _ClassVar[int]
        goods_id: int
        pos: _containers.RepeatedScalarFieldContainer[int]
        rotate: int
        bag_id: int
        price: int
        def __init__(self, goods_id: _Optional[int] = ..., pos: _Optional[_Iterable[int]] = ..., rotate: _Optional[int] = ..., bag_id: _Optional[int] = ..., price: _Optional[int] = ...) -> None: ...
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    items: _containers.RepeatedCompositeFieldContainer[ReqIslandActivityBuy.BuyItems]
    def __init__(self, activity_id: _Optional[int] = ..., items: _Optional[_Iterable[_Union[ReqIslandActivityBuy.BuyItems, _Mapping]]] = ...) -> None: ...

class ReqIslandActivitySell(_message.Message):
    __slots__ = ["activity_id", "items"]
    class SellItem(_message.Message):
        __slots__ = ["bag_id", "id", "price"]
        BAG_ID_FIELD_NUMBER: _ClassVar[int]
        ID_FIELD_NUMBER: _ClassVar[int]
        PRICE_FIELD_NUMBER: _ClassVar[int]
        bag_id: int
        id: int
        price: int
        def __init__(self, bag_id: _Optional[int] = ..., id: _Optional[int] = ..., price: _Optional[int] = ...) -> None: ...
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    items: _containers.RepeatedCompositeFieldContainer[ReqIslandActivitySell.SellItem]
    def __init__(self, activity_id: _Optional[int] = ..., items: _Optional[_Iterable[_Union[ReqIslandActivitySell.SellItem, _Mapping]]] = ...) -> None: ...

class ReqIslandActivityTidyBag(_message.Message):
    __slots__ = ["activity_id", "bag_data"]
    class BagData(_message.Message):
        __slots__ = ["bag_id", "items", "drops"]
        class ITemData(_message.Message):
            __slots__ = ["id", "pos", "rotate"]
            ID_FIELD_NUMBER: _ClassVar[int]
            POS_FIELD_NUMBER: _ClassVar[int]
            ROTATE_FIELD_NUMBER: _ClassVar[int]
            id: int
            pos: _containers.RepeatedScalarFieldContainer[int]
            rotate: int
            def __init__(self, id: _Optional[int] = ..., pos: _Optional[_Iterable[int]] = ..., rotate: _Optional[int] = ...) -> None: ...
        BAG_ID_FIELD_NUMBER: _ClassVar[int]
        ITEMS_FIELD_NUMBER: _ClassVar[int]
        DROPS_FIELD_NUMBER: _ClassVar[int]
        bag_id: int
        items: _containers.RepeatedCompositeFieldContainer[ReqIslandActivityTidyBag.BagData.ITemData]
        drops: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, bag_id: _Optional[int] = ..., items: _Optional[_Iterable[_Union[ReqIslandActivityTidyBag.BagData.ITemData, _Mapping]]] = ..., drops: _Optional[_Iterable[int]] = ...) -> None: ...
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    BAG_DATA_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    bag_data: _containers.RepeatedCompositeFieldContainer[ReqIslandActivityTidyBag.BagData]
    def __init__(self, activity_id: _Optional[int] = ..., bag_data: _Optional[_Iterable[_Union[ReqIslandActivityTidyBag.BagData, _Mapping]]] = ...) -> None: ...

class ReqIslandActivityUnlockBagGrid(_message.Message):
    __slots__ = ["activity_id", "bag_id", "pos"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    BAG_ID_FIELD_NUMBER: _ClassVar[int]
    POS_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    bag_id: int
    pos: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, activity_id: _Optional[int] = ..., bag_id: _Optional[int] = ..., pos: _Optional[_Iterable[int]] = ...) -> None: ...

class ContestSetting(_message.Message):
    __slots__ = ["level_limit", "game_limit", "system_broadcast"]
    class LevelLimit(_message.Message):
        __slots__ = ["type", "value"]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        type: int
        value: int
        def __init__(self, type: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    LEVEL_LIMIT_FIELD_NUMBER: _ClassVar[int]
    GAME_LIMIT_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_BROADCAST_FIELD_NUMBER: _ClassVar[int]
    level_limit: _containers.RepeatedCompositeFieldContainer[ContestSetting.LevelLimit]
    game_limit: int
    system_broadcast: int
    def __init__(self, level_limit: _Optional[_Iterable[_Union[ContestSetting.LevelLimit, _Mapping]]] = ..., game_limit: _Optional[int] = ..., system_broadcast: _Optional[int] = ...) -> None: ...

class ReqCreateCustomizedContest(_message.Message):
    __slots__ = ["name", "open_show", "game_rule_setting", "start_time", "end_time", "auto_match", "rank_rule", "contest_setting"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    OPEN_SHOW_FIELD_NUMBER: _ClassVar[int]
    GAME_RULE_SETTING_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    AUTO_MATCH_FIELD_NUMBER: _ClassVar[int]
    RANK_RULE_FIELD_NUMBER: _ClassVar[int]
    CONTEST_SETTING_FIELD_NUMBER: _ClassVar[int]
    name: str
    open_show: int
    game_rule_setting: GameMode
    start_time: int
    end_time: int
    auto_match: int
    rank_rule: int
    contest_setting: ContestSetting
    def __init__(self, name: _Optional[str] = ..., open_show: _Optional[int] = ..., game_rule_setting: _Optional[_Union[GameMode, _Mapping]] = ..., start_time: _Optional[int] = ..., end_time: _Optional[int] = ..., auto_match: _Optional[int] = ..., rank_rule: _Optional[int] = ..., contest_setting: _Optional[_Union[ContestSetting, _Mapping]] = ...) -> None: ...

class ResCreateCustomizedContest(_message.Message):
    __slots__ = ["error", "unique_id"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    unique_id: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., unique_id: _Optional[int] = ...) -> None: ...

class ReqFetchmanagerCustomizedContestList(_message.Message):
    __slots__ = ["lang"]
    LANG_FIELD_NUMBER: _ClassVar[int]
    lang: str
    def __init__(self, lang: _Optional[str] = ...) -> None: ...

class ResFetchManagerCustomizedContestList(_message.Message):
    __slots__ = ["error", "contests"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    CONTESTS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    contests: _containers.RepeatedCompositeFieldContainer[CustomizedContestBase]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., contests: _Optional[_Iterable[_Union[CustomizedContestBase, _Mapping]]] = ...) -> None: ...

class ReqFetchManagerCustomizedContest(_message.Message):
    __slots__ = ["unique_id"]
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    unique_id: int
    def __init__(self, unique_id: _Optional[int] = ...) -> None: ...

class ResFetchManagerCustomizedContest(_message.Message):
    __slots__ = ["error", "name", "open_show", "game_rule_setting", "start_time", "end_time", "auto_match", "rank_rule", "check_state", "checking_name", "contest_setting"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    OPEN_SHOW_FIELD_NUMBER: _ClassVar[int]
    GAME_RULE_SETTING_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    AUTO_MATCH_FIELD_NUMBER: _ClassVar[int]
    RANK_RULE_FIELD_NUMBER: _ClassVar[int]
    CHECK_STATE_FIELD_NUMBER: _ClassVar[int]
    CHECKING_NAME_FIELD_NUMBER: _ClassVar[int]
    CONTEST_SETTING_FIELD_NUMBER: _ClassVar[int]
    error: Error
    name: str
    open_show: int
    game_rule_setting: GameMode
    start_time: int
    end_time: int
    auto_match: int
    rank_rule: int
    check_state: int
    checking_name: str
    contest_setting: ContestSetting
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., name: _Optional[str] = ..., open_show: _Optional[int] = ..., game_rule_setting: _Optional[_Union[GameMode, _Mapping]] = ..., start_time: _Optional[int] = ..., end_time: _Optional[int] = ..., auto_match: _Optional[int] = ..., rank_rule: _Optional[int] = ..., check_state: _Optional[int] = ..., checking_name: _Optional[str] = ..., contest_setting: _Optional[_Union[ContestSetting, _Mapping]] = ...) -> None: ...

class ReqUpdateManagerCustomizedContest(_message.Message):
    __slots__ = ["name", "open_show", "game_rule_setting", "start_time", "end_time", "unique_id", "auto_match", "rank_rule", "contest_setting"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    OPEN_SHOW_FIELD_NUMBER: _ClassVar[int]
    GAME_RULE_SETTING_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    AUTO_MATCH_FIELD_NUMBER: _ClassVar[int]
    RANK_RULE_FIELD_NUMBER: _ClassVar[int]
    CONTEST_SETTING_FIELD_NUMBER: _ClassVar[int]
    name: str
    open_show: int
    game_rule_setting: GameMode
    start_time: int
    end_time: int
    unique_id: int
    auto_match: int
    rank_rule: int
    contest_setting: ContestSetting
    def __init__(self, name: _Optional[str] = ..., open_show: _Optional[int] = ..., game_rule_setting: _Optional[_Union[GameMode, _Mapping]] = ..., start_time: _Optional[int] = ..., end_time: _Optional[int] = ..., unique_id: _Optional[int] = ..., auto_match: _Optional[int] = ..., rank_rule: _Optional[int] = ..., contest_setting: _Optional[_Union[ContestSetting, _Mapping]] = ...) -> None: ...

class ReqFetchContestPlayerRank(_message.Message):
    __slots__ = ["unique_id", "limit", "offset"]
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    unique_id: int
    limit: int
    offset: int
    def __init__(self, unique_id: _Optional[int] = ..., limit: _Optional[int] = ..., offset: _Optional[int] = ...) -> None: ...

class ResFetchContestPlayerRank(_message.Message):
    __slots__ = ["error", "total", "rank", "player_data"]
    class ContestPlayerAccountData(_message.Message):
        __slots__ = ["total_game_count", "recent_games", "highest_series_points"]
        class ContestGameResult(_message.Message):
            __slots__ = ["rank", "total_point"]
            RANK_FIELD_NUMBER: _ClassVar[int]
            TOTAL_POINT_FIELD_NUMBER: _ClassVar[int]
            rank: int
            total_point: int
            def __init__(self, rank: _Optional[int] = ..., total_point: _Optional[int] = ...) -> None: ...
        class ContestSeriesGameResult(_message.Message):
            __slots__ = ["key", "results"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            RESULTS_FIELD_NUMBER: _ClassVar[int]
            key: int
            results: _containers.RepeatedCompositeFieldContainer[ResFetchContestPlayerRank.ContestPlayerAccountData.ContestGameResult]
            def __init__(self, key: _Optional[int] = ..., results: _Optional[_Iterable[_Union[ResFetchContestPlayerRank.ContestPlayerAccountData.ContestGameResult, _Mapping]]] = ...) -> None: ...
        TOTAL_GAME_COUNT_FIELD_NUMBER: _ClassVar[int]
        RECENT_GAMES_FIELD_NUMBER: _ClassVar[int]
        HIGHEST_SERIES_POINTS_FIELD_NUMBER: _ClassVar[int]
        total_game_count: int
        recent_games: _containers.RepeatedCompositeFieldContainer[ResFetchContestPlayerRank.ContestPlayerAccountData.ContestGameResult]
        highest_series_points: _containers.RepeatedCompositeFieldContainer[ResFetchContestPlayerRank.ContestPlayerAccountData.ContestSeriesGameResult]
        def __init__(self, total_game_count: _Optional[int] = ..., recent_games: _Optional[_Iterable[_Union[ResFetchContestPlayerRank.ContestPlayerAccountData.ContestGameResult, _Mapping]]] = ..., highest_series_points: _Optional[_Iterable[_Union[ResFetchContestPlayerRank.ContestPlayerAccountData.ContestSeriesGameResult, _Mapping]]] = ...) -> None: ...
    class SeasonRank(_message.Message):
        __slots__ = ["account_id", "nickname", "data"]
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        NICKNAME_FIELD_NUMBER: _ClassVar[int]
        DATA_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        nickname: str
        data: ResFetchContestPlayerRank.ContestPlayerAccountData
        def __init__(self, account_id: _Optional[int] = ..., nickname: _Optional[str] = ..., data: _Optional[_Union[ResFetchContestPlayerRank.ContestPlayerAccountData, _Mapping]] = ...) -> None: ...
    class PlayerData(_message.Message):
        __slots__ = ["rank", "data"]
        RANK_FIELD_NUMBER: _ClassVar[int]
        DATA_FIELD_NUMBER: _ClassVar[int]
        rank: int
        data: ResFetchContestPlayerRank.ContestPlayerAccountData
        def __init__(self, rank: _Optional[int] = ..., data: _Optional[_Union[ResFetchContestPlayerRank.ContestPlayerAccountData, _Mapping]] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    RANK_FIELD_NUMBER: _ClassVar[int]
    PLAYER_DATA_FIELD_NUMBER: _ClassVar[int]
    error: Error
    total: int
    rank: _containers.RepeatedCompositeFieldContainer[ResFetchContestPlayerRank.SeasonRank]
    player_data: ResFetchContestPlayerRank.PlayerData
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., total: _Optional[int] = ..., rank: _Optional[_Iterable[_Union[ResFetchContestPlayerRank.SeasonRank, _Mapping]]] = ..., player_data: _Optional[_Union[ResFetchContestPlayerRank.PlayerData, _Mapping]] = ...) -> None: ...

class ReqFetchReadyPlayerList(_message.Message):
    __slots__ = ["unique_id"]
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    unique_id: int
    def __init__(self, unique_id: _Optional[int] = ...) -> None: ...

class ResFetchReadyPlayerList(_message.Message):
    __slots__ = ["error", "list"]
    class Player(_message.Message):
        __slots__ = ["account_id", "nickname"]
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        NICKNAME_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        nickname: str
        def __init__(self, account_id: _Optional[int] = ..., nickname: _Optional[str] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    LIST_FIELD_NUMBER: _ClassVar[int]
    error: Error
    list: _containers.RepeatedCompositeFieldContainer[ResFetchReadyPlayerList.Player]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., list: _Optional[_Iterable[_Union[ResFetchReadyPlayerList.Player, _Mapping]]] = ...) -> None: ...

class ReqCreateGamePlan(_message.Message):
    __slots__ = ["unique_id", "account_list", "game_start_time", "shuffle_seats", "ai_level"]
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_LIST_FIELD_NUMBER: _ClassVar[int]
    GAME_START_TIME_FIELD_NUMBER: _ClassVar[int]
    SHUFFLE_SEATS_FIELD_NUMBER: _ClassVar[int]
    AI_LEVEL_FIELD_NUMBER: _ClassVar[int]
    unique_id: int
    account_list: _containers.RepeatedScalarFieldContainer[int]
    game_start_time: int
    shuffle_seats: int
    ai_level: int
    def __init__(self, unique_id: _Optional[int] = ..., account_list: _Optional[_Iterable[int]] = ..., game_start_time: _Optional[int] = ..., shuffle_seats: _Optional[int] = ..., ai_level: _Optional[int] = ...) -> None: ...

class ResGenerateContestManagerLoginCode(_message.Message):
    __slots__ = ["error", "code"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    error: Error
    code: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., code: _Optional[str] = ...) -> None: ...

class ReqAmuletActivityStartGame(_message.Message):
    __slots__ = ["activity_id"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ResAmuletActivityStartGame(_message.Message):
    __slots__ = ["error", "game"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    GAME_FIELD_NUMBER: _ClassVar[int]
    error: Error
    game: AmuletGameData
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., game: _Optional[_Union[AmuletGameData, _Mapping]] = ...) -> None: ...

class ReqAmuletActivityOperate(_message.Message):
    __slots__ = ["activity_id", "type", "tile"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TILE_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    type: int
    tile: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, activity_id: _Optional[int] = ..., type: _Optional[int] = ..., tile: _Optional[_Iterable[int]] = ...) -> None: ...

class ResAmuletActivityOperate(_message.Message):
    __slots__ = ["error", "hu_result", "gang_result", "deal_result", "upgrade_result", "upgraded", "failed", "game_update"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    HU_RESULT_FIELD_NUMBER: _ClassVar[int]
    GANG_RESULT_FIELD_NUMBER: _ClassVar[int]
    DEAL_RESULT_FIELD_NUMBER: _ClassVar[int]
    UPGRADE_RESULT_FIELD_NUMBER: _ClassVar[int]
    UPGRADED_FIELD_NUMBER: _ClassVar[int]
    FAILED_FIELD_NUMBER: _ClassVar[int]
    GAME_UPDATE_FIELD_NUMBER: _ClassVar[int]
    error: Error
    hu_result: AmuletHuleOperateResult
    gang_result: AmuletGangOperateResult
    deal_result: AmuletDealTileResult
    upgrade_result: AmuletUpgradeResult
    upgraded: bool
    failed: bool
    game_update: AmuletGameUpdateData
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., hu_result: _Optional[_Union[AmuletHuleOperateResult, _Mapping]] = ..., gang_result: _Optional[_Union[AmuletGangOperateResult, _Mapping]] = ..., deal_result: _Optional[_Union[AmuletDealTileResult, _Mapping]] = ..., upgrade_result: _Optional[_Union[AmuletUpgradeResult, _Mapping]] = ..., upgraded: bool = ..., failed: bool = ..., game_update: _Optional[_Union[AmuletGameUpdateData, _Mapping]] = ...) -> None: ...

class ReqAmuletActivityChangeHands(_message.Message):
    __slots__ = ["activity_id", "hands"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    HANDS_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    hands: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, activity_id: _Optional[int] = ..., hands: _Optional[_Iterable[int]] = ...) -> None: ...

class ResAmuletActivityChangeHands(_message.Message):
    __slots__ = ["error", "hands", "remain_change_tile_count", "ting_list", "effect_list"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    HANDS_FIELD_NUMBER: _ClassVar[int]
    REMAIN_CHANGE_TILE_COUNT_FIELD_NUMBER: _ClassVar[int]
    TING_LIST_FIELD_NUMBER: _ClassVar[int]
    EFFECT_LIST_FIELD_NUMBER: _ClassVar[int]
    error: Error
    hands: _containers.RepeatedScalarFieldContainer[int]
    remain_change_tile_count: int
    ting_list: _containers.RepeatedCompositeFieldContainer[AmuletActivityTingInfo]
    effect_list: _containers.RepeatedCompositeFieldContainer[AmuletEffectData]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., hands: _Optional[_Iterable[int]] = ..., remain_change_tile_count: _Optional[int] = ..., ting_list: _Optional[_Iterable[_Union[AmuletActivityTingInfo, _Mapping]]] = ..., effect_list: _Optional[_Iterable[_Union[AmuletEffectData, _Mapping]]] = ...) -> None: ...

class ReqAmuletActivityUpgrade(_message.Message):
    __slots__ = ["activity_id"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ResAmuletActivityUpgrade(_message.Message):
    __slots__ = ["error", "game", "hook_effect"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    GAME_FIELD_NUMBER: _ClassVar[int]
    HOOK_EFFECT_FIELD_NUMBER: _ClassVar[int]
    error: Error
    game: AmuletGameData
    hook_effect: _containers.RepeatedCompositeFieldContainer[AmuletActivityHookEffect]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., game: _Optional[_Union[AmuletGameData, _Mapping]] = ..., hook_effect: _Optional[_Iterable[_Union[AmuletActivityHookEffect, _Mapping]]] = ...) -> None: ...

class ReqAmuletActivitySelectPack(_message.Message):
    __slots__ = ["activity_id", "id"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    id: int
    def __init__(self, activity_id: _Optional[int] = ..., id: _Optional[int] = ...) -> None: ...

class ResAmuletActivitySelectPack(_message.Message):
    __slots__ = ["error", "effect_list", "shop"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    EFFECT_LIST_FIELD_NUMBER: _ClassVar[int]
    SHOP_FIELD_NUMBER: _ClassVar[int]
    error: Error
    effect_list: _containers.RepeatedCompositeFieldContainer[AmuletEffectData]
    shop: AmuletGameShopData
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., effect_list: _Optional[_Iterable[_Union[AmuletEffectData, _Mapping]]] = ..., shop: _Optional[_Union[AmuletGameShopData, _Mapping]] = ...) -> None: ...

class ReqAmuletActivityBuy(_message.Message):
    __slots__ = ["activity_id", "id"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    id: int
    def __init__(self, activity_id: _Optional[int] = ..., id: _Optional[int] = ...) -> None: ...

class ResAmuletActivityBuy(_message.Message):
    __slots__ = ["error", "coin", "shop", "stage", "effect_list", "total_consumed_coin"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    COIN_FIELD_NUMBER: _ClassVar[int]
    SHOP_FIELD_NUMBER: _ClassVar[int]
    STAGE_FIELD_NUMBER: _ClassVar[int]
    EFFECT_LIST_FIELD_NUMBER: _ClassVar[int]
    TOTAL_CONSUMED_COIN_FIELD_NUMBER: _ClassVar[int]
    error: Error
    coin: int
    shop: AmuletGameShopData
    stage: int
    effect_list: _containers.RepeatedCompositeFieldContainer[AmuletEffectData]
    total_consumed_coin: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., coin: _Optional[int] = ..., shop: _Optional[_Union[AmuletGameShopData, _Mapping]] = ..., stage: _Optional[int] = ..., effect_list: _Optional[_Iterable[_Union[AmuletEffectData, _Mapping]]] = ..., total_consumed_coin: _Optional[int] = ...) -> None: ...

class ReqAmuletActivitySellEffect(_message.Message):
    __slots__ = ["activity_id", "id"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    id: int
    def __init__(self, activity_id: _Optional[int] = ..., id: _Optional[int] = ...) -> None: ...

class ResAmuletActivitySellEffect(_message.Message):
    __slots__ = ["error", "coin", "effect_list", "game_update", "remain_change_tile_count"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    COIN_FIELD_NUMBER: _ClassVar[int]
    EFFECT_LIST_FIELD_NUMBER: _ClassVar[int]
    GAME_UPDATE_FIELD_NUMBER: _ClassVar[int]
    REMAIN_CHANGE_TILE_COUNT_FIELD_NUMBER: _ClassVar[int]
    error: Error
    coin: int
    effect_list: _containers.RepeatedCompositeFieldContainer[AmuletEffectData]
    game_update: AmuletGameUpdateData
    remain_change_tile_count: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., coin: _Optional[int] = ..., effect_list: _Optional[_Iterable[_Union[AmuletEffectData, _Mapping]]] = ..., game_update: _Optional[_Union[AmuletGameUpdateData, _Mapping]] = ..., remain_change_tile_count: _Optional[int] = ...) -> None: ...

class ReqAmuletActivityEffectSort(_message.Message):
    __slots__ = ["activity_id", "sorted_id"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    SORTED_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    sorted_id: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, activity_id: _Optional[int] = ..., sorted_id: _Optional[_Iterable[int]] = ...) -> None: ...

class ReqAmuletActivityGiveup(_message.Message):
    __slots__ = ["activity_id"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ReqAmuletActivityRefreshShop(_message.Message):
    __slots__ = ["activity_id"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ResAmuletActivityRefreshShop(_message.Message):
    __slots__ = ["error", "shop", "coin", "effect_list"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    SHOP_FIELD_NUMBER: _ClassVar[int]
    COIN_FIELD_NUMBER: _ClassVar[int]
    EFFECT_LIST_FIELD_NUMBER: _ClassVar[int]
    error: Error
    shop: AmuletGameShopData
    coin: int
    effect_list: _containers.RepeatedCompositeFieldContainer[AmuletEffectData]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., shop: _Optional[_Union[AmuletGameShopData, _Mapping]] = ..., coin: _Optional[int] = ..., effect_list: _Optional[_Iterable[_Union[AmuletEffectData, _Mapping]]] = ...) -> None: ...

class ReqAmuletActivitySelectFreeEffect(_message.Message):
    __slots__ = ["activity_id", "selected_id"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    SELECTED_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    selected_id: int
    def __init__(self, activity_id: _Optional[int] = ..., selected_id: _Optional[int] = ...) -> None: ...

class ResAmuletActivitySelectFreeEffect(_message.Message):
    __slots__ = ["error", "game_update", "remain_change_tile_count"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    GAME_UPDATE_FIELD_NUMBER: _ClassVar[int]
    REMAIN_CHANGE_TILE_COUNT_FIELD_NUMBER: _ClassVar[int]
    error: Error
    game_update: AmuletGameUpdateData
    remain_change_tile_count: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., game_update: _Optional[_Union[AmuletGameUpdateData, _Mapping]] = ..., remain_change_tile_count: _Optional[int] = ...) -> None: ...

class ReqAmuletActivityUpgradeShopBuff(_message.Message):
    __slots__ = ["activity_id", "id"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    id: int
    def __init__(self, activity_id: _Optional[int] = ..., id: _Optional[int] = ...) -> None: ...

class ResAmuletActivityUpgradeShopBuff(_message.Message):
    __slots__ = ["error", "game_update", "shop_buff_list", "total_consumed_coin"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    GAME_UPDATE_FIELD_NUMBER: _ClassVar[int]
    SHOP_BUFF_LIST_FIELD_NUMBER: _ClassVar[int]
    TOTAL_CONSUMED_COIN_FIELD_NUMBER: _ClassVar[int]
    error: Error
    game_update: AmuletGameUpdateData
    shop_buff_list: _containers.RepeatedCompositeFieldContainer[AmuletEffectData]
    total_consumed_coin: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., game_update: _Optional[_Union[AmuletGameUpdateData, _Mapping]] = ..., shop_buff_list: _Optional[_Iterable[_Union[AmuletEffectData, _Mapping]]] = ..., total_consumed_coin: _Optional[int] = ...) -> None: ...

class ReqAmuletActivityEndShopping(_message.Message):
    __slots__ = ["activity_id"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ResAmuletActivityEndShopping(_message.Message):
    __slots__ = ["error", "game_update"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    GAME_UPDATE_FIELD_NUMBER: _ClassVar[int]
    error: Error
    game_update: AmuletGameUpdateData
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., game_update: _Optional[_Union[AmuletGameUpdateData, _Mapping]] = ...) -> None: ...

class ReqAmuletActivitySetSkillLevel(_message.Message):
    __slots__ = ["activity_id", "skill"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    SKILL_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    skill: _containers.RepeatedCompositeFieldContainer[AmuletSkillData]
    def __init__(self, activity_id: _Optional[int] = ..., skill: _Optional[_Iterable[_Union[AmuletSkillData, _Mapping]]] = ...) -> None: ...

class ResAmuletActivityMaintainInfo(_message.Message):
    __slots__ = ["error", "mode"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    error: Error
    mode: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., mode: _Optional[str] = ...) -> None: ...

class ReqStoryActivityUnlock(_message.Message):
    __slots__ = ["activity_id", "story_id"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    STORY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    story_id: int
    def __init__(self, activity_id: _Optional[int] = ..., story_id: _Optional[int] = ...) -> None: ...

class ReqStoryActivityUnlockEnding(_message.Message):
    __slots__ = ["activity_id", "story_id", "ending_id"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    STORY_ID_FIELD_NUMBER: _ClassVar[int]
    ENDING_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    story_id: int
    ending_id: int
    def __init__(self, activity_id: _Optional[int] = ..., story_id: _Optional[int] = ..., ending_id: _Optional[int] = ...) -> None: ...

class ReqStoryActivityReceiveEndingReward(_message.Message):
    __slots__ = ["activity_id", "story_id", "ending_id"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    STORY_ID_FIELD_NUMBER: _ClassVar[int]
    ENDING_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    story_id: int
    ending_id: int
    def __init__(self, activity_id: _Optional[int] = ..., story_id: _Optional[int] = ..., ending_id: _Optional[int] = ...) -> None: ...

class ResStoryReward(_message.Message):
    __slots__ = ["error", "reward_items"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    REWARD_ITEMS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    reward_items: _containers.RepeatedCompositeFieldContainer[ExecuteReward]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., reward_items: _Optional[_Iterable[_Union[ExecuteReward, _Mapping]]] = ...) -> None: ...

class ReqStoryActivityReceiveFinishReward(_message.Message):
    __slots__ = ["activity_id", "story_id"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    STORY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    story_id: int
    def __init__(self, activity_id: _Optional[int] = ..., story_id: _Optional[int] = ...) -> None: ...

class ReqStoryActivityReceiveAllFinishReward(_message.Message):
    __slots__ = ["activity_id", "story_id"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    STORY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    story_id: int
    def __init__(self, activity_id: _Optional[int] = ..., story_id: _Optional[int] = ...) -> None: ...

class ReqStoryActivityUnlockEndingAndReceive(_message.Message):
    __slots__ = ["activity_id", "story_id", "ending_id"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    STORY_ID_FIELD_NUMBER: _ClassVar[int]
    ENDING_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    story_id: int
    ending_id: int
    def __init__(self, activity_id: _Optional[int] = ..., story_id: _Optional[int] = ..., ending_id: _Optional[int] = ...) -> None: ...

class ResStoryActivityUnlockEndingAndReceive(_message.Message):
    __slots__ = ["error", "ending_reward", "finish_reward", "all_finish_reward"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ENDING_REWARD_FIELD_NUMBER: _ClassVar[int]
    FINISH_REWARD_FIELD_NUMBER: _ClassVar[int]
    ALL_FINISH_REWARD_FIELD_NUMBER: _ClassVar[int]
    error: Error
    ending_reward: _containers.RepeatedCompositeFieldContainer[ExecuteReward]
    finish_reward: _containers.RepeatedCompositeFieldContainer[ExecuteReward]
    all_finish_reward: _containers.RepeatedCompositeFieldContainer[ExecuteReward]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., ending_reward: _Optional[_Iterable[_Union[ExecuteReward, _Mapping]]] = ..., finish_reward: _Optional[_Iterable[_Union[ExecuteReward, _Mapping]]] = ..., all_finish_reward: _Optional[_Iterable[_Union[ExecuteReward, _Mapping]]] = ...) -> None: ...

class ReqFetchActivityRank(_message.Message):
    __slots__ = ["activity_id", "account_list"]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_LIST_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    account_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, activity_id: _Optional[int] = ..., account_list: _Optional[_Iterable[int]] = ...) -> None: ...

class ResFetchActivityRank(_message.Message):
    __slots__ = ["error", "items", "self"]
    class ActivityRankItem(_message.Message):
        __slots__ = ["account_id", "score", "data", "rank"]
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        SCORE_FIELD_NUMBER: _ClassVar[int]
        DATA_FIELD_NUMBER: _ClassVar[int]
        RANK_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        score: int
        data: str
        rank: int
        def __init__(self, account_id: _Optional[int] = ..., score: _Optional[int] = ..., data: _Optional[str] = ..., rank: _Optional[int] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    SELF_FIELD_NUMBER: _ClassVar[int]
    error: Error
    items: _containers.RepeatedCompositeFieldContainer[ResFetchActivityRank.ActivityRankItem]
    self: ResFetchActivityRank.ActivityRankItem
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., items: _Optional[_Iterable[_Union[ResFetchActivityRank.ActivityRankItem, _Mapping]]] = ..., self: _Optional[_Union[ResFetchActivityRank.ActivityRankItem, _Mapping]] = ...) -> None: ...

class ReqFetchQuestionnaireList(_message.Message):
    __slots__ = ["lang"]
    LANG_FIELD_NUMBER: _ClassVar[int]
    lang: str
    def __init__(self, lang: _Optional[str] = ...) -> None: ...

class ResFetchQuestionnaireList(_message.Message):
    __slots__ = ["error", "list", "finished_list"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    LIST_FIELD_NUMBER: _ClassVar[int]
    FINISHED_LIST_FIELD_NUMBER: _ClassVar[int]
    error: Error
    list: _containers.RepeatedCompositeFieldContainer[QuestionnaireBrief]
    finished_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., list: _Optional[_Iterable[_Union[QuestionnaireBrief, _Mapping]]] = ..., finished_list: _Optional[_Iterable[int]] = ...) -> None: ...

class ReqFetchQuestionnaireDetail(_message.Message):
    __slots__ = ["id", "lang"]
    ID_FIELD_NUMBER: _ClassVar[int]
    LANG_FIELD_NUMBER: _ClassVar[int]
    id: int
    lang: str
    def __init__(self, id: _Optional[int] = ..., lang: _Optional[str] = ...) -> None: ...

class ResFetchQuestionnaireDetail(_message.Message):
    __slots__ = ["error", "detail"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    DETAIL_FIELD_NUMBER: _ClassVar[int]
    error: Error
    detail: QuestionnaireDetail
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., detail: _Optional[_Union[QuestionnaireDetail, _Mapping]] = ...) -> None: ...

class ReqSetVerifiedHidden(_message.Message):
    __slots__ = ["verified_hidden"]
    VERIFIED_HIDDEN_FIELD_NUMBER: _ClassVar[int]
    verified_hidden: int
    def __init__(self, verified_hidden: _Optional[int] = ...) -> None: ...

class ReqSubmitQuestionnaire(_message.Message):
    __slots__ = ["questionnaire_id", "questionnaire_version_id", "answers", "open_time", "finish_time", "client"]
    class QuestionnaireAnswer(_message.Message):
        __slots__ = ["question_id", "values"]
        class QuestionnaireAnswerValue(_message.Message):
            __slots__ = ["value", "custom_input"]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            CUSTOM_INPUT_FIELD_NUMBER: _ClassVar[int]
            value: str
            custom_input: str
            def __init__(self, value: _Optional[str] = ..., custom_input: _Optional[str] = ...) -> None: ...
        QUESTION_ID_FIELD_NUMBER: _ClassVar[int]
        VALUES_FIELD_NUMBER: _ClassVar[int]
        question_id: int
        values: _containers.RepeatedCompositeFieldContainer[ReqSubmitQuestionnaire.QuestionnaireAnswer.QuestionnaireAnswerValue]
        def __init__(self, question_id: _Optional[int] = ..., values: _Optional[_Iterable[_Union[ReqSubmitQuestionnaire.QuestionnaireAnswer.QuestionnaireAnswerValue, _Mapping]]] = ...) -> None: ...
    QUESTIONNAIRE_ID_FIELD_NUMBER: _ClassVar[int]
    QUESTIONNAIRE_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    ANSWERS_FIELD_NUMBER: _ClassVar[int]
    OPEN_TIME_FIELD_NUMBER: _ClassVar[int]
    FINISH_TIME_FIELD_NUMBER: _ClassVar[int]
    CLIENT_FIELD_NUMBER: _ClassVar[int]
    questionnaire_id: int
    questionnaire_version_id: int
    answers: _containers.RepeatedCompositeFieldContainer[ReqSubmitQuestionnaire.QuestionnaireAnswer]
    open_time: int
    finish_time: int
    client: str
    def __init__(self, questionnaire_id: _Optional[int] = ..., questionnaire_version_id: _Optional[int] = ..., answers: _Optional[_Iterable[_Union[ReqSubmitQuestionnaire.QuestionnaireAnswer, _Mapping]]] = ..., open_time: _Optional[int] = ..., finish_time: _Optional[int] = ..., client: _Optional[str] = ...) -> None: ...

class ReqAuthGame(_message.Message):
    __slots__ = ["account_id", "token", "game_uuid", "session", "gift", "vs"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    GAME_UUID_FIELD_NUMBER: _ClassVar[int]
    SESSION_FIELD_NUMBER: _ClassVar[int]
    GIFT_FIELD_NUMBER: _ClassVar[int]
    VS_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    token: str
    game_uuid: str
    session: str
    gift: str
    vs: int
    def __init__(self, account_id: _Optional[int] = ..., token: _Optional[str] = ..., game_uuid: _Optional[str] = ..., session: _Optional[str] = ..., gift: _Optional[str] = ..., vs: _Optional[int] = ...) -> None: ...

class ResAuthGame(_message.Message):
    __slots__ = ["error", "players", "seat_list", "is_game_start", "game_config", "ready_id_list"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    SEAT_LIST_FIELD_NUMBER: _ClassVar[int]
    IS_GAME_START_FIELD_NUMBER: _ClassVar[int]
    GAME_CONFIG_FIELD_NUMBER: _ClassVar[int]
    READY_ID_LIST_FIELD_NUMBER: _ClassVar[int]
    error: Error
    players: _containers.RepeatedCompositeFieldContainer[PlayerGameView]
    seat_list: _containers.RepeatedScalarFieldContainer[int]
    is_game_start: bool
    game_config: GameConfig
    ready_id_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., players: _Optional[_Iterable[_Union[PlayerGameView, _Mapping]]] = ..., seat_list: _Optional[_Iterable[int]] = ..., is_game_start: bool = ..., game_config: _Optional[_Union[GameConfig, _Mapping]] = ..., ready_id_list: _Optional[_Iterable[int]] = ...) -> None: ...

class GameRestore(_message.Message):
    __slots__ = ["snapshot", "actions", "passed_waiting_time", "game_state", "start_time", "last_pause_time_ms"]
    SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    ACTIONS_FIELD_NUMBER: _ClassVar[int]
    PASSED_WAITING_TIME_FIELD_NUMBER: _ClassVar[int]
    GAME_STATE_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    LAST_PAUSE_TIME_MS_FIELD_NUMBER: _ClassVar[int]
    snapshot: GameSnapshot
    actions: _containers.RepeatedCompositeFieldContainer[ActionPrototype]
    passed_waiting_time: int
    game_state: int
    start_time: int
    last_pause_time_ms: int
    def __init__(self, snapshot: _Optional[_Union[GameSnapshot, _Mapping]] = ..., actions: _Optional[_Iterable[_Union[ActionPrototype, _Mapping]]] = ..., passed_waiting_time: _Optional[int] = ..., game_state: _Optional[int] = ..., start_time: _Optional[int] = ..., last_pause_time_ms: _Optional[int] = ...) -> None: ...

class ResEnterGame(_message.Message):
    __slots__ = ["error", "is_end", "step", "game_restore"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    IS_END_FIELD_NUMBER: _ClassVar[int]
    STEP_FIELD_NUMBER: _ClassVar[int]
    GAME_RESTORE_FIELD_NUMBER: _ClassVar[int]
    error: Error
    is_end: bool
    step: int
    game_restore: GameRestore
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., is_end: bool = ..., step: _Optional[int] = ..., game_restore: _Optional[_Union[GameRestore, _Mapping]] = ...) -> None: ...

class ReqSyncGame(_message.Message):
    __slots__ = ["round_id", "step"]
    ROUND_ID_FIELD_NUMBER: _ClassVar[int]
    STEP_FIELD_NUMBER: _ClassVar[int]
    round_id: str
    step: int
    def __init__(self, round_id: _Optional[str] = ..., step: _Optional[int] = ...) -> None: ...

class ResSyncGame(_message.Message):
    __slots__ = ["error", "is_end", "step", "game_restore"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    IS_END_FIELD_NUMBER: _ClassVar[int]
    STEP_FIELD_NUMBER: _ClassVar[int]
    GAME_RESTORE_FIELD_NUMBER: _ClassVar[int]
    error: Error
    is_end: bool
    step: int
    game_restore: GameRestore
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., is_end: bool = ..., step: _Optional[int] = ..., game_restore: _Optional[_Union[GameRestore, _Mapping]] = ...) -> None: ...

class ReqSelfOperation(_message.Message):
    __slots__ = ["type", "index", "tile", "cancel_operation", "moqie", "timeuse", "tile_state", "change_tiles", "tile_states", "gap_type"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    TILE_FIELD_NUMBER: _ClassVar[int]
    CANCEL_OPERATION_FIELD_NUMBER: _ClassVar[int]
    MOQIE_FIELD_NUMBER: _ClassVar[int]
    TIMEUSE_FIELD_NUMBER: _ClassVar[int]
    TILE_STATE_FIELD_NUMBER: _ClassVar[int]
    CHANGE_TILES_FIELD_NUMBER: _ClassVar[int]
    TILE_STATES_FIELD_NUMBER: _ClassVar[int]
    GAP_TYPE_FIELD_NUMBER: _ClassVar[int]
    type: int
    index: int
    tile: str
    cancel_operation: bool
    moqie: bool
    timeuse: int
    tile_state: int
    change_tiles: _containers.RepeatedScalarFieldContainer[str]
    tile_states: _containers.RepeatedScalarFieldContainer[int]
    gap_type: int
    def __init__(self, type: _Optional[int] = ..., index: _Optional[int] = ..., tile: _Optional[str] = ..., cancel_operation: bool = ..., moqie: bool = ..., timeuse: _Optional[int] = ..., tile_state: _Optional[int] = ..., change_tiles: _Optional[_Iterable[str]] = ..., tile_states: _Optional[_Iterable[int]] = ..., gap_type: _Optional[int] = ...) -> None: ...

class ReqChiPengGang(_message.Message):
    __slots__ = ["type", "index", "cancel_operation", "timeuse"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    CANCEL_OPERATION_FIELD_NUMBER: _ClassVar[int]
    TIMEUSE_FIELD_NUMBER: _ClassVar[int]
    type: int
    index: int
    cancel_operation: bool
    timeuse: int
    def __init__(self, type: _Optional[int] = ..., index: _Optional[int] = ..., cancel_operation: bool = ..., timeuse: _Optional[int] = ...) -> None: ...

class ReqBroadcastInGame(_message.Message):
    __slots__ = ["content", "except_self"]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    EXCEPT_SELF_FIELD_NUMBER: _ClassVar[int]
    content: str
    except_self: bool
    def __init__(self, content: _Optional[str] = ..., except_self: bool = ...) -> None: ...

class ReqGMCommandInGaming(_message.Message):
    __slots__ = ["json_data"]
    JSON_DATA_FIELD_NUMBER: _ClassVar[int]
    json_data: str
    def __init__(self, json_data: _Optional[str] = ...) -> None: ...

class ResGamePlayerState(_message.Message):
    __slots__ = ["error", "state_list"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    STATE_LIST_FIELD_NUMBER: _ClassVar[int]
    error: Error
    state_list: _containers.RepeatedScalarFieldContainer[GamePlayerState]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., state_list: _Optional[_Iterable[_Union[GamePlayerState, str]]] = ...) -> None: ...

class ReqVoteGameEnd(_message.Message):
    __slots__ = ["yes"]
    YES_FIELD_NUMBER: _ClassVar[int]
    yes: bool
    def __init__(self, yes: bool = ...) -> None: ...

class ResGameEndVote(_message.Message):
    __slots__ = ["success", "vote_cd_end_time", "error"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    VOTE_CD_END_TIME_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: bool
    vote_cd_end_time: int
    error: Error
    def __init__(self, success: bool = ..., vote_cd_end_time: _Optional[int] = ..., error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class ReqAuthObserve(_message.Message):
    __slots__ = ["token"]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: str
    def __init__(self, token: _Optional[str] = ...) -> None: ...

class ResStartObserve(_message.Message):
    __slots__ = ["head", "passed"]
    HEAD_FIELD_NUMBER: _ClassVar[int]
    PASSED_FIELD_NUMBER: _ClassVar[int]
    head: GameLiveHead
    passed: GameLiveSegment
    def __init__(self, head: _Optional[_Union[GameLiveHead, _Mapping]] = ..., passed: _Optional[_Union[GameLiveSegment, _Mapping]] = ...) -> None: ...

class NotifyNewGame(_message.Message):
    __slots__ = ["game_uuid", "player_list"]
    GAME_UUID_FIELD_NUMBER: _ClassVar[int]
    PLAYER_LIST_FIELD_NUMBER: _ClassVar[int]
    game_uuid: str
    player_list: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, game_uuid: _Optional[str] = ..., player_list: _Optional[_Iterable[str]] = ...) -> None: ...

class NotifyPlayerLoadGameReady(_message.Message):
    __slots__ = ["ready_id_list"]
    READY_ID_LIST_FIELD_NUMBER: _ClassVar[int]
    ready_id_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, ready_id_list: _Optional[_Iterable[int]] = ...) -> None: ...

class NotifyGameBroadcast(_message.Message):
    __slots__ = ["seat", "content"]
    SEAT_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    seat: int
    content: str
    def __init__(self, seat: _Optional[int] = ..., content: _Optional[str] = ...) -> None: ...

class NotifyGameEndResult(_message.Message):
    __slots__ = ["result"]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: GameEndResult
    def __init__(self, result: _Optional[_Union[GameEndResult, _Mapping]] = ...) -> None: ...

class NotifyGameTerminate(_message.Message):
    __slots__ = ["reason"]
    REASON_FIELD_NUMBER: _ClassVar[int]
    reason: str
    def __init__(self, reason: _Optional[str] = ...) -> None: ...

class NotifyPlayerConnectionState(_message.Message):
    __slots__ = ["seat", "state"]
    SEAT_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    seat: int
    state: GamePlayerState
    def __init__(self, seat: _Optional[int] = ..., state: _Optional[_Union[GamePlayerState, str]] = ...) -> None: ...

class NotifyAccountLevelChange(_message.Message):
    __slots__ = ["origin", "final", "type"]
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    FINAL_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    origin: AccountLevel
    final: AccountLevel
    type: int
    def __init__(self, origin: _Optional[_Union[AccountLevel, _Mapping]] = ..., final: _Optional[_Union[AccountLevel, _Mapping]] = ..., type: _Optional[int] = ...) -> None: ...

class NotifyGameFinishReward(_message.Message):
    __slots__ = ["mode_id", "level_change", "match_chest", "main_character", "character_gift"]
    class LevelChange(_message.Message):
        __slots__ = ["origin", "final", "type"]
        ORIGIN_FIELD_NUMBER: _ClassVar[int]
        FINAL_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        origin: AccountLevel
        final: AccountLevel
        type: int
        def __init__(self, origin: _Optional[_Union[AccountLevel, _Mapping]] = ..., final: _Optional[_Union[AccountLevel, _Mapping]] = ..., type: _Optional[int] = ...) -> None: ...
    class MatchChest(_message.Message):
        __slots__ = ["chest_id", "origin", "final", "is_graded", "rewards"]
        CHEST_ID_FIELD_NUMBER: _ClassVar[int]
        ORIGIN_FIELD_NUMBER: _ClassVar[int]
        FINAL_FIELD_NUMBER: _ClassVar[int]
        IS_GRADED_FIELD_NUMBER: _ClassVar[int]
        REWARDS_FIELD_NUMBER: _ClassVar[int]
        chest_id: int
        origin: int
        final: int
        is_graded: bool
        rewards: _containers.RepeatedCompositeFieldContainer[RewardSlot]
        def __init__(self, chest_id: _Optional[int] = ..., origin: _Optional[int] = ..., final: _Optional[int] = ..., is_graded: bool = ..., rewards: _Optional[_Iterable[_Union[RewardSlot, _Mapping]]] = ...) -> None: ...
    class MainCharacter(_message.Message):
        __slots__ = ["level", "exp", "add"]
        LEVEL_FIELD_NUMBER: _ClassVar[int]
        EXP_FIELD_NUMBER: _ClassVar[int]
        ADD_FIELD_NUMBER: _ClassVar[int]
        level: int
        exp: int
        add: int
        def __init__(self, level: _Optional[int] = ..., exp: _Optional[int] = ..., add: _Optional[int] = ...) -> None: ...
    class CharacterGift(_message.Message):
        __slots__ = ["origin", "final", "add", "is_graded"]
        ORIGIN_FIELD_NUMBER: _ClassVar[int]
        FINAL_FIELD_NUMBER: _ClassVar[int]
        ADD_FIELD_NUMBER: _ClassVar[int]
        IS_GRADED_FIELD_NUMBER: _ClassVar[int]
        origin: int
        final: int
        add: int
        is_graded: bool
        def __init__(self, origin: _Optional[int] = ..., final: _Optional[int] = ..., add: _Optional[int] = ..., is_graded: bool = ...) -> None: ...
    MODE_ID_FIELD_NUMBER: _ClassVar[int]
    LEVEL_CHANGE_FIELD_NUMBER: _ClassVar[int]
    MATCH_CHEST_FIELD_NUMBER: _ClassVar[int]
    MAIN_CHARACTER_FIELD_NUMBER: _ClassVar[int]
    CHARACTER_GIFT_FIELD_NUMBER: _ClassVar[int]
    mode_id: int
    level_change: NotifyGameFinishReward.LevelChange
    match_chest: NotifyGameFinishReward.MatchChest
    main_character: NotifyGameFinishReward.MainCharacter
    character_gift: NotifyGameFinishReward.CharacterGift
    def __init__(self, mode_id: _Optional[int] = ..., level_change: _Optional[_Union[NotifyGameFinishReward.LevelChange, _Mapping]] = ..., match_chest: _Optional[_Union[NotifyGameFinishReward.MatchChest, _Mapping]] = ..., main_character: _Optional[_Union[NotifyGameFinishReward.MainCharacter, _Mapping]] = ..., character_gift: _Optional[_Union[NotifyGameFinishReward.CharacterGift, _Mapping]] = ...) -> None: ...

class NotifyActivityReward(_message.Message):
    __slots__ = ["activity_reward"]
    class ActivityReward(_message.Message):
        __slots__ = ["activity_id", "rewards"]
        ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
        REWARDS_FIELD_NUMBER: _ClassVar[int]
        activity_id: int
        rewards: _containers.RepeatedCompositeFieldContainer[RewardSlot]
        def __init__(self, activity_id: _Optional[int] = ..., rewards: _Optional[_Iterable[_Union[RewardSlot, _Mapping]]] = ...) -> None: ...
    ACTIVITY_REWARD_FIELD_NUMBER: _ClassVar[int]
    activity_reward: _containers.RepeatedCompositeFieldContainer[NotifyActivityReward.ActivityReward]
    def __init__(self, activity_reward: _Optional[_Iterable[_Union[NotifyActivityReward.ActivityReward, _Mapping]]] = ...) -> None: ...

class NotifyActivityPoint(_message.Message):
    __slots__ = ["activity_points"]
    class ActivityPoint(_message.Message):
        __slots__ = ["activity_id", "point"]
        ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
        POINT_FIELD_NUMBER: _ClassVar[int]
        activity_id: int
        point: int
        def __init__(self, activity_id: _Optional[int] = ..., point: _Optional[int] = ...) -> None: ...
    ACTIVITY_POINTS_FIELD_NUMBER: _ClassVar[int]
    activity_points: _containers.RepeatedCompositeFieldContainer[NotifyActivityPoint.ActivityPoint]
    def __init__(self, activity_points: _Optional[_Iterable[_Union[NotifyActivityPoint.ActivityPoint, _Mapping]]] = ...) -> None: ...

class NotifyLeaderboardPoint(_message.Message):
    __slots__ = ["leaderboard_points"]
    class LeaderboardPoint(_message.Message):
        __slots__ = ["leaderboard_id", "point"]
        LEADERBOARD_ID_FIELD_NUMBER: _ClassVar[int]
        POINT_FIELD_NUMBER: _ClassVar[int]
        leaderboard_id: int
        point: int
        def __init__(self, leaderboard_id: _Optional[int] = ..., point: _Optional[int] = ...) -> None: ...
    LEADERBOARD_POINTS_FIELD_NUMBER: _ClassVar[int]
    leaderboard_points: _containers.RepeatedCompositeFieldContainer[NotifyLeaderboardPoint.LeaderboardPoint]
    def __init__(self, leaderboard_points: _Optional[_Iterable[_Union[NotifyLeaderboardPoint.LeaderboardPoint, _Mapping]]] = ...) -> None: ...

class NotifyGamePause(_message.Message):
    __slots__ = ["paused"]
    PAUSED_FIELD_NUMBER: _ClassVar[int]
    paused: bool
    def __init__(self, paused: bool = ...) -> None: ...

class NotifyEndGameVote(_message.Message):
    __slots__ = ["results", "start_time", "duration_time"]
    class VoteResult(_message.Message):
        __slots__ = ["account_id", "yes"]
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        YES_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        yes: bool
        def __init__(self, account_id: _Optional[int] = ..., yes: bool = ...) -> None: ...
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    DURATION_TIME_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[NotifyEndGameVote.VoteResult]
    start_time: int
    duration_time: int
    def __init__(self, results: _Optional[_Iterable[_Union[NotifyEndGameVote.VoteResult, _Mapping]]] = ..., start_time: _Optional[int] = ..., duration_time: _Optional[int] = ...) -> None: ...

class NotifyObserveData(_message.Message):
    __slots__ = ["unit"]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    unit: GameLiveUnit
    def __init__(self, unit: _Optional[_Union[GameLiveUnit, _Mapping]] = ...) -> None: ...

class ActionMJStart(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class NewRoundOpenedTiles(_message.Message):
    __slots__ = ["seat", "tiles", "count"]
    SEAT_FIELD_NUMBER: _ClassVar[int]
    TILES_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    seat: int
    tiles: _containers.RepeatedScalarFieldContainer[str]
    count: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, seat: _Optional[int] = ..., tiles: _Optional[_Iterable[str]] = ..., count: _Optional[_Iterable[int]] = ...) -> None: ...

class MuyuInfo(_message.Message):
    __slots__ = ["seat", "count", "count_max", "id"]
    SEAT_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    COUNT_MAX_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    seat: int
    count: int
    count_max: int
    id: int
    def __init__(self, seat: _Optional[int] = ..., count: _Optional[int] = ..., count_max: _Optional[int] = ..., id: _Optional[int] = ...) -> None: ...

class ChuanmaGang(_message.Message):
    __slots__ = ["old_scores", "delta_scores", "scores", "gameend", "hules_history"]
    OLD_SCORES_FIELD_NUMBER: _ClassVar[int]
    DELTA_SCORES_FIELD_NUMBER: _ClassVar[int]
    SCORES_FIELD_NUMBER: _ClassVar[int]
    GAMEEND_FIELD_NUMBER: _ClassVar[int]
    HULES_HISTORY_FIELD_NUMBER: _ClassVar[int]
    old_scores: _containers.RepeatedScalarFieldContainer[int]
    delta_scores: _containers.RepeatedScalarFieldContainer[int]
    scores: _containers.RepeatedScalarFieldContainer[int]
    gameend: GameEnd
    hules_history: _containers.RepeatedCompositeFieldContainer[HuleInfo]
    def __init__(self, old_scores: _Optional[_Iterable[int]] = ..., delta_scores: _Optional[_Iterable[int]] = ..., scores: _Optional[_Iterable[int]] = ..., gameend: _Optional[_Union[GameEnd, _Mapping]] = ..., hules_history: _Optional[_Iterable[_Union[HuleInfo, _Mapping]]] = ...) -> None: ...

class YongchangInfo(_message.Message):
    __slots__ = ["seat", "moqie_count", "moqie_bonus", "shouqie_count", "shouqie_bonus"]
    SEAT_FIELD_NUMBER: _ClassVar[int]
    MOQIE_COUNT_FIELD_NUMBER: _ClassVar[int]
    MOQIE_BONUS_FIELD_NUMBER: _ClassVar[int]
    SHOUQIE_COUNT_FIELD_NUMBER: _ClassVar[int]
    SHOUQIE_BONUS_FIELD_NUMBER: _ClassVar[int]
    seat: int
    moqie_count: int
    moqie_bonus: int
    shouqie_count: int
    shouqie_bonus: int
    def __init__(self, seat: _Optional[int] = ..., moqie_count: _Optional[int] = ..., moqie_bonus: _Optional[int] = ..., shouqie_count: _Optional[int] = ..., shouqie_bonus: _Optional[int] = ...) -> None: ...

class ActionNewCard(_message.Message):
    __slots__ = ["field_spell"]
    FIELD_SPELL_FIELD_NUMBER: _ClassVar[int]
    field_spell: int
    def __init__(self, field_spell: _Optional[int] = ...) -> None: ...

class RecordNewCard(_message.Message):
    __slots__ = ["field_spell"]
    FIELD_SPELL_FIELD_NUMBER: _ClassVar[int]
    field_spell: int
    def __init__(self, field_spell: _Optional[int] = ...) -> None: ...

class ActionNewRound(_message.Message):
    __slots__ = ["chang", "ju", "ben", "tiles", "dora", "scores", "operation", "liqibang", "tingpais0", "tingpais1", "al", "md5", "left_tile_count", "doras", "opens", "muyu", "ju_count", "field_spell", "sha256", "yongchang", "saltSha256"]
    CHANG_FIELD_NUMBER: _ClassVar[int]
    JU_FIELD_NUMBER: _ClassVar[int]
    BEN_FIELD_NUMBER: _ClassVar[int]
    TILES_FIELD_NUMBER: _ClassVar[int]
    DORA_FIELD_NUMBER: _ClassVar[int]
    SCORES_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    LIQIBANG_FIELD_NUMBER: _ClassVar[int]
    TINGPAIS0_FIELD_NUMBER: _ClassVar[int]
    TINGPAIS1_FIELD_NUMBER: _ClassVar[int]
    AL_FIELD_NUMBER: _ClassVar[int]
    MD5_FIELD_NUMBER: _ClassVar[int]
    LEFT_TILE_COUNT_FIELD_NUMBER: _ClassVar[int]
    DORAS_FIELD_NUMBER: _ClassVar[int]
    OPENS_FIELD_NUMBER: _ClassVar[int]
    MUYU_FIELD_NUMBER: _ClassVar[int]
    JU_COUNT_FIELD_NUMBER: _ClassVar[int]
    FIELD_SPELL_FIELD_NUMBER: _ClassVar[int]
    SHA256_FIELD_NUMBER: _ClassVar[int]
    YONGCHANG_FIELD_NUMBER: _ClassVar[int]
    SALTSHA256_FIELD_NUMBER: _ClassVar[int]
    chang: int
    ju: int
    ben: int
    tiles: _containers.RepeatedScalarFieldContainer[str]
    dora: str
    scores: _containers.RepeatedScalarFieldContainer[int]
    operation: OptionalOperationList
    liqibang: int
    tingpais0: _containers.RepeatedCompositeFieldContainer[TingPaiDiscardInfo]
    tingpais1: _containers.RepeatedCompositeFieldContainer[TingPaiInfo]
    al: bool
    md5: str
    left_tile_count: int
    doras: _containers.RepeatedScalarFieldContainer[str]
    opens: _containers.RepeatedCompositeFieldContainer[NewRoundOpenedTiles]
    muyu: MuyuInfo
    ju_count: int
    field_spell: int
    sha256: str
    yongchang: YongchangInfo
    saltSha256: str
    def __init__(self, chang: _Optional[int] = ..., ju: _Optional[int] = ..., ben: _Optional[int] = ..., tiles: _Optional[_Iterable[str]] = ..., dora: _Optional[str] = ..., scores: _Optional[_Iterable[int]] = ..., operation: _Optional[_Union[OptionalOperationList, _Mapping]] = ..., liqibang: _Optional[int] = ..., tingpais0: _Optional[_Iterable[_Union[TingPaiDiscardInfo, _Mapping]]] = ..., tingpais1: _Optional[_Iterable[_Union[TingPaiInfo, _Mapping]]] = ..., al: bool = ..., md5: _Optional[str] = ..., left_tile_count: _Optional[int] = ..., doras: _Optional[_Iterable[str]] = ..., opens: _Optional[_Iterable[_Union[NewRoundOpenedTiles, _Mapping]]] = ..., muyu: _Optional[_Union[MuyuInfo, _Mapping]] = ..., ju_count: _Optional[int] = ..., field_spell: _Optional[int] = ..., sha256: _Optional[str] = ..., yongchang: _Optional[_Union[YongchangInfo, _Mapping]] = ..., saltSha256: _Optional[str] = ...) -> None: ...

class RecordNewRound(_message.Message):
    __slots__ = ["chang", "ju", "ben", "dora", "scores", "liqibang", "tiles0", "tiles1", "tiles2", "tiles3", "tingpai", "operation", "md5", "paishan", "left_tile_count", "doras", "opens", "muyu", "operations", "ju_count", "field_spell", "sha256", "yongchang", "saltSha256", "salt"]
    class TingPai(_message.Message):
        __slots__ = ["seat", "tingpais1"]
        SEAT_FIELD_NUMBER: _ClassVar[int]
        TINGPAIS1_FIELD_NUMBER: _ClassVar[int]
        seat: int
        tingpais1: _containers.RepeatedCompositeFieldContainer[TingPaiInfo]
        def __init__(self, seat: _Optional[int] = ..., tingpais1: _Optional[_Iterable[_Union[TingPaiInfo, _Mapping]]] = ...) -> None: ...
    CHANG_FIELD_NUMBER: _ClassVar[int]
    JU_FIELD_NUMBER: _ClassVar[int]
    BEN_FIELD_NUMBER: _ClassVar[int]
    DORA_FIELD_NUMBER: _ClassVar[int]
    SCORES_FIELD_NUMBER: _ClassVar[int]
    LIQIBANG_FIELD_NUMBER: _ClassVar[int]
    TILES0_FIELD_NUMBER: _ClassVar[int]
    TILES1_FIELD_NUMBER: _ClassVar[int]
    TILES2_FIELD_NUMBER: _ClassVar[int]
    TILES3_FIELD_NUMBER: _ClassVar[int]
    TINGPAI_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    MD5_FIELD_NUMBER: _ClassVar[int]
    PAISHAN_FIELD_NUMBER: _ClassVar[int]
    LEFT_TILE_COUNT_FIELD_NUMBER: _ClassVar[int]
    DORAS_FIELD_NUMBER: _ClassVar[int]
    OPENS_FIELD_NUMBER: _ClassVar[int]
    MUYU_FIELD_NUMBER: _ClassVar[int]
    OPERATIONS_FIELD_NUMBER: _ClassVar[int]
    JU_COUNT_FIELD_NUMBER: _ClassVar[int]
    FIELD_SPELL_FIELD_NUMBER: _ClassVar[int]
    SHA256_FIELD_NUMBER: _ClassVar[int]
    YONGCHANG_FIELD_NUMBER: _ClassVar[int]
    SALTSHA256_FIELD_NUMBER: _ClassVar[int]
    SALT_FIELD_NUMBER: _ClassVar[int]
    chang: int
    ju: int
    ben: int
    dora: str
    scores: _containers.RepeatedScalarFieldContainer[int]
    liqibang: int
    tiles0: _containers.RepeatedScalarFieldContainer[str]
    tiles1: _containers.RepeatedScalarFieldContainer[str]
    tiles2: _containers.RepeatedScalarFieldContainer[str]
    tiles3: _containers.RepeatedScalarFieldContainer[str]
    tingpai: _containers.RepeatedCompositeFieldContainer[RecordNewRound.TingPai]
    operation: OptionalOperationList
    md5: str
    paishan: str
    left_tile_count: int
    doras: _containers.RepeatedScalarFieldContainer[str]
    opens: _containers.RepeatedCompositeFieldContainer[NewRoundOpenedTiles]
    muyu: MuyuInfo
    operations: _containers.RepeatedCompositeFieldContainer[OptionalOperationList]
    ju_count: int
    field_spell: int
    sha256: str
    yongchang: YongchangInfo
    saltSha256: str
    salt: str
    def __init__(self, chang: _Optional[int] = ..., ju: _Optional[int] = ..., ben: _Optional[int] = ..., dora: _Optional[str] = ..., scores: _Optional[_Iterable[int]] = ..., liqibang: _Optional[int] = ..., tiles0: _Optional[_Iterable[str]] = ..., tiles1: _Optional[_Iterable[str]] = ..., tiles2: _Optional[_Iterable[str]] = ..., tiles3: _Optional[_Iterable[str]] = ..., tingpai: _Optional[_Iterable[_Union[RecordNewRound.TingPai, _Mapping]]] = ..., operation: _Optional[_Union[OptionalOperationList, _Mapping]] = ..., md5: _Optional[str] = ..., paishan: _Optional[str] = ..., left_tile_count: _Optional[int] = ..., doras: _Optional[_Iterable[str]] = ..., opens: _Optional[_Iterable[_Union[NewRoundOpenedTiles, _Mapping]]] = ..., muyu: _Optional[_Union[MuyuInfo, _Mapping]] = ..., operations: _Optional[_Iterable[_Union[OptionalOperationList, _Mapping]]] = ..., ju_count: _Optional[int] = ..., field_spell: _Optional[int] = ..., sha256: _Optional[str] = ..., yongchang: _Optional[_Union[YongchangInfo, _Mapping]] = ..., saltSha256: _Optional[str] = ..., salt: _Optional[str] = ...) -> None: ...

class GameSnapshot(_message.Message):
    __slots__ = ["chang", "ju", "ben", "index_player", "left_tile_count", "hands", "doras", "liqibang", "players", "zhenting"]
    class PlayerSnapshot(_message.Message):
        __slots__ = ["score", "liqiposition", "tilenum", "qipais", "mings"]
        class Fulu(_message.Message):
            __slots__ = ["type", "tile"]
            TYPE_FIELD_NUMBER: _ClassVar[int]
            TILE_FIELD_NUMBER: _ClassVar[int]
            FROM_FIELD_NUMBER: _ClassVar[int]
            type: int
            tile: _containers.RepeatedScalarFieldContainer[str]
            def __init__(self, type: _Optional[int] = ..., tile: _Optional[_Iterable[str]] = ..., **kwargs) -> None: ...
        SCORE_FIELD_NUMBER: _ClassVar[int]
        LIQIPOSITION_FIELD_NUMBER: _ClassVar[int]
        TILENUM_FIELD_NUMBER: _ClassVar[int]
        QIPAIS_FIELD_NUMBER: _ClassVar[int]
        MINGS_FIELD_NUMBER: _ClassVar[int]
        score: int
        liqiposition: int
        tilenum: int
        qipais: _containers.RepeatedScalarFieldContainer[str]
        mings: _containers.RepeatedCompositeFieldContainer[GameSnapshot.PlayerSnapshot.Fulu]
        def __init__(self, score: _Optional[int] = ..., liqiposition: _Optional[int] = ..., tilenum: _Optional[int] = ..., qipais: _Optional[_Iterable[str]] = ..., mings: _Optional[_Iterable[_Union[GameSnapshot.PlayerSnapshot.Fulu, _Mapping]]] = ...) -> None: ...
    CHANG_FIELD_NUMBER: _ClassVar[int]
    JU_FIELD_NUMBER: _ClassVar[int]
    BEN_FIELD_NUMBER: _ClassVar[int]
    INDEX_PLAYER_FIELD_NUMBER: _ClassVar[int]
    LEFT_TILE_COUNT_FIELD_NUMBER: _ClassVar[int]
    HANDS_FIELD_NUMBER: _ClassVar[int]
    DORAS_FIELD_NUMBER: _ClassVar[int]
    LIQIBANG_FIELD_NUMBER: _ClassVar[int]
    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    ZHENTING_FIELD_NUMBER: _ClassVar[int]
    chang: int
    ju: int
    ben: int
    index_player: int
    left_tile_count: int
    hands: _containers.RepeatedScalarFieldContainer[str]
    doras: _containers.RepeatedScalarFieldContainer[str]
    liqibang: int
    players: _containers.RepeatedCompositeFieldContainer[GameSnapshot.PlayerSnapshot]
    zhenting: bool
    def __init__(self, chang: _Optional[int] = ..., ju: _Optional[int] = ..., ben: _Optional[int] = ..., index_player: _Optional[int] = ..., left_tile_count: _Optional[int] = ..., hands: _Optional[_Iterable[str]] = ..., doras: _Optional[_Iterable[str]] = ..., liqibang: _Optional[int] = ..., players: _Optional[_Iterable[_Union[GameSnapshot.PlayerSnapshot, _Mapping]]] = ..., zhenting: bool = ...) -> None: ...

class ActionPrototype(_message.Message):
    __slots__ = ["step", "name", "data"]
    STEP_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    step: int
    name: str
    data: bytes
    def __init__(self, step: _Optional[int] = ..., name: _Optional[str] = ..., data: _Optional[bytes] = ...) -> None: ...

class GameDetailRecords(_message.Message):
    __slots__ = ["records", "version", "actions", "bar"]
    RECORDS_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    ACTIONS_FIELD_NUMBER: _ClassVar[int]
    BAR_FIELD_NUMBER: _ClassVar[int]
    records: _containers.RepeatedScalarFieldContainer[bytes]
    version: int
    actions: _containers.RepeatedCompositeFieldContainer[GameAction]
    bar: bytes
    def __init__(self, records: _Optional[_Iterable[bytes]] = ..., version: _Optional[int] = ..., actions: _Optional[_Iterable[_Union[GameAction, _Mapping]]] = ..., bar: _Optional[bytes] = ...) -> None: ...

class GameSelfOperation(_message.Message):
    __slots__ = ["type", "index", "tile", "cancel_operation", "moqie", "timeuse", "tile_state", "change_tiles", "tile_states", "gap_type"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    TILE_FIELD_NUMBER: _ClassVar[int]
    CANCEL_OPERATION_FIELD_NUMBER: _ClassVar[int]
    MOQIE_FIELD_NUMBER: _ClassVar[int]
    TIMEUSE_FIELD_NUMBER: _ClassVar[int]
    TILE_STATE_FIELD_NUMBER: _ClassVar[int]
    CHANGE_TILES_FIELD_NUMBER: _ClassVar[int]
    TILE_STATES_FIELD_NUMBER: _ClassVar[int]
    GAP_TYPE_FIELD_NUMBER: _ClassVar[int]
    type: int
    index: int
    tile: str
    cancel_operation: bool
    moqie: bool
    timeuse: int
    tile_state: int
    change_tiles: _containers.RepeatedScalarFieldContainer[str]
    tile_states: _containers.RepeatedScalarFieldContainer[int]
    gap_type: int
    def __init__(self, type: _Optional[int] = ..., index: _Optional[int] = ..., tile: _Optional[str] = ..., cancel_operation: bool = ..., moqie: bool = ..., timeuse: _Optional[int] = ..., tile_state: _Optional[int] = ..., change_tiles: _Optional[_Iterable[str]] = ..., tile_states: _Optional[_Iterable[int]] = ..., gap_type: _Optional[int] = ...) -> None: ...

class GameChiPengGang(_message.Message):
    __slots__ = ["type", "index", "cancel_operation", "timeuse"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    CANCEL_OPERATION_FIELD_NUMBER: _ClassVar[int]
    TIMEUSE_FIELD_NUMBER: _ClassVar[int]
    type: int
    index: int
    cancel_operation: bool
    timeuse: int
    def __init__(self, type: _Optional[int] = ..., index: _Optional[int] = ..., cancel_operation: bool = ..., timeuse: _Optional[int] = ...) -> None: ...

class GameVoteGameEnd(_message.Message):
    __slots__ = ["yes"]
    YES_FIELD_NUMBER: _ClassVar[int]
    yes: bool
    def __init__(self, yes: bool = ...) -> None: ...

class GameUserInput(_message.Message):
    __slots__ = ["seat", "type", "emo", "operation", "cpg", "vote"]
    SEAT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    EMO_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    CPG_FIELD_NUMBER: _ClassVar[int]
    VOTE_FIELD_NUMBER: _ClassVar[int]
    seat: int
    type: int
    emo: int
    operation: GameSelfOperation
    cpg: GameChiPengGang
    vote: GameVoteGameEnd
    def __init__(self, seat: _Optional[int] = ..., type: _Optional[int] = ..., emo: _Optional[int] = ..., operation: _Optional[_Union[GameSelfOperation, _Mapping]] = ..., cpg: _Optional[_Union[GameChiPengGang, _Mapping]] = ..., vote: _Optional[_Union[GameVoteGameEnd, _Mapping]] = ...) -> None: ...

class GameUserEvent(_message.Message):
    __slots__ = ["seat", "type"]
    SEAT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    seat: int
    type: int
    def __init__(self, seat: _Optional[int] = ..., type: _Optional[int] = ...) -> None: ...

class GameAction(_message.Message):
    __slots__ = ["passed", "type", "result", "user_input", "user_event", "game_event"]
    PASSED_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    USER_INPUT_FIELD_NUMBER: _ClassVar[int]
    USER_EVENT_FIELD_NUMBER: _ClassVar[int]
    GAME_EVENT_FIELD_NUMBER: _ClassVar[int]
    passed: int
    type: int
    result: bytes
    user_input: GameUserInput
    user_event: GameUserEvent
    game_event: int
    def __init__(self, passed: _Optional[int] = ..., type: _Optional[int] = ..., result: _Optional[bytes] = ..., user_input: _Optional[_Union[GameUserInput, _Mapping]] = ..., user_event: _Optional[_Union[GameUserEvent, _Mapping]] = ..., game_event: _Optional[int] = ...) -> None: ...

class OptionalOperation(_message.Message):
    __slots__ = ["type", "combination", "change_tiles", "change_tile_states", "gap_type"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    COMBINATION_FIELD_NUMBER: _ClassVar[int]
    CHANGE_TILES_FIELD_NUMBER: _ClassVar[int]
    CHANGE_TILE_STATES_FIELD_NUMBER: _ClassVar[int]
    GAP_TYPE_FIELD_NUMBER: _ClassVar[int]
    type: int
    combination: _containers.RepeatedScalarFieldContainer[str]
    change_tiles: _containers.RepeatedScalarFieldContainer[str]
    change_tile_states: _containers.RepeatedScalarFieldContainer[int]
    gap_type: int
    def __init__(self, type: _Optional[int] = ..., combination: _Optional[_Iterable[str]] = ..., change_tiles: _Optional[_Iterable[str]] = ..., change_tile_states: _Optional[_Iterable[int]] = ..., gap_type: _Optional[int] = ...) -> None: ...

class OptionalOperationList(_message.Message):
    __slots__ = ["seat", "operation_list", "time_add", "time_fixed"]
    SEAT_FIELD_NUMBER: _ClassVar[int]
    OPERATION_LIST_FIELD_NUMBER: _ClassVar[int]
    TIME_ADD_FIELD_NUMBER: _ClassVar[int]
    TIME_FIXED_FIELD_NUMBER: _ClassVar[int]
    seat: int
    operation_list: _containers.RepeatedCompositeFieldContainer[OptionalOperation]
    time_add: int
    time_fixed: int
    def __init__(self, seat: _Optional[int] = ..., operation_list: _Optional[_Iterable[_Union[OptionalOperation, _Mapping]]] = ..., time_add: _Optional[int] = ..., time_fixed: _Optional[int] = ...) -> None: ...

class LiQiSuccess(_message.Message):
    __slots__ = ["seat", "score", "liqibang", "failed"]
    SEAT_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    LIQIBANG_FIELD_NUMBER: _ClassVar[int]
    FAILED_FIELD_NUMBER: _ClassVar[int]
    seat: int
    score: int
    liqibang: int
    failed: bool
    def __init__(self, seat: _Optional[int] = ..., score: _Optional[int] = ..., liqibang: _Optional[int] = ..., failed: bool = ...) -> None: ...

class FanInfo(_message.Message):
    __slots__ = ["name", "val", "id"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VAL_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    val: int
    id: int
    def __init__(self, name: _Optional[str] = ..., val: _Optional[int] = ..., id: _Optional[int] = ...) -> None: ...

class HuleInfo(_message.Message):
    __slots__ = ["hand", "ming", "hu_tile", "seat", "zimo", "qinjia", "liqi", "doras", "li_doras", "yiman", "count", "fans", "fu", "title", "point_rong", "point_zimo_qin", "point_zimo_xian", "title_id", "point_sum", "dadian", "baopai", "baopai_seats", "lines", "tianming_bonus"]
    HAND_FIELD_NUMBER: _ClassVar[int]
    MING_FIELD_NUMBER: _ClassVar[int]
    HU_TILE_FIELD_NUMBER: _ClassVar[int]
    SEAT_FIELD_NUMBER: _ClassVar[int]
    ZIMO_FIELD_NUMBER: _ClassVar[int]
    QINJIA_FIELD_NUMBER: _ClassVar[int]
    LIQI_FIELD_NUMBER: _ClassVar[int]
    DORAS_FIELD_NUMBER: _ClassVar[int]
    LI_DORAS_FIELD_NUMBER: _ClassVar[int]
    YIMAN_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    FANS_FIELD_NUMBER: _ClassVar[int]
    FU_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    POINT_RONG_FIELD_NUMBER: _ClassVar[int]
    POINT_ZIMO_QIN_FIELD_NUMBER: _ClassVar[int]
    POINT_ZIMO_XIAN_FIELD_NUMBER: _ClassVar[int]
    TITLE_ID_FIELD_NUMBER: _ClassVar[int]
    POINT_SUM_FIELD_NUMBER: _ClassVar[int]
    DADIAN_FIELD_NUMBER: _ClassVar[int]
    BAOPAI_FIELD_NUMBER: _ClassVar[int]
    BAOPAI_SEATS_FIELD_NUMBER: _ClassVar[int]
    LINES_FIELD_NUMBER: _ClassVar[int]
    TIANMING_BONUS_FIELD_NUMBER: _ClassVar[int]
    hand: _containers.RepeatedScalarFieldContainer[str]
    ming: _containers.RepeatedScalarFieldContainer[str]
    hu_tile: str
    seat: int
    zimo: bool
    qinjia: bool
    liqi: bool
    doras: _containers.RepeatedScalarFieldContainer[str]
    li_doras: _containers.RepeatedScalarFieldContainer[str]
    yiman: bool
    count: int
    fans: _containers.RepeatedCompositeFieldContainer[FanInfo]
    fu: int
    title: str
    point_rong: int
    point_zimo_qin: int
    point_zimo_xian: int
    title_id: int
    point_sum: int
    dadian: int
    baopai: int
    baopai_seats: _containers.RepeatedScalarFieldContainer[int]
    lines: _containers.RepeatedScalarFieldContainer[str]
    tianming_bonus: int
    def __init__(self, hand: _Optional[_Iterable[str]] = ..., ming: _Optional[_Iterable[str]] = ..., hu_tile: _Optional[str] = ..., seat: _Optional[int] = ..., zimo: bool = ..., qinjia: bool = ..., liqi: bool = ..., doras: _Optional[_Iterable[str]] = ..., li_doras: _Optional[_Iterable[str]] = ..., yiman: bool = ..., count: _Optional[int] = ..., fans: _Optional[_Iterable[_Union[FanInfo, _Mapping]]] = ..., fu: _Optional[int] = ..., title: _Optional[str] = ..., point_rong: _Optional[int] = ..., point_zimo_qin: _Optional[int] = ..., point_zimo_xian: _Optional[int] = ..., title_id: _Optional[int] = ..., point_sum: _Optional[int] = ..., dadian: _Optional[int] = ..., baopai: _Optional[int] = ..., baopai_seats: _Optional[_Iterable[int]] = ..., lines: _Optional[_Iterable[str]] = ..., tianming_bonus: _Optional[int] = ...) -> None: ...

class TingPaiInfo(_message.Message):
    __slots__ = ["tile", "haveyi", "yiman", "count", "fu", "biao_dora_count", "yiman_zimo", "count_zimo", "fu_zimo"]
    TILE_FIELD_NUMBER: _ClassVar[int]
    HAVEYI_FIELD_NUMBER: _ClassVar[int]
    YIMAN_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    FU_FIELD_NUMBER: _ClassVar[int]
    BIAO_DORA_COUNT_FIELD_NUMBER: _ClassVar[int]
    YIMAN_ZIMO_FIELD_NUMBER: _ClassVar[int]
    COUNT_ZIMO_FIELD_NUMBER: _ClassVar[int]
    FU_ZIMO_FIELD_NUMBER: _ClassVar[int]
    tile: str
    haveyi: bool
    yiman: bool
    count: int
    fu: int
    biao_dora_count: int
    yiman_zimo: bool
    count_zimo: int
    fu_zimo: int
    def __init__(self, tile: _Optional[str] = ..., haveyi: bool = ..., yiman: bool = ..., count: _Optional[int] = ..., fu: _Optional[int] = ..., biao_dora_count: _Optional[int] = ..., yiman_zimo: bool = ..., count_zimo: _Optional[int] = ..., fu_zimo: _Optional[int] = ...) -> None: ...

class TingPaiDiscardInfo(_message.Message):
    __slots__ = ["tile", "zhenting", "infos"]
    TILE_FIELD_NUMBER: _ClassVar[int]
    ZHENTING_FIELD_NUMBER: _ClassVar[int]
    INFOS_FIELD_NUMBER: _ClassVar[int]
    tile: str
    zhenting: bool
    infos: _containers.RepeatedCompositeFieldContainer[TingPaiInfo]
    def __init__(self, tile: _Optional[str] = ..., zhenting: bool = ..., infos: _Optional[_Iterable[_Union[TingPaiInfo, _Mapping]]] = ...) -> None: ...

class HunZhiYiJiBuffInfo(_message.Message):
    __slots__ = ["seat", "continue_deal_count", "overload"]
    SEAT_FIELD_NUMBER: _ClassVar[int]
    CONTINUE_DEAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    OVERLOAD_FIELD_NUMBER: _ClassVar[int]
    seat: int
    continue_deal_count: int
    overload: bool
    def __init__(self, seat: _Optional[int] = ..., continue_deal_count: _Optional[int] = ..., overload: bool = ...) -> None: ...

class GameEnd(_message.Message):
    __slots__ = ["scores"]
    SCORES_FIELD_NUMBER: _ClassVar[int]
    scores: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, scores: _Optional[_Iterable[int]] = ...) -> None: ...

class ActionSelectGap(_message.Message):
    __slots__ = ["gap_types", "tingpais0", "tingpais1", "operation"]
    GAP_TYPES_FIELD_NUMBER: _ClassVar[int]
    TINGPAIS0_FIELD_NUMBER: _ClassVar[int]
    TINGPAIS1_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    gap_types: _containers.RepeatedScalarFieldContainer[int]
    tingpais0: _containers.RepeatedCompositeFieldContainer[TingPaiDiscardInfo]
    tingpais1: _containers.RepeatedCompositeFieldContainer[TingPaiInfo]
    operation: OptionalOperationList
    def __init__(self, gap_types: _Optional[_Iterable[int]] = ..., tingpais0: _Optional[_Iterable[_Union[TingPaiDiscardInfo, _Mapping]]] = ..., tingpais1: _Optional[_Iterable[_Union[TingPaiInfo, _Mapping]]] = ..., operation: _Optional[_Union[OptionalOperationList, _Mapping]] = ...) -> None: ...

class RecordSelectGap(_message.Message):
    __slots__ = ["gap_types", "tingpai", "operation"]
    class TingPai(_message.Message):
        __slots__ = ["seat", "tingpais1"]
        SEAT_FIELD_NUMBER: _ClassVar[int]
        TINGPAIS1_FIELD_NUMBER: _ClassVar[int]
        seat: int
        tingpais1: _containers.RepeatedCompositeFieldContainer[TingPaiInfo]
        def __init__(self, seat: _Optional[int] = ..., tingpais1: _Optional[_Iterable[_Union[TingPaiInfo, _Mapping]]] = ...) -> None: ...
    GAP_TYPES_FIELD_NUMBER: _ClassVar[int]
    TINGPAI_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    gap_types: _containers.RepeatedScalarFieldContainer[int]
    tingpai: _containers.RepeatedCompositeFieldContainer[RecordSelectGap.TingPai]
    operation: OptionalOperationList
    def __init__(self, gap_types: _Optional[_Iterable[int]] = ..., tingpai: _Optional[_Iterable[_Union[RecordSelectGap.TingPai, _Mapping]]] = ..., operation: _Optional[_Union[OptionalOperationList, _Mapping]] = ...) -> None: ...

class ActionChangeTile(_message.Message):
    __slots__ = ["in_tiles", "in_tile_states", "out_tiles", "out_tile_states", "doras", "tingpais0", "tingpais1", "operation", "change_type"]
    IN_TILES_FIELD_NUMBER: _ClassVar[int]
    IN_TILE_STATES_FIELD_NUMBER: _ClassVar[int]
    OUT_TILES_FIELD_NUMBER: _ClassVar[int]
    OUT_TILE_STATES_FIELD_NUMBER: _ClassVar[int]
    DORAS_FIELD_NUMBER: _ClassVar[int]
    TINGPAIS0_FIELD_NUMBER: _ClassVar[int]
    TINGPAIS1_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    CHANGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    in_tiles: _containers.RepeatedScalarFieldContainer[str]
    in_tile_states: _containers.RepeatedScalarFieldContainer[int]
    out_tiles: _containers.RepeatedScalarFieldContainer[str]
    out_tile_states: _containers.RepeatedScalarFieldContainer[int]
    doras: _containers.RepeatedScalarFieldContainer[str]
    tingpais0: _containers.RepeatedCompositeFieldContainer[TingPaiDiscardInfo]
    tingpais1: _containers.RepeatedCompositeFieldContainer[TingPaiInfo]
    operation: OptionalOperationList
    change_type: int
    def __init__(self, in_tiles: _Optional[_Iterable[str]] = ..., in_tile_states: _Optional[_Iterable[int]] = ..., out_tiles: _Optional[_Iterable[str]] = ..., out_tile_states: _Optional[_Iterable[int]] = ..., doras: _Optional[_Iterable[str]] = ..., tingpais0: _Optional[_Iterable[_Union[TingPaiDiscardInfo, _Mapping]]] = ..., tingpais1: _Optional[_Iterable[_Union[TingPaiInfo, _Mapping]]] = ..., operation: _Optional[_Union[OptionalOperationList, _Mapping]] = ..., change_type: _Optional[int] = ...) -> None: ...

class RecordChangeTile(_message.Message):
    __slots__ = ["doras", "tingpai", "change_tile_infos", "operation", "change_type", "operations"]
    class TingPai(_message.Message):
        __slots__ = ["seat", "tingpais1"]
        SEAT_FIELD_NUMBER: _ClassVar[int]
        TINGPAIS1_FIELD_NUMBER: _ClassVar[int]
        seat: int
        tingpais1: _containers.RepeatedCompositeFieldContainer[TingPaiInfo]
        def __init__(self, seat: _Optional[int] = ..., tingpais1: _Optional[_Iterable[_Union[TingPaiInfo, _Mapping]]] = ...) -> None: ...
    class ChangeTile(_message.Message):
        __slots__ = ["in_tiles", "in_tile_states", "out_tiles", "out_tile_states"]
        IN_TILES_FIELD_NUMBER: _ClassVar[int]
        IN_TILE_STATES_FIELD_NUMBER: _ClassVar[int]
        OUT_TILES_FIELD_NUMBER: _ClassVar[int]
        OUT_TILE_STATES_FIELD_NUMBER: _ClassVar[int]
        in_tiles: _containers.RepeatedScalarFieldContainer[str]
        in_tile_states: _containers.RepeatedScalarFieldContainer[int]
        out_tiles: _containers.RepeatedScalarFieldContainer[str]
        out_tile_states: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, in_tiles: _Optional[_Iterable[str]] = ..., in_tile_states: _Optional[_Iterable[int]] = ..., out_tiles: _Optional[_Iterable[str]] = ..., out_tile_states: _Optional[_Iterable[int]] = ...) -> None: ...
    DORAS_FIELD_NUMBER: _ClassVar[int]
    TINGPAI_FIELD_NUMBER: _ClassVar[int]
    CHANGE_TILE_INFOS_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    CHANGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    OPERATIONS_FIELD_NUMBER: _ClassVar[int]
    doras: _containers.RepeatedScalarFieldContainer[str]
    tingpai: _containers.RepeatedCompositeFieldContainer[RecordChangeTile.TingPai]
    change_tile_infos: _containers.RepeatedCompositeFieldContainer[RecordChangeTile.ChangeTile]
    operation: OptionalOperationList
    change_type: int
    operations: _containers.RepeatedCompositeFieldContainer[OptionalOperationList]
    def __init__(self, doras: _Optional[_Iterable[str]] = ..., tingpai: _Optional[_Iterable[_Union[RecordChangeTile.TingPai, _Mapping]]] = ..., change_tile_infos: _Optional[_Iterable[_Union[RecordChangeTile.ChangeTile, _Mapping]]] = ..., operation: _Optional[_Union[OptionalOperationList, _Mapping]] = ..., change_type: _Optional[int] = ..., operations: _Optional[_Iterable[_Union[OptionalOperationList, _Mapping]]] = ...) -> None: ...

class ActionRevealTile(_message.Message):
    __slots__ = ["seat", "is_liqi", "is_wliqi", "moqie", "scores", "liqibang", "operation", "tingpais", "tile", "zhenting"]
    SEAT_FIELD_NUMBER: _ClassVar[int]
    IS_LIQI_FIELD_NUMBER: _ClassVar[int]
    IS_WLIQI_FIELD_NUMBER: _ClassVar[int]
    MOQIE_FIELD_NUMBER: _ClassVar[int]
    SCORES_FIELD_NUMBER: _ClassVar[int]
    LIQIBANG_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    TINGPAIS_FIELD_NUMBER: _ClassVar[int]
    TILE_FIELD_NUMBER: _ClassVar[int]
    ZHENTING_FIELD_NUMBER: _ClassVar[int]
    seat: int
    is_liqi: bool
    is_wliqi: bool
    moqie: bool
    scores: _containers.RepeatedScalarFieldContainer[int]
    liqibang: int
    operation: OptionalOperationList
    tingpais: _containers.RepeatedCompositeFieldContainer[TingPaiInfo]
    tile: str
    zhenting: bool
    def __init__(self, seat: _Optional[int] = ..., is_liqi: bool = ..., is_wliqi: bool = ..., moqie: bool = ..., scores: _Optional[_Iterable[int]] = ..., liqibang: _Optional[int] = ..., operation: _Optional[_Union[OptionalOperationList, _Mapping]] = ..., tingpais: _Optional[_Iterable[_Union[TingPaiInfo, _Mapping]]] = ..., tile: _Optional[str] = ..., zhenting: bool = ...) -> None: ...

class RecordRevealTile(_message.Message):
    __slots__ = ["seat", "is_liqi", "is_wliqi", "moqie", "scores", "liqibang", "operations", "tingpais", "tile", "zhenting"]
    SEAT_FIELD_NUMBER: _ClassVar[int]
    IS_LIQI_FIELD_NUMBER: _ClassVar[int]
    IS_WLIQI_FIELD_NUMBER: _ClassVar[int]
    MOQIE_FIELD_NUMBER: _ClassVar[int]
    SCORES_FIELD_NUMBER: _ClassVar[int]
    LIQIBANG_FIELD_NUMBER: _ClassVar[int]
    OPERATIONS_FIELD_NUMBER: _ClassVar[int]
    TINGPAIS_FIELD_NUMBER: _ClassVar[int]
    TILE_FIELD_NUMBER: _ClassVar[int]
    ZHENTING_FIELD_NUMBER: _ClassVar[int]
    seat: int
    is_liqi: bool
    is_wliqi: bool
    moqie: bool
    scores: _containers.RepeatedScalarFieldContainer[int]
    liqibang: int
    operations: _containers.RepeatedCompositeFieldContainer[OptionalOperationList]
    tingpais: _containers.RepeatedCompositeFieldContainer[TingPaiInfo]
    tile: str
    zhenting: _containers.RepeatedScalarFieldContainer[bool]
    def __init__(self, seat: _Optional[int] = ..., is_liqi: bool = ..., is_wliqi: bool = ..., moqie: bool = ..., scores: _Optional[_Iterable[int]] = ..., liqibang: _Optional[int] = ..., operations: _Optional[_Iterable[_Union[OptionalOperationList, _Mapping]]] = ..., tingpais: _Optional[_Iterable[_Union[TingPaiInfo, _Mapping]]] = ..., tile: _Optional[str] = ..., zhenting: _Optional[_Iterable[bool]] = ...) -> None: ...

class ActionUnveilTile(_message.Message):
    __slots__ = ["seat", "scores", "liqibang", "operation"]
    SEAT_FIELD_NUMBER: _ClassVar[int]
    SCORES_FIELD_NUMBER: _ClassVar[int]
    LIQIBANG_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    seat: int
    scores: _containers.RepeatedScalarFieldContainer[int]
    liqibang: int
    operation: OptionalOperationList
    def __init__(self, seat: _Optional[int] = ..., scores: _Optional[_Iterable[int]] = ..., liqibang: _Optional[int] = ..., operation: _Optional[_Union[OptionalOperationList, _Mapping]] = ...) -> None: ...

class RecordUnveilTile(_message.Message):
    __slots__ = ["seat", "scores", "liqibang", "operation"]
    SEAT_FIELD_NUMBER: _ClassVar[int]
    SCORES_FIELD_NUMBER: _ClassVar[int]
    LIQIBANG_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    seat: int
    scores: _containers.RepeatedScalarFieldContainer[int]
    liqibang: int
    operation: OptionalOperationList
    def __init__(self, seat: _Optional[int] = ..., scores: _Optional[_Iterable[int]] = ..., liqibang: _Optional[int] = ..., operation: _Optional[_Union[OptionalOperationList, _Mapping]] = ...) -> None: ...

class ActionLockTile(_message.Message):
    __slots__ = ["seat", "scores", "liqibang", "tile", "operation", "zhenting", "tingpais", "doras", "lock_state"]
    SEAT_FIELD_NUMBER: _ClassVar[int]
    SCORES_FIELD_NUMBER: _ClassVar[int]
    LIQIBANG_FIELD_NUMBER: _ClassVar[int]
    TILE_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    ZHENTING_FIELD_NUMBER: _ClassVar[int]
    TINGPAIS_FIELD_NUMBER: _ClassVar[int]
    DORAS_FIELD_NUMBER: _ClassVar[int]
    LOCK_STATE_FIELD_NUMBER: _ClassVar[int]
    seat: int
    scores: _containers.RepeatedScalarFieldContainer[int]
    liqibang: int
    tile: str
    operation: OptionalOperationList
    zhenting: bool
    tingpais: _containers.RepeatedCompositeFieldContainer[TingPaiInfo]
    doras: _containers.RepeatedScalarFieldContainer[str]
    lock_state: int
    def __init__(self, seat: _Optional[int] = ..., scores: _Optional[_Iterable[int]] = ..., liqibang: _Optional[int] = ..., tile: _Optional[str] = ..., operation: _Optional[_Union[OptionalOperationList, _Mapping]] = ..., zhenting: bool = ..., tingpais: _Optional[_Iterable[_Union[TingPaiInfo, _Mapping]]] = ..., doras: _Optional[_Iterable[str]] = ..., lock_state: _Optional[int] = ...) -> None: ...

class RecordLockTile(_message.Message):
    __slots__ = ["seat", "scores", "liqibang", "tile", "operation", "zhentings", "tingpais", "doras", "lock_state"]
    SEAT_FIELD_NUMBER: _ClassVar[int]
    SCORES_FIELD_NUMBER: _ClassVar[int]
    LIQIBANG_FIELD_NUMBER: _ClassVar[int]
    TILE_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    ZHENTINGS_FIELD_NUMBER: _ClassVar[int]
    TINGPAIS_FIELD_NUMBER: _ClassVar[int]
    DORAS_FIELD_NUMBER: _ClassVar[int]
    LOCK_STATE_FIELD_NUMBER: _ClassVar[int]
    seat: int
    scores: _containers.RepeatedScalarFieldContainer[int]
    liqibang: int
    tile: str
    operation: _containers.RepeatedCompositeFieldContainer[OptionalOperationList]
    zhentings: _containers.RepeatedScalarFieldContainer[bool]
    tingpais: _containers.RepeatedCompositeFieldContainer[TingPaiInfo]
    doras: _containers.RepeatedScalarFieldContainer[str]
    lock_state: int
    def __init__(self, seat: _Optional[int] = ..., scores: _Optional[_Iterable[int]] = ..., liqibang: _Optional[int] = ..., tile: _Optional[str] = ..., operation: _Optional[_Iterable[_Union[OptionalOperationList, _Mapping]]] = ..., zhentings: _Optional[_Iterable[bool]] = ..., tingpais: _Optional[_Iterable[_Union[TingPaiInfo, _Mapping]]] = ..., doras: _Optional[_Iterable[str]] = ..., lock_state: _Optional[int] = ...) -> None: ...

class ActionDiscardTile(_message.Message):
    __slots__ = ["seat", "tile", "is_liqi", "operation", "moqie", "zhenting", "tingpais", "doras", "is_wliqi", "tile_state", "muyu", "revealed", "scores", "liqibang", "yongchang", "hun_zhi_yi_ji_info"]
    SEAT_FIELD_NUMBER: _ClassVar[int]
    TILE_FIELD_NUMBER: _ClassVar[int]
    IS_LIQI_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    MOQIE_FIELD_NUMBER: _ClassVar[int]
    ZHENTING_FIELD_NUMBER: _ClassVar[int]
    TINGPAIS_FIELD_NUMBER: _ClassVar[int]
    DORAS_FIELD_NUMBER: _ClassVar[int]
    IS_WLIQI_FIELD_NUMBER: _ClassVar[int]
    TILE_STATE_FIELD_NUMBER: _ClassVar[int]
    MUYU_FIELD_NUMBER: _ClassVar[int]
    REVEALED_FIELD_NUMBER: _ClassVar[int]
    SCORES_FIELD_NUMBER: _ClassVar[int]
    LIQIBANG_FIELD_NUMBER: _ClassVar[int]
    YONGCHANG_FIELD_NUMBER: _ClassVar[int]
    HUN_ZHI_YI_JI_INFO_FIELD_NUMBER: _ClassVar[int]
    seat: int
    tile: str
    is_liqi: bool
    operation: OptionalOperationList
    moqie: bool
    zhenting: bool
    tingpais: _containers.RepeatedCompositeFieldContainer[TingPaiInfo]
    doras: _containers.RepeatedScalarFieldContainer[str]
    is_wliqi: bool
    tile_state: int
    muyu: MuyuInfo
    revealed: bool
    scores: _containers.RepeatedScalarFieldContainer[int]
    liqibang: int
    yongchang: YongchangInfo
    hun_zhi_yi_ji_info: HunZhiYiJiBuffInfo
    def __init__(self, seat: _Optional[int] = ..., tile: _Optional[str] = ..., is_liqi: bool = ..., operation: _Optional[_Union[OptionalOperationList, _Mapping]] = ..., moqie: bool = ..., zhenting: bool = ..., tingpais: _Optional[_Iterable[_Union[TingPaiInfo, _Mapping]]] = ..., doras: _Optional[_Iterable[str]] = ..., is_wliqi: bool = ..., tile_state: _Optional[int] = ..., muyu: _Optional[_Union[MuyuInfo, _Mapping]] = ..., revealed: bool = ..., scores: _Optional[_Iterable[int]] = ..., liqibang: _Optional[int] = ..., yongchang: _Optional[_Union[YongchangInfo, _Mapping]] = ..., hun_zhi_yi_ji_info: _Optional[_Union[HunZhiYiJiBuffInfo, _Mapping]] = ...) -> None: ...

class RecordDiscardTile(_message.Message):
    __slots__ = ["seat", "tile", "is_liqi", "moqie", "zhenting", "tingpais", "doras", "is_wliqi", "operations", "tile_state", "muyu", "yongchang", "hun_zhi_yi_ji_info"]
    SEAT_FIELD_NUMBER: _ClassVar[int]
    TILE_FIELD_NUMBER: _ClassVar[int]
    IS_LIQI_FIELD_NUMBER: _ClassVar[int]
    MOQIE_FIELD_NUMBER: _ClassVar[int]
    ZHENTING_FIELD_NUMBER: _ClassVar[int]
    TINGPAIS_FIELD_NUMBER: _ClassVar[int]
    DORAS_FIELD_NUMBER: _ClassVar[int]
    IS_WLIQI_FIELD_NUMBER: _ClassVar[int]
    OPERATIONS_FIELD_NUMBER: _ClassVar[int]
    TILE_STATE_FIELD_NUMBER: _ClassVar[int]
    MUYU_FIELD_NUMBER: _ClassVar[int]
    YONGCHANG_FIELD_NUMBER: _ClassVar[int]
    HUN_ZHI_YI_JI_INFO_FIELD_NUMBER: _ClassVar[int]
    seat: int
    tile: str
    is_liqi: bool
    moqie: bool
    zhenting: _containers.RepeatedScalarFieldContainer[bool]
    tingpais: _containers.RepeatedCompositeFieldContainer[TingPaiInfo]
    doras: _containers.RepeatedScalarFieldContainer[str]
    is_wliqi: bool
    operations: _containers.RepeatedCompositeFieldContainer[OptionalOperationList]
    tile_state: int
    muyu: MuyuInfo
    yongchang: YongchangInfo
    hun_zhi_yi_ji_info: HunZhiYiJiBuffInfo
    def __init__(self, seat: _Optional[int] = ..., tile: _Optional[str] = ..., is_liqi: bool = ..., moqie: bool = ..., zhenting: _Optional[_Iterable[bool]] = ..., tingpais: _Optional[_Iterable[_Union[TingPaiInfo, _Mapping]]] = ..., doras: _Optional[_Iterable[str]] = ..., is_wliqi: bool = ..., operations: _Optional[_Iterable[_Union[OptionalOperationList, _Mapping]]] = ..., tile_state: _Optional[int] = ..., muyu: _Optional[_Union[MuyuInfo, _Mapping]] = ..., yongchang: _Optional[_Union[YongchangInfo, _Mapping]] = ..., hun_zhi_yi_ji_info: _Optional[_Union[HunZhiYiJiBuffInfo, _Mapping]] = ...) -> None: ...

class ActionDealTile(_message.Message):
    __slots__ = ["seat", "tile", "left_tile_count", "operation", "liqi", "doras", "zhenting", "tingpais", "tile_state", "muyu", "tile_index", "hun_zhi_yi_ji_info"]
    SEAT_FIELD_NUMBER: _ClassVar[int]
    TILE_FIELD_NUMBER: _ClassVar[int]
    LEFT_TILE_COUNT_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    LIQI_FIELD_NUMBER: _ClassVar[int]
    DORAS_FIELD_NUMBER: _ClassVar[int]
    ZHENTING_FIELD_NUMBER: _ClassVar[int]
    TINGPAIS_FIELD_NUMBER: _ClassVar[int]
    TILE_STATE_FIELD_NUMBER: _ClassVar[int]
    MUYU_FIELD_NUMBER: _ClassVar[int]
    TILE_INDEX_FIELD_NUMBER: _ClassVar[int]
    HUN_ZHI_YI_JI_INFO_FIELD_NUMBER: _ClassVar[int]
    seat: int
    tile: str
    left_tile_count: int
    operation: OptionalOperationList
    liqi: LiQiSuccess
    doras: _containers.RepeatedScalarFieldContainer[str]
    zhenting: bool
    tingpais: _containers.RepeatedCompositeFieldContainer[TingPaiDiscardInfo]
    tile_state: int
    muyu: MuyuInfo
    tile_index: int
    hun_zhi_yi_ji_info: HunZhiYiJiBuffInfo
    def __init__(self, seat: _Optional[int] = ..., tile: _Optional[str] = ..., left_tile_count: _Optional[int] = ..., operation: _Optional[_Union[OptionalOperationList, _Mapping]] = ..., liqi: _Optional[_Union[LiQiSuccess, _Mapping]] = ..., doras: _Optional[_Iterable[str]] = ..., zhenting: bool = ..., tingpais: _Optional[_Iterable[_Union[TingPaiDiscardInfo, _Mapping]]] = ..., tile_state: _Optional[int] = ..., muyu: _Optional[_Union[MuyuInfo, _Mapping]] = ..., tile_index: _Optional[int] = ..., hun_zhi_yi_ji_info: _Optional[_Union[HunZhiYiJiBuffInfo, _Mapping]] = ...) -> None: ...

class RecordDealTile(_message.Message):
    __slots__ = ["seat", "tile", "left_tile_count", "liqi", "doras", "zhenting", "operation", "tile_state", "muyu", "tile_index", "hun_zhi_yi_ji_info"]
    SEAT_FIELD_NUMBER: _ClassVar[int]
    TILE_FIELD_NUMBER: _ClassVar[int]
    LEFT_TILE_COUNT_FIELD_NUMBER: _ClassVar[int]
    LIQI_FIELD_NUMBER: _ClassVar[int]
    DORAS_FIELD_NUMBER: _ClassVar[int]
    ZHENTING_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    TILE_STATE_FIELD_NUMBER: _ClassVar[int]
    MUYU_FIELD_NUMBER: _ClassVar[int]
    TILE_INDEX_FIELD_NUMBER: _ClassVar[int]
    HUN_ZHI_YI_JI_INFO_FIELD_NUMBER: _ClassVar[int]
    seat: int
    tile: str
    left_tile_count: int
    liqi: LiQiSuccess
    doras: _containers.RepeatedScalarFieldContainer[str]
    zhenting: _containers.RepeatedScalarFieldContainer[bool]
    operation: OptionalOperationList
    tile_state: int
    muyu: MuyuInfo
    tile_index: int
    hun_zhi_yi_ji_info: HunZhiYiJiBuffInfo
    def __init__(self, seat: _Optional[int] = ..., tile: _Optional[str] = ..., left_tile_count: _Optional[int] = ..., liqi: _Optional[_Union[LiQiSuccess, _Mapping]] = ..., doras: _Optional[_Iterable[str]] = ..., zhenting: _Optional[_Iterable[bool]] = ..., operation: _Optional[_Union[OptionalOperationList, _Mapping]] = ..., tile_state: _Optional[int] = ..., muyu: _Optional[_Union[MuyuInfo, _Mapping]] = ..., tile_index: _Optional[int] = ..., hun_zhi_yi_ji_info: _Optional[_Union[HunZhiYiJiBuffInfo, _Mapping]] = ...) -> None: ...

class ActionFillAwaitingTiles(_message.Message):
    __slots__ = ["awaiting_tiles", "left_tile_count", "operation", "liqi"]
    AWAITING_TILES_FIELD_NUMBER: _ClassVar[int]
    LEFT_TILE_COUNT_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    LIQI_FIELD_NUMBER: _ClassVar[int]
    awaiting_tiles: _containers.RepeatedScalarFieldContainer[str]
    left_tile_count: int
    operation: OptionalOperationList
    liqi: LiQiSuccess
    def __init__(self, awaiting_tiles: _Optional[_Iterable[str]] = ..., left_tile_count: _Optional[int] = ..., operation: _Optional[_Union[OptionalOperationList, _Mapping]] = ..., liqi: _Optional[_Union[LiQiSuccess, _Mapping]] = ...) -> None: ...

class RecordFillAwaitingTiles(_message.Message):
    __slots__ = ["awaiting_tiles", "left_tile_count", "operation", "liqi"]
    AWAITING_TILES_FIELD_NUMBER: _ClassVar[int]
    LEFT_TILE_COUNT_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    LIQI_FIELD_NUMBER: _ClassVar[int]
    awaiting_tiles: _containers.RepeatedScalarFieldContainer[str]
    left_tile_count: int
    operation: OptionalOperationList
    liqi: LiQiSuccess
    def __init__(self, awaiting_tiles: _Optional[_Iterable[str]] = ..., left_tile_count: _Optional[int] = ..., operation: _Optional[_Union[OptionalOperationList, _Mapping]] = ..., liqi: _Optional[_Union[LiQiSuccess, _Mapping]] = ...) -> None: ...

class ActionChiPengGang(_message.Message):
    __slots__ = ["seat", "type", "tiles", "froms", "liqi", "operation", "zhenting", "tingpais", "tile_states", "muyu", "scores", "liqibang", "yongchang", "hun_zhi_yi_ji_info"]
    SEAT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TILES_FIELD_NUMBER: _ClassVar[int]
    FROMS_FIELD_NUMBER: _ClassVar[int]
    LIQI_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    ZHENTING_FIELD_NUMBER: _ClassVar[int]
    TINGPAIS_FIELD_NUMBER: _ClassVar[int]
    TILE_STATES_FIELD_NUMBER: _ClassVar[int]
    MUYU_FIELD_NUMBER: _ClassVar[int]
    SCORES_FIELD_NUMBER: _ClassVar[int]
    LIQIBANG_FIELD_NUMBER: _ClassVar[int]
    YONGCHANG_FIELD_NUMBER: _ClassVar[int]
    HUN_ZHI_YI_JI_INFO_FIELD_NUMBER: _ClassVar[int]
    seat: int
    type: int
    tiles: _containers.RepeatedScalarFieldContainer[str]
    froms: _containers.RepeatedScalarFieldContainer[int]
    liqi: LiQiSuccess
    operation: OptionalOperationList
    zhenting: bool
    tingpais: _containers.RepeatedCompositeFieldContainer[TingPaiDiscardInfo]
    tile_states: _containers.RepeatedScalarFieldContainer[int]
    muyu: MuyuInfo
    scores: _containers.RepeatedScalarFieldContainer[int]
    liqibang: int
    yongchang: YongchangInfo
    hun_zhi_yi_ji_info: HunZhiYiJiBuffInfo
    def __init__(self, seat: _Optional[int] = ..., type: _Optional[int] = ..., tiles: _Optional[_Iterable[str]] = ..., froms: _Optional[_Iterable[int]] = ..., liqi: _Optional[_Union[LiQiSuccess, _Mapping]] = ..., operation: _Optional[_Union[OptionalOperationList, _Mapping]] = ..., zhenting: bool = ..., tingpais: _Optional[_Iterable[_Union[TingPaiDiscardInfo, _Mapping]]] = ..., tile_states: _Optional[_Iterable[int]] = ..., muyu: _Optional[_Union[MuyuInfo, _Mapping]] = ..., scores: _Optional[_Iterable[int]] = ..., liqibang: _Optional[int] = ..., yongchang: _Optional[_Union[YongchangInfo, _Mapping]] = ..., hun_zhi_yi_ji_info: _Optional[_Union[HunZhiYiJiBuffInfo, _Mapping]] = ...) -> None: ...

class RecordChiPengGang(_message.Message):
    __slots__ = ["seat", "type", "tiles", "froms", "liqi", "zhenting", "operation", "tile_states", "muyu", "scores", "liqibang", "yongchang", "hun_zhi_yi_ji_info"]
    SEAT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TILES_FIELD_NUMBER: _ClassVar[int]
    FROMS_FIELD_NUMBER: _ClassVar[int]
    LIQI_FIELD_NUMBER: _ClassVar[int]
    ZHENTING_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    TILE_STATES_FIELD_NUMBER: _ClassVar[int]
    MUYU_FIELD_NUMBER: _ClassVar[int]
    SCORES_FIELD_NUMBER: _ClassVar[int]
    LIQIBANG_FIELD_NUMBER: _ClassVar[int]
    YONGCHANG_FIELD_NUMBER: _ClassVar[int]
    HUN_ZHI_YI_JI_INFO_FIELD_NUMBER: _ClassVar[int]
    seat: int
    type: int
    tiles: _containers.RepeatedScalarFieldContainer[str]
    froms: _containers.RepeatedScalarFieldContainer[int]
    liqi: LiQiSuccess
    zhenting: _containers.RepeatedScalarFieldContainer[bool]
    operation: OptionalOperationList
    tile_states: _containers.RepeatedScalarFieldContainer[int]
    muyu: MuyuInfo
    scores: _containers.RepeatedScalarFieldContainer[int]
    liqibang: int
    yongchang: YongchangInfo
    hun_zhi_yi_ji_info: HunZhiYiJiBuffInfo
    def __init__(self, seat: _Optional[int] = ..., type: _Optional[int] = ..., tiles: _Optional[_Iterable[str]] = ..., froms: _Optional[_Iterable[int]] = ..., liqi: _Optional[_Union[LiQiSuccess, _Mapping]] = ..., zhenting: _Optional[_Iterable[bool]] = ..., operation: _Optional[_Union[OptionalOperationList, _Mapping]] = ..., tile_states: _Optional[_Iterable[int]] = ..., muyu: _Optional[_Union[MuyuInfo, _Mapping]] = ..., scores: _Optional[_Iterable[int]] = ..., liqibang: _Optional[int] = ..., yongchang: _Optional[_Union[YongchangInfo, _Mapping]] = ..., hun_zhi_yi_ji_info: _Optional[_Union[HunZhiYiJiBuffInfo, _Mapping]] = ...) -> None: ...

class ActionGangResult(_message.Message):
    __slots__ = ["gang_infos"]
    GANG_INFOS_FIELD_NUMBER: _ClassVar[int]
    gang_infos: ChuanmaGang
    def __init__(self, gang_infos: _Optional[_Union[ChuanmaGang, _Mapping]] = ...) -> None: ...

class RecordGangResult(_message.Message):
    __slots__ = ["gang_infos"]
    GANG_INFOS_FIELD_NUMBER: _ClassVar[int]
    gang_infos: ChuanmaGang
    def __init__(self, gang_infos: _Optional[_Union[ChuanmaGang, _Mapping]] = ...) -> None: ...

class ActionGangResultEnd(_message.Message):
    __slots__ = ["gang_infos"]
    GANG_INFOS_FIELD_NUMBER: _ClassVar[int]
    gang_infos: ChuanmaGang
    def __init__(self, gang_infos: _Optional[_Union[ChuanmaGang, _Mapping]] = ...) -> None: ...

class RecordGangResultEnd(_message.Message):
    __slots__ = ["gang_infos"]
    GANG_INFOS_FIELD_NUMBER: _ClassVar[int]
    gang_infos: ChuanmaGang
    def __init__(self, gang_infos: _Optional[_Union[ChuanmaGang, _Mapping]] = ...) -> None: ...

class ActionAnGangAddGang(_message.Message):
    __slots__ = ["seat", "type", "tiles", "operation", "doras", "zhenting", "tingpais", "muyu"]
    SEAT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TILES_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    DORAS_FIELD_NUMBER: _ClassVar[int]
    ZHENTING_FIELD_NUMBER: _ClassVar[int]
    TINGPAIS_FIELD_NUMBER: _ClassVar[int]
    MUYU_FIELD_NUMBER: _ClassVar[int]
    seat: int
    type: int
    tiles: str
    operation: OptionalOperationList
    doras: _containers.RepeatedScalarFieldContainer[str]
    zhenting: bool
    tingpais: _containers.RepeatedCompositeFieldContainer[TingPaiInfo]
    muyu: MuyuInfo
    def __init__(self, seat: _Optional[int] = ..., type: _Optional[int] = ..., tiles: _Optional[str] = ..., operation: _Optional[_Union[OptionalOperationList, _Mapping]] = ..., doras: _Optional[_Iterable[str]] = ..., zhenting: bool = ..., tingpais: _Optional[_Iterable[_Union[TingPaiInfo, _Mapping]]] = ..., muyu: _Optional[_Union[MuyuInfo, _Mapping]] = ...) -> None: ...

class RecordAnGangAddGang(_message.Message):
    __slots__ = ["seat", "type", "tiles", "doras", "operations", "muyu"]
    SEAT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TILES_FIELD_NUMBER: _ClassVar[int]
    DORAS_FIELD_NUMBER: _ClassVar[int]
    OPERATIONS_FIELD_NUMBER: _ClassVar[int]
    MUYU_FIELD_NUMBER: _ClassVar[int]
    seat: int
    type: int
    tiles: str
    doras: _containers.RepeatedScalarFieldContainer[str]
    operations: _containers.RepeatedCompositeFieldContainer[OptionalOperationList]
    muyu: MuyuInfo
    def __init__(self, seat: _Optional[int] = ..., type: _Optional[int] = ..., tiles: _Optional[str] = ..., doras: _Optional[_Iterable[str]] = ..., operations: _Optional[_Iterable[_Union[OptionalOperationList, _Mapping]]] = ..., muyu: _Optional[_Union[MuyuInfo, _Mapping]] = ...) -> None: ...

class ActionBaBei(_message.Message):
    __slots__ = ["seat", "operation", "doras", "zhenting", "tingpais", "moqie", "tile_state", "muyu"]
    SEAT_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    DORAS_FIELD_NUMBER: _ClassVar[int]
    ZHENTING_FIELD_NUMBER: _ClassVar[int]
    TINGPAIS_FIELD_NUMBER: _ClassVar[int]
    MOQIE_FIELD_NUMBER: _ClassVar[int]
    TILE_STATE_FIELD_NUMBER: _ClassVar[int]
    MUYU_FIELD_NUMBER: _ClassVar[int]
    seat: int
    operation: OptionalOperationList
    doras: _containers.RepeatedScalarFieldContainer[str]
    zhenting: bool
    tingpais: _containers.RepeatedCompositeFieldContainer[TingPaiInfo]
    moqie: bool
    tile_state: int
    muyu: MuyuInfo
    def __init__(self, seat: _Optional[int] = ..., operation: _Optional[_Union[OptionalOperationList, _Mapping]] = ..., doras: _Optional[_Iterable[str]] = ..., zhenting: bool = ..., tingpais: _Optional[_Iterable[_Union[TingPaiInfo, _Mapping]]] = ..., moqie: bool = ..., tile_state: _Optional[int] = ..., muyu: _Optional[_Union[MuyuInfo, _Mapping]] = ...) -> None: ...

class RecordBaBei(_message.Message):
    __slots__ = ["seat", "doras", "operations", "moqie", "tile_state", "muyu"]
    SEAT_FIELD_NUMBER: _ClassVar[int]
    DORAS_FIELD_NUMBER: _ClassVar[int]
    OPERATIONS_FIELD_NUMBER: _ClassVar[int]
    MOQIE_FIELD_NUMBER: _ClassVar[int]
    TILE_STATE_FIELD_NUMBER: _ClassVar[int]
    MUYU_FIELD_NUMBER: _ClassVar[int]
    seat: int
    doras: _containers.RepeatedScalarFieldContainer[str]
    operations: _containers.RepeatedCompositeFieldContainer[OptionalOperationList]
    moqie: bool
    tile_state: int
    muyu: MuyuInfo
    def __init__(self, seat: _Optional[int] = ..., doras: _Optional[_Iterable[str]] = ..., operations: _Optional[_Iterable[_Union[OptionalOperationList, _Mapping]]] = ..., moqie: bool = ..., tile_state: _Optional[int] = ..., muyu: _Optional[_Union[MuyuInfo, _Mapping]] = ...) -> None: ...

class ActionHule(_message.Message):
    __slots__ = ["hules", "old_scores", "delta_scores", "wait_timeout", "scores", "gameend", "doras", "muyu", "baopai", "hun_zhi_yi_ji_info"]
    HULES_FIELD_NUMBER: _ClassVar[int]
    OLD_SCORES_FIELD_NUMBER: _ClassVar[int]
    DELTA_SCORES_FIELD_NUMBER: _ClassVar[int]
    WAIT_TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    SCORES_FIELD_NUMBER: _ClassVar[int]
    GAMEEND_FIELD_NUMBER: _ClassVar[int]
    DORAS_FIELD_NUMBER: _ClassVar[int]
    MUYU_FIELD_NUMBER: _ClassVar[int]
    BAOPAI_FIELD_NUMBER: _ClassVar[int]
    HUN_ZHI_YI_JI_INFO_FIELD_NUMBER: _ClassVar[int]
    hules: _containers.RepeatedCompositeFieldContainer[HuleInfo]
    old_scores: _containers.RepeatedScalarFieldContainer[int]
    delta_scores: _containers.RepeatedScalarFieldContainer[int]
    wait_timeout: int
    scores: _containers.RepeatedScalarFieldContainer[int]
    gameend: GameEnd
    doras: _containers.RepeatedScalarFieldContainer[str]
    muyu: MuyuInfo
    baopai: int
    hun_zhi_yi_ji_info: HunZhiYiJiBuffInfo
    def __init__(self, hules: _Optional[_Iterable[_Union[HuleInfo, _Mapping]]] = ..., old_scores: _Optional[_Iterable[int]] = ..., delta_scores: _Optional[_Iterable[int]] = ..., wait_timeout: _Optional[int] = ..., scores: _Optional[_Iterable[int]] = ..., gameend: _Optional[_Union[GameEnd, _Mapping]] = ..., doras: _Optional[_Iterable[str]] = ..., muyu: _Optional[_Union[MuyuInfo, _Mapping]] = ..., baopai: _Optional[int] = ..., hun_zhi_yi_ji_info: _Optional[_Union[HunZhiYiJiBuffInfo, _Mapping]] = ...) -> None: ...

class RecordHule(_message.Message):
    __slots__ = ["hules", "old_scores", "delta_scores", "wait_timeout", "scores", "gameend", "doras", "muyu", "baopai", "hun_zhi_yi_ji_info"]
    HULES_FIELD_NUMBER: _ClassVar[int]
    OLD_SCORES_FIELD_NUMBER: _ClassVar[int]
    DELTA_SCORES_FIELD_NUMBER: _ClassVar[int]
    WAIT_TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    SCORES_FIELD_NUMBER: _ClassVar[int]
    GAMEEND_FIELD_NUMBER: _ClassVar[int]
    DORAS_FIELD_NUMBER: _ClassVar[int]
    MUYU_FIELD_NUMBER: _ClassVar[int]
    BAOPAI_FIELD_NUMBER: _ClassVar[int]
    HUN_ZHI_YI_JI_INFO_FIELD_NUMBER: _ClassVar[int]
    hules: _containers.RepeatedCompositeFieldContainer[HuleInfo]
    old_scores: _containers.RepeatedScalarFieldContainer[int]
    delta_scores: _containers.RepeatedScalarFieldContainer[int]
    wait_timeout: int
    scores: _containers.RepeatedScalarFieldContainer[int]
    gameend: GameEnd
    doras: _containers.RepeatedScalarFieldContainer[str]
    muyu: MuyuInfo
    baopai: int
    hun_zhi_yi_ji_info: HunZhiYiJiBuffInfo
    def __init__(self, hules: _Optional[_Iterable[_Union[HuleInfo, _Mapping]]] = ..., old_scores: _Optional[_Iterable[int]] = ..., delta_scores: _Optional[_Iterable[int]] = ..., wait_timeout: _Optional[int] = ..., scores: _Optional[_Iterable[int]] = ..., gameend: _Optional[_Union[GameEnd, _Mapping]] = ..., doras: _Optional[_Iterable[str]] = ..., muyu: _Optional[_Union[MuyuInfo, _Mapping]] = ..., baopai: _Optional[int] = ..., hun_zhi_yi_ji_info: _Optional[_Union[HunZhiYiJiBuffInfo, _Mapping]] = ...) -> None: ...

class HuInfoXueZhanMid(_message.Message):
    __slots__ = ["seat", "hand_count", "hand", "ming", "hu_tile", "zimo", "yiman", "count", "fans", "fu", "title_id"]
    SEAT_FIELD_NUMBER: _ClassVar[int]
    HAND_COUNT_FIELD_NUMBER: _ClassVar[int]
    HAND_FIELD_NUMBER: _ClassVar[int]
    MING_FIELD_NUMBER: _ClassVar[int]
    HU_TILE_FIELD_NUMBER: _ClassVar[int]
    ZIMO_FIELD_NUMBER: _ClassVar[int]
    YIMAN_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    FANS_FIELD_NUMBER: _ClassVar[int]
    FU_FIELD_NUMBER: _ClassVar[int]
    TITLE_ID_FIELD_NUMBER: _ClassVar[int]
    seat: int
    hand_count: int
    hand: _containers.RepeatedScalarFieldContainer[str]
    ming: _containers.RepeatedScalarFieldContainer[str]
    hu_tile: str
    zimo: bool
    yiman: bool
    count: int
    fans: _containers.RepeatedCompositeFieldContainer[FanInfo]
    fu: int
    title_id: int
    def __init__(self, seat: _Optional[int] = ..., hand_count: _Optional[int] = ..., hand: _Optional[_Iterable[str]] = ..., ming: _Optional[_Iterable[str]] = ..., hu_tile: _Optional[str] = ..., zimo: bool = ..., yiman: bool = ..., count: _Optional[int] = ..., fans: _Optional[_Iterable[_Union[FanInfo, _Mapping]]] = ..., fu: _Optional[int] = ..., title_id: _Optional[int] = ...) -> None: ...

class ActionHuleXueZhanMid(_message.Message):
    __slots__ = ["hules", "old_scores", "delta_scores", "scores", "doras", "muyu", "liqi", "zhenting"]
    HULES_FIELD_NUMBER: _ClassVar[int]
    OLD_SCORES_FIELD_NUMBER: _ClassVar[int]
    DELTA_SCORES_FIELD_NUMBER: _ClassVar[int]
    SCORES_FIELD_NUMBER: _ClassVar[int]
    DORAS_FIELD_NUMBER: _ClassVar[int]
    MUYU_FIELD_NUMBER: _ClassVar[int]
    LIQI_FIELD_NUMBER: _ClassVar[int]
    ZHENTING_FIELD_NUMBER: _ClassVar[int]
    hules: _containers.RepeatedCompositeFieldContainer[HuInfoXueZhanMid]
    old_scores: _containers.RepeatedScalarFieldContainer[int]
    delta_scores: _containers.RepeatedScalarFieldContainer[int]
    scores: _containers.RepeatedScalarFieldContainer[int]
    doras: _containers.RepeatedScalarFieldContainer[str]
    muyu: MuyuInfo
    liqi: LiQiSuccess
    zhenting: bool
    def __init__(self, hules: _Optional[_Iterable[_Union[HuInfoXueZhanMid, _Mapping]]] = ..., old_scores: _Optional[_Iterable[int]] = ..., delta_scores: _Optional[_Iterable[int]] = ..., scores: _Optional[_Iterable[int]] = ..., doras: _Optional[_Iterable[str]] = ..., muyu: _Optional[_Union[MuyuInfo, _Mapping]] = ..., liqi: _Optional[_Union[LiQiSuccess, _Mapping]] = ..., zhenting: bool = ...) -> None: ...

class RecordHuleXueZhanMid(_message.Message):
    __slots__ = ["hules", "old_scores", "delta_scores", "scores", "doras", "muyu", "liqi", "zhenting"]
    HULES_FIELD_NUMBER: _ClassVar[int]
    OLD_SCORES_FIELD_NUMBER: _ClassVar[int]
    DELTA_SCORES_FIELD_NUMBER: _ClassVar[int]
    SCORES_FIELD_NUMBER: _ClassVar[int]
    DORAS_FIELD_NUMBER: _ClassVar[int]
    MUYU_FIELD_NUMBER: _ClassVar[int]
    LIQI_FIELD_NUMBER: _ClassVar[int]
    ZHENTING_FIELD_NUMBER: _ClassVar[int]
    hules: _containers.RepeatedCompositeFieldContainer[HuInfoXueZhanMid]
    old_scores: _containers.RepeatedScalarFieldContainer[int]
    delta_scores: _containers.RepeatedScalarFieldContainer[int]
    scores: _containers.RepeatedScalarFieldContainer[int]
    doras: _containers.RepeatedScalarFieldContainer[str]
    muyu: MuyuInfo
    liqi: LiQiSuccess
    zhenting: _containers.RepeatedScalarFieldContainer[bool]
    def __init__(self, hules: _Optional[_Iterable[_Union[HuInfoXueZhanMid, _Mapping]]] = ..., old_scores: _Optional[_Iterable[int]] = ..., delta_scores: _Optional[_Iterable[int]] = ..., scores: _Optional[_Iterable[int]] = ..., doras: _Optional[_Iterable[str]] = ..., muyu: _Optional[_Union[MuyuInfo, _Mapping]] = ..., liqi: _Optional[_Union[LiQiSuccess, _Mapping]] = ..., zhenting: _Optional[_Iterable[bool]] = ...) -> None: ...

class ActionHuleXueZhanEnd(_message.Message):
    __slots__ = ["hules", "old_scores", "delta_scores", "scores", "wait_timeout", "gameend", "doras", "muyu", "hules_history"]
    HULES_FIELD_NUMBER: _ClassVar[int]
    OLD_SCORES_FIELD_NUMBER: _ClassVar[int]
    DELTA_SCORES_FIELD_NUMBER: _ClassVar[int]
    SCORES_FIELD_NUMBER: _ClassVar[int]
    WAIT_TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    GAMEEND_FIELD_NUMBER: _ClassVar[int]
    DORAS_FIELD_NUMBER: _ClassVar[int]
    MUYU_FIELD_NUMBER: _ClassVar[int]
    HULES_HISTORY_FIELD_NUMBER: _ClassVar[int]
    hules: _containers.RepeatedCompositeFieldContainer[HuInfoXueZhanMid]
    old_scores: _containers.RepeatedScalarFieldContainer[int]
    delta_scores: _containers.RepeatedScalarFieldContainer[int]
    scores: _containers.RepeatedScalarFieldContainer[int]
    wait_timeout: int
    gameend: GameEnd
    doras: _containers.RepeatedScalarFieldContainer[str]
    muyu: MuyuInfo
    hules_history: _containers.RepeatedCompositeFieldContainer[HuleInfo]
    def __init__(self, hules: _Optional[_Iterable[_Union[HuInfoXueZhanMid, _Mapping]]] = ..., old_scores: _Optional[_Iterable[int]] = ..., delta_scores: _Optional[_Iterable[int]] = ..., scores: _Optional[_Iterable[int]] = ..., wait_timeout: _Optional[int] = ..., gameend: _Optional[_Union[GameEnd, _Mapping]] = ..., doras: _Optional[_Iterable[str]] = ..., muyu: _Optional[_Union[MuyuInfo, _Mapping]] = ..., hules_history: _Optional[_Iterable[_Union[HuleInfo, _Mapping]]] = ...) -> None: ...

class RecordHuleXueZhanEnd(_message.Message):
    __slots__ = ["hules", "old_scores", "delta_scores", "scores", "wait_timeout", "gameend", "doras", "muyu", "hules_history"]
    HULES_FIELD_NUMBER: _ClassVar[int]
    OLD_SCORES_FIELD_NUMBER: _ClassVar[int]
    DELTA_SCORES_FIELD_NUMBER: _ClassVar[int]
    SCORES_FIELD_NUMBER: _ClassVar[int]
    WAIT_TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    GAMEEND_FIELD_NUMBER: _ClassVar[int]
    DORAS_FIELD_NUMBER: _ClassVar[int]
    MUYU_FIELD_NUMBER: _ClassVar[int]
    HULES_HISTORY_FIELD_NUMBER: _ClassVar[int]
    hules: _containers.RepeatedCompositeFieldContainer[HuInfoXueZhanMid]
    old_scores: _containers.RepeatedScalarFieldContainer[int]
    delta_scores: _containers.RepeatedScalarFieldContainer[int]
    scores: _containers.RepeatedScalarFieldContainer[int]
    wait_timeout: int
    gameend: GameEnd
    doras: _containers.RepeatedScalarFieldContainer[str]
    muyu: MuyuInfo
    hules_history: _containers.RepeatedCompositeFieldContainer[HuleInfo]
    def __init__(self, hules: _Optional[_Iterable[_Union[HuInfoXueZhanMid, _Mapping]]] = ..., old_scores: _Optional[_Iterable[int]] = ..., delta_scores: _Optional[_Iterable[int]] = ..., scores: _Optional[_Iterable[int]] = ..., wait_timeout: _Optional[int] = ..., gameend: _Optional[_Union[GameEnd, _Mapping]] = ..., doras: _Optional[_Iterable[str]] = ..., muyu: _Optional[_Union[MuyuInfo, _Mapping]] = ..., hules_history: _Optional[_Iterable[_Union[HuleInfo, _Mapping]]] = ...) -> None: ...

class ActionLiuJu(_message.Message):
    __slots__ = ["type", "gameend", "seat", "tiles", "liqi", "allplayertiles", "muyu", "hules_history"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    GAMEEND_FIELD_NUMBER: _ClassVar[int]
    SEAT_FIELD_NUMBER: _ClassVar[int]
    TILES_FIELD_NUMBER: _ClassVar[int]
    LIQI_FIELD_NUMBER: _ClassVar[int]
    ALLPLAYERTILES_FIELD_NUMBER: _ClassVar[int]
    MUYU_FIELD_NUMBER: _ClassVar[int]
    HULES_HISTORY_FIELD_NUMBER: _ClassVar[int]
    type: int
    gameend: GameEnd
    seat: int
    tiles: _containers.RepeatedScalarFieldContainer[str]
    liqi: LiQiSuccess
    allplayertiles: _containers.RepeatedScalarFieldContainer[str]
    muyu: MuyuInfo
    hules_history: _containers.RepeatedCompositeFieldContainer[HuleInfo]
    def __init__(self, type: _Optional[int] = ..., gameend: _Optional[_Union[GameEnd, _Mapping]] = ..., seat: _Optional[int] = ..., tiles: _Optional[_Iterable[str]] = ..., liqi: _Optional[_Union[LiQiSuccess, _Mapping]] = ..., allplayertiles: _Optional[_Iterable[str]] = ..., muyu: _Optional[_Union[MuyuInfo, _Mapping]] = ..., hules_history: _Optional[_Iterable[_Union[HuleInfo, _Mapping]]] = ...) -> None: ...

class RecordLiuJu(_message.Message):
    __slots__ = ["type", "gameend", "seat", "tiles", "liqi", "allplayertiles", "muyu", "hules_history"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    GAMEEND_FIELD_NUMBER: _ClassVar[int]
    SEAT_FIELD_NUMBER: _ClassVar[int]
    TILES_FIELD_NUMBER: _ClassVar[int]
    LIQI_FIELD_NUMBER: _ClassVar[int]
    ALLPLAYERTILES_FIELD_NUMBER: _ClassVar[int]
    MUYU_FIELD_NUMBER: _ClassVar[int]
    HULES_HISTORY_FIELD_NUMBER: _ClassVar[int]
    type: int
    gameend: GameEnd
    seat: int
    tiles: _containers.RepeatedScalarFieldContainer[str]
    liqi: LiQiSuccess
    allplayertiles: _containers.RepeatedScalarFieldContainer[str]
    muyu: MuyuInfo
    hules_history: _containers.RepeatedCompositeFieldContainer[HuleInfo]
    def __init__(self, type: _Optional[int] = ..., gameend: _Optional[_Union[GameEnd, _Mapping]] = ..., seat: _Optional[int] = ..., tiles: _Optional[_Iterable[str]] = ..., liqi: _Optional[_Union[LiQiSuccess, _Mapping]] = ..., allplayertiles: _Optional[_Iterable[str]] = ..., muyu: _Optional[_Union[MuyuInfo, _Mapping]] = ..., hules_history: _Optional[_Iterable[_Union[HuleInfo, _Mapping]]] = ...) -> None: ...

class NoTilePlayerInfo(_message.Message):
    __slots__ = ["tingpai", "hand", "tings", "already_hule"]
    TINGPAI_FIELD_NUMBER: _ClassVar[int]
    HAND_FIELD_NUMBER: _ClassVar[int]
    TINGS_FIELD_NUMBER: _ClassVar[int]
    ALREADY_HULE_FIELD_NUMBER: _ClassVar[int]
    tingpai: bool
    hand: _containers.RepeatedScalarFieldContainer[str]
    tings: _containers.RepeatedCompositeFieldContainer[TingPaiInfo]
    already_hule: bool
    def __init__(self, tingpai: bool = ..., hand: _Optional[_Iterable[str]] = ..., tings: _Optional[_Iterable[_Union[TingPaiInfo, _Mapping]]] = ..., already_hule: bool = ...) -> None: ...

class NoTileScoreInfo(_message.Message):
    __slots__ = ["seat", "old_scores", "delta_scores", "hand", "ming", "doras", "score", "taxes", "lines"]
    SEAT_FIELD_NUMBER: _ClassVar[int]
    OLD_SCORES_FIELD_NUMBER: _ClassVar[int]
    DELTA_SCORES_FIELD_NUMBER: _ClassVar[int]
    HAND_FIELD_NUMBER: _ClassVar[int]
    MING_FIELD_NUMBER: _ClassVar[int]
    DORAS_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    TAXES_FIELD_NUMBER: _ClassVar[int]
    LINES_FIELD_NUMBER: _ClassVar[int]
    seat: int
    old_scores: _containers.RepeatedScalarFieldContainer[int]
    delta_scores: _containers.RepeatedScalarFieldContainer[int]
    hand: _containers.RepeatedScalarFieldContainer[str]
    ming: _containers.RepeatedScalarFieldContainer[str]
    doras: _containers.RepeatedScalarFieldContainer[str]
    score: int
    taxes: _containers.RepeatedScalarFieldContainer[int]
    lines: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, seat: _Optional[int] = ..., old_scores: _Optional[_Iterable[int]] = ..., delta_scores: _Optional[_Iterable[int]] = ..., hand: _Optional[_Iterable[str]] = ..., ming: _Optional[_Iterable[str]] = ..., doras: _Optional[_Iterable[str]] = ..., score: _Optional[int] = ..., taxes: _Optional[_Iterable[int]] = ..., lines: _Optional[_Iterable[str]] = ...) -> None: ...

class ActionNoTile(_message.Message):
    __slots__ = ["liujumanguan", "players", "scores", "gameend", "muyu", "hules_history"]
    LIUJUMANGUAN_FIELD_NUMBER: _ClassVar[int]
    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    SCORES_FIELD_NUMBER: _ClassVar[int]
    GAMEEND_FIELD_NUMBER: _ClassVar[int]
    MUYU_FIELD_NUMBER: _ClassVar[int]
    HULES_HISTORY_FIELD_NUMBER: _ClassVar[int]
    liujumanguan: bool
    players: _containers.RepeatedCompositeFieldContainer[NoTilePlayerInfo]
    scores: _containers.RepeatedCompositeFieldContainer[NoTileScoreInfo]
    gameend: bool
    muyu: MuyuInfo
    hules_history: _containers.RepeatedCompositeFieldContainer[HuleInfo]
    def __init__(self, liujumanguan: bool = ..., players: _Optional[_Iterable[_Union[NoTilePlayerInfo, _Mapping]]] = ..., scores: _Optional[_Iterable[_Union[NoTileScoreInfo, _Mapping]]] = ..., gameend: bool = ..., muyu: _Optional[_Union[MuyuInfo, _Mapping]] = ..., hules_history: _Optional[_Iterable[_Union[HuleInfo, _Mapping]]] = ...) -> None: ...

class RecordNoTile(_message.Message):
    __slots__ = ["liujumanguan", "players", "scores", "gameend", "muyu", "hules_history"]
    LIUJUMANGUAN_FIELD_NUMBER: _ClassVar[int]
    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    SCORES_FIELD_NUMBER: _ClassVar[int]
    GAMEEND_FIELD_NUMBER: _ClassVar[int]
    MUYU_FIELD_NUMBER: _ClassVar[int]
    HULES_HISTORY_FIELD_NUMBER: _ClassVar[int]
    liujumanguan: bool
    players: _containers.RepeatedCompositeFieldContainer[NoTilePlayerInfo]
    scores: _containers.RepeatedCompositeFieldContainer[NoTileScoreInfo]
    gameend: bool
    muyu: MuyuInfo
    hules_history: _containers.RepeatedCompositeFieldContainer[HuleInfo]
    def __init__(self, liujumanguan: bool = ..., players: _Optional[_Iterable[_Union[NoTilePlayerInfo, _Mapping]]] = ..., scores: _Optional[_Iterable[_Union[NoTileScoreInfo, _Mapping]]] = ..., gameend: bool = ..., muyu: _Optional[_Union[MuyuInfo, _Mapping]] = ..., hules_history: _Optional[_Iterable[_Union[HuleInfo, _Mapping]]] = ...) -> None: ...

class PlayerLeaving(_message.Message):
    __slots__ = ["seat"]
    SEAT_FIELD_NUMBER: _ClassVar[int]
    seat: int
    def __init__(self, seat: _Optional[int] = ...) -> None: ...

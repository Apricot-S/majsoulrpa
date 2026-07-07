from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GamePlayerState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NULL: _ClassVar[GamePlayerState]
    AUTH: _ClassVar[GamePlayerState]
    SYNCING: _ClassVar[GamePlayerState]
    READY: _ClassVar[GamePlayerState]
NULL: GamePlayerState
AUTH: GamePlayerState
SYNCING: GamePlayerState
READY: GamePlayerState

class AccSn(_message.Message):
    __slots__ = ()
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
    __slots__ = ()
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    time: int
    snapshot: bytes
    def __init__(self, account_id: _Optional[int] = ..., time: _Optional[int] = ..., snapshot: _Optional[bytes] = ...) -> None: ...

class Account(_message.Message):
    __slots__ = ()
    class PlatformDiamond(_message.Message):
        __slots__ = ()
        ID_FIELD_NUMBER: _ClassVar[int]
        COUNT_FIELD_NUMBER: _ClassVar[int]
        id: int
        count: int
        def __init__(self, id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...
    class PlatformSkinTicket(_message.Message):
        __slots__ = ()
        ID_FIELD_NUMBER: _ClassVar[int]
        COUNT_FIELD_NUMBER: _ClassVar[int]
        id: int
        count: int
        def __init__(self, id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...
    class ChallengeLevel(_message.Message):
        __slots__ = ()
        SEASON_FIELD_NUMBER: _ClassVar[int]
        LEVEL_FIELD_NUMBER: _ClassVar[int]
        RANK_FIELD_NUMBER: _ClassVar[int]
        season: int
        level: int
        rank: int
        def __init__(self, season: _Optional[int] = ..., level: _Optional[int] = ..., rank: _Optional[int] = ...) -> None: ...
    class AchievementCount(_message.Message):
        __slots__ = ()
        RARE_FIELD_NUMBER: _ClassVar[int]
        COUNT_FIELD_NUMBER: _ClassVar[int]
        rare: int
        count: int
        def __init__(self, rare: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...
    class Badge(_message.Message):
        __slots__ = ()
        ID_FIELD_NUMBER: _ClassVar[int]
        ACHIEVED_TIME_FIELD_NUMBER: _ClassVar[int]
        ACHIEVED_COUNTER_FIELD_NUMBER: _ClassVar[int]
        id: int
        achieved_time: int
        achieved_counter: int
        def __init__(self, id: _Optional[int] = ..., achieved_time: _Optional[int] = ..., achieved_counter: _Optional[int] = ...) -> None: ...
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
    FAVORITE_HU_FIELD_NUMBER: _ClassVar[int]
    BADGES_FIELD_NUMBER: _ClassVar[int]
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
    favorite_hu: _containers.RepeatedCompositeFieldContainer[FavoriteHu]
    badges: _containers.RepeatedCompositeFieldContainer[Account.Badge]
    def __init__(self, account_id: _Optional[int] = ..., nickname: _Optional[str] = ..., login_time: _Optional[int] = ..., logout_time: _Optional[int] = ..., room_id: _Optional[int] = ..., anti_addiction: _Optional[_Union[AntiAddiction, _Mapping]] = ..., title: _Optional[int] = ..., signature: _Optional[str] = ..., email: _Optional[str] = ..., email_verify: _Optional[int] = ..., gold: _Optional[int] = ..., diamond: _Optional[int] = ..., avatar_id: _Optional[int] = ..., vip: _Optional[int] = ..., birthday: _Optional[int] = ..., phone: _Optional[str] = ..., phone_verify: _Optional[int] = ..., platform_diamond: _Optional[_Iterable[_Union[Account.PlatformDiamond, _Mapping]]] = ..., level: _Optional[_Union[AccountLevel, _Mapping]] = ..., level3: _Optional[_Union[AccountLevel, _Mapping]] = ..., avatar_frame: _Optional[int] = ..., skin_ticket: _Optional[int] = ..., platform_skin_ticket: _Optional[_Iterable[_Union[Account.PlatformSkinTicket, _Mapping]]] = ..., verified: _Optional[int] = ..., challenge_levels: _Optional[_Iterable[_Union[Account.ChallengeLevel, _Mapping]]] = ..., achievement_count: _Optional[_Iterable[_Union[Account.AchievementCount, _Mapping]]] = ..., frozen_state: _Optional[int] = ..., loading_image: _Optional[_Iterable[int]] = ..., favorite_hu: _Optional[_Iterable[_Union[FavoriteHu, _Mapping]]] = ..., badges: _Optional[_Iterable[_Union[Account.Badge, _Mapping]]] = ...) -> None: ...

class AccountAchievementSnapshot(_message.Message):
    __slots__ = ()
    class RewardedGroupSnapshot(_message.Message):
        __slots__ = ()
        REWARDED_ID_FIELD_NUMBER: _ClassVar[int]
        rewarded_id: int
        def __init__(self, rewarded_id: _Optional[int] = ...) -> None: ...
    class AchievementVersion(_message.Message):
        __slots__ = ()
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

class AccountActiveState(_message.Message):
    __slots__ = ()
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
    def __init__(self, account_id: _Optional[int] = ..., login_time: _Optional[int] = ..., logout_time: _Optional[int] = ..., is_online: _Optional[bool] = ..., playing: _Optional[_Union[AccountPlayingGame, _Mapping]] = ...) -> None: ...

class AccountActivityUpdate(_message.Message):
    __slots__ = ()
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
    STORY_DATA_FIELD_NUMBER: _ClassVar[int]
    CHOOSE_UP_DATA_FIELD_NUMBER: _ClassVar[int]
    SIMULATION_V2_DATA_FIELD_NUMBER: _ClassVar[int]
    QUEST_CREW_DATA_FIELD_NUMBER: _ClassVar[int]
    SHOOT_DATA_FIELD_NUMBER: _ClassVar[int]
    BINGO_DATA_FIELD_NUMBER: _ClassVar[int]
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
    story_data: _containers.RepeatedCompositeFieldContainer[ActivityStoryData]
    choose_up_data: _containers.RepeatedCompositeFieldContainer[ActivityChooseUpData]
    simulation_v2_data: _containers.RepeatedCompositeFieldContainer[SimulationV2Data]
    quest_crew_data: _containers.RepeatedCompositeFieldContainer[ActivityQuestCrewChanges]
    shoot_data: _containers.RepeatedCompositeFieldContainer[ActivityShootData]
    bingo_data: _containers.RepeatedCompositeFieldContainer[ActivityBingoData]
    def __init__(self, mine_data: _Optional[_Iterable[_Union[MineActivityData, _Mapping]]] = ..., rpg_data: _Optional[_Iterable[_Union[RPGActivity, _Mapping]]] = ..., feed_data: _Optional[_Iterable[_Union[ActivityFeedData, _Mapping]]] = ..., spot_data: _Optional[_Iterable[_Union[ActivitySpotData, _Mapping]]] = ..., friend_gift_data: _Optional[_Iterable[_Union[ActivityFriendGiftData, _Mapping]]] = ..., upgrade_data: _Optional[_Iterable[_Union[ActivityUpgradeData, _Mapping]]] = ..., gacha_data: _Optional[_Iterable[_Union[ActivityGachaUpdateData, _Mapping]]] = ..., simulation_data: _Optional[_Iterable[_Union[ActivitySimulationData, _Mapping]]] = ..., combining_data: _Optional[_Iterable[_Union[ActivityCombiningLQData, _Mapping]]] = ..., village_data: _Optional[_Iterable[_Union[ActivityVillageData, _Mapping]]] = ..., festival_data: _Optional[_Iterable[_Union[ActivityFestivalData, _Mapping]]] = ..., island_data: _Optional[_Iterable[_Union[ActivityIslandData, _Mapping]]] = ..., story_data: _Optional[_Iterable[_Union[ActivityStoryData, _Mapping]]] = ..., choose_up_data: _Optional[_Iterable[_Union[ActivityChooseUpData, _Mapping]]] = ..., simulation_v2_data: _Optional[_Iterable[_Union[SimulationV2Data, _Mapping]]] = ..., quest_crew_data: _Optional[_Iterable[_Union[ActivityQuestCrewChanges, _Mapping]]] = ..., shoot_data: _Optional[_Iterable[_Union[ActivityShootData, _Mapping]]] = ..., bingo_data: _Optional[_Iterable[_Union[ActivityBingoData, _Mapping]]] = ...) -> None: ...

class AccountCacheView(_message.Message):
    __slots__ = ()
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
    def __init__(self, cache_version: _Optional[int] = ..., account_id: _Optional[int] = ..., nickname: _Optional[str] = ..., login_time: _Optional[int] = ..., logout_time: _Optional[int] = ..., is_online: _Optional[bool] = ..., room_id: _Optional[int] = ..., title: _Optional[int] = ..., avatar_id: _Optional[int] = ..., vip: _Optional[int] = ..., level: _Optional[_Union[AccountLevel, _Mapping]] = ..., playing_game: _Optional[_Union[AccountPlayingGame, _Mapping]] = ..., level3: _Optional[_Union[AccountLevel, _Mapping]] = ..., avatar_frame: _Optional[int] = ..., verified: _Optional[int] = ..., ban_deadline: _Optional[int] = ..., comment_ban: _Optional[int] = ..., ban_state: _Optional[int] = ...) -> None: ...

class AccountCharacterSnapshot(_message.Message):
    __slots__ = ()
    class MainCharacterSnapshot(_message.Message):
        __slots__ = ()
        CHARACTER_ID_FIELD_NUMBER: _ClassVar[int]
        character_id: int
        def __init__(self, character_id: _Optional[int] = ...) -> None: ...
    class SkinsSnapshot(_message.Message):
        __slots__ = ()
        SKIN_LIST_FIELD_NUMBER: _ClassVar[int]
        skin_list: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, skin_list: _Optional[_Iterable[int]] = ...) -> None: ...
    class HiddenCharacter(_message.Message):
        __slots__ = ()
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

class AccountDetailStatistic(_message.Message):
    __slots__ = ()
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
    __slots__ = ()
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    DETAIL_STATISTIC_FIELD_NUMBER: _ClassVar[int]
    category: int
    detail_statistic: AccountDetailStatistic
    def __init__(self, category: _Optional[int] = ..., detail_statistic: _Optional[_Union[AccountDetailStatistic, _Mapping]] = ...) -> None: ...

class AccountDetailStatisticV2(_message.Message):
    __slots__ = ()
    class RankStatistic(_message.Message):
        __slots__ = ()
        class RankData(_message.Message):
            __slots__ = ()
            class RankLevelData(_message.Message):
                __slots__ = ()
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
        __slots__ = ()
        TOTAL_STATISTIC_FIELD_NUMBER: _ClassVar[int]
        MONTH_STATISTIC_FIELD_NUMBER: _ClassVar[int]
        MONTH_REFRESH_TIME_FIELD_NUMBER: _ClassVar[int]
        total_statistic: AccountDetailStatistic
        month_statistic: AccountDetailStatistic
        month_refresh_time: int
        def __init__(self, total_statistic: _Optional[_Union[AccountDetailStatistic, _Mapping]] = ..., month_statistic: _Optional[_Union[AccountDetailStatistic, _Mapping]] = ..., month_refresh_time: _Optional[int] = ...) -> None: ...
    class ChallengeStatistic(_message.Message):
        __slots__ = ()
        class SeasonData(_message.Message):
            __slots__ = ()
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

class AccountFanAchieved(_message.Message):
    __slots__ = ()
    MAHJONG_CATEGORY_FIELD_NUMBER: _ClassVar[int]
    FAN_FIELD_NUMBER: _ClassVar[int]
    LIUJUMANGUAN_FIELD_NUMBER: _ClassVar[int]
    mahjong_category: int
    fan: _containers.RepeatedCompositeFieldContainer[AccountStatisticByFan]
    liujumanguan: int
    def __init__(self, mahjong_category: _Optional[int] = ..., fan: _Optional[_Iterable[_Union[AccountStatisticByFan, _Mapping]]] = ..., liujumanguan: _Optional[int] = ...) -> None: ...

class AccountGiftCodeRecord(_message.Message):
    __slots__ = ()
    USED_GIFT_CODE_FIELD_NUMBER: _ClassVar[int]
    used_gift_code: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, used_gift_code: _Optional[_Iterable[str]] = ...) -> None: ...

class AccountLevel(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    id: int
    score: int
    def __init__(self, id: _Optional[int] = ..., score: _Optional[int] = ...) -> None: ...

class AccountMahjongStatistic(_message.Message):
    __slots__ = ()
    class RoundSummary(_message.Message):
        __slots__ = ()
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
        __slots__ = ()
        TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
        DORA_ROUND_COUNT_FIELD_NUMBER: _ClassVar[int]
        TOTAL_FAN_FIELD_NUMBER: _ClassVar[int]
        total_count: int
        dora_round_count: int
        total_fan: int
        def __init__(self, total_count: _Optional[int] = ..., dora_round_count: _Optional[int] = ..., total_fan: _Optional[int] = ...) -> None: ...
    class Liqi20Summary(_message.Message):
        __slots__ = ()
        TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
        TOTAL_LIDORA_COUNT_FIELD_NUMBER: _ClassVar[int]
        AVERAGE_HU_POINT_FIELD_NUMBER: _ClassVar[int]
        total_count: int
        total_lidora_count: int
        average_hu_point: int
        def __init__(self, total_count: _Optional[int] = ..., total_lidora_count: _Optional[int] = ..., average_hu_point: _Optional[int] = ...) -> None: ...
    class LiQi10Summary(_message.Message):
        __slots__ = ()
        TOTAL_XUANSHANG_FIELD_NUMBER: _ClassVar[int]
        TOTAL_FANSHU_FIELD_NUMBER: _ClassVar[int]
        total_xuanshang: int
        total_fanshu: int
        def __init__(self, total_xuanshang: _Optional[int] = ..., total_fanshu: _Optional[int] = ...) -> None: ...
    class GameResult(_message.Message):
        __slots__ = ()
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
    highest_hu: HighestHuRecord
    recent_20_hu_summary: AccountMahjongStatistic.Liqi20Summary
    recent_10_hu_summary: AccountMahjongStatistic.LiQi10Summary
    recent_10_game_result: _containers.RepeatedCompositeFieldContainer[AccountMahjongStatistic.GameResult]
    def __init__(self, final_position_counts: _Optional[_Iterable[int]] = ..., recent_round: _Optional[_Union[AccountMahjongStatistic.RoundSummary, _Mapping]] = ..., recent_hu: _Optional[_Union[AccountMahjongStatistic.HuSummary, _Mapping]] = ..., highest_hu: _Optional[_Union[HighestHuRecord, _Mapping]] = ..., recent_20_hu_summary: _Optional[_Union[AccountMahjongStatistic.Liqi20Summary, _Mapping]] = ..., recent_10_hu_summary: _Optional[_Union[AccountMahjongStatistic.LiQi10Summary, _Mapping]] = ..., recent_10_game_result: _Optional[_Iterable[_Union[AccountMahjongStatistic.GameResult, _Mapping]]] = ...) -> None: ...

class AccountMailRecord(_message.Message):
    __slots__ = ()
    class MailSnapshot(_message.Message):
        __slots__ = ()
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

class AccountMiscSnapshot(_message.Message):
    __slots__ = ()
    class AccountVIPRewardSnapshot(_message.Message):
        __slots__ = ()
        REWARDED_FIELD_NUMBER: _ClassVar[int]
        rewarded: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, rewarded: _Optional[_Iterable[int]] = ...) -> None: ...
    class MonthTicketInfo(_message.Message):
        __slots__ = ()
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
        __slots__ = ()
        TICKETS_FIELD_NUMBER: _ClassVar[int]
        tickets: _containers.RepeatedCompositeFieldContainer[AccountMiscSnapshot.MonthTicketInfo]
        def __init__(self, tickets: _Optional[_Iterable[_Union[AccountMiscSnapshot.MonthTicketInfo, _Mapping]]] = ...) -> None: ...
    class AccountVIP(_message.Message):
        __slots__ = ()
        VIP_FIELD_NUMBER: _ClassVar[int]
        vip: int
        def __init__(self, vip: _Optional[int] = ...) -> None: ...
    class AccountRechargeInfo(_message.Message):
        __slots__ = ()
        class RechargeRecord(_message.Message):
            __slots__ = ()
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
        __slots__ = ()
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

class AccountOwnerData(_message.Message):
    __slots__ = ()
    UNLOCK_CHARACTERS_FIELD_NUMBER: _ClassVar[int]
    unlock_characters: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, unlock_characters: _Optional[_Iterable[int]] = ...) -> None: ...

class AccountPlayingGame(_message.Message):
    __slots__ = ()
    GAME_UUID_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    META_FIELD_NUMBER: _ClassVar[int]
    game_uuid: str
    category: int
    meta: GameMetaData
    def __init__(self, game_uuid: _Optional[str] = ..., category: _Optional[int] = ..., meta: _Optional[_Union[GameMetaData, _Mapping]] = ...) -> None: ...

class AccountResourceSnapshot(_message.Message):
    __slots__ = ()
    class BagItemSnapshot(_message.Message):
        __slots__ = ()
        RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
        RESOURCE_COUNT_FIELD_NUMBER: _ClassVar[int]
        RESOURCE_VERSION_FIELD_NUMBER: _ClassVar[int]
        resource_id: int
        resource_count: int
        resource_version: int
        def __init__(self, resource_id: _Optional[int] = ..., resource_count: _Optional[int] = ..., resource_version: _Optional[int] = ...) -> None: ...
    class CurrencySnapshot(_message.Message):
        __slots__ = ()
        CURRENCY_ID_FIELD_NUMBER: _ClassVar[int]
        CURRENCY_COUNT_FIELD_NUMBER: _ClassVar[int]
        currency_id: int
        currency_count: int
        def __init__(self, currency_id: _Optional[int] = ..., currency_count: _Optional[int] = ...) -> None: ...
    class TitleSnapshot(_message.Message):
        __slots__ = ()
        TITLE_LIST_FIELD_NUMBER: _ClassVar[int]
        title_list: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, title_list: _Optional[_Iterable[int]] = ...) -> None: ...
    class UsedTitleSnapshot(_message.Message):
        __slots__ = ()
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

class AccountSetting(_message.Message):
    __slots__ = ()
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: int
    value: int
    def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...

class AccountShiLian(_message.Message):
    __slots__ = ()
    STEP_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    step: int
    state: int
    def __init__(self, step: _Optional[int] = ..., state: _Optional[int] = ...) -> None: ...

class AccountStatisticByFan(_message.Message):
    __slots__ = ()
    FAN_ID_FIELD_NUMBER: _ClassVar[int]
    SUM_FIELD_NUMBER: _ClassVar[int]
    fan_id: int
    sum: int
    def __init__(self, fan_id: _Optional[int] = ..., sum: _Optional[int] = ...) -> None: ...

class AccountStatisticByGameMode(_message.Message):
    __slots__ = ()
    class RoundEndData(_message.Message):
        __slots__ = ()
        TYPE_FIELD_NUMBER: _ClassVar[int]
        SUM_FIELD_NUMBER: _ClassVar[int]
        type: int
        sum: int
        def __init__(self, type: _Optional[int] = ..., sum: _Optional[int] = ...) -> None: ...
    class RankScore(_message.Message):
        __slots__ = ()
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

class AccountStatisticData(_message.Message):
    __slots__ = ()
    MAHJONG_CATEGORY_FIELD_NUMBER: _ClassVar[int]
    GAME_CATEGORY_FIELD_NUMBER: _ClassVar[int]
    STATISTIC_FIELD_NUMBER: _ClassVar[int]
    GAME_TYPE_FIELD_NUMBER: _ClassVar[int]
    mahjong_category: int
    game_category: int
    statistic: AccountMahjongStatistic
    game_type: int
    def __init__(self, mahjong_category: _Optional[int] = ..., game_category: _Optional[int] = ..., statistic: _Optional[_Union[AccountMahjongStatistic, _Mapping]] = ..., game_type: _Optional[int] = ...) -> None: ...

class AccountUpdate(_message.Message):
    __slots__ = ()
    class NumericalUpdate(_message.Message):
        __slots__ = ()
        ID_FIELD_NUMBER: _ClassVar[int]
        FINAL_FIELD_NUMBER: _ClassVar[int]
        id: int
        final: int
        def __init__(self, id: _Optional[int] = ..., final: _Optional[int] = ...) -> None: ...
    class CharacterUpdate(_message.Message):
        __slots__ = ()
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
        __slots__ = ()
        PROGRESSES_FIELD_NUMBER: _ClassVar[int]
        REWARDED_GROUP_FIELD_NUMBER: _ClassVar[int]
        progresses: _containers.RepeatedCompositeFieldContainer[AchievementProgress]
        rewarded_group: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, progresses: _Optional[_Iterable[_Union[AchievementProgress, _Mapping]]] = ..., rewarded_group: _Optional[_Iterable[int]] = ...) -> None: ...
    class DailyTaskUpdate(_message.Message):
        __slots__ = ()
        PROGRESSES_FIELD_NUMBER: _ClassVar[int]
        TASK_LIST_FIELD_NUMBER: _ClassVar[int]
        progresses: _containers.RepeatedCompositeFieldContainer[TaskProgress]
        task_list: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, progresses: _Optional[_Iterable[_Union[TaskProgress, _Mapping]]] = ..., task_list: _Optional[_Iterable[int]] = ...) -> None: ...
    class TitleUpdate(_message.Message):
        __slots__ = ()
        NEW_TITLES_FIELD_NUMBER: _ClassVar[int]
        REMOVE_TITLES_FIELD_NUMBER: _ClassVar[int]
        new_titles: _containers.RepeatedScalarFieldContainer[int]
        remove_titles: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, new_titles: _Optional[_Iterable[int]] = ..., remove_titles: _Optional[_Iterable[int]] = ...) -> None: ...
    class TaskUpdate(_message.Message):
        __slots__ = ()
        PROGRESSES_FIELD_NUMBER: _ClassVar[int]
        TASK_LIST_FIELD_NUMBER: _ClassVar[int]
        progresses: _containers.RepeatedCompositeFieldContainer[TaskProgress]
        task_list: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, progresses: _Optional[_Iterable[_Union[TaskProgress, _Mapping]]] = ..., task_list: _Optional[_Iterable[int]] = ...) -> None: ...
    class AccountChallengeUpdate(_message.Message):
        __slots__ = ()
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
        __slots__ = ()
        class MatchPoint(_message.Message):
            __slots__ = ()
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
        def __init__(self, match_id: _Optional[int] = ..., match_count: _Optional[int] = ..., buy_in_count: _Optional[int] = ..., point: _Optional[int] = ..., rewarded: _Optional[bool] = ..., match_max_point: _Optional[_Iterable[_Union[AccountUpdate.AccountABMatchUpdate.MatchPoint, _Mapping]]] = ..., quit: _Optional[bool] = ...) -> None: ...
    class SegmentTaskUpdate(_message.Message):
        __slots__ = ()
        PROGRESSES_FIELD_NUMBER: _ClassVar[int]
        TASK_LIST_FIELD_NUMBER: _ClassVar[int]
        progresses: _containers.RepeatedCompositeFieldContainer[SegmentTaskProgress]
        task_list: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, progresses: _Optional[_Iterable[_Union[SegmentTaskProgress, _Mapping]]] = ..., task_list: _Optional[_Iterable[int]] = ...) -> None: ...
    class MonthTicketUpdate(_message.Message):
        __slots__ = ()
        END_TIME_FIELD_NUMBER: _ClassVar[int]
        LAST_PAY_TIME_FIELD_NUMBER: _ClassVar[int]
        end_time: int
        last_pay_time: int
        def __init__(self, end_time: _Optional[int] = ..., last_pay_time: _Optional[int] = ...) -> None: ...
    class MainCharacterUpdate(_message.Message):
        __slots__ = ()
        CHARACTER_ID_FIELD_NUMBER: _ClassVar[int]
        SKIN_ID_FIELD_NUMBER: _ClassVar[int]
        character_id: int
        skin_id: int
        def __init__(self, character_id: _Optional[int] = ..., skin_id: _Optional[int] = ...) -> None: ...
    class BadgeUpdate(_message.Message):
        __slots__ = ()
        PROGRESSES_FIELD_NUMBER: _ClassVar[int]
        progresses: _containers.RepeatedCompositeFieldContainer[BadgeAchieveProgress]
        def __init__(self, progresses: _Optional[_Iterable[_Union[BadgeAchieveProgress, _Mapping]]] = ...) -> None: ...
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
    MAIN_CHARACTER_FIELD_NUMBER: _ClassVar[int]
    BADGE_FIELD_NUMBER: _ClassVar[int]
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
    main_character: AccountUpdate.MainCharacterUpdate
    badge: AccountUpdate.BadgeUpdate
    def __init__(self, numerical: _Optional[_Iterable[_Union[AccountUpdate.NumericalUpdate, _Mapping]]] = ..., character: _Optional[_Union[AccountUpdate.CharacterUpdate, _Mapping]] = ..., bag: _Optional[_Union[BagUpdate, _Mapping]] = ..., achievement: _Optional[_Union[AccountUpdate.AchievementUpdate, _Mapping]] = ..., shilian: _Optional[_Union[AccountShiLian, _Mapping]] = ..., daily_task: _Optional[_Union[AccountUpdate.DailyTaskUpdate, _Mapping]] = ..., title: _Optional[_Union[AccountUpdate.TitleUpdate, _Mapping]] = ..., new_recharged_list: _Optional[_Iterable[int]] = ..., activity_task: _Optional[_Union[AccountUpdate.TaskUpdate, _Mapping]] = ..., activity_flip_task: _Optional[_Union[AccountUpdate.TaskUpdate, _Mapping]] = ..., activity_period_task: _Optional[_Union[AccountUpdate.TaskUpdate, _Mapping]] = ..., activity_random_task: _Optional[_Union[AccountUpdate.TaskUpdate, _Mapping]] = ..., challenge: _Optional[_Union[AccountUpdate.AccountChallengeUpdate, _Mapping]] = ..., ab_match: _Optional[_Union[AccountUpdate.AccountABMatchUpdate, _Mapping]] = ..., activity: _Optional[_Union[AccountActivityUpdate, _Mapping]] = ..., activity_segment_task: _Optional[_Union[AccountUpdate.SegmentTaskUpdate, _Mapping]] = ..., month_ticket: _Optional[_Union[AccountUpdate.MonthTicketUpdate, _Mapping]] = ..., main_character: _Optional[_Union[AccountUpdate.MainCharacterUpdate, _Mapping]] = ..., badge: _Optional[_Union[AccountUpdate.BadgeUpdate, _Mapping]] = ...) -> None: ...

class AchievementProgress(_message.Message):
    __slots__ = ()
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
    def __init__(self, id: _Optional[int] = ..., counter: _Optional[int] = ..., achieved: _Optional[bool] = ..., rewarded: _Optional[bool] = ..., achieved_time: _Optional[int] = ...) -> None: ...

class ActionAnGangAddGang(_message.Message):
    __slots__ = ()
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
    def __init__(self, seat: _Optional[int] = ..., type: _Optional[int] = ..., tiles: _Optional[str] = ..., operation: _Optional[_Union[OptionalOperationList, _Mapping]] = ..., doras: _Optional[_Iterable[str]] = ..., zhenting: _Optional[bool] = ..., tingpais: _Optional[_Iterable[_Union[TingPaiInfo, _Mapping]]] = ..., muyu: _Optional[_Union[MuyuInfo, _Mapping]] = ...) -> None: ...

class ActionBaBei(_message.Message):
    __slots__ = ()
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
    def __init__(self, seat: _Optional[int] = ..., operation: _Optional[_Union[OptionalOperationList, _Mapping]] = ..., doras: _Optional[_Iterable[str]] = ..., zhenting: _Optional[bool] = ..., tingpais: _Optional[_Iterable[_Union[TingPaiInfo, _Mapping]]] = ..., moqie: _Optional[bool] = ..., tile_state: _Optional[int] = ..., muyu: _Optional[_Union[MuyuInfo, _Mapping]] = ...) -> None: ...

class ActionChangeTile(_message.Message):
    __slots__ = ()
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

class ActionChiPengGang(_message.Message):
    __slots__ = ()
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
    def __init__(self, seat: _Optional[int] = ..., type: _Optional[int] = ..., tiles: _Optional[_Iterable[str]] = ..., froms: _Optional[_Iterable[int]] = ..., liqi: _Optional[_Union[LiQiSuccess, _Mapping]] = ..., operation: _Optional[_Union[OptionalOperationList, _Mapping]] = ..., zhenting: _Optional[bool] = ..., tingpais: _Optional[_Iterable[_Union[TingPaiDiscardInfo, _Mapping]]] = ..., tile_states: _Optional[_Iterable[int]] = ..., muyu: _Optional[_Union[MuyuInfo, _Mapping]] = ..., scores: _Optional[_Iterable[int]] = ..., liqibang: _Optional[int] = ..., yongchang: _Optional[_Union[YongchangInfo, _Mapping]] = ..., hun_zhi_yi_ji_info: _Optional[_Union[HunZhiYiJiBuffInfo, _Mapping]] = ...) -> None: ...

class ActionDealTile(_message.Message):
    __slots__ = ()
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
    def __init__(self, seat: _Optional[int] = ..., tile: _Optional[str] = ..., left_tile_count: _Optional[int] = ..., operation: _Optional[_Union[OptionalOperationList, _Mapping]] = ..., liqi: _Optional[_Union[LiQiSuccess, _Mapping]] = ..., doras: _Optional[_Iterable[str]] = ..., zhenting: _Optional[bool] = ..., tingpais: _Optional[_Iterable[_Union[TingPaiDiscardInfo, _Mapping]]] = ..., tile_state: _Optional[int] = ..., muyu: _Optional[_Union[MuyuInfo, _Mapping]] = ..., tile_index: _Optional[int] = ..., hun_zhi_yi_ji_info: _Optional[_Union[HunZhiYiJiBuffInfo, _Mapping]] = ...) -> None: ...

class ActionDiscardTile(_message.Message):
    __slots__ = ()
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
    LIQI_TYPE_BEISHUIZHIZHAN_FIELD_NUMBER: _ClassVar[int]
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
    liqi_type_beishuizhizhan: int
    def __init__(self, seat: _Optional[int] = ..., tile: _Optional[str] = ..., is_liqi: _Optional[bool] = ..., operation: _Optional[_Union[OptionalOperationList, _Mapping]] = ..., moqie: _Optional[bool] = ..., zhenting: _Optional[bool] = ..., tingpais: _Optional[_Iterable[_Union[TingPaiInfo, _Mapping]]] = ..., doras: _Optional[_Iterable[str]] = ..., is_wliqi: _Optional[bool] = ..., tile_state: _Optional[int] = ..., muyu: _Optional[_Union[MuyuInfo, _Mapping]] = ..., revealed: _Optional[bool] = ..., scores: _Optional[_Iterable[int]] = ..., liqibang: _Optional[int] = ..., yongchang: _Optional[_Union[YongchangInfo, _Mapping]] = ..., hun_zhi_yi_ji_info: _Optional[_Union[HunZhiYiJiBuffInfo, _Mapping]] = ..., liqi_type_beishuizhizhan: _Optional[int] = ...) -> None: ...

class ActionFillAwaitingTiles(_message.Message):
    __slots__ = ()
    AWAITING_TILES_FIELD_NUMBER: _ClassVar[int]
    LEFT_TILE_COUNT_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    LIQI_FIELD_NUMBER: _ClassVar[int]
    awaiting_tiles: _containers.RepeatedScalarFieldContainer[str]
    left_tile_count: int
    operation: OptionalOperationList
    liqi: LiQiSuccess
    def __init__(self, awaiting_tiles: _Optional[_Iterable[str]] = ..., left_tile_count: _Optional[int] = ..., operation: _Optional[_Union[OptionalOperationList, _Mapping]] = ..., liqi: _Optional[_Union[LiQiSuccess, _Mapping]] = ...) -> None: ...

class ActionGangResult(_message.Message):
    __slots__ = ()
    GANG_INFOS_FIELD_NUMBER: _ClassVar[int]
    gang_infos: ChuanmaGang
    def __init__(self, gang_infos: _Optional[_Union[ChuanmaGang, _Mapping]] = ...) -> None: ...

class ActionGangResultEnd(_message.Message):
    __slots__ = ()
    GANG_INFOS_FIELD_NUMBER: _ClassVar[int]
    gang_infos: ChuanmaGang
    def __init__(self, gang_infos: _Optional[_Union[ChuanmaGang, _Mapping]] = ...) -> None: ...

class ActionHule(_message.Message):
    __slots__ = ()
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

class ActionHuleXueZhanEnd(_message.Message):
    __slots__ = ()
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

class ActionHuleXueZhanMid(_message.Message):
    __slots__ = ()
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
    def __init__(self, hules: _Optional[_Iterable[_Union[HuInfoXueZhanMid, _Mapping]]] = ..., old_scores: _Optional[_Iterable[int]] = ..., delta_scores: _Optional[_Iterable[int]] = ..., scores: _Optional[_Iterable[int]] = ..., doras: _Optional[_Iterable[str]] = ..., muyu: _Optional[_Union[MuyuInfo, _Mapping]] = ..., liqi: _Optional[_Union[LiQiSuccess, _Mapping]] = ..., zhenting: _Optional[bool] = ...) -> None: ...

class ActionLiuJu(_message.Message):
    __slots__ = ()
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

class ActionLockTile(_message.Message):
    __slots__ = ()
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
    def __init__(self, seat: _Optional[int] = ..., scores: _Optional[_Iterable[int]] = ..., liqibang: _Optional[int] = ..., tile: _Optional[str] = ..., operation: _Optional[_Union[OptionalOperationList, _Mapping]] = ..., zhenting: _Optional[bool] = ..., tingpais: _Optional[_Iterable[_Union[TingPaiInfo, _Mapping]]] = ..., doras: _Optional[_Iterable[str]] = ..., lock_state: _Optional[int] = ...) -> None: ...

class ActionMJStart(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ActionNewCard(_message.Message):
    __slots__ = ()
    FIELD_SPELL_FIELD_NUMBER: _ClassVar[int]
    field_spell: int
    def __init__(self, field_spell: _Optional[int] = ...) -> None: ...

class ActionNewRound(_message.Message):
    __slots__ = ()
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
    XIA_KE_SHANG_FIELD_NUMBER: _ClassVar[int]
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
    xia_ke_shang: XiaKeShangInfo
    def __init__(self, chang: _Optional[int] = ..., ju: _Optional[int] = ..., ben: _Optional[int] = ..., tiles: _Optional[_Iterable[str]] = ..., dora: _Optional[str] = ..., scores: _Optional[_Iterable[int]] = ..., operation: _Optional[_Union[OptionalOperationList, _Mapping]] = ..., liqibang: _Optional[int] = ..., tingpais0: _Optional[_Iterable[_Union[TingPaiDiscardInfo, _Mapping]]] = ..., tingpais1: _Optional[_Iterable[_Union[TingPaiInfo, _Mapping]]] = ..., al: _Optional[bool] = ..., md5: _Optional[str] = ..., left_tile_count: _Optional[int] = ..., doras: _Optional[_Iterable[str]] = ..., opens: _Optional[_Iterable[_Union[NewRoundOpenedTiles, _Mapping]]] = ..., muyu: _Optional[_Union[MuyuInfo, _Mapping]] = ..., ju_count: _Optional[int] = ..., field_spell: _Optional[int] = ..., sha256: _Optional[str] = ..., yongchang: _Optional[_Union[YongchangInfo, _Mapping]] = ..., saltSha256: _Optional[str] = ..., xia_ke_shang: _Optional[_Union[XiaKeShangInfo, _Mapping]] = ...) -> None: ...

class ActionNoTile(_message.Message):
    __slots__ = ()
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
    def __init__(self, liujumanguan: _Optional[bool] = ..., players: _Optional[_Iterable[_Union[NoTilePlayerInfo, _Mapping]]] = ..., scores: _Optional[_Iterable[_Union[NoTileScoreInfo, _Mapping]]] = ..., gameend: _Optional[bool] = ..., muyu: _Optional[_Union[MuyuInfo, _Mapping]] = ..., hules_history: _Optional[_Iterable[_Union[HuleInfo, _Mapping]]] = ...) -> None: ...

class ActionPrototype(_message.Message):
    __slots__ = ()
    STEP_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    step: int
    name: str
    data: bytes
    def __init__(self, step: _Optional[int] = ..., name: _Optional[str] = ..., data: _Optional[bytes] = ...) -> None: ...

class ActionRevealTile(_message.Message):
    __slots__ = ()
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
    def __init__(self, seat: _Optional[int] = ..., is_liqi: _Optional[bool] = ..., is_wliqi: _Optional[bool] = ..., moqie: _Optional[bool] = ..., scores: _Optional[_Iterable[int]] = ..., liqibang: _Optional[int] = ..., operation: _Optional[_Union[OptionalOperationList, _Mapping]] = ..., tingpais: _Optional[_Iterable[_Union[TingPaiInfo, _Mapping]]] = ..., tile: _Optional[str] = ..., zhenting: _Optional[bool] = ...) -> None: ...

class ActionSelectGap(_message.Message):
    __slots__ = ()
    GAP_TYPES_FIELD_NUMBER: _ClassVar[int]
    TINGPAIS0_FIELD_NUMBER: _ClassVar[int]
    TINGPAIS1_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    gap_types: _containers.RepeatedScalarFieldContainer[int]
    tingpais0: _containers.RepeatedCompositeFieldContainer[TingPaiDiscardInfo]
    tingpais1: _containers.RepeatedCompositeFieldContainer[TingPaiInfo]
    operation: OptionalOperationList
    def __init__(self, gap_types: _Optional[_Iterable[int]] = ..., tingpais0: _Optional[_Iterable[_Union[TingPaiDiscardInfo, _Mapping]]] = ..., tingpais1: _Optional[_Iterable[_Union[TingPaiInfo, _Mapping]]] = ..., operation: _Optional[_Union[OptionalOperationList, _Mapping]] = ...) -> None: ...

class ActionUnveilTile(_message.Message):
    __slots__ = ()
    SEAT_FIELD_NUMBER: _ClassVar[int]
    SCORES_FIELD_NUMBER: _ClassVar[int]
    LIQIBANG_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    seat: int
    scores: _containers.RepeatedScalarFieldContainer[int]
    liqibang: int
    operation: OptionalOperationList
    def __init__(self, seat: _Optional[int] = ..., scores: _Optional[_Iterable[int]] = ..., liqibang: _Optional[int] = ..., operation: _Optional[_Union[OptionalOperationList, _Mapping]] = ...) -> None: ...

class Activity(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    start_time: int
    end_time: int
    type: str
    def __init__(self, activity_id: _Optional[int] = ..., start_time: _Optional[int] = ..., end_time: _Optional[int] = ..., type: _Optional[str] = ...) -> None: ...

class ActivityAccumulatedPointData(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    POINT_FIELD_NUMBER: _ClassVar[int]
    GAINED_REWARD_LIST_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    point: int
    gained_reward_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, activity_id: _Optional[int] = ..., point: _Optional[int] = ..., gained_reward_list: _Optional[_Iterable[int]] = ...) -> None: ...

class ActivityAmuletData(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    GAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    UPGRADE_FIELD_NUMBER: _ClassVar[int]
    ILLUSTRATED_BOOK_FIELD_NUMBER: _ClassVar[int]
    BOOK_EFFECT_ID_FIELD_NUMBER: _ClassVar[int]
    GAME_RECORDS_FIELD_NUMBER: _ClassVar[int]
    STATISTIC_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    game: AmuletGameData
    version: int
    upgrade: ActivityAmuletUpgradeData
    illustrated_book: ActivityAmuletIllustratedBookData
    book_effect_id: int
    game_records: _containers.RepeatedCompositeFieldContainer[ActivityAmuletGameRecordData]
    statistic: ActivityAmuletStatisticData
    def __init__(self, activity_id: _Optional[int] = ..., game: _Optional[_Union[AmuletGameData, _Mapping]] = ..., version: _Optional[int] = ..., upgrade: _Optional[_Union[ActivityAmuletUpgradeData, _Mapping]] = ..., illustrated_book: _Optional[_Union[ActivityAmuletIllustratedBookData, _Mapping]] = ..., book_effect_id: _Optional[int] = ..., game_records: _Optional[_Iterable[_Union[ActivityAmuletGameRecordData, _Mapping]]] = ..., statistic: _Optional[_Union[ActivityAmuletStatisticData, _Mapping]] = ...) -> None: ...

class ActivityAmuletEffectRecordData(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    BADGE_ID_FIELD_NUMBER: _ClassVar[int]
    VOLUME_FIELD_NUMBER: _ClassVar[int]
    id: int
    badge_id: int
    volume: int
    def __init__(self, id: _Optional[int] = ..., badge_id: _Optional[int] = ..., volume: _Optional[int] = ...) -> None: ...

class ActivityAmuletGameRecordData(_message.Message):
    __slots__ = ()
    EFFECT_BUILDS_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    HIGHEST_LEVEL_SCORE_FIELD_NUMBER: _ClassVar[int]
    HIGHEST_FAN_FIELD_NUMBER: _ClassVar[int]
    HIGHEST_SCORE_FIELD_NUMBER: _ClassVar[int]
    COIN_CONSUMED_FIELD_NUMBER: _ClassVar[int]
    PACK_COUNT_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    HIGHEST_HU_FIELD_NUMBER: _ClassVar[int]
    effect_builds: _containers.RepeatedCompositeFieldContainer[ActivityAmuletEffectRecordData]
    level: int
    highest_level_score: str
    highest_fan: str
    highest_score: str
    coin_consumed: str
    pack_count: int
    time: int
    highest_hu: ActivityAmuletHuRecord
    def __init__(self, effect_builds: _Optional[_Iterable[_Union[ActivityAmuletEffectRecordData, _Mapping]]] = ..., level: _Optional[int] = ..., highest_level_score: _Optional[str] = ..., highest_fan: _Optional[str] = ..., highest_score: _Optional[str] = ..., coin_consumed: _Optional[str] = ..., pack_count: _Optional[int] = ..., time: _Optional[int] = ..., highest_hu: _Optional[_Union[ActivityAmuletHuRecord, _Mapping]] = ...) -> None: ...

class ActivityAmuletHuRecord(_message.Message):
    __slots__ = ()
    POINT_FIELD_NUMBER: _ClassVar[int]
    PAI_FIELD_NUMBER: _ClassVar[int]
    FAN_FIELD_NUMBER: _ClassVar[int]
    BASE_FIELD_NUMBER: _ClassVar[int]
    EFFECT_BUILDS_FIELD_NUMBER: _ClassVar[int]
    point: str
    pai: str
    fan: str
    base: str
    effect_builds: _containers.RepeatedCompositeFieldContainer[ActivityAmuletEffectRecordData]
    def __init__(self, point: _Optional[str] = ..., pai: _Optional[str] = ..., fan: _Optional[str] = ..., base: _Optional[str] = ..., effect_builds: _Optional[_Iterable[_Union[ActivityAmuletEffectRecordData, _Mapping]]] = ...) -> None: ...

class ActivityAmuletHuRecordDirty(_message.Message):
    __slots__ = ()
    DIRTY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    dirty: bool
    value: ActivityAmuletHuRecord
    def __init__(self, dirty: _Optional[bool] = ..., value: _Optional[_Union[ActivityAmuletHuRecord, _Mapping]] = ...) -> None: ...

class ActivityAmuletIllustratedBookData(_message.Message):
    __slots__ = ()
    EFFECT_COLLECTION_FIELD_NUMBER: _ClassVar[int]
    BADGE_COLLECTION_FIELD_NUMBER: _ClassVar[int]
    effect_collection: _containers.RepeatedScalarFieldContainer[int]
    badge_collection: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, effect_collection: _Optional[_Iterable[int]] = ..., badge_collection: _Optional[_Iterable[int]] = ...) -> None: ...

class ActivityAmuletStatisticData(_message.Message):
    __slots__ = ()
    HIGHEST_LEVEL_FIELD_NUMBER: _ClassVar[int]
    HIGHEST_HU_FIELD_NUMBER: _ClassVar[int]
    HIGHEST_LEVEL_SCORE_FIELD_NUMBER: _ClassVar[int]
    HIGHEST_FAN_FIELD_NUMBER: _ClassVar[int]
    HIGHEST_SCORE_FIELD_NUMBER: _ClassVar[int]
    PASS_GAME_COUNT_FIELD_NUMBER: _ClassVar[int]
    ROUND_COUNT_FIELD_NUMBER: _ClassVar[int]
    OPEN_PACK_COUNT_FIELD_NUMBER: _ClassVar[int]
    HIGHEST_COIN_CONSUMED_FIELD_NUMBER: _ClassVar[int]
    highest_level: int
    highest_hu: ActivityAmuletHuRecord
    highest_level_score: str
    highest_fan: str
    highest_score: str
    pass_game_count: int
    round_count: int
    open_pack_count: int
    highest_coin_consumed: str
    def __init__(self, highest_level: _Optional[int] = ..., highest_hu: _Optional[_Union[ActivityAmuletHuRecord, _Mapping]] = ..., highest_level_score: _Optional[str] = ..., highest_fan: _Optional[str] = ..., highest_score: _Optional[str] = ..., pass_game_count: _Optional[int] = ..., round_count: _Optional[int] = ..., open_pack_count: _Optional[int] = ..., highest_coin_consumed: _Optional[str] = ...) -> None: ...

class ActivityAmuletUpgradeData(_message.Message):
    __slots__ = ()
    SKILL_FIELD_NUMBER: _ClassVar[int]
    skill: _containers.RepeatedCompositeFieldContainer[AmuletSkillData]
    def __init__(self, skill: _Optional[_Iterable[_Union[AmuletSkillData, _Mapping]]] = ...) -> None: ...

class ActivityArenaData(_message.Message):
    __slots__ = ()
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

class ActivityBingoCardData(_message.Message):
    __slots__ = ()
    class BingoAchievedRecord(_message.Message):
        __slots__ = ()
        POS_FIELD_NUMBER: _ClassVar[int]
        TIME_FIELD_NUMBER: _ClassVar[int]
        pos: int
        time: int
        def __init__(self, pos: _Optional[int] = ..., time: _Optional[int] = ...) -> None: ...
    class BingoRewardRecord(_message.Message):
        __slots__ = ()
        ID_FIELD_NUMBER: _ClassVar[int]
        TIME_FIELD_NUMBER: _ClassVar[int]
        id: int
        time: int
        def __init__(self, id: _Optional[int] = ..., time: _Optional[int] = ...) -> None: ...
    CARD_ID_FIELD_NUMBER: _ClassVar[int]
    ACHIEVED_POS_FIELD_NUMBER: _ClassVar[int]
    REWARDED_IDS_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    ACHIEVED_RECORDS_FIELD_NUMBER: _ClassVar[int]
    REWARD_RECORDS_FIELD_NUMBER: _ClassVar[int]
    card_id: int
    achieved_pos: _containers.RepeatedScalarFieldContainer[int]
    rewarded_ids: _containers.RepeatedScalarFieldContainer[int]
    state: int
    achieved_records: _containers.RepeatedCompositeFieldContainer[ActivityBingoCardData.BingoAchievedRecord]
    reward_records: _containers.RepeatedCompositeFieldContainer[ActivityBingoCardData.BingoRewardRecord]
    def __init__(self, card_id: _Optional[int] = ..., achieved_pos: _Optional[_Iterable[int]] = ..., rewarded_ids: _Optional[_Iterable[int]] = ..., state: _Optional[int] = ..., achieved_records: _Optional[_Iterable[_Union[ActivityBingoCardData.BingoAchievedRecord, _Mapping]]] = ..., reward_records: _Optional[_Iterable[_Union[ActivityBingoCardData.BingoRewardRecord, _Mapping]]] = ...) -> None: ...

class ActivityBingoData(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    CARDS_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    cards: _containers.RepeatedCompositeFieldContainer[ActivityBingoCardData]
    def __init__(self, activity_id: _Optional[int] = ..., cards: _Optional[_Iterable[_Union[ActivityBingoCardData, _Mapping]]] = ...) -> None: ...

class ActivityBuffData(_message.Message):
    __slots__ = ()
    BUFF_ID_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    buff_id: int
    level: int
    count: int
    update_time: int
    def __init__(self, buff_id: _Optional[int] = ..., level: _Optional[int] = ..., count: _Optional[int] = ..., update_time: _Optional[int] = ...) -> None: ...

class ActivityChooseUpData(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    CHEST_ID_FIELD_NUMBER: _ClassVar[int]
    SELECTION_FIELD_NUMBER: _ClassVar[int]
    IS_END_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    chest_id: int
    selection: int
    is_end: int
    def __init__(self, activity_id: _Optional[int] = ..., chest_id: _Optional[int] = ..., selection: _Optional[int] = ..., is_end: _Optional[int] = ...) -> None: ...

class ActivityCombiningData(_message.Message):
    __slots__ = ()
    class BonusData(_message.Message):
        __slots__ = ()
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

class ActivityCombiningLQData(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    WORKBENCH_FIELD_NUMBER: _ClassVar[int]
    ORDERS_FIELD_NUMBER: _ClassVar[int]
    RECYCLE_BIN_FIELD_NUMBER: _ClassVar[int]
    UNLOCKED_CRAFT_FIELD_NUMBER: _ClassVar[int]
    DAILY_BONUS_COUNT_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    workbench: _containers.RepeatedCompositeFieldContainer[ActivityCombiningWorkbench]
    orders: _containers.RepeatedCompositeFieldContainer[ActivityCombiningOrderData]
    recycle_bin: ActivityCombiningWorkbench
    unlocked_craft: _containers.RepeatedScalarFieldContainer[int]
    daily_bonus_count: int
    def __init__(self, activity_id: _Optional[int] = ..., workbench: _Optional[_Iterable[_Union[ActivityCombiningWorkbench, _Mapping]]] = ..., orders: _Optional[_Iterable[_Union[ActivityCombiningOrderData, _Mapping]]] = ..., recycle_bin: _Optional[_Union[ActivityCombiningWorkbench, _Mapping]] = ..., unlocked_craft: _Optional[_Iterable[int]] = ..., daily_bonus_count: _Optional[int] = ...) -> None: ...

class ActivityCombiningMenuData(_message.Message):
    __slots__ = ()
    class MenuRequire(_message.Message):
        __slots__ = ()
        LEVEL_FIELD_NUMBER: _ClassVar[int]
        COUNT_FIELD_NUMBER: _ClassVar[int]
        level: int
        count: int
        def __init__(self, level: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...
    MENU_GROUP_FIELD_NUMBER: _ClassVar[int]
    GENERATED_FIELD_NUMBER: _ClassVar[int]
    MULTI_GENERATED_FIELD_NUMBER: _ClassVar[int]
    menu_group: int
    generated: _containers.RepeatedCompositeFieldContainer[ActivityCombiningMenuData.MenuRequire]
    multi_generated: _containers.RepeatedCompositeFieldContainer[ActivityCombiningMenuData.MenuRequire]
    def __init__(self, menu_group: _Optional[int] = ..., generated: _Optional[_Iterable[_Union[ActivityCombiningMenuData.MenuRequire, _Mapping]]] = ..., multi_generated: _Optional[_Iterable[_Union[ActivityCombiningMenuData.MenuRequire, _Mapping]]] = ...) -> None: ...

class ActivityCombiningOrderData(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    POS_FIELD_NUMBER: _ClassVar[int]
    UNLOCK_DAY_FIELD_NUMBER: _ClassVar[int]
    CHAR_ID_FIELD_NUMBER: _ClassVar[int]
    FINISHED_CRAFT_ID_FIELD_NUMBER: _ClassVar[int]
    CRAFT_ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    pos: int
    unlock_day: int
    char_id: int
    finished_craft_id: _containers.RepeatedScalarFieldContainer[int]
    craft_id: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, id: _Optional[int] = ..., pos: _Optional[int] = ..., unlock_day: _Optional[int] = ..., char_id: _Optional[int] = ..., finished_craft_id: _Optional[_Iterable[int]] = ..., craft_id: _Optional[_Iterable[int]] = ...) -> None: ...

class ActivityCombiningPoolData(_message.Message):
    __slots__ = ()
    GROUP_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    group: int
    count: int
    def __init__(self, group: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class ActivityCombiningWorkbench(_message.Message):
    __slots__ = ()
    CRAFT_ID_FIELD_NUMBER: _ClassVar[int]
    POS_FIELD_NUMBER: _ClassVar[int]
    craft_id: int
    pos: int
    def __init__(self, craft_id: _Optional[int] = ..., pos: _Optional[int] = ...) -> None: ...

class ActivityFeedData(_message.Message):
    __slots__ = ()
    class CountWithTimeData(_message.Message):
        __slots__ = ()
        COUNT_FIELD_NUMBER: _ClassVar[int]
        LAST_UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
        count: int
        last_update_time: int
        def __init__(self, count: _Optional[int] = ..., last_update_time: _Optional[int] = ...) -> None: ...
    class GiftBoxData(_message.Message):
        __slots__ = ()
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

class ActivityFestivalData(_message.Message):
    __slots__ = ()
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

class ActivityFriendGiftData(_message.Message):
    __slots__ = ()
    class CountWithTimeData(_message.Message):
        __slots__ = ()
        COUNT_FIELD_NUMBER: _ClassVar[int]
        LAST_UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
        SEND_FRIEND_ID_FIELD_NUMBER: _ClassVar[int]
        count: int
        last_update_time: int
        send_friend_id: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, count: _Optional[int] = ..., last_update_time: _Optional[int] = ..., send_friend_id: _Optional[_Iterable[int]] = ...) -> None: ...
    class GiftBoxData(_message.Message):
        __slots__ = ()
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

class ActivityGachaData(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    GAINED_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    gained: _containers.RepeatedCompositeFieldContainer[GachaRecord]
    def __init__(self, activity_id: _Optional[int] = ..., gained: _Optional[_Iterable[_Union[GachaRecord, _Mapping]]] = ...) -> None: ...

class ActivityGachaUpdateData(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    GAINED_FIELD_NUMBER: _ClassVar[int]
    REMAIN_COUNT_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    gained: _containers.RepeatedCompositeFieldContainer[GachaRecord]
    remain_count: int
    def __init__(self, activity_id: _Optional[int] = ..., gained: _Optional[_Iterable[_Union[GachaRecord, _Mapping]]] = ..., remain_count: _Optional[int] = ...) -> None: ...

class ActivityIslandData(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    ZONE_FIELD_NUMBER: _ClassVar[int]
    BAGS_FIELD_NUMBER: _ClassVar[int]
    ZONES_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    zone: int
    bags: _containers.RepeatedCompositeFieldContainer[IslandBagData]
    zones: _containers.RepeatedCompositeFieldContainer[IslandZoneData]
    def __init__(self, activity_id: _Optional[int] = ..., zone: _Optional[int] = ..., bags: _Optional[_Iterable[_Union[IslandBagData, _Mapping]]] = ..., zones: _Optional[_Iterable[_Union[IslandZoneData, _Mapping]]] = ...) -> None: ...

class ActivityProgressRewardData(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    REWARDED_PROGRESSES_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    rewarded_progresses: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, activity_id: _Optional[int] = ..., rewarded_progresses: _Optional[_Iterable[int]] = ...) -> None: ...

class ActivityQuestCrewChanges(_message.Message):
    __slots__ = ()
    class QCMemberArrayDirty(_message.Message):
        __slots__ = ()
        DIRTY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        dirty: bool
        value: _containers.RepeatedCompositeFieldContainer[QCMember]
        def __init__(self, dirty: _Optional[bool] = ..., value: _Optional[_Iterable[_Union[QCMember, _Mapping]]] = ...) -> None: ...
    class QCQuestArrayDirty(_message.Message):
        __slots__ = ()
        DIRTY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        dirty: bool
        value: _containers.RepeatedCompositeFieldContainer[QCQuest]
        def __init__(self, dirty: _Optional[bool] = ..., value: _Optional[_Iterable[_Union[QCQuest, _Mapping]]] = ...) -> None: ...
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    QUEST_BOARD_FIELD_NUMBER: _ClassVar[int]
    MARKET_BOARD_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    members: ActivityQuestCrewChanges.QCMemberArrayDirty
    quest_board: ActivityQuestCrewChanges.QCQuestArrayDirty
    market_board: UInt32ArrayDirty
    def __init__(self, activity_id: _Optional[int] = ..., members: _Optional[_Union[ActivityQuestCrewChanges.QCMemberArrayDirty, _Mapping]] = ..., quest_board: _Optional[_Union[ActivityQuestCrewChanges.QCQuestArrayDirty, _Mapping]] = ..., market_board: _Optional[_Union[UInt32ArrayDirty, _Mapping]] = ...) -> None: ...

class ActivityQuestCrewData(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    QUEST_BOARD_FIELD_NUMBER: _ClassVar[int]
    MARKET_BOARD_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    members: _containers.RepeatedCompositeFieldContainer[QCMember]
    quest_board: _containers.RepeatedCompositeFieldContainer[QCQuest]
    market_board: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, activity_id: _Optional[int] = ..., members: _Optional[_Iterable[_Union[QCMember, _Mapping]]] = ..., quest_board: _Optional[_Iterable[_Union[QCQuest, _Mapping]]] = ..., market_board: _Optional[_Iterable[int]] = ...) -> None: ...

class ActivityQuestCrewEffectResult(_message.Message):
    __slots__ = ()
    class QCQuestResultChange(_message.Message):
        __slots__ = ()
        FROM_FIELD_NUMBER: _ClassVar[int]
        TO_FIELD_NUMBER: _ClassVar[int]
        to: int
        def __init__(self, to: _Optional[int] = ..., **kwargs) -> None: ...
    class QCQuestConsumeChange(_message.Message):
        __slots__ = ()
        MEMBER_ID_FIELD_NUMBER: _ClassVar[int]
        FROM_FIELD_NUMBER: _ClassVar[int]
        TO_FIELD_NUMBER: _ClassVar[int]
        member_id: int
        to: int
        def __init__(self, member_id: _Optional[int] = ..., to: _Optional[int] = ..., **kwargs) -> None: ...
    class QCItemReward(_message.Message):
        __slots__ = ()
        EXECUTE_REWARD_FIELD_NUMBER: _ClassVar[int]
        execute_reward: _containers.RepeatedCompositeFieldContainer[ExecuteReward]
        def __init__(self, execute_reward: _Optional[_Iterable[_Union[ExecuteReward, _Mapping]]] = ...) -> None: ...
    RESULT_CHANGE_FIELD_NUMBER: _ClassVar[int]
    CONSUMED_CHANGE_FIELD_NUMBER: _ClassVar[int]
    REWARD_FIELD_NUMBER: _ClassVar[int]
    result_change: ActivityQuestCrewEffectResult.QCQuestResultChange
    consumed_change: _containers.RepeatedCompositeFieldContainer[ActivityQuestCrewEffectResult.QCQuestConsumeChange]
    reward: ActivityQuestCrewEffectResult.QCItemReward
    def __init__(self, result_change: _Optional[_Union[ActivityQuestCrewEffectResult.QCQuestResultChange, _Mapping]] = ..., consumed_change: _Optional[_Iterable[_Union[ActivityQuestCrewEffectResult.QCQuestConsumeChange, _Mapping]]] = ..., reward: _Optional[_Union[ActivityQuestCrewEffectResult.QCItemReward, _Mapping]] = ...) -> None: ...

class ActivityRankPointData(_message.Message):
    __slots__ = ()
    LEADERBOARD_ID_FIELD_NUMBER: _ClassVar[int]
    POINT_FIELD_NUMBER: _ClassVar[int]
    GAINED_REWARD_FIELD_NUMBER: _ClassVar[int]
    GAINABLE_TIME_FIELD_NUMBER: _ClassVar[int]
    leaderboard_id: int
    point: int
    gained_reward: bool
    gainable_time: int
    def __init__(self, leaderboard_id: _Optional[int] = ..., point: _Optional[int] = ..., gained_reward: _Optional[bool] = ..., gainable_time: _Optional[int] = ...) -> None: ...

class ActivityShootData(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    ENEMIES_FIELD_NUMBER: _ClassVar[int]
    REWARDED_IDS_FIELD_NUMBER: _ClassVar[int]
    ENDED_FIELD_NUMBER: _ClassVar[int]
    REWARDED_RECORDS_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    level: int
    enemies: _containers.RepeatedCompositeFieldContainer[ActivityShootEnemyInfo]
    rewarded_ids: _containers.RepeatedScalarFieldContainer[int]
    ended: bool
    rewarded_records: _containers.RepeatedCompositeFieldContainer[ActivityShootRewardRecord]
    def __init__(self, activity_id: _Optional[int] = ..., level: _Optional[int] = ..., enemies: _Optional[_Iterable[_Union[ActivityShootEnemyInfo, _Mapping]]] = ..., rewarded_ids: _Optional[_Iterable[int]] = ..., ended: _Optional[bool] = ..., rewarded_records: _Optional[_Iterable[_Union[ActivityShootRewardRecord, _Mapping]]] = ...) -> None: ...

class ActivityShootEnemyInfo(_message.Message):
    __slots__ = ()
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    ENEMY_ID_FIELD_NUMBER: _ClassVar[int]
    HP_FIELD_NUMBER: _ClassVar[int]
    group_id: int
    enemy_id: int
    hp: int
    def __init__(self, group_id: _Optional[int] = ..., enemy_id: _Optional[int] = ..., hp: _Optional[int] = ...) -> None: ...

class ActivityShootEnemyInfoDirty(_message.Message):
    __slots__ = ()
    DIRTY_FIELD_NUMBER: _ClassVar[int]
    ENEMIES_FIELD_NUMBER: _ClassVar[int]
    dirty: int
    enemies: _containers.RepeatedCompositeFieldContainer[ActivityShootEnemyInfo]
    def __init__(self, dirty: _Optional[int] = ..., enemies: _Optional[_Iterable[_Union[ActivityShootEnemyInfo, _Mapping]]] = ...) -> None: ...

class ActivityShootRewardRecord(_message.Message):
    __slots__ = ()
    ENEMY_ID_FIELD_NUMBER: _ClassVar[int]
    REWARD_ID_FIELD_NUMBER: _ClassVar[int]
    REWARDED_TIME_FIELD_NUMBER: _ClassVar[int]
    enemy_id: int
    reward_id: int
    rewarded_time: int
    def __init__(self, enemy_id: _Optional[int] = ..., reward_id: _Optional[int] = ..., rewarded_time: _Optional[int] = ...) -> None: ...

class ActivityShootValueChange(_message.Message):
    __slots__ = ()
    class Uint32ValueDirty(_message.Message):
        __slots__ = ()
        VALUE_FIELD_NUMBER: _ClassVar[int]
        DIRTY_FIELD_NUMBER: _ClassVar[int]
        value: int
        dirty: int
        def __init__(self, value: _Optional[int] = ..., dirty: _Optional[int] = ...) -> None: ...
    class RewardArrayDirty(_message.Message):
        __slots__ = ()
        REWARD_IDS_FIELD_NUMBER: _ClassVar[int]
        DIRTY_FIELD_NUMBER: _ClassVar[int]
        reward_ids: _containers.RepeatedScalarFieldContainer[int]
        dirty: int
        def __init__(self, reward_ids: _Optional[_Iterable[int]] = ..., dirty: _Optional[int] = ...) -> None: ...
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    ENEMIES_FIELD_NUMBER: _ClassVar[int]
    REWARDED_IDS_FIELD_NUMBER: _ClassVar[int]
    level: ActivityShootValueChange.Uint32ValueDirty
    enemies: ActivityShootEnemyInfoDirty
    rewarded_ids: ActivityShootValueChange.RewardArrayDirty
    def __init__(self, level: _Optional[_Union[ActivityShootValueChange.Uint32ValueDirty, _Mapping]] = ..., enemies: _Optional[_Union[ActivityShootEnemyInfoDirty, _Mapping]] = ..., rewarded_ids: _Optional[_Union[ActivityShootValueChange.RewardArrayDirty, _Mapping]] = ...) -> None: ...

class ActivitySimulationDailyContest(_message.Message):
    __slots__ = ()
    DAY_FIELD_NUMBER: _ClassVar[int]
    CHARACTERS_FIELD_NUMBER: _ClassVar[int]
    RECORDS_FIELD_NUMBER: _ClassVar[int]
    ROUND_FIELD_NUMBER: _ClassVar[int]
    day: int
    characters: _containers.RepeatedScalarFieldContainer[int]
    records: _containers.RepeatedCompositeFieldContainer[ActivitySimulationGameRecord]
    round: int
    def __init__(self, day: _Optional[int] = ..., characters: _Optional[_Iterable[int]] = ..., records: _Optional[_Iterable[_Union[ActivitySimulationGameRecord, _Mapping]]] = ..., round: _Optional[int] = ...) -> None: ...

class ActivitySimulationData(_message.Message):
    __slots__ = ()
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

class ActivitySimulationGameRecord(_message.Message):
    __slots__ = ()
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

class ActivitySimulationGameRecordMessage(_message.Message):
    __slots__ = ()
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    XUN_FIELD_NUMBER: _ClassVar[int]
    type: int
    args: _containers.RepeatedScalarFieldContainer[int]
    xun: int
    def __init__(self, type: _Optional[int] = ..., args: _Optional[_Iterable[int]] = ..., xun: _Optional[int] = ...) -> None: ...

class ActivitySimulationTrainRecord(_message.Message):
    __slots__ = ()
    TIME_FIELD_NUMBER: _ClassVar[int]
    MODIFY_STATS_FIELD_NUMBER: _ClassVar[int]
    FINAL_STATS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    time: int
    modify_stats: _containers.RepeatedScalarFieldContainer[int]
    final_stats: _containers.RepeatedScalarFieldContainer[int]
    type: int
    def __init__(self, time: _Optional[int] = ..., modify_stats: _Optional[_Iterable[int]] = ..., final_stats: _Optional[_Iterable[int]] = ..., type: _Optional[int] = ...) -> None: ...

class ActivitySpotData(_message.Message):
    __slots__ = ()
    class SpotData(_message.Message):
        __slots__ = ()
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

class ActivityStoryData(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    UNLOCKED_STORY_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    unlocked_story: _containers.RepeatedCompositeFieldContainer[UnlockedStoryData]
    def __init__(self, activity_id: _Optional[int] = ..., unlocked_story: _Optional[_Iterable[_Union[UnlockedStoryData, _Mapping]]] = ...) -> None: ...

class ActivityUpgradeData(_message.Message):
    __slots__ = ()
    class LevelGroup(_message.Message):
        __slots__ = ()
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

class ActivityVillageData(_message.Message):
    __slots__ = ()
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

class AmuletActivityTingInfo(_message.Message):
    __slots__ = ()
    TILE_FIELD_NUMBER: _ClassVar[int]
    FAN_FIELD_NUMBER: _ClassVar[int]
    TING_TILE_FIELD_NUMBER: _ClassVar[int]
    tile: str
    fan: str
    ting_tile: str
    def __init__(self, tile: _Optional[str] = ..., fan: _Optional[str] = ..., ting_tile: _Optional[str] = ...) -> None: ...

class AmuletBadgeData(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    UID_FIELD_NUMBER: _ClassVar[int]
    STORE_FIELD_NUMBER: _ClassVar[int]
    RANDOM_FIELD_NUMBER: _ClassVar[int]
    id: int
    uid: int
    store: _containers.RepeatedScalarFieldContainer[str]
    random: int
    def __init__(self, id: _Optional[int] = ..., uid: _Optional[int] = ..., store: _Optional[_Iterable[str]] = ..., random: _Optional[int] = ...) -> None: ...

class AmuletBuffData(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    STORE_FIELD_NUMBER: _ClassVar[int]
    id: int
    store: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[int] = ..., store: _Optional[_Iterable[str]] = ...) -> None: ...

class AmuletBuffDataArrayDirty(_message.Message):
    __slots__ = ()
    DIRTY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    dirty: bool
    value: _containers.RepeatedCompositeFieldContainer[AmuletBuffData]
    def __init__(self, dirty: _Optional[bool] = ..., value: _Optional[_Iterable[_Union[AmuletBuffData, _Mapping]]] = ...) -> None: ...

class AmuletEffectCandidate(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    BADGE_ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    badge_id: int
    def __init__(self, id: _Optional[int] = ..., badge_id: _Optional[int] = ...) -> None: ...

class AmuletEffectCandidatesArrayDirty(_message.Message):
    __slots__ = ()
    DIRTY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    dirty: bool
    value: _containers.RepeatedCompositeFieldContainer[AmuletEffectCandidate]
    def __init__(self, dirty: _Optional[bool] = ..., value: _Optional[_Iterable[_Union[AmuletEffectCandidate, _Mapping]]] = ...) -> None: ...

class AmuletEffectCounterData(_message.Message):
    __slots__ = ()
    EFFECT_ID_FIELD_NUMBER: _ClassVar[int]
    PACK_CANDIDATE_COUNT_FIELD_NUMBER: _ClassVar[int]
    GAIN_COUNT_FIELD_NUMBER: _ClassVar[int]
    effect_id: int
    pack_candidate_count: int
    gain_count: int
    def __init__(self, effect_id: _Optional[int] = ..., pack_candidate_count: _Optional[int] = ..., gain_count: _Optional[int] = ...) -> None: ...

class AmuletEffectCounterDataArrayDirty(_message.Message):
    __slots__ = ()
    DIRTY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    dirty: bool
    value: _containers.RepeatedCompositeFieldContainer[AmuletEffectCounterData]
    def __init__(self, dirty: _Optional[bool] = ..., value: _Optional[_Iterable[_Union[AmuletEffectCounterData, _Mapping]]] = ...) -> None: ...

class AmuletEffectData(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    UID_FIELD_NUMBER: _ClassVar[int]
    STORE_FIELD_NUMBER: _ClassVar[int]
    BADGE_FIELD_NUMBER: _ClassVar[int]
    VOLUME_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    id: int
    uid: int
    store: _containers.RepeatedScalarFieldContainer[str]
    badge: AmuletBadgeData
    volume: int
    tags: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, id: _Optional[int] = ..., uid: _Optional[int] = ..., store: _Optional[_Iterable[str]] = ..., badge: _Optional[_Union[AmuletBadgeData, _Mapping]] = ..., volume: _Optional[int] = ..., tags: _Optional[_Iterable[int]] = ...) -> None: ...

class AmuletEffectDataArrayDirty(_message.Message):
    __slots__ = ()
    DIRTY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    dirty: bool
    value: _containers.RepeatedCompositeFieldContainer[AmuletEffectData]
    def __init__(self, dirty: _Optional[bool] = ..., value: _Optional[_Iterable[_Union[AmuletEffectData, _Mapping]]] = ...) -> None: ...

class AmuletEffectDataChanges(_message.Message):
    __slots__ = ()
    EFFECT_LIST_FIELD_NUMBER: _ClassVar[int]
    BUFF_LIST_FIELD_NUMBER: _ClassVar[int]
    SKILL_BUFF_LIST_FIELD_NUMBER: _ClassVar[int]
    SHOP_BUFF_LIST_FIELD_NUMBER: _ClassVar[int]
    FREE_REWARD_CANDIDATES_FIELD_NUMBER: _ClassVar[int]
    LEVEL_REWARD_CANDIDATES_FIELD_NUMBER: _ClassVar[int]
    CURRENT_LEVEL_REWARD_PACK_FIELD_NUMBER: _ClassVar[int]
    effect_list: AmuletEffectDataArrayDirty
    buff_list: AmuletBuffDataArrayDirty
    skill_buff_list: AmuletBuffDataArrayDirty
    shop_buff_list: AmuletBuffDataArrayDirty
    free_reward_candidates: AmuletEffectCandidatesArrayDirty
    level_reward_candidates: AmuletEffectCandidatesArrayDirty
    current_level_reward_pack: UInt32Dirty
    def __init__(self, effect_list: _Optional[_Union[AmuletEffectDataArrayDirty, _Mapping]] = ..., buff_list: _Optional[_Union[AmuletBuffDataArrayDirty, _Mapping]] = ..., skill_buff_list: _Optional[_Union[AmuletBuffDataArrayDirty, _Mapping]] = ..., shop_buff_list: _Optional[_Union[AmuletBuffDataArrayDirty, _Mapping]] = ..., free_reward_candidates: _Optional[_Union[AmuletEffectCandidatesArrayDirty, _Mapping]] = ..., level_reward_candidates: _Optional[_Union[AmuletEffectCandidatesArrayDirty, _Mapping]] = ..., current_level_reward_pack: _Optional[_Union[UInt32Dirty, _Mapping]] = ...) -> None: ...

class AmuletEffectedHookData(_message.Message):
    __slots__ = ()
    UID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    uid: int
    id: int
    result: AmuletHookResult
    type: int
    def __init__(self, uid: _Optional[int] = ..., id: _Optional[int] = ..., result: _Optional[_Union[AmuletHookResult, _Mapping]] = ..., type: _Optional[int] = ...) -> None: ...

class AmuletEventData(_message.Message):
    __slots__ = ()
    TYPE_FIELD_NUMBER: _ClassVar[int]
    EFFECTED_HOOKS_FIELD_NUMBER: _ClassVar[int]
    VALUE_CHANGES_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    EVENT_HOOKS_FIELD_NUMBER: _ClassVar[int]
    type: int
    effected_hooks: _containers.RepeatedCompositeFieldContainer[AmuletEffectedHookData]
    value_changes: AmuletValueChanges
    result: AmuletEventResult
    event_hooks: _containers.RepeatedCompositeFieldContainer[AmuletEventHookData]
    def __init__(self, type: _Optional[int] = ..., effected_hooks: _Optional[_Iterable[_Union[AmuletEffectedHookData, _Mapping]]] = ..., value_changes: _Optional[_Union[AmuletValueChanges, _Mapping]] = ..., result: _Optional[_Union[AmuletEventResult, _Mapping]] = ..., event_hooks: _Optional[_Iterable[_Union[AmuletEventHookData, _Mapping]]] = ...) -> None: ...

class AmuletEventHookData(_message.Message):
    __slots__ = ()
    REMOVE_EFFECT_FIELD_NUMBER: _ClassVar[int]
    remove_effect: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, remove_effect: _Optional[_Iterable[int]] = ...) -> None: ...

class AmuletEventResult(_message.Message):
    __slots__ = ()
    class DealResult(_message.Message):
        __slots__ = ()
        TILE_FIELD_NUMBER: _ClassVar[int]
        tile: int
        def __init__(self, tile: _Optional[int] = ...) -> None: ...
    class HuResult(_message.Message):
        __slots__ = ()
        class HuInfo(_message.Message):
            __slots__ = ()
            TILE_FIELD_NUMBER: _ClassVar[int]
            FAN_LIST_FIELD_NUMBER: _ClassVar[int]
            FAN_FIELD_NUMBER: _ClassVar[int]
            BASE_FIELD_NUMBER: _ClassVar[int]
            POINT_FIELD_NUMBER: _ClassVar[int]
            tile: int
            fan_list: _containers.RepeatedCompositeFieldContainer[AmuletFan]
            fan: str
            base: str
            point: str
            def __init__(self, tile: _Optional[int] = ..., fan_list: _Optional[_Iterable[_Union[AmuletFan, _Mapping]]] = ..., fan: _Optional[str] = ..., base: _Optional[str] = ..., point: _Optional[str] = ...) -> None: ...
        HU_FINAL_FIELD_NUMBER: _ClassVar[int]
        HU_BASE_FIELD_NUMBER: _ClassVar[int]
        hu_final: AmuletEventResult.HuResult.HuInfo
        hu_base: AmuletEventResult.HuResult.HuInfo
        def __init__(self, hu_final: _Optional[_Union[AmuletEventResult.HuResult.HuInfo, _Mapping]] = ..., hu_base: _Optional[_Union[AmuletEventResult.HuResult.HuInfo, _Mapping]] = ...) -> None: ...
    class GameEndResult(_message.Message):
        __slots__ = ()
        REASON_FIELD_NUMBER: _ClassVar[int]
        reason: int
        def __init__(self, reason: _Optional[int] = ...) -> None: ...
    class GangResult(_message.Message):
        __slots__ = ()
        NEW_DORA_FIELD_NUMBER: _ClassVar[int]
        new_dora: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, new_dora: _Optional[_Iterable[int]] = ...) -> None: ...
    class UpgradeResult(_message.Message):
        __slots__ = ()
        LEVEL_COIN_FIELD_NUMBER: _ClassVar[int]
        POINT_COIN_FIELD_NUMBER: _ClassVar[int]
        level_coin: str
        point_coin: str
        def __init__(self, level_coin: _Optional[str] = ..., point_coin: _Optional[str] = ...) -> None: ...
    class SellEffectResult(_message.Message):
        __slots__ = ()
        PRICE_FIELD_NUMBER: _ClassVar[int]
        price: str
        def __init__(self, price: _Optional[str] = ...) -> None: ...
    class SelectPackResult(_message.Message):
        __slots__ = ()
        UID_FIELD_NUMBER: _ClassVar[int]
        ID_FIELD_NUMBER: _ClassVar[int]
        MERGE_TYPE_FIELD_NUMBER: _ClassVar[int]
        MERGED_LIST_FIELD_NUMBER: _ClassVar[int]
        MERGED_RESULT_FIELD_NUMBER: _ClassVar[int]
        BADGE_FIELD_NUMBER: _ClassVar[int]
        uid: int
        id: int
        merge_type: int
        merged_list: _containers.RepeatedScalarFieldContainer[int]
        merged_result: int
        badge: AmuletBadgeData
        def __init__(self, uid: _Optional[int] = ..., id: _Optional[int] = ..., merge_type: _Optional[int] = ..., merged_list: _Optional[_Iterable[int]] = ..., merged_result: _Optional[int] = ..., badge: _Optional[_Union[AmuletBadgeData, _Mapping]] = ...) -> None: ...
    DEAL_RESULT_FIELD_NUMBER: _ClassVar[int]
    HU_RESULT_FIELD_NUMBER: _ClassVar[int]
    GAME_END_RESULT_FIELD_NUMBER: _ClassVar[int]
    GANG_RESULT_FIELD_NUMBER: _ClassVar[int]
    UPGRADE_RESULT_FIELD_NUMBER: _ClassVar[int]
    NEW_GAME_RESULT_FIELD_NUMBER: _ClassVar[int]
    SELL_EFFECT_RESULT_FIELD_NUMBER: _ClassVar[int]
    SELECT_PACK_RESULT_FIELD_NUMBER: _ClassVar[int]
    deal_result: AmuletEventResult.DealResult
    hu_result: AmuletEventResult.HuResult
    game_end_result: AmuletEventResult.GameEndResult
    gang_result: AmuletEventResult.GangResult
    upgrade_result: AmuletEventResult.UpgradeResult
    new_game_result: AmuletGameData
    sell_effect_result: AmuletEventResult.SellEffectResult
    select_pack_result: AmuletEventResult.SelectPackResult
    def __init__(self, deal_result: _Optional[_Union[AmuletEventResult.DealResult, _Mapping]] = ..., hu_result: _Optional[_Union[AmuletEventResult.HuResult, _Mapping]] = ..., game_end_result: _Optional[_Union[AmuletEventResult.GameEndResult, _Mapping]] = ..., gang_result: _Optional[_Union[AmuletEventResult.GangResult, _Mapping]] = ..., upgrade_result: _Optional[_Union[AmuletEventResult.UpgradeResult, _Mapping]] = ..., new_game_result: _Optional[_Union[AmuletGameData, _Mapping]] = ..., sell_effect_result: _Optional[_Union[AmuletEventResult.SellEffectResult, _Mapping]] = ..., select_pack_result: _Optional[_Union[AmuletEventResult.SelectPackResult, _Mapping]] = ...) -> None: ...

class AmuletFan(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    VAL_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    YIMAN_FIELD_NUMBER: _ClassVar[int]
    id: int
    val: str
    count: int
    yiman: bool
    def __init__(self, id: _Optional[int] = ..., val: _Optional[str] = ..., count: _Optional[int] = ..., yiman: _Optional[bool] = ...) -> None: ...

class AmuletGameData(_message.Message):
    __slots__ = ()
    ROUND_FIELD_NUMBER: _ClassVar[int]
    EFFECT_FIELD_NUMBER: _ClassVar[int]
    GAME_FIELD_NUMBER: _ClassVar[int]
    STAGE_FIELD_NUMBER: _ClassVar[int]
    SHOP_FIELD_NUMBER: _ClassVar[int]
    RECORD_FIELD_NUMBER: _ClassVar[int]
    ENDED_FIELD_NUMBER: _ClassVar[int]
    round: AmuletGameRoundData
    effect: AmuletGameEffectData
    game: AmuletGameInfoData
    stage: int
    shop: AmuletShopData
    record: AmuletGameRecordData
    ended: bool
    def __init__(self, round: _Optional[_Union[AmuletGameRoundData, _Mapping]] = ..., effect: _Optional[_Union[AmuletGameEffectData, _Mapping]] = ..., game: _Optional[_Union[AmuletGameInfoData, _Mapping]] = ..., stage: _Optional[int] = ..., shop: _Optional[_Union[AmuletShopData, _Mapping]] = ..., record: _Optional[_Union[AmuletGameRecordData, _Mapping]] = ..., ended: _Optional[bool] = ...) -> None: ...

class AmuletGameEffectData(_message.Message):
    __slots__ = ()
    EFFECT_LIST_FIELD_NUMBER: _ClassVar[int]
    BUFF_LIST_FIELD_NUMBER: _ClassVar[int]
    SKILL_BUFF_LIST_FIELD_NUMBER: _ClassVar[int]
    SHOP_BUFF_LIST_FIELD_NUMBER: _ClassVar[int]
    FREE_REWARD_CANDIDATES_FIELD_NUMBER: _ClassVar[int]
    LEVEL_REWARD_CANDIDATES_FIELD_NUMBER: _ClassVar[int]
    LEVEL_REWARD_PACKS_FIELD_NUMBER: _ClassVar[int]
    CURRENT_LEVEL_REWARD_PACK_FIELD_NUMBER: _ClassVar[int]
    MAX_EFFECT_VOLUME_FIELD_NUMBER: _ClassVar[int]
    effect_list: _containers.RepeatedCompositeFieldContainer[AmuletEffectData]
    buff_list: _containers.RepeatedCompositeFieldContainer[AmuletBuffData]
    skill_buff_list: _containers.RepeatedCompositeFieldContainer[AmuletBuffData]
    shop_buff_list: _containers.RepeatedCompositeFieldContainer[AmuletBuffData]
    free_reward_candidates: _containers.RepeatedCompositeFieldContainer[AmuletEffectCandidate]
    level_reward_candidates: _containers.RepeatedCompositeFieldContainer[AmuletEffectCandidate]
    level_reward_packs: _containers.RepeatedScalarFieldContainer[int]
    current_level_reward_pack: int
    max_effect_volume: int
    def __init__(self, effect_list: _Optional[_Iterable[_Union[AmuletEffectData, _Mapping]]] = ..., buff_list: _Optional[_Iterable[_Union[AmuletBuffData, _Mapping]]] = ..., skill_buff_list: _Optional[_Iterable[_Union[AmuletBuffData, _Mapping]]] = ..., shop_buff_list: _Optional[_Iterable[_Union[AmuletBuffData, _Mapping]]] = ..., free_reward_candidates: _Optional[_Iterable[_Union[AmuletEffectCandidate, _Mapping]]] = ..., level_reward_candidates: _Optional[_Iterable[_Union[AmuletEffectCandidate, _Mapping]]] = ..., level_reward_packs: _Optional[_Iterable[int]] = ..., current_level_reward_pack: _Optional[int] = ..., max_effect_volume: _Optional[int] = ...) -> None: ...

class AmuletGameInfoData(_message.Message):
    __slots__ = ()
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    COIN_FIELD_NUMBER: _ClassVar[int]
    MAX_EFFECT_VOLUME_FIELD_NUMBER: _ClassVar[int]
    NEXT_BOSS_BUFF_FIELD_NUMBER: _ClassVar[int]
    BOSS_BUFF_FIELD_NUMBER: _ClassVar[int]
    TILE_SCORE_MAP_FIELD_NUMBER: _ClassVar[int]
    BOOK_EFFECT_ID_FIELD_NUMBER: _ClassVar[int]
    level: int
    coin: str
    max_effect_volume: int
    next_boss_buff: _containers.RepeatedScalarFieldContainer[int]
    boss_buff: _containers.RepeatedScalarFieldContainer[int]
    tile_score_map: _containers.RepeatedCompositeFieldContainer[AmuletTileScore]
    book_effect_id: int
    def __init__(self, level: _Optional[int] = ..., coin: _Optional[str] = ..., max_effect_volume: _Optional[int] = ..., next_boss_buff: _Optional[_Iterable[int]] = ..., boss_buff: _Optional[_Iterable[int]] = ..., tile_score_map: _Optional[_Iterable[_Union[AmuletTileScore, _Mapping]]] = ..., book_effect_id: _Optional[int] = ...) -> None: ...

class AmuletGameInfoDataChanges(_message.Message):
    __slots__ = ()
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    COIN_FIELD_NUMBER: _ClassVar[int]
    MAX_EFFECT_VOLUME_FIELD_NUMBER: _ClassVar[int]
    NEXT_BOSS_BUFF_FIELD_NUMBER: _ClassVar[int]
    BOSS_BUFF_FIELD_NUMBER: _ClassVar[int]
    TILE_SCORE_MAP_FIELD_NUMBER: _ClassVar[int]
    level: UInt32Dirty
    coin: StringDirty
    max_effect_volume: UInt32Dirty
    next_boss_buff: UInt32ArrayDirty
    boss_buff: UInt32ArrayDirty
    tile_score_map: AmuletTileScoreArrayDirty
    def __init__(self, level: _Optional[_Union[UInt32Dirty, _Mapping]] = ..., coin: _Optional[_Union[StringDirty, _Mapping]] = ..., max_effect_volume: _Optional[_Union[UInt32Dirty, _Mapping]] = ..., next_boss_buff: _Optional[_Union[UInt32ArrayDirty, _Mapping]] = ..., boss_buff: _Optional[_Union[UInt32ArrayDirty, _Mapping]] = ..., tile_score_map: _Optional[_Union[AmuletTileScoreArrayDirty, _Mapping]] = ...) -> None: ...

class AmuletGameOperation(_message.Message):
    __slots__ = ()
    class GangTiles(_message.Message):
        __slots__ = ()
        TILES_FIELD_NUMBER: _ClassVar[int]
        tiles: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, tiles: _Optional[_Iterable[int]] = ...) -> None: ...
    TYPE_FIELD_NUMBER: _ClassVar[int]
    GANG_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    type: int
    gang: _containers.RepeatedCompositeFieldContainer[AmuletGameOperation.GangTiles]
    value: int
    def __init__(self, type: _Optional[int] = ..., gang: _Optional[_Iterable[_Union[AmuletGameOperation.GangTiles, _Mapping]]] = ..., value: _Optional[int] = ...) -> None: ...

class AmuletGameOperationArrayDirty(_message.Message):
    __slots__ = ()
    DIRTY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    dirty: bool
    value: _containers.RepeatedCompositeFieldContainer[AmuletGameOperation]
    def __init__(self, dirty: _Optional[bool] = ..., value: _Optional[_Iterable[_Union[AmuletGameOperation, _Mapping]]] = ...) -> None: ...

class AmuletGameRecordData(_message.Message):
    __slots__ = ()
    YIMAN_COUNT_FIELD_NUMBER: _ClassVar[int]
    LEVEL_HU_COUNT_FIELD_NUMBER: _ClassVar[int]
    GAME_HU_COUNT_FIELD_NUMBER: _ClassVar[int]
    EFFECT_GAIN_FIELD_NUMBER: _ClassVar[int]
    COIN_CONSUME_FIELD_NUMBER: _ClassVar[int]
    COIN_GAIN_FIELD_NUMBER: _ClassVar[int]
    HIGHEST_HU_FIELD_NUMBER: _ClassVar[int]
    HIGHEST_LEVEL_SCORE_FIELD_NUMBER: _ClassVar[int]
    HIGHEST_FAN_FIELD_NUMBER: _ClassVar[int]
    PACK_COUNT_FIELD_NUMBER: _ClassVar[int]
    ROUND_COUNT_FIELD_NUMBER: _ClassVar[int]
    EFFECT_COUNTER_FIELD_NUMBER: _ClassVar[int]
    HU_TILES_ID_FIELD_NUMBER: _ClassVar[int]
    yiman_count: int
    level_hu_count: int
    game_hu_count: int
    effect_gain: int
    coin_consume: str
    coin_gain: str
    highest_hu: ActivityAmuletHuRecord
    highest_level_score: str
    highest_fan: str
    pack_count: int
    round_count: int
    effect_counter: _containers.RepeatedCompositeFieldContainer[AmuletEffectCounterData]
    hu_tiles_id: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, yiman_count: _Optional[int] = ..., level_hu_count: _Optional[int] = ..., game_hu_count: _Optional[int] = ..., effect_gain: _Optional[int] = ..., coin_consume: _Optional[str] = ..., coin_gain: _Optional[str] = ..., highest_hu: _Optional[_Union[ActivityAmuletHuRecord, _Mapping]] = ..., highest_level_score: _Optional[str] = ..., highest_fan: _Optional[str] = ..., pack_count: _Optional[int] = ..., round_count: _Optional[int] = ..., effect_counter: _Optional[_Iterable[_Union[AmuletEffectCounterData, _Mapping]]] = ..., hu_tiles_id: _Optional[_Iterable[int]] = ...) -> None: ...

class AmuletGameRoundData(_message.Message):
    __slots__ = ()
    POOL_FIELD_NUMBER: _ClassVar[int]
    TILE_REPLACE_FIELD_NUMBER: _ClassVar[int]
    TIAN_DORA_FIELD_NUMBER: _ClassVar[int]
    MOUNTAIN_FIELD_NUMBER: _ClassVar[int]
    DORA_FIELD_NUMBER: _ClassVar[int]
    HANDS_FIELD_NUMBER: _ClassVar[int]
    USED_FIELD_NUMBER: _ClassVar[int]
    USED_DESKTOP_FIELD_NUMBER: _ClassVar[int]
    MING_FIELD_NUMBER: _ClassVar[int]
    DESKTOP_FIELD_NUMBER: _ClassVar[int]
    SHOW_DESKTOP_FIELD_NUMBER: _ClassVar[int]
    LOCKED_TILE_FIELD_NUMBER: _ClassVar[int]
    CHANGE_TILE_COUNT_FIELD_NUMBER: _ClassVar[int]
    TOTAL_CHANGE_TILE_COUNT_FIELD_NUMBER: _ClassVar[int]
    NEXT_OPERATION_FIELD_NUMBER: _ClassVar[int]
    TING_LIST_FIELD_NUMBER: _ClassVar[int]
    AFTER_GANG_FIELD_NUMBER: _ClassVar[int]
    POINT_FIELD_NUMBER: _ClassVar[int]
    TARGET_POINT_FIELD_NUMBER: _ClassVar[int]
    DESKTOP_REMAIN_FIELD_NUMBER: _ClassVar[int]
    SHOW_DESKTOP_TILES_FIELD_NUMBER: _ClassVar[int]
    LOCKED_TILE_COUNT_FIELD_NUMBER: _ClassVar[int]
    pool: _containers.RepeatedCompositeFieldContainer[AmuletTile]
    tile_replace: _containers.RepeatedCompositeFieldContainer[AmuletTile]
    tian_dora: _containers.RepeatedScalarFieldContainer[str]
    mountain: _containers.RepeatedScalarFieldContainer[int]
    dora: _containers.RepeatedScalarFieldContainer[int]
    hands: _containers.RepeatedScalarFieldContainer[int]
    used: _containers.RepeatedScalarFieldContainer[int]
    used_desktop: _containers.RepeatedScalarFieldContainer[int]
    ming: _containers.RepeatedCompositeFieldContainer[AmuletMingInfo]
    desktop: _containers.RepeatedScalarFieldContainer[int]
    show_desktop: _containers.RepeatedScalarFieldContainer[int]
    locked_tile: _containers.RepeatedScalarFieldContainer[int]
    change_tile_count: int
    total_change_tile_count: int
    next_operation: _containers.RepeatedCompositeFieldContainer[AmuletGameOperation]
    ting_list: _containers.RepeatedCompositeFieldContainer[AmuletActivityTingInfo]
    after_gang: int
    point: str
    target_point: str
    desktop_remain: int
    show_desktop_tiles: _containers.RepeatedCompositeFieldContainer[AmuletShowDesktopTileData]
    locked_tile_count: int
    def __init__(self, pool: _Optional[_Iterable[_Union[AmuletTile, _Mapping]]] = ..., tile_replace: _Optional[_Iterable[_Union[AmuletTile, _Mapping]]] = ..., tian_dora: _Optional[_Iterable[str]] = ..., mountain: _Optional[_Iterable[int]] = ..., dora: _Optional[_Iterable[int]] = ..., hands: _Optional[_Iterable[int]] = ..., used: _Optional[_Iterable[int]] = ..., used_desktop: _Optional[_Iterable[int]] = ..., ming: _Optional[_Iterable[_Union[AmuletMingInfo, _Mapping]]] = ..., desktop: _Optional[_Iterable[int]] = ..., show_desktop: _Optional[_Iterable[int]] = ..., locked_tile: _Optional[_Iterable[int]] = ..., change_tile_count: _Optional[int] = ..., total_change_tile_count: _Optional[int] = ..., next_operation: _Optional[_Iterable[_Union[AmuletGameOperation, _Mapping]]] = ..., ting_list: _Optional[_Iterable[_Union[AmuletActivityTingInfo, _Mapping]]] = ..., after_gang: _Optional[int] = ..., point: _Optional[str] = ..., target_point: _Optional[str] = ..., desktop_remain: _Optional[int] = ..., show_desktop_tiles: _Optional[_Iterable[_Union[AmuletShowDesktopTileData, _Mapping]]] = ..., locked_tile_count: _Optional[int] = ...) -> None: ...

class AmuletGameShopGoods(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    SOLD_FIELD_NUMBER: _ClassVar[int]
    GOODS_ID_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    id: int
    sold: bool
    goods_id: int
    price: int
    def __init__(self, id: _Optional[int] = ..., sold: _Optional[bool] = ..., goods_id: _Optional[int] = ..., price: _Optional[int] = ...) -> None: ...

class AmuletHookResult(_message.Message):
    __slots__ = ()
    class AddEffectResult(_message.Message):
        __slots__ = ()
        UID_FIELD_NUMBER: _ClassVar[int]
        ID_FIELD_NUMBER: _ClassVar[int]
        MERGE_TYPE_FIELD_NUMBER: _ClassVar[int]
        MERGED_LIST_FIELD_NUMBER: _ClassVar[int]
        MERGED_RESULT_FIELD_NUMBER: _ClassVar[int]
        BADGE_FIELD_NUMBER: _ClassVar[int]
        STORE_FIELD_NUMBER: _ClassVar[int]
        VOLUME_FIELD_NUMBER: _ClassVar[int]
        uid: int
        id: int
        merge_type: int
        merged_list: _containers.RepeatedScalarFieldContainer[int]
        merged_result: int
        badge: AmuletBadgeData
        store: _containers.RepeatedScalarFieldContainer[str]
        volume: int
        def __init__(self, uid: _Optional[int] = ..., id: _Optional[int] = ..., merge_type: _Optional[int] = ..., merged_list: _Optional[_Iterable[int]] = ..., merged_result: _Optional[int] = ..., badge: _Optional[_Union[AmuletBadgeData, _Mapping]] = ..., store: _Optional[_Iterable[str]] = ..., volume: _Optional[int] = ...) -> None: ...
    class AddDoraResult(_message.Message):
        __slots__ = ()
        COUNT_FIELD_NUMBER: _ClassVar[int]
        LIST_FIELD_NUMBER: _ClassVar[int]
        count: int
        list: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, count: _Optional[int] = ..., list: _Optional[_Iterable[int]] = ...) -> None: ...
    class ValueResult(_message.Message):
        __slots__ = ()
        ORIGIN_FIELD_NUMBER: _ClassVar[int]
        MODIFY_FIELD_NUMBER: _ClassVar[int]
        FINAL_FIELD_NUMBER: _ClassVar[int]
        origin: str
        modify: str
        final: str
        def __init__(self, origin: _Optional[str] = ..., modify: _Optional[str] = ..., final: _Optional[str] = ...) -> None: ...
    class ModifyDoraResult(_message.Message):
        __slots__ = ()
        TILE_FIELD_NUMBER: _ClassVar[int]
        IS_DORA_FIELD_NUMBER: _ClassVar[int]
        IS_RED_DORA_FIELD_NUMBER: _ClassVar[int]
        IS_TIAN_DORA_FIELD_NUMBER: _ClassVar[int]
        DORA_COUNT_FIELD_NUMBER: _ClassVar[int]
        tile: str
        is_dora: bool
        is_red_dora: bool
        is_tian_dora: bool
        dora_count: int
        def __init__(self, tile: _Optional[str] = ..., is_dora: _Optional[bool] = ..., is_red_dora: _Optional[bool] = ..., is_tian_dora: _Optional[bool] = ..., dora_count: _Optional[int] = ...) -> None: ...
    class TransformResult(_message.Message):
        __slots__ = ()
        UID_FIELD_NUMBER: _ClassVar[int]
        EFFECT_ID_FIELD_NUMBER: _ClassVar[int]
        ADD_RESULT_FIELD_NUMBER: _ClassVar[int]
        uid: int
        effect_id: int
        add_result: AmuletHookResult.AddEffectResult
        def __init__(self, uid: _Optional[int] = ..., effect_id: _Optional[int] = ..., add_result: _Optional[_Union[AmuletHookResult.AddEffectResult, _Mapping]] = ...) -> None: ...
    class AddBadge(_message.Message):
        __slots__ = ()
        UID_FIELD_NUMBER: _ClassVar[int]
        BADGE_ID_FIELD_NUMBER: _ClassVar[int]
        BADGE_UID_FIELD_NUMBER: _ClassVar[int]
        uid: int
        badge_id: int
        badge_uid: int
        def __init__(self, uid: _Optional[int] = ..., badge_id: _Optional[int] = ..., badge_uid: _Optional[int] = ...) -> None: ...
    class CopyEffect(_message.Message):
        __slots__ = ()
        UID_FIELD_NUMBER: _ClassVar[int]
        FROM_UID_FIELD_NUMBER: _ClassVar[int]
        uid: int
        from_uid: int
        def __init__(self, uid: _Optional[int] = ..., from_uid: _Optional[int] = ...) -> None: ...
    class AmuletChangeDesktopResult(_message.Message):
        __slots__ = ()
        SHOW_DESKTOP_TILES_FIELD_NUMBER: _ClassVar[int]
        LOCKED_TILE_COUNT_FIELD_NUMBER: _ClassVar[int]
        DESKTOP_REMAIN_FIELD_NUMBER: _ClassVar[int]
        LOCKED_TILE_FIELD_NUMBER: _ClassVar[int]
        show_desktop_tiles: _containers.RepeatedCompositeFieldContainer[AmuletShowDesktopTileData]
        locked_tile_count: int
        desktop_remain: int
        locked_tile: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, show_desktop_tiles: _Optional[_Iterable[_Union[AmuletShowDesktopTileData, _Mapping]]] = ..., locked_tile_count: _Optional[int] = ..., desktop_remain: _Optional[int] = ..., locked_tile: _Optional[_Iterable[int]] = ...) -> None: ...
    class UpgradeEffectResult(_message.Message):
        __slots__ = ()
        UID_FIELD_NUMBER: _ClassVar[int]
        ID_FIELD_NUMBER: _ClassVar[int]
        BADGE_FIELD_NUMBER: _ClassVar[int]
        STORE_FIELD_NUMBER: _ClassVar[int]
        VOLUME_FIELD_NUMBER: _ClassVar[int]
        uid: int
        id: int
        badge: AmuletBadgeData
        store: _containers.RepeatedScalarFieldContainer[str]
        volume: int
        def __init__(self, uid: _Optional[int] = ..., id: _Optional[int] = ..., badge: _Optional[_Union[AmuletBadgeData, _Mapping]] = ..., store: _Optional[_Iterable[str]] = ..., volume: _Optional[int] = ...) -> None: ...
    ADD_EFFECT_FIELD_NUMBER: _ClassVar[int]
    REMOVE_EFFECT_FIELD_NUMBER: _ClassVar[int]
    ADD_BUFF_FIELD_NUMBER: _ClassVar[int]
    REMOVE_BUFF_FIELD_NUMBER: _ClassVar[int]
    ADD_TIAN_DORA_FIELD_NUMBER: _ClassVar[int]
    ADD_DORA_FIELD_NUMBER: _ClassVar[int]
    COIN_MODIFY_FIELD_NUMBER: _ClassVar[int]
    TILE_REPLACE_FIELD_NUMBER: _ClassVar[int]
    ADD_SHOW_TILE_FIELD_NUMBER: _ClassVar[int]
    MODIFY_TILE_SCORE_FIELD_NUMBER: _ClassVar[int]
    MODIFY_DESKTOP_COUNT_FIELD_NUMBER: _ClassVar[int]
    MODIFY_SHOW_DESKTOP_COUNT_FIELD_NUMBER: _ClassVar[int]
    MODIFY_LOCK_TILE_COUNT_FIELD_NUMBER: _ClassVar[int]
    MODIFY_CHANGE_HANDS_COUNT_FIELD_NUMBER: _ClassVar[int]
    MODIFY_CHANGE_HANDS_TILE_COUNT_FIELD_NUMBER: _ClassVar[int]
    FORCE_MOQIE_FIELD_NUMBER: _ClassVar[int]
    REPLACE_HU_FIELD_NUMBER: _ClassVar[int]
    MODIFY_TARGET_POINT_FIELD_NUMBER: _ClassVar[int]
    UPGRADE_LEVEL_FIELD_NUMBER: _ClassVar[int]
    MODIFY_DORA_FIELD_NUMBER: _ClassVar[int]
    MODIFY_DORA_MAX_COUNT_FIELD_NUMBER: _ClassVar[int]
    MODIFY_SHOP_GOODS_COUNT_FIELD_NUMBER: _ClassVar[int]
    MODIFY_SHOP_RARE_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    MODIFY_SHOP_GOODS_PRICE_FIELD_NUMBER: _ClassVar[int]
    MODIFY_SHOP_PACK_EFFECT_FIELD_NUMBER: _ClassVar[int]
    MODIFY_EFFECT_MAX_COUNT_FIELD_NUMBER: _ClassVar[int]
    MODIFY_GOODS_FIELD_NUMBER: _ClassVar[int]
    REMOVE_GOODS_FIELD_NUMBER: _ClassVar[int]
    MODIFY_BASE_FIELD_NUMBER: _ClassVar[int]
    MODIFY_FAN_FIELD_NUMBER: _ClassVar[int]
    MODIFY_FAN_INFO_FIELD_NUMBER: _ClassVar[int]
    TRANSFORM_EFFECT_FIELD_NUMBER: _ClassVar[int]
    ADD_BADGE_FIELD_NUMBER: _ClassVar[int]
    REMOVE_BADGE_FIELD_NUMBER: _ClassVar[int]
    MODIFY_EFFECT_PRICE_FIELD_NUMBER: _ClassVar[int]
    COPY_EFFECT_FIELD_NUMBER: _ClassVar[int]
    EFFECT_GROWTH_FIELD_NUMBER: _ClassVar[int]
    MODIFY_TILE_SCORE_AURA_FIELD_NUMBER: _ClassVar[int]
    MODIFY_HULE_COUNT_FIELD_NUMBER: _ClassVar[int]
    CAN_GANG_FIELD_NUMBER: _ClassVar[int]
    MODIFY_CHANGE_HANDS_LIST_FIELD_NUMBER: _ClassVar[int]
    MODIFY_CHANGE_DESKTOP_FIELD_NUMBER: _ClassVar[int]
    SELF_EFFECT_ID_FIELD_NUMBER: _ClassVar[int]
    MODIFY_CHANGE_COIN_FIELD_NUMBER: _ClassVar[int]
    SET_TILE_SCORE_FIELD_NUMBER: _ClassVar[int]
    UPGRADE_EFFECT_FIELD_NUMBER: _ClassVar[int]
    MODIFY_TILE_BASE_SCORE_FIELD_NUMBER: _ClassVar[int]
    add_effect: _containers.RepeatedCompositeFieldContainer[AmuletHookResult.AddEffectResult]
    remove_effect: _containers.RepeatedScalarFieldContainer[int]
    add_buff: _containers.RepeatedScalarFieldContainer[int]
    remove_buff: _containers.RepeatedScalarFieldContainer[int]
    add_tian_dora: _containers.RepeatedScalarFieldContainer[str]
    add_dora: AmuletHookResult.AddDoraResult
    coin_modify: AmuletHookResult.ValueResult
    tile_replace: _containers.RepeatedCompositeFieldContainer[AmuletTile]
    add_show_tile: _containers.RepeatedScalarFieldContainer[int]
    modify_tile_score: _containers.RepeatedCompositeFieldContainer[AmuletTileScore]
    modify_desktop_count: int
    modify_show_desktop_count: int
    modify_lock_tile_count: int
    modify_change_hands_count: int
    modify_change_hands_tile_count: int
    force_moqie: bool
    replace_hu: bool
    modify_target_point: str
    upgrade_level: bool
    modify_dora: _containers.RepeatedCompositeFieldContainer[AmuletHookResult.ModifyDoraResult]
    modify_dora_max_count: int
    modify_shop_goods_count: int
    modify_shop_rare_weight: bool
    modify_shop_goods_price: bool
    modify_shop_pack_effect: _containers.RepeatedScalarFieldContainer[int]
    modify_effect_max_count: int
    modify_goods: _containers.RepeatedCompositeFieldContainer[AmuletGameShopGoods]
    remove_goods: _containers.RepeatedScalarFieldContainer[int]
    modify_base: AmuletHookResult.ValueResult
    modify_fan: AmuletHookResult.ValueResult
    modify_fan_info: _containers.RepeatedCompositeFieldContainer[AmuletFan]
    transform_effect: _containers.RepeatedCompositeFieldContainer[AmuletHookResult.TransformResult]
    add_badge: _containers.RepeatedCompositeFieldContainer[AmuletHookResult.AddBadge]
    remove_badge: _containers.RepeatedScalarFieldContainer[int]
    modify_effect_price: str
    copy_effect: _containers.RepeatedCompositeFieldContainer[AmuletHookResult.CopyEffect]
    effect_growth: bool
    modify_tile_score_aura: str
    modify_hule_count: int
    can_gang: bool
    modify_change_hands_list: _containers.RepeatedScalarFieldContainer[int]
    modify_change_desktop: AmuletHookResult.AmuletChangeDesktopResult
    self_effect_id: int
    modify_change_coin: str
    set_tile_score: _containers.RepeatedCompositeFieldContainer[AmuletTileScore]
    upgrade_effect: _containers.RepeatedCompositeFieldContainer[AmuletHookResult.UpgradeEffectResult]
    modify_tile_base_score: _containers.RepeatedCompositeFieldContainer[AmuletTileScore]
    def __init__(self, add_effect: _Optional[_Iterable[_Union[AmuletHookResult.AddEffectResult, _Mapping]]] = ..., remove_effect: _Optional[_Iterable[int]] = ..., add_buff: _Optional[_Iterable[int]] = ..., remove_buff: _Optional[_Iterable[int]] = ..., add_tian_dora: _Optional[_Iterable[str]] = ..., add_dora: _Optional[_Union[AmuletHookResult.AddDoraResult, _Mapping]] = ..., coin_modify: _Optional[_Union[AmuletHookResult.ValueResult, _Mapping]] = ..., tile_replace: _Optional[_Iterable[_Union[AmuletTile, _Mapping]]] = ..., add_show_tile: _Optional[_Iterable[int]] = ..., modify_tile_score: _Optional[_Iterable[_Union[AmuletTileScore, _Mapping]]] = ..., modify_desktop_count: _Optional[int] = ..., modify_show_desktop_count: _Optional[int] = ..., modify_lock_tile_count: _Optional[int] = ..., modify_change_hands_count: _Optional[int] = ..., modify_change_hands_tile_count: _Optional[int] = ..., force_moqie: _Optional[bool] = ..., replace_hu: _Optional[bool] = ..., modify_target_point: _Optional[str] = ..., upgrade_level: _Optional[bool] = ..., modify_dora: _Optional[_Iterable[_Union[AmuletHookResult.ModifyDoraResult, _Mapping]]] = ..., modify_dora_max_count: _Optional[int] = ..., modify_shop_goods_count: _Optional[int] = ..., modify_shop_rare_weight: _Optional[bool] = ..., modify_shop_goods_price: _Optional[bool] = ..., modify_shop_pack_effect: _Optional[_Iterable[int]] = ..., modify_effect_max_count: _Optional[int] = ..., modify_goods: _Optional[_Iterable[_Union[AmuletGameShopGoods, _Mapping]]] = ..., remove_goods: _Optional[_Iterable[int]] = ..., modify_base: _Optional[_Union[AmuletHookResult.ValueResult, _Mapping]] = ..., modify_fan: _Optional[_Union[AmuletHookResult.ValueResult, _Mapping]] = ..., modify_fan_info: _Optional[_Iterable[_Union[AmuletFan, _Mapping]]] = ..., transform_effect: _Optional[_Iterable[_Union[AmuletHookResult.TransformResult, _Mapping]]] = ..., add_badge: _Optional[_Iterable[_Union[AmuletHookResult.AddBadge, _Mapping]]] = ..., remove_badge: _Optional[_Iterable[int]] = ..., modify_effect_price: _Optional[str] = ..., copy_effect: _Optional[_Iterable[_Union[AmuletHookResult.CopyEffect, _Mapping]]] = ..., effect_growth: _Optional[bool] = ..., modify_tile_score_aura: _Optional[str] = ..., modify_hule_count: _Optional[int] = ..., can_gang: _Optional[bool] = ..., modify_change_hands_list: _Optional[_Iterable[int]] = ..., modify_change_desktop: _Optional[_Union[AmuletHookResult.AmuletChangeDesktopResult, _Mapping]] = ..., self_effect_id: _Optional[int] = ..., modify_change_coin: _Optional[str] = ..., set_tile_score: _Optional[_Iterable[_Union[AmuletTileScore, _Mapping]]] = ..., upgrade_effect: _Optional[_Iterable[_Union[AmuletHookResult.UpgradeEffectResult, _Mapping]]] = ..., modify_tile_base_score: _Optional[_Iterable[_Union[AmuletTileScore, _Mapping]]] = ...) -> None: ...

class AmuletMingInfo(_message.Message):
    __slots__ = ()
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TILE_LIST_FIELD_NUMBER: _ClassVar[int]
    type: int
    tile_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, type: _Optional[int] = ..., tile_list: _Optional[_Iterable[int]] = ...) -> None: ...

class AmuletMingInfoArrayDirty(_message.Message):
    __slots__ = ()
    DIRTY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    dirty: bool
    value: _containers.RepeatedCompositeFieldContainer[AmuletMingInfo]
    def __init__(self, dirty: _Optional[bool] = ..., value: _Optional[_Iterable[_Union[AmuletMingInfo, _Mapping]]] = ...) -> None: ...

class AmuletRecordDataChanges(_message.Message):
    __slots__ = ()
    YIMAN_COUNT_FIELD_NUMBER: _ClassVar[int]
    LEVEL_HU_COUNT_FIELD_NUMBER: _ClassVar[int]
    GAME_HU_COUNT_FIELD_NUMBER: _ClassVar[int]
    EFFECT_GAIN_FIELD_NUMBER: _ClassVar[int]
    COIN_CONSUME_FIELD_NUMBER: _ClassVar[int]
    COIN_GAIN_FIELD_NUMBER: _ClassVar[int]
    HIGHEST_HU_FIELD_NUMBER: _ClassVar[int]
    HIGHEST_LEVEL_SCORE_FIELD_NUMBER: _ClassVar[int]
    HIGHEST_FAN_FIELD_NUMBER: _ClassVar[int]
    PACK_COUNT_FIELD_NUMBER: _ClassVar[int]
    ROUND_COUNT_FIELD_NUMBER: _ClassVar[int]
    EFFECT_COUNTER_FIELD_NUMBER: _ClassVar[int]
    yiman_count: UInt32Dirty
    level_hu_count: UInt32Dirty
    game_hu_count: UInt32Dirty
    effect_gain: UInt32Dirty
    coin_consume: StringDirty
    coin_gain: StringDirty
    highest_hu: ActivityAmuletHuRecordDirty
    highest_level_score: StringDirty
    highest_fan: StringDirty
    pack_count: UInt32Dirty
    round_count: UInt32Dirty
    effect_counter: AmuletEffectCounterDataArrayDirty
    def __init__(self, yiman_count: _Optional[_Union[UInt32Dirty, _Mapping]] = ..., level_hu_count: _Optional[_Union[UInt32Dirty, _Mapping]] = ..., game_hu_count: _Optional[_Union[UInt32Dirty, _Mapping]] = ..., effect_gain: _Optional[_Union[UInt32Dirty, _Mapping]] = ..., coin_consume: _Optional[_Union[StringDirty, _Mapping]] = ..., coin_gain: _Optional[_Union[StringDirty, _Mapping]] = ..., highest_hu: _Optional[_Union[ActivityAmuletHuRecordDirty, _Mapping]] = ..., highest_level_score: _Optional[_Union[StringDirty, _Mapping]] = ..., highest_fan: _Optional[_Union[StringDirty, _Mapping]] = ..., pack_count: _Optional[_Union[UInt32Dirty, _Mapping]] = ..., round_count: _Optional[_Union[UInt32Dirty, _Mapping]] = ..., effect_counter: _Optional[_Union[AmuletEffectCounterDataArrayDirty, _Mapping]] = ...) -> None: ...

class AmuletRoundDataChanges(_message.Message):
    __slots__ = ()
    POOL_FIELD_NUMBER: _ClassVar[int]
    TILE_REPLACE_FIELD_NUMBER: _ClassVar[int]
    TIAN_DORA_FIELD_NUMBER: _ClassVar[int]
    DORA_FIELD_NUMBER: _ClassVar[int]
    HANDS_FIELD_NUMBER: _ClassVar[int]
    USED_DESKTOP_FIELD_NUMBER: _ClassVar[int]
    USED_FIELD_NUMBER: _ClassVar[int]
    MING_FIELD_NUMBER: _ClassVar[int]
    LOCKED_TILE_FIELD_NUMBER: _ClassVar[int]
    CHANGE_TILE_COUNT_FIELD_NUMBER: _ClassVar[int]
    TOTAL_CHANGE_TILE_COUNT_FIELD_NUMBER: _ClassVar[int]
    NEXT_OPERATION_FIELD_NUMBER: _ClassVar[int]
    TING_LIST_FIELD_NUMBER: _ClassVar[int]
    POINT_FIELD_NUMBER: _ClassVar[int]
    TARGET_POINT_FIELD_NUMBER: _ClassVar[int]
    DESKTOP_REMAIN_FIELD_NUMBER: _ClassVar[int]
    SHOW_DESKTOP_TILES_FIELD_NUMBER: _ClassVar[int]
    LOCKED_TILE_COUNT_FIELD_NUMBER: _ClassVar[int]
    pool: AmuletTileArrayDirty
    tile_replace: AmuletTileArrayDirty
    tian_dora: StringArrayDirty
    dora: UInt32ArrayDirty
    hands: UInt32ArrayDirty
    used_desktop: UInt32ArrayDirty
    used: UInt32ArrayDirty
    ming: AmuletMingInfoArrayDirty
    locked_tile: UInt32ArrayDirty
    change_tile_count: UInt32Dirty
    total_change_tile_count: UInt32Dirty
    next_operation: AmuletGameOperationArrayDirty
    ting_list: AmuletTingInfoArrayDirty
    point: StringDirty
    target_point: StringDirty
    desktop_remain: UInt32Dirty
    show_desktop_tiles: AmuletShowDesktopTileDataArrayDirty
    locked_tile_count: UInt32Dirty
    def __init__(self, pool: _Optional[_Union[AmuletTileArrayDirty, _Mapping]] = ..., tile_replace: _Optional[_Union[AmuletTileArrayDirty, _Mapping]] = ..., tian_dora: _Optional[_Union[StringArrayDirty, _Mapping]] = ..., dora: _Optional[_Union[UInt32ArrayDirty, _Mapping]] = ..., hands: _Optional[_Union[UInt32ArrayDirty, _Mapping]] = ..., used_desktop: _Optional[_Union[UInt32ArrayDirty, _Mapping]] = ..., used: _Optional[_Union[UInt32ArrayDirty, _Mapping]] = ..., ming: _Optional[_Union[AmuletMingInfoArrayDirty, _Mapping]] = ..., locked_tile: _Optional[_Union[UInt32ArrayDirty, _Mapping]] = ..., change_tile_count: _Optional[_Union[UInt32Dirty, _Mapping]] = ..., total_change_tile_count: _Optional[_Union[UInt32Dirty, _Mapping]] = ..., next_operation: _Optional[_Union[AmuletGameOperationArrayDirty, _Mapping]] = ..., ting_list: _Optional[_Union[AmuletTingInfoArrayDirty, _Mapping]] = ..., point: _Optional[_Union[StringDirty, _Mapping]] = ..., target_point: _Optional[_Union[StringDirty, _Mapping]] = ..., desktop_remain: _Optional[_Union[UInt32Dirty, _Mapping]] = ..., show_desktop_tiles: _Optional[_Union[AmuletShowDesktopTileDataArrayDirty, _Mapping]] = ..., locked_tile_count: _Optional[_Union[UInt32Dirty, _Mapping]] = ...) -> None: ...

class AmuletShopData(_message.Message):
    __slots__ = ()
    GOODS_FIELD_NUMBER: _ClassVar[int]
    CANDIDATE_EFFECT_LIST_FIELD_NUMBER: _ClassVar[int]
    SHOP_REFRESH_COUNT_FIELD_NUMBER: _ClassVar[int]
    REFRESH_PRICE_FIELD_NUMBER: _ClassVar[int]
    goods: _containers.RepeatedCompositeFieldContainer[AmuletGameShopGoods]
    candidate_effect_list: _containers.RepeatedCompositeFieldContainer[AmuletEffectCandidate]
    shop_refresh_count: int
    refresh_price: int
    def __init__(self, goods: _Optional[_Iterable[_Union[AmuletGameShopGoods, _Mapping]]] = ..., candidate_effect_list: _Optional[_Iterable[_Union[AmuletEffectCandidate, _Mapping]]] = ..., shop_refresh_count: _Optional[int] = ..., refresh_price: _Optional[int] = ...) -> None: ...

class AmuletShopDataChanges(_message.Message):
    __slots__ = ()
    GOODS_FIELD_NUMBER: _ClassVar[int]
    CANDIDATE_EFFECT_LIST_FIELD_NUMBER: _ClassVar[int]
    SHOP_REFRESH_COUNT_FIELD_NUMBER: _ClassVar[int]
    REFRESH_PRICE_FIELD_NUMBER: _ClassVar[int]
    goods: AmuletShopGoodsArrayDirty
    candidate_effect_list: AmuletEffectCandidatesArrayDirty
    shop_refresh_count: UInt32Dirty
    refresh_price: UInt32Dirty
    def __init__(self, goods: _Optional[_Union[AmuletShopGoodsArrayDirty, _Mapping]] = ..., candidate_effect_list: _Optional[_Union[AmuletEffectCandidatesArrayDirty, _Mapping]] = ..., shop_refresh_count: _Optional[_Union[UInt32Dirty, _Mapping]] = ..., refresh_price: _Optional[_Union[UInt32Dirty, _Mapping]] = ...) -> None: ...

class AmuletShopGoodsArrayDirty(_message.Message):
    __slots__ = ()
    DIRTY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    dirty: bool
    value: _containers.RepeatedCompositeFieldContainer[AmuletGameShopGoods]
    def __init__(self, dirty: _Optional[bool] = ..., value: _Optional[_Iterable[_Union[AmuletGameShopGoods, _Mapping]]] = ...) -> None: ...

class AmuletShowDesktopTileData(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    POS_FIELD_NUMBER: _ClassVar[int]
    id: int
    pos: int
    def __init__(self, id: _Optional[int] = ..., pos: _Optional[int] = ...) -> None: ...

class AmuletShowDesktopTileDataArrayDirty(_message.Message):
    __slots__ = ()
    DIRTY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    dirty: bool
    value: _containers.RepeatedCompositeFieldContainer[AmuletShowDesktopTileData]
    def __init__(self, dirty: _Optional[bool] = ..., value: _Optional[_Iterable[_Union[AmuletShowDesktopTileData, _Mapping]]] = ...) -> None: ...

class AmuletSkillData(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    id: int
    level: int
    def __init__(self, id: _Optional[int] = ..., level: _Optional[int] = ...) -> None: ...

class AmuletTile(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    TILE_FIELD_NUMBER: _ClassVar[int]
    id: int
    tile: str
    def __init__(self, id: _Optional[int] = ..., tile: _Optional[str] = ...) -> None: ...

class AmuletTileArrayDirty(_message.Message):
    __slots__ = ()
    DIRTY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    dirty: bool
    value: _containers.RepeatedCompositeFieldContainer[AmuletTile]
    def __init__(self, dirty: _Optional[bool] = ..., value: _Optional[_Iterable[_Union[AmuletTile, _Mapping]]] = ...) -> None: ...

class AmuletTileScore(_message.Message):
    __slots__ = ()
    TILE_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    tile: str
    score: str
    def __init__(self, tile: _Optional[str] = ..., score: _Optional[str] = ...) -> None: ...

class AmuletTileScoreArrayDirty(_message.Message):
    __slots__ = ()
    DIRTY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    dirty: bool
    value: _containers.RepeatedCompositeFieldContainer[AmuletTileScore]
    def __init__(self, dirty: _Optional[bool] = ..., value: _Optional[_Iterable[_Union[AmuletTileScore, _Mapping]]] = ...) -> None: ...

class AmuletTingInfoArrayDirty(_message.Message):
    __slots__ = ()
    DIRTY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    dirty: bool
    value: _containers.RepeatedCompositeFieldContainer[AmuletActivityTingInfo]
    def __init__(self, dirty: _Optional[bool] = ..., value: _Optional[_Iterable[_Union[AmuletActivityTingInfo, _Mapping]]] = ...) -> None: ...

class AmuletValueChanges(_message.Message):
    __slots__ = ()
    ROUND_FIELD_NUMBER: _ClassVar[int]
    EFFECT_FIELD_NUMBER: _ClassVar[int]
    GAME_FIELD_NUMBER: _ClassVar[int]
    STAGE_FIELD_NUMBER: _ClassVar[int]
    SHOP_FIELD_NUMBER: _ClassVar[int]
    RECORD_FIELD_NUMBER: _ClassVar[int]
    ENDED_FIELD_NUMBER: _ClassVar[int]
    round: AmuletRoundDataChanges
    effect: AmuletEffectDataChanges
    game: AmuletGameInfoDataChanges
    stage: int
    shop: AmuletShopDataChanges
    record: AmuletRecordDataChanges
    ended: bool
    def __init__(self, round: _Optional[_Union[AmuletRoundDataChanges, _Mapping]] = ..., effect: _Optional[_Union[AmuletEffectDataChanges, _Mapping]] = ..., game: _Optional[_Union[AmuletGameInfoDataChanges, _Mapping]] = ..., stage: _Optional[int] = ..., shop: _Optional[_Union[AmuletShopDataChanges, _Mapping]] = ..., record: _Optional[_Union[AmuletRecordDataChanges, _Mapping]] = ..., ended: _Optional[bool] = ...) -> None: ...

class Announcement(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    HEADER_IMAGE_FIELD_NUMBER: _ClassVar[int]
    id: int
    title: str
    content: str
    header_image: str
    def __init__(self, id: _Optional[int] = ..., title: _Optional[str] = ..., content: _Optional[str] = ..., header_image: _Optional[str] = ...) -> None: ...

class AntiAddiction(_message.Message):
    __slots__ = ()
    ONLINE_DURATION_FIELD_NUMBER: _ClassVar[int]
    online_duration: int
    def __init__(self, online_duration: _Optional[int] = ...) -> None: ...

class BadgeAchieveProgress(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    COUNTER_FIELD_NUMBER: _ClassVar[int]
    ACHIEVED_COUNTER_FIELD_NUMBER: _ClassVar[int]
    ACHIEVED_TIME_FIELD_NUMBER: _ClassVar[int]
    id: int
    counter: int
    achieved_counter: int
    achieved_time: int
    def __init__(self, id: _Optional[int] = ..., counter: _Optional[int] = ..., achieved_counter: _Optional[int] = ..., achieved_time: _Optional[int] = ...) -> None: ...

class Bag(_message.Message):
    __slots__ = ()
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    DAILY_GAIN_RECORD_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[Item]
    daily_gain_record: _containers.RepeatedCompositeFieldContainer[ItemGainRecords]
    def __init__(self, items: _Optional[_Iterable[_Union[Item, _Mapping]]] = ..., daily_gain_record: _Optional[_Iterable[_Union[ItemGainRecords, _Mapping]]] = ...) -> None: ...

class BagUpdate(_message.Message):
    __slots__ = ()
    UPDATE_ITEMS_FIELD_NUMBER: _ClassVar[int]
    UPDATE_DAILY_GAIN_RECORD_FIELD_NUMBER: _ClassVar[int]
    update_items: _containers.RepeatedCompositeFieldContainer[Item]
    update_daily_gain_record: _containers.RepeatedCompositeFieldContainer[ItemGainRecords]
    def __init__(self, update_items: _Optional[_Iterable[_Union[Item, _Mapping]]] = ..., update_daily_gain_record: _Optional[_Iterable[_Union[ItemGainRecords, _Mapping]]] = ...) -> None: ...

class BillShortcut(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    DEALPRICE_FIELD_NUMBER: _ClassVar[int]
    id: int
    count: int
    dealPrice: int
    def __init__(self, id: _Optional[int] = ..., count: _Optional[int] = ..., dealPrice: _Optional[int] = ...) -> None: ...

class BillingGoods(_message.Message):
    __slots__ = ()
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

class BillingProduct(_message.Message):
    __slots__ = ()
    GOODS_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_CODE_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_PRICE_FIELD_NUMBER: _ClassVar[int]
    SORT_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    goods: BillingGoods
    currency_code: str
    currency_price: int
    sort_weight: int
    def __init__(self, goods: _Optional[_Union[BillingGoods, _Mapping]] = ..., currency_code: _Optional[str] = ..., currency_price: _Optional[int] = ..., sort_weight: _Optional[int] = ...) -> None: ...

class BuyRecord(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    id: int
    count: int
    def __init__(self, id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class ChangeNicknameRecord(_message.Message):
    __slots__ = ()
    FROM_FIELD_NUMBER: _ClassVar[int]
    TO_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    to: str
    time: int
    def __init__(self, to: _Optional[str] = ..., time: _Optional[int] = ..., **kwargs) -> None: ...

class Character(_message.Message):
    __slots__ = ()
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
    def __init__(self, charid: _Optional[int] = ..., level: _Optional[int] = ..., exp: _Optional[int] = ..., views: _Optional[_Iterable[_Union[ViewSlot, _Mapping]]] = ..., skin: _Optional[int] = ..., is_upgraded: _Optional[bool] = ..., extra_emoji: _Optional[_Iterable[int]] = ..., rewarded_level: _Optional[_Iterable[int]] = ...) -> None: ...

class ChestData(_message.Message):
    __slots__ = ()
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
    __slots__ = ()
    CHEST_ID_FIELD_NUMBER: _ClassVar[int]
    TOTAL_OPEN_COUNT_FIELD_NUMBER: _ClassVar[int]
    FACE_BLACK_COUNT_FIELD_NUMBER: _ClassVar[int]
    TICKET_FACE_BLACK_COUNT_FIELD_NUMBER: _ClassVar[int]
    chest_id: int
    total_open_count: int
    face_black_count: int
    ticket_face_black_count: int
    def __init__(self, chest_id: _Optional[int] = ..., total_open_count: _Optional[int] = ..., face_black_count: _Optional[int] = ..., ticket_face_black_count: _Optional[int] = ...) -> None: ...

class ChuanmaGang(_message.Message):
    __slots__ = ()
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

class ClientDeviceInfo(_message.Message):
    __slots__ = ()
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
    USER_AGENT_FIELD_NUMBER: _ClassVar[int]
    SCREEN_TYPE_FIELD_NUMBER: _ClassVar[int]
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
    user_agent: str
    screen_type: int
    def __init__(self, platform: _Optional[str] = ..., hardware: _Optional[str] = ..., os: _Optional[str] = ..., os_version: _Optional[str] = ..., is_browser: _Optional[bool] = ..., software: _Optional[str] = ..., sale_platform: _Optional[str] = ..., hardware_vendor: _Optional[str] = ..., model_number: _Optional[str] = ..., screen_width: _Optional[int] = ..., screen_height: _Optional[int] = ..., user_agent: _Optional[str] = ..., screen_type: _Optional[int] = ...) -> None: ...

class ClientVersionInfo(_message.Message):
    __slots__ = ()
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    PACKAGE_FIELD_NUMBER: _ClassVar[int]
    resource: str
    package: str
    def __init__(self, resource: _Optional[str] = ..., package: _Optional[str] = ...) -> None: ...

class CommentItem(_message.Message):
    __slots__ = ()
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

class ContestDetailRule(_message.Message):
    __slots__ = ()
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
    def __init__(self, init_point: _Optional[int] = ..., fandian: _Optional[int] = ..., can_jifei: _Optional[bool] = ..., tianbian_value: _Optional[int] = ..., liqibang_value: _Optional[int] = ..., changbang_value: _Optional[int] = ..., noting_fafu_1: _Optional[int] = ..., noting_fafu_2: _Optional[int] = ..., noting_fafu_3: _Optional[int] = ..., have_liujumanguan: _Optional[bool] = ..., have_qieshangmanguan: _Optional[bool] = ..., have_biao_dora: _Optional[bool] = ..., have_gang_biao_dora: _Optional[bool] = ..., ming_dora_immediately_open: _Optional[bool] = ..., have_li_dora: _Optional[bool] = ..., have_gang_li_dora: _Optional[bool] = ..., have_sifenglianda: _Optional[bool] = ..., have_sigangsanle: _Optional[bool] = ..., have_sijializhi: _Optional[bool] = ..., have_jiuzhongjiupai: _Optional[bool] = ..., have_sanjiahele: _Optional[bool] = ..., have_toutiao: _Optional[bool] = ..., have_helelianzhuang: _Optional[bool] = ..., have_helezhongju: _Optional[bool] = ..., have_tingpailianzhuang: _Optional[bool] = ..., have_tingpaizhongju: _Optional[bool] = ..., have_yifa: _Optional[bool] = ..., have_nanruxiru: _Optional[bool] = ..., jingsuanyuandian: _Optional[int] = ..., shunweima_2: _Optional[int] = ..., shunweima_3: _Optional[int] = ..., shunweima_4: _Optional[int] = ..., bianjietishi: _Optional[bool] = ..., ai_level: _Optional[int] = ..., have_zimosun: _Optional[bool] = ..., disable_multi_yukaman: _Optional[bool] = ..., guyi_mode: _Optional[int] = ..., disable_leijiyiman: _Optional[bool] = ..., dora3_mode: _Optional[int] = ..., xuezhandaodi: _Optional[int] = ..., huansanzhang: _Optional[int] = ..., chuanma: _Optional[int] = ..., disable_double_yakuman: _Optional[int] = ..., disable_composite_yakuman: _Optional[int] = ..., enable_shiti: _Optional[int] = ..., enable_nontsumo_liqi: _Optional[int] = ..., disable_double_wind_four_fu: _Optional[int] = ..., disable_angang_guoshi: _Optional[int] = ..., enable_renhe: _Optional[int] = ..., enable_baopai_extend_settings: _Optional[int] = ..., fanfu: _Optional[int] = ...) -> None: ...

class ContestDetailRuleV2(_message.Message):
    __slots__ = ()
    class ExtraRule(_message.Message):
        __slots__ = ()
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

class ContestGameMetaData(_message.Message):
    __slots__ = ()
    class ContestTypeZoneData(_message.Message):
        __slots__ = ()
        ZONE_FIELD_NUMBER: _ClassVar[int]
        CONTEST_TYPE_FIELD_NUMBER: _ClassVar[int]
        zone: int
        contest_type: int
        def __init__(self, zone: _Optional[int] = ..., contest_type: _Optional[int] = ...) -> None: ...
    TYPE_LIST_FIELD_NUMBER: _ClassVar[int]
    RANK_TYPE_FIELD_NUMBER: _ClassVar[int]
    type_list: _containers.RepeatedCompositeFieldContainer[ContestGameMetaData.ContestTypeZoneData]
    rank_type: int
    def __init__(self, type_list: _Optional[_Iterable[_Union[ContestGameMetaData.ContestTypeZoneData, _Mapping]]] = ..., rank_type: _Optional[int] = ...) -> None: ...

class ContestSetting(_message.Message):
    __slots__ = ()
    class LevelLimit(_message.Message):
        __slots__ = ()
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

class CustomizedContestAbstract(_message.Message):
    __slots__ = ()
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
    def __init__(self, unique_id: _Optional[int] = ..., contest_id: _Optional[int] = ..., contest_name: _Optional[str] = ..., state: _Optional[int] = ..., creator_id: _Optional[int] = ..., create_time: _Optional[int] = ..., start_time: _Optional[int] = ..., finish_time: _Optional[int] = ..., open: _Optional[bool] = ..., public_notice: _Optional[str] = ..., contest_type: _Optional[int] = ...) -> None: ...

class CustomizedContestBase(_message.Message):
    __slots__ = ()
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
    RANK_TYPE_FIELD_NUMBER: _ClassVar[int]
    SHOW_TEAM_RANK_FIELD_NUMBER: _ClassVar[int]
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
    rank_type: int
    show_team_rank: bool
    def __init__(self, unique_id: _Optional[int] = ..., contest_id: _Optional[int] = ..., contest_name: _Optional[str] = ..., state: _Optional[int] = ..., creator_id: _Optional[int] = ..., create_time: _Optional[int] = ..., start_time: _Optional[int] = ..., finish_time: _Optional[int] = ..., open: _Optional[bool] = ..., contest_type: _Optional[int] = ..., public_notice: _Optional[str] = ..., check_state: _Optional[int] = ..., checking_name: _Optional[str] = ..., rank_type: _Optional[int] = ..., show_team_rank: _Optional[bool] = ...) -> None: ...

class CustomizedContestDetail(_message.Message):
    __slots__ = ()
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
    RANK_TYPE_FIELD_NUMBER: _ClassVar[int]
    SHOW_TEAM_RANK_FIELD_NUMBER: _ClassVar[int]
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
    rank_type: int
    show_team_rank: bool
    def __init__(self, unique_id: _Optional[int] = ..., contest_id: _Optional[int] = ..., contest_name: _Optional[str] = ..., state: _Optional[int] = ..., creator_id: _Optional[int] = ..., create_time: _Optional[int] = ..., start_time: _Optional[int] = ..., finish_time: _Optional[int] = ..., open: _Optional[bool] = ..., rank_rule: _Optional[int] = ..., game_mode: _Optional[_Union[GameMode, _Mapping]] = ..., private_notice: _Optional[str] = ..., observer_switch: _Optional[int] = ..., emoji_switch: _Optional[int] = ..., contest_type: _Optional[int] = ..., disable_broadcast: _Optional[int] = ..., signup_start_time: _Optional[int] = ..., signup_end_time: _Optional[int] = ..., signup_type: _Optional[int] = ..., auto_match: _Optional[int] = ..., rank_type: _Optional[int] = ..., show_team_rank: _Optional[bool] = ...) -> None: ...

class CustomizedContestExtend(_message.Message):
    __slots__ = ()
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_NOTICE_FIELD_NUMBER: _ClassVar[int]
    unique_id: int
    public_notice: str
    def __init__(self, unique_id: _Optional[int] = ..., public_notice: _Optional[str] = ...) -> None: ...

class CustomizedContestGameEnd(_message.Message):
    __slots__ = ()
    class Item(_message.Message):
        __slots__ = ()
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

class CustomizedContestGameStart(_message.Message):
    __slots__ = ()
    class Item(_message.Message):
        __slots__ = ()
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        NICKNAME_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        nickname: str
        def __init__(self, account_id: _Optional[int] = ..., nickname: _Optional[str] = ...) -> None: ...
    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    players: _containers.RepeatedCompositeFieldContainer[CustomizedContestGameStart.Item]
    def __init__(self, players: _Optional[_Iterable[_Union[CustomizedContestGameStart.Item, _Mapping]]] = ...) -> None: ...

class CustomizedContestPlayerReport(_message.Message):
    __slots__ = ()
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

class Error(_message.Message):
    __slots__ = ()
    CODE_FIELD_NUMBER: _ClassVar[int]
    U32_PARAMS_FIELD_NUMBER: _ClassVar[int]
    STR_PARAMS_FIELD_NUMBER: _ClassVar[int]
    JSON_PARAM_FIELD_NUMBER: _ClassVar[int]
    code: int
    u32_params: _containers.RepeatedScalarFieldContainer[int]
    str_params: _containers.RepeatedScalarFieldContainer[str]
    json_param: str
    def __init__(self, code: _Optional[int] = ..., u32_params: _Optional[_Iterable[int]] = ..., str_params: _Optional[_Iterable[str]] = ..., json_param: _Optional[str] = ...) -> None: ...

class ExchangeRecord(_message.Message):
    __slots__ = ()
    EXCHANGE_ID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    exchange_id: int
    count: int
    def __init__(self, exchange_id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class ExecuteResult(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    id: int
    count: int
    def __init__(self, id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class ExecuteReward(_message.Message):
    __slots__ = ()
    REWARD_FIELD_NUMBER: _ClassVar[int]
    REPLACE_FIELD_NUMBER: _ClassVar[int]
    REPLACE_COUNT_FIELD_NUMBER: _ClassVar[int]
    reward: RewardSlot
    replace: RewardSlot
    replace_count: int
    def __init__(self, reward: _Optional[_Union[RewardSlot, _Mapping]] = ..., replace: _Optional[_Union[RewardSlot, _Mapping]] = ..., replace_count: _Optional[int] = ...) -> None: ...

class FaithData(_message.Message):
    __slots__ = ()
    FAITH_ID_FIELD_NUMBER: _ClassVar[int]
    TOTAL_OPEN_COUNT_FIELD_NUMBER: _ClassVar[int]
    CONSUME_COUNT_FIELD_NUMBER: _ClassVar[int]
    MODIFY_COUNT_FIELD_NUMBER: _ClassVar[int]
    faith_id: int
    total_open_count: int
    consume_count: int
    modify_count: int
    def __init__(self, faith_id: _Optional[int] = ..., total_open_count: _Optional[int] = ..., consume_count: _Optional[int] = ..., modify_count: _Optional[int] = ...) -> None: ...

class FakeRandomRecords(_message.Message):
    __slots__ = ()
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    SPECIAL_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    GAIN_COUNT_FIELD_NUMBER: _ClassVar[int]
    GAIN_HISTORY_FIELD_NUMBER: _ClassVar[int]
    item_id: int
    special_item_id: int
    gain_count: int
    gain_history: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, item_id: _Optional[int] = ..., special_item_id: _Optional[int] = ..., gain_count: _Optional[int] = ..., gain_history: _Optional[_Iterable[int]] = ...) -> None: ...

class FanInfo(_message.Message):
    __slots__ = ()
    NAME_FIELD_NUMBER: _ClassVar[int]
    VAL_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    val: int
    id: int
    def __init__(self, name: _Optional[str] = ..., val: _Optional[int] = ..., id: _Optional[int] = ...) -> None: ...

class FavoriteHu(_message.Message):
    __slots__ = ()
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    HU_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    category: int
    type: int
    hu: HighestHuRecord
    mode: int
    def __init__(self, category: _Optional[int] = ..., type: _Optional[int] = ..., hu: _Optional[_Union[HighestHuRecord, _Mapping]] = ..., mode: _Optional[int] = ...) -> None: ...

class FeedActivityData(_message.Message):
    __slots__ = ()
    class CountWithTimeData(_message.Message):
        __slots__ = ()
        COUNT_FIELD_NUMBER: _ClassVar[int]
        LAST_UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
        count: int
        last_update_time: int
        def __init__(self, count: _Optional[int] = ..., last_update_time: _Optional[int] = ...) -> None: ...
    class GiftBoxData(_message.Message):
        __slots__ = ()
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

class FestivalProposalData(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    PROPOSAL_ID_FIELD_NUMBER: _ClassVar[int]
    POS_FIELD_NUMBER: _ClassVar[int]
    id: int
    proposal_id: int
    pos: int
    def __init__(self, id: _Optional[int] = ..., proposal_id: _Optional[int] = ..., pos: _Optional[int] = ...) -> None: ...

class Friend(_message.Message):
    __slots__ = ()
    BASE_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    REMARK_FIELD_NUMBER: _ClassVar[int]
    base: PlayerBaseView
    state: AccountActiveState
    remark: str
    def __init__(self, base: _Optional[_Union[PlayerBaseView, _Mapping]] = ..., state: _Optional[_Union[AccountActiveState, _Mapping]] = ..., remark: _Optional[str] = ...) -> None: ...

class GachaRecord(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    id: int
    count: int
    def __init__(self, id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class GameAction(_message.Message):
    __slots__ = ()
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

class GameChiPengGang(_message.Message):
    __slots__ = ()
    TYPE_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    CANCEL_OPERATION_FIELD_NUMBER: _ClassVar[int]
    TIMEUSE_FIELD_NUMBER: _ClassVar[int]
    type: int
    index: int
    cancel_operation: bool
    timeuse: int
    def __init__(self, type: _Optional[int] = ..., index: _Optional[int] = ..., cancel_operation: _Optional[bool] = ..., timeuse: _Optional[int] = ...) -> None: ...

class GameConfig(_message.Message):
    __slots__ = ()
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    META_FIELD_NUMBER: _ClassVar[int]
    category: int
    mode: GameMode
    meta: GameMetaData
    def __init__(self, category: _Optional[int] = ..., mode: _Optional[_Union[GameMode, _Mapping]] = ..., meta: _Optional[_Union[GameMetaData, _Mapping]] = ...) -> None: ...

class GameConnectInfo(_message.Message):
    __slots__ = ()
    CONNECT_TOKEN_FIELD_NUMBER: _ClassVar[int]
    GAME_UUID_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    connect_token: str
    game_uuid: str
    location: str
    def __init__(self, connect_token: _Optional[str] = ..., game_uuid: _Optional[str] = ..., location: _Optional[str] = ...) -> None: ...

class GameDetailRecords(_message.Message):
    __slots__ = ()
    RECORDS_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    ACTIONS_FIELD_NUMBER: _ClassVar[int]
    BAR_FIELD_NUMBER: _ClassVar[int]
    records: _containers.RepeatedScalarFieldContainer[bytes]
    version: int
    actions: _containers.RepeatedCompositeFieldContainer[GameAction]
    bar: bytes
    def __init__(self, records: _Optional[_Iterable[bytes]] = ..., version: _Optional[int] = ..., actions: _Optional[_Iterable[_Union[GameAction, _Mapping]]] = ..., bar: _Optional[bytes] = ...) -> None: ...

class GameDetailRule(_message.Message):
    __slots__ = ()
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
    WANXIANGXIULUO_MODE_FIELD_NUMBER: _ClassVar[int]
    BEISHUIZHIZHAN_MODE_FIELD_NUMBER: _ClassVar[int]
    AMUSEMENT_SWITCHES_FIELD_NUMBER: _ClassVar[int]
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
    wanxiangxiuluo_mode: int
    beishuizhizhan_mode: int
    amusement_switches: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, time_fixed: _Optional[int] = ..., time_add: _Optional[int] = ..., dora_count: _Optional[int] = ..., shiduan: _Optional[int] = ..., init_point: _Optional[int] = ..., fandian: _Optional[int] = ..., can_jifei: _Optional[bool] = ..., tianbian_value: _Optional[int] = ..., liqibang_value: _Optional[int] = ..., changbang_value: _Optional[int] = ..., noting_fafu_1: _Optional[int] = ..., noting_fafu_2: _Optional[int] = ..., noting_fafu_3: _Optional[int] = ..., have_liujumanguan: _Optional[bool] = ..., have_qieshangmanguan: _Optional[bool] = ..., have_biao_dora: _Optional[bool] = ..., have_gang_biao_dora: _Optional[bool] = ..., ming_dora_immediately_open: _Optional[bool] = ..., have_li_dora: _Optional[bool] = ..., have_gang_li_dora: _Optional[bool] = ..., have_sifenglianda: _Optional[bool] = ..., have_sigangsanle: _Optional[bool] = ..., have_sijializhi: _Optional[bool] = ..., have_jiuzhongjiupai: _Optional[bool] = ..., have_sanjiahele: _Optional[bool] = ..., have_toutiao: _Optional[bool] = ..., have_helelianzhuang: _Optional[bool] = ..., have_helezhongju: _Optional[bool] = ..., have_tingpailianzhuang: _Optional[bool] = ..., have_tingpaizhongju: _Optional[bool] = ..., have_yifa: _Optional[bool] = ..., have_nanruxiru: _Optional[bool] = ..., jingsuanyuandian: _Optional[int] = ..., shunweima_2: _Optional[int] = ..., shunweima_3: _Optional[int] = ..., shunweima_4: _Optional[int] = ..., bianjietishi: _Optional[bool] = ..., ai_level: _Optional[int] = ..., have_zimosun: _Optional[bool] = ..., disable_multi_yukaman: _Optional[bool] = ..., fanfu: _Optional[int] = ..., guyi_mode: _Optional[int] = ..., dora3_mode: _Optional[int] = ..., begin_open_mode: _Optional[int] = ..., jiuchao_mode: _Optional[int] = ..., muyu_mode: _Optional[int] = ..., open_hand: _Optional[int] = ..., xuezhandaodi: _Optional[int] = ..., huansanzhang: _Optional[int] = ..., chuanma: _Optional[int] = ..., reveal_discard: _Optional[int] = ..., field_spell_mode: _Optional[int] = ..., zhanxing: _Optional[int] = ..., tianming_mode: _Optional[int] = ..., disable_leijiyiman: _Optional[bool] = ..., disable_double_yakuman: _Optional[int] = ..., disable_composite_yakuman: _Optional[int] = ..., enable_shiti: _Optional[int] = ..., enable_nontsumo_liqi: _Optional[int] = ..., disable_double_wind_four_fu: _Optional[int] = ..., disable_angang_guoshi: _Optional[int] = ..., enable_renhe: _Optional[int] = ..., enable_baopai_extend_settings: _Optional[int] = ..., yongchang_mode: _Optional[int] = ..., hunzhiyiji_mode: _Optional[int] = ..., wanxiangxiuluo_mode: _Optional[int] = ..., beishuizhizhan_mode: _Optional[int] = ..., amusement_switches: _Optional[_Iterable[int]] = ...) -> None: ...

class GameEnd(_message.Message):
    __slots__ = ()
    SCORES_FIELD_NUMBER: _ClassVar[int]
    scores: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, scores: _Optional[_Iterable[int]] = ...) -> None: ...

class GameEndAction(_message.Message):
    __slots__ = ()
    STATE_FIELD_NUMBER: _ClassVar[int]
    state: int
    def __init__(self, state: _Optional[int] = ...) -> None: ...

class GameEndResult(_message.Message):
    __slots__ = ()
    class PlayerItem(_message.Message):
        __slots__ = ()
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

class GameFinalSnapshot(_message.Message):
    __slots__ = ()
    class CalculateParam(_message.Message):
        __slots__ = ()
        INIT_POINT_FIELD_NUMBER: _ClassVar[int]
        JINGSUANYUANDIAN_FIELD_NUMBER: _ClassVar[int]
        RANK_POINTS_FIELD_NUMBER: _ClassVar[int]
        init_point: int
        jingsuanyuandian: int
        rank_points: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, init_point: _Optional[int] = ..., jingsuanyuandian: _Optional[int] = ..., rank_points: _Optional[_Iterable[int]] = ...) -> None: ...
    class GameSeat(_message.Message):
        __slots__ = ()
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
        def __init__(self, type: _Optional[int] = ..., account_id: _Optional[int] = ..., notify_endpoint: _Optional[_Union[NetworkEndpoint, _Mapping]] = ..., client_address: _Optional[str] = ..., is_connected: _Optional[bool] = ...) -> None: ...
    class FinalPlayer(_message.Message):
        __slots__ = ()
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
        __slots__ = ()
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
    ROBOT_VIEWS_FIELD_NUMBER: _ClassVar[int]
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
    robot_views: _containers.RepeatedCompositeFieldContainer[PlayerGameView]
    def __init__(self, uuid: _Optional[str] = ..., state: _Optional[int] = ..., category: _Optional[int] = ..., mode: _Optional[_Union[GameMode, _Mapping]] = ..., meta: _Optional[_Union[GameMetaData, _Mapping]] = ..., calculate_param: _Optional[_Union[GameFinalSnapshot.CalculateParam, _Mapping]] = ..., create_time: _Optional[int] = ..., start_time: _Optional[int] = ..., finish_time: _Optional[int] = ..., seats: _Optional[_Iterable[_Union[GameFinalSnapshot.GameSeat, _Mapping]]] = ..., rounds: _Optional[_Iterable[_Union[GameRoundSnapshot, _Mapping]]] = ..., account_views: _Optional[_Iterable[_Union[PlayerGameView, _Mapping]]] = ..., final_players: _Optional[_Iterable[_Union[GameFinalSnapshot.FinalPlayer, _Mapping]]] = ..., afk_info: _Optional[_Iterable[_Union[GameFinalSnapshot.AFKInfo, _Mapping]]] = ..., robot_views: _Optional[_Iterable[_Union[PlayerGameView, _Mapping]]] = ...) -> None: ...

class GameLiveHead(_message.Message):
    __slots__ = ()
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

class GameLiveSegment(_message.Message):
    __slots__ = ()
    ACTIONS_FIELD_NUMBER: _ClassVar[int]
    actions: _containers.RepeatedCompositeFieldContainer[GameLiveUnit]
    def __init__(self, actions: _Optional[_Iterable[_Union[GameLiveUnit, _Mapping]]] = ...) -> None: ...

class GameLiveSegmentUri(_message.Message):
    __slots__ = ()
    SEGMENT_ID_FIELD_NUMBER: _ClassVar[int]
    SEGMENT_URI_FIELD_NUMBER: _ClassVar[int]
    segment_id: int
    segment_uri: str
    def __init__(self, segment_id: _Optional[int] = ..., segment_uri: _Optional[str] = ...) -> None: ...

class GameLiveUnit(_message.Message):
    __slots__ = ()
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    ACTION_CATEGORY_FIELD_NUMBER: _ClassVar[int]
    ACTION_DATA_FIELD_NUMBER: _ClassVar[int]
    timestamp: int
    action_category: int
    action_data: bytes
    def __init__(self, timestamp: _Optional[int] = ..., action_category: _Optional[int] = ..., action_data: _Optional[bytes] = ...) -> None: ...

class GameMetaData(_message.Message):
    __slots__ = ()
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    MODE_ID_FIELD_NUMBER: _ClassVar[int]
    CONTEST_UID_FIELD_NUMBER: _ClassVar[int]
    CONTEST_INFO_FIELD_NUMBER: _ClassVar[int]
    room_id: int
    mode_id: int
    contest_uid: int
    contest_info: ContestGameMetaData
    def __init__(self, room_id: _Optional[int] = ..., mode_id: _Optional[int] = ..., contest_uid: _Optional[int] = ..., contest_info: _Optional[_Union[ContestGameMetaData, _Mapping]] = ...) -> None: ...

class GameMode(_message.Message):
    __slots__ = ()
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
    def __init__(self, mode: _Optional[int] = ..., ai: _Optional[bool] = ..., extendinfo: _Optional[str] = ..., detail_rule: _Optional[_Union[GameDetailRule, _Mapping]] = ..., testing_environment: _Optional[_Union[GameTestingEnvironmentSet, _Mapping]] = ..., game_setting: _Optional[_Union[GameSetting, _Mapping]] = ...) -> None: ...

class GameNewRoundState(_message.Message):
    __slots__ = ()
    SEAT_STATES_FIELD_NUMBER: _ClassVar[int]
    seat_states: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, seat_states: _Optional[_Iterable[int]] = ...) -> None: ...

class GameNoopAction(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GameRestore(_message.Message):
    __slots__ = ()
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

class GameRoundHuData(_message.Message):
    __slots__ = ()
    class HuPai(_message.Message):
        __slots__ = ()
        TILE_FIELD_NUMBER: _ClassVar[int]
        SEAT_FIELD_NUMBER: _ClassVar[int]
        LIQI_FIELD_NUMBER: _ClassVar[int]
        tile: str
        seat: int
        liqi: int
        def __init__(self, tile: _Optional[str] = ..., seat: _Optional[int] = ..., liqi: _Optional[int] = ...) -> None: ...
    class Fan(_message.Message):
        __slots__ = ()
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
    PAI_LEFT_COUNT_FIELD_NUMBER: _ClassVar[int]
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
    pai_left_count: int
    def __init__(self, hupai: _Optional[_Union[GameRoundHuData.HuPai, _Mapping]] = ..., fans: _Optional[_Iterable[_Union[GameRoundHuData.Fan, _Mapping]]] = ..., score: _Optional[int] = ..., xun: _Optional[int] = ..., title_id: _Optional[int] = ..., fan_sum: _Optional[int] = ..., fu_sum: _Optional[int] = ..., yakuman_count: _Optional[int] = ..., biao_dora_count: _Optional[int] = ..., red_dora_count: _Optional[int] = ..., li_dora_count: _Optional[int] = ..., babei_count: _Optional[int] = ..., xuan_shang_count: _Optional[int] = ..., pai_left_count: _Optional[int] = ...) -> None: ...

class GameRoundPlayer(_message.Message):
    __slots__ = ()
    SCORE_FIELD_NUMBER: _ClassVar[int]
    RANK_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    score: int
    rank: int
    result: GameRoundPlayerResult
    def __init__(self, score: _Optional[int] = ..., rank: _Optional[int] = ..., result: _Optional[_Union[GameRoundPlayerResult, _Mapping]] = ...) -> None: ...

class GameRoundPlayerFangChongInfo(_message.Message):
    __slots__ = ()
    SEAT_FIELD_NUMBER: _ClassVar[int]
    TILE_FIELD_NUMBER: _ClassVar[int]
    PAI_LEFT_COUNT_FIELD_NUMBER: _ClassVar[int]
    seat: int
    tile: str
    pai_left_count: int
    def __init__(self, seat: _Optional[int] = ..., tile: _Optional[str] = ..., pai_left_count: _Optional[int] = ...) -> None: ...

class GameRoundPlayerResult(_message.Message):
    __slots__ = ()
    TYPE_FIELD_NUMBER: _ClassVar[int]
    HANDS_FIELD_NUMBER: _ClassVar[int]
    MING_FIELD_NUMBER: _ClassVar[int]
    LIQI_TYPE_FIELD_NUMBER: _ClassVar[int]
    IS_FULU_FIELD_NUMBER: _ClassVar[int]
    IS_LIUJUMANGUAN_FIELD_NUMBER: _ClassVar[int]
    LIAN_ZHUANG_FIELD_NUMBER: _ClassVar[int]
    HU_FIELD_NUMBER: _ClassVar[int]
    FANGCHONGS_FIELD_NUMBER: _ClassVar[int]
    LIQI_FANGCHONG_FIELD_NUMBER: _ClassVar[int]
    LIQI_FAILED_FIELD_NUMBER: _ClassVar[int]
    type: int
    hands: _containers.RepeatedScalarFieldContainer[str]
    ming: _containers.RepeatedScalarFieldContainer[str]
    liqi_type: int
    is_fulu: bool
    is_liujumanguan: bool
    lian_zhuang: int
    hu: GameRoundHuData
    fangchongs: _containers.RepeatedCompositeFieldContainer[GameRoundPlayerFangChongInfo]
    liqi_fangchong: bool
    liqi_failed: bool
    def __init__(self, type: _Optional[int] = ..., hands: _Optional[_Iterable[str]] = ..., ming: _Optional[_Iterable[str]] = ..., liqi_type: _Optional[int] = ..., is_fulu: _Optional[bool] = ..., is_liujumanguan: _Optional[bool] = ..., lian_zhuang: _Optional[int] = ..., hu: _Optional[_Union[GameRoundHuData, _Mapping]] = ..., fangchongs: _Optional[_Iterable[_Union[GameRoundPlayerFangChongInfo, _Mapping]]] = ..., liqi_fangchong: _Optional[bool] = ..., liqi_failed: _Optional[bool] = ...) -> None: ...

class GameRoundSnapshot(_message.Message):
    __slots__ = ()
    JU_FIELD_NUMBER: _ClassVar[int]
    BEN_FIELD_NUMBER: _ClassVar[int]
    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    ju: int
    ben: int
    players: _containers.RepeatedCompositeFieldContainer[GameRoundPlayer]
    def __init__(self, ju: _Optional[int] = ..., ben: _Optional[int] = ..., players: _Optional[_Iterable[_Union[GameRoundPlayer, _Mapping]]] = ...) -> None: ...

class GameRuleSetting(_message.Message):
    __slots__ = ()
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
    def __init__(self, round_type: _Optional[int] = ..., shiduan: _Optional[bool] = ..., dora_count: _Optional[int] = ..., thinking_type: _Optional[int] = ..., use_detail_rule: _Optional[bool] = ..., detail_rule_v2: _Optional[_Union[ContestDetailRuleV2, _Mapping]] = ...) -> None: ...

class GameSelfOperation(_message.Message):
    __slots__ = ()
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
    def __init__(self, type: _Optional[int] = ..., index: _Optional[int] = ..., tile: _Optional[str] = ..., cancel_operation: _Optional[bool] = ..., moqie: _Optional[bool] = ..., timeuse: _Optional[int] = ..., tile_state: _Optional[int] = ..., change_tiles: _Optional[_Iterable[str]] = ..., tile_states: _Optional[_Iterable[int]] = ..., gap_type: _Optional[int] = ...) -> None: ...

class GameSetting(_message.Message):
    __slots__ = ()
    EMOJI_SWITCH_FIELD_NUMBER: _ClassVar[int]
    emoji_switch: int
    def __init__(self, emoji_switch: _Optional[int] = ...) -> None: ...

class GameSnapshot(_message.Message):
    __slots__ = ()
    class PlayerSnapshot(_message.Message):
        __slots__ = ()
        class Fulu(_message.Message):
            __slots__ = ()
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
    def __init__(self, chang: _Optional[int] = ..., ju: _Optional[int] = ..., ben: _Optional[int] = ..., index_player: _Optional[int] = ..., left_tile_count: _Optional[int] = ..., hands: _Optional[_Iterable[str]] = ..., doras: _Optional[_Iterable[str]] = ..., liqibang: _Optional[int] = ..., players: _Optional[_Iterable[_Union[GameSnapshot.PlayerSnapshot, _Mapping]]] = ..., zhenting: _Optional[bool] = ...) -> None: ...

class GameTestingEnvironmentSet(_message.Message):
    __slots__ = ()
    PAIXING_FIELD_NUMBER: _ClassVar[int]
    LEFT_COUNT_FIELD_NUMBER: _ClassVar[int]
    FIELD_SPELL_VAR_FIELD_NUMBER: _ClassVar[int]
    paixing: int
    left_count: int
    field_spell_var: int
    def __init__(self, paixing: _Optional[int] = ..., left_count: _Optional[int] = ..., field_spell_var: _Optional[int] = ...) -> None: ...

class GameUserEvent(_message.Message):
    __slots__ = ()
    SEAT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    seat: int
    type: int
    def __init__(self, seat: _Optional[int] = ..., type: _Optional[int] = ...) -> None: ...

class GameUserInput(_message.Message):
    __slots__ = ()
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

class GameVoteGameEnd(_message.Message):
    __slots__ = ()
    YES_FIELD_NUMBER: _ClassVar[int]
    yes: bool
    def __init__(self, yes: _Optional[bool] = ...) -> None: ...

class HighestHuRecord(_message.Message):
    __slots__ = ()
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

class HuInfoXueZhanMid(_message.Message):
    __slots__ = ()
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
    def __init__(self, seat: _Optional[int] = ..., hand_count: _Optional[int] = ..., hand: _Optional[_Iterable[str]] = ..., ming: _Optional[_Iterable[str]] = ..., hu_tile: _Optional[str] = ..., zimo: _Optional[bool] = ..., yiman: _Optional[bool] = ..., count: _Optional[int] = ..., fans: _Optional[_Iterable[_Union[FanInfo, _Mapping]]] = ..., fu: _Optional[int] = ..., title_id: _Optional[int] = ...) -> None: ...

class HuleInfo(_message.Message):
    __slots__ = ()
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
    BAIDA_CHANGED_FIELD_NUMBER: _ClassVar[int]
    HU_TILE_BAIDA_CHANGED_FIELD_NUMBER: _ClassVar[int]
    XIA_KE_SHANG_COEFFICIENT_FIELD_NUMBER: _ClassVar[int]
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
    baida_changed: _containers.RepeatedScalarFieldContainer[str]
    hu_tile_baiDa_changed: str
    xia_ke_shang_coefficient: int
    def __init__(self, hand: _Optional[_Iterable[str]] = ..., ming: _Optional[_Iterable[str]] = ..., hu_tile: _Optional[str] = ..., seat: _Optional[int] = ..., zimo: _Optional[bool] = ..., qinjia: _Optional[bool] = ..., liqi: _Optional[bool] = ..., doras: _Optional[_Iterable[str]] = ..., li_doras: _Optional[_Iterable[str]] = ..., yiman: _Optional[bool] = ..., count: _Optional[int] = ..., fans: _Optional[_Iterable[_Union[FanInfo, _Mapping]]] = ..., fu: _Optional[int] = ..., title: _Optional[str] = ..., point_rong: _Optional[int] = ..., point_zimo_qin: _Optional[int] = ..., point_zimo_xian: _Optional[int] = ..., title_id: _Optional[int] = ..., point_sum: _Optional[int] = ..., dadian: _Optional[int] = ..., baopai: _Optional[int] = ..., baopai_seats: _Optional[_Iterable[int]] = ..., lines: _Optional[_Iterable[str]] = ..., tianming_bonus: _Optional[int] = ..., baida_changed: _Optional[_Iterable[str]] = ..., hu_tile_baiDa_changed: _Optional[str] = ..., xia_ke_shang_coefficient: _Optional[int] = ...) -> None: ...

class HunZhiYiJiBuffInfo(_message.Message):
    __slots__ = ()
    SEAT_FIELD_NUMBER: _ClassVar[int]
    CONTINUE_DEAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    OVERLOAD_FIELD_NUMBER: _ClassVar[int]
    seat: int
    continue_deal_count: int
    overload: bool
    def __init__(self, seat: _Optional[int] = ..., continue_deal_count: _Optional[int] = ..., overload: _Optional[bool] = ...) -> None: ...

class I18nContext(_message.Message):
    __slots__ = ()
    LANG_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    lang: str
    context: str
    def __init__(self, lang: _Optional[str] = ..., context: _Optional[str] = ...) -> None: ...

class IslandBagData(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    MATRIX_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    id: int
    matrix: str
    items: _containers.RepeatedCompositeFieldContainer[IslandBagItemData]
    def __init__(self, id: _Optional[int] = ..., matrix: _Optional[str] = ..., items: _Optional[_Iterable[_Union[IslandBagItemData, _Mapping]]] = ...) -> None: ...

class IslandBagItemData(_message.Message):
    __slots__ = ()
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

class IslandGoodsData(_message.Message):
    __slots__ = ()
    GOODS_ID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    goods_id: int
    count: int
    update_time: int
    def __init__(self, goods_id: _Optional[int] = ..., count: _Optional[int] = ..., update_time: _Optional[int] = ...) -> None: ...

class IslandZoneData(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_USED_FIELD_NUMBER: _ClassVar[int]
    GOODS_RECORDS_FIELD_NUMBER: _ClassVar[int]
    id: int
    currency_used: SignedTimeCounterData
    goods_records: _containers.RepeatedCompositeFieldContainer[IslandGoodsData]
    def __init__(self, id: _Optional[int] = ..., currency_used: _Optional[_Union[SignedTimeCounterData, _Mapping]] = ..., goods_records: _Optional[_Iterable[_Union[IslandGoodsData, _Mapping]]] = ...) -> None: ...

class Item(_message.Message):
    __slots__ = ()
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    STACK_FIELD_NUMBER: _ClassVar[int]
    item_id: int
    stack: int
    def __init__(self, item_id: _Optional[int] = ..., stack: _Optional[int] = ...) -> None: ...

class ItemGainRecord(_message.Message):
    __slots__ = ()
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    item_id: int
    count: int
    def __init__(self, item_id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class ItemGainRecords(_message.Message):
    __slots__ = ()
    RECORD_TIME_FIELD_NUMBER: _ClassVar[int]
    LIMIT_SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    RECORDS_FIELD_NUMBER: _ClassVar[int]
    record_time: int
    limit_source_id: int
    records: _containers.RepeatedCompositeFieldContainer[ItemGainRecord]
    def __init__(self, record_time: _Optional[int] = ..., limit_source_id: _Optional[int] = ..., records: _Optional[_Iterable[_Union[ItemGainRecord, _Mapping]]] = ...) -> None: ...

class LiQiSuccess(_message.Message):
    __slots__ = ()
    SEAT_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    LIQIBANG_FIELD_NUMBER: _ClassVar[int]
    FAILED_FIELD_NUMBER: _ClassVar[int]
    LIQI_TYPE_BEISHUIZHIZHAN_FIELD_NUMBER: _ClassVar[int]
    XIA_KE_SHANG_FIELD_NUMBER: _ClassVar[int]
    seat: int
    score: int
    liqibang: int
    failed: bool
    liqi_type_beishuizhizhan: int
    xia_ke_shang: XiaKeShangInfo
    def __init__(self, seat: _Optional[int] = ..., score: _Optional[int] = ..., liqibang: _Optional[int] = ..., failed: _Optional[bool] = ..., liqi_type_beishuizhizhan: _Optional[int] = ..., xia_ke_shang: _Optional[_Union[XiaKeShangInfo, _Mapping]] = ...) -> None: ...

class Mail(_message.Message):
    __slots__ = ()
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
    def __init__(self, mail_id: _Optional[int] = ..., state: _Optional[int] = ..., take_attachment: _Optional[bool] = ..., title: _Optional[str] = ..., content: _Optional[str] = ..., attachments: _Optional[_Iterable[_Union[RewardSlot, _Mapping]]] = ..., create_time: _Optional[int] = ..., expire_time: _Optional[int] = ..., reference_id: _Optional[int] = ..., title_i18n: _Optional[_Iterable[_Union[I18nContext, _Mapping]]] = ..., content_i18n: _Optional[_Iterable[_Union[I18nContext, _Mapping]]] = ..., template_id: _Optional[int] = ...) -> None: ...

class MaintainNotice(_message.Message):
    __slots__ = ()
    MAINTAIN_TIME_FIELD_NUMBER: _ClassVar[int]
    maintain_time: int
    def __init__(self, maintain_time: _Optional[int] = ...) -> None: ...

class MineActivityData(_message.Message):
    __slots__ = ()
    DIG_POINT_FIELD_NUMBER: _ClassVar[int]
    MAP_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    dig_point: _containers.RepeatedCompositeFieldContainer[Point]
    map: _containers.RepeatedCompositeFieldContainer[MineReward]
    id: int
    def __init__(self, dig_point: _Optional[_Iterable[_Union[Point, _Mapping]]] = ..., map: _Optional[_Iterable[_Union[MineReward, _Mapping]]] = ..., id: _Optional[int] = ...) -> None: ...

class MineReward(_message.Message):
    __slots__ = ()
    POINT_FIELD_NUMBER: _ClassVar[int]
    REWARD_ID_FIELD_NUMBER: _ClassVar[int]
    RECEIVED_FIELD_NUMBER: _ClassVar[int]
    point: Point
    reward_id: int
    received: bool
    def __init__(self, point: _Optional[_Union[Point, _Mapping]] = ..., reward_id: _Optional[int] = ..., received: _Optional[bool] = ...) -> None: ...

class MonthTicketInfo(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    LAST_PAY_TIME_FIELD_NUMBER: _ClassVar[int]
    id: int
    end_time: int
    last_pay_time: int
    def __init__(self, id: _Optional[int] = ..., end_time: _Optional[int] = ..., last_pay_time: _Optional[int] = ...) -> None: ...

class MuyuInfo(_message.Message):
    __slots__ = ()
    SEAT_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    COUNT_MAX_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    seat: int
    count: int
    count_max: int
    id: int
    def __init__(self, seat: _Optional[int] = ..., count: _Optional[int] = ..., count_max: _Optional[int] = ..., id: _Optional[int] = ...) -> None: ...

class NetworkEndpoint(_message.Message):
    __slots__ = ()
    FAMILY_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    family: str
    address: str
    port: int
    def __init__(self, family: _Optional[str] = ..., address: _Optional[str] = ..., port: _Optional[int] = ...) -> None: ...

class NewRoundOpenedTiles(_message.Message):
    __slots__ = ()
    SEAT_FIELD_NUMBER: _ClassVar[int]
    TILES_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    seat: int
    tiles: _containers.RepeatedScalarFieldContainer[str]
    count: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, seat: _Optional[int] = ..., tiles: _Optional[_Iterable[str]] = ..., count: _Optional[_Iterable[int]] = ...) -> None: ...

class NicknameSetting(_message.Message):
    __slots__ = ()
    ENABLE_FIELD_NUMBER: _ClassVar[int]
    NICKNAMES_FIELD_NUMBER: _ClassVar[int]
    enable: int
    nicknames: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, enable: _Optional[int] = ..., nicknames: _Optional[_Iterable[str]] = ...) -> None: ...

class NoTilePlayerInfo(_message.Message):
    __slots__ = ()
    TINGPAI_FIELD_NUMBER: _ClassVar[int]
    HAND_FIELD_NUMBER: _ClassVar[int]
    TINGS_FIELD_NUMBER: _ClassVar[int]
    ALREADY_HULE_FIELD_NUMBER: _ClassVar[int]
    tingpai: bool
    hand: _containers.RepeatedScalarFieldContainer[str]
    tings: _containers.RepeatedCompositeFieldContainer[TingPaiInfo]
    already_hule: bool
    def __init__(self, tingpai: _Optional[bool] = ..., hand: _Optional[_Iterable[str]] = ..., tings: _Optional[_Iterable[_Union[TingPaiInfo, _Mapping]]] = ..., already_hule: _Optional[bool] = ...) -> None: ...

class NoTileScoreInfo(_message.Message):
    __slots__ = ()
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

class NotifyAFKResult(_message.Message):
    __slots__ = ()
    TYPE_FIELD_NUMBER: _ClassVar[int]
    BAN_END_TIME_FIELD_NUMBER: _ClassVar[int]
    GAME_UUID_FIELD_NUMBER: _ClassVar[int]
    type: int
    ban_end_time: int
    game_uuid: str
    def __init__(self, type: _Optional[int] = ..., ban_end_time: _Optional[int] = ..., game_uuid: _Optional[str] = ...) -> None: ...

class NotifyAccountChallengeTaskUpdate(_message.Message):
    __slots__ = ()
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

class NotifyAccountLevelChange(_message.Message):
    __slots__ = ()
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    FINAL_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    origin: AccountLevel
    final: AccountLevel
    type: int
    def __init__(self, origin: _Optional[_Union[AccountLevel, _Mapping]] = ..., final: _Optional[_Union[AccountLevel, _Mapping]] = ..., type: _Optional[int] = ...) -> None: ...

class NotifyAccountLogout(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class NotifyAccountRandomTaskUpdate(_message.Message):
    __slots__ = ()
    PROGRESSES_FIELD_NUMBER: _ClassVar[int]
    progresses: _containers.RepeatedCompositeFieldContainer[TaskProgress]
    def __init__(self, progresses: _Optional[_Iterable[_Union[TaskProgress, _Mapping]]] = ...) -> None: ...

class NotifyAccountUpdate(_message.Message):
    __slots__ = ()
    UPDATE_FIELD_NUMBER: _ClassVar[int]
    update: AccountUpdate
    def __init__(self, update: _Optional[_Union[AccountUpdate, _Mapping]] = ...) -> None: ...

class NotifyActivityChange(_message.Message):
    __slots__ = ()
    NEW_ACTIVITIES_FIELD_NUMBER: _ClassVar[int]
    END_ACTIVITIES_FIELD_NUMBER: _ClassVar[int]
    new_activities: _containers.RepeatedCompositeFieldContainer[Activity]
    end_activities: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, new_activities: _Optional[_Iterable[_Union[Activity, _Mapping]]] = ..., end_activities: _Optional[_Iterable[int]] = ...) -> None: ...

class NotifyActivityPeriodTaskUpdate(_message.Message):
    __slots__ = ()
    PROGRESSES_FIELD_NUMBER: _ClassVar[int]
    progresses: _containers.RepeatedCompositeFieldContainer[TaskProgress]
    def __init__(self, progresses: _Optional[_Iterable[_Union[TaskProgress, _Mapping]]] = ...) -> None: ...

class NotifyActivityPoint(_message.Message):
    __slots__ = ()
    class ActivityPoint(_message.Message):
        __slots__ = ()
        ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
        POINT_FIELD_NUMBER: _ClassVar[int]
        activity_id: int
        point: int
        def __init__(self, activity_id: _Optional[int] = ..., point: _Optional[int] = ...) -> None: ...
    ACTIVITY_POINTS_FIELD_NUMBER: _ClassVar[int]
    activity_points: _containers.RepeatedCompositeFieldContainer[NotifyActivityPoint.ActivityPoint]
    def __init__(self, activity_points: _Optional[_Iterable[_Union[NotifyActivityPoint.ActivityPoint, _Mapping]]] = ...) -> None: ...

class NotifyActivityPointV2(_message.Message):
    __slots__ = ()
    class ActivityPoint(_message.Message):
        __slots__ = ()
        ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
        POINT_FIELD_NUMBER: _ClassVar[int]
        activity_id: int
        point: int
        def __init__(self, activity_id: _Optional[int] = ..., point: _Optional[int] = ...) -> None: ...
    ACTIVITY_POINTS_FIELD_NUMBER: _ClassVar[int]
    activity_points: _containers.RepeatedCompositeFieldContainer[NotifyActivityPointV2.ActivityPoint]
    def __init__(self, activity_points: _Optional[_Iterable[_Union[NotifyActivityPointV2.ActivityPoint, _Mapping]]] = ...) -> None: ...

class NotifyActivityReward(_message.Message):
    __slots__ = ()
    class ActivityReward(_message.Message):
        __slots__ = ()
        ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
        REWARDS_FIELD_NUMBER: _ClassVar[int]
        activity_id: int
        rewards: _containers.RepeatedCompositeFieldContainer[RewardSlot]
        def __init__(self, activity_id: _Optional[int] = ..., rewards: _Optional[_Iterable[_Union[RewardSlot, _Mapping]]] = ...) -> None: ...
    ACTIVITY_REWARD_FIELD_NUMBER: _ClassVar[int]
    activity_reward: _containers.RepeatedCompositeFieldContainer[NotifyActivityReward.ActivityReward]
    def __init__(self, activity_reward: _Optional[_Iterable[_Union[NotifyActivityReward.ActivityReward, _Mapping]]] = ...) -> None: ...

class NotifyActivityRewardV2(_message.Message):
    __slots__ = ()
    class ActivityReward(_message.Message):
        __slots__ = ()
        ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
        REWARDS_FIELD_NUMBER: _ClassVar[int]
        activity_id: int
        rewards: _containers.RepeatedCompositeFieldContainer[RewardSlot]
        def __init__(self, activity_id: _Optional[int] = ..., rewards: _Optional[_Iterable[_Union[RewardSlot, _Mapping]]] = ...) -> None: ...
    ACTIVITY_REWARD_FIELD_NUMBER: _ClassVar[int]
    activity_reward: _containers.RepeatedCompositeFieldContainer[NotifyActivityRewardV2.ActivityReward]
    def __init__(self, activity_reward: _Optional[_Iterable[_Union[NotifyActivityRewardV2.ActivityReward, _Mapping]]] = ...) -> None: ...

class NotifyActivitySegmentTaskUpdate(_message.Message):
    __slots__ = ()
    PROGRESSES_FIELD_NUMBER: _ClassVar[int]
    progresses: _containers.RepeatedCompositeFieldContainer[SegmentTaskProgress]
    def __init__(self, progresses: _Optional[_Iterable[_Union[SegmentTaskProgress, _Mapping]]] = ...) -> None: ...

class NotifyActivityTaskUpdate(_message.Message):
    __slots__ = ()
    PROGRESSES_FIELD_NUMBER: _ClassVar[int]
    progresses: _containers.RepeatedCompositeFieldContainer[TaskProgress]
    def __init__(self, progresses: _Optional[_Iterable[_Union[TaskProgress, _Mapping]]] = ...) -> None: ...

class NotifyActivityUpdate(_message.Message):
    __slots__ = ()
    class FeedActivityData(_message.Message):
        __slots__ = ()
        class CountWithTimeData(_message.Message):
            __slots__ = ()
            COUNT_FIELD_NUMBER: _ClassVar[int]
            LAST_UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
            count: int
            last_update_time: int
            def __init__(self, count: _Optional[int] = ..., last_update_time: _Optional[int] = ...) -> None: ...
        class GiftBoxData(_message.Message):
            __slots__ = ()
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

class NotifyAnnouncementUpdate(_message.Message):
    __slots__ = ()
    class AnnouncementUpdate(_message.Message):
        __slots__ = ()
        LANG_FIELD_NUMBER: _ClassVar[int]
        PLATFORM_FIELD_NUMBER: _ClassVar[int]
        lang: str
        platform: str
        def __init__(self, lang: _Optional[str] = ..., platform: _Optional[str] = ...) -> None: ...
    UPDATE_LIST_FIELD_NUMBER: _ClassVar[int]
    update_list: _containers.RepeatedCompositeFieldContainer[NotifyAnnouncementUpdate.AnnouncementUpdate]
    def __init__(self, update_list: _Optional[_Iterable[_Union[NotifyAnnouncementUpdate.AnnouncementUpdate, _Mapping]]] = ...) -> None: ...

class NotifyAnotherLogin(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class NotifyClientMessage(_message.Message):
    __slots__ = ()
    SENDER_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    sender: PlayerBaseView
    type: int
    content: str
    def __init__(self, sender: _Optional[_Union[PlayerBaseView, _Mapping]] = ..., type: _Optional[int] = ..., content: _Optional[str] = ...) -> None: ...

class NotifyConnectionShutdown(_message.Message):
    __slots__ = ()
    REASON_FIELD_NUMBER: _ClassVar[int]
    CLOSE_AT_FIELD_NUMBER: _ClassVar[int]
    reason: int
    close_at: int
    def __init__(self, reason: _Optional[int] = ..., close_at: _Optional[int] = ...) -> None: ...

class NotifyCustomContestAccountMsg(_message.Message):
    __slots__ = ()
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

class NotifyCustomContestState(_message.Message):
    __slots__ = ()
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    unique_id: int
    state: int
    def __init__(self, unique_id: _Optional[int] = ..., state: _Optional[int] = ...) -> None: ...

class NotifyCustomContestSystemMsg(_message.Message):
    __slots__ = ()
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

class NotifyDailyTaskUpdate(_message.Message):
    __slots__ = ()
    PROGRESSES_FIELD_NUMBER: _ClassVar[int]
    MAX_DAILY_TASK_COUNT_FIELD_NUMBER: _ClassVar[int]
    REFRESH_COUNT_FIELD_NUMBER: _ClassVar[int]
    progresses: _containers.RepeatedCompositeFieldContainer[TaskProgress]
    max_daily_task_count: int
    refresh_count: int
    def __init__(self, progresses: _Optional[_Iterable[_Union[TaskProgress, _Mapping]]] = ..., max_daily_task_count: _Optional[int] = ..., refresh_count: _Optional[int] = ...) -> None: ...

class NotifyDeleteMail(_message.Message):
    __slots__ = ()
    MAIL_ID_LIST_FIELD_NUMBER: _ClassVar[int]
    mail_id_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, mail_id_list: _Optional[_Iterable[int]] = ...) -> None: ...

class NotifyEndGameVote(_message.Message):
    __slots__ = ()
    class VoteResult(_message.Message):
        __slots__ = ()
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        YES_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        yes: bool
        def __init__(self, account_id: _Optional[int] = ..., yes: _Optional[bool] = ...) -> None: ...
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    DURATION_TIME_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[NotifyEndGameVote.VoteResult]
    start_time: int
    duration_time: int
    def __init__(self, results: _Optional[_Iterable[_Union[NotifyEndGameVote.VoteResult, _Mapping]]] = ..., start_time: _Optional[int] = ..., duration_time: _Optional[int] = ...) -> None: ...

class NotifyFriendChange(_message.Message):
    __slots__ = ()
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    FRIEND_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    type: int
    friend: Friend
    def __init__(self, account_id: _Optional[int] = ..., type: _Optional[int] = ..., friend: _Optional[_Union[Friend, _Mapping]] = ...) -> None: ...

class NotifyFriendStateChange(_message.Message):
    __slots__ = ()
    TARGET_ID_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_STATE_FIELD_NUMBER: _ClassVar[int]
    target_id: int
    active_state: AccountActiveState
    def __init__(self, target_id: _Optional[int] = ..., active_state: _Optional[_Union[AccountActiveState, _Mapping]] = ...) -> None: ...

class NotifyFriendViewChange(_message.Message):
    __slots__ = ()
    TARGET_ID_FIELD_NUMBER: _ClassVar[int]
    BASE_FIELD_NUMBER: _ClassVar[int]
    target_id: int
    base: PlayerBaseView
    def __init__(self, target_id: _Optional[int] = ..., base: _Optional[_Union[PlayerBaseView, _Mapping]] = ...) -> None: ...

class NotifyGameBroadcast(_message.Message):
    __slots__ = ()
    SEAT_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    seat: int
    content: str
    def __init__(self, seat: _Optional[int] = ..., content: _Optional[str] = ...) -> None: ...

class NotifyGameEndResult(_message.Message):
    __slots__ = ()
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: GameEndResult
    def __init__(self, result: _Optional[_Union[GameEndResult, _Mapping]] = ...) -> None: ...

class NotifyGameFinishReward(_message.Message):
    __slots__ = ()
    class LevelChange(_message.Message):
        __slots__ = ()
        ORIGIN_FIELD_NUMBER: _ClassVar[int]
        FINAL_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        origin: AccountLevel
        final: AccountLevel
        type: int
        def __init__(self, origin: _Optional[_Union[AccountLevel, _Mapping]] = ..., final: _Optional[_Union[AccountLevel, _Mapping]] = ..., type: _Optional[int] = ...) -> None: ...
    class MatchChest(_message.Message):
        __slots__ = ()
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
        def __init__(self, chest_id: _Optional[int] = ..., origin: _Optional[int] = ..., final: _Optional[int] = ..., is_graded: _Optional[bool] = ..., rewards: _Optional[_Iterable[_Union[RewardSlot, _Mapping]]] = ...) -> None: ...
    class MainCharacter(_message.Message):
        __slots__ = ()
        LEVEL_FIELD_NUMBER: _ClassVar[int]
        EXP_FIELD_NUMBER: _ClassVar[int]
        ADD_FIELD_NUMBER: _ClassVar[int]
        level: int
        exp: int
        add: int
        def __init__(self, level: _Optional[int] = ..., exp: _Optional[int] = ..., add: _Optional[int] = ...) -> None: ...
    class CharacterGift(_message.Message):
        __slots__ = ()
        ORIGIN_FIELD_NUMBER: _ClassVar[int]
        FINAL_FIELD_NUMBER: _ClassVar[int]
        ADD_FIELD_NUMBER: _ClassVar[int]
        IS_GRADED_FIELD_NUMBER: _ClassVar[int]
        origin: int
        final: int
        add: int
        is_graded: bool
        def __init__(self, origin: _Optional[int] = ..., final: _Optional[int] = ..., add: _Optional[int] = ..., is_graded: _Optional[bool] = ...) -> None: ...
    MODE_ID_FIELD_NUMBER: _ClassVar[int]
    LEVEL_CHANGE_FIELD_NUMBER: _ClassVar[int]
    MATCH_CHEST_FIELD_NUMBER: _ClassVar[int]
    MAIN_CHARACTER_FIELD_NUMBER: _ClassVar[int]
    CHARACTER_GIFT_FIELD_NUMBER: _ClassVar[int]
    BADGES_FIELD_NUMBER: _ClassVar[int]
    mode_id: int
    level_change: NotifyGameFinishReward.LevelChange
    match_chest: NotifyGameFinishReward.MatchChest
    main_character: NotifyGameFinishReward.MainCharacter
    character_gift: NotifyGameFinishReward.CharacterGift
    badges: _containers.RepeatedCompositeFieldContainer[BadgeAchieveProgress]
    def __init__(self, mode_id: _Optional[int] = ..., level_change: _Optional[_Union[NotifyGameFinishReward.LevelChange, _Mapping]] = ..., match_chest: _Optional[_Union[NotifyGameFinishReward.MatchChest, _Mapping]] = ..., main_character: _Optional[_Union[NotifyGameFinishReward.MainCharacter, _Mapping]] = ..., character_gift: _Optional[_Union[NotifyGameFinishReward.CharacterGift, _Mapping]] = ..., badges: _Optional[_Iterable[_Union[BadgeAchieveProgress, _Mapping]]] = ...) -> None: ...

class NotifyGameFinishRewardV2(_message.Message):
    __slots__ = ()
    class LevelChange(_message.Message):
        __slots__ = ()
        ORIGIN_FIELD_NUMBER: _ClassVar[int]
        FINAL_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        origin: AccountLevel
        final: AccountLevel
        type: int
        def __init__(self, origin: _Optional[_Union[AccountLevel, _Mapping]] = ..., final: _Optional[_Union[AccountLevel, _Mapping]] = ..., type: _Optional[int] = ...) -> None: ...
    class MatchChest(_message.Message):
        __slots__ = ()
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
        def __init__(self, chest_id: _Optional[int] = ..., origin: _Optional[int] = ..., final: _Optional[int] = ..., is_graded: _Optional[bool] = ..., rewards: _Optional[_Iterable[_Union[RewardSlot, _Mapping]]] = ...) -> None: ...
    class MainCharacter(_message.Message):
        __slots__ = ()
        LEVEL_FIELD_NUMBER: _ClassVar[int]
        EXP_FIELD_NUMBER: _ClassVar[int]
        ADD_FIELD_NUMBER: _ClassVar[int]
        level: int
        exp: int
        add: int
        def __init__(self, level: _Optional[int] = ..., exp: _Optional[int] = ..., add: _Optional[int] = ...) -> None: ...
    class CharacterGift(_message.Message):
        __slots__ = ()
        ORIGIN_FIELD_NUMBER: _ClassVar[int]
        FINAL_FIELD_NUMBER: _ClassVar[int]
        ADD_FIELD_NUMBER: _ClassVar[int]
        IS_GRADED_FIELD_NUMBER: _ClassVar[int]
        origin: int
        final: int
        add: int
        is_graded: bool
        def __init__(self, origin: _Optional[int] = ..., final: _Optional[int] = ..., add: _Optional[int] = ..., is_graded: _Optional[bool] = ...) -> None: ...
    MODE_ID_FIELD_NUMBER: _ClassVar[int]
    LEVEL_CHANGE_FIELD_NUMBER: _ClassVar[int]
    MATCH_CHEST_FIELD_NUMBER: _ClassVar[int]
    MAIN_CHARACTER_FIELD_NUMBER: _ClassVar[int]
    CHARACTER_GIFT_FIELD_NUMBER: _ClassVar[int]
    BADGES_FIELD_NUMBER: _ClassVar[int]
    mode_id: int
    level_change: NotifyGameFinishRewardV2.LevelChange
    match_chest: NotifyGameFinishRewardV2.MatchChest
    main_character: NotifyGameFinishRewardV2.MainCharacter
    character_gift: NotifyGameFinishRewardV2.CharacterGift
    badges: _containers.RepeatedCompositeFieldContainer[BadgeAchieveProgress]
    def __init__(self, mode_id: _Optional[int] = ..., level_change: _Optional[_Union[NotifyGameFinishRewardV2.LevelChange, _Mapping]] = ..., match_chest: _Optional[_Union[NotifyGameFinishRewardV2.MatchChest, _Mapping]] = ..., main_character: _Optional[_Union[NotifyGameFinishRewardV2.MainCharacter, _Mapping]] = ..., character_gift: _Optional[_Union[NotifyGameFinishRewardV2.CharacterGift, _Mapping]] = ..., badges: _Optional[_Iterable[_Union[BadgeAchieveProgress, _Mapping]]] = ...) -> None: ...

class NotifyGamePause(_message.Message):
    __slots__ = ()
    PAUSED_FIELD_NUMBER: _ClassVar[int]
    paused: bool
    def __init__(self, paused: _Optional[bool] = ...) -> None: ...

class NotifyGameTerminate(_message.Message):
    __slots__ = ()
    REASON_FIELD_NUMBER: _ClassVar[int]
    reason: str
    def __init__(self, reason: _Optional[str] = ...) -> None: ...

class NotifyGiftSendRefresh(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class NotifyIntervalUpdate(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class NotifyLeaderboardPoint(_message.Message):
    __slots__ = ()
    class LeaderboardPoint(_message.Message):
        __slots__ = ()
        LEADERBOARD_ID_FIELD_NUMBER: _ClassVar[int]
        POINT_FIELD_NUMBER: _ClassVar[int]
        leaderboard_id: int
        point: int
        def __init__(self, leaderboard_id: _Optional[int] = ..., point: _Optional[int] = ...) -> None: ...
    LEADERBOARD_POINTS_FIELD_NUMBER: _ClassVar[int]
    leaderboard_points: _containers.RepeatedCompositeFieldContainer[NotifyLeaderboardPoint.LeaderboardPoint]
    def __init__(self, leaderboard_points: _Optional[_Iterable[_Union[NotifyLeaderboardPoint.LeaderboardPoint, _Mapping]]] = ...) -> None: ...

class NotifyLeaderboardPointV2(_message.Message):
    __slots__ = ()
    class LeaderboardPoint(_message.Message):
        __slots__ = ()
        LEADERBOARD_ID_FIELD_NUMBER: _ClassVar[int]
        POINT_FIELD_NUMBER: _ClassVar[int]
        leaderboard_id: int
        point: int
        def __init__(self, leaderboard_id: _Optional[int] = ..., point: _Optional[int] = ...) -> None: ...
    LEADERBOARD_POINTS_FIELD_NUMBER: _ClassVar[int]
    leaderboard_points: _containers.RepeatedCompositeFieldContainer[NotifyLeaderboardPointV2.LeaderboardPoint]
    def __init__(self, leaderboard_points: _Optional[_Iterable[_Union[NotifyLeaderboardPointV2.LeaderboardPoint, _Mapping]]] = ...) -> None: ...

class NotifyLoginQueueFinished(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class NotifyMaintainNotice(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class NotifyMatchFailed(_message.Message):
    __slots__ = ()
    SID_FIELD_NUMBER: _ClassVar[int]
    sid: str
    def __init__(self, sid: _Optional[str] = ...) -> None: ...

class NotifyMatchGameStart(_message.Message):
    __slots__ = ()
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

class NotifyMatchTimeout(_message.Message):
    __slots__ = ()
    SID_FIELD_NUMBER: _ClassVar[int]
    sid: str
    def __init__(self, sid: _Optional[str] = ...) -> None: ...

class NotifyNewComment(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class NotifyNewFriendApply(_message.Message):
    __slots__ = ()
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    APPLY_TIME_FIELD_NUMBER: _ClassVar[int]
    REMOVED_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    apply_time: int
    removed_id: int
    def __init__(self, account_id: _Optional[int] = ..., apply_time: _Optional[int] = ..., removed_id: _Optional[int] = ...) -> None: ...

class NotifyNewGame(_message.Message):
    __slots__ = ()
    GAME_UUID_FIELD_NUMBER: _ClassVar[int]
    PLAYER_LIST_FIELD_NUMBER: _ClassVar[int]
    game_uuid: str
    player_list: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, game_uuid: _Optional[str] = ..., player_list: _Optional[_Iterable[str]] = ...) -> None: ...

class NotifyNewMail(_message.Message):
    __slots__ = ()
    MAIL_FIELD_NUMBER: _ClassVar[int]
    mail: Mail
    def __init__(self, mail: _Optional[_Union[Mail, _Mapping]] = ...) -> None: ...

class NotifyObserveData(_message.Message):
    __slots__ = ()
    UNIT_FIELD_NUMBER: _ClassVar[int]
    unit: GameLiveUnit
    def __init__(self, unit: _Optional[_Union[GameLiveUnit, _Mapping]] = ...) -> None: ...

class NotifyPayResult(_message.Message):
    __slots__ = ()
    class ResourceModify(_message.Message):
        __slots__ = ()
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

class NotifyPlayerConnectionState(_message.Message):
    __slots__ = ()
    SEAT_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    seat: int
    state: GamePlayerState
    def __init__(self, seat: _Optional[int] = ..., state: _Optional[_Union[GamePlayerState, str]] = ...) -> None: ...

class NotifyPlayerLoadGameReady(_message.Message):
    __slots__ = ()
    READY_ID_LIST_FIELD_NUMBER: _ClassVar[int]
    ready_id_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, ready_id_list: _Optional[_Iterable[int]] = ...) -> None: ...

class NotifyReviveCoinUpdate(_message.Message):
    __slots__ = ()
    HAS_GAINED_FIELD_NUMBER: _ClassVar[int]
    has_gained: bool
    def __init__(self, has_gained: _Optional[bool] = ...) -> None: ...

class NotifyRollingNotice(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class NotifyRoomGameStart(_message.Message):
    __slots__ = ()
    GAME_URL_FIELD_NUMBER: _ClassVar[int]
    CONNECT_TOKEN_FIELD_NUMBER: _ClassVar[int]
    GAME_UUID_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    game_url: str
    connect_token: str
    game_uuid: str
    location: str
    def __init__(self, game_url: _Optional[str] = ..., connect_token: _Optional[str] = ..., game_uuid: _Optional[str] = ..., location: _Optional[str] = ...) -> None: ...

class NotifyRoomKickOut(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class NotifyRoomPlayerDressing(_message.Message):
    __slots__ = ()
    class AccountDressingState(_message.Message):
        __slots__ = ()
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        DRESSING_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        dressing: bool
        def __init__(self, account_id: _Optional[int] = ..., dressing: _Optional[bool] = ...) -> None: ...
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    DRESSING_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_LIST_FIELD_NUMBER: _ClassVar[int]
    SEQ_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    dressing: bool
    account_list: NotifyRoomPlayerDressing.AccountDressingState
    seq: int
    def __init__(self, account_id: _Optional[int] = ..., dressing: _Optional[bool] = ..., account_list: _Optional[_Union[NotifyRoomPlayerDressing.AccountDressingState, _Mapping]] = ..., seq: _Optional[int] = ...) -> None: ...

class NotifyRoomPlayerReady(_message.Message):
    __slots__ = ()
    class AccountReadyState(_message.Message):
        __slots__ = ()
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        READY_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        ready: bool
        def __init__(self, account_id: _Optional[int] = ..., ready: _Optional[bool] = ...) -> None: ...
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    READY_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_LIST_FIELD_NUMBER: _ClassVar[int]
    SEQ_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    ready: bool
    account_list: NotifyRoomPlayerReady.AccountReadyState
    seq: int
    def __init__(self, account_id: _Optional[int] = ..., ready: _Optional[bool] = ..., account_list: _Optional[_Union[NotifyRoomPlayerReady.AccountReadyState, _Mapping]] = ..., seq: _Optional[int] = ...) -> None: ...

class NotifyRoomPlayerUpdate(_message.Message):
    __slots__ = ()
    OWNER_ID_FIELD_NUMBER: _ClassVar[int]
    ROBOT_COUNT_FIELD_NUMBER: _ClassVar[int]
    PLAYER_LIST_FIELD_NUMBER: _ClassVar[int]
    SEQ_FIELD_NUMBER: _ClassVar[int]
    ROBOTS_FIELD_NUMBER: _ClassVar[int]
    POSITIONS_FIELD_NUMBER: _ClassVar[int]
    owner_id: int
    robot_count: int
    player_list: _containers.RepeatedCompositeFieldContainer[PlayerGameView]
    seq: int
    robots: _containers.RepeatedCompositeFieldContainer[PlayerGameView]
    positions: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, owner_id: _Optional[int] = ..., robot_count: _Optional[int] = ..., player_list: _Optional[_Iterable[_Union[PlayerGameView, _Mapping]]] = ..., seq: _Optional[int] = ..., robots: _Optional[_Iterable[_Union[PlayerGameView, _Mapping]]] = ..., positions: _Optional[_Iterable[int]] = ...) -> None: ...

class NotifySeerReport(_message.Message):
    __slots__ = ()
    REPORT_FIELD_NUMBER: _ClassVar[int]
    report: SeerBrief
    def __init__(self, report: _Optional[_Union[SeerBrief, _Mapping]] = ...) -> None: ...

class NotifyServerSetting(_message.Message):
    __slots__ = ()
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    settings: ServerSettings
    def __init__(self, settings: _Optional[_Union[ServerSettings, _Mapping]] = ...) -> None: ...

class NotifyShopUpdate(_message.Message):
    __slots__ = ()
    SHOP_INFO_FIELD_NUMBER: _ClassVar[int]
    shop_info: ShopInfo
    def __init__(self, shop_info: _Optional[_Union[ShopInfo, _Mapping]] = ...) -> None: ...

class NotifyVipLevelChange(_message.Message):
    __slots__ = ()
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

class OpenResult(_message.Message):
    __slots__ = ()
    REWARD_FIELD_NUMBER: _ClassVar[int]
    REPLACE_FIELD_NUMBER: _ClassVar[int]
    reward: RewardSlot
    replace: RewardSlot
    def __init__(self, reward: _Optional[_Union[RewardSlot, _Mapping]] = ..., replace: _Optional[_Union[RewardSlot, _Mapping]] = ...) -> None: ...

class OptionalOperation(_message.Message):
    __slots__ = ()
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
    __slots__ = ()
    SEAT_FIELD_NUMBER: _ClassVar[int]
    OPERATION_LIST_FIELD_NUMBER: _ClassVar[int]
    TIME_ADD_FIELD_NUMBER: _ClassVar[int]
    TIME_FIXED_FIELD_NUMBER: _ClassVar[int]
    seat: int
    operation_list: _containers.RepeatedCompositeFieldContainer[OptionalOperation]
    time_add: int
    time_fixed: int
    def __init__(self, seat: _Optional[int] = ..., operation_list: _Optional[_Iterable[_Union[OptionalOperation, _Mapping]]] = ..., time_add: _Optional[int] = ..., time_fixed: _Optional[int] = ...) -> None: ...

class PaymentSetting(_message.Message):
    __slots__ = ()
    class WechatData(_message.Message):
        __slots__ = ()
        DISABLE_CREATE_FIELD_NUMBER: _ClassVar[int]
        PAYMENT_SOURCE_PLATFORM_FIELD_NUMBER: _ClassVar[int]
        ENABLE_CREDIT_FIELD_NUMBER: _ClassVar[int]
        disable_create: bool
        payment_source_platform: int
        enable_credit: bool
        def __init__(self, disable_create: _Optional[bool] = ..., payment_source_platform: _Optional[int] = ..., enable_credit: _Optional[bool] = ...) -> None: ...
    class AlipayData(_message.Message):
        __slots__ = ()
        DISABLE_CREATE_FIELD_NUMBER: _ClassVar[int]
        PAYMENT_SOURCE_PLATFORM_FIELD_NUMBER: _ClassVar[int]
        disable_create: bool
        payment_source_platform: int
        def __init__(self, disable_create: _Optional[bool] = ..., payment_source_platform: _Optional[int] = ...) -> None: ...
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

class PaymentSettingV2(_message.Message):
    __slots__ = ()
    class PaymentMaintain(_message.Message):
        __slots__ = ()
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
        __slots__ = ()
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
        def __init__(self, platform: _Optional[str] = ..., is_show: _Optional[bool] = ..., goods_click_action: _Optional[int] = ..., goods_click_text: _Optional[str] = ..., maintain: _Optional[_Union[PaymentSettingV2.PaymentMaintain, _Mapping]] = ..., enable_for_frozen_account: _Optional[bool] = ..., extra_data: _Optional[str] = ..., enabled_channel: _Optional[_Iterable[str]] = ...) -> None: ...
    OPEN_PAYMENT_FIELD_NUMBER: _ClassVar[int]
    PAYMENT_PLATFORMS_FIELD_NUMBER: _ClassVar[int]
    open_payment: int
    payment_platforms: _containers.RepeatedCompositeFieldContainer[PaymentSettingV2.PaymentSettingUnit]
    def __init__(self, open_payment: _Optional[int] = ..., payment_platforms: _Optional[_Iterable[_Union[PaymentSettingV2.PaymentSettingUnit, _Mapping]]] = ...) -> None: ...

class PlayerBaseView(_message.Message):
    __slots__ = ()
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
    __slots__ = ()
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
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_NAME_FIELD_NUMBER: _ClassVar[int]
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
    team_id: int
    team_name: str
    def __init__(self, account_id: _Optional[int] = ..., avatar_id: _Optional[int] = ..., title: _Optional[int] = ..., nickname: _Optional[str] = ..., level: _Optional[_Union[AccountLevel, _Mapping]] = ..., character: _Optional[_Union[Character, _Mapping]] = ..., level3: _Optional[_Union[AccountLevel, _Mapping]] = ..., avatar_frame: _Optional[int] = ..., verified: _Optional[int] = ..., views: _Optional[_Iterable[_Union[ViewSlot, _Mapping]]] = ..., team_id: _Optional[int] = ..., team_name: _Optional[str] = ...) -> None: ...

class PlayerLeaving(_message.Message):
    __slots__ = ()
    SEAT_FIELD_NUMBER: _ClassVar[int]
    seat: int
    def __init__(self, seat: _Optional[int] = ...) -> None: ...

class Point(_message.Message):
    __slots__ = ()
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    x: int
    y: int
    def __init__(self, x: _Optional[int] = ..., y: _Optional[int] = ...) -> None: ...

class QCMember(_message.Message):
    __slots__ = ()
    MEMBER_ID_FIELD_NUMBER: _ClassVar[int]
    CONSUMED_STA_FIELD_NUMBER: _ClassVar[int]
    member_id: int
    consumed_sta: TimeCounterData
    def __init__(self, member_id: _Optional[int] = ..., consumed_sta: _Optional[_Union[TimeCounterData, _Mapping]] = ...) -> None: ...

class QCQuest(_message.Message):
    __slots__ = ()
    QUEST_ID_FIELD_NUMBER: _ClassVar[int]
    FINISHED_FIELD_NUMBER: _ClassVar[int]
    FINISHED_TIME_FIELD_NUMBER: _ClassVar[int]
    quest_id: int
    finished: int
    finished_time: int
    def __init__(self, quest_id: _Optional[int] = ..., finished: _Optional[int] = ..., finished_time: _Optional[int] = ...) -> None: ...

class QuestionnaireBrief(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    EFFECTIVE_TIME_START_FIELD_NUMBER: _ClassVar[int]
    EFFECTIVE_TIME_END_FIELD_NUMBER: _ClassVar[int]
    REWARDS_FIELD_NUMBER: _ClassVar[int]
    BANNER_TITLE_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    id: int
    version_id: int
    effective_time_start: int
    effective_time_end: int
    rewards: _containers.RepeatedCompositeFieldContainer[QuestionnaireReward]
    banner_title: str
    title: str
    type: int
    def __init__(self, id: _Optional[int] = ..., version_id: _Optional[int] = ..., effective_time_start: _Optional[int] = ..., effective_time_end: _Optional[int] = ..., rewards: _Optional[_Iterable[_Union[QuestionnaireReward, _Mapping]]] = ..., banner_title: _Optional[str] = ..., title: _Optional[str] = ..., type: _Optional[int] = ...) -> None: ...

class QuestionnaireDetail(_message.Message):
    __slots__ = ()
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
    TYPE_FIELD_NUMBER: _ClassVar[int]
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
    type: int
    def __init__(self, id: _Optional[int] = ..., version_id: _Optional[int] = ..., effective_time_start: _Optional[int] = ..., effective_time_end: _Optional[int] = ..., rewards: _Optional[_Iterable[_Union[QuestionnaireReward, _Mapping]]] = ..., banner_title: _Optional[str] = ..., title: _Optional[str] = ..., announcement_title: _Optional[str] = ..., announcement_content: _Optional[str] = ..., final_text: _Optional[str] = ..., questions: _Optional[_Iterable[_Union[QuestionnaireQuestion, _Mapping]]] = ..., type: _Optional[int] = ...) -> None: ...

class QuestionnaireQuestion(_message.Message):
    __slots__ = ()
    class QuestionOption(_message.Message):
        __slots__ = ()
        LABEL_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        ALLOW_INPUT_FIELD_NUMBER: _ClassVar[int]
        label: str
        value: str
        allow_input: bool
        def __init__(self, label: _Optional[str] = ..., value: _Optional[str] = ..., allow_input: _Optional[bool] = ...) -> None: ...
    class NextQuestionData(_message.Message):
        __slots__ = ()
        class QuestionCondition(_message.Message):
            __slots__ = ()
            QUESTION_ID_FIELD_NUMBER: _ClassVar[int]
            OP_FIELD_NUMBER: _ClassVar[int]
            VALUES_FIELD_NUMBER: _ClassVar[int]
            question_id: int
            op: str
            values: _containers.RepeatedScalarFieldContainer[str]
            def __init__(self, question_id: _Optional[int] = ..., op: _Optional[str] = ..., values: _Optional[_Iterable[str]] = ...) -> None: ...
        class QuestionconditionWrapper(_message.Message):
            __slots__ = ()
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
    OPTION_RANDOM_SORT_INDEX_FIELD_NUMBER: _ClassVar[int]
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
    option_random_sort_index: int
    def __init__(self, id: _Optional[int] = ..., title: _Optional[str] = ..., describe: _Optional[str] = ..., type: _Optional[str] = ..., sub_type: _Optional[str] = ..., options: _Optional[_Iterable[_Union[QuestionnaireQuestion.QuestionOption, _Mapping]]] = ..., option_random_sort: _Optional[bool] = ..., require: _Optional[bool] = ..., max_choice: _Optional[int] = ..., next_question: _Optional[_Iterable[_Union[QuestionnaireQuestion.NextQuestionData, _Mapping]]] = ..., matrix_row: _Optional[_Iterable[str]] = ..., option_random_sort_index: _Optional[int] = ...) -> None: ...

class QuestionnaireReward(_message.Message):
    __slots__ = ()
    RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    resource_id: int
    count: int
    def __init__(self, resource_id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class RPGActivity(_message.Message):
    __slots__ = ()
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

class RPGState(_message.Message):
    __slots__ = ()
    PLAYER_DAMAGED_FIELD_NUMBER: _ClassVar[int]
    MONSTER_DAMAGED_FIELD_NUMBER: _ClassVar[int]
    MONSTER_SEQ_FIELD_NUMBER: _ClassVar[int]
    player_damaged: int
    monster_damaged: int
    monster_seq: int
    def __init__(self, player_damaged: _Optional[int] = ..., monster_damaged: _Optional[int] = ..., monster_seq: _Optional[int] = ...) -> None: ...

class RandomCharacter(_message.Message):
    __slots__ = ()
    CHARACTER_ID_FIELD_NUMBER: _ClassVar[int]
    SKIN_ID_FIELD_NUMBER: _ClassVar[int]
    character_id: int
    skin_id: int
    def __init__(self, character_id: _Optional[int] = ..., skin_id: _Optional[int] = ...) -> None: ...

class RecordAnGangAddGang(_message.Message):
    __slots__ = ()
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

class RecordAnalysisedData(_message.Message):
    __slots__ = ()
    ROUND_INFOS_FIELD_NUMBER: _ClassVar[int]
    round_infos: _containers.RepeatedCompositeFieldContainer[RecordRoundInfo]
    def __init__(self, round_infos: _Optional[_Iterable[_Union[RecordRoundInfo, _Mapping]]] = ...) -> None: ...

class RecordBaBei(_message.Message):
    __slots__ = ()
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
    def __init__(self, seat: _Optional[int] = ..., doras: _Optional[_Iterable[str]] = ..., operations: _Optional[_Iterable[_Union[OptionalOperationList, _Mapping]]] = ..., moqie: _Optional[bool] = ..., tile_state: _Optional[int] = ..., muyu: _Optional[_Union[MuyuInfo, _Mapping]] = ...) -> None: ...

class RecordBaBeiInfo(_message.Message):
    __slots__ = ()
    SEAT_FIELD_NUMBER: _ClassVar[int]
    IS_ZI_MO_FIELD_NUMBER: _ClassVar[int]
    IS_CHONG_FIELD_NUMBER: _ClassVar[int]
    IS_BEI_FIELD_NUMBER: _ClassVar[int]
    seat: int
    is_zi_mo: bool
    is_chong: bool
    is_bei: bool
    def __init__(self, seat: _Optional[int] = ..., is_zi_mo: _Optional[bool] = ..., is_chong: _Optional[bool] = ..., is_bei: _Optional[bool] = ...) -> None: ...

class RecordChangeTile(_message.Message):
    __slots__ = ()
    class TingPai(_message.Message):
        __slots__ = ()
        SEAT_FIELD_NUMBER: _ClassVar[int]
        TINGPAIS1_FIELD_NUMBER: _ClassVar[int]
        seat: int
        tingpais1: _containers.RepeatedCompositeFieldContainer[TingPaiInfo]
        def __init__(self, seat: _Optional[int] = ..., tingpais1: _Optional[_Iterable[_Union[TingPaiInfo, _Mapping]]] = ...) -> None: ...
    class ChangeTile(_message.Message):
        __slots__ = ()
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

class RecordChiPengGang(_message.Message):
    __slots__ = ()
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

class RecordCollectedData(_message.Message):
    __slots__ = ()
    UUID_FIELD_NUMBER: _ClassVar[int]
    REMARKS_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    remarks: str
    start_time: int
    end_time: int
    def __init__(self, uuid: _Optional[str] = ..., remarks: _Optional[str] = ..., start_time: _Optional[int] = ..., end_time: _Optional[int] = ...) -> None: ...

class RecordDealTile(_message.Message):
    __slots__ = ()
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

class RecordDiscardTile(_message.Message):
    __slots__ = ()
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
    LIQI_TYPE_BEISHUIZHIZHAN_FIELD_NUMBER: _ClassVar[int]
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
    liqi_type_beishuizhizhan: int
    def __init__(self, seat: _Optional[int] = ..., tile: _Optional[str] = ..., is_liqi: _Optional[bool] = ..., moqie: _Optional[bool] = ..., zhenting: _Optional[_Iterable[bool]] = ..., tingpais: _Optional[_Iterable[_Union[TingPaiInfo, _Mapping]]] = ..., doras: _Optional[_Iterable[str]] = ..., is_wliqi: _Optional[bool] = ..., operations: _Optional[_Iterable[_Union[OptionalOperationList, _Mapping]]] = ..., tile_state: _Optional[int] = ..., muyu: _Optional[_Union[MuyuInfo, _Mapping]] = ..., yongchang: _Optional[_Union[YongchangInfo, _Mapping]] = ..., hun_zhi_yi_ji_info: _Optional[_Union[HunZhiYiJiBuffInfo, _Mapping]] = ..., liqi_type_beishuizhizhan: _Optional[int] = ...) -> None: ...

class RecordFillAwaitingTiles(_message.Message):
    __slots__ = ()
    AWAITING_TILES_FIELD_NUMBER: _ClassVar[int]
    LEFT_TILE_COUNT_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    LIQI_FIELD_NUMBER: _ClassVar[int]
    awaiting_tiles: _containers.RepeatedScalarFieldContainer[str]
    left_tile_count: int
    operation: OptionalOperationList
    liqi: LiQiSuccess
    def __init__(self, awaiting_tiles: _Optional[_Iterable[str]] = ..., left_tile_count: _Optional[int] = ..., operation: _Optional[_Union[OptionalOperationList, _Mapping]] = ..., liqi: _Optional[_Union[LiQiSuccess, _Mapping]] = ...) -> None: ...

class RecordGame(_message.Message):
    __slots__ = ()
    class AccountInfo(_message.Message):
        __slots__ = ()
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
    ROBOTS_FIELD_NUMBER: _ClassVar[int]
    STANDARD_RULE_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    start_time: int
    end_time: int
    config: GameConfig
    accounts: _containers.RepeatedCompositeFieldContainer[RecordGame.AccountInfo]
    result: GameEndResult
    robots: _containers.RepeatedCompositeFieldContainer[RecordGame.AccountInfo]
    standard_rule: int
    def __init__(self, uuid: _Optional[str] = ..., start_time: _Optional[int] = ..., end_time: _Optional[int] = ..., config: _Optional[_Union[GameConfig, _Mapping]] = ..., accounts: _Optional[_Iterable[_Union[RecordGame.AccountInfo, _Mapping]]] = ..., result: _Optional[_Union[GameEndResult, _Mapping]] = ..., robots: _Optional[_Iterable[_Union[RecordGame.AccountInfo, _Mapping]]] = ..., standard_rule: _Optional[int] = ...) -> None: ...

class RecordGangInfo(_message.Message):
    __slots__ = ()
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
    def __init__(self, seat: _Optional[int] = ..., type: _Optional[int] = ..., pai: _Optional[str] = ..., is_dora: _Optional[bool] = ..., xun: _Optional[int] = ...) -> None: ...

class RecordGangResult(_message.Message):
    __slots__ = ()
    GANG_INFOS_FIELD_NUMBER: _ClassVar[int]
    gang_infos: ChuanmaGang
    def __init__(self, gang_infos: _Optional[_Union[ChuanmaGang, _Mapping]] = ...) -> None: ...

class RecordGangResultEnd(_message.Message):
    __slots__ = ()
    GANG_INFOS_FIELD_NUMBER: _ClassVar[int]
    gang_infos: ChuanmaGang
    def __init__(self, gang_infos: _Optional[_Union[ChuanmaGang, _Mapping]] = ...) -> None: ...

class RecordHule(_message.Message):
    __slots__ = ()
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

class RecordHuleInfo(_message.Message):
    __slots__ = ()
    class RecordFanInfo(_message.Message):
        __slots__ = ()
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
    def __init__(self, hand: _Optional[_Iterable[str]] = ..., ming: _Optional[_Iterable[str]] = ..., hu_tile: _Optional[str] = ..., seat: _Optional[int] = ..., zimo: _Optional[bool] = ..., qinjia: _Optional[bool] = ..., liqi: _Optional[bool] = ..., doras: _Optional[_Iterable[str]] = ..., li_doras: _Optional[_Iterable[str]] = ..., yiman: _Optional[bool] = ..., count: _Optional[int] = ..., fans: _Optional[_Iterable[_Union[RecordHuleInfo.RecordFanInfo, _Mapping]]] = ..., fu: _Optional[int] = ..., point_zimo_qin: _Optional[int] = ..., point_zimo_xian: _Optional[int] = ..., title_id: _Optional[int] = ..., point_sum: _Optional[int] = ..., dadian: _Optional[int] = ..., is_jue_zhang: _Optional[bool] = ..., xun: _Optional[int] = ..., ting_type: _Optional[int] = ..., ting_mian: _Optional[int] = ...) -> None: ...

class RecordHuleXueZhanEnd(_message.Message):
    __slots__ = ()
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

class RecordHuleXueZhanMid(_message.Message):
    __slots__ = ()
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

class RecordHulesInfo(_message.Message):
    __slots__ = ()
    SEAT_FIELD_NUMBER: _ClassVar[int]
    HULES_FIELD_NUMBER: _ClassVar[int]
    seat: int
    hules: _containers.RepeatedCompositeFieldContainer[RecordHuleInfo]
    def __init__(self, seat: _Optional[int] = ..., hules: _Optional[_Iterable[_Union[RecordHuleInfo, _Mapping]]] = ...) -> None: ...

class RecordLiqiInfo(_message.Message):
    __slots__ = ()
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
    def __init__(self, seat: _Optional[int] = ..., score: _Optional[int] = ..., is_w: _Optional[bool] = ..., is_zhen_ting: _Optional[bool] = ..., xun: _Optional[int] = ..., is_success: _Optional[bool] = ...) -> None: ...

class RecordListEntry(_message.Message):
    __slots__ = ()
    VERSION_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    SUBTAG_FIELD_NUMBER: _ClassVar[int]
    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    STANDARD_RULE_FIELD_NUMBER: _ClassVar[int]
    version: int
    uuid: str
    start_time: int
    end_time: int
    tag: int
    subtag: int
    players: _containers.RepeatedCompositeFieldContainer[RecordPlayerResult]
    standard_rule: int
    def __init__(self, version: _Optional[int] = ..., uuid: _Optional[str] = ..., start_time: _Optional[int] = ..., end_time: _Optional[int] = ..., tag: _Optional[int] = ..., subtag: _Optional[int] = ..., players: _Optional[_Iterable[_Union[RecordPlayerResult, _Mapping]]] = ..., standard_rule: _Optional[int] = ...) -> None: ...

class RecordLiuJu(_message.Message):
    __slots__ = ()
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

class RecordLiujuInfo(_message.Message):
    __slots__ = ()
    SEAT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    seat: int
    type: int
    def __init__(self, seat: _Optional[int] = ..., type: _Optional[int] = ...) -> None: ...

class RecordLockTile(_message.Message):
    __slots__ = ()
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

class RecordNewCard(_message.Message):
    __slots__ = ()
    FIELD_SPELL_FIELD_NUMBER: _ClassVar[int]
    field_spell: int
    def __init__(self, field_spell: _Optional[int] = ...) -> None: ...

class RecordNewRound(_message.Message):
    __slots__ = ()
    class TingPai(_message.Message):
        __slots__ = ()
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
    XIA_KE_SHANG_FIELD_NUMBER: _ClassVar[int]
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
    xia_ke_shang: XiaKeShangInfo
    def __init__(self, chang: _Optional[int] = ..., ju: _Optional[int] = ..., ben: _Optional[int] = ..., dora: _Optional[str] = ..., scores: _Optional[_Iterable[int]] = ..., liqibang: _Optional[int] = ..., tiles0: _Optional[_Iterable[str]] = ..., tiles1: _Optional[_Iterable[str]] = ..., tiles2: _Optional[_Iterable[str]] = ..., tiles3: _Optional[_Iterable[str]] = ..., tingpai: _Optional[_Iterable[_Union[RecordNewRound.TingPai, _Mapping]]] = ..., operation: _Optional[_Union[OptionalOperationList, _Mapping]] = ..., md5: _Optional[str] = ..., paishan: _Optional[str] = ..., left_tile_count: _Optional[int] = ..., doras: _Optional[_Iterable[str]] = ..., opens: _Optional[_Iterable[_Union[NewRoundOpenedTiles, _Mapping]]] = ..., muyu: _Optional[_Union[MuyuInfo, _Mapping]] = ..., operations: _Optional[_Iterable[_Union[OptionalOperationList, _Mapping]]] = ..., ju_count: _Optional[int] = ..., field_spell: _Optional[int] = ..., sha256: _Optional[str] = ..., yongchang: _Optional[_Union[YongchangInfo, _Mapping]] = ..., saltSha256: _Optional[str] = ..., salt: _Optional[str] = ..., xia_ke_shang: _Optional[_Union[XiaKeShangInfo, _Mapping]] = ...) -> None: ...

class RecordNoTile(_message.Message):
    __slots__ = ()
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
    def __init__(self, liujumanguan: _Optional[bool] = ..., players: _Optional[_Iterable[_Union[NoTilePlayerInfo, _Mapping]]] = ..., scores: _Optional[_Iterable[_Union[NoTileScoreInfo, _Mapping]]] = ..., gameend: _Optional[bool] = ..., muyu: _Optional[_Union[MuyuInfo, _Mapping]] = ..., hules_history: _Optional[_Iterable[_Union[HuleInfo, _Mapping]]] = ...) -> None: ...

class RecordNoTileInfo(_message.Message):
    __slots__ = ()
    LIUJUMANGUAN_FIELD_NUMBER: _ClassVar[int]
    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    liujumanguan: bool
    players: _containers.RepeatedCompositeFieldContainer[RecordNoTilePlayerInfo]
    def __init__(self, liujumanguan: _Optional[bool] = ..., players: _Optional[_Iterable[_Union[RecordNoTilePlayerInfo, _Mapping]]] = ...) -> None: ...

class RecordNoTilePlayerInfo(_message.Message):
    __slots__ = ()
    TINGPAI_FIELD_NUMBER: _ClassVar[int]
    HAND_FIELD_NUMBER: _ClassVar[int]
    TINGS_FIELD_NUMBER: _ClassVar[int]
    LIUMAN_FIELD_NUMBER: _ClassVar[int]
    tingpai: bool
    hand: _containers.RepeatedScalarFieldContainer[str]
    tings: _containers.RepeatedCompositeFieldContainer[RecordTingPaiInfo]
    liuman: bool
    def __init__(self, tingpai: _Optional[bool] = ..., hand: _Optional[_Iterable[str]] = ..., tings: _Optional[_Iterable[_Union[RecordTingPaiInfo, _Mapping]]] = ..., liuman: _Optional[bool] = ...) -> None: ...

class RecordPeiPaiInfo(_message.Message):
    __slots__ = ()
    DORA_COUNT_FIELD_NUMBER: _ClassVar[int]
    R_DORA_COUNT_FIELD_NUMBER: _ClassVar[int]
    BEI_COUNT_FIELD_NUMBER: _ClassVar[int]
    dora_count: int
    r_dora_count: int
    bei_count: int
    def __init__(self, dora_count: _Optional[int] = ..., r_dora_count: _Optional[int] = ..., bei_count: _Optional[int] = ...) -> None: ...

class RecordPlayerResult(_message.Message):
    __slots__ = ()
    RANK_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    NICKNAME_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    LEVEL3_FIELD_NUMBER: _ClassVar[int]
    SEAT_FIELD_NUMBER: _ClassVar[int]
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
    seat: int
    pt: int
    point: int
    max_hu_type: int
    action_liqi: int
    action_rong: int
    action_zimo: int
    action_chong: int
    verified: int
    def __init__(self, rank: _Optional[int] = ..., account_id: _Optional[int] = ..., nickname: _Optional[str] = ..., level: _Optional[_Union[AccountLevel, _Mapping]] = ..., level3: _Optional[_Union[AccountLevel, _Mapping]] = ..., seat: _Optional[int] = ..., pt: _Optional[int] = ..., point: _Optional[int] = ..., max_hu_type: _Optional[int] = ..., action_liqi: _Optional[int] = ..., action_rong: _Optional[int] = ..., action_zimo: _Optional[int] = ..., action_chong: _Optional[int] = ..., verified: _Optional[int] = ...) -> None: ...

class RecordRevealTile(_message.Message):
    __slots__ = ()
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
    def __init__(self, seat: _Optional[int] = ..., is_liqi: _Optional[bool] = ..., is_wliqi: _Optional[bool] = ..., moqie: _Optional[bool] = ..., scores: _Optional[_Iterable[int]] = ..., liqibang: _Optional[int] = ..., operations: _Optional[_Iterable[_Union[OptionalOperationList, _Mapping]]] = ..., tingpais: _Optional[_Iterable[_Union[TingPaiInfo, _Mapping]]] = ..., tile: _Optional[str] = ..., zhenting: _Optional[_Iterable[bool]] = ...) -> None: ...

class RecordRoundInfo(_message.Message):
    __slots__ = ()
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
    XIULUO_HULES_INFO_FIELD_NUMBER: _ClassVar[int]
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
    xiuluo_hules_info: _containers.RepeatedCompositeFieldContainer[RecordHulesInfo]
    def __init__(self, name: _Optional[str] = ..., chang: _Optional[int] = ..., ju: _Optional[int] = ..., ben: _Optional[int] = ..., scores: _Optional[_Iterable[int]] = ..., liqi_infos: _Optional[_Iterable[_Union[RecordLiqiInfo, _Mapping]]] = ..., gang_infos: _Optional[_Iterable[_Union[RecordGangInfo, _Mapping]]] = ..., peipai_infos: _Optional[_Iterable[_Union[RecordPeiPaiInfo, _Mapping]]] = ..., babai_infos: _Optional[_Iterable[_Union[RecordBaBeiInfo, _Mapping]]] = ..., hules_info: _Optional[_Union[RecordHulesInfo, _Mapping]] = ..., liuju_info: _Optional[_Union[RecordLiujuInfo, _Mapping]] = ..., no_tile_info: _Optional[_Union[RecordNoTileInfo, _Mapping]] = ..., xiuluo_hules_info: _Optional[_Iterable[_Union[RecordHulesInfo, _Mapping]]] = ...) -> None: ...

class RecordSelectGap(_message.Message):
    __slots__ = ()
    class TingPai(_message.Message):
        __slots__ = ()
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

class RecordTingPaiInfo(_message.Message):
    __slots__ = ()
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
    def __init__(self, tile: _Optional[str] = ..., haveyi: _Optional[bool] = ..., yiman: _Optional[bool] = ..., count: _Optional[int] = ..., fu: _Optional[int] = ..., biao_dora_count: _Optional[int] = ..., yiman_zimo: _Optional[bool] = ..., count_zimo: _Optional[int] = ..., fu_zimo: _Optional[int] = ...) -> None: ...

class RecordUnveilTile(_message.Message):
    __slots__ = ()
    SEAT_FIELD_NUMBER: _ClassVar[int]
    SCORES_FIELD_NUMBER: _ClassVar[int]
    LIQIBANG_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    seat: int
    scores: _containers.RepeatedScalarFieldContainer[int]
    liqibang: int
    operation: OptionalOperationList
    def __init__(self, seat: _Optional[int] = ..., scores: _Optional[_Iterable[int]] = ..., liqibang: _Optional[int] = ..., operation: _Optional[_Union[OptionalOperationList, _Mapping]] = ...) -> None: ...

class ReqAccountInfo(_message.Message):
    __slots__ = ()
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    def __init__(self, account_id: _Optional[int] = ...) -> None: ...

class ReqAccountList(_message.Message):
    __slots__ = ()
    ACCOUNT_ID_LIST_FIELD_NUMBER: _ClassVar[int]
    account_id_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, account_id_list: _Optional[_Iterable[int]] = ...) -> None: ...

class ReqAccountStatisticInfo(_message.Message):
    __slots__ = ()
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    def __init__(self, account_id: _Optional[int] = ...) -> None: ...

class ReqAddCollectedGameRecord(_message.Message):
    __slots__ = ()
    UUID_FIELD_NUMBER: _ClassVar[int]
    REMARKS_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    remarks: str
    start_time: int
    end_time: int
    def __init__(self, uuid: _Optional[str] = ..., remarks: _Optional[str] = ..., start_time: _Optional[int] = ..., end_time: _Optional[int] = ...) -> None: ...

class ReqAddRoomRobot(_message.Message):
    __slots__ = ()
    POSITION_FIELD_NUMBER: _ClassVar[int]
    position: int
    def __init__(self, position: _Optional[int] = ...) -> None: ...

class ReqAmuletActivityBuy(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    id: int
    def __init__(self, activity_id: _Optional[int] = ..., id: _Optional[int] = ...) -> None: ...

class ReqAmuletActivityEffectSort(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    SORTED_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    sorted_id: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, activity_id: _Optional[int] = ..., sorted_id: _Optional[_Iterable[int]] = ...) -> None: ...

class ReqAmuletActivityEndShopping(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ReqAmuletActivityFetchBrief(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ReqAmuletActivityFetchInfo(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ReqAmuletActivityGiveup(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ReqAmuletActivityOperate(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TILE_LIST_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    type: int
    tile_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, activity_id: _Optional[int] = ..., type: _Optional[int] = ..., tile_list: _Optional[_Iterable[int]] = ...) -> None: ...

class ReqAmuletActivityRefreshShop(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ReqAmuletActivitySelectBookEffect(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    EFFECT_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    effect_id: int
    def __init__(self, activity_id: _Optional[int] = ..., effect_id: _Optional[int] = ...) -> None: ...

class ReqAmuletActivitySelectFreeEffect(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    SELECTED_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    selected_id: int
    def __init__(self, activity_id: _Optional[int] = ..., selected_id: _Optional[int] = ...) -> None: ...

class ReqAmuletActivitySelectPack(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    id: int
    def __init__(self, activity_id: _Optional[int] = ..., id: _Optional[int] = ...) -> None: ...

class ReqAmuletActivitySelectRewardPack(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    id: int
    def __init__(self, activity_id: _Optional[int] = ..., id: _Optional[int] = ...) -> None: ...

class ReqAmuletActivitySellEffect(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    id: int
    def __init__(self, activity_id: _Optional[int] = ..., id: _Optional[int] = ...) -> None: ...

class ReqAmuletActivitySetSkillLevel(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    SKILL_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    skill: _containers.RepeatedCompositeFieldContainer[AmuletSkillData]
    def __init__(self, activity_id: _Optional[int] = ..., skill: _Optional[_Iterable[_Union[AmuletSkillData, _Mapping]]] = ...) -> None: ...

class ReqAmuletActivityStartGame(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ReqAmuletActivityUpgrade(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ReqAmuletActivityUpgradeShopBuff(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    id: int
    def __init__(self, activity_id: _Optional[int] = ..., id: _Optional[int] = ...) -> None: ...

class ReqApplyFriend(_message.Message):
    __slots__ = ()
    TARGET_ID_FIELD_NUMBER: _ClassVar[int]
    target_id: int
    def __init__(self, target_id: _Optional[int] = ...) -> None: ...

class ReqArenaReward(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ReqAuthGame(_message.Message):
    __slots__ = ()
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

class ReqAuthObserve(_message.Message):
    __slots__ = ()
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: str
    def __init__(self, token: _Optional[str] = ...) -> None: ...

class ReqBindAccount(_message.Message):
    __slots__ = ()
    ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    account: str
    password: str
    def __init__(self, account: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class ReqBindEmail(_message.Message):
    __slots__ = ()
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    email: str
    code: str
    password: str
    def __init__(self, email: _Optional[str] = ..., code: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class ReqBindOauth2(_message.Message):
    __slots__ = ()
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    type: int
    token: str
    def __init__(self, type: _Optional[int] = ..., token: _Optional[str] = ...) -> None: ...

class ReqBindPhoneNumber(_message.Message):
    __slots__ = ()
    CODE_FIELD_NUMBER: _ClassVar[int]
    PHONE_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    MULTI_BIND_VERSION_FIELD_NUMBER: _ClassVar[int]
    code: str
    phone: str
    password: str
    multi_bind_version: bool
    def __init__(self, code: _Optional[str] = ..., phone: _Optional[str] = ..., password: _Optional[str] = ..., multi_bind_version: _Optional[bool] = ...) -> None: ...

class ReqBingoActivityReceiveReward(_message.Message):
    __slots__ = ()
    class BingoReward(_message.Message):
        __slots__ = ()
        REWARD_ID_FIELD_NUMBER: _ClassVar[int]
        CARD_ID_FIELD_NUMBER: _ClassVar[int]
        reward_id: int
        card_id: int
        def __init__(self, reward_id: _Optional[int] = ..., card_id: _Optional[int] = ...) -> None: ...
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    REWARDS_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    rewards: _containers.RepeatedCompositeFieldContainer[ReqBingoActivityReceiveReward.BingoReward]
    def __init__(self, activity_id: _Optional[int] = ..., rewards: _Optional[_Iterable[_Union[ReqBingoActivityReceiveReward.BingoReward, _Mapping]]] = ...) -> None: ...

class ReqBroadcastInGame(_message.Message):
    __slots__ = ()
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    EXCEPT_SELF_FIELD_NUMBER: _ClassVar[int]
    content: str
    except_self: bool
    def __init__(self, content: _Optional[str] = ..., except_self: _Optional[bool] = ...) -> None: ...

class ReqBuyArenaTicket(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ReqBuyFestivalProposal(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ReqBuyFromChestShop(_message.Message):
    __slots__ = ()
    GOODS_ID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    goods_id: int
    count: int
    def __init__(self, goods_id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class ReqBuyFromShop(_message.Message):
    __slots__ = ()
    class Item(_message.Message):
        __slots__ = ()
        ID_FIELD_NUMBER: _ClassVar[int]
        COUNT_FIELD_NUMBER: _ClassVar[int]
        id: int
        count: int
        def __init__(self, id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...
    GOODS_ID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    VER_PRICE_FIELD_NUMBER: _ClassVar[int]
    VER_GOODS_FIELD_NUMBER: _ClassVar[int]
    PACKAGE_GOODS_FIELD_NUMBER: _ClassVar[int]
    goods_id: int
    count: int
    ver_price: _containers.RepeatedCompositeFieldContainer[ReqBuyFromShop.Item]
    ver_goods: _containers.RepeatedCompositeFieldContainer[ReqBuyFromShop.Item]
    package_goods: _containers.RepeatedCompositeFieldContainer[ReqBuyFromShop.Item]
    def __init__(self, goods_id: _Optional[int] = ..., count: _Optional[int] = ..., ver_price: _Optional[_Iterable[_Union[ReqBuyFromShop.Item, _Mapping]]] = ..., ver_goods: _Optional[_Iterable[_Union[ReqBuyFromShop.Item, _Mapping]]] = ..., package_goods: _Optional[_Iterable[_Union[ReqBuyFromShop.Item, _Mapping]]] = ...) -> None: ...

class ReqBuyFromZHP(_message.Message):
    __slots__ = ()
    GOODS_ID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    goods_id: int
    count: int
    def __init__(self, goods_id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class ReqBuyInABMatch(_message.Message):
    __slots__ = ()
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    match_id: int
    def __init__(self, match_id: _Optional[int] = ...) -> None: ...

class ReqBuyShiLian(_message.Message):
    __slots__ = ()
    TYPE_FIELD_NUMBER: _ClassVar[int]
    type: int
    def __init__(self, type: _Optional[int] = ...) -> None: ...

class ReqCancelGooglePlayOrder(_message.Message):
    __slots__ = ()
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    def __init__(self, order_id: _Optional[str] = ...) -> None: ...

class ReqCancelMatchQueue(_message.Message):
    __slots__ = ()
    MATCH_MODE_FIELD_NUMBER: _ClassVar[int]
    match_mode: int
    def __init__(self, match_mode: _Optional[int] = ...) -> None: ...

class ReqCancelUnifiedMatch(_message.Message):
    __slots__ = ()
    MATCH_SID_FIELD_NUMBER: _ClassVar[int]
    match_sid: str
    def __init__(self, match_sid: _Optional[str] = ...) -> None: ...

class ReqChallangeLeaderboard(_message.Message):
    __slots__ = ()
    SEASON_FIELD_NUMBER: _ClassVar[int]
    season: int
    def __init__(self, season: _Optional[int] = ...) -> None: ...

class ReqChangeAvatar(_message.Message):
    __slots__ = ()
    AVATAR_ID_FIELD_NUMBER: _ClassVar[int]
    avatar_id: int
    def __init__(self, avatar_id: _Optional[int] = ...) -> None: ...

class ReqChangeCharacterSkin(_message.Message):
    __slots__ = ()
    CHARACTER_ID_FIELD_NUMBER: _ClassVar[int]
    SKIN_FIELD_NUMBER: _ClassVar[int]
    character_id: int
    skin: int
    def __init__(self, character_id: _Optional[int] = ..., skin: _Optional[int] = ...) -> None: ...

class ReqChangeCharacterView(_message.Message):
    __slots__ = ()
    CHARACTER_ID_FIELD_NUMBER: _ClassVar[int]
    SLOT_FIELD_NUMBER: _ClassVar[int]
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    character_id: int
    slot: int
    item_id: int
    def __init__(self, character_id: _Optional[int] = ..., slot: _Optional[int] = ..., item_id: _Optional[int] = ...) -> None: ...

class ReqChangeCollectedGameRecordRemarks(_message.Message):
    __slots__ = ()
    UUID_FIELD_NUMBER: _ClassVar[int]
    REMARKS_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    remarks: str
    def __init__(self, uuid: _Optional[str] = ..., remarks: _Optional[str] = ...) -> None: ...

class ReqChangeCommonView(_message.Message):
    __slots__ = ()
    SLOT_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    slot: int
    value: int
    def __init__(self, slot: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...

class ReqChangeMainCharacter(_message.Message):
    __slots__ = ()
    CHARACTER_ID_FIELD_NUMBER: _ClassVar[int]
    character_id: int
    def __init__(self, character_id: _Optional[int] = ...) -> None: ...

class ReqCheckPrivacy(_message.Message):
    __slots__ = ()
    class Versions(_message.Message):
        __slots__ = ()
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

class ReqChiPengGang(_message.Message):
    __slots__ = ()
    TYPE_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    CANCEL_OPERATION_FIELD_NUMBER: _ClassVar[int]
    TIMEUSE_FIELD_NUMBER: _ClassVar[int]
    type: int
    index: int
    cancel_operation: bool
    timeuse: int
    def __init__(self, type: _Optional[int] = ..., index: _Optional[int] = ..., cancel_operation: _Optional[bool] = ..., timeuse: _Optional[int] = ...) -> None: ...

class ReqClientMessage(_message.Message):
    __slots__ = ()
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    timestamp: int
    message: str
    def __init__(self, timestamp: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...

class ReqCombiningRecycleCraft(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    POS_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    pos: int
    def __init__(self, activity_id: _Optional[int] = ..., pos: _Optional[int] = ...) -> None: ...

class ReqCommon(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ReqCommonViews(_message.Message):
    __slots__ = ()
    INDEX_FIELD_NUMBER: _ClassVar[int]
    index: int
    def __init__(self, index: _Optional[int] = ...) -> None: ...

class ReqCompleteActivityTask(_message.Message):
    __slots__ = ()
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    task_id: int
    def __init__(self, task_id: _Optional[int] = ...) -> None: ...

class ReqCompleteActivityTaskBatch(_message.Message):
    __slots__ = ()
    TASK_LIST_FIELD_NUMBER: _ClassVar[int]
    task_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, task_list: _Optional[_Iterable[int]] = ...) -> None: ...

class ReqCompletePeriodActivityTaskBatch(_message.Message):
    __slots__ = ()
    TASK_LIST_FIELD_NUMBER: _ClassVar[int]
    task_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, task_list: _Optional[_Iterable[int]] = ...) -> None: ...

class ReqCompleteSegmentTaskReward(_message.Message):
    __slots__ = ()
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    task_id: int
    count: int
    def __init__(self, task_id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class ReqCompleteVillageTask(_message.Message):
    __slots__ = ()
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    task_id: int
    activity_id: int
    def __init__(self, task_id: _Optional[int] = ..., activity_id: _Optional[int] = ...) -> None: ...

class ReqComposeShard(_message.Message):
    __slots__ = ()
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    item_id: int
    def __init__(self, item_id: _Optional[int] = ...) -> None: ...

class ReqCreateAlipayAppOrder(_message.Message):
    __slots__ = ()
    GOODS_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    goods_id: int
    client_type: int
    account_id: int
    client_version_string: str
    def __init__(self, goods_id: _Optional[int] = ..., client_type: _Optional[int] = ..., account_id: _Optional[int] = ..., client_version_string: _Optional[str] = ...) -> None: ...

class ReqCreateAlipayOrder(_message.Message):
    __slots__ = ()
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

class ReqCreateAlipayScanOrder(_message.Message):
    __slots__ = ()
    GOODS_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    goods_id: int
    client_type: int
    account_id: int
    client_version_string: str
    def __init__(self, goods_id: _Optional[int] = ..., client_type: _Optional[int] = ..., account_id: _Optional[int] = ..., client_version_string: _Optional[str] = ...) -> None: ...

class ReqCreateBillingOrder(_message.Message):
    __slots__ = ()
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

class ReqCreateCustomizedContest(_message.Message):
    __slots__ = ()
    NAME_FIELD_NUMBER: _ClassVar[int]
    OPEN_SHOW_FIELD_NUMBER: _ClassVar[int]
    GAME_RULE_SETTING_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    AUTO_MATCH_FIELD_NUMBER: _ClassVar[int]
    RANK_RULE_FIELD_NUMBER: _ClassVar[int]
    CONTEST_SETTING_FIELD_NUMBER: _ClassVar[int]
    RANK_TYPE_FIELD_NUMBER: _ClassVar[int]
    name: str
    open_show: int
    game_rule_setting: GameMode
    start_time: int
    end_time: int
    auto_match: int
    rank_rule: int
    contest_setting: ContestSetting
    rank_type: int
    def __init__(self, name: _Optional[str] = ..., open_show: _Optional[int] = ..., game_rule_setting: _Optional[_Union[GameMode, _Mapping]] = ..., start_time: _Optional[int] = ..., end_time: _Optional[int] = ..., auto_match: _Optional[int] = ..., rank_rule: _Optional[int] = ..., contest_setting: _Optional[_Union[ContestSetting, _Mapping]] = ..., rank_type: _Optional[int] = ...) -> None: ...

class ReqCreateDMMOrder(_message.Message):
    __slots__ = ()
    GOODS_ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    goods_id: int
    account_id: int
    client_type: int
    client_version_string: str
    def __init__(self, goods_id: _Optional[int] = ..., account_id: _Optional[int] = ..., client_type: _Optional[int] = ..., client_version_string: _Optional[str] = ...) -> None: ...

class ReqCreateENAlipayOrder(_message.Message):
    __slots__ = ()
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

class ReqCreateENJCBOrder(_message.Message):
    __slots__ = ()
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

class ReqCreateENMasterCardOrder(_message.Message):
    __slots__ = ()
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

class ReqCreateENPaypalOrder(_message.Message):
    __slots__ = ()
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

class ReqCreateENVisaOrder(_message.Message):
    __slots__ = ()
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

class ReqCreateEmailVerifyCode(_message.Message):
    __slots__ = ()
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    USAGE_FIELD_NUMBER: _ClassVar[int]
    email: str
    usage: int
    def __init__(self, email: _Optional[str] = ..., usage: _Optional[int] = ...) -> None: ...

class ReqCreateGameObserveAuth(_message.Message):
    __slots__ = ()
    GAME_UUID_FIELD_NUMBER: _ClassVar[int]
    game_uuid: str
    def __init__(self, game_uuid: _Optional[str] = ...) -> None: ...

class ReqCreateGamePlan(_message.Message):
    __slots__ = ()
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

class ReqCreateIAPOrder(_message.Message):
    __slots__ = ()
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

class ReqCreateJPAuOrder(_message.Message):
    __slots__ = ()
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

class ReqCreateJPCreditCardOrder(_message.Message):
    __slots__ = ()
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

class ReqCreateJPDocomoOrder(_message.Message):
    __slots__ = ()
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

class ReqCreateJPGMOOrder(_message.Message):
    __slots__ = ()
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

class ReqCreateJPPayPayOrder(_message.Message):
    __slots__ = ()
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

class ReqCreateJPPaypalOrder(_message.Message):
    __slots__ = ()
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

class ReqCreateJPSoftbankOrder(_message.Message):
    __slots__ = ()
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

class ReqCreateJPWebMoneyOrder(_message.Message):
    __slots__ = ()
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

class ReqCreateKRAlipayOrder(_message.Message):
    __slots__ = ()
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

class ReqCreateKRJCBOrder(_message.Message):
    __slots__ = ()
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

class ReqCreateKRMasterCardOrder(_message.Message):
    __slots__ = ()
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

class ReqCreateKRPaypalOrder(_message.Message):
    __slots__ = ()
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

class ReqCreateKRVisaOrder(_message.Message):
    __slots__ = ()
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

class ReqCreateMyCardOrder(_message.Message):
    __slots__ = ()
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

class ReqCreateNickname(_message.Message):
    __slots__ = ()
    NICKNAME_FIELD_NUMBER: _ClassVar[int]
    ADVERTISE_STR_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    nickname: str
    advertise_str: str
    tag: str
    def __init__(self, nickname: _Optional[str] = ..., advertise_str: _Optional[str] = ..., tag: _Optional[str] = ...) -> None: ...

class ReqCreatePaypalOrder(_message.Message):
    __slots__ = ()
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

class ReqCreatePhoneLoginBind(_message.Message):
    __slots__ = ()
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    password: str
    def __init__(self, password: _Optional[str] = ...) -> None: ...

class ReqCreatePhoneVerifyCode(_message.Message):
    __slots__ = ()
    PHONE_FIELD_NUMBER: _ClassVar[int]
    USAGE_FIELD_NUMBER: _ClassVar[int]
    phone: str
    usage: int
    def __init__(self, phone: _Optional[str] = ..., usage: _Optional[int] = ...) -> None: ...

class ReqCreateRoom(_message.Message):
    __slots__ = ()
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
    def __init__(self, player_count: _Optional[int] = ..., mode: _Optional[_Union[GameMode, _Mapping]] = ..., public_live: _Optional[bool] = ..., client_version_string: _Optional[str] = ..., pre_rule: _Optional[str] = ...) -> None: ...

class ReqCreateSeerReport(_message.Message):
    __slots__ = ()
    UUID_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    def __init__(self, uuid: _Optional[str] = ...) -> None: ...

class ReqCreateSteamOrder(_message.Message):
    __slots__ = ()
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

class ReqCreateWechatAppOrder(_message.Message):
    __slots__ = ()
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

class ReqCreateWechatNativeOrder(_message.Message):
    __slots__ = ()
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

class ReqCreateXsollaOrder(_message.Message):
    __slots__ = ()
    GOODS_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    PAYMENT_METHOD_FIELD_NUMBER: _ClassVar[int]
    DEBT_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_IP_FIELD_NUMBER: _ClassVar[int]
    goods_id: int
    client_type: int
    account_id: int
    payment_method: int
    debt_order_id: str
    client_version_string: str
    account_ip: str
    def __init__(self, goods_id: _Optional[int] = ..., client_type: _Optional[int] = ..., account_id: _Optional[int] = ..., payment_method: _Optional[int] = ..., debt_order_id: _Optional[str] = ..., client_version_string: _Optional[str] = ..., account_ip: _Optional[str] = ...) -> None: ...

class ReqCreateYostarOrder(_message.Message):
    __slots__ = ()
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

class ReqCurrentMatchInfo(_message.Message):
    __slots__ = ()
    MODE_LIST_FIELD_NUMBER: _ClassVar[int]
    mode_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, mode_list: _Optional[_Iterable[int]] = ...) -> None: ...

class ReqDMMPreLogin(_message.Message):
    __slots__ = ()
    FINISH_URL_FIELD_NUMBER: _ClassVar[int]
    finish_url: str
    def __init__(self, finish_url: _Optional[str] = ...) -> None: ...

class ReqDeleteComment(_message.Message):
    __slots__ = ()
    TARGET_ID_FIELD_NUMBER: _ClassVar[int]
    DELETE_LIST_FIELD_NUMBER: _ClassVar[int]
    target_id: int
    delete_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, target_id: _Optional[int] = ..., delete_list: _Optional[_Iterable[int]] = ...) -> None: ...

class ReqDeleteMail(_message.Message):
    __slots__ = ()
    MAIL_ID_FIELD_NUMBER: _ClassVar[int]
    mail_id: int
    def __init__(self, mail_id: _Optional[int] = ...) -> None: ...

class ReqDeliverAA32Order(_message.Message):
    __slots__ = ()
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    NSA_ID_FIELD_NUMBER: _ClassVar[int]
    NSA_TOKEN_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    nsa_id: str
    nsa_token: str
    def __init__(self, account_id: _Optional[int] = ..., nsa_id: _Optional[str] = ..., nsa_token: _Optional[str] = ...) -> None: ...

class ReqDigMine(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    POINT_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    point: Point
    def __init__(self, activity_id: _Optional[int] = ..., point: _Optional[_Union[Point, _Mapping]] = ...) -> None: ...

class ReqDoActivitySignIn(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ReqEmailLogin(_message.Message):
    __slots__ = ()
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
    def __init__(self, email: _Optional[str] = ..., password: _Optional[str] = ..., reconnect: _Optional[bool] = ..., device: _Optional[_Union[ClientDeviceInfo, _Mapping]] = ..., random_key: _Optional[str] = ..., client_version: _Optional[str] = ..., gen_access_token: _Optional[bool] = ..., currency_platforms: _Optional[_Iterable[int]] = ...) -> None: ...

class ReqEnterArena(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ReqEnterCustomizedContest(_message.Message):
    __slots__ = ()
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    LANG_FIELD_NUMBER: _ClassVar[int]
    unique_id: int
    lang: str
    def __init__(self, unique_id: _Optional[int] = ..., lang: _Optional[str] = ...) -> None: ...

class ReqExchangeActivityItem(_message.Message):
    __slots__ = ()
    EXCHANGE_ID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    exchange_id: int
    count: int
    def __init__(self, exchange_id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class ReqExchangeCurrency(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    id: int
    count: int
    def __init__(self, id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class ReqFastLogin(_message.Message):
    __slots__ = ()
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    client_version_string: str
    def __init__(self, client_version_string: _Optional[str] = ...) -> None: ...

class ReqFeedActivityFeed(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    count: int
    def __init__(self, activity_id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class ReqFetchAccountGameHuRecords(_message.Message):
    __slots__ = ()
    UUID_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    category: int
    type: int
    def __init__(self, uuid: _Optional[str] = ..., category: _Optional[int] = ..., type: _Optional[int] = ...) -> None: ...

class ReqFetchAccountInfoExtra(_message.Message):
    __slots__ = ()
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    category: int
    type: int
    def __init__(self, account_id: _Optional[int] = ..., category: _Optional[int] = ..., type: _Optional[int] = ...) -> None: ...

class ReqFetchActivityFlipInfo(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ReqFetchActivityRank(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_LIST_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    account_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, activity_id: _Optional[int] = ..., account_list: _Optional[_Iterable[int]] = ...) -> None: ...

class ReqFetchAmuletActivityData(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ReqFetchAnnouncement(_message.Message):
    __slots__ = ()
    LANG_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_FIELD_NUMBER: _ClassVar[int]
    lang: str
    platform: str
    def __init__(self, lang: _Optional[str] = ..., platform: _Optional[str] = ...) -> None: ...

class ReqFetchBingoActivityData(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ReqFetchCommentContent(_message.Message):
    __slots__ = ()
    TARGET_ID_FIELD_NUMBER: _ClassVar[int]
    COMMENT_ID_LIST_FIELD_NUMBER: _ClassVar[int]
    target_id: int
    comment_id_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, target_id: _Optional[int] = ..., comment_id_list: _Optional[_Iterable[int]] = ...) -> None: ...

class ReqFetchCommentList(_message.Message):
    __slots__ = ()
    TARGET_ID_FIELD_NUMBER: _ClassVar[int]
    target_id: int
    def __init__(self, target_id: _Optional[int] = ...) -> None: ...

class ReqFetchContestPlayerRank(_message.Message):
    __slots__ = ()
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    unique_id: int
    limit: int
    offset: int
    def __init__(self, unique_id: _Optional[int] = ..., limit: _Optional[int] = ..., offset: _Optional[int] = ...) -> None: ...

class ReqFetchContestTeamMember(_message.Message):
    __slots__ = ()
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    unique_id: int
    team_id: int
    offset: int
    limit: int
    def __init__(self, unique_id: _Optional[int] = ..., team_id: _Optional[int] = ..., offset: _Optional[int] = ..., limit: _Optional[int] = ...) -> None: ...

class ReqFetchContestTeamPlayerRank(_message.Message):
    __slots__ = ()
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    unique_id: int
    offset: int
    limit: int
    def __init__(self, unique_id: _Optional[int] = ..., offset: _Optional[int] = ..., limit: _Optional[int] = ...) -> None: ...

class ReqFetchContestTeamRank(_message.Message):
    __slots__ = ()
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    unique_id: int
    limit: int
    offset: int
    def __init__(self, unique_id: _Optional[int] = ..., limit: _Optional[int] = ..., offset: _Optional[int] = ...) -> None: ...

class ReqFetchCustomizedContestAuthInfo(_message.Message):
    __slots__ = ()
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    unique_id: int
    def __init__(self, unique_id: _Optional[int] = ...) -> None: ...

class ReqFetchCustomizedContestByContestId(_message.Message):
    __slots__ = ()
    CONTEST_ID_FIELD_NUMBER: _ClassVar[int]
    LANG_FIELD_NUMBER: _ClassVar[int]
    contest_id: int
    lang: str
    def __init__(self, contest_id: _Optional[int] = ..., lang: _Optional[str] = ...) -> None: ...

class ReqFetchCustomizedContestGameLiveList(_message.Message):
    __slots__ = ()
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    unique_id: int
    def __init__(self, unique_id: _Optional[int] = ...) -> None: ...

class ReqFetchCustomizedContestGameRecords(_message.Message):
    __slots__ = ()
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_INDEX_FIELD_NUMBER: _ClassVar[int]
    SEASON_ID_FIELD_NUMBER: _ClassVar[int]
    unique_id: int
    last_index: int
    season_id: int
    def __init__(self, unique_id: _Optional[int] = ..., last_index: _Optional[int] = ..., season_id: _Optional[int] = ...) -> None: ...

class ReqFetchCustomizedContestList(_message.Message):
    __slots__ = ()
    START_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    LANG_FIELD_NUMBER: _ClassVar[int]
    start: int
    count: int
    lang: str
    def __init__(self, start: _Optional[int] = ..., count: _Optional[int] = ..., lang: _Optional[str] = ...) -> None: ...

class ReqFetchCustomizedContestOnlineInfo(_message.Message):
    __slots__ = ()
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    unique_id: int
    def __init__(self, unique_id: _Optional[int] = ...) -> None: ...

class ReqFetchFriendGiftActivityData(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_LIST_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    account_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, activity_id: _Optional[int] = ..., account_list: _Optional[_Iterable[int]] = ...) -> None: ...

class ReqFetchJPCommonCreditCardOrder(_message.Message):
    __slots__ = ()
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    account_id: int
    def __init__(self, order_id: _Optional[str] = ..., account_id: _Optional[int] = ...) -> None: ...

class ReqFetchLastPrivacy(_message.Message):
    __slots__ = ()
    TYPE_FIELD_NUMBER: _ClassVar[int]
    type: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, type: _Optional[_Iterable[int]] = ...) -> None: ...

class ReqFetchManagerCustomizedContest(_message.Message):
    __slots__ = ()
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    unique_id: int
    def __init__(self, unique_id: _Optional[int] = ...) -> None: ...

class ReqFetchOBToken(_message.Message):
    __slots__ = ()
    UUID_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    def __init__(self, uuid: _Optional[str] = ...) -> None: ...

class ReqFetchOauth2(_message.Message):
    __slots__ = ()
    TYPE_FIELD_NUMBER: _ClassVar[int]
    type: int
    def __init__(self, type: _Optional[int] = ...) -> None: ...

class ReqFetchProgressRewardActivityInfo(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ReqFetchQuestionnaireDetail(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    LANG_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    id: int
    lang: str
    channel: str
    def __init__(self, id: _Optional[int] = ..., lang: _Optional[str] = ..., channel: _Optional[str] = ...) -> None: ...

class ReqFetchQuestionnaireList(_message.Message):
    __slots__ = ()
    LANG_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    lang: str
    channel: str
    def __init__(self, lang: _Optional[str] = ..., channel: _Optional[str] = ...) -> None: ...

class ReqFetchRPGBattleHistory(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ReqFetchRankPointLeaderboard(_message.Message):
    __slots__ = ()
    LEADERBOARD_ID_FIELD_NUMBER: _ClassVar[int]
    leaderboard_id: int
    def __init__(self, leaderboard_id: _Optional[int] = ...) -> None: ...

class ReqFetchReadyPlayerList(_message.Message):
    __slots__ = ()
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    unique_id: int
    def __init__(self, unique_id: _Optional[int] = ...) -> None: ...

class ReqFetchRollingNotice(_message.Message):
    __slots__ = ()
    LANG_FIELD_NUMBER: _ClassVar[int]
    lang: str
    def __init__(self, lang: _Optional[str] = ...) -> None: ...

class ReqFetchSeerReport(_message.Message):
    __slots__ = ()
    UUID_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    def __init__(self, uuid: _Optional[str] = ...) -> None: ...

class ReqFetchSimulationGameRank(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    DAY_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    day: int
    def __init__(self, activity_id: _Optional[int] = ..., day: _Optional[int] = ...) -> None: ...

class ReqFetchSimulationGameRecord(_message.Message):
    __slots__ = ()
    GAME_UUID_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    game_uuid: str
    activity_id: int
    def __init__(self, game_uuid: _Optional[str] = ..., activity_id: _Optional[int] = ...) -> None: ...

class ReqFetchVoteActivity(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ReqFetchmanagerCustomizedContestList(_message.Message):
    __slots__ = ()
    LANG_FIELD_NUMBER: _ClassVar[int]
    lang: str
    def __init__(self, lang: _Optional[str] = ...) -> None: ...

class ReqFinishCombiningOrder(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    CRAFT_POS_FIELD_NUMBER: _ClassVar[int]
    ORDER_POS_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    craft_pos: int
    order_pos: int
    def __init__(self, activity_id: _Optional[int] = ..., craft_pos: _Optional[int] = ..., order_pos: _Optional[int] = ...) -> None: ...

class ReqFinishedEnding(_message.Message):
    __slots__ = ()
    CHARACTER_ID_FIELD_NUMBER: _ClassVar[int]
    STORY_ID_FIELD_NUMBER: _ClassVar[int]
    ENDING_ID_FIELD_NUMBER: _ClassVar[int]
    character_id: int
    story_id: int
    ending_id: int
    def __init__(self, character_id: _Optional[int] = ..., story_id: _Optional[int] = ..., ending_id: _Optional[int] = ...) -> None: ...

class ReqForceCompleteChallengeTask(_message.Message):
    __slots__ = ()
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    task_id: int
    def __init__(self, task_id: _Optional[int] = ...) -> None: ...

class ReqGMCommand(_message.Message):
    __slots__ = ()
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    command: str
    def __init__(self, command: _Optional[str] = ...) -> None: ...

class ReqGMCommandInGaming(_message.Message):
    __slots__ = ()
    JSON_DATA_FIELD_NUMBER: _ClassVar[int]
    json_data: str
    def __init__(self, json_data: _Optional[str] = ...) -> None: ...

class ReqGainAccumulatedPointActivityReward(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    REWARD_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    reward_id: int
    def __init__(self, activity_id: _Optional[int] = ..., reward_id: _Optional[int] = ...) -> None: ...

class ReqGainMultiPointActivityReward(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    REWARD_ID_LIST_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    reward_id_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, activity_id: _Optional[int] = ..., reward_id_list: _Optional[_Iterable[int]] = ...) -> None: ...

class ReqGainRankPointReward(_message.Message):
    __slots__ = ()
    LEADERBOARD_ID_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    leaderboard_id: int
    activity_id: int
    def __init__(self, leaderboard_id: _Optional[int] = ..., activity_id: _Optional[int] = ...) -> None: ...

class ReqGainVipReward(_message.Message):
    __slots__ = ()
    VIP_LEVEL_FIELD_NUMBER: _ClassVar[int]
    vip_level: int
    def __init__(self, vip_level: _Optional[int] = ...) -> None: ...

class ReqGameLiveInfo(_message.Message):
    __slots__ = ()
    GAME_UUID_FIELD_NUMBER: _ClassVar[int]
    game_uuid: str
    def __init__(self, game_uuid: _Optional[str] = ...) -> None: ...

class ReqGameLiveLeftSegment(_message.Message):
    __slots__ = ()
    GAME_UUID_FIELD_NUMBER: _ClassVar[int]
    LAST_SEGMENT_ID_FIELD_NUMBER: _ClassVar[int]
    game_uuid: str
    last_segment_id: int
    def __init__(self, game_uuid: _Optional[str] = ..., last_segment_id: _Optional[int] = ...) -> None: ...

class ReqGameLiveList(_message.Message):
    __slots__ = ()
    FILTER_ID_FIELD_NUMBER: _ClassVar[int]
    filter_id: int
    def __init__(self, filter_id: _Optional[int] = ...) -> None: ...

class ReqGamePointRank(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ReqGameRecord(_message.Message):
    __slots__ = ()
    GAME_UUID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    game_uuid: str
    client_version_string: str
    def __init__(self, game_uuid: _Optional[str] = ..., client_version_string: _Optional[str] = ...) -> None: ...

class ReqGameRecordList(_message.Message):
    __slots__ = ()
    START_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    start: int
    count: int
    type: int
    def __init__(self, start: _Optional[int] = ..., count: _Optional[int] = ..., type: _Optional[int] = ...) -> None: ...

class ReqGameRecordListV2(_message.Message):
    __slots__ = ()
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

class ReqGameRecordsDetail(_message.Message):
    __slots__ = ()
    UUID_LIST_FIELD_NUMBER: _ClassVar[int]
    uuid_list: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, uuid_list: _Optional[_Iterable[str]] = ...) -> None: ...

class ReqGameRecordsDetailV2(_message.Message):
    __slots__ = ()
    UUID_LIST_FIELD_NUMBER: _ClassVar[int]
    uuid_list: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, uuid_list: _Optional[_Iterable[str]] = ...) -> None: ...

class ReqGenerateAnnualReportToken(_message.Message):
    __slots__ = ()
    LANG_FIELD_NUMBER: _ClassVar[int]
    lang: str
    def __init__(self, lang: _Optional[str] = ...) -> None: ...

class ReqGenerateCombiningCraft(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    BIN_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    bin_id: int
    def __init__(self, activity_id: _Optional[int] = ..., bin_id: _Optional[int] = ...) -> None: ...

class ReqGetFriendVillageData(_message.Message):
    __slots__ = ()
    ACCOUNT_LIST_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    account_list: _containers.RepeatedScalarFieldContainer[int]
    activity_id: int
    def __init__(self, account_list: _Optional[_Iterable[int]] = ..., activity_id: _Optional[int] = ...) -> None: ...

class ReqHandleFriendApply(_message.Message):
    __slots__ = ()
    TARGET_ID_FIELD_NUMBER: _ClassVar[int]
    METHOD_FIELD_NUMBER: _ClassVar[int]
    target_id: int
    method: int
    def __init__(self, target_id: _Optional[int] = ..., method: _Optional[int] = ...) -> None: ...

class ReqHeartbeat(_message.Message):
    __slots__ = ()
    DELAY_FIELD_NUMBER: _ClassVar[int]
    NO_OPERATION_COUNTER_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_FIELD_NUMBER: _ClassVar[int]
    NETWORK_QUALITY_FIELD_NUMBER: _ClassVar[int]
    delay: int
    no_operation_counter: int
    platform: int
    network_quality: int
    def __init__(self, delay: _Optional[int] = ..., no_operation_counter: _Optional[int] = ..., platform: _Optional[int] = ..., network_quality: _Optional[int] = ...) -> None: ...

class ReqHeatBeat(_message.Message):
    __slots__ = ()
    NO_OPERATION_COUNTER_FIELD_NUMBER: _ClassVar[int]
    no_operation_counter: int
    def __init__(self, no_operation_counter: _Optional[int] = ...) -> None: ...

class ReqIslandActivityBuy(_message.Message):
    __slots__ = ()
    class BuyItems(_message.Message):
        __slots__ = ()
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

class ReqIslandActivityMove(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    ZONE_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    zone_id: int
    def __init__(self, activity_id: _Optional[int] = ..., zone_id: _Optional[int] = ...) -> None: ...

class ReqIslandActivitySell(_message.Message):
    __slots__ = ()
    class SellItem(_message.Message):
        __slots__ = ()
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
    __slots__ = ()
    class BagData(_message.Message):
        __slots__ = ()
        class ITemData(_message.Message):
            __slots__ = ()
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
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    BAG_ID_FIELD_NUMBER: _ClassVar[int]
    POS_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    bag_id: int
    pos: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, activity_id: _Optional[int] = ..., bag_id: _Optional[int] = ..., pos: _Optional[_Iterable[int]] = ...) -> None: ...

class ReqJoinCustomizedContestChatRoom(_message.Message):
    __slots__ = ()
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    unique_id: int
    def __init__(self, unique_id: _Optional[int] = ...) -> None: ...

class ReqJoinMatchQueue(_message.Message):
    __slots__ = ()
    MATCH_MODE_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    match_mode: int
    client_version_string: str
    def __init__(self, match_mode: _Optional[int] = ..., client_version_string: _Optional[str] = ...) -> None: ...

class ReqJoinRoom(_message.Message):
    __slots__ = ()
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    room_id: int
    client_version_string: str
    def __init__(self, room_id: _Optional[int] = ..., client_version_string: _Optional[str] = ...) -> None: ...

class ReqLeaveComment(_message.Message):
    __slots__ = ()
    TARGET_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    target_id: int
    content: str
    def __init__(self, target_id: _Optional[int] = ..., content: _Optional[str] = ...) -> None: ...

class ReqLevelLeaderboard(_message.Message):
    __slots__ = ()
    TYPE_FIELD_NUMBER: _ClassVar[int]
    type: int
    def __init__(self, type: _Optional[int] = ...) -> None: ...

class ReqLikeSNS(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class ReqLogReport(_message.Message):
    __slots__ = ()
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    FAILED_FIELD_NUMBER: _ClassVar[int]
    success: int
    failed: int
    def __init__(self, success: _Optional[int] = ..., failed: _Optional[int] = ...) -> None: ...

class ReqLogin(_message.Message):
    __slots__ = ()
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
    def __init__(self, account: _Optional[str] = ..., password: _Optional[str] = ..., reconnect: _Optional[bool] = ..., device: _Optional[_Union[ClientDeviceInfo, _Mapping]] = ..., random_key: _Optional[str] = ..., client_version: _Optional[_Union[ClientVersionInfo, _Mapping]] = ..., gen_access_token: _Optional[bool] = ..., currency_platforms: _Optional[_Iterable[int]] = ..., type: _Optional[int] = ..., version: _Optional[int] = ..., client_version_string: _Optional[str] = ..., tag: _Optional[str] = ...) -> None: ...

class ReqLoginBeat(_message.Message):
    __slots__ = ()
    CONTRACT_FIELD_NUMBER: _ClassVar[int]
    contract: str
    def __init__(self, contract: _Optional[str] = ...) -> None: ...

class ReqLogout(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ReqModifyBirthday(_message.Message):
    __slots__ = ()
    BIRTHDAY_FIELD_NUMBER: _ClassVar[int]
    birthday: int
    def __init__(self, birthday: _Optional[int] = ...) -> None: ...

class ReqModifyNickname(_message.Message):
    __slots__ = ()
    NICKNAME_FIELD_NUMBER: _ClassVar[int]
    USE_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    nickname: str
    use_item_id: int
    def __init__(self, nickname: _Optional[str] = ..., use_item_id: _Optional[int] = ...) -> None: ...

class ReqModifyPassword(_message.Message):
    __slots__ = ()
    NEW_PASSWORD_FIELD_NUMBER: _ClassVar[int]
    OLD_PASSWORD_FIELD_NUMBER: _ClassVar[int]
    SECURE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    new_password: str
    old_password: str
    secure_token: str
    def __init__(self, new_password: _Optional[str] = ..., old_password: _Optional[str] = ..., secure_token: _Optional[str] = ...) -> None: ...

class ReqModifyRoom(_message.Message):
    __slots__ = ()
    ROBOT_COUNT_FIELD_NUMBER: _ClassVar[int]
    robot_count: int
    def __init__(self, robot_count: _Optional[int] = ...) -> None: ...

class ReqModifySignature(_message.Message):
    __slots__ = ()
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    signature: str
    def __init__(self, signature: _Optional[str] = ...) -> None: ...

class ReqMoveCombiningCraft(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    FROM_FIELD_NUMBER: _ClassVar[int]
    TO_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    to: int
    def __init__(self, activity_id: _Optional[int] = ..., to: _Optional[int] = ..., **kwargs) -> None: ...

class ReqMultiAccountId(_message.Message):
    __slots__ = ()
    ACCOUNT_ID_LIST_FIELD_NUMBER: _ClassVar[int]
    account_id_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, account_id_list: _Optional[_Iterable[int]] = ...) -> None: ...

class ReqMutiChallengeLevel(_message.Message):
    __slots__ = ()
    ACCOUNT_ID_LIST_FIELD_NUMBER: _ClassVar[int]
    SEASON_FIELD_NUMBER: _ClassVar[int]
    account_id_list: _containers.RepeatedScalarFieldContainer[int]
    season: int
    def __init__(self, account_id_list: _Optional[_Iterable[int]] = ..., season: _Optional[int] = ...) -> None: ...

class ReqNextGameRecordList(_message.Message):
    __slots__ = ()
    ITERATOR_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    iterator: str
    count: int
    def __init__(self, iterator: _Optional[str] = ..., count: _Optional[int] = ...) -> None: ...

class ReqNextRoundVillage(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ReqOauth2Auth(_message.Message):
    __slots__ = ()
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    UID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    type: int
    code: str
    uid: str
    client_version_string: str
    def __init__(self, type: _Optional[int] = ..., code: _Optional[str] = ..., uid: _Optional[str] = ..., client_version_string: _Optional[str] = ...) -> None: ...

class ReqOauth2Check(_message.Message):
    __slots__ = ()
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    type: int
    access_token: str
    def __init__(self, type: _Optional[int] = ..., access_token: _Optional[str] = ...) -> None: ...

class ReqOauth2Login(_message.Message):
    __slots__ = ()
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
    def __init__(self, type: _Optional[int] = ..., access_token: _Optional[str] = ..., reconnect: _Optional[bool] = ..., device: _Optional[_Union[ClientDeviceInfo, _Mapping]] = ..., random_key: _Optional[str] = ..., client_version: _Optional[_Union[ClientVersionInfo, _Mapping]] = ..., gen_access_token: _Optional[bool] = ..., currency_platforms: _Optional[_Iterable[int]] = ..., version: _Optional[int] = ..., client_version_string: _Optional[str] = ..., tag: _Optional[str] = ...) -> None: ...

class ReqOauth2Signup(_message.Message):
    __slots__ = ()
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

class ReqOpenAllRewardItem(_message.Message):
    __slots__ = ()
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    item_id: int
    def __init__(self, item_id: _Optional[int] = ...) -> None: ...

class ReqOpenChest(_message.Message):
    __slots__ = ()
    CHEST_ID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    USE_TICKET_FIELD_NUMBER: _ClassVar[int]
    CHOOSE_UP_ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    chest_id: int
    count: int
    use_ticket: bool
    choose_up_activity_id: int
    def __init__(self, chest_id: _Optional[int] = ..., count: _Optional[int] = ..., use_ticket: _Optional[bool] = ..., choose_up_activity_id: _Optional[int] = ...) -> None: ...

class ReqOpenGacha(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    count: int
    def __init__(self, activity_id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class ReqOpenManualItem(_message.Message):
    __slots__ = ()
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    SELECT_ID_FIELD_NUMBER: _ClassVar[int]
    item_id: int
    count: int
    select_id: int
    def __init__(self, item_id: _Optional[int] = ..., count: _Optional[int] = ..., select_id: _Optional[int] = ...) -> None: ...

class ReqOpenPreChestItem(_message.Message):
    __slots__ = ()
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    item_id: int
    pool_id: int
    def __init__(self, item_id: _Optional[int] = ..., pool_id: _Optional[int] = ...) -> None: ...

class ReqOpenRandomRewardItem(_message.Message):
    __slots__ = ()
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    item_id: int
    count: int
    def __init__(self, item_id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class ReqOpenidCheck(_message.Message):
    __slots__ = ()
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    type: int
    token: str
    def __init__(self, type: _Optional[int] = ..., token: _Optional[str] = ...) -> None: ...

class ReqPayMonthTicket(_message.Message):
    __slots__ = ()
    TICKET_ID_FIELD_NUMBER: _ClassVar[int]
    ticket_id: int
    def __init__(self, ticket_id: _Optional[int] = ...) -> None: ...

class ReqPlatformBillingProducts(_message.Message):
    __slots__ = ()
    SHELVES_ID_FIELD_NUMBER: _ClassVar[int]
    shelves_id: int
    def __init__(self, shelves_id: _Optional[int] = ...) -> None: ...

class ReqPrepareLogin(_message.Message):
    __slots__ = ()
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    access_token: str
    type: int
    def __init__(self, access_token: _Optional[str] = ..., type: _Optional[int] = ...) -> None: ...

class ReqProgressRewardActivityReceive(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    PROGRESSES_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    progresses: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, activity_id: _Optional[int] = ..., progresses: _Optional[_Iterable[int]] = ...) -> None: ...

class ReqQuestCrewActivityFeed(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    MEMBER_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    member_id: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, activity_id: _Optional[int] = ..., member_id: _Optional[_Iterable[int]] = ...) -> None: ...

class ReqQuestCrewActivityHire(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    MEMBER_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    member_id: int
    def __init__(self, activity_id: _Optional[int] = ..., member_id: _Optional[int] = ...) -> None: ...

class ReqQuestCrewActivityRefreshMarket(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ReqQuestCrewActivityStartQuest(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    JOINED_MEMBERS_FIELD_NUMBER: _ClassVar[int]
    QUEST_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    joined_members: _containers.RepeatedScalarFieldContainer[int]
    quest_id: int
    def __init__(self, activity_id: _Optional[int] = ..., joined_members: _Optional[_Iterable[int]] = ..., quest_id: _Optional[int] = ...) -> None: ...

class ReqRandomCharacter(_message.Message):
    __slots__ = ()
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    POOL_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    pool: _containers.RepeatedCompositeFieldContainer[RandomCharacter]
    def __init__(self, enabled: _Optional[bool] = ..., pool: _Optional[_Iterable[_Union[RandomCharacter, _Mapping]]] = ...) -> None: ...

class ReqReadAnnouncement(_message.Message):
    __slots__ = ()
    ANNOUNCEMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ANNOUNCEMENT_LIST_FIELD_NUMBER: _ClassVar[int]
    announcement_id: int
    announcement_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, announcement_id: _Optional[int] = ..., announcement_list: _Optional[_Iterable[int]] = ...) -> None: ...

class ReqReadMail(_message.Message):
    __slots__ = ()
    MAIL_ID_FIELD_NUMBER: _ClassVar[int]
    mail_id: int
    def __init__(self, mail_id: _Optional[int] = ...) -> None: ...

class ReqReadSNS(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class ReqReceiveAchievementGroupReward(_message.Message):
    __slots__ = ()
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    group_id: int
    def __init__(self, group_id: _Optional[int] = ...) -> None: ...

class ReqReceiveAchievementReward(_message.Message):
    __slots__ = ()
    ACHIEVEMENT_ID_FIELD_NUMBER: _ClassVar[int]
    achievement_id: int
    def __init__(self, achievement_id: _Optional[int] = ...) -> None: ...

class ReqReceiveActivityFlipTask(_message.Message):
    __slots__ = ()
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    task_id: int
    def __init__(self, task_id: _Optional[int] = ...) -> None: ...

class ReqReceiveActivityGift(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    id: int
    def __init__(self, activity_id: _Optional[int] = ..., id: _Optional[int] = ...) -> None: ...

class ReqReceiveActivitySpotReward(_message.Message):
    __slots__ = ()
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    unique_id: int
    def __init__(self, unique_id: _Optional[int] = ...) -> None: ...

class ReqReceiveAllActivityGift(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ReqReceiveChallengeRankReward(_message.Message):
    __slots__ = ()
    SEASON_ID_FIELD_NUMBER: _ClassVar[int]
    season_id: int
    def __init__(self, season_id: _Optional[int] = ...) -> None: ...

class ReqReceiveCharacterRewards(_message.Message):
    __slots__ = ()
    CHARACTER_ID_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    character_id: int
    level: int
    def __init__(self, character_id: _Optional[int] = ..., level: _Optional[int] = ...) -> None: ...

class ReqReceiveRPGReward(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    MONSTER_SEQ_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    monster_seq: int
    def __init__(self, activity_id: _Optional[int] = ..., monster_seq: _Optional[int] = ...) -> None: ...

class ReqReceiveRPGRewards(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ReqReceiveUpgradeActivityReward(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ReqReceiveVillageBuildingReward(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    BUILDING_ID_FIELD_NUMBER: _ClassVar[int]
    REWARDS_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    building_id: int
    rewards: _containers.RepeatedCompositeFieldContainer[RewardSlot]
    def __init__(self, activity_id: _Optional[int] = ..., building_id: _Optional[int] = ..., rewards: _Optional[_Iterable[_Union[RewardSlot, _Mapping]]] = ...) -> None: ...

class ReqReceiveVillageTripReward(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    DEST_ID_FIELD_NUMBER: _ClassVar[int]
    REWARDS_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    dest_id: int
    rewards: _containers.RepeatedCompositeFieldContainer[RewardSlot]
    def __init__(self, activity_id: _Optional[int] = ..., dest_id: _Optional[int] = ..., rewards: _Optional[_Iterable[_Union[RewardSlot, _Mapping]]] = ...) -> None: ...

class ReqRecoverCombiningRecycle(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ReqRefreshDailyTask(_message.Message):
    __slots__ = ()
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    task_id: int
    def __init__(self, task_id: _Optional[int] = ...) -> None: ...

class ReqRefreshGameObserveAuth(_message.Message):
    __slots__ = ()
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: str
    def __init__(self, token: _Optional[str] = ...) -> None: ...

class ReqRemarkFriend(_message.Message):
    __slots__ = ()
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    REMARK_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    remark: str
    def __init__(self, account_id: _Optional[int] = ..., remark: _Optional[str] = ...) -> None: ...

class ReqRemoveCollectedGameRecord(_message.Message):
    __slots__ = ()
    UUID_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    def __init__(self, uuid: _Optional[str] = ...) -> None: ...

class ReqRemoveFriend(_message.Message):
    __slots__ = ()
    TARGET_ID_FIELD_NUMBER: _ClassVar[int]
    target_id: int
    def __init__(self, target_id: _Optional[int] = ...) -> None: ...

class ReqReplySNS(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class ReqRequestConnection(_message.Message):
    __slots__ = ()
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ROUTE_ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    type: int
    route_id: str
    timestamp: int
    def __init__(self, type: _Optional[int] = ..., route_id: _Optional[str] = ..., timestamp: _Optional[int] = ...) -> None: ...

class ReqRequestRouteChange(_message.Message):
    __slots__ = ()
    BEFORE_FIELD_NUMBER: _ClassVar[int]
    ROUTE_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    before: str
    route_id: str
    type: int
    def __init__(self, before: _Optional[str] = ..., route_id: _Optional[str] = ..., type: _Optional[int] = ...) -> None: ...

class ReqReshZHPShop(_message.Message):
    __slots__ = ()
    FREE_REFRESH_FIELD_NUMBER: _ClassVar[int]
    COST_REFRESH_FIELD_NUMBER: _ClassVar[int]
    free_refresh: int
    cost_refresh: int
    def __init__(self, free_refresh: _Optional[int] = ..., cost_refresh: _Optional[int] = ...) -> None: ...

class ReqResolveFestivalActivityEvent(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    SELECT_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    id: int
    select: int
    def __init__(self, activity_id: _Optional[int] = ..., id: _Optional[int] = ..., select: _Optional[int] = ...) -> None: ...

class ReqResolveFestivalActivityProposal(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    SELECT_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    id: int
    select: int
    def __init__(self, activity_id: _Optional[int] = ..., id: _Optional[int] = ..., select: _Optional[int] = ...) -> None: ...

class ReqRichmanChestInfo(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ReqRichmanNextMove(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ReqRichmanSpecialMove(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    STEP_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    step: int
    def __init__(self, activity_id: _Optional[int] = ..., step: _Optional[int] = ...) -> None: ...

class ReqRoomDressing(_message.Message):
    __slots__ = ()
    DRESSING_FIELD_NUMBER: _ClassVar[int]
    dressing: bool
    def __init__(self, dressing: _Optional[bool] = ...) -> None: ...

class ReqRoomKickPlayer(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class ReqRoomReady(_message.Message):
    __slots__ = ()
    READY_FIELD_NUMBER: _ClassVar[int]
    ready: bool
    def __init__(self, ready: _Optional[bool] = ...) -> None: ...

class ReqRoomStart(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ReqSaveCommonViews(_message.Message):
    __slots__ = ()
    VIEWS_FIELD_NUMBER: _ClassVar[int]
    SAVE_INDEX_FIELD_NUMBER: _ClassVar[int]
    IS_USE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    views: _containers.RepeatedCompositeFieldContainer[ViewSlot]
    save_index: int
    is_use: int
    name: str
    def __init__(self, views: _Optional[_Iterable[_Union[ViewSlot, _Mapping]]] = ..., save_index: _Optional[int] = ..., is_use: _Optional[int] = ..., name: _Optional[str] = ...) -> None: ...

class ReqSayChatMessage(_message.Message):
    __slots__ = ()
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    content: str
    unique_id: int
    def __init__(self, content: _Optional[str] = ..., unique_id: _Optional[int] = ...) -> None: ...

class ReqSearchAccountByEidLobby(_message.Message):
    __slots__ = ()
    EID_FIELD_NUMBER: _ClassVar[int]
    eid: int
    def __init__(self, eid: _Optional[int] = ...) -> None: ...

class ReqSearchAccountById(_message.Message):
    __slots__ = ()
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    def __init__(self, account_id: _Optional[int] = ...) -> None: ...

class ReqSearchAccountByPattern(_message.Message):
    __slots__ = ()
    SEARCH_NEXT_FIELD_NUMBER: _ClassVar[int]
    PATTERN_FIELD_NUMBER: _ClassVar[int]
    search_next: bool
    pattern: str
    def __init__(self, search_next: _Optional[bool] = ..., pattern: _Optional[str] = ...) -> None: ...

class ReqSelectChestChooseUp(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    SELECTION_FIELD_NUMBER: _ClassVar[int]
    CHEST_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    selection: int
    chest_id: int
    def __init__(self, activity_id: _Optional[int] = ..., selection: _Optional[int] = ..., chest_id: _Optional[int] = ...) -> None: ...

class ReqSelfOperation(_message.Message):
    __slots__ = ()
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
    def __init__(self, type: _Optional[int] = ..., index: _Optional[int] = ..., tile: _Optional[str] = ..., cancel_operation: _Optional[bool] = ..., moqie: _Optional[bool] = ..., timeuse: _Optional[int] = ..., tile_state: _Optional[int] = ..., change_tiles: _Optional[_Iterable[str]] = ..., tile_states: _Optional[_Iterable[int]] = ..., gap_type: _Optional[int] = ...) -> None: ...

class ReqSellItem(_message.Message):
    __slots__ = ()
    class Item(_message.Message):
        __slots__ = ()
        ITEM_ID_FIELD_NUMBER: _ClassVar[int]
        COUNT_FIELD_NUMBER: _ClassVar[int]
        item_id: int
        count: int
        def __init__(self, item_id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...
    SELLS_FIELD_NUMBER: _ClassVar[int]
    sells: _containers.RepeatedCompositeFieldContainer[ReqSellItem.Item]
    def __init__(self, sells: _Optional[_Iterable[_Union[ReqSellItem.Item, _Mapping]]] = ...) -> None: ...

class ReqSendActivityGiftToFriend(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    item_id: int
    target_id: int
    def __init__(self, activity_id: _Optional[int] = ..., item_id: _Optional[int] = ..., target_id: _Optional[int] = ...) -> None: ...

class ReqSendClientMessage(_message.Message):
    __slots__ = ()
    TARGET_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    target_id: int
    type: int
    content: str
    def __init__(self, target_id: _Optional[int] = ..., type: _Optional[int] = ..., content: _Optional[str] = ...) -> None: ...

class ReqSendGiftToCharacter(_message.Message):
    __slots__ = ()
    class Gift(_message.Message):
        __slots__ = ()
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

class ReqSetAccountFavoriteHu(_message.Message):
    __slots__ = ()
    MODE_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    CHANG_FIELD_NUMBER: _ClassVar[int]
    JU_FIELD_NUMBER: _ClassVar[int]
    BEN_FIELD_NUMBER: _ClassVar[int]
    mode: int
    category: int
    type: int
    uuid: str
    chang: int
    ju: int
    ben: int
    def __init__(self, mode: _Optional[int] = ..., category: _Optional[int] = ..., type: _Optional[int] = ..., uuid: _Optional[str] = ..., chang: _Optional[int] = ..., ju: _Optional[int] = ..., ben: _Optional[int] = ...) -> None: ...

class ReqSetFriendRoomRandomBotChar(_message.Message):
    __slots__ = ()
    DISABLE_RANDOM_CHAR_FIELD_NUMBER: _ClassVar[int]
    disable_random_char: int
    def __init__(self, disable_random_char: _Optional[int] = ...) -> None: ...

class ReqSetHiddenCharacter(_message.Message):
    __slots__ = ()
    CHARA_LIST_FIELD_NUMBER: _ClassVar[int]
    chara_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, chara_list: _Optional[_Iterable[int]] = ...) -> None: ...

class ReqSetLoadingImage(_message.Message):
    __slots__ = ()
    IMAGES_FIELD_NUMBER: _ClassVar[int]
    images: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, images: _Optional[_Iterable[int]] = ...) -> None: ...

class ReqSetVerifiedHidden(_message.Message):
    __slots__ = ()
    VERIFIED_HIDDEN_FIELD_NUMBER: _ClassVar[int]
    verified_hidden: int
    def __init__(self, verified_hidden: _Optional[int] = ...) -> None: ...

class ReqSetVillageWorker(_message.Message):
    __slots__ = ()
    BUILDING_ID_FIELD_NUMBER: _ClassVar[int]
    WORKER_POS_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    building_id: int
    worker_pos: int
    activity_id: int
    def __init__(self, building_id: _Optional[int] = ..., worker_pos: _Optional[int] = ..., activity_id: _Optional[int] = ...) -> None: ...

class ReqShootActivityAttackEnemies(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    BULLETS_COUNT_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    bullets_count: int
    position: int
    def __init__(self, activity_id: _Optional[int] = ..., bullets_count: _Optional[int] = ..., position: _Optional[int] = ...) -> None: ...

class ReqShopPurchase(_message.Message):
    __slots__ = ()
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    type: str
    id: int
    def __init__(self, type: _Optional[str] = ..., id: _Optional[int] = ...) -> None: ...

class ReqSignupAccount(_message.Message):
    __slots__ = ()
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

class ReqSignupCustomizedContest(_message.Message):
    __slots__ = ()
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    unique_id: int
    client_version_string: str
    def __init__(self, unique_id: _Optional[int] = ..., client_version_string: _Optional[str] = ...) -> None: ...

class ReqSimV2ActivityEndMatch(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ReqSimV2ActivityFetchInfo(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ReqSimV2ActivityGiveUp(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ReqSimV2ActivitySelectEvent(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    SELECTION_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    selection_id: int
    def __init__(self, activity_id: _Optional[int] = ..., selection_id: _Optional[int] = ...) -> None: ...

class ReqSimV2ActivitySetUpgrade(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    UPGRADE_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    upgrade: SimulationV2Ability
    def __init__(self, activity_id: _Optional[int] = ..., upgrade: _Optional[_Union[SimulationV2Ability, _Mapping]] = ...) -> None: ...

class ReqSimV2ActivityStartMatch(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ReqSimV2ActivityStartSeason(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ReqSimV2ActivityTrain(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    ABILITY_FIELD_NUMBER: _ClassVar[int]
    SKIP_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    ability: int
    skip: int
    def __init__(self, activity_id: _Optional[int] = ..., ability: _Optional[int] = ..., skip: _Optional[int] = ...) -> None: ...

class ReqSimulationActivityTrain(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    type: int
    def __init__(self, activity_id: _Optional[int] = ..., type: _Optional[int] = ...) -> None: ...

class ReqSolveGooglePlayOrder(_message.Message):
    __slots__ = ()
    INAPP_PURCHASE_DATA_FIELD_NUMBER: _ClassVar[int]
    INAPP_DATA_SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    inapp_purchase_data: str
    inapp_data_signature: str
    def __init__(self, inapp_purchase_data: _Optional[str] = ..., inapp_data_signature: _Optional[str] = ...) -> None: ...

class ReqSolveGooglePlayOrderV3(_message.Message):
    __slots__ = ()
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    TRANSACTION_ID_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    transaction_id: str
    token: str
    account_id: int
    def __init__(self, order_id: _Optional[str] = ..., transaction_id: _Optional[str] = ..., token: _Optional[str] = ..., account_id: _Optional[int] = ...) -> None: ...

class ReqStartCustomizedContest(_message.Message):
    __slots__ = ()
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    unique_id: int
    client_version_string: str
    def __init__(self, unique_id: _Optional[int] = ..., client_version_string: _Optional[str] = ...) -> None: ...

class ReqStartSimulationActivityGame(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    def __init__(self, activity_id: _Optional[int] = ...) -> None: ...

class ReqStartUnifiedMatch(_message.Message):
    __slots__ = ()
    MATCH_SID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    match_sid: str
    client_version_string: str
    def __init__(self, match_sid: _Optional[str] = ..., client_version_string: _Optional[str] = ...) -> None: ...

class ReqStartVillageTrip(_message.Message):
    __slots__ = ()
    DEST_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    dest: int
    activity_id: int
    def __init__(self, dest: _Optional[int] = ..., activity_id: _Optional[int] = ...) -> None: ...

class ReqStopCustomizedContest(_message.Message):
    __slots__ = ()
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    unique_id: int
    def __init__(self, unique_id: _Optional[int] = ...) -> None: ...

class ReqStoryActivityReceiveAllFinishReward(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    STORY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    story_id: int
    def __init__(self, activity_id: _Optional[int] = ..., story_id: _Optional[int] = ...) -> None: ...

class ReqStoryActivityReceiveEndingReward(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    STORY_ID_FIELD_NUMBER: _ClassVar[int]
    ENDING_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    story_id: int
    ending_id: int
    def __init__(self, activity_id: _Optional[int] = ..., story_id: _Optional[int] = ..., ending_id: _Optional[int] = ...) -> None: ...

class ReqStoryActivityReceiveFinishReward(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    STORY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    story_id: int
    def __init__(self, activity_id: _Optional[int] = ..., story_id: _Optional[int] = ...) -> None: ...

class ReqStoryActivityUnlock(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    STORY_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    story_id: int
    def __init__(self, activity_id: _Optional[int] = ..., story_id: _Optional[int] = ...) -> None: ...

class ReqStoryActivityUnlockEnding(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    STORY_ID_FIELD_NUMBER: _ClassVar[int]
    ENDING_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    story_id: int
    ending_id: int
    def __init__(self, activity_id: _Optional[int] = ..., story_id: _Optional[int] = ..., ending_id: _Optional[int] = ...) -> None: ...

class ReqStoryActivityUnlockEndingAndReceive(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    STORY_ID_FIELD_NUMBER: _ClassVar[int]
    ENDING_ID_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    story_id: int
    ending_id: int
    def __init__(self, activity_id: _Optional[int] = ..., story_id: _Optional[int] = ..., ending_id: _Optional[int] = ...) -> None: ...

class ReqSubmitQuestionnaire(_message.Message):
    __slots__ = ()
    class QuestionnaireAnswer(_message.Message):
        __slots__ = ()
        class QuestionnaireAnswerValue(_message.Message):
            __slots__ = ()
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

class ReqSyncGame(_message.Message):
    __slots__ = ()
    ROUND_ID_FIELD_NUMBER: _ClassVar[int]
    STEP_FIELD_NUMBER: _ClassVar[int]
    round_id: str
    step: int
    def __init__(self, round_id: _Optional[str] = ..., step: _Optional[int] = ...) -> None: ...

class ReqTakeAttachment(_message.Message):
    __slots__ = ()
    MAIL_ID_FIELD_NUMBER: _ClassVar[int]
    mail_id: int
    def __init__(self, mail_id: _Optional[int] = ...) -> None: ...

class ReqTargetCustomizedContest(_message.Message):
    __slots__ = ()
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    unique_id: int
    def __init__(self, unique_id: _Optional[int] = ...) -> None: ...

class ReqTaskRequest(_message.Message):
    __slots__ = ()
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    params: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, params: _Optional[_Iterable[int]] = ...) -> None: ...

class ReqUnbindPhoneNumber(_message.Message):
    __slots__ = ()
    CODE_FIELD_NUMBER: _ClassVar[int]
    PHONE_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    code: str
    phone: str
    password: str
    def __init__(self, code: _Optional[str] = ..., phone: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class ReqUnlockActivitySpot(_message.Message):
    __slots__ = ()
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    unique_id: int
    def __init__(self, unique_id: _Optional[int] = ...) -> None: ...

class ReqUnlockActivitySpotEnding(_message.Message):
    __slots__ = ()
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    ENDING_ID_FIELD_NUMBER: _ClassVar[int]
    unique_id: int
    ending_id: int
    def __init__(self, unique_id: _Optional[int] = ..., ending_id: _Optional[int] = ...) -> None: ...

class ReqUpdateAccountSettings(_message.Message):
    __slots__ = ()
    SETTING_FIELD_NUMBER: _ClassVar[int]
    setting: AccountSetting
    def __init__(self, setting: _Optional[_Union[AccountSetting, _Mapping]] = ...) -> None: ...

class ReqUpdateCharacterSort(_message.Message):
    __slots__ = ()
    SORT_FIELD_NUMBER: _ClassVar[int]
    OTHER_SORT_FIELD_NUMBER: _ClassVar[int]
    HIDDEN_CHARACTERS_FIELD_NUMBER: _ClassVar[int]
    sort: _containers.RepeatedScalarFieldContainer[int]
    other_sort: _containers.RepeatedScalarFieldContainer[int]
    hidden_characters: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, sort: _Optional[_Iterable[int]] = ..., other_sort: _Optional[_Iterable[int]] = ..., hidden_characters: _Optional[_Iterable[int]] = ...) -> None: ...

class ReqUpdateClientValue(_message.Message):
    __slots__ = ()
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: int
    value: int
    def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...

class ReqUpdateCommentSetting(_message.Message):
    __slots__ = ()
    COMMENT_ALLOW_FIELD_NUMBER: _ClassVar[int]
    comment_allow: int
    def __init__(self, comment_allow: _Optional[int] = ...) -> None: ...

class ReqUpdateIDCardInfo(_message.Message):
    __slots__ = ()
    FULLNAME_FIELD_NUMBER: _ClassVar[int]
    CARD_NO_FIELD_NUMBER: _ClassVar[int]
    fullname: str
    card_no: str
    def __init__(self, fullname: _Optional[str] = ..., card_no: _Optional[str] = ...) -> None: ...

class ReqUpdateManagerCustomizedContest(_message.Message):
    __slots__ = ()
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

class ReqUpdateReadComment(_message.Message):
    __slots__ = ()
    READ_ID_FIELD_NUMBER: _ClassVar[int]
    read_id: int
    def __init__(self, read_id: _Optional[int] = ...) -> None: ...

class ReqUpgradeActivityBuff(_message.Message):
    __slots__ = ()
    BUFF_ID_FIELD_NUMBER: _ClassVar[int]
    buff_id: int
    def __init__(self, buff_id: _Optional[int] = ...) -> None: ...

class ReqUpgradeActivityLevel(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    group: int
    count: int
    def __init__(self, activity_id: _Optional[int] = ..., group: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class ReqUpgradeCharacter(_message.Message):
    __slots__ = ()
    CHARACTER_ID_FIELD_NUMBER: _ClassVar[int]
    character_id: int
    def __init__(self, character_id: _Optional[int] = ...) -> None: ...

class ReqUpgradeVillageBuilding(_message.Message):
    __slots__ = ()
    BUILDING_ID_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    building_id: int
    activity_id: int
    def __init__(self, building_id: _Optional[int] = ..., activity_id: _Optional[int] = ...) -> None: ...

class ReqUseBagItem(_message.Message):
    __slots__ = ()
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    item_id: int
    def __init__(self, item_id: _Optional[int] = ...) -> None: ...

class ReqUseCommonView(_message.Message):
    __slots__ = ()
    INDEX_FIELD_NUMBER: _ClassVar[int]
    index: int
    def __init__(self, index: _Optional[int] = ...) -> None: ...

class ReqUseGiftCode(_message.Message):
    __slots__ = ()
    CODE_FIELD_NUMBER: _ClassVar[int]
    code: str
    def __init__(self, code: _Optional[str] = ...) -> None: ...

class ReqUseTitle(_message.Message):
    __slots__ = ()
    TITLE_FIELD_NUMBER: _ClassVar[int]
    title: int
    def __init__(self, title: _Optional[int] = ...) -> None: ...

class ReqUserComplain(_message.Message):
    __slots__ = ()
    class GameRoundInfo(_message.Message):
        __slots__ = ()
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

class ReqVerificationIAPOrder(_message.Message):
    __slots__ = ()
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    TRANSACTION_ID_FIELD_NUMBER: _ClassVar[int]
    RECEIPT_DATA_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    transaction_id: str
    receipt_data: str
    account_id: int
    def __init__(self, order_id: _Optional[str] = ..., transaction_id: _Optional[str] = ..., receipt_data: _Optional[str] = ..., account_id: _Optional[int] = ...) -> None: ...

class ReqVerifyCodeForSecure(_message.Message):
    __slots__ = ()
    CODE_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    code: str
    operation: int
    def __init__(self, code: _Optional[str] = ..., operation: _Optional[int] = ...) -> None: ...

class ReqVerifyMyCardOrder(_message.Message):
    __slots__ = ()
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    account_id: int
    def __init__(self, order_id: _Optional[str] = ..., account_id: _Optional[int] = ...) -> None: ...

class ReqVerifySteamOrder(_message.Message):
    __slots__ = ()
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    account_id: int
    def __init__(self, order_id: _Optional[str] = ..., account_id: _Optional[int] = ...) -> None: ...

class ReqVoteActivity(_message.Message):
    __slots__ = ()
    VOTE_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    vote: int
    activity_id: int
    count: int
    def __init__(self, vote: _Optional[int] = ..., activity_id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class ReqVoteGameEnd(_message.Message):
    __slots__ = ()
    YES_FIELD_NUMBER: _ClassVar[int]
    yes: bool
    def __init__(self, yes: _Optional[bool] = ...) -> None: ...

class ResAccountActivityData(_message.Message):
    __slots__ = ()
    class ActivitySignInData(_message.Message):
        __slots__ = ()
        ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
        SIGN_IN_COUNT_FIELD_NUMBER: _ClassVar[int]
        LAST_SIGN_IN_TIME_FIELD_NUMBER: _ClassVar[int]
        activity_id: int
        sign_in_count: int
        last_sign_in_time: int
        def __init__(self, activity_id: _Optional[int] = ..., sign_in_count: _Optional[int] = ..., last_sign_in_time: _Optional[int] = ...) -> None: ...
    class BuffData(_message.Message):
        __slots__ = ()
        TYPE_FIELD_NUMBER: _ClassVar[int]
        REMAIN_FIELD_NUMBER: _ClassVar[int]
        EFFECT_FIELD_NUMBER: _ClassVar[int]
        type: int
        remain: int
        effect: int
        def __init__(self, type: _Optional[int] = ..., remain: _Optional[int] = ..., effect: _Optional[int] = ...) -> None: ...
    class ActivityRichmanData(_message.Message):
        __slots__ = ()
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
        __slots__ = ()
        ID_FIELD_NUMBER: _ClassVar[int]
        COUNT_FIELD_NUMBER: _ClassVar[int]
        id: int
        count: int
        def __init__(self, id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...
    class ActivitySNSData(_message.Message):
        __slots__ = ()
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
    STORY_DATA_FIELD_NUMBER: _ClassVar[int]
    CHOOSE_UP_DATA_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_REWARD_DATA_FIELD_NUMBER: _ClassVar[int]
    QUEST_CREW_DATA_FIELD_NUMBER: _ClassVar[int]
    SHOOT_DATA_FIELD_NUMBER: _ClassVar[int]
    BINGO_DATA_FIELD_NUMBER: _ClassVar[int]
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
    story_data: _containers.RepeatedCompositeFieldContainer[ActivityStoryData]
    choose_up_data: _containers.RepeatedCompositeFieldContainer[ActivityChooseUpData]
    progress_reward_data: _containers.RepeatedCompositeFieldContainer[ActivityProgressRewardData]
    quest_crew_data: _containers.RepeatedCompositeFieldContainer[ActivityQuestCrewData]
    shoot_data: _containers.RepeatedCompositeFieldContainer[ActivityShootData]
    bingo_data: _containers.RepeatedCompositeFieldContainer[ActivityBingoData]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., exchange_records: _Optional[_Iterable[_Union[ExchangeRecord, _Mapping]]] = ..., task_progress_list: _Optional[_Iterable[_Union[TaskProgress, _Mapping]]] = ..., accumulated_point_list: _Optional[_Iterable[_Union[ActivityAccumulatedPointData, _Mapping]]] = ..., rank_data_list: _Optional[_Iterable[_Union[ActivityRankPointData, _Mapping]]] = ..., flip_task_progress_list: _Optional[_Iterable[_Union[TaskProgress, _Mapping]]] = ..., sign_in_data: _Optional[_Iterable[_Union[ResAccountActivityData.ActivitySignInData, _Mapping]]] = ..., richman_data: _Optional[_Iterable[_Union[ResAccountActivityData.ActivityRichmanData, _Mapping]]] = ..., period_task_progress_list: _Optional[_Iterable[_Union[TaskProgress, _Mapping]]] = ..., random_task_progress_list: _Optional[_Iterable[_Union[TaskProgress, _Mapping]]] = ..., chest_up_data: _Optional[_Iterable[_Union[ResAccountActivityData.ChestUpData, _Mapping]]] = ..., sns_data: _Optional[_Union[ResAccountActivityData.ActivitySNSData, _Mapping]] = ..., mine_data: _Optional[_Iterable[_Union[MineActivityData, _Mapping]]] = ..., rpg_data: _Optional[_Iterable[_Union[RPGActivity, _Mapping]]] = ..., arena_data: _Optional[_Iterable[_Union[ActivityArenaData, _Mapping]]] = ..., feed_data: _Optional[_Iterable[_Union[FeedActivityData, _Mapping]]] = ..., segment_task_progress_list: _Optional[_Iterable[_Union[SegmentTaskProgress, _Mapping]]] = ..., vote_records: _Optional[_Iterable[_Union[VoteData, _Mapping]]] = ..., spot_data: _Optional[_Iterable[_Union[ActivitySpotData, _Mapping]]] = ..., friend_gift_data: _Optional[_Iterable[_Union[ActivityFriendGiftData, _Mapping]]] = ..., upgrade_data: _Optional[_Iterable[_Union[ActivityUpgradeData, _Mapping]]] = ..., gacha_data: _Optional[_Iterable[_Union[ActivityGachaUpdateData, _Mapping]]] = ..., simulation_data: _Optional[_Iterable[_Union[ActivitySimulationData, _Mapping]]] = ..., combining_data: _Optional[_Iterable[_Union[ActivityCombiningLQData, _Mapping]]] = ..., village_data: _Optional[_Iterable[_Union[ActivityVillageData, _Mapping]]] = ..., festival_data: _Optional[_Iterable[_Union[ActivityFestivalData, _Mapping]]] = ..., island_data: _Optional[_Iterable[_Union[ActivityIslandData, _Mapping]]] = ..., story_data: _Optional[_Iterable[_Union[ActivityStoryData, _Mapping]]] = ..., choose_up_data: _Optional[_Iterable[_Union[ActivityChooseUpData, _Mapping]]] = ..., progress_reward_data: _Optional[_Iterable[_Union[ActivityProgressRewardData, _Mapping]]] = ..., quest_crew_data: _Optional[_Iterable[_Union[ActivityQuestCrewData, _Mapping]]] = ..., shoot_data: _Optional[_Iterable[_Union[ActivityShootData, _Mapping]]] = ..., bingo_data: _Optional[_Iterable[_Union[ActivityBingoData, _Mapping]]] = ...) -> None: ...

class ResAccountChallengeRankInfo(_message.Message):
    __slots__ = ()
    class ChallengeRank(_message.Message):
        __slots__ = ()
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
    __slots__ = ()
    UNLOCK_LIST_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    unlock_list: _containers.RepeatedScalarFieldContainer[int]
    error: Error
    def __init__(self, unlock_list: _Optional[_Iterable[int]] = ..., error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class ResAccountInfo(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    ROOM_FIELD_NUMBER: _ClassVar[int]
    error: Error
    account: Account
    room: Room
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., account: _Optional[_Union[Account, _Mapping]] = ..., room: _Optional[_Union[Room, _Mapping]] = ...) -> None: ...

class ResAccountSettings(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    settings: _containers.RepeatedCompositeFieldContainer[AccountSetting]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., settings: _Optional[_Iterable[_Union[AccountSetting, _Mapping]]] = ...) -> None: ...

class ResAccountStates(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    STATES_FIELD_NUMBER: _ClassVar[int]
    error: Error
    states: _containers.RepeatedCompositeFieldContainer[AccountActiveState]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., states: _Optional[_Iterable[_Union[AccountActiveState, _Mapping]]] = ...) -> None: ...

class ResAccountStatisticInfo(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    STATISTIC_DATA_FIELD_NUMBER: _ClassVar[int]
    DETAIL_DATA_FIELD_NUMBER: _ClassVar[int]
    error: Error
    statistic_data: _containers.RepeatedCompositeFieldContainer[AccountStatisticData]
    detail_data: AccountDetailStatisticV2
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., statistic_data: _Optional[_Iterable[_Union[AccountStatisticData, _Mapping]]] = ..., detail_data: _Optional[_Union[AccountDetailStatisticV2, _Mapping]] = ...) -> None: ...

class ResAccountUpdate(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    UPDATE_FIELD_NUMBER: _ClassVar[int]
    error: Error
    update: AccountUpdate
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., update: _Optional[_Union[AccountUpdate, _Mapping]] = ...) -> None: ...

class ResAchievement(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    PROGRESSES_FIELD_NUMBER: _ClassVar[int]
    REWARDED_GROUP_FIELD_NUMBER: _ClassVar[int]
    error: Error
    progresses: _containers.RepeatedCompositeFieldContainer[AchievementProgress]
    rewarded_group: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., progresses: _Optional[_Iterable[_Union[AchievementProgress, _Mapping]]] = ..., rewarded_group: _Optional[_Iterable[int]] = ...) -> None: ...

class ResActivityBuff(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    BUFF_LIST_FIELD_NUMBER: _ClassVar[int]
    error: Error
    buff_list: _containers.RepeatedCompositeFieldContainer[ActivityBuffData]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., buff_list: _Optional[_Iterable[_Union[ActivityBuffData, _Mapping]]] = ...) -> None: ...

class ResActivityList(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ACTIVITIES_FIELD_NUMBER: _ClassVar[int]
    error: Error
    activities: _containers.RepeatedCompositeFieldContainer[Activity]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., activities: _Optional[_Iterable[_Union[Activity, _Mapping]]] = ...) -> None: ...

class ResAddCollectedGameRecord(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    error: Error
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class ResAllcommonViews(_message.Message):
    __slots__ = ()
    class Views(_message.Message):
        __slots__ = ()
        VALUES_FIELD_NUMBER: _ClassVar[int]
        INDEX_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        values: _containers.RepeatedCompositeFieldContainer[ViewSlot]
        index: int
        name: str
        def __init__(self, values: _Optional[_Iterable[_Union[ViewSlot, _Mapping]]] = ..., index: _Optional[int] = ..., name: _Optional[str] = ...) -> None: ...
    VIEWS_FIELD_NUMBER: _ClassVar[int]
    USE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    views: _containers.RepeatedCompositeFieldContainer[ResAllcommonViews.Views]
    use: int
    error: Error
    def __init__(self, views: _Optional[_Iterable[_Union[ResAllcommonViews.Views, _Mapping]]] = ..., use: _Optional[int] = ..., error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class ResAmuletActivityFetchBrief(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    UPGRADE_FIELD_NUMBER: _ClassVar[int]
    ILLUSTRATED_BOOK_FIELD_NUMBER: _ClassVar[int]
    GAME_RECORDS_FIELD_NUMBER: _ClassVar[int]
    STATISTIC_FIELD_NUMBER: _ClassVar[int]
    error: Error
    upgrade: ActivityAmuletUpgradeData
    illustrated_book: ActivityAmuletIllustratedBookData
    game_records: _containers.RepeatedCompositeFieldContainer[ActivityAmuletGameRecordData]
    statistic: ActivityAmuletStatisticData
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., upgrade: _Optional[_Union[ActivityAmuletUpgradeData, _Mapping]] = ..., illustrated_book: _Optional[_Union[ActivityAmuletIllustratedBookData, _Mapping]] = ..., game_records: _Optional[_Iterable[_Union[ActivityAmuletGameRecordData, _Mapping]]] = ..., statistic: _Optional[_Union[ActivityAmuletStatisticData, _Mapping]] = ...) -> None: ...

class ResAmuletActivityFetchInfo(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    error: Error
    data: ActivityAmuletData
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., data: _Optional[_Union[ActivityAmuletData, _Mapping]] = ...) -> None: ...

class ResAmuletActivityMaintainInfo(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    error: Error
    mode: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., mode: _Optional[str] = ...) -> None: ...

class ResAmuletEventResponse(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    events: _containers.RepeatedCompositeFieldContainer[AmuletEventData]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., events: _Optional[_Iterable[_Union[AmuletEventData, _Mapping]]] = ...) -> None: ...

class ResAnnouncement(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ANNOUNCEMENTS_FIELD_NUMBER: _ClassVar[int]
    SORT_FIELD_NUMBER: _ClassVar[int]
    READ_LIST_FIELD_NUMBER: _ClassVar[int]
    error: Error
    announcements: _containers.RepeatedCompositeFieldContainer[Announcement]
    sort: _containers.RepeatedScalarFieldContainer[int]
    read_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., announcements: _Optional[_Iterable[_Union[Announcement, _Mapping]]] = ..., sort: _Optional[_Iterable[int]] = ..., read_list: _Optional[_Iterable[int]] = ...) -> None: ...

class ResArenaReward(_message.Message):
    __slots__ = ()
    class RewardItem(_message.Message):
        __slots__ = ()
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

class ResAuthGame(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    SEAT_LIST_FIELD_NUMBER: _ClassVar[int]
    IS_GAME_START_FIELD_NUMBER: _ClassVar[int]
    GAME_CONFIG_FIELD_NUMBER: _ClassVar[int]
    READY_ID_LIST_FIELD_NUMBER: _ClassVar[int]
    ROBOTS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    players: _containers.RepeatedCompositeFieldContainer[PlayerGameView]
    seat_list: _containers.RepeatedScalarFieldContainer[int]
    is_game_start: bool
    game_config: GameConfig
    ready_id_list: _containers.RepeatedScalarFieldContainer[int]
    robots: _containers.RepeatedCompositeFieldContainer[PlayerGameView]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., players: _Optional[_Iterable[_Union[PlayerGameView, _Mapping]]] = ..., seat_list: _Optional[_Iterable[int]] = ..., is_game_start: _Optional[bool] = ..., game_config: _Optional[_Union[GameConfig, _Mapping]] = ..., ready_id_list: _Optional[_Iterable[int]] = ..., robots: _Optional[_Iterable[_Union[PlayerGameView, _Mapping]]] = ...) -> None: ...

class ResBagInfo(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    BAG_FIELD_NUMBER: _ClassVar[int]
    error: Error
    bag: Bag
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., bag: _Optional[_Union[Bag, _Mapping]] = ...) -> None: ...

class ResBingoActivityReceiveReward(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    EXECUTE_RESULT_FIELD_NUMBER: _ClassVar[int]
    CARDS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    execute_result: _containers.RepeatedCompositeFieldContainer[ExecuteResult]
    cards: _containers.RepeatedCompositeFieldContainer[ActivityBingoCardData]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., execute_result: _Optional[_Iterable[_Union[ExecuteResult, _Mapping]]] = ..., cards: _Optional[_Iterable[_Union[ActivityBingoCardData, _Mapping]]] = ...) -> None: ...

class ResBuyFestivalProposal(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    NEW_PROPOSAL_FIELD_NUMBER: _ClassVar[int]
    error: Error
    new_proposal: FestivalProposalData
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., new_proposal: _Optional[_Union[FestivalProposalData, _Mapping]] = ...) -> None: ...

class ResBuyFromChestShop(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    CHEST_ID_FIELD_NUMBER: _ClassVar[int]
    CONSUME_COUNT_FIELD_NUMBER: _ClassVar[int]
    FAITH_COUNT_FIELD_NUMBER: _ClassVar[int]
    error: Error
    chest_id: int
    consume_count: int
    faith_count: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., chest_id: _Optional[int] = ..., consume_count: _Optional[int] = ..., faith_count: _Optional[int] = ...) -> None: ...

class ResBuyFromShop(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    REWARDS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    rewards: _containers.RepeatedCompositeFieldContainer[RewardSlot]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., rewards: _Optional[_Iterable[_Union[RewardSlot, _Mapping]]] = ...) -> None: ...

class ResChallengeLeaderboard(_message.Message):
    __slots__ = ()
    class Item(_message.Message):
        __slots__ = ()
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

class ResChallengeSeasonInfo(_message.Message):
    __slots__ = ()
    class ChallengeInfo(_message.Message):
        __slots__ = ()
        SEASON_ID_FIELD_NUMBER: _ClassVar[int]
        START_TIME_FIELD_NUMBER: _ClassVar[int]
        END_TIME_FIELD_NUMBER: _ClassVar[int]
        STATE_FIELD_NUMBER: _ClassVar[int]
        season_id: int
        start_time: int
        end_time: int
        state: int
        def __init__(self, season_id: _Optional[int] = ..., start_time: _Optional[int] = ..., end_time: _Optional[int] = ..., state: _Optional[int] = ...) -> None: ...
    CHALLENGE_SEASON_LIST_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    challenge_season_list: _containers.RepeatedCompositeFieldContainer[ResChallengeSeasonInfo.ChallengeInfo]
    error: Error
    def __init__(self, challenge_season_list: _Optional[_Iterable[_Union[ResChallengeSeasonInfo.ChallengeInfo, _Mapping]]] = ..., error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class ResChangeCollectedGameRecordRemarks(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    error: Error
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class ResCharacterInfo(_message.Message):
    __slots__ = ()
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
    OTHER_CHARACTER_SORT_FIELD_NUMBER: _ClassVar[int]
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
    other_character_sort: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., characters: _Optional[_Iterable[_Union[Character, _Mapping]]] = ..., skins: _Optional[_Iterable[int]] = ..., main_character_id: _Optional[int] = ..., send_gift_count: _Optional[int] = ..., send_gift_limit: _Optional[int] = ..., finished_endings: _Optional[_Iterable[int]] = ..., rewarded_endings: _Optional[_Iterable[int]] = ..., character_sort: _Optional[_Iterable[int]] = ..., hidden_characters: _Optional[_Iterable[int]] = ..., other_character_sort: _Optional[_Iterable[int]] = ...) -> None: ...

class ResClientValue(_message.Message):
    __slots__ = ()
    class Value(_message.Message):
        __slots__ = ()
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    DATAS_FIELD_NUMBER: _ClassVar[int]
    RECHARGED_COUNT_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    datas: _containers.RepeatedCompositeFieldContainer[ResClientValue.Value]
    recharged_count: int
    error: Error
    def __init__(self, datas: _Optional[_Iterable[_Union[ResClientValue.Value, _Mapping]]] = ..., recharged_count: _Optional[int] = ..., error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class ResCollectedGameRecordList(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    RECORD_LIST_FIELD_NUMBER: _ClassVar[int]
    RECORD_COLLECT_LIMIT_FIELD_NUMBER: _ClassVar[int]
    error: Error
    record_list: _containers.RepeatedCompositeFieldContainer[RecordCollectedData]
    record_collect_limit: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., record_list: _Optional[_Iterable[_Union[RecordCollectedData, _Mapping]]] = ..., record_collect_limit: _Optional[int] = ...) -> None: ...

class ResCombiningRecycleCraft(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    REWARD_ITEMS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    reward_items: _containers.RepeatedCompositeFieldContainer[ExecuteReward]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., reward_items: _Optional[_Iterable[_Union[ExecuteReward, _Mapping]]] = ...) -> None: ...

class ResCommentSetting(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    COMMENT_ALLOW_FIELD_NUMBER: _ClassVar[int]
    error: Error
    comment_allow: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., comment_allow: _Optional[int] = ...) -> None: ...

class ResCommon(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    error: Error
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class ResCommonView(_message.Message):
    __slots__ = ()
    class Slot(_message.Message):
        __slots__ = ()
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

class ResCommonViews(_message.Message):
    __slots__ = ()
    VIEWS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    views: _containers.RepeatedCompositeFieldContainer[ViewSlot]
    error: Error
    name: str
    def __init__(self, views: _Optional[_Iterable[_Union[ViewSlot, _Mapping]]] = ..., error: _Optional[_Union[Error, _Mapping]] = ..., name: _Optional[str] = ...) -> None: ...

class ResCompleteSegmentTaskReward(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    REWARDS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    rewards: _containers.RepeatedCompositeFieldContainer[ExecuteReward]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., rewards: _Optional[_Iterable[_Union[ExecuteReward, _Mapping]]] = ...) -> None: ...

class ResCompleteVillageTask(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    REWARD_ITEMS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    reward_items: _containers.RepeatedCompositeFieldContainer[ExecuteReward]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., reward_items: _Optional[_Iterable[_Union[ExecuteReward, _Mapping]]] = ...) -> None: ...

class ResConnectionInfo(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    error: Error
    client_endpoint: NetworkEndpoint
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., client_endpoint: _Optional[_Union[NetworkEndpoint, _Mapping]] = ...) -> None: ...

class ResCreateAlipayAppOrder(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ALIPAY_URL_FIELD_NUMBER: _ClassVar[int]
    error: Error
    alipay_url: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., alipay_url: _Optional[str] = ...) -> None: ...

class ResCreateAlipayOrder(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ALIPAY_URL_FIELD_NUMBER: _ClassVar[int]
    error: Error
    alipay_url: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., alipay_url: _Optional[str] = ...) -> None: ...

class ResCreateAlipayScanOrder(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    QRCODE_BUFFER_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    QR_CODE_FIELD_NUMBER: _ClassVar[int]
    error: Error
    qrcode_buffer: str
    order_id: str
    qr_code: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., qrcode_buffer: _Optional[str] = ..., order_id: _Optional[str] = ..., qr_code: _Optional[str] = ...) -> None: ...

class ResCreateBillingOrder(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    order_id: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., order_id: _Optional[str] = ...) -> None: ...

class ResCreateCustomizedContest(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    unique_id: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., unique_id: _Optional[int] = ...) -> None: ...

class ResCreateDmmOrder(_message.Message):
    __slots__ = ()
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

class ResCreateENAlipayOrder(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    order_id: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., order_id: _Optional[str] = ...) -> None: ...

class ResCreateENJCBOrder(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    order_id: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., order_id: _Optional[str] = ...) -> None: ...

class ResCreateENMasterCardOrder(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    order_id: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., order_id: _Optional[str] = ...) -> None: ...

class ResCreateENPaypalOrder(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    order_id: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., order_id: _Optional[str] = ...) -> None: ...

class ResCreateENVisaOrder(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    order_id: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., order_id: _Optional[str] = ...) -> None: ...

class ResCreateGameObserveAuth(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    error: Error
    token: str
    location: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., token: _Optional[str] = ..., location: _Optional[str] = ...) -> None: ...

class ResCreateIAPOrder(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    order_id: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., order_id: _Optional[str] = ...) -> None: ...

class ResCreateJPAuOrder(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    order_id: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., order_id: _Optional[str] = ...) -> None: ...

class ResCreateJPCreditCardOrder(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    order_id: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., order_id: _Optional[str] = ...) -> None: ...

class ResCreateJPDocomoOrder(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    order_id: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., order_id: _Optional[str] = ...) -> None: ...

class ResCreateJPGMOOrder(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    order_id: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., order_id: _Optional[str] = ...) -> None: ...

class ResCreateJPPayPayOrder(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    order_id: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., order_id: _Optional[str] = ...) -> None: ...

class ResCreateJPPaypalOrder(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    order_id: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., order_id: _Optional[str] = ...) -> None: ...

class ResCreateJPSoftbankOrder(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    order_id: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., order_id: _Optional[str] = ...) -> None: ...

class ResCreateJPWebMoneyOrder(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    order_id: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., order_id: _Optional[str] = ...) -> None: ...

class ResCreateKRAlipayOrder(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    order_id: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., order_id: _Optional[str] = ...) -> None: ...

class ResCreateKRJCBOrder(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    order_id: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., order_id: _Optional[str] = ...) -> None: ...

class ResCreateKRMasterCardOrder(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    order_id: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., order_id: _Optional[str] = ...) -> None: ...

class ResCreateKRPaypalOrder(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    order_id: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., order_id: _Optional[str] = ...) -> None: ...

class ResCreateKRVisaOrder(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    order_id: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., order_id: _Optional[str] = ...) -> None: ...

class ResCreateMyCardOrder(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    AUTH_CODE_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    auth_code: str
    order_id: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., auth_code: _Optional[str] = ..., order_id: _Optional[str] = ...) -> None: ...

class ResCreatePaypalOrder(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    error: Error
    order_id: str
    url: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., order_id: _Optional[str] = ..., url: _Optional[str] = ...) -> None: ...

class ResCreateRoom(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ROOM_FIELD_NUMBER: _ClassVar[int]
    error: Error
    room: Room
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., room: _Optional[_Union[Room, _Mapping]] = ...) -> None: ...

class ResCreateSeerReport(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    SEER_REPORT_FIELD_NUMBER: _ClassVar[int]
    error: Error
    seer_report: SeerBrief
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., seer_report: _Optional[_Union[SeerBrief, _Mapping]] = ...) -> None: ...

class ResCreateSteamOrder(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    order_id: str
    platform_order_id: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., order_id: _Optional[str] = ..., platform_order_id: _Optional[str] = ...) -> None: ...

class ResCreateWechatAppOrder(_message.Message):
    __slots__ = ()
    class CallWechatAppParam(_message.Message):
        __slots__ = ()
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

class ResCreateWechatNativeOrder(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    QRCODE_BUFFER_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    qrcode_buffer: str
    order_id: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., qrcode_buffer: _Optional[str] = ..., order_id: _Optional[str] = ...) -> None: ...

class ResCreateXsollaOrder(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    error: Error
    order_id: str
    url: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., order_id: _Optional[str] = ..., url: _Optional[str] = ...) -> None: ...

class ResCreateYostarOrder(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    order_id: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., order_id: _Optional[str] = ...) -> None: ...

class ResCurrentMatchInfo(_message.Message):
    __slots__ = ()
    class CurrentMatchInfo(_message.Message):
        __slots__ = ()
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

class ResDMMPreLogin(_message.Message):
    __slots__ = ()
    PARAMETER_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    parameter: str
    error: Error
    def __init__(self, parameter: _Optional[str] = ..., error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class ResDailySignInInfo(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    SIGN_IN_DAYS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    sign_in_days: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., sign_in_days: _Optional[int] = ...) -> None: ...

class ResDailyTask(_message.Message):
    __slots__ = ()
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
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., progresses: _Optional[_Iterable[_Union[TaskProgress, _Mapping]]] = ..., has_refresh_count: _Optional[bool] = ..., max_daily_task_count: _Optional[int] = ..., refresh_count: _Optional[int] = ...) -> None: ...

class ResDeleteAccount(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    DELETE_TIME_FIELD_NUMBER: _ClassVar[int]
    error: Error
    delete_time: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., delete_time: _Optional[int] = ...) -> None: ...

class ResDigMine(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    MAP_FIELD_NUMBER: _ClassVar[int]
    REWARD_FIELD_NUMBER: _ClassVar[int]
    error: Error
    map: _containers.RepeatedCompositeFieldContainer[MineReward]
    reward: _containers.RepeatedCompositeFieldContainer[RewardSlot]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., map: _Optional[_Iterable[_Union[MineReward, _Mapping]]] = ..., reward: _Optional[_Iterable[_Union[RewardSlot, _Mapping]]] = ...) -> None: ...

class ResDoActivitySignIn(_message.Message):
    __slots__ = ()
    class RewardData(_message.Message):
        __slots__ = ()
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

class ResEnterCustomizedContest(_message.Message):
    __slots__ = ()
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
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., detail_info: _Optional[_Union[CustomizedContestDetail, _Mapping]] = ..., player_report: _Optional[_Union[CustomizedContestPlayerReport, _Mapping]] = ..., is_followed: _Optional[bool] = ..., state: _Optional[int] = ..., is_admin: _Optional[bool] = ...) -> None: ...

class ResEnterGame(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    IS_END_FIELD_NUMBER: _ClassVar[int]
    STEP_FIELD_NUMBER: _ClassVar[int]
    GAME_RESTORE_FIELD_NUMBER: _ClassVar[int]
    error: Error
    is_end: bool
    step: int
    game_restore: GameRestore
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., is_end: _Optional[bool] = ..., step: _Optional[int] = ..., game_restore: _Optional[_Union[GameRestore, _Mapping]] = ...) -> None: ...

class ResExchangeActivityItem(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    EXECUTE_REWARD_FIELD_NUMBER: _ClassVar[int]
    error: Error
    execute_reward: _containers.RepeatedCompositeFieldContainer[ExecuteReward]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., execute_reward: _Optional[_Iterable[_Union[ExecuteReward, _Mapping]]] = ...) -> None: ...

class ResFastLogin(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    GAME_INFO_FIELD_NUMBER: _ClassVar[int]
    ROOM_FIELD_NUMBER: _ClassVar[int]
    error: Error
    game_info: GameConnectInfo
    room: Room
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., game_info: _Optional[_Union[GameConnectInfo, _Mapping]] = ..., room: _Optional[_Union[Room, _Mapping]] = ...) -> None: ...

class ResFeedActivityFeed(_message.Message):
    __slots__ = ()
    class RewardItem(_message.Message):
        __slots__ = ()
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

class ResFetchABMatch(_message.Message):
    __slots__ = ()
    class MatchPoint(_message.Message):
        __slots__ = ()
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
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., match_id: _Optional[int] = ..., match_count: _Optional[int] = ..., buy_in_count: _Optional[int] = ..., point: _Optional[int] = ..., rewarded: _Optional[bool] = ..., match_max_point: _Optional[_Iterable[_Union[ResFetchABMatch.MatchPoint, _Mapping]]] = ..., quit: _Optional[bool] = ...) -> None: ...

class ResFetchAccountGameHuRecords(_message.Message):
    __slots__ = ()
    class GameHuRecords(_message.Message):
        __slots__ = ()
        CHANG_FIELD_NUMBER: _ClassVar[int]
        JU_FIELD_NUMBER: _ClassVar[int]
        BEN_FIELD_NUMBER: _ClassVar[int]
        TITLE_ID_FIELD_NUMBER: _ClassVar[int]
        HANDS_FIELD_NUMBER: _ClassVar[int]
        MING_FIELD_NUMBER: _ClassVar[int]
        HUPAI_FIELD_NUMBER: _ClassVar[int]
        HU_FANS_FIELD_NUMBER: _ClassVar[int]
        chang: int
        ju: int
        ben: int
        title_id: int
        hands: _containers.RepeatedScalarFieldContainer[str]
        ming: _containers.RepeatedScalarFieldContainer[str]
        hupai: str
        hu_fans: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, chang: _Optional[int] = ..., ju: _Optional[int] = ..., ben: _Optional[int] = ..., title_id: _Optional[int] = ..., hands: _Optional[_Iterable[str]] = ..., ming: _Optional[_Iterable[str]] = ..., hupai: _Optional[str] = ..., hu_fans: _Optional[_Iterable[int]] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    RECORDS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    records: _containers.RepeatedCompositeFieldContainer[ResFetchAccountGameHuRecords.GameHuRecords]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., records: _Optional[_Iterable[_Union[ResFetchAccountGameHuRecords.GameHuRecords, _Mapping]]] = ...) -> None: ...

class ResFetchAccountInfoExtra(_message.Message):
    __slots__ = ()
    class AccountInfoGameRecord(_message.Message):
        __slots__ = ()
        class AccountGameResult(_message.Message):
            __slots__ = ()
            RANK_FIELD_NUMBER: _ClassVar[int]
            ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
            NICKNAME_FIELD_NUMBER: _ClassVar[int]
            VERIFIED_FIELD_NUMBER: _ClassVar[int]
            GRADING_SCORE_FIELD_NUMBER: _ClassVar[int]
            FINAL_POINT_FIELD_NUMBER: _ClassVar[int]
            SEAT_FIELD_NUMBER: _ClassVar[int]
            LEVEL_FIELD_NUMBER: _ClassVar[int]
            LEVEL3_FIELD_NUMBER: _ClassVar[int]
            rank: int
            account_id: int
            nickname: str
            verified: int
            grading_score: int
            final_point: int
            seat: int
            level: AccountLevel
            level3: AccountLevel
            def __init__(self, rank: _Optional[int] = ..., account_id: _Optional[int] = ..., nickname: _Optional[str] = ..., verified: _Optional[int] = ..., grading_score: _Optional[int] = ..., final_point: _Optional[int] = ..., seat: _Optional[int] = ..., level: _Optional[_Union[AccountLevel, _Mapping]] = ..., level3: _Optional[_Union[AccountLevel, _Mapping]] = ...) -> None: ...
        UUID_FIELD_NUMBER: _ClassVar[int]
        START_TIME_FIELD_NUMBER: _ClassVar[int]
        END_TIME_FIELD_NUMBER: _ClassVar[int]
        TAG_FIELD_NUMBER: _ClassVar[int]
        SUB_TAG_FIELD_NUMBER: _ClassVar[int]
        RANK_FIELD_NUMBER: _ClassVar[int]
        FINAL_POINT_FIELD_NUMBER: _ClassVar[int]
        RESULTS_FIELD_NUMBER: _ClassVar[int]
        uuid: str
        start_time: int
        end_time: int
        tag: int
        sub_tag: int
        rank: int
        final_point: int
        results: _containers.RepeatedCompositeFieldContainer[ResFetchAccountInfoExtra.AccountInfoGameRecord.AccountGameResult]
        def __init__(self, uuid: _Optional[str] = ..., start_time: _Optional[int] = ..., end_time: _Optional[int] = ..., tag: _Optional[int] = ..., sub_tag: _Optional[int] = ..., rank: _Optional[int] = ..., final_point: _Optional[int] = ..., results: _Optional[_Iterable[_Union[ResFetchAccountInfoExtra.AccountInfoGameRecord.AccountGameResult, _Mapping]]] = ...) -> None: ...
    class GameHuTypeDetail(_message.Message):
        __slots__ = ()
        TYPE_FIELD_NUMBER: _ClassVar[int]
        COUNT_FIELD_NUMBER: _ClassVar[int]
        type: int
        count: int
        def __init__(self, type: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...
    class AccountGameRankDetail(_message.Message):
        __slots__ = ()
        RANK_FIELD_NUMBER: _ClassVar[int]
        COUNT_FIELD_NUMBER: _ClassVar[int]
        rank: int
        count: int
        def __init__(self, rank: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    RECENT_GAMES_FIELD_NUMBER: _ClassVar[int]
    HU_TYPE_DETAILS_FIELD_NUMBER: _ClassVar[int]
    GAME_RANK_DETAILS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    recent_games: _containers.RepeatedCompositeFieldContainer[ResFetchAccountInfoExtra.AccountInfoGameRecord]
    hu_type_details: _containers.RepeatedCompositeFieldContainer[ResFetchAccountInfoExtra.GameHuTypeDetail]
    game_rank_details: _containers.RepeatedCompositeFieldContainer[ResFetchAccountInfoExtra.AccountGameRankDetail]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., recent_games: _Optional[_Iterable[_Union[ResFetchAccountInfoExtra.AccountInfoGameRecord, _Mapping]]] = ..., hu_type_details: _Optional[_Iterable[_Union[ResFetchAccountInfoExtra.GameHuTypeDetail, _Mapping]]] = ..., game_rank_details: _Optional[_Iterable[_Union[ResFetchAccountInfoExtra.AccountGameRankDetail, _Mapping]]] = ...) -> None: ...

class ResFetchAchievementRate(_message.Message):
    __slots__ = ()
    class AchievementRate(_message.Message):
        __slots__ = ()
        ID_FIELD_NUMBER: _ClassVar[int]
        RATE_FIELD_NUMBER: _ClassVar[int]
        id: int
        rate: int
        def __init__(self, id: _Optional[int] = ..., rate: _Optional[int] = ...) -> None: ...
    RATE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    rate: _containers.RepeatedCompositeFieldContainer[ResFetchAchievementRate.AchievementRate]
    error: Error
    def __init__(self, rate: _Optional[_Iterable[_Union[ResFetchAchievementRate.AchievementRate, _Mapping]]] = ..., error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class ResFetchActivityFlipInfo(_message.Message):
    __slots__ = ()
    REWARDS_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    rewards: _containers.RepeatedScalarFieldContainer[int]
    count: int
    error: Error
    def __init__(self, rewards: _Optional[_Iterable[int]] = ..., count: _Optional[int] = ..., error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class ResFetchActivityInterval(_message.Message):
    __slots__ = ()
    class ActivityInterval(_message.Message):
        __slots__ = ()
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

class ResFetchActivityRank(_message.Message):
    __slots__ = ()
    class ActivityRankItem(_message.Message):
        __slots__ = ()
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
    def __init__(self_, error: _Optional[_Union[Error, _Mapping]] = ..., items: _Optional[_Iterable[_Union[ResFetchActivityRank.ActivityRankItem, _Mapping]]] = ..., self: _Optional[_Union[ResFetchActivityRank.ActivityRankItem, _Mapping]] = ...) -> None: ...

class ResFetchAmuletActivityData(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    error: Error
    data: ActivityAmuletData
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., data: _Optional[_Union[ActivityAmuletData, _Mapping]] = ...) -> None: ...

class ResFetchAnnualReportInfo(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    error: Error
    start_time: int
    end_time: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., start_time: _Optional[int] = ..., end_time: _Optional[int] = ...) -> None: ...

class ResFetchBingoActivityData(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    error: Error
    data: ActivityBingoData
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., data: _Optional[_Union[ActivityBingoData, _Mapping]] = ...) -> None: ...

class ResFetchChallengeInfo(_message.Message):
    __slots__ = ()
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

class ResFetchCommentContent(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    COMMENTS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    comments: _containers.RepeatedCompositeFieldContainer[CommentItem]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., comments: _Optional[_Iterable[_Union[CommentItem, _Mapping]]] = ...) -> None: ...

class ResFetchCommentList(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    COMMENT_ALLOW_FIELD_NUMBER: _ClassVar[int]
    COMMENT_ID_LIST_FIELD_NUMBER: _ClassVar[int]
    LAST_READ_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    comment_allow: int
    comment_id_list: _containers.RepeatedScalarFieldContainer[int]
    last_read_id: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., comment_allow: _Optional[int] = ..., comment_id_list: _Optional[_Iterable[int]] = ..., last_read_id: _Optional[int] = ...) -> None: ...

class ResFetchContestPlayerRank(_message.Message):
    __slots__ = ()
    class ContestPlayerAccountData(_message.Message):
        __slots__ = ()
        class ContestGameResult(_message.Message):
            __slots__ = ()
            RANK_FIELD_NUMBER: _ClassVar[int]
            TOTAL_POINT_FIELD_NUMBER: _ClassVar[int]
            rank: int
            total_point: int
            def __init__(self, rank: _Optional[int] = ..., total_point: _Optional[int] = ...) -> None: ...
        class ContestSeriesGameResult(_message.Message):
            __slots__ = ()
            KEY_FIELD_NUMBER: _ClassVar[int]
            RESULTS_FIELD_NUMBER: _ClassVar[int]
            key: int
            results: _containers.RepeatedCompositeFieldContainer[ResFetchContestPlayerRank.ContestPlayerAccountData.ContestGameResult]
            def __init__(self, key: _Optional[int] = ..., results: _Optional[_Iterable[_Union[ResFetchContestPlayerRank.ContestPlayerAccountData.ContestGameResult, _Mapping]]] = ...) -> None: ...
        TOTAL_GAME_COUNT_FIELD_NUMBER: _ClassVar[int]
        RECENT_GAMES_FIELD_NUMBER: _ClassVar[int]
        HIGHEST_SERIES_POINTS_FIELD_NUMBER: _ClassVar[int]
        ACCUMULATE_POINT_FIELD_NUMBER: _ClassVar[int]
        total_game_count: int
        recent_games: _containers.RepeatedCompositeFieldContainer[ResFetchContestPlayerRank.ContestPlayerAccountData.ContestGameResult]
        highest_series_points: _containers.RepeatedCompositeFieldContainer[ResFetchContestPlayerRank.ContestPlayerAccountData.ContestSeriesGameResult]
        accumulate_point: int
        def __init__(self, total_game_count: _Optional[int] = ..., recent_games: _Optional[_Iterable[_Union[ResFetchContestPlayerRank.ContestPlayerAccountData.ContestGameResult, _Mapping]]] = ..., highest_series_points: _Optional[_Iterable[_Union[ResFetchContestPlayerRank.ContestPlayerAccountData.ContestSeriesGameResult, _Mapping]]] = ..., accumulate_point: _Optional[int] = ...) -> None: ...
    class SeasonRank(_message.Message):
        __slots__ = ()
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        NICKNAME_FIELD_NUMBER: _ClassVar[int]
        DATA_FIELD_NUMBER: _ClassVar[int]
        TEAM_NAME_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        nickname: str
        data: ResFetchContestPlayerRank.ContestPlayerAccountData
        team_name: str
        def __init__(self, account_id: _Optional[int] = ..., nickname: _Optional[str] = ..., data: _Optional[_Union[ResFetchContestPlayerRank.ContestPlayerAccountData, _Mapping]] = ..., team_name: _Optional[str] = ...) -> None: ...
    class PlayerData(_message.Message):
        __slots__ = ()
        RANK_FIELD_NUMBER: _ClassVar[int]
        DATA_FIELD_NUMBER: _ClassVar[int]
        TEAM_NAME_FIELD_NUMBER: _ClassVar[int]
        rank: int
        data: ResFetchContestPlayerRank.ContestPlayerAccountData
        team_name: str
        def __init__(self, rank: _Optional[int] = ..., data: _Optional[_Union[ResFetchContestPlayerRank.ContestPlayerAccountData, _Mapping]] = ..., team_name: _Optional[str] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    RANK_FIELD_NUMBER: _ClassVar[int]
    PLAYER_DATA_FIELD_NUMBER: _ClassVar[int]
    error: Error
    total: int
    rank: _containers.RepeatedCompositeFieldContainer[ResFetchContestPlayerRank.SeasonRank]
    player_data: ResFetchContestPlayerRank.PlayerData
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., total: _Optional[int] = ..., rank: _Optional[_Iterable[_Union[ResFetchContestPlayerRank.SeasonRank, _Mapping]]] = ..., player_data: _Optional[_Union[ResFetchContestPlayerRank.PlayerData, _Mapping]] = ...) -> None: ...

class ResFetchContestTeamMember(_message.Message):
    __slots__ = ()
    class ContestTeamMemberRank(_message.Message):
        __slots__ = ()
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        TOTAL_GAME_COUNT_FIELD_NUMBER: _ClassVar[int]
        TOTAL_SCORE_FIELD_NUMBER: _ClassVar[int]
        NICKNAME_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        total_game_count: int
        total_score: int
        nickname: str
        def __init__(self, account_id: _Optional[int] = ..., total_game_count: _Optional[int] = ..., total_score: _Optional[int] = ..., nickname: _Optional[str] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    RANK_FIELD_NUMBER: _ClassVar[int]
    error: Error
    total: int
    rank: _containers.RepeatedCompositeFieldContainer[ResFetchContestTeamMember.ContestTeamMemberRank]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., total: _Optional[int] = ..., rank: _Optional[_Iterable[_Union[ResFetchContestTeamMember.ContestTeamMemberRank, _Mapping]]] = ...) -> None: ...

class ResFetchContestTeamRank(_message.Message):
    __slots__ = ()
    class ContestTeamData(_message.Message):
        __slots__ = ()
        TOTAL_POINT_FIELD_NUMBER: _ClassVar[int]
        TOTAL_GAME_COUNT_FIELD_NUMBER: _ClassVar[int]
        MEMBER_COUNT_FIELD_NUMBER: _ClassVar[int]
        total_point: int
        total_game_count: int
        member_count: int
        def __init__(self, total_point: _Optional[int] = ..., total_game_count: _Optional[int] = ..., member_count: _Optional[int] = ...) -> None: ...
    class SeasonTeamRank(_message.Message):
        __slots__ = ()
        TEAM_ID_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        DATA_FIELD_NUMBER: _ClassVar[int]
        RANK_FIELD_NUMBER: _ClassVar[int]
        team_id: int
        name: str
        data: ResFetchContestTeamRank.ContestTeamData
        rank: int
        def __init__(self, team_id: _Optional[int] = ..., name: _Optional[str] = ..., data: _Optional[_Union[ResFetchContestTeamRank.ContestTeamData, _Mapping]] = ..., rank: _Optional[int] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    RANK_FIELD_NUMBER: _ClassVar[int]
    SELF_TEAM_RANK_FIELD_NUMBER: _ClassVar[int]
    error: Error
    total: int
    rank: _containers.RepeatedCompositeFieldContainer[ResFetchContestTeamRank.SeasonTeamRank]
    self_team_rank: ResFetchContestTeamRank.SeasonTeamRank
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., total: _Optional[int] = ..., rank: _Optional[_Iterable[_Union[ResFetchContestTeamRank.SeasonTeamRank, _Mapping]]] = ..., self_team_rank: _Optional[_Union[ResFetchContestTeamRank.SeasonTeamRank, _Mapping]] = ...) -> None: ...

class ResFetchCustomizedContestAuthInfo(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    OBSERVER_LEVEL_FIELD_NUMBER: _ClassVar[int]
    error: Error
    observer_level: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., observer_level: _Optional[int] = ...) -> None: ...

class ResFetchCustomizedContestByContestId(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    CONTEST_INFO_FIELD_NUMBER: _ClassVar[int]
    error: Error
    contest_info: CustomizedContestAbstract
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., contest_info: _Optional[_Union[CustomizedContestAbstract, _Mapping]] = ...) -> None: ...

class ResFetchCustomizedContestGameLiveList(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    LIVE_LIST_FIELD_NUMBER: _ClassVar[int]
    error: Error
    live_list: _containers.RepeatedCompositeFieldContainer[GameLiveHead]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., live_list: _Optional[_Iterable[_Union[GameLiveHead, _Mapping]]] = ...) -> None: ...

class ResFetchCustomizedContestGameRecords(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    NEXT_INDEX_FIELD_NUMBER: _ClassVar[int]
    RECORD_LIST_FIELD_NUMBER: _ClassVar[int]
    error: Error
    next_index: int
    record_list: _containers.RepeatedCompositeFieldContainer[RecordGame]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., next_index: _Optional[int] = ..., record_list: _Optional[_Iterable[_Union[RecordGame, _Mapping]]] = ...) -> None: ...

class ResFetchCustomizedContestList(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    CONTESTS_FIELD_NUMBER: _ClassVar[int]
    FOLLOW_CONTESTS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    contests: _containers.RepeatedCompositeFieldContainer[CustomizedContestBase]
    follow_contests: _containers.RepeatedCompositeFieldContainer[CustomizedContestBase]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., contests: _Optional[_Iterable[_Union[CustomizedContestBase, _Mapping]]] = ..., follow_contests: _Optional[_Iterable[_Union[CustomizedContestBase, _Mapping]]] = ...) -> None: ...

class ResFetchCustomizedContestOnlineInfo(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ONLINE_PLAYER_FIELD_NUMBER: _ClassVar[int]
    error: Error
    online_player: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., online_player: _Optional[int] = ...) -> None: ...

class ResFetchFriendGiftActivityData(_message.Message):
    __slots__ = ()
    class ItemCountData(_message.Message):
        __slots__ = ()
        ITEM_FIELD_NUMBER: _ClassVar[int]
        COUNT_FIELD_NUMBER: _ClassVar[int]
        item: int
        count: int
        def __init__(self, item: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...
    class FriendData(_message.Message):
        __slots__ = ()
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

class ResFetchGamingInfo(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    GAME_INFO_FIELD_NUMBER: _ClassVar[int]
    error: Error
    game_info: GameConnectInfo
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., game_info: _Optional[_Union[GameConnectInfo, _Mapping]] = ...) -> None: ...

class ResFetchInfo(_message.Message):
    __slots__ = ()
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
    RANDOM_CHARACTER_FIELD_NUMBER: _ClassVar[int]
    MAINTENANCE_INFO_FIELD_NUMBER: _ClassVar[int]
    SEER_INFO_FIELD_NUMBER: _ClassVar[int]
    ANNUAL_REPORT_INFO_FIELD_NUMBER: _ClassVar[int]
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
    random_character: ResRandomCharacter
    maintenance_info: ResFetchServerMaintenanceInfo
    seer_info: ResFetchSeerInfo
    annual_report_info: ResFetchAnnualReportInfo
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., server_time: _Optional[_Union[ResServerTime, _Mapping]] = ..., server_setting: _Optional[_Union[ResServerSettings, _Mapping]] = ..., client_value: _Optional[_Union[ResClientValue, _Mapping]] = ..., friend_list: _Optional[_Union[ResFriendList, _Mapping]] = ..., friend_apply_list: _Optional[_Union[ResFriendApplyList, _Mapping]] = ..., recent_friend: _Optional[_Union[ResFetchrecentFriend, _Mapping]] = ..., mail_info: _Optional[_Union[ResMailInfo, _Mapping]] = ..., receive_coin_info: _Optional[_Union[ResReviveCoinInfo, _Mapping]] = ..., title_list: _Optional[_Union[ResTitleList, _Mapping]] = ..., bag_info: _Optional[_Union[ResBagInfo, _Mapping]] = ..., shop_info: _Optional[_Union[ResShopInfo, _Mapping]] = ..., shop_interval: _Optional[_Union[ResFetchShopInterval, _Mapping]] = ..., activity_data: _Optional[_Union[ResAccountActivityData, _Mapping]] = ..., activity_interval: _Optional[_Union[ResFetchActivityInterval, _Mapping]] = ..., activity_buff: _Optional[_Union[ResActivityBuff, _Mapping]] = ..., vip_reward: _Optional[_Union[ResVipReward, _Mapping]] = ..., month_ticket_info: _Optional[_Union[ResMonthTicketInfo, _Mapping]] = ..., achievement: _Optional[_Union[ResAchievement, _Mapping]] = ..., comment_setting: _Optional[_Union[ResCommentSetting, _Mapping]] = ..., account_settings: _Optional[_Union[ResAccountSettings, _Mapping]] = ..., mod_nickname_time: _Optional[_Union[ResModNicknameTime, _Mapping]] = ..., misc: _Optional[_Union[ResMisc, _Mapping]] = ..., announcement: _Optional[_Union[ResAnnouncement, _Mapping]] = ..., activity_list: _Optional[_Union[ResActivityList, _Mapping]] = ..., character_info: _Optional[_Union[ResCharacterInfo, _Mapping]] = ..., all_common_views: _Optional[_Union[ResAllcommonViews, _Mapping]] = ..., collected_game_record_list: _Optional[_Union[ResCollectedGameRecordList, _Mapping]] = ..., maintain_notice: _Optional[_Union[ResFetchMaintainNotice, _Mapping]] = ..., random_character: _Optional[_Union[ResRandomCharacter, _Mapping]] = ..., maintenance_info: _Optional[_Union[ResFetchServerMaintenanceInfo, _Mapping]] = ..., seer_info: _Optional[_Union[ResFetchSeerInfo, _Mapping]] = ..., annual_report_info: _Optional[_Union[ResFetchAnnualReportInfo, _Mapping]] = ...) -> None: ...

class ResFetchJPCommonCreditCardOrder(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    error: Error
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class ResFetchLastPrivacy(_message.Message):
    __slots__ = ()
    class PrivacyInfo(_message.Message):
        __slots__ = ()
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

class ResFetchMaintainNotice(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    NOTICE_FIELD_NUMBER: _ClassVar[int]
    error: Error
    notice: MaintainNotice
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., notice: _Optional[_Union[MaintainNotice, _Mapping]] = ...) -> None: ...

class ResFetchManagerCustomizedContest(_message.Message):
    __slots__ = ()
    class SeasonInfo(_message.Message):
        __slots__ = ()
        CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
        START_TIME_FIELD_NUMBER: _ClassVar[int]
        END_TIME_FIELD_NUMBER: _ClassVar[int]
        create_time: int
        start_time: int
        end_time: int
        def __init__(self, create_time: _Optional[int] = ..., start_time: _Optional[int] = ..., end_time: _Optional[int] = ...) -> None: ...
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
    RANK_TYPE_FIELD_NUMBER: _ClassVar[int]
    SEASON_FIELD_NUMBER: _ClassVar[int]
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
    rank_type: int
    season: ResFetchManagerCustomizedContest.SeasonInfo
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., name: _Optional[str] = ..., open_show: _Optional[int] = ..., game_rule_setting: _Optional[_Union[GameMode, _Mapping]] = ..., start_time: _Optional[int] = ..., end_time: _Optional[int] = ..., auto_match: _Optional[int] = ..., rank_rule: _Optional[int] = ..., check_state: _Optional[int] = ..., checking_name: _Optional[str] = ..., contest_setting: _Optional[_Union[ContestSetting, _Mapping]] = ..., rank_type: _Optional[int] = ..., season: _Optional[_Union[ResFetchManagerCustomizedContest.SeasonInfo, _Mapping]] = ...) -> None: ...

class ResFetchManagerCustomizedContestList(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    CONTESTS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    contests: _containers.RepeatedCompositeFieldContainer[CustomizedContestBase]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., contests: _Optional[_Iterable[_Union[CustomizedContestBase, _Mapping]]] = ...) -> None: ...

class ResFetchOBToken(_message.Message):
    __slots__ = ()
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

class ResFetchOauth2(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    OPENID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    openid: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., openid: _Optional[str] = ...) -> None: ...

class ResFetchPhoneLoginBind(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    PHONE_LOGIN_FIELD_NUMBER: _ClassVar[int]
    error: Error
    phone_login: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., phone_login: _Optional[int] = ...) -> None: ...

class ResFetchProgressRewardActivityInfo(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    progress: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., progress: _Optional[int] = ...) -> None: ...

class ResFetchQuestionnaireDetail(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    DETAIL_FIELD_NUMBER: _ClassVar[int]
    error: Error
    detail: QuestionnaireDetail
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., detail: _Optional[_Union[QuestionnaireDetail, _Mapping]] = ...) -> None: ...

class ResFetchQuestionnaireList(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    LIST_FIELD_NUMBER: _ClassVar[int]
    FINISHED_LIST_FIELD_NUMBER: _ClassVar[int]
    error: Error
    list: _containers.RepeatedCompositeFieldContainer[QuestionnaireBrief]
    finished_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., list: _Optional[_Iterable[_Union[QuestionnaireBrief, _Mapping]]] = ..., finished_list: _Optional[_Iterable[int]] = ...) -> None: ...

class ResFetchQueueInfo(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    REMAIN_FIELD_NUMBER: _ClassVar[int]
    RANK_FIELD_NUMBER: _ClassVar[int]
    error: Error
    remain: int
    rank: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., remain: _Optional[int] = ..., rank: _Optional[int] = ...) -> None: ...

class ResFetchRPGBattleHistory(_message.Message):
    __slots__ = ()
    class BattleResult(_message.Message):
        __slots__ = ()
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
        UUID_FIELD_NUMBER: _ClassVar[int]
        POINTS_FIELD_NUMBER: _ClassVar[int]
        IS_ZIMO_FIELD_NUMBER: _ClassVar[int]
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
        uuid: str
        points: int
        is_zimo: int
        def __init__(self, chang: _Optional[int] = ..., ju: _Optional[int] = ..., ben: _Optional[int] = ..., target: _Optional[int] = ..., damage: _Optional[int] = ..., heal: _Optional[int] = ..., monster_seq: _Optional[int] = ..., chain_atk: _Optional[int] = ..., killed: _Optional[int] = ..., is_luk: _Optional[int] = ..., is_dex: _Optional[int] = ..., is_extra: _Optional[int] = ..., reward: _Optional[str] = ..., uuid: _Optional[str] = ..., points: _Optional[int] = ..., is_zimo: _Optional[int] = ...) -> None: ...
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
    __slots__ = ()
    class BattleResultV2(_message.Message):
        __slots__ = ()
        CHANG_FIELD_NUMBER: _ClassVar[int]
        JU_FIELD_NUMBER: _ClassVar[int]
        BEN_FIELD_NUMBER: _ClassVar[int]
        DAMAGE_FIELD_NUMBER: _ClassVar[int]
        MONSTER_SEQ_FIELD_NUMBER: _ClassVar[int]
        KILLED_FIELD_NUMBER: _ClassVar[int]
        BUFF_FIELD_NUMBER: _ClassVar[int]
        POINTS_FIELD_NUMBER: _ClassVar[int]
        UUID_FIELD_NUMBER: _ClassVar[int]
        chang: int
        ju: int
        ben: int
        damage: int
        monster_seq: int
        killed: int
        buff: _containers.RepeatedCompositeFieldContainer[ActivityBuffData]
        points: int
        uuid: str
        def __init__(self, chang: _Optional[int] = ..., ju: _Optional[int] = ..., ben: _Optional[int] = ..., damage: _Optional[int] = ..., monster_seq: _Optional[int] = ..., killed: _Optional[int] = ..., buff: _Optional[_Iterable[_Union[ActivityBuffData, _Mapping]]] = ..., points: _Optional[int] = ..., uuid: _Optional[str] = ...) -> None: ...
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

class ResFetchRankPointLeaderboard(_message.Message):
    __slots__ = ()
    class Item(_message.Message):
        __slots__ = ()
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

class ResFetchReadyPlayerList(_message.Message):
    __slots__ = ()
    class Player(_message.Message):
        __slots__ = ()
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        NICKNAME_FIELD_NUMBER: _ClassVar[int]
        TEAM_NAME_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        nickname: str
        team_name: str
        def __init__(self, account_id: _Optional[int] = ..., nickname: _Optional[str] = ..., team_name: _Optional[str] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    LIST_FIELD_NUMBER: _ClassVar[int]
    error: Error
    list: _containers.RepeatedCompositeFieldContainer[ResFetchReadyPlayerList.Player]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., list: _Optional[_Iterable[_Union[ResFetchReadyPlayerList.Player, _Mapping]]] = ...) -> None: ...

class ResFetchRefundOrder(_message.Message):
    __slots__ = ()
    class OrderInfo(_message.Message):
        __slots__ = ()
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

class ResFetchRollingNotice(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    NOTICE_FIELD_NUMBER: _ClassVar[int]
    error: Error
    notice: RollingNotice
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., notice: _Optional[_Union[RollingNotice, _Mapping]] = ...) -> None: ...

class ResFetchSeerInfo(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    REMAIN_COUNT_FIELD_NUMBER: _ClassVar[int]
    DATE_LIMIT_FIELD_NUMBER: _ClassVar[int]
    EXPIRE_TIME_FIELD_NUMBER: _ClassVar[int]
    error: Error
    remain_count: int
    date_limit: int
    expire_time: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., remain_count: _Optional[int] = ..., date_limit: _Optional[int] = ..., expire_time: _Optional[int] = ...) -> None: ...

class ResFetchSeerReport(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    REPORT_FIELD_NUMBER: _ClassVar[int]
    error: Error
    report: SeerReport
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., report: _Optional[_Union[SeerReport, _Mapping]] = ...) -> None: ...

class ResFetchSeerReportList(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    SEER_REPORT_LIST_FIELD_NUMBER: _ClassVar[int]
    error: Error
    seer_report_list: _containers.RepeatedCompositeFieldContainer[SeerBrief]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., seer_report_list: _Optional[_Iterable[_Union[SeerBrief, _Mapping]]] = ...) -> None: ...

class ResFetchSelfGamePointRank(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    SELF_RATE_FIELD_NUMBER: _ClassVar[int]
    error: Error
    self_rate: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., self_rate: _Optional[int] = ...) -> None: ...

class ResFetchServerMaintenanceInfo(_message.Message):
    __slots__ = ()
    class ServerFunctionMaintenanceInfo(_message.Message):
        __slots__ = ()
        NAME_FIELD_NUMBER: _ClassVar[int]
        OPEN_FIELD_NUMBER: _ClassVar[int]
        name: str
        open: bool
        def __init__(self, name: _Optional[str] = ..., open: _Optional[bool] = ...) -> None: ...
    FUNCTION_MAINTENANCE_FIELD_NUMBER: _ClassVar[int]
    function_maintenance: _containers.RepeatedCompositeFieldContainer[ResFetchServerMaintenanceInfo.ServerFunctionMaintenanceInfo]
    def __init__(self, function_maintenance: _Optional[_Iterable[_Union[ResFetchServerMaintenanceInfo.ServerFunctionMaintenanceInfo, _Mapping]]] = ...) -> None: ...

class ResFetchShopInterval(_message.Message):
    __slots__ = ()
    class ShopInterval(_message.Message):
        __slots__ = ()
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

class ResFetchSimulationGameRank(_message.Message):
    __slots__ = ()
    class RankInfo(_message.Message):
        __slots__ = ()
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

class ResFetchSimulationGameRecord(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    error: Error
    messages: _containers.RepeatedCompositeFieldContainer[ActivitySimulationGameRecordMessage]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., messages: _Optional[_Iterable[_Union[ActivitySimulationGameRecordMessage, _Mapping]]] = ...) -> None: ...

class ResFetchVoteActivity(_message.Message):
    __slots__ = ()
    class VoteRankData(_message.Message):
        __slots__ = ()
        ID_FIELD_NUMBER: _ClassVar[int]
        SHARE_FIELD_NUMBER: _ClassVar[int]
        id: int
        share: int
        def __init__(self, id: _Optional[int] = ..., share: _Optional[int] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    error: Error
    update_time: int
    data: _containers.RepeatedCompositeFieldContainer[ResFetchVoteActivity.VoteRankData]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., update_time: _Optional[int] = ..., data: _Optional[_Iterable[_Union[ResFetchVoteActivity.VoteRankData, _Mapping]]] = ...) -> None: ...

class ResFetchrecentFriend(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_LIST_FIELD_NUMBER: _ClassVar[int]
    error: Error
    account_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., account_list: _Optional[_Iterable[int]] = ...) -> None: ...

class ResFinishCombiningOrder(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    REWARD_ITEMS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    reward_items: _containers.RepeatedCompositeFieldContainer[ExecuteReward]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., reward_items: _Optional[_Iterable[_Union[ExecuteReward, _Mapping]]] = ...) -> None: ...

class ResFriendApplyList(_message.Message):
    __slots__ = ()
    class FriendApply(_message.Message):
        __slots__ = ()
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

class ResFriendList(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    FRIENDS_FIELD_NUMBER: _ClassVar[int]
    FRIEND_MAX_COUNT_FIELD_NUMBER: _ClassVar[int]
    FRIEND_COUNT_FIELD_NUMBER: _ClassVar[int]
    error: Error
    friends: _containers.RepeatedCompositeFieldContainer[Friend]
    friend_max_count: int
    friend_count: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., friends: _Optional[_Iterable[_Union[Friend, _Mapping]]] = ..., friend_max_count: _Optional[int] = ..., friend_count: _Optional[int] = ...) -> None: ...

class ResGameEndVote(_message.Message):
    __slots__ = ()
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    VOTE_CD_END_TIME_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: bool
    vote_cd_end_time: int
    error: Error
    def __init__(self, success: _Optional[bool] = ..., vote_cd_end_time: _Optional[int] = ..., error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class ResGameLiveInfo(_message.Message):
    __slots__ = ()
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

class ResGameLiveLeftSegment(_message.Message):
    __slots__ = ()
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

class ResGameLiveList(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    LIVE_LIST_FIELD_NUMBER: _ClassVar[int]
    error: Error
    live_list: _containers.RepeatedCompositeFieldContainer[GameLiveHead]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., live_list: _Optional[_Iterable[_Union[GameLiveHead, _Mapping]]] = ...) -> None: ...

class ResGamePlayerState(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    STATE_LIST_FIELD_NUMBER: _ClassVar[int]
    error: Error
    state_list: _containers.RepeatedScalarFieldContainer[GamePlayerState]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., state_list: _Optional[_Iterable[_Union[GamePlayerState, str]]] = ...) -> None: ...

class ResGamePointRank(_message.Message):
    __slots__ = ()
    class RankInfo(_message.Message):
        __slots__ = ()
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

class ResGameRecord(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    HEAD_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    DATA_URL_FIELD_NUMBER: _ClassVar[int]
    error: Error
    head: RecordGame
    data: bytes
    data_url: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., head: _Optional[_Union[RecordGame, _Mapping]] = ..., data: _Optional[bytes] = ..., data_url: _Optional[str] = ...) -> None: ...

class ResGameRecordList(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    RECORD_LIST_FIELD_NUMBER: _ClassVar[int]
    error: Error
    total_count: int
    record_list: _containers.RepeatedCompositeFieldContainer[RecordGame]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., total_count: _Optional[int] = ..., record_list: _Optional[_Iterable[_Union[RecordGame, _Mapping]]] = ...) -> None: ...

class ResGameRecordListV2(_message.Message):
    __slots__ = ()
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

class ResGameRecordsDetail(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    RECORD_LIST_FIELD_NUMBER: _ClassVar[int]
    error: Error
    record_list: _containers.RepeatedCompositeFieldContainer[RecordGame]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., record_list: _Optional[_Iterable[_Union[RecordGame, _Mapping]]] = ...) -> None: ...

class ResGameRecordsDetailV2(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    error: Error
    entries: _containers.RepeatedCompositeFieldContainer[RecordListEntry]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., entries: _Optional[_Iterable[_Union[RecordListEntry, _Mapping]]] = ...) -> None: ...

class ResGenerateAnnualReportToken(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    error: Error
    token: str
    url: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., token: _Optional[str] = ..., url: _Optional[str] = ...) -> None: ...

class ResGenerateCombiningCraft(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    POS_FIELD_NUMBER: _ClassVar[int]
    CRAFT_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    pos: int
    craft_id: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., pos: _Optional[int] = ..., craft_id: _Optional[int] = ...) -> None: ...

class ResGenerateContestManagerLoginCode(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    error: Error
    code: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., code: _Optional[str] = ...) -> None: ...

class ResGetFriendVillageData(_message.Message):
    __slots__ = ()
    class FriendVillageData(_message.Message):
        __slots__ = ()
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

class ResHeartbeat(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    error: Error
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class ResIDCardInfo(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    IS_AUTHED_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_FIELD_NUMBER: _ClassVar[int]
    error: Error
    is_authed: bool
    country: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., is_authed: _Optional[bool] = ..., country: _Optional[str] = ...) -> None: ...

class ResJoinCustomizedContestChatRoom(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    error: Error
    token: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., token: _Optional[str] = ...) -> None: ...

class ResJoinRoom(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ROOM_FIELD_NUMBER: _ClassVar[int]
    error: Error
    room: Room
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., room: _Optional[_Union[Room, _Mapping]] = ...) -> None: ...

class ResLevelLeaderboard(_message.Message):
    __slots__ = ()
    class Item(_message.Message):
        __slots__ = ()
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

class ResLikeSNS(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    IS_LIKED_FIELD_NUMBER: _ClassVar[int]
    error: Error
    is_liked: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., is_liked: _Optional[int] = ...) -> None: ...

class ResLogin(_message.Message):
    __slots__ = ()
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
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., account_id: _Optional[int] = ..., account: _Optional[_Union[Account, _Mapping]] = ..., game_info: _Optional[_Union[GameConnectInfo, _Mapping]] = ..., has_unread_announcement: _Optional[bool] = ..., access_token: _Optional[str] = ..., signup_time: _Optional[int] = ..., is_id_card_authed: _Optional[bool] = ..., country: _Optional[str] = ..., logined_version: _Optional[_Iterable[int]] = ..., rewarded_version: _Optional[_Iterable[int]] = ...) -> None: ...

class ResLogout(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    error: Error
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class ResMailInfo(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    MAILS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    mails: _containers.RepeatedCompositeFieldContainer[Mail]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., mails: _Optional[_Iterable[_Union[Mail, _Mapping]]] = ...) -> None: ...

class ResMisc(_message.Message):
    __slots__ = ()
    class MiscFaithData(_message.Message):
        __slots__ = ()
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
    DISABLE_ROOM_RANDOM_BOT_CHAR_FIELD_NUMBER: _ClassVar[int]
    error: Error
    recharged_list: _containers.RepeatedScalarFieldContainer[int]
    faiths: _containers.RepeatedCompositeFieldContainer[ResMisc.MiscFaithData]
    verified_hidden: int
    verified_value: int
    disable_room_random_bot_char: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., recharged_list: _Optional[_Iterable[int]] = ..., faiths: _Optional[_Iterable[_Union[ResMisc.MiscFaithData, _Mapping]]] = ..., verified_hidden: _Optional[int] = ..., verified_value: _Optional[int] = ..., disable_room_random_bot_char: _Optional[int] = ...) -> None: ...

class ResModNicknameTime(_message.Message):
    __slots__ = ()
    LAST_MOD_TIME_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    last_mod_time: int
    error: Error
    def __init__(self, last_mod_time: _Optional[int] = ..., error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class ResMonthTicketInfo(_message.Message):
    __slots__ = ()
    MONTH_TICKET_INFO_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    month_ticket_info: MonthTicketInfo
    error: Error
    def __init__(self, month_ticket_info: _Optional[_Union[MonthTicketInfo, _Mapping]] = ..., error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class ResMoveCombiningCraft(_message.Message):
    __slots__ = ()
    class BonusData(_message.Message):
        __slots__ = ()
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

class ResMultiAccountBrief(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    players: _containers.RepeatedCompositeFieldContainer[PlayerBaseView]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., players: _Optional[_Iterable[_Union[PlayerBaseView, _Mapping]]] = ...) -> None: ...

class ResMutiChallengeLevel(_message.Message):
    __slots__ = ()
    class Item(_message.Message):
        __slots__ = ()
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

class ResNextGameRecordList(_message.Message):
    __slots__ = ()
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
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., next: _Optional[bool] = ..., entries: _Optional[_Iterable[_Union[RecordListEntry, _Mapping]]] = ..., iterator_expire: _Optional[int] = ..., next_end_time: _Optional[int] = ...) -> None: ...

class ResNextRoundVillage(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_DATA_FIELD_NUMBER: _ClassVar[int]
    error: Error
    activity_data: ActivityVillageData
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., activity_data: _Optional[_Union[ActivityVillageData, _Mapping]] = ...) -> None: ...

class ResOauth2Auth(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    error: Error
    access_token: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., access_token: _Optional[str] = ...) -> None: ...

class ResOauth2Check(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    HAS_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    error: Error
    has_account: bool
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., has_account: _Optional[bool] = ...) -> None: ...

class ResOauth2Signup(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    error: Error
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class ResOpenAllRewardItem(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    results: _containers.RepeatedCompositeFieldContainer[OpenResult]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., results: _Optional[_Iterable[_Union[OpenResult, _Mapping]]] = ...) -> None: ...

class ResOpenChest(_message.Message):
    __slots__ = ()
    class ChestReplaceCountData(_message.Message):
        __slots__ = ()
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

class ResOpenGacha(_message.Message):
    __slots__ = ()
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

class ResOpenPreChestItem(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    results: _containers.RepeatedCompositeFieldContainer[OpenResult]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., results: _Optional[_Iterable[_Union[OpenResult, _Mapping]]] = ...) -> None: ...

class ResOpenRandomRewardItem(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    results: _containers.RepeatedCompositeFieldContainer[OpenResult]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., results: _Optional[_Iterable[_Union[OpenResult, _Mapping]]] = ...) -> None: ...

class ResPayMonthTicket(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_COUNT_FIELD_NUMBER: _ClassVar[int]
    error: Error
    resource_id: int
    resource_count: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., resource_id: _Optional[int] = ..., resource_count: _Optional[int] = ...) -> None: ...

class ResPlatformBillingProducts(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    PRODUCTS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    products: _containers.RepeatedCompositeFieldContainer[BillingProduct]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., products: _Optional[_Iterable[_Union[BillingProduct, _Mapping]]] = ...) -> None: ...

class ResProgressRewardActivityReceive(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    REWARD_ITEMS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    reward_items: _containers.RepeatedCompositeFieldContainer[ExecuteReward]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., reward_items: _Optional[_Iterable[_Union[ExecuteReward, _Mapping]]] = ...) -> None: ...

class ResQuestCrewActivityFeed(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    VALUE_CHANGES_FIELD_NUMBER: _ClassVar[int]
    EXECUTE_RESULT_FIELD_NUMBER: _ClassVar[int]
    error: Error
    value_changes: ActivityQuestCrewChanges
    execute_result: _containers.RepeatedCompositeFieldContainer[ExecuteResult]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., value_changes: _Optional[_Union[ActivityQuestCrewChanges, _Mapping]] = ..., execute_result: _Optional[_Iterable[_Union[ExecuteResult, _Mapping]]] = ...) -> None: ...

class ResQuestCrewActivityHire(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    VALUE_CHANGES_FIELD_NUMBER: _ClassVar[int]
    EXECUTE_RESULT_FIELD_NUMBER: _ClassVar[int]
    error: Error
    value_changes: ActivityQuestCrewChanges
    execute_result: _containers.RepeatedCompositeFieldContainer[ExecuteResult]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., value_changes: _Optional[_Union[ActivityQuestCrewChanges, _Mapping]] = ..., execute_result: _Optional[_Iterable[_Union[ExecuteResult, _Mapping]]] = ...) -> None: ...

class ResQuestCrewActivityRefreshMarket(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    VALUE_CHANGES_FIELD_NUMBER: _ClassVar[int]
    EXECUTE_RESULT_FIELD_NUMBER: _ClassVar[int]
    error: Error
    value_changes: ActivityQuestCrewChanges
    execute_result: _containers.RepeatedCompositeFieldContainer[ExecuteResult]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., value_changes: _Optional[_Union[ActivityQuestCrewChanges, _Mapping]] = ..., execute_result: _Optional[_Iterable[_Union[ExecuteResult, _Mapping]]] = ...) -> None: ...

class ResQuestCrewActivityStartQuest(_message.Message):
    __slots__ = ()
    class ActivityQuestCrewEffectInfo(_message.Message):
        __slots__ = ()
        MEMBER_ID_FIELD_NUMBER: _ClassVar[int]
        EFFECT_ID_FIELD_NUMBER: _ClassVar[int]
        RESULT_FIELD_NUMBER: _ClassVar[int]
        member_id: int
        effect_id: int
        result: ActivityQuestCrewEffectResult
        def __init__(self, member_id: _Optional[int] = ..., effect_id: _Optional[int] = ..., result: _Optional[_Union[ActivityQuestCrewEffectResult, _Mapping]] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    VALUE_CHANGES_FIELD_NUMBER: _ClassVar[int]
    EFFECT_INFO_FIELD_NUMBER: _ClassVar[int]
    error: Error
    result: int
    value_changes: ActivityQuestCrewChanges
    effect_info: _containers.RepeatedCompositeFieldContainer[ResQuestCrewActivityStartQuest.ActivityQuestCrewEffectInfo]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., result: _Optional[int] = ..., value_changes: _Optional[_Union[ActivityQuestCrewChanges, _Mapping]] = ..., effect_info: _Optional[_Iterable[_Union[ResQuestCrewActivityStartQuest.ActivityQuestCrewEffectInfo, _Mapping]]] = ...) -> None: ...

class ResRandomCharacter(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    POOL_FIELD_NUMBER: _ClassVar[int]
    error: Error
    enabled: bool
    pool: _containers.RepeatedCompositeFieldContainer[RandomCharacter]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., enabled: _Optional[bool] = ..., pool: _Optional[_Iterable[_Union[RandomCharacter, _Mapping]]] = ...) -> None: ...

class ResReadSNS(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    SNS_CONTENT_FIELD_NUMBER: _ClassVar[int]
    error: Error
    sns_content: SNSBlog
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., sns_content: _Optional[_Union[SNSBlog, _Mapping]] = ...) -> None: ...

class ResReceiveAchievementGroupReward(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    EXECUTE_REWARD_FIELD_NUMBER: _ClassVar[int]
    error: Error
    execute_reward: _containers.RepeatedCompositeFieldContainer[ExecuteReward]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., execute_reward: _Optional[_Iterable[_Union[ExecuteReward, _Mapping]]] = ...) -> None: ...

class ResReceiveAchievementReward(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    EXECUTE_REWARD_FIELD_NUMBER: _ClassVar[int]
    error: Error
    execute_reward: _containers.RepeatedCompositeFieldContainer[ExecuteReward]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., execute_reward: _Optional[_Iterable[_Union[ExecuteReward, _Mapping]]] = ...) -> None: ...

class ResReceiveActivityFlipTask(_message.Message):
    __slots__ = ()
    COUNT_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    count: int
    error: Error
    def __init__(self, count: _Optional[int] = ..., error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class ResReceiveActivitySpotReward(_message.Message):
    __slots__ = ()
    class RewardItem(_message.Message):
        __slots__ = ()
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

class ResReceiveAllActivityGift(_message.Message):
    __slots__ = ()
    class ReceiveRewards(_message.Message):
        __slots__ = ()
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

class ResReceiveChallengeRankReward(_message.Message):
    __slots__ = ()
    class Reward(_message.Message):
        __slots__ = ()
        RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
        COUNT_FIELD_NUMBER: _ClassVar[int]
        resource_id: int
        count: int
        def __init__(self, resource_id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...
    REWARDS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    rewards: _containers.RepeatedCompositeFieldContainer[ResReceiveChallengeRankReward.Reward]
    error: Error
    def __init__(self, rewards: _Optional[_Iterable[_Union[ResReceiveChallengeRankReward.Reward, _Mapping]]] = ..., error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class ResReceiveCharacterRewards(_message.Message):
    __slots__ = ()
    class RewardItem(_message.Message):
        __slots__ = ()
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

class ResReceiveRPGRewards(_message.Message):
    __slots__ = ()
    class RewardItem(_message.Message):
        __slots__ = ()
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

class ResReceiveUpgradeActivityReward(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    REWARDS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    rewards: _containers.RepeatedCompositeFieldContainer[ExecuteReward]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., rewards: _Optional[_Iterable[_Union[ExecuteReward, _Mapping]]] = ...) -> None: ...

class ResReceiveVillageBuildingReward(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    REWARD_ITEMS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    reward_items: _containers.RepeatedCompositeFieldContainer[ExecuteReward]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., reward_items: _Optional[_Iterable[_Union[ExecuteReward, _Mapping]]] = ...) -> None: ...

class ResReceiveVillageTripReward(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    REWARD_ITEMS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    reward_items: _containers.RepeatedCompositeFieldContainer[ExecuteReward]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., reward_items: _Optional[_Iterable[_Union[ExecuteReward, _Mapping]]] = ...) -> None: ...

class ResRecoverCombiningRecycle(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    CRAFT_ID_FIELD_NUMBER: _ClassVar[int]
    POS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    craft_id: int
    pos: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., craft_id: _Optional[int] = ..., pos: _Optional[int] = ...) -> None: ...

class ResRefreshChallenge(_message.Message):
    __slots__ = ()
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

class ResRefreshDailyTask(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    REFRESH_COUNT_FIELD_NUMBER: _ClassVar[int]
    error: Error
    progress: TaskProgress
    refresh_count: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., progress: _Optional[_Union[TaskProgress, _Mapping]] = ..., refresh_count: _Optional[int] = ...) -> None: ...

class ResRefreshGameObserveAuth(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    TTL_FIELD_NUMBER: _ClassVar[int]
    error: Error
    ttl: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., ttl: _Optional[int] = ...) -> None: ...

class ResRefreshZHPShop(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ZHP_FIELD_NUMBER: _ClassVar[int]
    error: Error
    zhp: ZHPShop
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., zhp: _Optional[_Union[ZHPShop, _Mapping]] = ...) -> None: ...

class ResRemoveCollectedGameRecord(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    error: Error
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class ResReplySNS(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    SNS_REPLY_FIELD_NUMBER: _ClassVar[int]
    error: Error
    sns_reply: SNSReply
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., sns_reply: _Optional[_Union[SNSReply, _Mapping]] = ...) -> None: ...

class ResRequestConnection(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    error: Error
    timestamp: int
    result: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., timestamp: _Optional[int] = ..., result: _Optional[int] = ...) -> None: ...

class ResRequestRouteChange(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    error: Error
    result: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., result: _Optional[int] = ...) -> None: ...

class ResResolveFestivalActivityEvent(_message.Message):
    __slots__ = ()
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

class ResResolveFestivalActivityProposal(_message.Message):
    __slots__ = ()
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

class ResReviveCoinInfo(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    HAS_GAINED_FIELD_NUMBER: _ClassVar[int]
    error: Error
    has_gained: bool
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., has_gained: _Optional[bool] = ...) -> None: ...

class ResRichmanChestInfo(_message.Message):
    __slots__ = ()
    class ItemData(_message.Message):
        __slots__ = ()
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

class ResRichmanNextMove(_message.Message):
    __slots__ = ()
    class RewardData(_message.Message):
        __slots__ = ()
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
        __slots__ = ()
        LOCATION_FIELD_NUMBER: _ClassVar[int]
        REWARDS_FIELD_NUMBER: _ClassVar[int]
        EVENTS_FIELD_NUMBER: _ClassVar[int]
        location: int
        rewards: _containers.RepeatedCompositeFieldContainer[ResRichmanNextMove.RewardData]
        events: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, location: _Optional[int] = ..., rewards: _Optional[_Iterable[_Union[ResRichmanNextMove.RewardData, _Mapping]]] = ..., events: _Optional[_Iterable[int]] = ...) -> None: ...
    class BuffData(_message.Message):
        __slots__ = ()
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

class ResSearchAccountById(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    PLAYER_FIELD_NUMBER: _ClassVar[int]
    error: Error
    player: PlayerBaseView
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., player: _Optional[_Union[PlayerBaseView, _Mapping]] = ...) -> None: ...

class ResSearchAccountByPattern(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    IS_FINISHED_FIELD_NUMBER: _ClassVar[int]
    MATCH_ACCOUNTS_FIELD_NUMBER: _ClassVar[int]
    DECODE_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    is_finished: bool
    match_accounts: _containers.RepeatedScalarFieldContainer[int]
    decode_id: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., is_finished: _Optional[bool] = ..., match_accounts: _Optional[_Iterable[int]] = ..., decode_id: _Optional[int] = ...) -> None: ...

class ResSearchAccountbyEidLobby(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    error: Error
    account_id: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., account_id: _Optional[int] = ...) -> None: ...

class ResSelfRoom(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ROOM_FIELD_NUMBER: _ClassVar[int]
    error: Error
    room: Room
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., room: _Optional[_Union[Room, _Mapping]] = ...) -> None: ...

class ResSendActivityGiftToFriend(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    SEND_GIFT_COUNT_FIELD_NUMBER: _ClassVar[int]
    error: Error
    send_gift_count: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., send_gift_count: _Optional[int] = ...) -> None: ...

class ResSendGiftToCharacter(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    EXP_FIELD_NUMBER: _ClassVar[int]
    error: Error
    level: int
    exp: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., level: _Optional[int] = ..., exp: _Optional[int] = ...) -> None: ...

class ResServerSettings(_message.Message):
    __slots__ = ()
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    settings: ServerSettings
    error: Error
    def __init__(self, settings: _Optional[_Union[ServerSettings, _Mapping]] = ..., error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class ResServerTime(_message.Message):
    __slots__ = ()
    SERVER_TIME_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    server_time: int
    error: Error
    def __init__(self, server_time: _Optional[int] = ..., error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class ResSetHiddenCharacter(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    HIDDEN_CHARACTERS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    hidden_characters: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., hidden_characters: _Optional[_Iterable[int]] = ...) -> None: ...

class ResSetVillageWorker(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    BUILDING_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    error: Error
    building: VillageBuildingData
    update_time: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., building: _Optional[_Union[VillageBuildingData, _Mapping]] = ..., update_time: _Optional[int] = ...) -> None: ...

class ResShootActivityAttackEnemies(_message.Message):
    __slots__ = ()
    class ActivityShootAttackRecord(_message.Message):
        __slots__ = ()
        POSITION_FIELD_NUMBER: _ClassVar[int]
        ENEMY_FIELD_NUMBER: _ClassVar[int]
        LEVEL_FIELD_NUMBER: _ClassVar[int]
        REWARD_IDS_FIELD_NUMBER: _ClassVar[int]
        REWARDS_FIELD_NUMBER: _ClassVar[int]
        position: int
        enemy: ActivityShootEnemyInfo
        level: int
        reward_ids: _containers.RepeatedScalarFieldContainer[int]
        rewards: _containers.RepeatedCompositeFieldContainer[ExecuteReward]
        def __init__(self, position: _Optional[int] = ..., enemy: _Optional[_Union[ActivityShootEnemyInfo, _Mapping]] = ..., level: _Optional[int] = ..., reward_ids: _Optional[_Iterable[int]] = ..., rewards: _Optional[_Iterable[_Union[ExecuteReward, _Mapping]]] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    RECORDS_FIELD_NUMBER: _ClassVar[int]
    VALUE_CHANGE_FIELD_NUMBER: _ClassVar[int]
    error: Error
    records: _containers.RepeatedCompositeFieldContainer[ResShootActivityAttackEnemies.ActivityShootAttackRecord]
    value_change: ActivityShootValueChange
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., records: _Optional[_Iterable[_Union[ResShootActivityAttackEnemies.ActivityShootAttackRecord, _Mapping]]] = ..., value_change: _Optional[_Union[ActivityShootValueChange, _Mapping]] = ...) -> None: ...

class ResShopInfo(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    SHOP_INFO_FIELD_NUMBER: _ClassVar[int]
    error: Error
    shop_info: ShopInfo
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., shop_info: _Optional[_Union[ShopInfo, _Mapping]] = ...) -> None: ...

class ResShopPurchase(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    UPDATE_FIELD_NUMBER: _ClassVar[int]
    error: Error
    update: AccountUpdate
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., update: _Optional[_Union[AccountUpdate, _Mapping]] = ...) -> None: ...

class ResSignupAccount(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    error: Error
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class ResSignupCustomizedContest(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    error: Error
    state: int
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., state: _Optional[int] = ...) -> None: ...

class ResSimV2ActivityEndMatch(_message.Message):
    __slots__ = ()
    class SimulationV2MatchReward(_message.Message):
        __slots__ = ()
        TYPE_FIELD_NUMBER: _ClassVar[int]
        PARAMS_FIELD_NUMBER: _ClassVar[int]
        type: int
        params: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, type: _Optional[int] = ..., params: _Optional[_Iterable[int]] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ROUND_FIELD_NUMBER: _ClassVar[int]
    IS_END_FIELD_NUMBER: _ClassVar[int]
    RECORD_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SCORE_FIELD_NUMBER: _ClassVar[int]
    MATCH_HISTORY_FIELD_NUMBER: _ClassVar[int]
    REWARDS_FIELD_NUMBER: _ClassVar[int]
    EFFECT_LIST_FIELD_NUMBER: _ClassVar[int]
    ABILITY_FIELD_NUMBER: _ClassVar[int]
    error: Error
    round: int
    is_end: bool
    record: SimulationV2Record
    total_score: int
    match_history: _containers.RepeatedCompositeFieldContainer[SimulationV2MatchRecord]
    rewards: _containers.RepeatedCompositeFieldContainer[ResSimV2ActivityEndMatch.SimulationV2MatchReward]
    effect_list: _containers.RepeatedCompositeFieldContainer[SimulationV2Effect]
    ability: SimulationV2Ability
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., round: _Optional[int] = ..., is_end: _Optional[bool] = ..., record: _Optional[_Union[SimulationV2Record, _Mapping]] = ..., total_score: _Optional[int] = ..., match_history: _Optional[_Iterable[_Union[SimulationV2MatchRecord, _Mapping]]] = ..., rewards: _Optional[_Iterable[_Union[ResSimV2ActivityEndMatch.SimulationV2MatchReward, _Mapping]]] = ..., effect_list: _Optional[_Iterable[_Union[SimulationV2Effect, _Mapping]]] = ..., ability: _Optional[_Union[SimulationV2Ability, _Mapping]] = ...) -> None: ...

class ResSimV2ActivityFetchInfo(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    error: Error
    data: SimulationV2Data
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., data: _Optional[_Union[SimulationV2Data, _Mapping]] = ...) -> None: ...

class ResSimV2ActivitySelectEvent(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    EVENT_FIELD_NUMBER: _ClassVar[int]
    ABILITY_FIELD_NUMBER: _ClassVar[int]
    MATCH_FIELD_NUMBER: _ClassVar[int]
    EFFECT_LIST_FIELD_NUMBER: _ClassVar[int]
    ROUND_FIELD_NUMBER: _ClassVar[int]
    IS_END_FIELD_NUMBER: _ClassVar[int]
    RESULT_ID_FIELD_NUMBER: _ClassVar[int]
    RECORD_FIELD_NUMBER: _ClassVar[int]
    EFFECTED_BUFF_LIST_FIELD_NUMBER: _ClassVar[int]
    error: Error
    event: SimulationV2Event
    ability: SimulationV2Ability
    match: SimulationV2Match
    effect_list: _containers.RepeatedCompositeFieldContainer[SimulationV2Effect]
    round: int
    is_end: bool
    result_id: int
    record: SimulationV2Record
    effected_buff_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., event: _Optional[_Union[SimulationV2Event, _Mapping]] = ..., ability: _Optional[_Union[SimulationV2Ability, _Mapping]] = ..., match: _Optional[_Union[SimulationV2Match, _Mapping]] = ..., effect_list: _Optional[_Iterable[_Union[SimulationV2Effect, _Mapping]]] = ..., round: _Optional[int] = ..., is_end: _Optional[bool] = ..., result_id: _Optional[int] = ..., record: _Optional[_Union[SimulationV2Record, _Mapping]] = ..., effected_buff_list: _Optional[_Iterable[int]] = ...) -> None: ...

class ResSimV2ActivityStartMatch(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    EVENT_FIELD_NUMBER: _ClassVar[int]
    MATCH_FIELD_NUMBER: _ClassVar[int]
    EFFECT_LIST_FIELD_NUMBER: _ClassVar[int]
    IS_MATCH_END_FIELD_NUMBER: _ClassVar[int]
    error: Error
    event: SimulationV2Event
    match: SimulationV2Match
    effect_list: _containers.RepeatedCompositeFieldContainer[SimulationV2Effect]
    is_match_end: bool
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., event: _Optional[_Union[SimulationV2Event, _Mapping]] = ..., match: _Optional[_Union[SimulationV2Match, _Mapping]] = ..., effect_list: _Optional[_Iterable[_Union[SimulationV2Effect, _Mapping]]] = ..., is_match_end: _Optional[bool] = ...) -> None: ...

class ResSimV2ActivityStartSeason(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    SEASON_FIELD_NUMBER: _ClassVar[int]
    error: Error
    season: SimulationV2SeasonData
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., season: _Optional[_Union[SimulationV2SeasonData, _Mapping]] = ...) -> None: ...

class ResSimV2ActivityTrain(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    EVENT_FIELD_NUMBER: _ClassVar[int]
    ABILITY_FIELD_NUMBER: _ClassVar[int]
    ROUND_FIELD_NUMBER: _ClassVar[int]
    EFFECT_LIST_FIELD_NUMBER: _ClassVar[int]
    TRAIN_RESULT_FIELD_NUMBER: _ClassVar[int]
    IS_END_FIELD_NUMBER: _ClassVar[int]
    RECORD_FIELD_NUMBER: _ClassVar[int]
    error: Error
    event: SimulationV2Event
    ability: SimulationV2Ability
    round: int
    effect_list: _containers.RepeatedCompositeFieldContainer[SimulationV2Effect]
    train_result: int
    is_end: bool
    record: SimulationV2Record
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., event: _Optional[_Union[SimulationV2Event, _Mapping]] = ..., ability: _Optional[_Union[SimulationV2Ability, _Mapping]] = ..., round: _Optional[int] = ..., effect_list: _Optional[_Iterable[_Union[SimulationV2Effect, _Mapping]]] = ..., train_result: _Optional[int] = ..., is_end: _Optional[bool] = ..., record: _Optional[_Union[SimulationV2Record, _Mapping]] = ...) -> None: ...

class ResSimulationActivityTrain(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    RESULT_TYPE_FIELD_NUMBER: _ClassVar[int]
    FINAL_STATS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    result_type: int
    final_stats: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., result_type: _Optional[int] = ..., final_stats: _Optional[_Iterable[int]] = ...) -> None: ...

class ResStartObserve(_message.Message):
    __slots__ = ()
    HEAD_FIELD_NUMBER: _ClassVar[int]
    PASSED_FIELD_NUMBER: _ClassVar[int]
    head: GameLiveHead
    passed: GameLiveSegment
    def __init__(self, head: _Optional[_Union[GameLiveHead, _Mapping]] = ..., passed: _Optional[_Union[GameLiveSegment, _Mapping]] = ...) -> None: ...

class ResStartSimulationActivityGame(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    RECORDS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    records: _containers.RepeatedCompositeFieldContainer[ActivitySimulationGameRecord]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., records: _Optional[_Iterable[_Union[ActivitySimulationGameRecord, _Mapping]]] = ...) -> None: ...

class ResStoryActivityUnlockEndingAndReceive(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ENDING_REWARD_FIELD_NUMBER: _ClassVar[int]
    FINISH_REWARD_FIELD_NUMBER: _ClassVar[int]
    ALL_FINISH_REWARD_FIELD_NUMBER: _ClassVar[int]
    error: Error
    ending_reward: _containers.RepeatedCompositeFieldContainer[ExecuteReward]
    finish_reward: _containers.RepeatedCompositeFieldContainer[ExecuteReward]
    all_finish_reward: _containers.RepeatedCompositeFieldContainer[ExecuteReward]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., ending_reward: _Optional[_Iterable[_Union[ExecuteReward, _Mapping]]] = ..., finish_reward: _Optional[_Iterable[_Union[ExecuteReward, _Mapping]]] = ..., all_finish_reward: _Optional[_Iterable[_Union[ExecuteReward, _Mapping]]] = ...) -> None: ...

class ResStoryReward(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    REWARD_ITEMS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    reward_items: _containers.RepeatedCompositeFieldContainer[ExecuteReward]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., reward_items: _Optional[_Iterable[_Union[ExecuteReward, _Mapping]]] = ...) -> None: ...

class ResSyncGame(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    IS_END_FIELD_NUMBER: _ClassVar[int]
    STEP_FIELD_NUMBER: _ClassVar[int]
    GAME_RESTORE_FIELD_NUMBER: _ClassVar[int]
    error: Error
    is_end: bool
    step: int
    game_restore: GameRestore
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., is_end: _Optional[bool] = ..., step: _Optional[int] = ..., game_restore: _Optional[_Union[GameRestore, _Mapping]] = ...) -> None: ...

class ResTitleList(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    TITLE_LIST_FIELD_NUMBER: _ClassVar[int]
    error: Error
    title_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., title_list: _Optional[_Iterable[int]] = ...) -> None: ...

class ResUpgradeActivityLevel(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    REWARDS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    rewards: _containers.RepeatedCompositeFieldContainer[ExecuteReward]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., rewards: _Optional[_Iterable[_Union[ExecuteReward, _Mapping]]] = ...) -> None: ...

class ResUpgradeChallenge(_message.Message):
    __slots__ = ()
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

class ResUpgradeCharacter(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    CHARACTER_FIELD_NUMBER: _ClassVar[int]
    error: Error
    character: Character
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., character: _Optional[_Union[Character, _Mapping]] = ...) -> None: ...

class ResUseGiftCode(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    REWARDS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    rewards: _containers.RepeatedCompositeFieldContainer[RewardSlot]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., rewards: _Optional[_Iterable[_Union[RewardSlot, _Mapping]]] = ...) -> None: ...

class ResUseSpecialGiftCode(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    REWARDS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    rewards: _containers.RepeatedCompositeFieldContainer[ExecuteReward]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., rewards: _Optional[_Iterable[_Union[ExecuteReward, _Mapping]]] = ...) -> None: ...

class ResVerfiyCodeForSecure(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    SECURE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    error: Error
    secure_token: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., secure_token: _Optional[str] = ...) -> None: ...

class ResVerificationIAPOrder(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    error: Error
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class ResVipReward(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    GAINED_VIP_LEVELS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    gained_vip_levels: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., gained_vip_levels: _Optional[_Iterable[int]] = ...) -> None: ...

class ResVoteActivity(_message.Message):
    __slots__ = ()
    ERROR_FIELD_NUMBER: _ClassVar[int]
    VOTE_RECORDS_FIELD_NUMBER: _ClassVar[int]
    error: Error
    vote_records: _containers.RepeatedCompositeFieldContainer[VoteData]
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., vote_records: _Optional[_Iterable[_Union[VoteData, _Mapping]]] = ...) -> None: ...

class RewardPlusResult(_message.Message):
    __slots__ = ()
    class Exchange(_message.Message):
        __slots__ = ()
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

class RewardSlot(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    id: int
    count: int
    def __init__(self, id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class RollingNotice(_message.Message):
    __slots__ = ()
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

class Room(_message.Message):
    __slots__ = ()
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
    ROBOTS_FIELD_NUMBER: _ClassVar[int]
    POSITIONS_FIELD_NUMBER: _ClassVar[int]
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
    robots: _containers.RepeatedCompositeFieldContainer[PlayerGameView]
    positions: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, room_id: _Optional[int] = ..., owner_id: _Optional[int] = ..., mode: _Optional[_Union[GameMode, _Mapping]] = ..., max_player_count: _Optional[int] = ..., persons: _Optional[_Iterable[_Union[PlayerGameView, _Mapping]]] = ..., ready_list: _Optional[_Iterable[int]] = ..., is_playing: _Optional[bool] = ..., public_live: _Optional[bool] = ..., robot_count: _Optional[int] = ..., tournament_id: _Optional[int] = ..., seq: _Optional[int] = ..., pre_rule: _Optional[str] = ..., robots: _Optional[_Iterable[_Union[PlayerGameView, _Mapping]]] = ..., positions: _Optional[_Iterable[int]] = ...) -> None: ...

class SNSBlog(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    READ_TIME_FIELD_NUMBER: _ClassVar[int]
    id: int
    read_time: int
    def __init__(self, id: _Optional[int] = ..., read_time: _Optional[int] = ...) -> None: ...

class SNSReply(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    REPLY_TIME_FIELD_NUMBER: _ClassVar[int]
    id: int
    reply_time: int
    def __init__(self, id: _Optional[int] = ..., reply_time: _Optional[int] = ...) -> None: ...

class SeerBrief(_message.Message):
    __slots__ = ()
    UUID_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    EXPIRE_TIME_FIELD_NUMBER: _ClassVar[int]
    PLAYER_SCORES_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    state: int
    expire_time: int
    player_scores: _containers.RepeatedCompositeFieldContainer[SeerScore]
    create_time: int
    def __init__(self, uuid: _Optional[str] = ..., state: _Optional[int] = ..., expire_time: _Optional[int] = ..., player_scores: _Optional[_Iterable[_Union[SeerScore, _Mapping]]] = ..., create_time: _Optional[int] = ...) -> None: ...

class SeerEvent(_message.Message):
    __slots__ = ()
    RECORD_INDEX_FIELD_NUMBER: _ClassVar[int]
    SEER_INDEX_FIELD_NUMBER: _ClassVar[int]
    RECOMMENDS_FIELD_NUMBER: _ClassVar[int]
    record_index: int
    seer_index: int
    recommends: _containers.RepeatedCompositeFieldContainer[SeerRecommend]
    def __init__(self, record_index: _Optional[int] = ..., seer_index: _Optional[int] = ..., recommends: _Optional[_Iterable[_Union[SeerRecommend, _Mapping]]] = ...) -> None: ...

class SeerPrediction(_message.Message):
    __slots__ = ()
    ACTION_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    action: int
    score: int
    def __init__(self, action: _Optional[int] = ..., score: _Optional[int] = ...) -> None: ...

class SeerRecommend(_message.Message):
    __slots__ = ()
    SEAT_FIELD_NUMBER: _ClassVar[int]
    PREDICTIONS_FIELD_NUMBER: _ClassVar[int]
    seat: int
    predictions: _containers.RepeatedCompositeFieldContainer[SeerPrediction]
    def __init__(self, seat: _Optional[int] = ..., predictions: _Optional[_Iterable[_Union[SeerPrediction, _Mapping]]] = ...) -> None: ...

class SeerReport(_message.Message):
    __slots__ = ()
    UUID_FIELD_NUMBER: _ClassVar[int]
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    ROUNDS_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    events: _containers.RepeatedCompositeFieldContainer[SeerEvent]
    rounds: _containers.RepeatedCompositeFieldContainer[SeerRound]
    def __init__(self, uuid: _Optional[str] = ..., events: _Optional[_Iterable[_Union[SeerEvent, _Mapping]]] = ..., rounds: _Optional[_Iterable[_Union[SeerRound, _Mapping]]] = ...) -> None: ...

class SeerRound(_message.Message):
    __slots__ = ()
    CHANG_FIELD_NUMBER: _ClassVar[int]
    JU_FIELD_NUMBER: _ClassVar[int]
    BEN_FIELD_NUMBER: _ClassVar[int]
    PLAYER_SCORES_FIELD_NUMBER: _ClassVar[int]
    chang: int
    ju: int
    ben: int
    player_scores: _containers.RepeatedCompositeFieldContainer[SeerScore]
    def __init__(self, chang: _Optional[int] = ..., ju: _Optional[int] = ..., ben: _Optional[int] = ..., player_scores: _Optional[_Iterable[_Union[SeerScore, _Mapping]]] = ...) -> None: ...

class SeerScore(_message.Message):
    __slots__ = ()
    SEAT_FIELD_NUMBER: _ClassVar[int]
    RATING_FIELD_NUMBER: _ClassVar[int]
    seat: int
    rating: int
    def __init__(self, seat: _Optional[int] = ..., rating: _Optional[int] = ...) -> None: ...

class SegmentTaskProgress(_message.Message):
    __slots__ = ()
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
    def __init__(self, id: _Optional[int] = ..., counter: _Optional[int] = ..., achieved: _Optional[bool] = ..., rewarded: _Optional[bool] = ..., failed: _Optional[bool] = ..., reward_count: _Optional[int] = ..., achieved_count: _Optional[int] = ...) -> None: ...

class ServerSettings(_message.Message):
    __slots__ = ()
    PAYMENT_SETTING_FIELD_NUMBER: _ClassVar[int]
    PAYMENT_SETTING_V2_FIELD_NUMBER: _ClassVar[int]
    NICKNAME_SETTING_FIELD_NUMBER: _ClassVar[int]
    payment_setting: PaymentSetting
    payment_setting_v2: PaymentSettingV2
    nickname_setting: NicknameSetting
    def __init__(self, payment_setting: _Optional[_Union[PaymentSetting, _Mapping]] = ..., payment_setting_v2: _Optional[_Union[PaymentSettingV2, _Mapping]] = ..., nickname_setting: _Optional[_Union[NicknameSetting, _Mapping]] = ...) -> None: ...

class ShopInfo(_message.Message):
    __slots__ = ()
    class SelectedPackageBuyRecord(_message.Message):
        __slots__ = ()
        PACKAGE_ID_FIELD_NUMBER: _ClassVar[int]
        BUY_RECORDS_FIELD_NUMBER: _ClassVar[int]
        package_id: int
        buy_records: _containers.RepeatedCompositeFieldContainer[BuyRecord]
        def __init__(self, package_id: _Optional[int] = ..., buy_records: _Optional[_Iterable[_Union[BuyRecord, _Mapping]]] = ...) -> None: ...
    ZHP_FIELD_NUMBER: _ClassVar[int]
    BUY_RECORDS_FIELD_NUMBER: _ClassVar[int]
    LAST_REFRESH_TIME_FIELD_NUMBER: _ClassVar[int]
    SELECTED_PACKAGE_RECORDS_FIELD_NUMBER: _ClassVar[int]
    zhp: ZHPShop
    buy_records: _containers.RepeatedCompositeFieldContainer[BuyRecord]
    last_refresh_time: int
    selected_package_records: _containers.RepeatedCompositeFieldContainer[ShopInfo.SelectedPackageBuyRecord]
    def __init__(self, zhp: _Optional[_Union[ZHPShop, _Mapping]] = ..., buy_records: _Optional[_Iterable[_Union[BuyRecord, _Mapping]]] = ..., last_refresh_time: _Optional[int] = ..., selected_package_records: _Optional[_Iterable[_Union[ShopInfo.SelectedPackageBuyRecord, _Mapping]]] = ...) -> None: ...

class SignedTimeCounterData(_message.Message):
    __slots__ = ()
    COUNT_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    count: int
    update_time: int
    def __init__(self, count: _Optional[int] = ..., update_time: _Optional[int] = ...) -> None: ...

class SimulationActionData(_message.Message):
    __slots__ = ()
    class ActionRiichiData(_message.Message):
        __slots__ = ()
        SEAT_FIELD_NUMBER: _ClassVar[int]
        seat: int
        def __init__(self, seat: _Optional[int] = ...) -> None: ...
    class ActionHuleData(_message.Message):
        __slots__ = ()
        class HuleInfo(_message.Message):
            __slots__ = ()
            FAN_FIELD_NUMBER: _ClassVar[int]
            ZIMO_FIELD_NUMBER: _ClassVar[int]
            POINT_FIELD_NUMBER: _ClassVar[int]
            OYA_FIELD_NUMBER: _ClassVar[int]
            PLAYER_FIELD_NUMBER: _ClassVar[int]
            CHONG_FIELD_NUMBER: _ClassVar[int]
            TOUTIAO_FIELD_NUMBER: _ClassVar[int]
            fan: int
            zimo: bool
            point: int
            oya: bool
            player: int
            chong: int
            toutiao: bool
            def __init__(self, fan: _Optional[int] = ..., zimo: _Optional[bool] = ..., point: _Optional[int] = ..., oya: _Optional[bool] = ..., player: _Optional[int] = ..., chong: _Optional[int] = ..., toutiao: _Optional[bool] = ...) -> None: ...
        HULE_FIELD_NUMBER: _ClassVar[int]
        hule: _containers.RepeatedCompositeFieldContainer[SimulationActionData.ActionHuleData.HuleInfo]
        def __init__(self, hule: _Optional[_Iterable[_Union[SimulationActionData.ActionHuleData.HuleInfo, _Mapping]]] = ...) -> None: ...
    class ActionFuluData(_message.Message):
        __slots__ = ()
        SEAT_FIELD_NUMBER: _ClassVar[int]
        seat: int
        def __init__(self, seat: _Optional[int] = ...) -> None: ...
    class ActionDiscardData(_message.Message):
        __slots__ = ()
        SEAT_FIELD_NUMBER: _ClassVar[int]
        RIICHI_FIELD_NUMBER: _ClassVar[int]
        seat: int
        riichi: bool
        def __init__(self, seat: _Optional[int] = ..., riichi: _Optional[bool] = ...) -> None: ...
    class ActionDealTileData(_message.Message):
        __slots__ = ()
        SEAT_FIELD_NUMBER: _ClassVar[int]
        seat: int
        def __init__(self, seat: _Optional[int] = ...) -> None: ...
    TYPE_FIELD_NUMBER: _ClassVar[int]
    RIICHI_FIELD_NUMBER: _ClassVar[int]
    HULE_FIELD_NUMBER: _ClassVar[int]
    FULU_FIELD_NUMBER: _ClassVar[int]
    DISCARD_TILE_FIELD_NUMBER: _ClassVar[int]
    DEAL_TILE_FIELD_NUMBER: _ClassVar[int]
    type: int
    riichi: SimulationActionData.ActionRiichiData
    hule: SimulationActionData.ActionHuleData
    fulu: SimulationActionData.ActionFuluData
    discard_tile: SimulationActionData.ActionDiscardData
    deal_tile: SimulationActionData.ActionDealTileData
    def __init__(self, type: _Optional[int] = ..., riichi: _Optional[_Union[SimulationActionData.ActionRiichiData, _Mapping]] = ..., hule: _Optional[_Union[SimulationActionData.ActionHuleData, _Mapping]] = ..., fulu: _Optional[_Union[SimulationActionData.ActionFuluData, _Mapping]] = ..., discard_tile: _Optional[_Union[SimulationActionData.ActionDiscardData, _Mapping]] = ..., deal_tile: _Optional[_Union[SimulationActionData.ActionDealTileData, _Mapping]] = ...) -> None: ...

class SimulationV2Ability(_message.Message):
    __slots__ = ()
    LUK_FIELD_NUMBER: _ClassVar[int]
    TEC_FIELD_NUMBER: _ClassVar[int]
    INS_FIELD_NUMBER: _ClassVar[int]
    INT_FIELD_NUMBER: _ClassVar[int]
    RES_FIELD_NUMBER: _ClassVar[int]
    luk: int
    tec: int
    ins: int
    int: int
    res: int
    def __init__(self, luk: _Optional[int] = ..., tec: _Optional[int] = ..., ins: _Optional[int] = ..., int: _Optional[int] = ..., res: _Optional[int] = ...) -> None: ...

class SimulationV2Buff(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    ROUND_FIELD_NUMBER: _ClassVar[int]
    STORE_FIELD_NUMBER: _ClassVar[int]
    id: int
    round: int
    store: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, id: _Optional[int] = ..., round: _Optional[int] = ..., store: _Optional[_Iterable[int]] = ...) -> None: ...

class SimulationV2Data(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    SEASON_FIELD_NUMBER: _ClassVar[int]
    HIGHEST_SCORE_FIELD_NUMBER: _ClassVar[int]
    UPGRADE_FIELD_NUMBER: _ClassVar[int]
    EVENT_POOL_FIELD_NUMBER: _ClassVar[int]
    SEASON_COUNT_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    season: SimulationV2SeasonData
    highest_score: int
    upgrade: SimulationV2Ability
    event_pool: _containers.RepeatedScalarFieldContainer[int]
    season_count: int
    def __init__(self, activity_id: _Optional[int] = ..., season: _Optional[_Union[SimulationV2SeasonData, _Mapping]] = ..., highest_score: _Optional[int] = ..., upgrade: _Optional[_Union[SimulationV2Ability, _Mapping]] = ..., event_pool: _Optional[_Iterable[int]] = ..., season_count: _Optional[int] = ...) -> None: ...

class SimulationV2Effect(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class SimulationV2Event(_message.Message):
    __slots__ = ()
    class SimulationV2EventSelection(_message.Message):
        __slots__ = ()
        class SimulationV2EventResult(_message.Message):
            __slots__ = ()
            ID_FIELD_NUMBER: _ClassVar[int]
            WEIGHT_FIELD_NUMBER: _ClassVar[int]
            id: int
            weight: int
            def __init__(self, id: _Optional[int] = ..., weight: _Optional[int] = ...) -> None: ...
        ID_FIELD_NUMBER: _ClassVar[int]
        RESULTS_FIELD_NUMBER: _ClassVar[int]
        id: int
        results: _containers.RepeatedCompositeFieldContainer[SimulationV2Event.SimulationV2EventSelection.SimulationV2EventResult]
        def __init__(self, id: _Optional[int] = ..., results: _Optional[_Iterable[_Union[SimulationV2Event.SimulationV2EventSelection.SimulationV2EventResult, _Mapping]]] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    SELECTIONS_FIELD_NUMBER: _ClassVar[int]
    NEXT_ROUND_FIELD_NUMBER: _ClassVar[int]
    id: int
    selections: _containers.RepeatedCompositeFieldContainer[SimulationV2Event.SimulationV2EventSelection]
    next_round: int
    def __init__(self, id: _Optional[int] = ..., selections: _Optional[_Iterable[_Union[SimulationV2Event.SimulationV2EventSelection, _Mapping]]] = ..., next_round: _Optional[int] = ...) -> None: ...

class SimulationV2EventHistory(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    ROUND_FIELD_NUMBER: _ClassVar[int]
    id: int
    round: int
    def __init__(self, id: _Optional[int] = ..., round: _Optional[int] = ...) -> None: ...

class SimulationV2Match(_message.Message):
    __slots__ = ()
    class SimulationV2Player(_message.Message):
        __slots__ = ()
        ID_FIELD_NUMBER: _ClassVar[int]
        MAIN_FIELD_NUMBER: _ClassVar[int]
        TING_FIELD_NUMBER: _ClassVar[int]
        SCORE_FIELD_NUMBER: _ClassVar[int]
        FULU_FIELD_NUMBER: _ClassVar[int]
        RIICHI_FIELD_NUMBER: _ClassVar[int]
        FIND_TING_FIELD_NUMBER: _ClassVar[int]
        SEAT_FIELD_NUMBER: _ClassVar[int]
        CON_PUSH_TING_FIELD_NUMBER: _ClassVar[int]
        CON_KEEP_TING_FIELD_NUMBER: _ClassVar[int]
        IPPATSU_FIELD_NUMBER: _ClassVar[int]
        id: int
        main: bool
        ting: int
        score: int
        fulu: int
        riichi: bool
        find_ting: _containers.RepeatedScalarFieldContainer[int]
        seat: int
        con_push_ting: int
        con_keep_ting: int
        ippatsu: bool
        def __init__(self, id: _Optional[int] = ..., main: _Optional[bool] = ..., ting: _Optional[int] = ..., score: _Optional[int] = ..., fulu: _Optional[int] = ..., riichi: _Optional[bool] = ..., find_ting: _Optional[_Iterable[int]] = ..., seat: _Optional[int] = ..., con_push_ting: _Optional[int] = ..., con_keep_ting: _Optional[int] = ..., ippatsu: _Optional[bool] = ...) -> None: ...
    INFO_FIELD_NUMBER: _ClassVar[int]
    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    HISTORY_FIELD_NUMBER: _ClassVar[int]
    RANK_FIELD_NUMBER: _ClassVar[int]
    IS_MATCH_END_FIELD_NUMBER: _ClassVar[int]
    ACTIONS_FIELD_NUMBER: _ClassVar[int]
    BUFF_LIST_FIELD_NUMBER: _ClassVar[int]
    IS_FIRST_ROUND_FIELD_NUMBER: _ClassVar[int]
    LAST_EVENT_REMAIN_FIELD_NUMBER: _ClassVar[int]
    EFFECTED_BUFF_LIST_FIELD_NUMBER: _ClassVar[int]
    TRIGGERED_STORY_FIELD_NUMBER: _ClassVar[int]
    info: SimulationV2MatchInfo
    players: _containers.RepeatedCompositeFieldContainer[SimulationV2Match.SimulationV2Player]
    history: _containers.RepeatedCompositeFieldContainer[SimulationV2MatchHistory]
    rank: _containers.RepeatedScalarFieldContainer[int]
    is_match_end: bool
    actions: _containers.RepeatedCompositeFieldContainer[SimulationActionData]
    buff_list: _containers.RepeatedCompositeFieldContainer[SimulationV2Buff]
    is_first_round: bool
    last_event_remain: int
    effected_buff_list: _containers.RepeatedScalarFieldContainer[int]
    triggered_story: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, info: _Optional[_Union[SimulationV2MatchInfo, _Mapping]] = ..., players: _Optional[_Iterable[_Union[SimulationV2Match.SimulationV2Player, _Mapping]]] = ..., history: _Optional[_Iterable[_Union[SimulationV2MatchHistory, _Mapping]]] = ..., rank: _Optional[_Iterable[int]] = ..., is_match_end: _Optional[bool] = ..., actions: _Optional[_Iterable[_Union[SimulationActionData, _Mapping]]] = ..., buff_list: _Optional[_Iterable[_Union[SimulationV2Buff, _Mapping]]] = ..., is_first_round: _Optional[bool] = ..., last_event_remain: _Optional[int] = ..., effected_buff_list: _Optional[_Iterable[int]] = ..., triggered_story: _Optional[_Iterable[int]] = ...) -> None: ...

class SimulationV2MatchHistory(_message.Message):
    __slots__ = ()
    class RoundStartArgs(_message.Message):
        __slots__ = ()
        INFO_FIELD_NUMBER: _ClassVar[int]
        SCORES_FIELD_NUMBER: _ClassVar[int]
        TING_FIELD_NUMBER: _ClassVar[int]
        EFFECTED_BUFF_LIST_FIELD_NUMBER: _ClassVar[int]
        info: SimulationV2MatchInfo
        scores: _containers.RepeatedScalarFieldContainer[int]
        ting: int
        effected_buff_list: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, info: _Optional[_Union[SimulationV2MatchInfo, _Mapping]] = ..., scores: _Optional[_Iterable[int]] = ..., ting: _Optional[int] = ..., effected_buff_list: _Optional[_Iterable[int]] = ...) -> None: ...
    class RiichiArgs(_message.Message):
        __slots__ = ()
        SEAT_FIELD_NUMBER: _ClassVar[int]
        seat: int
        def __init__(self, seat: _Optional[int] = ...) -> None: ...
    class FuluArgs(_message.Message):
        __slots__ = ()
        SEAT_FIELD_NUMBER: _ClassVar[int]
        TING_FIELD_NUMBER: _ClassVar[int]
        FULU_FIELD_NUMBER: _ClassVar[int]
        seat: int
        ting: int
        fulu: int
        def __init__(self, seat: _Optional[int] = ..., ting: _Optional[int] = ..., fulu: _Optional[int] = ...) -> None: ...
    class HuleArgs(_message.Message):
        __slots__ = ()
        SEAT_FIELD_NUMBER: _ClassVar[int]
        ZIMO_FIELD_NUMBER: _ClassVar[int]
        CHONG_SEAT_FIELD_NUMBER: _ClassVar[int]
        POINT_FIELD_NUMBER: _ClassVar[int]
        FAN_FIELD_NUMBER: _ClassVar[int]
        SCORE_MODIFY_FIELD_NUMBER: _ClassVar[int]
        seat: int
        zimo: bool
        chong_seat: int
        point: int
        fan: int
        score_modify: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, seat: _Optional[int] = ..., zimo: _Optional[bool] = ..., chong_seat: _Optional[int] = ..., point: _Optional[int] = ..., fan: _Optional[int] = ..., score_modify: _Optional[_Iterable[int]] = ...) -> None: ...
    class PushTingArgs(_message.Message):
        __slots__ = ()
        SEAT_FIELD_NUMBER: _ClassVar[int]
        TING_FIELD_NUMBER: _ClassVar[int]
        seat: int
        ting: int
        def __init__(self, seat: _Optional[int] = ..., ting: _Optional[int] = ...) -> None: ...
    class FindTingArgs(_message.Message):
        __slots__ = ()
        SEAT_FIELD_NUMBER: _ClassVar[int]
        TARGET_FIELD_NUMBER: _ClassVar[int]
        seat: int
        target: int
        def __init__(self, seat: _Optional[int] = ..., target: _Optional[int] = ...) -> None: ...
    class LiujuArgs(_message.Message):
        __slots__ = ()
        TING_FIELD_NUMBER: _ClassVar[int]
        ting: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, ting: _Optional[_Iterable[int]] = ...) -> None: ...
    class StoryArgs(_message.Message):
        __slots__ = ()
        STORY_ID_FIELD_NUMBER: _ClassVar[int]
        story_id: int
        def __init__(self, story_id: _Optional[int] = ...) -> None: ...
    TYPE_FIELD_NUMBER: _ClassVar[int]
    REMAIN_FIELD_NUMBER: _ClassVar[int]
    SCORE_MODIFY_FIELD_NUMBER: _ClassVar[int]
    ROUND_START_FIELD_NUMBER: _ClassVar[int]
    RIICHI_FIELD_NUMBER: _ClassVar[int]
    FULU_FIELD_NUMBER: _ClassVar[int]
    HULE_FIELD_NUMBER: _ClassVar[int]
    PUSH_TING_FIELD_NUMBER: _ClassVar[int]
    FIND_TING_FIELD_NUMBER: _ClassVar[int]
    LIUJU_FIELD_NUMBER: _ClassVar[int]
    STORY_FIELD_NUMBER: _ClassVar[int]
    type: int
    remain: int
    score_modify: _containers.RepeatedScalarFieldContainer[int]
    round_start: SimulationV2MatchHistory.RoundStartArgs
    riichi: SimulationV2MatchHistory.RiichiArgs
    fulu: SimulationV2MatchHistory.FuluArgs
    hule: _containers.RepeatedCompositeFieldContainer[SimulationV2MatchHistory.HuleArgs]
    push_ting: SimulationV2MatchHistory.PushTingArgs
    find_ting: SimulationV2MatchHistory.FindTingArgs
    liuju: SimulationV2MatchHistory.LiujuArgs
    story: SimulationV2MatchHistory.StoryArgs
    def __init__(self, type: _Optional[int] = ..., remain: _Optional[int] = ..., score_modify: _Optional[_Iterable[int]] = ..., round_start: _Optional[_Union[SimulationV2MatchHistory.RoundStartArgs, _Mapping]] = ..., riichi: _Optional[_Union[SimulationV2MatchHistory.RiichiArgs, _Mapping]] = ..., fulu: _Optional[_Union[SimulationV2MatchHistory.FuluArgs, _Mapping]] = ..., hule: _Optional[_Iterable[_Union[SimulationV2MatchHistory.HuleArgs, _Mapping]]] = ..., push_ting: _Optional[_Union[SimulationV2MatchHistory.PushTingArgs, _Mapping]] = ..., find_ting: _Optional[_Union[SimulationV2MatchHistory.FindTingArgs, _Mapping]] = ..., liuju: _Optional[_Union[SimulationV2MatchHistory.LiujuArgs, _Mapping]] = ..., story: _Optional[_Union[SimulationV2MatchHistory.StoryArgs, _Mapping]] = ...) -> None: ...

class SimulationV2MatchInfo(_message.Message):
    __slots__ = ()
    CHANG_FIELD_NUMBER: _ClassVar[int]
    JU_FIELD_NUMBER: _ClassVar[int]
    BEN_FIELD_NUMBER: _ClassVar[int]
    GONG_FIELD_NUMBER: _ClassVar[int]
    REMAIN_FIELD_NUMBER: _ClassVar[int]
    chang: int
    ju: int
    ben: int
    gong: int
    remain: int
    def __init__(self, chang: _Optional[int] = ..., ju: _Optional[int] = ..., ben: _Optional[int] = ..., gong: _Optional[int] = ..., remain: _Optional[int] = ...) -> None: ...

class SimulationV2MatchRecord(_message.Message):
    __slots__ = ()
    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    ROUND_FIELD_NUMBER: _ClassVar[int]
    players: _containers.RepeatedCompositeFieldContainer[SimulationV2PlayerRecord]
    round: int
    def __init__(self, players: _Optional[_Iterable[_Union[SimulationV2PlayerRecord, _Mapping]]] = ..., round: _Optional[int] = ...) -> None: ...

class SimulationV2PlayerRecord(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    MAIN_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    RANK_FIELD_NUMBER: _ClassVar[int]
    SEAT_FIELD_NUMBER: _ClassVar[int]
    id: int
    main: bool
    score: int
    rank: int
    seat: int
    def __init__(self, id: _Optional[int] = ..., main: _Optional[bool] = ..., score: _Optional[int] = ..., rank: _Optional[int] = ..., seat: _Optional[int] = ...) -> None: ...

class SimulationV2Record(_message.Message):
    __slots__ = ()
    HU_COUNT_FIELD_NUMBER: _ClassVar[int]
    CHONG_COUNT_FIELD_NUMBER: _ClassVar[int]
    HIGHEST_HU_FIELD_NUMBER: _ClassVar[int]
    RANK_FIELD_NUMBER: _ClassVar[int]
    ROUND_COUNT_FIELD_NUMBER: _ClassVar[int]
    hu_count: int
    chong_count: int
    highest_hu: int
    rank: _containers.RepeatedScalarFieldContainer[int]
    round_count: int
    def __init__(self, hu_count: _Optional[int] = ..., chong_count: _Optional[int] = ..., highest_hu: _Optional[int] = ..., rank: _Optional[_Iterable[int]] = ..., round_count: _Optional[int] = ...) -> None: ...

class SimulationV2SeasonData(_message.Message):
    __slots__ = ()
    ROUND_FIELD_NUMBER: _ClassVar[int]
    ABILITY_FIELD_NUMBER: _ClassVar[int]
    EFFECT_LIST_FIELD_NUMBER: _ClassVar[int]
    MATCH_FIELD_NUMBER: _ClassVar[int]
    EVENT_FIELD_NUMBER: _ClassVar[int]
    EVENT_HISTORY_FIELD_NUMBER: _ClassVar[int]
    RECORD_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SCORE_FIELD_NUMBER: _ClassVar[int]
    MATCH_HISTORY_FIELD_NUMBER: _ClassVar[int]
    round: int
    ability: SimulationV2Ability
    effect_list: _containers.RepeatedCompositeFieldContainer[SimulationV2Effect]
    match: SimulationV2Match
    event: SimulationV2Event
    event_history: _containers.RepeatedCompositeFieldContainer[SimulationV2EventHistory]
    record: SimulationV2Record
    total_score: int
    match_history: _containers.RepeatedCompositeFieldContainer[SimulationV2MatchRecord]
    def __init__(self, round: _Optional[int] = ..., ability: _Optional[_Union[SimulationV2Ability, _Mapping]] = ..., effect_list: _Optional[_Iterable[_Union[SimulationV2Effect, _Mapping]]] = ..., match: _Optional[_Union[SimulationV2Match, _Mapping]] = ..., event: _Optional[_Union[SimulationV2Event, _Mapping]] = ..., event_history: _Optional[_Iterable[_Union[SimulationV2EventHistory, _Mapping]]] = ..., record: _Optional[_Union[SimulationV2Record, _Mapping]] = ..., total_score: _Optional[int] = ..., match_history: _Optional[_Iterable[_Union[SimulationV2MatchRecord, _Mapping]]] = ...) -> None: ...

class StringArrayDirty(_message.Message):
    __slots__ = ()
    DIRTY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    dirty: bool
    value: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, dirty: _Optional[bool] = ..., value: _Optional[_Iterable[str]] = ...) -> None: ...

class StringDirty(_message.Message):
    __slots__ = ()
    DIRTY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    dirty: bool
    value: str
    def __init__(self, dirty: _Optional[bool] = ..., value: _Optional[str] = ...) -> None: ...

class TaskProgress(_message.Message):
    __slots__ = ()
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
    def __init__(self, id: _Optional[int] = ..., counter: _Optional[int] = ..., achieved: _Optional[bool] = ..., rewarded: _Optional[bool] = ..., failed: _Optional[bool] = ..., rewarded_time: _Optional[int] = ...) -> None: ...

class TimeCounterData(_message.Message):
    __slots__ = ()
    COUNT_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    count: int
    update_time: int
    def __init__(self, count: _Optional[int] = ..., update_time: _Optional[int] = ...) -> None: ...

class TingPaiDiscardInfo(_message.Message):
    __slots__ = ()
    TILE_FIELD_NUMBER: _ClassVar[int]
    ZHENTING_FIELD_NUMBER: _ClassVar[int]
    INFOS_FIELD_NUMBER: _ClassVar[int]
    tile: str
    zhenting: bool
    infos: _containers.RepeatedCompositeFieldContainer[TingPaiInfo]
    def __init__(self, tile: _Optional[str] = ..., zhenting: _Optional[bool] = ..., infos: _Optional[_Iterable[_Union[TingPaiInfo, _Mapping]]] = ...) -> None: ...

class TingPaiInfo(_message.Message):
    __slots__ = ()
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
    def __init__(self, tile: _Optional[str] = ..., haveyi: _Optional[bool] = ..., yiman: _Optional[bool] = ..., count: _Optional[int] = ..., fu: _Optional[int] = ..., biao_dora_count: _Optional[int] = ..., yiman_zimo: _Optional[bool] = ..., count_zimo: _Optional[int] = ..., fu_zimo: _Optional[int] = ...) -> None: ...

class TransparentData(_message.Message):
    __slots__ = ()
    METHOD_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    SESSION_FIELD_NUMBER: _ClassVar[int]
    REMOTE_FIELD_NUMBER: _ClassVar[int]
    method: str
    data: bytes
    session: str
    remote: NetworkEndpoint
    def __init__(self, method: _Optional[str] = ..., data: _Optional[bytes] = ..., session: _Optional[str] = ..., remote: _Optional[_Union[NetworkEndpoint, _Mapping]] = ...) -> None: ...

class UInt32ArrayDirty(_message.Message):
    __slots__ = ()
    DIRTY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    dirty: bool
    value: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, dirty: _Optional[bool] = ..., value: _Optional[_Iterable[int]] = ...) -> None: ...

class UInt32Dirty(_message.Message):
    __slots__ = ()
    DIRTY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    dirty: bool
    value: int
    def __init__(self, dirty: _Optional[bool] = ..., value: _Optional[int] = ...) -> None: ...

class UnlockedStoryData(_message.Message):
    __slots__ = ()
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

class ViewSlot(_message.Message):
    __slots__ = ()
    SLOT_FIELD_NUMBER: _ClassVar[int]
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ITEM_ID_LIST_FIELD_NUMBER: _ClassVar[int]
    slot: int
    item_id: int
    type: int
    item_id_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, slot: _Optional[int] = ..., item_id: _Optional[int] = ..., type: _Optional[int] = ..., item_id_list: _Optional[_Iterable[int]] = ...) -> None: ...

class VillageBuildingData(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    REWARD_FIELD_NUMBER: _ClassVar[int]
    WORKERS_FIELD_NUMBER: _ClassVar[int]
    id: int
    reward: _containers.RepeatedCompositeFieldContainer[VillageReward]
    workers: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, id: _Optional[int] = ..., reward: _Optional[_Iterable[_Union[VillageReward, _Mapping]]] = ..., workers: _Optional[_Iterable[int]] = ...) -> None: ...

class VillageReward(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    id: int
    count: int
    def __init__(self, id: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class VillageTargetInfo(_message.Message):
    __slots__ = ()
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

class VillageTaskData(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_COUNT_FIELD_NUMBER: _ClassVar[int]
    id: int
    completed_count: int
    def __init__(self, id: _Optional[int] = ..., completed_count: _Optional[int] = ...) -> None: ...

class VillageTripData(_message.Message):
    __slots__ = ()
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

class VoteData(_message.Message):
    __slots__ = ()
    ACTIVITY_ID_FIELD_NUMBER: _ClassVar[int]
    VOTE_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    activity_id: int
    vote: int
    count: int
    def __init__(self, activity_id: _Optional[int] = ..., vote: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class Wrapper(_message.Message):
    __slots__ = ()
    NAME_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    name: str
    data: bytes
    def __init__(self, name: _Optional[str] = ..., data: _Optional[bytes] = ...) -> None: ...

class XiaKeShangInfo(_message.Message):
    __slots__ = ()
    SCORE_COEFFICIENTS_FIELD_NUMBER: _ClassVar[int]
    score_coefficients: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, score_coefficients: _Optional[_Iterable[int]] = ...) -> None: ...

class YongchangInfo(_message.Message):
    __slots__ = ()
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

class ZHPShop(_message.Message):
    __slots__ = ()
    class RefreshCount(_message.Message):
        __slots__ = ()
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

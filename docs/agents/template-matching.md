# テンプレート照合設計メモ

この文書は、`LoginScreen` 到達判定に必要なテンプレート照合の設計メモです。
`LoginScreen.enter_email_address()` はまだ実装しません。まず、スクリーンショットが
対象画面に到達しているかを判定するための画像照合だけを実装対象にします。

## 目的

- 画面到達判定を synthetic screenshot で自動テストできるようにする
- 実スクリーンショット画像やテンプレート画像は、必要になった時点でユーザーに
  コミットを依頼する
- 将来のクリック操作でも使えるよう、画面上の矩形領域を共通表現にする
- テンプレート照合しない決め打ちクリックでも同じ `Region` を使えるようにする

## 依存

画像処理は OpenCV と numpy を使います。テストのためだけに Pillow は追加しません。

OpenCV と numpy は RPAApp 側の画像照合で必要になるため、`rpa` extra の
optional dependency として扱います。core import だけで OpenCV と numpy を
読み込まないようにします。

## Region

`Region` は画面上の矩形領域を表す実行時の値オブジェクトです。
テンプレート照合なしに決め打ちの定数領域として使うこともあるため、
`presentation.template` ではなく `presentation.region` に置きます。

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Region:
    left: float
    top: float
    width: float
    height: float

    @property
    def right(self) -> float:
        return self.left + self.width

    @property
    def bottom(self) -> float:
        return self.top + self.height
```

方針:

- `Region` は immutable な dataclass にする
- TOML 入力の validation は pydantic model で行い、実行時値として `Region` に変換する
- `left` と `top` は screenshot 全体座標系の左上座標とする
- `width` と `height` は矩形サイズとする
- クリック、入力欄探索、テンプレート照合結果、固定領域指定で同じ型を使う
- 領域内のクリック点サンプリングは `Region.random_point()` として提供する
- ランダムサンプリングはテストしやすいように `random.Random` を注入可能にする

## TOML 設定

テンプレートごとに `.toml` を置きます。テンプレート画像と `.toml` は対で扱います。
テンプレート画像は 1920x1080 の screenshot から切り出したものを基準にします。
TOML の `region` と `margin` も 1920x1080 基準の座標で記述します。

```toml
[region]
left = 100
top = 200
width = 320
height = 80

[margin]
top = 4
right = 4
bottom = 4
left = 4

[match]
threshold = 0.92
```

意味:

- `region`: テンプレートが本来ある想定位置
- `margin`: 位置ずれを許容する探索余白
- `threshold`: `cv2.matchTemplate` の最大スコアがこの値以上なら一致

探索領域は `region` を `margin` 分だけ拡張した矩形です。テンプレート画像のサイズは
`region.width x region.height` と一致させます。不一致の場合、黙って resize せず
設定または資産の不整合として例外にします。

## ビューポートスケーリング

基準座標系は 1920x1080 です。

```python
from majsoulrpa.constants import BASE_VIEWPORT_HEIGHT, BASE_VIEWPORT_WIDTH
```

720p と 1440p はスケーリングで対応します。

- 1280x720 screenshot: scale は `2 / 3`
- 1920x1080 screenshot: scale は `1`
- 2560x1440 screenshot: scale は `4 / 3`

`TemplateMatcher` は screenshot サイズから scale を求め、`region`、`margin`、
template image を同じ倍率で扱います。template image は 1920x1080 基準の画像なので、
720p screenshot に照合する場合は縮小し、1440p screenshot に照合する場合は拡大してから
`cv2.matchTemplate` に渡します。

`scale_x = screenshot_width / 1920`、`scale_y = screenshot_height / 1080` とし、
原則として `scale_x == scale_y` を要求します。異なる場合はアスペクト比不一致として
例外にします。許容誤差が必要かどうかは、最初の実装時にテストで固定します。

丸め規則:

- left と top はそれぞれ scale して `round()` する
- width と height は、元の矩形サイズを scale して `round()` する
- scale 後の width または height が 0 以下になる場合は例外にする

探索領域も同じ規則で scale します。端点を別々に丸めてから差分を取ると、
left/top の丸め誤差が width/height に混ざります。このプロジェクトでは
`Region.width` と `Region.height` の意味を保つため、引き算して得たサイズを
scale してから丸めます。

`TemplateMatchResult.region` は実 screenshot 座標系で返します。後続のクリック処理で
そのまま使えるようにするためです。

## 設定モデル

TOML 入力には pydantic model を使います。

```python
class RegionConfig(BaseModel):
    left: NonNegativeFloat
    top: NonNegativeFloat
    width: PositiveFloat
    height: PositiveFloat

    def to_region(self) -> Region: ...


class MarginConfig(BaseModel):
    top: NonNegativeFloat
    right: NonNegativeFloat
    bottom: NonNegativeFloat
    left: NonNegativeFloat


class TemplateMatchSettings(BaseModel):
    region: RegionConfig
    margin: MarginConfig
    threshold: float
```

制約:

- unknown key は reject する
- `left` と `top` は `>= 0`
- `width` と `height` は `> 0`
- margin はすべて `>= 0`
- threshold は `0.0 <= threshold <= 1.0`

## 照合結果

テンプレート照合の戻り値は score と `Region` を持ちます。

```python
@dataclass(frozen=True)
class TemplateMatchResult:
    score: float
    region: Region
```

`region.left` と `region.top` は、探索領域内の相対座標ではなく screenshot 全体座標系の
match 左上座標です。`region.width` と `region.height` は scale 後のテンプレート画像
サイズです。いずれも実 screenshot 座標系の値です。

## 照合 API

内部 API は小さく保ちます。

```python
class TemplateMatcher:
    def __init__(
        self,
        template: np.ndarray,
        settings: TemplateMatchSettings,
    ) -> None: ...

    def match(self, screenshot: np.ndarray) -> TemplateMatchResult: ...

    def matches(self, screenshot: np.ndarray) -> bool: ...
```

挙動:

- `match()` は `cv2.matchTemplate(..., cv2.TM_CCOEFF_NORMED)` を使う
- `match()` は threshold 未満でも最良候補を `TemplateMatchResult` として返す
- `matches()` は `match().score >= settings.threshold` を返す
- template size と `settings.region` size が違う場合は例外にする
- screenshot サイズに合わせて template、region、margin を scale する
- 720p、1080p、1440p の screenshot に対応する
- screenshot のアスペクト比が 16:9 でない場合は例外にする
- scale 後の template または search region のサイズが 0 以下になる場合は例外にする
- screenshot が探索領域を満たさない場合は例外にする
- 単純な不一致は `False` として扱う
- 設定不備、画像サイズ不整合、読み込み失敗は例外として見えるようにする

画像は `np.ndarray` を受けます。最初は synthetic な `uint8` array でテストします。
channel 数や dtype の扱いは、最初の実装時にテストで固定します。

## LoginScreen との接続

`LoginScreen` は `detection_spec()` で template predicate を返します。

```python
class LoginScreen(Screen):
    @classmethod
    @override
    def detection_spec(cls) -> ScreenDetectionSpec:
        return ScreenDetectionSpec(predicate=_login_template_matches)
```

`_login_template_matches()` は `TemplateMatcher` を使います。テンプレート画像と TOML を
毎回読み込まないように、実装時は module-level の遅延 cache などを検討します。

実テンプレート画像と TOML は、必要になった時点でユーザーにコミットを依頼します。
初期実装では synthetic numpy array だけで照合ロジックを固定します。

## TDD 順序

1. TOML から `TemplateMatchSettings` を読める
2. unknown key を reject する
3. region、margin、threshold の不正値を reject する
4. `RegionConfig.to_region()` が immutable な `Region` を返す
5. `Region.right` と `Region.bottom` が計算される
6. template size と region size が違うと例外
7. 1920x1080 screenshot では scale 1 で照合する
8. 1280x720 screenshot では template、region、margin を `2 / 3` に scale して照合する
9. 2560x1440 screenshot では template、region、margin を `4 / 3` に scale して照合する
10. アスペクト比が 16:9 でない screenshot は例外
11. fake `np.ndarray` screenshot の指定 region が一致したら `matches()` が true
12. `match()` が `score` と実 screenshot 座標系の `Region` を返す
13. margin 内でずれたテンプレートも match し、ずれた `Region` を返す
14. threshold 未満なら `matches()` が false
15. screenshot が探索領域より小さい場合は例外
16. `LoginScreen.detection_spec()` が template predicate を返す

この段階では `LoginScreen.enter_email_address()` は実装しません。

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

現時点では OpenCV と numpy は通常 dependency として扱います。browser 実装後に
optional dependency へ移すかどうかを再検討します。

## Region

`Region` は画面上の矩形領域を表す実行時の値オブジェクトです。

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

## TOML 設定

テンプレートごとに `.toml` を置きます。テンプレート画像と `.toml` は対で扱います。

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
match 左上座標です。`region.width` と `region.height` はテンプレート画像サイズです。

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
7. fake `np.ndarray` screenshot の指定 region が一致したら `matches()` が true
8. `match()` が `score` と `Region` を返す
9. margin 内でずれたテンプレートも match し、ずれた `Region` を返す
10. threshold 未満なら `matches()` が false
11. screenshot が探索領域より小さい場合は例外
12. `LoginScreen.detection_spec()` が template predicate を返す

この段階では `LoginScreen.enter_email_address()` は実装しません。

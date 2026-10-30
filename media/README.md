# media/

本地媒体放在这里。没有文件时页面照常运行：对应的音乐保持静音，视频节拍显示同风格的说明卡。

## 年代音乐 `media/music/`

| 文件名 | 曲目 | 用在 | 建议从哪里进 |
| --- | --- | --- | --- |
| `01-i-want-you-back.mp3` | I Want You Back（The Jackson 5，1969） | I 加里 | 前奏钢琴滑音 |
| `02-dont-stop-til-you-get-enough.mp3` | Don't Stop 'Til You Get Enough（1979） | II Off the Wall | 贝斯律动 |
| `03-billie-jean.mp3` | Billie Jean（1983） | III Thriller | 鼓与贝斯前奏 |
| `04-bad.mp3` | Bad（1987） | IV Bad | 前奏；MV 播放时自动让位 |
| `05-black-or-white.mp3` | Black or White（1991） | V Dangerous | 吉他前奏；静止计时器启动时切断 |
| `06-stranger-in-moscow.mp3` | Stranger in Moscow（1996） | VI 阴影 | 压到几乎听不见 |
| `07-earth-song.mp3` | Earth Song（1995） | 间奏 首尔 | 钢琴前奏 |
| `08-human-nature.mp3` | Human Nature（1982） | VII This Is It | 「2009. 6. 25」出现时切断 |
| `09-remember-the-time.mp3` | Remember the Time（1992） | VIII 遗产 | 随场灯渐亮升起 |
| `10-man-in-the-mirror.mp3` | Man in the Mirror（1988） | 终幕 | 光转向观众时推到最高 |

这些文件是可选的：没有本地文件时，页面自动改用 YouTube 上的官方音源（ID 写在 `index.html` 的 `TRACKS` 里）。本地文件的好处是没有广告、不依赖教室网络。

每首歌的起点（秒）在 设置 → 视频与音乐 里填写；点「试听 8 秒」时可以用「记当前为起点」一键记录。

## 照片 `media/photos/`

六张迈克尔本人的照片，全部来自 Wikimedia Commons，标为公有领域或 CC 许可。页面按这个顺序找照片：

1. 这个文件夹里的同名文件（离线、以及 claude.ai 预览页里都能显示）
2. Commons 上的原图（GitHub Pages 和本机打开时自动加载）
3. 都没有时照片不出现，画面保持插画版

| 文件名 | 用在 | Commons 文件 | 作者 · 许可 |
| --- | --- | --- | --- |
| `1969-jackson-5.jpg` | I 加里 ② | [Jackson_5_1969.jpg](https://commons.wikimedia.org/wiki/File:Jackson_5_1969.jpg) | Bernie Ilson, Inc. · 公有领域 |
| `1969-michael.jpg` | I 加里 ③ | [Michael_Jackson_1969.jpg](https://commons.wikimedia.org/wiki/File:Michael_Jackson_1969.jpg) | Bernie Ilson, Inc. · 公有领域 |
| `1983-michael.jpg` | III Thriller ④ | [Michael_Jackson_1983.jpg](https://commons.wikimedia.org/wiki/File:Michael_Jackson_1983.jpg) | Epic Records · 公有领域 |
| `1984-white-house.jpg` | III Thriller ⑥ | [Michael_Jackson_1984.jpg](https://commons.wikimedia.org/wiki/File:Michael_Jackson_1984.jpg) | White House Photo Office · 公有领域 |
| `1988-bad-tour-vienna.jpg` | IV Bad ② | [Michael_Jackson_in_1988.jpg](https://commons.wikimedia.org/wiki/File:Michael_Jackson_in_1988.jpg) | Zoran Veselinović · CC BY-SA 2.0 |
| `1992-dangerous-tour-bucharest.jpg` | V Dangerous ③ | [Michael_Jackson_Live_in_Bucharest_1992_Toni_Salabasev.jpg](https://commons.wikimedia.org/wiki/File:Michael_Jackson_Live_in_Bucharest_1992_Toni_Salabasev.jpg) | Toni Salabasev · CC BY-SA 4.0 |

每张照片的相纸下方都印着作者和许可，CC 许可要求的署名就在画面上。想换成别的照片，用同样的文件名放进来即可（页面会裁成竖幅或横幅相纸，人脸默认在上方三分之一）；用 Commons 以外的照片时，许可请自己确认。

## 本地视频（可选）`media/video/`

预告片、Smooth Criminal、Motown 25 片段也可以用本地 mp4 / webm 文件代替 YouTube：把路径（例如 `media/video/trailer.mp4`）填进设置里对应的链接栏即可。网络不稳定的教室里，这样最保险。

> 注意：公开仓库开启 GitHub Pages 后，这个文件夹里的文件会被公开访问。受版权保护的音频和视频建议只放在演讲用的那台电脑上（用 `python3 -m http.server` 本地打开），不要提交到公开仓库。


## 本地视频：在页面里离线播放（推荐）

点 MV 开关或按 V 时，页面先找下面这些本地文件，找到就在页面里的播放窗口直接播放，不经过任何网站；找不到才用嵌入的播放器。也可以用 `.webm`。

**这些文件需要你自己准备**（自己购买 / 有授权的版本）。它们受版权保护，`.gitignore` 已经把 `media/mv/` 和 `media/video/` 排除在外：只放在演讲用的电脑上，用 `python3 -m http.server` 在本机打开，不要上传到公开仓库。

### 每部作品的 MV `media/mv/`

| 文件名 | 作品 | 年份 |
| --- | --- | --- |
| `media/mv/iwyb.mp4` | I Want You Back | 1969 |
| `media/mv/abc.mp4` | ABC | 1970 |
| `media/mv/loveyousave.mp4` | The Love You Save | 1970 |
| `media/mv/illbethere.mp4` | I'll Be There | 1970 |
| `media/mv/dstyge.mp4` | Don't Stop 'Til You Get Enough | 1979 |
| `media/mv/rockwithyou.mp4` | Rock with You | 1979 |
| `media/mv/offthewall.mp4` | Off the Wall | 1979 |
| `media/mv/shesout.mp4` | She's Out of My Life | 1979 |
| `media/mv/wbss.mp4` | Wanna Be Startin' Somethin' | 1982 |
| `media/mv/thriller.mp4` | Thriller | 1983 |
| `media/mv/billiejean.mp4` | Billie Jean | 1983 |
| `media/mv/beatit.mp4` | Beat It | 1983 |
| `media/mv/motown25.mp4` | Billie Jean · Motown 25 | 1983 |
| `media/mv/ijcslu.mp4` | I Just Can't Stop Loving You | 1987 |
| `media/mv/bad.mp4` | Bad | 1987 |
| `media/mv/twymmf.mp4` | The Way You Make Me Feel | 1987 |
| `media/mv/mitm.mp4` | Man in the Mirror | 1988 |
| `media/mv/dirtydiana.mp4` | Dirty Diana | 1988 |
| `media/mv/smooth.mp4` | Smooth Criminal | 1988 |
| `media/mv/bow.mp4` | Black or White | 1991 |
| `media/mv/rtt.mp4` | Remember the Time | 1992 |
| `media/mv/superbowl.mp4` | Super Bowl XXVII Halftime | 1993 |
| `media/mv/earth.mp4` | Earth Song | 1995 |
| `media/mv/moscow.mp4` | Stranger in Moscow | 1996 |
| `media/mv/tdcau.mp4` | They Don't Care About Us | 1996 |
| `media/mv/human.mp4` | Human Nature | 1982 |
| `media/mv/thisisit.mp4` | Michael Jackson's This Is It | 2009 |
| `media/mv/michael.mp4` | Michael (2026) — Official Trailer | 2026 |

### 排好的视频 `media/video/`

| 文件名 | 用在 |
| --- | --- |
| `media/video/trailer.mp4` | 第 1 场 ② 预告片（银幕 → 整屏 → 银幕） |
| `media/video/sc.mp4` | 第 6 场 ④⑤ Smooth Criminal 提示点 |
| `media/video/bj.mp4` | 第 5 场 ③ 显像管电视（摩城 25 现场） |
| `media/video/motown.mp4` | 第 5 场 ⑤ 摩城 25 片段 |

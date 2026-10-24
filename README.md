# 竹林七贤与荣启期 · 错版拼砖画数字展厅

南京六朝博物馆《竹林七贤与荣启期》错版拼砖画科普数字展厅，纯前端、**全本地化、零境外网络依赖**，国内网络直开即丝滑流畅。

## 在线访问

- **GitHub Pages**：仓库合并到 Pages 后，通过 `https://<用户名>.github.io/ZHULINQIXIAN/` 在手机 / 电脑浏览器直接打开。
- 本地打开：双击 `启动预览.bat`（或 `python run_local.py --open`），浏览器进入 `http://127.0.0.1:8000/puzzle.html`。

## 页面

| 页面 | 说明 |
| ---- | ---- |
| `index.html` | 首页：大图、金色粒子/丝带光效、七贤名录（8 张工笔画像卡片，点击进入对话）、观展信息 |
| `dialogue.html?sage=<slug>` | 沉浸式互动对话：开场 → 选择 → 回应 → 故事深化 → 选择 → 回应 → 结语 + 解锁知识卡，8 位人物 |
| `puzzle.html` | 拼图游戏：鼠标 / 触屏 / **摄像头手势**（MediaPipe 本地推理引擎）三种操作 |

`?sage=` 取值：`ji-kang`（嵇康）、`ruan-ji`（阮籍）、`shan-tao`（山涛）、`wang-rong`（王戎）、`xiang-xiu`（向秀）、`liu-ling`（刘伶）、`ruan-xian`（阮咸）、`rong-qiqi`（荣启期）。

## 特性

- **国内网络友好**：字体（Noto Serif/Sans SC、JetBrains Mono）全部本地化在 `assets/fonts/`，无 Google Fonts 外链；运行期零外网请求。
- **摄像头手势全本地**：MediaPipe Tasks Vision 引擎 + WASM + `hand_landmarker.task` 均在 `assets/mediapipe/` 与 `assets/`，摄像头 `getUserMedia` 需 `http`/`https` 环境；内置预览 iframe 未授予摄像头权限时自动回退到鼠标手势模式。
- 响应式布局，手机 / 电脑均可流畅操作。

## 目录结构

```
index.html      首页
dialogue.html   互动对话页
puzzle.html     拼图游戏页
run_local.py    本地静态服务器（--open / --port）
启动预览.bat      双击即用本地预览入口
assets/
  hero-combined.png      拼砖画大图（拼图背景与参考图）
  portraits/*.png        8 张工笔重彩人物画像
  mediapipe/             本地 MediaPipe 引擎（vision_bundle.mjs + wasm/）
  hand_landmarker.task   本地手势识别模型
  fonts/                 本地化字体（woff2 + fonts.css）
CHANGELOG.md    版本记录
```

## 运行本地服务器

```bash
# 方式一：双击 启动预览.bat
# 方式二：终端
python run_local.py --open
# 打开 http://127.0.0.1:8000/
```

## 版本

采用 Git + `CHANGELOG.md` + 语义化 tag（当前 v5.5）。详见 `CHANGELOG.md`。

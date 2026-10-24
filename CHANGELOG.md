# 变更日志

## v5.7 - 2026-10-24 17:20
- 修复"打开线上链接图片加载不出来"：把**所有图片直接打包进 HTML**（base64 内嵌），弱网 / 图片资源请求失败时也能秒开：
  - 用 Pillow 压缩：`hero-combined` 1400px JPEG q85（2.9MB→352KB），8 张人物画像 720px JPEG q82（~1.5MB/张→~115KB/张）
  - `index.html` / `puzzle.html` / `dialogue.html` 的 `<img src>` 与 CSS `background-image` 全部替换为 `data:image/jpeg;base64` 内嵌
  - `dialogue.html` 的动态画像路径改为 `portraitSrc(slug)` 查表（内嵌数据优先，缺 slug 时回退文件路径）
  - 无头浏览器实测：4 个页面**图片网络请求 = 0**，所有图片走内嵌 data URI
  - 代价：HTML 体积增大（index ~2MB / puzzle ~1.4MB / dialogue ~1.5MB），但换来零外部图片依赖
- 变更文件：`index.html`、`puzzle.html`、`dialogue.html`

## v5.6 - 2026-10-24 14:25
- 全面本地化字体、**移除 Google Fonts 外链**，国内网络零境外依赖、打开丝滑：
  - 下载 Noto Serif SC / Noto Sans SC / JetBrains Mono 全量 woff2 切片（208 个，约 10MB）到 `assets/fonts/`，生成本地 `assets/fonts/fonts.css`（618 个 `@font-face`，全部 `font-display: swap`，`url()` 改相对路径）
  - `index.html` / `puzzle.html` / `dialogue.html` 删除 `fonts.googleapis.com` 与 `fonts.gstatic.com` 的 preconnect + `<link>`，改为引用本地 `assets/fonts/fonts.css`
  - 无头浏览器验证：三个页面**外部网络请求为 0**，字体正常渲染
- 对话界面放大铺满全屏、字体加大：`.stage` 加宽并 `min-height` 撑满视口，气泡/选项/按钮/知识卡/头像字号同步放大
- 新增 `README.md`（在线访问 / 本地运行 / 目录结构 / 特性说明）
- 变更文件：`assets/fonts/*`（新增）、`index.html`、`puzzle.html`、`dialogue.html`、`README.md`、`CHANGELOG.md`

## v5.5 - 2026-10-21 14:50
- 按《人物对话.docx》重新实现"七贤与荣启期"名录的沉浸式互动对话功能（此前 v5.3 曾移除该功能）：
  - 新增 `dialogue.html`：读取 `?sage=` 参数，展示对应人物画像 + 性格 + 场景，按"开场 → 选择一 → 回应 → 故事深化 → 选择二 → 回应 → 结语 → 解锁知识卡"的七步状态机推进，对话进度点、人物/用户双色气泡、选项 A/B(/C) 按钮、"再听一次/与下一位对话/返回名录"操作
  - 八位人物脚本全部录入（嵇康·临刑奏琴、阮籍·穷途之哭、山涛·举荐嵇康、刘伶·荷锸随酒、阮咸·竹竿晒衣、向秀·闻笛思旧、王戎·道旁苦李、荣启期·荣公三乐），荣启期额外附"文化说明"时代局限提示
  - 未带 `?sage=` 或参数无效时给出"未找到名士"回退页
  - `index.html` 名录 8 张画像卡片重新包回 `<a href="dialogue.html?sage=...">`，恢复"💬 与XX对话"角标与"点击任意人物"提示
- 变更文件：`dialogue.html`（新增）、`index.html`、`CHANGELOG.md`

## v5.4 - 2026-10-17 16:55
- 解决"网址打不开、摄像头开不了"的落地问题——用户环境没有可用的系统 Python（PATH 中 `python` 是 WindowsApps 空壳），此前只能靠终端手动跑 `run_local.py`，实际难以启动：
  - 新增双击即用入口 `启动预览.bat`：自动探测 Python（`py` launcher → 系统 `python` → WorkBuddy 内置 `.workbuddy/binaries/python/versions/*/python.exe`），启动服务器并自动在浏览器打开拼图页；纯 ASCII 无 BOM，GBK/ANSI 系统均兼容
  - `run_local.py` 增强：支持 `--open`（启动后自动打开浏览器到 `puzzle.html`）与 `--port`（端口被占用时换端口）
  - 已用无头 Chrome + 假摄像头在 `http://127.0.0.1:8000/puzzle.html` 实测：本地模型加载成功、摄像头成功进入"摄像头模式"，全链路可用
- 变更文件：`启动预览.bat`（新增）、`run_local.py`

## v5.3 - 2026-10-17 14:30
- 删除首页"七贤与荣启期"名录的对话功能：
  - 移除 8 张画像卡片的外层 `<a href="dialogue.html?sage=...">` 链接与"💬 与 XX 对话"角标、"点击任意人物…"提示文案
  - 清理不再使用的 CSS（`a.sage-card-link` / `.sage-talk` / `.sage-hint`）；画像卡片保留为静态展示
  - 卡片区块重新规整缩进
- 摄像头手势"开不起来"排查与加固（`puzzle.html`）：
  - 用无头 Chrome + 假摄像头实测整条链路（引擎/模型/`getUserMedia`）：本地模型 `hand_landmarker.task` 合法、`vision_bundle.mjs` 无外网依赖，摄像头成功进入"摄像头模式"——**代码本身无回归**
  - 根因确认：WorkBuddy 内置预览是 iframe，Permission Policy 未授予摄像头，`getUserMedia` 必被拦截；真实摄像头只能在独立标签页 / `http://127.0.0.1` 下使用
  - 加固：所有"摄像头不可用"分支（iframe / file:// / 拒绝 / 占用 / 通用）统一附"本机 `python run_local.py` → 独立标签打开 http://127.0.0.1:8000/puzzle.html 并允许摄像头"的可操作指引
- 变更文件：`index.html`、`puzzle.html`

## v5.2 - 2026-10-10 16:40
- 手势操作说明不再悬浮在拼图框左上角（绝对定位会遮挡碎片）：
  - `board-area` 改为左右 flex 布局：手势说明面板移到拼图**左侧**的独立列（`flex: 0 0 200px`，顶部对齐），拼图占剩余宽度
  - 面板由 `position: absolute`（z-index 50 覆盖碎片）改为静态独立卡片，`pointer-events` 不再拦截碎片拖拽
  - 窄屏（≤1100px）时自动改为拼图**上方**的横向排列
- 变更文件：`puzzle.html`

## v5.1 - 2026-10-10 15:50
- 修复"摄像头无法开启"的根本原因——本地手势模型文件损坏：
  - 用无头 Chrome（`--use-fake-device-for-media-stream`）实测整条链路，定位到 `createFromOptions` 阶段报 `Unable to open zip archive`
  - 根因：`assets/hand_landmarker.task` 头部多了 2 个空字节、且缺 zip 结束符（EOCD），MediaPipe 严格 zip 解析器拒绝加载 → 模型初始化失败 → 整条摄像头链路降级到鼠标模式
  - 修复：解包出两个 tflite（hand_detector / hand_landmarks_detector）后用 Python zipfile 重新打包成干净的 `.task`（PK 开头 + EOCD 完整 + 2 条目），无头测试 `step3 OK via GPU` 通过
- `puzzle.html` 将"模型初始化"与"开启摄像头"拆成两个独立阶段，各自 try/catch，避免模型报错被误报为"摄像头失败"；模型损坏时给出可操作的重下载指引
- 变更文件：`assets/hand_landmarker.task`（重打包）、`puzzle.html`

## v5.0 - 2026-10-10 15:00
- 首页"七贤名录"新增人物画像：
  - 用文生图生成 8 幅风格统一的工笔重彩画像（深绿衣·金边·松竹背景），存放于 `assets/portraits/`
  - 名录区块由纯文字标签改为画像卡片网格：画像 + 姓名/拼音 + 性格标签 + 简介，悬停放大
- 强化 WorkBuddy 内置预览下的摄像头手势可用性（`puzzle.html`）：
  - 精确诊断摄像头被阻断原因：内置预览 iframe 未授予摄像头权限（Permission Policy）/ 用户拒绝 / 无设备 / 设备占用
  - 内置预览 iframe 无摄像头权限时：自动切到鼠标手势兜底，并明确提示 + 提供"📷 在浏览器中打开"按钮（独立标签页可正常用摄像头）
  - 摄像头成功时仍走本地 MediaPipe 模型真实手势
- 变更文件：`index.html`、`puzzle.html`、`assets/portraits/*.png`（新增 8 张）

## v4.3 - 2026-10-10 14:18
- 让内置右侧预览也能开箱即用，新增"双通道手势"：
  - 摄像头可用时（HTTP/localhost/https）仍走 MediaPipe 本地模型识别真实手势
  - 摄像头不可用时（`file://` 双击打开、嵌入预览被拦截等）自动回退到**鼠标手势模式**：按下=食指选中、拖动=手掌移动、松开=握拳嵌入，虚拟光标跟随鼠标
  - 摄像头 `getUserMedia` 抛错时也会自动降级到鼠标手势，保证任何预览环境都能操作
  - 参考图面板与页面说明补充了鼠标手势回退的提示文案
- 变更文件：`puzzle.html`

## v4.2 - 2026-10-04 21:35
- 手势模型完全本地化，运行期不再依赖任何境外 CDN，国内任何环境均可正常运行：
  - 下载 `assets/mediapipe/vision_bundle.mjs`（134KB ESM 模块）
  - 下载 `assets/mediapipe/wasm/vision_wasm_internal.js`（205KB）+ `vision_wasm_internal.wasm`（9.2MB）
  - 本地模型 `assets/hand_landmarker.task`（7.5MB）v4.1 已下载
  - 总计约 17MB 本地资源，首次加载后无需网络
- 移除所有境外 CDN 引用（jsDelivr / unpkg / fastly / storage.googleapis.com），`vision_bundle.mjs` 与 WASM 文件均由本地 `import()` 和 `FilesetResolver` 读取
- `file://` 协议下（双击打开）检测到则提前拦截，提示需部署到 GitHub Pages 或用本地 HTTP 服务器（如 `python -m http.server`）
- 拼图框左上角新增三种手势说明卡片：☝️食指伸出=选中碎片 / 🖐️五指张开=随手掌移动 / ✊握拳=放下嵌入
- 变更文件：`puzzle.html`、`assets/mediapipe/`（新增）

## v4.1 - 2026-10-04 21:20
- 修复手势开启失败的问题：
  - 本地化手势模型：下载 `assets/hand_landmarker.task`（约 7.5MB）到项目内，优先加载本地模型，避免在线 GCS 模型文件加载缓慢或失败导致初始化卡死
  - MediaPipe 视觉模块增加多 CDN 回退（jsDelivr → unpkg → fastly jsDelivr）并加 15 秒加载超时，失败时明确提示
  - 增加 `navigator.mediaDevices` 不存在时的友好报错（file:// 等环境不支持摄像头）
  - 细分摄像头异常提示：权限被拒 / 无设备 / 设备被占用（NotReadableError）分别给出不同说明
  - 模型加载期间按钮禁用并显示"加载手势模型…"，防止重复点击
  - 骨架绘制改用模块导出的 `HAND_CONNECTIONS`，视频流增加 onerror 监听
- 变更文件：`puzzle.html`、`assets/hand_landmarker.task`（新增）

## v4.0 - 2026-10-04 21:05
- 手势识别迁移至 MediaPipe Tasks Vision（HandLandmarker 手部关键点模型），替代已废弃的旧版 @mediapipe/hands 方案：
  - 通过 CDN 动态加载 `@mediapipe/tasks-vision@0.10.14` 与官方 hand_landmarker 模型，GPU 推理失败自动回退 CPU
  - 摄像头改用原生 getUserMedia，配合 requestAnimationFrame 逐帧检测
  - 手势判定：食指伸开=选中、四指张开=移动、握拳=放下，5 帧多数投票防抖
  - 加载失败/权限被拒时给出明确状态提示
- 拼图玩法重构：移除右侧碎片栏，20 块碎片直接打乱铺进中间拼图框（保证开局无碎片在正确位置）
- 拖动碎片可与任意未锁定碎片交换位置，落到正确位置自动锁定并闪光提示，全部锁定即成功
- 右侧栏新增拼图进度条面板，拖拽时高亮目标格与悬停格
- 变更文件：`puzzle.html`

## v3.1 - 2026-10-04 20:40
- 拼图页面参考图不再悬浮于拼图板左上角，移至右侧栏顶部（碎片栏上方），彻底避免遮挡拼图。
- 新增右侧纵向栏 `.side-column`，参考图与碎片栏上下排列；碎片栏自适应剩余高度并内部滚动。
- 更新参考提示文案；窄屏（≤1100px）下参考图改为纵向堆叠展示。
- 变更文件：`puzzle.html`

## v3.0 - 2026-10-04 19:14
- 新增拼图游戏页面 `puzzle.html`。
- 将竹林七贤拼砖画分割为 5×4 共 20 块砖形碎片并随机打乱，展示在右侧碎片栏。
- 左上角提供原图参考，拼图板带淡色底图与网格辅助线。
- 支持三种操作方式：
  - 鼠标拖拽
  - 手指触控拖拽
  - 摄像头手势控制（食指选中、张开手掌移动、握拳嵌入）
- 首页大图新增点击跳转，可进入拼图游戏页面。
- 变更文件：`puzzle.html`、`index.html`

## v2.1 - 2026-10-04 18:57
- 调整首页布局，改为图片在上、文字在下的纵向排列，浮动大图整体上移。
- 大图最大高度从 78vh 调整为 66vh，预留标题与说明文字空间，避免被遮挡。
- 变更文件：`index.html`

## v2.0 - 2026-10-04 17:30
- 页面主题更新为《竹林七贤与荣启期 · 错版拼砖画》，展品信息改为南京六朝博物馆。
- 重新生成 `assets/hero-combined.png`，整体绿色调更鲜亮，边缘不再过于暗沉。
- 新增金色亮色粒子与流动丝带光影特效，标题改为金绿渐变，卡片边框和按钮加入金色点缀。
- 变更文件：`index.html`、`process_image.py`、`assets/hero-combined.png`

## v1.0 - 2026-10-04 17:10
- 初始版本：竹林七贤拼砖画数字展厅。
- 将两张参考图上下拼接为 `assets/hero-combined.png`，并做深竹绿/瓷青纸色双色处理、边缘暗角与颗粒质感。
- 首页采用深绿色调、玻璃拟态导航、居中大图、缓慢浮动与鼠标视差、绿色粒子特效、响应式布局。
- 变更文件：`index.html`、`process_image.py`、`assets/hero-combined.png`

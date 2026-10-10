# 变更日志

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

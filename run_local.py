# -*- coding: utf-8 -*-
"""本地静态服务器：将项目以 HTTP 方式提供，供拼图游戏使用摄像头与本地 WASM 手势模型。

用法：
    python run_local.py            启动后手动打开 http://127.0.0.1:8000/
    python run_local.py --open     启动后自动在浏览器中打开拼图游戏页（摄像头手势入口）
    python run_local.py --port 8001  指定其它端口

说明：
    - 手势模型（assets/mediapipe/ 与 assets/hand_landmarker.task）均为本地文件，
      通过本服务器访问时完全无需外网。
    - 摄像头（getUserMedia）必须在 http://127.0.0.1 或 https 环境下使用，
      直接双击打开（file://）会被浏览器拦截。
    - 如需部署到 GitHub Pages，直接把仓库文件推上去即可，同样不需要额外配置。
"""
import http.server
import functools
import os
import sys

PORT = 8000


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # 允许 localhost 上的摄像头与模块加载
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()


def main():
    args = sys.argv[1:]
    port = PORT
    auto_open = False
    i = 0
    while i < len(args):
        if args[i] == "--open":
            auto_open = True
        elif args[i] == "--port" and i + 1 < len(args):
            try:
                port = int(args[i + 1])
                i += 1
            except ValueError:
                print(f"无法识别端口：{args[i + 1]}，使用默认 {PORT}")
        i += 1

    root = os.path.dirname(os.path.abspath(__file__))
    url = f"http://127.0.0.1:{port}/puzzle.html"
    try:
        server = http.server.HTTPServer(("127.0.0.1", port), functools.partial(Handler, directory=root))
    except OSError as e:
        print(f"无法监听 127.0.0.1:{port}（{e}）。")
        print("若端口被占用：python run_local.py --port 8001")
        sys.exit(1)

    if auto_open:
        import webbrowser
        webbrowser.open(url)

    print(f"本地服务器已启动：http://127.0.0.1:{port}/")
    print(f"摄像头手势入口：{url}")
    print("按 Ctrl+C 停止（关闭本窗口即停止）。")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n已停止。")


if __name__ == "__main__":
    main()

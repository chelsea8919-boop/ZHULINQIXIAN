# -*- coding: utf-8 -*-
"""本地静态服务器：将项目以 HTTP 方式提供，供拼图游戏使用摄像头与本地 WASM 手势模型。

用法：
    python run_local.py
    然后浏览器打开 http://127.0.0.1:8000/

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

PORT = 8000


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # 允许 localhost 上的摄像头与模块加载
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()


def main():
    root = os.path.dirname(os.path.abspath(__file__))
    server = http.server.HTTPServer(("127.0.0.1", PORT), functools.partial(Handler, directory=root))
    print(f"本地服务器已启动：http://127.0.0.1:{PORT}/")
    print(f"服务目录：{root}")
    print("按 Ctrl+C 停止。")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n已停止。")


if __name__ == "__main__":
    main()

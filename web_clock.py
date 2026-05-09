#!/usr/bin/env python3
"""
Web Clock - 在浏览器中显示实时时钟
运行: python web_clock.py
"""

import http.server
import webbrowser
import threading
import json
from datetime import datetime

PORT = 8080

# this is a test
# hello everyone
#github is a good resposite
# this is a test for github
# this is a test for github

HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Web Clock</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: 'Segoe UI', -apple-system, sans-serif;
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    color: #fff;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .container { text-align: center; padding: 20px; }

  /* 数字时钟 */
  .digital { margin-bottom: 60px; }
  .digital .time {
    font-size: 100px;
    font-weight: 300;
    letter-spacing: 5px;
    font-variant-numeric: tabular-nums;
    text-shadow: 0 0 30px rgba(100, 150, 255, 0.3);
  }
  .digital .time .seconds {
    font-size: 40px;
    color: rgba(255,255,255,0.5);
  }
  .digital .colon { animation: blink 1s steps(1) infinite; }
  @keyframes blink { 50% { opacity: 0; } }
  .digital .date {
    font-size: 20px;
    color: rgba(255,255,255,0.5);
    margin-top: 10px;
  }

  /* 模拟时钟 */
  .analog { position: relative; display: inline-block; }
  canvas {
    background: rgba(255,255,255,0.03);
    border-radius: 50%;
    box-shadow: 0 0 60px rgba(100, 150, 255, 0.1);
  }
  .markers {
    margin-top: 40px;
    display: flex;
    gap: 30px;
    justify-content: center;
    font-size: 14px;
    color: rgba(255,255,255,0.4);
  }
  .markers span { transition: color 0.3s; }
</style>
</head>
<body>
<div class="container">
  <div class="digital">
    <div class="time">
      <span id="hours">00</span><span class="colon">:</span><span id="minutes">00</span><span class="colon">:</span><span id="seconds" class="seconds">00</span>
    </div>
    <div class="date" id="date"></div>
  </div>
  <div class="analog">
    <canvas id="canvas" width="280" height="280"></canvas>
  </div>
</div>

<script>
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const size = 280, cx = 140, cy = 140, r = 120;

function drawClock(h, m, s) {
  ctx.clearRect(0, 0, size, size);

  // 表盘
  ctx.beginPath();
  ctx.arc(cx, cy, r, 0, Math.PI * 2);
  ctx.strokeStyle = 'rgba(255,255,255,0.15)';
  ctx.lineWidth = 2;
  ctx.stroke();

  // 刻度
  for (let i = 0; i < 60; i++) {
    const a = (i * Math.PI * 2) / 60 - Math.PI / 2;
    const len = i % 5 === 0 ? 12 : 6;
    const w = i % 5 === 0 ? 2.5 : 1;
    ctx.beginPath();
    ctx.moveTo(cx + Math.cos(a) * (r - 18), cy + Math.sin(a) * (r - 18));
    ctx.lineTo(cx + Math.cos(a) * (r - 18 - len), cy + Math.sin(a) * (r - 18 - len));
    ctx.strokeStyle = i % 5 === 0 ? 'rgba(255,255,255,0.7)' : 'rgba(255,255,255,0.2)';
    ctx.lineWidth = w;
    ctx.stroke();
  }

  // 时针
  const ha = (h % 12 + m / 60) * (Math.PI * 2 / 12) - Math.PI / 2;
  ctx.beginPath();
  ctx.moveTo(cx, cy);
  ctx.lineTo(cx + Math.cos(ha) * r * 0.5, cy + Math.sin(ha) * r * 0.5);
  ctx.strokeStyle = '#fff';
  ctx.lineWidth = 4;
  ctx.lineCap = 'round';
  ctx.stroke();

  // 分针
  const ma = (m + s / 60) * (Math.PI * 2 / 60) - Math.PI / 2;
  ctx.beginPath();
  ctx.moveTo(cx, cy);
  ctx.lineTo(cx + Math.cos(ma) * r * 0.7, cy + Math.sin(ma) * r * 0.7);
  ctx.strokeStyle = 'rgba(200, 220, 255, 0.9)';
  ctx.lineWidth = 2.5;
  ctx.stroke();

  // 秒针
  const sa = s * (Math.PI * 2 / 60) - Math.PI / 2;
  ctx.beginPath();
  ctx.moveTo(cx, cy);
  ctx.lineTo(cx + Math.cos(sa) * r * 0.85, cy + Math.sin(sa) * r * 0.85);
  ctx.strokeStyle = '#ff6b6b';
  ctx.lineWidth = 1.5;
  ctx.stroke();

  // 中心点
  ctx.beginPath();
  ctx.arc(cx, cy, 4, 0, Math.PI * 2);
  ctx.fillStyle = '#ff6b6b';
  ctx.fill();
  ctx.beginPath();
  ctx.arc(cx, cy, 2, 0, Math.PI * 2);
  ctx.fillStyle = '#fff';
  ctx.fill();
}

function update() {
  const now = new Date();
  const h = String(now.getHours()).padStart(2, '0');
  const m = String(now.getMinutes()).padStart(2, '0');
  const s = String(now.getSeconds()).padStart(2, '0');
  document.getElementById('hours').textContent = h;
  document.getElementById('minutes').textContent = m;
  document.getElementById('seconds').textContent = s;

  const days = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六'];
  const d = now;
  document.getElementById('date').textContent =
    `${d.getFullYear()}年${d.getMonth()+1}月${d.getDate()}日 ${days[d.getDay()]}`;

  drawClock(d.getHours(), d.getMinutes(), d.getSeconds());
}

update();
setInterval(update, 1000);
</script>
</body>
</html>"""

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/time':
            now = datetime.now()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'h': now.hour, 'm': now.minute, 's': now.second,
                'iso': now.isoformat()
            }).encode())
        else:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML.encode('utf-8'))

    def log_message(self, format, *args):
        pass  # 静默日志

if __name__ == '__main__':
    server = http.server.HTTPServer(('127.0.0.1', PORT), Handler)
    url = f'http://127.0.0.1:{PORT}'
    print(f'时钟已启动: {url}')
    threading.Timer(0.5, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n关闭中...')
        server.shutdown()

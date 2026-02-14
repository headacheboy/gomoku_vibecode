# 🎮 五子棋游戏 - 发布说明

## ✅ 打包完成

项目已成功打包为**便携版**，可直接分发和运行。

---

## 📦 如何使用

### 快速启动

**Windows 用户（最简单）**
```
双击: Gomoku_Portable/START_GAME.bat
```

**Linux/macOS 用户**
```bash
cd Gomoku_Portable
chmod +x start_game.sh
./start_game.sh
```

**任何系统（Python）**
```bash
cd Gomoku_Portable
python gomoku_launcher.py
```

---

## 🎯 游戏特性

✅ **完整五子棋规则实现**
- 15x15 棋盘
- 胜利检测（横/竖/斜5连珠）
- 撤销/重做支持

✅ **智能 AI 对手**
- 使用 Minimax + Alpha-Beta 剪枝
- Numba JIT 加速评估
- Killer moves & History heuristic
- 搜索深度可调（推荐 depth=2-3）

✅ **完整功能**
- 存档/读档（JSON 格式）
- 本地双人对战
- 人机对战
- 棋谱记录

✅ **优化加速**
- Numba JIT 编译（~1.15 秒/步 depth=2）
- 评估缓存
- Byte-grid 序列化
- 转置表优化

---

## 📋 系统要求

| 要求 | 规格 |
|------|------|
| Python | 3.5+ |
| 内存 | 512 MB |
| 磁盘 | 50 MB（含依赖） |
| 显示 | 800×600 最小分辨率 |
| 操作系统 | Windows / macOS / Linux |

---

## 🎮 游戏控制

| 按键 | 动作 |
|------|------|
| **鼠标左击** | 放置棋子 |
| **A** | 切换 AI（启用/禁用） |
| **P** | 切换 AI 颜色（黑/白） |
| **+** | 提高 AI 搜索深度 |
| **-** | 降低 AI 搜索深度 |
| **U** | 撤销最后一步 |
| **R** | 重做上一步 |
| **N** | 新游戏 |
| **S** | 保存游戏（带文件对话框） |
| **L** | 加载游戏（带文件对话框） |
| **ESC** | 退出游戏 |

---

## 📂 文件清单

```
Gomoku_Portable/
├── START_GAME.bat             # ⭐ Windows 用户：双击此文件启动
├── start_game.sh              # macOS/Linux 用户：运行此脚本
├── gomoku_launcher.py         # Python 启动器
├── gomoku/                    # 游戏源代码
│   ├── __init__.py
│   ├── main.py                # 主程序入口
│   ├── game.py                # 棋盘模型和规则
│   ├── ai.py                  # AI 引擎（Minimax + α-β）
│   ├── ai_numba.py            # Numba JIT 加速函数
│   ├── ai_cy.pyx              # Cython 脚手架（可选）
│   ├── ui.py                  # Pygame GUI
│   └── storage.py             # 存档功能
├── requirements.txt           # Python 依赖
├── README.md                  # 项目说明
└── PORTABLE_README.md         # 便携版使用指南
```

---

## 🔧 故障排除

### "Python not found"
```
解决：从 https://www.python.org/downloads/ 安装 Python 3.5+
确保选中"Add Python to PATH"选项
```

### "pygame/numba not found"
```
解决：手动运行：
  python -m pip install pygame numba numpy
```

### "游戏启动缓慢"
```
原因：首次运行时 Numba 需要 JIT 编译（5-10秒）
解决：等待加载，后续运行会快得多
```

### "游戏卡顿/响应慢"
```
原因：AI 搜索深度设置过高
解决：按 - 键降低 AI 深度到 2-3
```

---

## 📊 性能基准

| 配置 | 首步耗时 | 后续步 | AI 强度 |
|------|---------|--------|--------|
| depth=2 | 2.0 秒* | 1.15 秒 | ⭐⭐ 中等 |
| depth=3 | 5-10 秒 | 3-5 秒 | ⭐⭐⭐ 较强 |
| depth=4 | 20+ 秒 | 10+ 秒 | ⭐⭐⭐⭐ 很强 |

*包含 Numba JIT 编译开销，第二步后恢复正常

---

## 🚀 进阶使用

### 自定义 AI 难度

编辑 `gomoku/ui.py`，找到初始化部分（约第 50 行）：
```python
self.ai_depth = 2  # 改为 3-4 获得更强的 AI
```

### 编译 Cython 版本（仅 Linux/WSL）

获得 ~30% 速度提升：
```bash
pip install cython
python ../setup_cython.py build_ext --inplace
```

### 查看游戏日志

游戏保存状态到 `savegame.json`，可用文本编辑器查看。

---

## 📜 许可与致谢

本项目为教学演示项目。
- 游戏规则：五子棋（连珠）经典规则
- 界面库：Pygame
- AI 加速：Numba (LLVM)

---

## 💬 反馈

若遇问题或有改进建议，欢迎提出！

---

**祝你在五子棋之旅中玩得开心！** 🎯🎮

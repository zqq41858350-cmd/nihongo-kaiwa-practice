#!/usr/bin/env python3
"""训练记录脚本的离线验证。"""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from datetime import date
from pathlib import Path


脚本路径 = Path(__file__).with_name("records.py")
规范 = importlib.util.spec_from_file_location("训练记录", 脚本路径)
模块 = importlib.util.module_from_spec(规范)
规范.loader.exec_module(模块)


def 示例记录(编号: str) -> dict:
    问题 = "これから、どんなことをやってみたいですか？"
    return {
        "训练编号": 编号,
        "训练时间": "2026-09-15T20:30:00+08:00",
        "话题编号": "future-plans",
        "问题表现": [{"问题": 问题, "状态": "prompted", "最高提示": "中文方向"}],
        "逐题自然整理": [{"问题": 问题, "原回答": "日本に行きたいです。", "自然表达": "日本へ行ってみたいです。"}],
        "复习安排": [{"日期": "2026-09-16", "问题": 问题, "阶段": "次日复习"}],
        "已完成复习": [],
    }


class 记录测试(unittest.TestCase):
    def test_保存读取与完成复习(self):
        with tempfile.TemporaryDirectory() as root:
            folder = Path(root)
            input_path = folder / "input.json"
            first = 示例记录("2026-09-15-001")
            input_path.write_text(json.dumps(first, ensure_ascii=False), encoding="utf-8")
            模块.保存(input_path, folder / "记录")
            records = 模块.记录列表(folder / "记录")
            self.assertEqual(len(records), 1)
            self.assertEqual(len(模块.到期(records, date(2026, 9, 15))), 0)
            self.assertEqual(len(模块.到期(records, date(2026, 9, 16))), 1)
            模块.保存(input_path, folder / "记录")  # 相同内容重复保存可安全重试
            self.assertEqual(len(模块.记录列表(folder / "记录")), 1)

            follow_up = 示例记录("2026-09-16-001")
            follow_up["训练时间"] = "2026-09-16T20:30:00+08:00"
            follow_up["复习安排"] = []
            follow_up["已完成复习"] = [{
                "原训练编号": first["训练编号"],
                "日期": "2026-09-16",
                "问题": first["问题表现"][0]["问题"],
            }]
            input_path.write_text(json.dumps(follow_up, ensure_ascii=False), encoding="utf-8")
            模块.保存(input_path, folder / "记录")
            self.assertEqual(模块.到期(模块.记录列表(folder / "记录"), date(2026, 9, 16)), [])

    def test_不同内容不能覆盖同一编号(self):
        with tempfile.TemporaryDirectory() as root:
            folder = Path(root)
            input_path = folder / "input.json"
            record = 示例记录("2026-09-15-001")
            input_path.write_text(json.dumps(record, ensure_ascii=False), encoding="utf-8")
            模块.保存(input_path, folder / "记录")
            record["话题编号"] = "ai"
            input_path.write_text(json.dumps(record, ensure_ascii=False), encoding="utf-8")
            with self.assertRaises(ValueError):
                模块.保存(input_path, folder / "记录")


if __name__ == "__main__":
    unittest.main()

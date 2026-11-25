#!/usr/bin/env python3
"""在学员指定的目录中保存和读取日语口语训练记录。"""

from __future__ import annotations

import argparse
import json
import os
import re
import tempfile
from datetime import date, datetime
from pathlib import Path


编号格式 = re.compile(r"^[A-Za-z0-9._-]+$")
回答状态 = {"independent", "prompted", "imitated", "incomplete"}


def 读取(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as file:
        value = json.load(file)
    if not isinstance(value, dict):
        raise ValueError("训练记录必须是 JSON 对象")
    return value


def 检查(record: dict) -> None:
    for field in ("训练编号", "训练时间", "话题编号", "问题表现", "逐题自然整理", "复习安排"):
        if field not in record:
            raise ValueError(f"缺少字段：{field}")
    if not isinstance(record["训练编号"], str) or not 编号格式.fullmatch(record["训练编号"]):
        raise ValueError("训练编号只能使用字母、数字、点、下划线和连字符")
    datetime.fromisoformat(record["训练时间"])
    if not isinstance(record["话题编号"], str) or not record["话题编号"]:
        raise ValueError("话题编号必须是非空文本")
    if not isinstance(record["问题表现"], list) or not record["问题表现"]:
        raise ValueError("问题表现至少应包含一道已回答的问题")
    for item in record["问题表现"]:
        if not isinstance(item, dict) or item.get("状态") not in 回答状态 or not item.get("问题"):
            raise ValueError("问题表现需要问题和有效状态")
    if not isinstance(record["逐题自然整理"], list):
        raise ValueError("逐题自然整理必须是列表")
    for item in record["逐题自然整理"]:
        if not isinstance(item, dict) or not all(item.get(key) for key in ("问题", "原回答", "自然表达")):
            raise ValueError("逐题自然整理需要问题、原回答和自然表达")
    if not isinstance(record["复习安排"], list):
        raise ValueError("复习安排必须是列表")
    for item in record["复习安排"]:
        if not isinstance(item, dict) or not item.get("日期") or not item.get("问题"):
            raise ValueError("每条复习安排需要日期和问题")
        date.fromisoformat(item["日期"])
    completed = record.get("已完成复习", [])
    if not isinstance(completed, list):
        raise ValueError("已完成复习必须是列表")
    for item in completed:
        if not isinstance(item, dict) or not all(item.get(key) for key in ("原训练编号", "日期", "问题")):
            raise ValueError("已完成复习需要原训练编号、日期和问题")


def 记录列表(data_dir: Path) -> list[dict]:
    sessions_dir = data_dir / "sessions"
    if not sessions_dir.exists():
        return []
    result = []
    for path in sessions_dir.glob("*.json"):
        record = 读取(path)
        检查(record)
        result.append(record)
    return sorted(result, key=lambda item: item["训练时间"], reverse=True)


def 保存(input_path: Path, data_dir: Path) -> None:
    record = 读取(input_path)
    检查(record)
    sessions_dir = data_dir / "sessions"
    sessions_dir.mkdir(parents=True, exist_ok=True)
    destination = sessions_dir / f"{record['训练编号']}.json"
    if destination.exists():
        existing = 读取(destination)
        if existing != record:
            raise ValueError("同一训练编号已有不同内容；请使用新编号，避免覆盖历史")
        print(json.dumps({"状态": "已存在", "路径": str(destination)}, ensure_ascii=False))
        return
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=sessions_dir, delete=False, suffix=".tmp") as file:
        json.dump(record, file, ensure_ascii=False, indent=2)
        file.write("\n")
        temp_path = Path(file.name)
    try:
        os.replace(temp_path, destination)
    finally:
        temp_path.unlink(missing_ok=True)
    print(json.dumps({"状态": "已保存", "路径": str(destination)}, ensure_ascii=False))


def 到期(records: list[dict], today: date) -> list[dict]:
    completed = {
        (item["原训练编号"], item["日期"], item["问题"])
        for record in records
        for item in record.get("已完成复习", [])
    }
    result = []
    for record in records:
        for item in record["复习安排"]:
            key = (record["训练编号"], item["日期"], item["问题"])
            if date.fromisoformat(item["日期"]) <= today and key not in completed:
                result.append({"训练编号": record["训练编号"], "话题编号": record["话题编号"], **item})
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", required=True, type=Path, help="学员明确授权的记录目录")
    commands = parser.add_subparsers(dest="command", required=True)
    archive = commands.add_parser("archive", help="保存一条训练记录")
    archive.add_argument("--input", required=True, type=Path)
    commands.add_parser("latest", help="读取最近一条训练记录")
    commands.add_parser("history", help="读取全部训练记录，用于成长对比")
    due = commands.add_parser("due", help="读取今天及之前到期的复习问题")
    due.add_argument("--date", type=date.fromisoformat, default=date.today())
    args = parser.parse_args()
    data_dir = args.data_dir.expanduser().resolve()
    if args.command == "archive":
        保存(args.input, data_dir)
        return
    records = 记录列表(data_dir)
    if args.command == "latest":
        print(json.dumps(records[0] if records else None, ensure_ascii=False, indent=2))
    elif args.command == "history":
        print(json.dumps(records, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(到期(records, args.date), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

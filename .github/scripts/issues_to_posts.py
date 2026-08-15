#!/usr/bin/env python3
"""把仓库中带 post 标签的 open Issues 生成为 Hexo 文章 (source/_posts/issue-<n>.md)。

- 触发时机：GitHub Actions 里 issues 事件（opened/edited/reopened/closed）由 workflow 调用
- 全量重建：每次拉取所有 open+post 的 Issues，清理旧的 issue-*.md
  → 新增/编辑自动生效，关闭/移除标签自动下架
- 约定：标题=文章标题；正文=Markdown 正文；第一个非 post 标签=分类，其余=标签
"""
import json
import os
import re
import subprocess
import glob

POSTS_DIR = "source/_posts"
LABEL = "post"


def main():
    out = subprocess.run(
        ["gh", "issue", "list", "--label", LABEL, "--state", "open",
         "--json", "number,title,createdAt,labels,body", "--limit", "200"],
        capture_output=True, text=True, check=True)
    issues = json.loads(out.stdout)

    # 清理旧的 issue-*.md（关闭/移除标签的 Issue 自动下架）
    for f in glob.glob(os.path.join(POSTS_DIR, "issue-*.md")):
        os.remove(f)

    for i in issues:
        labels = [l["name"] for l in i["labels"] if l["name"] != LABEL]
        category = labels[0] if labels else "随笔"
        tags = labels[1:] if len(labels) > 1 else []
        title = i["title"].strip().replace('"', '\\"')
        created = i["createdAt"].replace("T", " ").replace("Z", "")[:19]

        fm = ["---", f'title: "{title}"', f"date: {created}"]
        if tags:
            fm.append("tags:")
            fm += [f"  - {t}" for t in tags]
        fm += ["categories:", f"  - {category}", "---", ""]

        body = (i["body"] or "").strip()
        # marked 不渲染 **中文引号**，预处理成 <strong>
        body = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", body, flags=re.S)
        # 转义 Issue 引用 #数字（避免渲染成标题），行首的 # 标题不动
        body = re.sub(r"(?<!^)(?<!\w)#(\d+)", r"\\#\1", body, flags=re.M)

        with open(os.path.join(POSTS_DIR, f"issue-{i['number']}.md"),
                  "w", encoding="utf-8") as f:
            f.write("\n".join(fm) + "\n\n" + body + "\n")
        print(f"generated: issue-{i['number']}.md <- {i['title']}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""把仓库中所有 open 的 Issues 生成为 Hexo 文章 (source/_posts/issue-<n>.md)。

- 触发时机：GitHub Actions 里 issues 事件（opened/edited/reopened/closed）由 workflow 调用
- 全量重建：每次拉取所有 open Issues，清理旧的 issue-*.md
  → 新增/编辑自动生效，关闭/删除自动下架
- 约定：标题=文章标题；正文=Markdown 正文；第一个标签=分类，其余=标签；无标签默认分类"随笔"
"""
import json
import os
import re
import subprocess
import glob

POSTS_DIR = "source/_posts"

# 分类标签白名单：命中任意一个即作为文章分类，其余标签全部作为文章标签。
# 与标签添加顺序无关；不命中任何分类标签时默认"随笔"。
# 新增分类时在此追加（如 "教程", "求职"）。
CATEGORIES = {"项目", "随笔", "教程", "笔记", "技术", "生活", "求职"}


def main():
    out = subprocess.run(
        ["gh", "issue", "list", "--state", "open",
         "--json", "number,title,createdAt,labels,body", "--limit", "200"],
        capture_output=True, text=True, check=True)
    issues = json.loads(out.stdout)

    # 清理旧的 issue-*.md（关闭的 Issue 自动下架）
    for f in glob.glob(os.path.join(POSTS_DIR, "issue-*.md")):
        os.remove(f)

    for i in issues:
        labels = [l["name"] for l in i["labels"]]
        # 分类：labels 中第一个命中白名单的；标签：所有非分类标签
        category = next((c for c in labels if c in CATEGORIES), "随笔")
        tags = [t for t in labels if t not in CATEGORIES]
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

        # 首页摘要截断：尊重手动 <!-- more -->；否则自动取前 2 段（按空行分段）
        if "<!-- more -->" not in body:
            paras = re.split(r"\n\s*\n", body)
            if len(paras) > 2:
                body = ("\n\n".join(paras[:2]) + "\n\n<!-- more -->\n\n"
                        + "\n\n".join(paras[2:]))

        with open(os.path.join(POSTS_DIR, f"issue-{i['number']}.md"),
                  "w", encoding="utf-8") as f:
            f.write("\n".join(fm) + "\n\n" + body + "\n")
        print(f"generated: issue-{i['number']}.md <- {i['title']}")


if __name__ == "__main__":
    main()

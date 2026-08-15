---
title: FileGuard 跨平台文件加密工具
date: 2026-08-15 10:00:00
tags:
  - Python
  - 加密
  - 桌面应用
categories:
  - 项目
---

> 🔒 拖拽即用的高速文件加解密软件 —— AES-256-GCM · 口令/密钥文件双模式 · 文件夹打包 · 批量并行

**项目地址**：[github.com/CmeiLYL/fileguard](https://github.com/CmeiLYL/fileguard)（Win + Linux 双平台 Release，MIT 协议）

<!-- more -->

## 为什么做这个项目

日常工作里经常需要在 U 盘、网盘、邮件附件之间传递文件，明文存放总不放心。市面上的加密工具要么收费、要么绑定平台、要么操作复杂。于是自己用 Python 写了一个 **拖进去 → 输口令 → 点一下** 就完事的加密工具。

## 核心特性

| 特性 | 说明 |
|---|---|
| 🖱️ 拖拽即用 | 文件/文件夹直接拖入，自动去重 |
| ⚡ 高速 | AES-256-GCM 硬件加速，512 MB ≈ 0.4s（约 1400 MB/s） |
| 🔑 双加密方式 | 记忆口令 或 密钥文件，二选一，解密自动识别 |
| 📁 文件夹支持 | 文件夹一键打包加密；多文件可合并加密为单个包 |
| 📦 批量并行 | 多线程并行处理，进度条实时显示 |
| 🕵️ 加密文件名 | 可选隐藏真实文件名，防目录结构泄露 |
| 🛡️ 军用级安全 | AEAD 认证加密，密码错/被篡改/密文重排全部拦截 |

## 技术要点

- **算法**：AES-256-GCM（认证加密 AEAD），密钥派生走 PBKDF2（口令模式）
- **语言/框架**：Python 3.11 + cryptography 库 + CustomTkinter GUI
- **架构**：domain / interfaces / infrastructure / application 分层，JSON 配置驱动
- **打包**：PyInstaller 双平台构建，Win 下带图标拖拽支持
- **质量**：pytest 全覆盖，算法层与 GUI 层解耦可单测

## 使用三步

1. **拖入**文件/文件夹（或选「合并加密」打包多个）
2. **选加密方式**：口令模式填口令；密钥文件模式点「生成」新建密钥文件
3. 点 **加密** 或 **解密** —— 完成

解密时程序自动读取文件头，判断加密方式并切换到对应输入框，无需手动选择。

## 下载体验

GitHub Releases 页面提供 Windows / Linux 两个平台的免环境可执行文件，下载即用：[github.com/CmeiLYL/fileguard/releases](https://github.com/CmeiLYL/fileguard/releases)

后续方向：信创（麒麟/统信）系统适配、右键菜单集成。

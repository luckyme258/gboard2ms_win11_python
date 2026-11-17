**中文** ｜ [English](#english-manual)

# 微软拼音词库管理器 使用手册

> **⬇️ 下载最新版**：请到 [Releases](https://github.com/luckyme258/gboard2ms_win11/releases/latest) 下载 **v1.0**。
>
> **⚠️ v0.1 / v0.2 已停止维护**：这两个旧版的 Gboard 导出还是旧格式 txt，导入新版安卓 Gboard 只会得到**空词典**，请勿下载使用。

## 一、简介

微软拼音词库管理器是一个图形化工具，用于管理输入法的自定义短语词库，在内置的 `book.txt` 里统一维护一套条目，再分别导出到两套输入法：

- **Gboard（安卓）**：导出为新版 Gboard 词典包（`.zip`，内含按语言拆分的 `dictionary_*.txt`），可直接在手机 Gboard 的个人词典里导入
- **微软拼音（Windows）**：导出为 `.dat`，可在微软拼音的用户自定义短语里导入

同时支持从 Gboard 导出的文本词库、微软拼音的 `.dat` 反向导入。

**界面支持中文 / English 两种语言**：启动时按系统语言自动选择，也可在窗口右上角随时手动切换。

演示放在哔哩哔哩了

使用演示：Gboard自定义词典编辑器 [谷歌输入法（安卓）与微软输入法（Windows）]

[▶️ 点击观看使用演示（B站）](https://www.bilibili/video/BV1tj7k6VEeh/)

## 二、安装与运行

### 方式一：Python 脚本运行
```bash
python ms_manager.py
```

### 方式二：直接运行 exe
双击 `微软拼音词库管理器.exe` 即可运行。

> 目前 Releases 上的 **v1.0 是源码版，暂无官方 exe**；如需 exe，可自行用 PyInstaller 打包本仓库的 `ms_manager.py`。

**注意**：`book.txt` 文件自动生成，与 exe 放在同一目录下。

## 三、主界面

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ 搜索: [        ] [添加] [删除] [导入 Gboard] [导入 DAT] [导出 Gboard] [导出 DAT] [保存] [打开文件夹]      语言: [中文 ▾] │
├──────────────────────────────────────────────────────────────────────────────┤
│ 总计: 33 条 | 唯一编码: 33 个 | 重复编码: 0 个                                  │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  短语              │ 编码            │ 候选位置                                  │
│  ─────────────────┼────────────────┼─────────────────────────────────────── │
│  ad               │ adb devices    │ 1                                        │
│  xm               │ 小米9           │ 1                                        │
│  gp               │ git push       │ 1                                        │
│  ...              │ ...            │ ...                                      │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│ 显示 33 / 33 条                                                    就绪        │
└──────────────────────────────────────────────────────────────────────────────┘
```

> 界面列标题是「短语 | 编码」，但**当前 `book.txt` 的实际列序是「编码在前、短语在后」**，所以表格里「短语」列显示的是编码、「编码」列显示的是短语。原因与处理见第七章「book.txt 的列序问题」。

### 3.1 界面语言（右上角）

- **启动时自动判断**：Windows 下读取系统的显示语言，中文系统用中文界面，其它语言用 English
- **随时手动切换**：点右上角「语言:」下拉框，选 `中文` 或 `English`，界面立即整体切换（按钮、列标题、统计栏、状态栏、右键菜单、所有弹窗文案）
- 切换只影响界面语言，不改动词库数据与导出内容

## 四、基本操作

### 4.1 搜索
在搜索框中输入文字，实时过滤显示匹配的词条（短语或编码任一命中即显示）。

### 4.2 添加词条
1. 点击「添加」按钮
2. 填写短语（如：`你好`）
3. 填写编码（如：`nh`）
4. 选择候选位置（1-9，数字越小越靠前）
5. 点击「确定」

### 4.3 编辑词条
- **双击**表格中的任意词条
- 或**右键**点击 → 选择「编辑」
- 修改后点击「确定」

### 4.4 删除词条
- **选中词条**（支持多选），按 `Delete` 键
- 或点击「删除」按钮
- 或右键 →「删除」

### 4.5 多选技巧
| 操作           | 效果              |
| -------------- | ----------------- |
| `Ctrl + 点击`  | 选中/取消选中单个 |
| `Shift + 点击` | 连续选中多个      |
| `Ctrl + A`     | 全选              |
| `Delete`       | 删除选中          |

## 五、导入导出

### 5.1 导入 Gboard 词库
1. 在手机上打开 Gboard 设置 → 词典 → 个人词典 → 导出，得到一个 `PersonalDictionary-*.zip`
2. **先解压**，取出里面的 `dictionary.txt`（本工具目前只读文本文件，不解压 zip）
3. 把这个 `.txt` 传到电脑
4. 点击「导入 Gboard」，选择该文件
5. 程序自动去重合并；同编码的多条会按候选位置依次往后排（上限 9）

> 新版 Gboard 导出的 txt 第 1 行是 `# Gboard Dictionary version:2`，第 2 行是格式声明，条目为 `编码 → 短语 → 语言标签 → 候选标记` 四列。导入时程序会自动跳过 `#` 开头的头行、剥掉尾部的语言标签。

### 5.2 导入微软拼音 DAT
1. 在微软拼音设置中导出用户自定义短语（得到 `.dat` 文件）
2. 点击「导入 DAT」，选择该文件
3. 程序自动解析并合并（候选位置取自 DAT 条目里记录的候选位）

### 5.3 导出 Gboard 词典包（zip）
1. 点击「导出 Gboard」
2. 选择保存位置，默认文件名 `Gboard_Dictionary_<时间戳>.zip`
3. 生成的是**一个 zip**，包内按语言拆分：

```
Gboard_Dictionary_20261117_223000.zip
├─ dictionary_zh-CN.txt     ← 所有含中文的条目
└─ dictionary_zz.txt        ← 所有纯英文/符号的条目
```

- **语言自动判断**：短语里含中文（基本区、扩展 A、兼容区、全角标点）→ `zh-CN`；其余 → `zz`
- **一个文件只装一种语言**，中英不混装；若某一语言没有条目，zip 里就不会有那个文件
- 包内每个 txt 都是新版 Gboard 的 `version:2` 格式：固定两行头 + 每条四列 + 行尾留 Tab + 纯 LF 换行 + UTF-8 无 BOM
- **导出后有自检**：程序会立刻回读生成的文件，校验头部、换行、列结构；不合规会弹「自检失败」并中止，不会出现「提示成功但文件无效」
- 导入手机：把整个 zip 传到手机 → Gboard 设置 → 词典 → 个人词典 → 导入，选择该 zip

### 5.4 导出微软拼音 DAT
1. 点击「导出 DAT」
2. 选择保存位置，默认文件名 `ms_export_<时间戳>.dat`
3. 生成的 `.dat` 可在微软拼音的用户自定义短语里导入（文件格式细节见《微软格式说明文档.md》）

### 5.5 保存
点击「保存」把当前数据写回 `book.txt`，写之前会自动把旧文件备份为 `book.txt.bak`。

## 六、文件说明

| 文件                          | 说明                                        |
| ----------------------------- | ------------------------------------------- |
| `book.txt`                    | 内部统一词库，三列 Tab 分隔                  |
| `book.txt.bak`                | 保存时自动生成的备份                        |
| `ms_manager.py` / `*.exe`     | 主程序                                      |
| `Gboard_Dictionary_*.zip`     | Gboard 导出产物（可含多个 `dictionary_*.txt`） |
| `ms_export_*.dat`             | 微软拼音导出产物                            |
| `微软格式说明文档.md`         | `.dat` 文件格式规则详解                     |

## 七、book.txt 格式

内部格式为 Tab 分隔的三列，程序按「第 1 列、第 2 列、第 3 列」依次读写：

```
# 微软拼音词库 - 统一格式
# 更新时间: 2026-11-17 22:30:00
# 总计: 3 条
# 格式: 短语	编码	候选位置
#--------------------------------------------------
ad	adb devices	1
xm	小米9	1
gp	git push	1
```

### ⚠ book.txt 的列序问题（现状说明）

程序文件头里写的注释是「格式: 短语 编码 候选位置」，界面列标题也是「短语 | 编码」，但**本机现有的 `book.txt` 里第 1 列实际是编码**（因为最初的数据来自 Gboard 导入，而导入逻辑把第 1 列当编码写入）。具体表现：

| 位置 | 程序以为 | 实际数据 |
| ---- | -------- | -------- |
| 第 1 列 | 短语 | 编码（如 `ad`、`xm`） |
| 第 2 列 | 编码 | 短语（如 `adb devices`、`小米9`） |
| 第 3 列 | 候选位置 | 候选位置（一致） |

受影响的地方（都源于同一个根因）：

- **Gboard 导出**已按「第 1 列 = shortcut、第 2 列 = 短语」处理，与实际数据一致，实测可正常导入 → **正确**
- **DAT 导出**按「第 2 列 = 编码、第 1 列 = 短语」处理，与实际数据相反 → 导出的 DAT 里「编码」是长句、「短语」是短码，详见第八章 Q7
- **统计栏**的「唯一编码 / 重复编码」也按第 2 列统计，所以当前显示「唯一编码 33 个、重复编码 0 个」；按实际的编码列算，应是 32 个唯一、1 组重复（`xm` 两条）
- **界面**因此把编码显示在「短语」列

统一列序需要动数据或动映射，属于单独一项改动，当前版本未做。

## 八、常见问题

### Q1: 打开程序提示「book.txt 不存在」
A: 程序会自动创建，首次运行正常现象。

### Q2: 导入 Gboard 文件提示「编码错误」
A: 确保文件是 UTF-8 编码的纯文本；如果拿到的是手机导出的 `.zip`，请先解压，导入里面的 `.txt`。

### Q3: 导出的 DAT 导入微软拼音后乱码
A: 检查 `book.txt` 内容是否正确；也请先看 Q7 的列序说明。

### Q4: 如何备份词库？
A: 直接复制 `book.txt`；程序每次保存也会生成 `book.txt.bak`。

### Q5: 支持哪些 Windows 版本？
A: Windows 10 / Windows 11。

### Q6: 导出的 zip 导入手机后词典是空的？
A: 按顺序排查：
1. 导出的是不是本版生成的 zip（旧版导出的 `.txt` 用的是旧头部，新版 Gboard 不认，导入后就是空的）
2. zip 是否被解压过又重命名（应直接把原始 zip 导入，不要只传内层的单个 txt）
3. 导入后到 Gboard「词典 → 个人词典」确认语言条目是否落在对应词典里

### Q7: DAT 导入后「输入一长串才出短码」？
A: 这是当前 `book.txt` 列序与 DAT 导出映射不一致导致的（见第七章）。DAT 导出取的是第 2 列当编码，而现有数据的第 2 列是短语。使用 DAT 前请先统一列序，或等该项修正。

### Q8: 界面是英文，能改回中文吗？
A: 右上角「Language:」下拉框选 `中文` 即可；这只影响界面显示，不影响数据与导出。

## 九、快捷键汇总

| 快捷键     | 功能     |
| ---------- | -------- |
| `Ctrl + A` | 全选     |
| `Delete`   | 删除选中 |
| `双击`     | 编辑词条 |

## 十、联系与反馈

如有问题或建议，欢迎反馈。

---

**版本**：1.0
**更新日期**：2026-11-17
**本次更新**：适配新版 Gboard（`version:2`）词典格式、导出改为 zip 词典包、新增导出后自检、界面支持中文/English 双语。详见《更新日志.md》。

---

# English Manual

> **⬇️ Download the latest version**: get **v1.0** from [Releases](https://github.com/luckyme258/gboard2ms_win11/releases/latest).
>
> **⚠️ v0.1 / v0.2 are no longer maintained**: they still export the legacy txt format, which imports as an **empty dictionary** on the current Android Gboard. Do not download them.

**English** ｜ [中文](#微软拼音词库管理器-使用手册)

## 1. Overview

Microsoft Pinyin Dictionary Manager is a GUI tool that keeps one single dictionary (`book.txt`) and exports it to two input methods:

- **Gboard (Android)** — exports a Gboard dictionary package (`.zip` containing per-language `dictionary_*.txt`), which can be imported directly in Gboard's personal dictionary
- **Microsoft Pinyin (Windows)** — exports a `.dat` file that can be imported as user-defined phrases

It can also import a Gboard exported text dictionary and a Microsoft Pinyin `.dat` file back into `book.txt`.

**The UI is available in Chinese and English**: the language is picked automatically from the system language at startup, and can be switched any time from the top-right corner.

## 2. Installation

### Option 1: run the Python script
```bash
python ms_manager.py
```

### Option 2: run the executable
Double-click `微软拼音词库管理器.exe`.

> The **v1.0 release is source-only — there is no official exe yet**. If you need one, build it yourself from `ms_manager.py` with PyInstaller.

**Note**: `book.txt` is created automatically next to the program.

## 3. Main Window

```
┌────────────────────────────────────────────────────────────────────────────┐
│ Search: [      ] [Add] [Delete] [Import Gboard] [Import DAT] [Export Gboard] [Export DAT] [Save] [Open Folder]      Language: [English ▾] │
├────────────────────────────────────────────────────────────────────────────┤
│ Total: 33 | Unique shortcuts: 33 | Duplicated: 0                            │
├────────────────────────────────────────────────────────────────────────────┤
│   Phrase    │ Shortcut       │ Position                                     │
│  ───────────┼────────────────┼────────────────────────────────────────────  │
│   ad        │ adb devices    │ 1                                           │
│   xm        │ 小米9           │ 1                                           │
│   gp        │ git push       │ 1                                           │
├────────────────────────────────────────────────────────────────────────────┤
│ Showing 33 / 33                                                  Ready      │
└────────────────────────────────────────────────────────────────────────────┘
```

### 3.1 Interface language (top-right)

- **Auto-detected at startup**: on Windows the system display language is read — Chinese systems get the Chinese UI, everything else gets English
- **Switch any time**: pick `中文` or `English` in the `Language:` dropdown; every label, column header, status bar, context menu and dialog is re-translated immediately
- Switching only changes the interface language — it never touches your data or the exported files

## 4. Basic Operations

### 4.1 Search
Type in the search box to filter entries live (matches either the phrase or the shortcut).

### 4.2 Add an entry
1. Click **Add**
2. Enter the phrase (e.g. `hello`)
3. Enter the shortcut (e.g. `he`)
4. Pick a position (1-9, smaller comes first)
5. Click **OK**

### 4.3 Edit an entry
- **Double-click** any row, or right-click → **Edit**
- Change the values and click **OK**

### 4.4 Delete entries
- Select the rows (multi-select supported) and press `Delete`
- Or click **Delete**, or right-click → **Delete**

### 4.5 Multi-select

| Action | Effect |
| --- | --- |
| `Ctrl + click` | toggle a single row |
| `Shift + click` | select a contiguous range |
| `Ctrl + A` | select all |
| `Delete` | delete the selection |

## 5. Import / Export

### 5.1 Import a Gboard dictionary
1. On the phone: Gboard → Dictionary → Personal dictionary → Export, which produces `PersonalDictionary-*.zip`
2. **Unzip it first** and take out the inner `dictionary.txt` (this tool reads plain text only, it does not unzip archives)
3. Copy the `.txt` to the PC
4. Click **Import Gboard** and pick the file
5. Entries are merged with de-duplication; entries sharing the same shortcut are appended with increasing positions (max 9)

> A dictionary exported by the new Gboard starts with `# Gboard Dictionary version:2` and a format line; each entry has four tab-separated fields: `shortcut → word → language_tag → pos_tag`. The importer skips `#` header lines and strips the trailing language tag.

### 5.2 Import a Microsoft Pinyin DAT
1. Export the user-defined phrases from Microsoft Pinyin settings (a `.dat` file)
2. Click **Import DAT** and pick the file
3. Entries are parsed and merged (the position stored in each DAT entry is kept)

### 5.3 Export a Gboard dictionary package (zip)
1. Click **Export Gboard**
2. Pick a location; the default name is `Gboard_Dictionary_<timestamp>.zip`
3. The result is **one zip** split by language:

```
Gboard_Dictionary_20261117_223000.zip
├─ dictionary_zh-CN.txt     ← entries containing Chinese
└─ dictionary_zz.txt        ← pure ASCII entries
```

- **Language detection**: a phrase containing Chinese characters (base block, extension A, compatibility block, full-width punctuation) → `zh-CN`; anything else → `zz`
- **One language per file**, never mixed; if a language has no entry, that file is simply absent from the zip
- Every inner txt follows Gboard's `version:2` format: two fixed header lines, four fields per entry, a trailing tab, LF-only line endings, UTF-8 without BOM
- **Post-export self-check**: the file just written is read back and validated (header, line endings, column layout). If anything is off, an error dialog is shown instead of a false "success"
- On the phone: copy the zip over → Gboard → Dictionary → Personal dictionary → Import → choose the zip

### 5.4 Export a Microsoft Pinyin DAT
1. Click **Export DAT**
2. Pick a location; the default name is `ms_export_<timestamp>.dat`
3. Import it in Microsoft Pinyin's user-defined phrases (see `微软格式说明文档.md` for the byte-level format)

### 5.5 Save
**Save** writes the current data back to `book.txt`, backing up the previous file as `book.txt.bak`.

## 6. Files

| File | Description |
| --- | --- |
| `book.txt` | the single internal dictionary, three tab-separated columns |
| `book.txt.bak` | automatic backup created on save |
| `ms_manager.py` / `*.exe` | the application |
| `Gboard_Dictionary_*.zip` | Gboard export (may contain several `dictionary_*.txt`) |
| `ms_export_*.dat` | Microsoft Pinyin export |
| `微软格式说明文档.md` | `.dat` format reference |

## 7. book.txt format

Three tab-separated columns, read and written in order:

```
# 微软拼音词库 - 统一格式
# 更新时间: 2026-11-17 22:30:00
# 总计: 3 条
# 格式: 短语	编码	候选位置
#--------------------------------------------------
ad	adb devices	1
xm	小米9	1
gp	git push	1
```

### ⚠ Known column-order issue

The header written by the program says "phrase, shortcut, position" and the table headers say "Phrase | Shortcut", but **in the current `book.txt` the first column actually holds the shortcut** (the data originated from a Gboard import, which stores the first field as the shortcut).

Consequences (all from the same root cause):

- **Gboard export** treats column 1 as the shortcut and column 2 as the phrase, which matches the real data → verified working
- **DAT export** treats column 2 as the shortcut and column 1 as the phrase → the DAT ends up with the long phrase as shortcut and the short code as phrase (see Q7)
- **The stats bar** counts unique/duplicated shortcuts on column 2, so it currently shows "unique 33, duplicated 0"; counting the real shortcut column it would be 32 unique with one duplicate (`xm` twice)
- **The table** therefore shows the shortcut under the "Phrase" header

Unifying the column order requires either migrating the data or changing the mappings; that is a separate change and is **not** done in this version.

## 8. FAQ

### Q1: "book.txt not found" on startup
A: It is created automatically; this is normal on first run.

### Q2: "Encoding error" when importing a Gboard file
A: Make sure it is UTF-8 plain text. If you have the `.zip` exported by the phone, unzip it first and import the inner `.txt`.

### Q3: Garbled text after importing the DAT into Microsoft Pinyin
A: Check the contents of `book.txt`, and read Q7 about the column order first.

### Q4: How do I back up my dictionary?
A: Copy `book.txt`. Every save also produces `book.txt.bak`.

### Q5: Which Windows versions are supported?
A: Windows 10 / Windows 11.

### Q6: After importing the zip, the phone dictionary is empty
A: Check in this order:
1. Was the zip produced by this version? A `.txt` from an older version uses the old header, which the new Gboard rejects and imports nothing
2. Was the zip unzipped and renamed? Import the original zip as-is instead of a single inner txt
3. In Gboard → Dictionary → Personal dictionary, check which dictionary the entries landed in

### Q7: In the DAT, typing a long string produces a short code
A: This comes from the column-order mismatch described in section 7 — DAT export takes column 2 as the shortcut while the real data has the phrase there. Unify the column order before relying on DAT export.

### Q8: The UI is in English, can I get Chinese back?
A: Pick `中文` in the `Language:` dropdown at the top-right. It only affects the interface, not your data or the exports.

## 9. Shortcuts

| Key | Action |
| --- | --- |
| `Ctrl + A` | select all |
| `Delete` | delete selection |
| double-click | edit an entry |

## 10. Feedback

Issues and suggestions are welcome.

---

**Version**: 1.0
**Date**: 2026-11-17
**This release**: Gboard `version:2` dictionary format support, zip export, post-export self-check, and a bilingual (Chinese / English) UI.

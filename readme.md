**中文** ｜ [English](#english-manual)

# 微软拼音词库管理器 使用手册

> **⬇️ 下载最新版**：请到 [Releases](https://github.com/luckyme258/gboard2ms_win11/releases/latest) 下载 **v1.0**。
>
> **⚠️ v0.1 / v0.2 已停止维护**：这两个旧版的 Gboard 导出还是旧格式 txt，导入新版安卓 Gboard 只会得到**空词典**，请勿下载使用。

## 一、简介

微软拼音词库管理器是一个图形化工具，用于管理输入法的自定义短语词库，在内置的 `book.txt` 里统一维护一套条目，再分别导出到两套输入法：

- **Gboard（安卓）**：导出为新版 Gboard 词典包（`.zip`，内含按语言拆分的 `dictionary_*.txt`），可直接在手机 Gboard 的个人词典里导入
- **微软拼音（Windows）**：导出为 `.dat`，可在微软拼音的用户自定义短语里导入

同时支持反向导入：**直接导入手机导出的 Gboard 词典 zip**（不必解压），或导入旧的纯文本词库、微软拼音的 `.dat`。

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
│ 搜索: [        ] [添加] [删除] [导入 Gboard（zip/txt）] [导入 DAT] [导出 Gboard] [导出 DAT] [保存] [打开文件夹]      语言: [中文 ▾] │
├──────────────────────────────────────────────────────────────────────────────┤
│ 总计: 32 条 | 唯一编码: 31 个 | 重复编码: 1 个                                  │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  短语              │ 编码            │ 候选位置                                  │
│  ─────────────────┼────────────────┼─────────────────────────────────────── │
│  adb devices      │ ad             │ 1                                        │
│  小米9             │ xm             │ 1                                        │
│  git push         │ gp             │ 1                                        │
│  ...              │ ...            │ ...                                      │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│ 显示 32 / 32 条                                                    就绪        │
└──────────────────────────────────────────────────────────────────────────────┘
```

> 表格列序与 `book.txt` 的存储顺序是分开的两件事：表格**按「短语在前、编码在后」显示**，`book.txt` **按「编码在前、短语在后」保存**。程序内部统一以「第 1 列 = 编码（shortcut）、第 2 列 = 短语（word）」为唯一约定，详见第七章。

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
2. 把这个 **zip 原样**传到电脑（不需要解压，程序会自己读里面的 `dictionary_*.txt`）
3. 点击「导入 Gboard（zip/txt）」，选择该 zip
4. 程序自动按语言分组读入、去重合并；同编码的多条会按候选位置依次往后排（上限 9）

> - zip 里的文件按内容识别，文件名不必严格叫 `dictionary_zh-CN.txt`；`__MACOSX/`、隐藏文件、目录项会自动跳过
> - 单个 zip 限制 50 个文件 / 20 MB，超限会直接中止并提示，不写入任何数据
> - 仍然兼容旧的纯文本词库：单个 `dictionary.txt` / 2 列旧格式 `.txt` 也能导入，提示里会标注「其中旧格式 N 条」
> - 新版格式：第 1 行 `# Gboard Dictionary version:2`，第 2 行格式声明，条目为 `编码 → 短语 → 语言标签 → 候选标记` 四列，行尾保留 Tab
> - 缺少 `version:2` 头部会照常解析，但会在结果提示里给出告警

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

内部格式为 Tab 分隔的三列，**第 1 列是编码（shortcut）、第 2 列是短语（word）、第 3 列是候选位置**，程序内部只有这一种约定：

```
# 微软拼音词库 - 统一格式
# 更新时间: 2026-11-18 01:10:00
# 总计: 3 条
# 格式: 编码	短语	候选位置
#--------------------------------------------------
ad	adb devices	1
xm	小米9	1
gp	git push	1
```

### 7.1 列序约定（v1.0 起已统一）

界面表格按「短语 | 编码 | 候选位置」显示，`book.txt` 按「编码 | 短语 | 候选位置」保存，两者只是显示与存储的差别，内部只有一套顺序，不会再出现显示相反的情况。

| 场景 | 取哪一列 | 状态 |
| ---- | -------- | ---- |
| 界面表格 | 第 2 列显示在「短语」、第 1 列显示在「编码」 | 正确 |
| 统计栏「唯一编码 / 重复编码」 | 按第 1 列（编码）统计 | 正确（现为 32 条、31 个唯一、1 组重复 `xm`） |
| Gboard 导出（zip） | 第 1 列 = shortcut、第 2 列 = word | 正确 |
| DAT 导出 | 第 1 列 = 编码、第 2 列 = 短语 | 正确 |
| Gboard 导入 / DAT 导入 | 写回时统一转成「编码在前、短语在后」 | 正确 |

> 旧版本（6 月发布的 v0.1 / v0.2 exe）存在列序反转：界面把编码显示在「短语」列、DAT 导出把长句写进编码字段、统计栏按短语统计。v1.0 已全部修正。若用旧版导入过词库，请检查 `book.txt` 里是否出现「中文短语在第 1 列」的行——本项目现有 32 条数据经检查全部正常，无需迁移。

## 八、常见问题

### Q1: 打开程序提示「book.txt 不存在」
A: 程序会自动创建，首次运行正常现象。

### Q2: 导入 Gboard 文件提示「编码错误」
A: 先确认选的文件本身是不是有效：`.zip` 请直接用手机导出的原始 zip（程序会读包内的 `dictionary_*.txt`，不用先解压）；纯文本请确保是 UTF-8 编码。若提示「不是有效的 zip 文件」，说明文件后缀是 zip 但内容已损坏或被改名。

### Q3: 导出的 DAT 导入微软拼音后乱码
A: 先确认 `book.txt` 内容是否正确（编码在前、短语在后），再用 v1.0 重新导出；旧的 DAT 建议不要再用。

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
A: 这是旧版本（v0.1 / v0.2）的列序反转造成的：旧版 DAT 导出把短语当编码写进 DAT。v1.0 已修正，重新导出一次 DAT 即可；旧版导出的 `.dat` 建议丢弃重导。

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
**更新日期**：2026-11-18
**本次更新**：适配新版 Gboard（`version:2`）词典格式、导出改为 zip 词典包、**支持直接导入手机导出的 zip**、统一列序（修复表格反序与 DAT 字段反转）、新增导出后自检、界面支持中文/English 双语。详见《更新日志.md》。

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

It can also import backwards: **the Gboard dictionary zip exported by the phone** (no unzipping needed), legacy plain-text dictionaries, and Microsoft Pinyin `.dat` files.

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
│ Search: [      ] [Add] [Delete] [Import Gboard (zip/txt)] [Import DAT] [Export Gboard] [Export DAT] [Save] [Open Folder]      Language: [English ▾] │
├────────────────────────────────────────────────────────────────────────────┤
│ Total: 32 | Unique shortcuts: 31 | Duplicated: 1                            │
├────────────────────────────────────────────────────────────────────────────┤
│   Phrase    │ Shortcut       │ Position                                     │
│  ───────────┼────────────────┼────────────────────────────────────────────  │
│   adb devices │ ad           │ 1                                           │
│   小米9        │ xm           │ 1                                           │
│   git push  │ gp             │ 1                                           │
├────────────────────────────────────────────────────────────────────────────┤
│ Showing 32 / 32                                                  Ready      │
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
2. Copy that **zip as-is** to the PC — no need to unzip; the tool reads the inner `dictionary_*.txt` itself
3. Click **Import Gboard (zip/txt)** and pick the zip
4. Entries are grouped by language, merged with de-duplication; entries sharing the same shortcut are appended with increasing positions (max 9)

> - Files inside the zip are recognised by content, so they do not have to be named `dictionary_zh-CN.txt` exactly; `__MACOSX/`, hidden files and directory entries are skipped
> - A single zip is limited to 50 files / 20 MB; anything larger aborts with an error and nothing is written
> - Legacy plain-text dictionaries still import: a single `dictionary.txt` or an old two-column `.txt` works, and the result message marks "N legacy row(s)"
> - New format: `# Gboard Dictionary version:2` on line 1, the format line on line 2, then four tab-separated fields `shortcut → word → language_tag → pos_tag` with a trailing tab
> - A missing `version:2` header is still parsed, but the result message warns about it

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

Three tab-separated columns: **column 1 = shortcut, column 2 = phrase (word), column 3 = position**. This is the only internal convention the program uses.

```
# 微软拼音词库 - 统一格式
# 更新时间: 2026-11-18 01:10:00
# 总计: 3 条
# 格式: 编码	短语	候选位置
#--------------------------------------------------
ad	adb devices	1
xm	小米9	1
gp	git push	1
```

### 7.1 Column order (unified as of v1.0)

The table displays "Phrase | Shortcut | Position" while `book.txt` stores "shortcut | phrase | position" — that is only a display/storage difference; internally there is a single order, so the reversed display of older builds cannot happen.

| Where | Which column is used | Status |
| --- | --- | --- |
| Table | column 2 shown under "Phrase", column 1 under "Shortcut" | correct |
| Stats bar (unique / duplicated shortcuts) | counted on column 1 | correct (currently 32 entries, 31 unique, 1 duplicate `xm`) |
| Gboard export (zip) | column 1 = shortcut, column 2 = word | correct |
| DAT export | column 1 = shortcut, column 2 = phrase | correct |
| Gboard import / DAT import | normalised to "shortcut first, phrase second" when written back | correct |

> Builds v0.1 / v0.2 (June) had the reversal: the table showed shortcuts under "Phrase", DAT export wrote the long phrase into the shortcut field, and the stats bar counted phrases. v1.0 fixes all of it. If you imported data with an old build, check whether any row has a Chinese phrase in column 1 — the 32 entries shipped here were audited and are all fine, so no migration is needed.

## 8. FAQ

### Q1: "book.txt not found" on startup
A: It is created automatically; this is normal on first run.

### Q2: "Encoding error" when importing a Gboard file
A: First check the file itself: for a `.zip`, use the original zip exported by the phone (the tool reads the inner `dictionary_*.txt`, no unzipping needed); for plain text, make sure it is UTF-8. An error saying it is not a valid zip means the extension says zip but the archive is corrupt or was renamed.

### Q3: Garbled text after importing the DAT into Microsoft Pinyin
A: Check that `book.txt` has shortcut first, phrase second, then re-export with v1.0; discard DAT files produced by older builds.

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
A: That is the reversal of builds v0.1 / v0.2, which wrote the phrase into the DAT shortcut field. v1.0 fixes it — just export the DAT again; DAT files from older builds should be discarded.

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
**Date**: 2026-11-18
**This release**: Gboard `version:2` dictionary format support, zip export, **direct import of the phone-exported zip**, unified column order (table display and DAT fields fixed), post-export self-check, and a bilingual (Chinese / English) UI.

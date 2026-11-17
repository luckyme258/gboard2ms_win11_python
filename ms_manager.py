#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微软拼音词库管理器 - 统一版
内部格式: book.txt (短语\t编码\t候选位置)
支持导入: Gboard TXT、微软拼音 DAT
支持导出: Gboard 词典包(ZIP)、微软拼音 DAT
界面语言: 启动时按系统语言自动选择（中文 / English），可在右上角手动切换
"""

import os
import re
import sys
import struct
import locale
import zipfile
import platform
import subprocess
import shutil
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from collections import defaultdict
from datetime import datetime
from pathlib import Path


def get_base_path():
    """获取可执行文件所在目录（兼容 Python 脚本和打包后的 exe）"""
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    else:
        return Path(__file__).parent


# 获取脚本所在目录
SCRIPT_DIR = get_base_path()
BOOK_FILE = SCRIPT_DIR / "book.txt"


# ========== 界面多语言 ==========

LANG_LABELS = {"zh": "中文", "en": "English"}

UI_TEXT = {
    "zh": {
        "title": "微软拼音词库管理器",
        "search": "搜索:",
        "add": "添加",
        "delete": "删除",
        "import_gboard": "导入 Gboard",
        "import_dat": "导入 DAT",
        "export_gboard": "导出 Gboard",
        "export_dat": "导出 DAT",
        "save": "保存",
        "open_folder": "打开文件夹",
        "language": "语言:",
        "col_phrase": "短语",
        "col_code": "编码",
        "col_position": "候选位置",
        "stats": "总计: {total} 条 | 唯一编码: {unique} 个 | 重复编码: {dup} 个",
        "status_ready": "就绪",
        "status_no_book": "book.txt 不存在，将创建新文件",
        "status_loaded": "已加载 {n} 条短语",
        "status_display": "显示 {shown} / {total} 条",
        "status_saved": "已保存到 book.txt ({n} 条)",
        "menu_edit": "编辑",
        "menu_delete": "删除",
        "hint": "提示",
        "warning": "警告",
        "error": "错误",
        "confirm_delete": "确认删除",
        "confirm_delete_msg": "确定要删除选中的 {n} 条词条吗？",
        "warn_select_first": "请先选中要删除的词条",
        "dlg_add_title": "添加短语",
        "dlg_edit_title": "编辑短语",
        "lbl_phrase": "短语:",
        "lbl_code": "编码:",
        "lbl_position": "候选位置(1-9):",
        "btn_ok": "确定",
        "btn_cancel": "取消",
        "err_fields_empty": "短语和编码不能为空",
        "err_dup_entry": "短语 '{phrase}' 与编码 '{code}' 已存在",
        "import_done_title": "导入完成",
        "import_done_msg": "成功导入 {n} 条新短语",
        "import_none": "未从文件中解析到有效条目",
        "import_enc_err": "文件编码错误，请确保文件是 UTF-8 编码的文本文件",
        "import_gboard_title": "选择 Gboard 导出的文件",
        "select_dat_title": "选择微软拼音 DAT 文件",
        "export_empty": "词库为空，无法导出",
        "ask_export_gboard": "导出为 Gboard 词典包",
        "ask_export_dat": "导出为微软拼音格式",
        "export_ok_title": "导出成功",
        "ft_zip": "Zip 压缩包",
        "ft_txt": "文本文件",
        "ft_dat": "DAT文件",
        "ft_all": "所有文件",
        "lang_detail": "{tag} {n} 条",
        "list_sep": "，",
        "export_gboard_msg": "已导出 {count} 条（{detail}）到\n{path}\n\n把该 zip 导入手机 Gboard 个人词典即可",
        "export_dat_msg": "已导出 {count} 条短语到\n{path}\n\n可在微软拼音中导入使用",
        "selfcheck_failed": "自检失败",
        "selfcheck_msg": "生成的文件不合规：{err}",
        "selfcheck_header": "{name} 头部不符",
        "selfcheck_cr": "{name} 含 CR，换行应为纯 LF",
        "selfcheck_cols": "{name} 列结构不符：{line}",
        "save_ok_title": "保存成功",
        "save_ok_msg": "已保存 {n} 条短语到 book.txt",
        "save_fail_title": "保存失败",
        "save_fail_msg": "无法保存文件：{err}",
        "load_fail_title": "加载失败",
        "load_fail_msg": "无法读取 book.txt：{err}",
        "parse_fail_title": "解析失败",
        "parse_fail_msg": "无法解析 DAT 文件：{err}",
    },
    "en": {
        "title": "Microsoft Pinyin Dictionary Manager",
        "search": "Search:",
        "add": "Add",
        "delete": "Delete",
        "import_gboard": "Import Gboard",
        "import_dat": "Import DAT",
        "export_gboard": "Export Gboard",
        "export_dat": "Export DAT",
        "save": "Save",
        "open_folder": "Open Folder",
        "language": "Language:",
        "col_phrase": "Phrase",
        "col_code": "Shortcut",
        "col_position": "Position",
        "stats": "Total: {total} | Unique shortcuts: {unique} | Duplicated: {dup}",
        "status_ready": "Ready",
        "status_no_book": "book.txt not found, a new one will be created",
        "status_loaded": "Loaded {n} entries",
        "status_display": "Showing {shown} / {total}",
        "status_saved": "Saved to book.txt ({n} entries)",
        "menu_edit": "Edit",
        "menu_delete": "Delete",
        "hint": "Hint",
        "warning": "Warning",
        "error": "Error",
        "confirm_delete": "Confirm delete",
        "confirm_delete_msg": "Delete the selected entries? ({n} in total)",
        "warn_select_first": "Please select the entries to delete first",
        "dlg_add_title": "Add Entry",
        "dlg_edit_title": "Edit Entry",
        "lbl_phrase": "Phrase:",
        "lbl_code": "Shortcut:",
        "lbl_position": "Position (1-9):",
        "btn_ok": "OK",
        "btn_cancel": "Cancel",
        "err_fields_empty": "Phrase and shortcut cannot be empty",
        "err_dup_entry": "Phrase '{phrase}' with shortcut '{code}' already exists",
        "import_done_title": "Import finished",
        "import_done_msg": "Imported {n} new entries",
        "import_none": "No valid entry found in the file",
        "import_enc_err": "Encoding error: the file must be UTF-8 text",
        "import_gboard_title": "Select a Gboard exported file",
        "select_dat_title": "Select a Microsoft Pinyin DAT file",
        "export_empty": "The dictionary is empty, nothing to export",
        "ask_export_gboard": "Export Gboard dictionary package",
        "ask_export_dat": "Export Microsoft Pinyin DAT",
        "export_ok_title": "Export finished",
        "ft_zip": "Zip archive",
        "ft_txt": "Text file",
        "ft_dat": "DAT file",
        "ft_all": "All files",
        "lang_detail": "{tag}: {n} entries",
        "list_sep": ", ",
        "export_gboard_msg": "Exported {count} entries ({detail}) to\n{path}\n\nImport this zip in Gboard > Dictionary > Personal dictionary",
        "export_dat_msg": "Exported {count} entries to\n{path}\n\nImport it in Microsoft Pinyin",
        "selfcheck_failed": "Self-check failed",
        "selfcheck_msg": "The generated file is not compliant: {err}",
        "selfcheck_header": "{name}: bad header",
        "selfcheck_cr": "{name}: contains CR, line endings must be LF only",
        "selfcheck_cols": "{name}: bad column layout: {line}",
        "save_ok_title": "Saved",
        "save_ok_msg": "Saved {n} entries to book.txt",
        "save_fail_title": "Save failed",
        "save_fail_msg": "Cannot save the file: {err}",
        "load_fail_title": "Load failed",
        "load_fail_msg": "Cannot read book.txt: {err}",
        "parse_fail_title": "Parse failed",
        "parse_fail_msg": "Cannot parse the DAT file: {err}",
    },
}


def detect_language():
    """启动时按系统语言选择界面语言：中文系统用中文，其余用英文"""
    # Windows：直接读系统 UI 语言 ID（最可靠）
    if platform.system() == "Windows":
        try:
            import ctypes
            lang_id = ctypes.windll.kernel32.GetUserDefaultUILanguage()
            primary = lang_id & 0x3FF
            return "zh" if primary == 0x04 else "en"
        except Exception:
            pass
    # 其它平台：locale / 环境变量
    try:
        candidates = [locale.getlocale()[0], os.environ.get("LC_ALL"),
                      os.environ.get("LC_MESSAGES"), os.environ.get("LANG")]
        for item in candidates:
            if not item:
                continue
            if str(item).lower().startswith("zh"):
                return "zh"
            if str(item).lower().startswith("en"):
                return "en"
    except Exception:
        pass
    return "en"



class MsPhraseManager:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x700")
        
        # 内部数据存储 (phrase, code, position)
        self.phrases = []
        self.filtered = []
        self.search_var = tk.StringVar()
        
        # 界面语言：默认跟随系统，用户可在右上角切换
        self.lang = detect_language()
        self.lang_var = tk.StringVar(value=LANG_LABELS[self.lang])
        
        self.setup_ui()
        self.apply_language()
        self.load_book()
    
    def t(self, key, **kwargs):
        """取界面文案：当前语言 → 中文回退 → 键名"""
        table = UI_TEXT.get(self.lang) or UI_TEXT["zh"]
        text = table.get(key) or UI_TEXT["zh"].get(key, key)
        if kwargs:
            try:
                return text.format(**kwargs)
            except Exception:
                return text
        return text
    
    def apply_language(self):
        """把当前语言套用到所有已创建的控件上"""
        self.root.title(self.t("title"))
        self.lang_var.set(LANG_LABELS[self.lang])
        self.lang_label.config(text=self.t("language"))
        self.search_label.config(text=self.t("search"))
        self.btn_add.config(text=self.t("add"))
        self.btn_delete.config(text=self.t("delete"))
        self.btn_import_gboard.config(text=self.t("import_gboard"))
        self.btn_import_dat.config(text=self.t("import_dat"))
        self.btn_export_gboard.config(text=self.t("export_gboard"))
        self.btn_export_dat.config(text=self.t("export_dat"))
        self.btn_save.config(text=self.t("save"))
        self.btn_open_folder.config(text=self.t("open_folder"))
        self.tree.heading("短语", text=self.t("col_phrase"))
        self.tree.heading("编码", text=self.t("col_code"))
        self.tree.heading("候选位置", text=self.t("col_position"))
        self.context_menu.entryconfig(0, label=self.t("menu_edit"))
        self.context_menu.entryconfig(1, label=self.t("menu_delete"))
        self.update_stats()
        self.refresh_display()
    
    def on_language_change(self, event=None):
        """用户在右上角手动切换语言"""
        for code, label in LANG_LABELS.items():
            if label == self.lang_var.get():
                self.lang = code
                break
        self.apply_language()
    
    def setup_ui(self):
        # 工具栏（左侧功能按钮，右上角语言选择）
        toolbar = ttk.Frame(self.root)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        self.search_label = ttk.Label(toolbar, text="")
        self.search_label.pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(toolbar, textvariable=self.search_var, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind('<KeyRelease>', self.on_search)
        
        self.btn_add = ttk.Button(toolbar, command=self.add_phrase)
        self.btn_add.pack(side=tk.LEFT, padx=5)
        self.btn_delete = ttk.Button(toolbar, command=self.delete_selected)
        self.btn_delete.pack(side=tk.LEFT, padx=5)
        self.btn_import_gboard = ttk.Button(toolbar, command=self.import_gboard)
        self.btn_import_gboard.pack(side=tk.LEFT, padx=5)
        self.btn_import_dat = ttk.Button(toolbar, command=self.import_ms_dat)
        self.btn_import_dat.pack(side=tk.LEFT, padx=5)
        self.btn_export_gboard = ttk.Button(toolbar, command=self.export_gboard)
        self.btn_export_gboard.pack(side=tk.LEFT, padx=5)
        self.btn_export_dat = ttk.Button(toolbar, command=self.export_dat)
        self.btn_export_dat.pack(side=tk.LEFT, padx=5)
        self.btn_save = ttk.Button(toolbar, command=self.save_book)
        self.btn_save.pack(side=tk.LEFT, padx=5)
        self.btn_open_folder = ttk.Button(toolbar, command=self.open_folder)
        self.btn_open_folder.pack(side=tk.LEFT, padx=5)
        
        # 右上角：语言选择
        self.lang_combo = ttk.Combobox(
            toolbar, textvariable=self.lang_var, width=9, state="readonly",
            values=list(LANG_LABELS.values()))
        self.lang_combo.pack(side=tk.RIGHT, padx=5)
        self.lang_combo.bind('<<ComboboxSelected>>', self.on_language_change)
        self.lang_label = ttk.Label(toolbar, text="")
        self.lang_label.pack(side=tk.RIGHT, padx=(10, 0))
        
        # 显示统计
        self.stats_label = ttk.Label(self.root, text="", relief=tk.SUNKEN, anchor=tk.W)
        self.stats_label.pack(fill=tk.X, side=tk.TOP, padx=5, pady=2)
        
        # 表格
        frame = ttk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        columns = ("短语", "编码", "候选位置")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", selectmode="extended")
        self.tree.heading("短语", text="")
        self.tree.heading("编码", text="")
        self.tree.heading("候选位置", text="")
        
        # 增大列宽以适应更大的字体
        self.tree.column("短语", width=500)
        self.tree.column("编码", width=200)
        self.tree.column("候选位置", width=100)
        
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 设置字体（全局样式）
        style = ttk.Style()
        style.configure("Treeview", font=("微软雅黑", 11), rowheight=30)
        style.configure("Treeview.Heading", font=("微软雅黑", 11, "bold"))
        style.configure("TLabel", font=("微软雅黑", 10))
        style.configure("TButton", font=("微软雅黑", 10))
        style.configure("TEntry", font=("微软雅黑", 10))
        style.configure("TCombobox", font=("微软雅黑", 10))
        
        self.tree.bind("<Double-1>", self.edit_phrase)
        # 绑定 Delete 键删除
        self.tree.bind("<Delete>", lambda e: self.delete_selected())
        # 绑定 Ctrl+A 全选
        self.tree.bind("<Control-a>", self.select_all)
        self.tree.bind("<Control-A>", self.select_all)
        
        self.context_menu = tk.Menu(self.root, tearoff=0, font=("微软雅黑", 10))
        self.context_menu.add_command(label="", command=self.edit_phrase)
        self.context_menu.add_command(label="", command=self.delete_selected)
        self.tree.bind("<Button-3>", self.show_context_menu)
        
        # 底部状态栏
        self.status = ttk.Label(self.root, text=self.t("status_ready"), relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(fill=tk.X, side=tk.BOTTOM, padx=5, pady=2)
    
    # ========== 全选功能 ==========
    
    def select_all(self, event=None):
        """Ctrl+A 全选"""
        for item in self.tree.get_children():
            self.tree.selection_add(item)
        return "break"
    
    # ========== 批量删除 ==========
    
    def delete_selected(self):
        """删除选中的词条（支持多选）"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning(self.t("hint"), self.t("warn_select_first"))
            return
        
        if messagebox.askyesno(self.t("confirm_delete"), self.t("confirm_delete_msg", n=len(selected))):
            # 获取所有选中的值
            to_delete = []
            for item in selected:
                values = self.tree.item(item, "values")
                if values and len(values) >= 3:
                    to_delete.append((values[0], values[1], int(values[2])))
            
            # 从数据中删除
            for phrase, code, pos in to_delete:
                for i, (p, c, position) in enumerate(self.phrases):
                    if p == phrase and c == code and position == pos:
                        del self.phrases[i]
                        break
            
            self.refresh_display()
            self.update_stats()
    
    # ========== 内部格式 (book.txt) 操作 ==========
    
    def load_book(self):
        """加载 book.txt 到内存"""
        self.phrases = []
        if not BOOK_FILE.exists():
            self.status.config(text=self.t("status_no_book"))
            self.update_stats()
            self.refresh_display()
            return
        
        try:
            with open(BOOK_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.rstrip('\n')
                    if not line or line.startswith('#'):
                        continue
                    parts = line.split('\t')
                    if len(parts) >= 2:
                        phrase = parts[0].strip()
                        code = parts[1].strip()
                        position = 1
                        if len(parts) >= 3 and parts[2].strip().isdigit():
                            position = int(parts[2].strip())
                        self.phrases.append((phrase, code, position))
            self.status.config(text=self.t("status_loaded", n=len(self.phrases)))
        except Exception as e:
            messagebox.showerror(self.t("load_fail_title"), self.t("load_fail_msg", err=e))
        
        self.update_stats()
        self.refresh_display()
    
    def save_book(self):
        """保存到 book.txt"""
        try:
            if BOOK_FILE.exists():
                backup = BOOK_FILE.with_suffix(".txt.bak")
                shutil.copy(BOOK_FILE, backup)
            
            with open(BOOK_FILE, 'w', encoding='utf-8') as f:
                f.write("# 微软拼音词库 - 统一格式\n")
                f.write(f"# 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"# 总计: {len(self.phrases)} 条\n")
                f.write("# 格式: 短语\t编码\t候选位置\n")
                f.write("#" + "-" * 50 + "\n")
                for phrase, code, position in self.phrases:
                    f.write(f"{phrase}\t{code}\t{position}\n")
            
            self.status.config(text=self.t("status_saved", n=len(self.phrases)))
            messagebox.showinfo(self.t("save_ok_title"), self.t("save_ok_msg", n=len(self.phrases)))
        except Exception as e:
            messagebox.showerror(self.t("save_fail_title"), self.t("save_fail_msg", err=e))
    
    def update_stats(self):
        """更新统计信息"""
        code_count = defaultdict(int)
        for _, code, _ in self.phrases:
            code_count[code] += 1
        multi_codes = {k: v for k, v in code_count.items() if v > 1}
        
        stats = self.t("stats", total=len(self.phrases), unique=len(code_count), dup=len(multi_codes))
        self.stats_label.config(text=stats)
    
    # ========== 表格显示 ==========
    
    def refresh_display(self):
        search_text = self.search_var.get().strip().lower()
        if search_text:
            self.filtered = [p for p in self.phrases 
                           if search_text in p[0].lower() or search_text in p[1].lower()]
        else:
            self.filtered = self.phrases.copy()
        self.update_tree()
        self.status.config(text=self.t("status_display", shown=len(self.filtered), total=len(self.phrases)))
    
    def update_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for phrase, code, position in self.filtered:
            self.tree.insert("", tk.END, values=(phrase, code, position))
    
    def on_search(self, event=None):
        self.refresh_display()
    
    # ========== 增删改查 ==========
    
    def add_phrase(self):
        dialog = tk.Toplevel(self.root)
        dialog.title(self.t("dlg_add_title"))
        dialog.geometry("450x280")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text=self.t("lbl_phrase")).grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        text_entry = ttk.Entry(dialog, width=45)
        text_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text=self.t("lbl_code")).grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        code_entry = ttk.Entry(dialog, width=45)
        code_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text=self.t("lbl_position")).grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        position_spin = ttk.Spinbox(dialog, from_=1, to=9, width=10)
        position_spin.insert(0, "1")
        position_spin.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        
        def save():
            phrase = text_entry.get().strip()
            code = code_entry.get().strip()
            position = int(position_spin.get())
            if not phrase or not code:
                messagebox.showerror(self.t("error"), self.t("err_fields_empty"))
                return
            for p, c, pos in self.phrases:
                if p == phrase and c == code:
                    messagebox.showerror(self.t("error"), self.t("err_dup_entry", phrase=phrase, code=code))
                    return
            self.phrases.append((phrase, code, position))
            self.refresh_display()
            self.update_stats()
            dialog.destroy()
        
        ttk.Button(dialog, text=self.t("btn_ok"), command=save).grid(row=3, column=0, pady=10)
        ttk.Button(dialog, text=self.t("btn_cancel"), command=dialog.destroy).grid(row=3, column=1, pady=10)
    
    def edit_phrase(self, event=None):
        # 获取选中的项目（支持双击编辑第一个选中的）
        selected = self.tree.selection()
        if not selected:
            # 如果没有选中，尝试获取焦点项目
            item = self.tree.focus()
            if not item:
                return
        else:
            item = selected[0]
        
        values = self.tree.item(item, "values")
        if not values or len(values) < 2:
            return
        old_phrase, old_code, old_position = values[0], values[1], int(values[2])
        
        dialog = tk.Toplevel(self.root)
        dialog.title(self.t("dlg_edit_title"))
        dialog.geometry("450x280")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text=self.t("lbl_phrase")).grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        text_entry = ttk.Entry(dialog, width=45)
        text_entry.insert(0, old_phrase)
        text_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text=self.t("lbl_code")).grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        code_entry = ttk.Entry(dialog, width=45)
        code_entry.insert(0, old_code)
        code_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text=self.t("lbl_position")).grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        position_spin = ttk.Spinbox(dialog, from_=1, to=9, width=10)
        position_spin.insert(0, str(old_position))
        position_spin.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        
        def save():
            new_phrase = text_entry.get().strip()
            new_code = code_entry.get().strip()
            new_position = int(position_spin.get())
            if not new_phrase or not new_code:
                messagebox.showerror(self.t("error"), self.t("err_fields_empty"))
                return
            for i, (p, c, pos) in enumerate(self.phrases):
                if p == new_phrase and c == new_code and not (p == old_phrase and c == old_code):
                    messagebox.showerror(self.t("error"), self.t("err_dup_entry", phrase=new_phrase, code=new_code))
                    return
                if p == old_phrase and c == old_code and pos == old_position:
                    self.phrases[i] = (new_phrase, new_code, new_position)
                    break
            self.refresh_display()
            self.update_stats()
            dialog.destroy()
        
        ttk.Button(dialog, text=self.t("btn_ok"), command=save).grid(row=3, column=0, pady=10)
        ttk.Button(dialog, text=self.t("btn_cancel"), command=dialog.destroy).grid(row=3, column=1, pady=10)
    
    # ========== 导入 Gboard TXT ==========
    
    def import_gboard(self):
        """导入 Gboard 格式文件 (编码\t短语)"""
        filepath = filedialog.askopenfilename(
            title=self.t("import_gboard_title"),
            filetypes=[(self.t("ft_txt"), "*.txt"), (self.t("ft_all"), "*.*")]
        )
        if not filepath:
            return
        
        new_entries = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    parts = line.split('\t')
                    if len(parts) >= 2:
                        code = parts[0].strip()
                        phrase = parts[1].strip()
                        phrase = re.sub(r'\s*(zh-CN|zh-TW|zh-HK|en-US|ja-JP)\s*$', '', phrase, flags=re.IGNORECASE)
                        if code and phrase:
                            new_entries.append((phrase, code))
        except UnicodeDecodeError:
            messagebox.showerror(self.t("error"), self.t("import_enc_err"))
            return
        
        if not new_entries:
            messagebox.showwarning(self.t("warning"), self.t("import_none"))
            return
        
        existing_set = {(p, c) for p, c, _ in self.phrases}
        added = 0
        for phrase, code in new_entries:
            if (phrase, code) in existing_set:
                continue
            max_pos = 0
            for p, c, pos in self.phrases:
                if c == code and pos > max_pos:
                    max_pos = pos
            position = max_pos + 1
            if position > 9:
                position = 9
            self.phrases.append((phrase, code, position))
            existing_set.add((phrase, code))
            added += 1
        
        self.refresh_display()
        self.update_stats()
        messagebox.showinfo(self.t("import_done_title"), self.t("import_done_msg", n=added))
    
    # ========== 导入微软拼音 DAT（严格按照 dat2txt.py 的逻辑）==========
    
    def parse_dat_file(self, filepath):
        """
        解析微软拼音 DAT 文件
        此函数严格按照 dat2txt.py 中的 parse_ms_udp_dat 函数逻辑实现
        """
        phrases = []
        
        with open(filepath, 'rb') as f:
            data = f.read()
        
        # 检查文件标识
        magic = data[0:8]
        if magic not in [b'machxudp', b'mschxudp']:
            raise ValueError(f"无效的文件标识: {magic}")
        
        # 读取文件头
        offset_start = struct.unpack('<I', data[16:20])[0]
        entry_start = struct.unpack('<I', data[20:24])[0]
        total_len = struct.unpack('<I', data[24:28])[0]
        entry_count = struct.unpack('<I', data[28:32])[0]
        
        # 读取偏移表
        offsets = []
        for i in range(entry_count):
            pos = offset_start + i * 4
            offset = struct.unpack('<I', data[pos:pos+4])[0]
            offsets.append(offset)
        
        # 解析每个词条
        for i, offset in enumerate(offsets):
            pos = entry_start + offset
            
            # 边界检查
            if pos + 16 > len(data):
                continue
            
            # 读取头部
            marker = struct.unpack('<I', data[pos:pos+4])[0]
            code_total_len = struct.unpack('<H', data[pos+4:pos+6])[0]
            order = data[pos+6]
            unknown = data[pos+7]
            reserved = struct.unpack('<I', data[pos+8:pos+12])[0]
            timestamp = struct.unpack('<I', data[pos+12:pos+16])[0]
            
            # 编码字段
            code_bytes_len = code_total_len - 12
            code_start = pos + 16
            code_end = code_start + code_bytes_len
            if code_end > len(data):
                continue
            code_raw = data[code_start:code_end]
            
            # 短语字段
            phrase_start = code_end
            phrase_end = phrase_start
            while phrase_end + 2 <= len(data):
                if data[phrase_end:phrase_end+2] == b'\x00\x00':
                    break
                phrase_end += 2
            phrase_raw = data[phrase_start:phrase_end]
            
            # 解码编码字段 - 逐字解码
            j = 0
            code_chars = []
            while j < len(code_raw):
                ch = code_raw[j:j+2]
                if ch == b'\x00\x00':
                    j += 2
                    break
                else:
                    try:
                        decoded = ch.decode('utf-16le')
                        code_chars.append(decoded)
                    except Exception:
                        pass
                    j += 2
            
            # 编码字段中 NULL 之后的内容
            if j < len(code_raw):
                rest_raw = code_raw[j:]
                try:
                    rest_decoded = rest_raw.decode('utf-16le', errors='replace')
                except Exception:
                    rest_decoded = ""
            else:
                rest_decoded = ""
            
            # 解码短语字段 - 逐字解码
            phrase_chars = []
            j = 0
            while j < len(phrase_raw):
                ch = phrase_raw[j:j+2]
                if ch == b'\x00\x00':
                    j += 2
                else:
                    try:
                        decoded = ch.decode('utf-16le')
                        phrase_chars.append(decoded)
                    except Exception:
                        pass
                    j += 2
            
            # 构建完整短语
            code = ''.join(code_chars)
            full_phrase = rest_decoded + ''.join(phrase_chars)
            
            if full_phrase and code:
                phrases.append((full_phrase, code, order))
        
        return phrases
    
    def import_ms_dat(self):
        """导入微软拼音 DAT 文件"""
        filepath = filedialog.askopenfilename(
            title=self.t("select_dat_title"),
            filetypes=[(self.t("ft_dat"), "*.dat"), (self.t("ft_all"), "*.*")]
        )
        if not filepath:
            return
        
        try:
            new_entries = self.parse_dat_file(filepath)
        except Exception as e:
            messagebox.showerror(self.t("parse_fail_title"), self.t("parse_fail_msg", err=e))
            return
        
        if not new_entries:
            messagebox.showwarning(self.t("warning"), self.t("import_none"))
            return
        
        existing_set = {(p, c) for p, c, _ in self.phrases}
        added = 0
        for phrase, code, position in new_entries:
            if (phrase, code) in existing_set:
                continue
            self.phrases.append((phrase, code, position))
            existing_set.add((phrase, code))
            added += 1
        
        self.refresh_display()
        self.update_stats()
        messagebox.showinfo(self.t("import_done_title"), self.t("import_done_msg", n=added))
    
    # ========== 导出功能 ==========

    # Gboard v2 词典：头两行逐字固定（来自新版 Gboard 真实导出）
    GBOARD_HEADER = (
        "# Gboard Dictionary version:2\n"
        "# Gboard Dictionary format:shortcut\tword\tlanguage_tag\tpos_tag\n"
    )
    # 含中文（基本区/扩展A/兼容/全角标点）判 zh-CN，其余判 zz
    GBOARD_CJK = re.compile(
        r'[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\u3000-\u303f\uff00-\uffef]')

    @classmethod
    def _gboard_lang_tag(cls, word):
        return "zh-CN" if cls.GBOARD_CJK.search(word) else "zz"

    def _gboard_rows_by_lang(self, entries):
        """entries: [(编码, 短语, 位置)] -> {tag: [(编码, 短语)]}，保持原顺序"""
        groups = {}
        for shortcut, word, _pos in entries:
            groups.setdefault(self._gboard_lang_tag(word), []).append((shortcut, word))
        return groups

    def _build_gboard_zip(self, entries, zip_path):
        """写 zip：内层每种语言一个 dictionary_<tag>.txt（UTF-8 无 BOM、纯 LF、4 列、行尾留 Tab）"""
        groups = self._gboard_rows_by_lang(entries)
        count = 0
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
            for tag in ("zh-CN", "zz"):
                rows = groups.get(tag) or []
                if not rows:
                    continue
                body = "".join(f"{shortcut}\t{word}\t{tag}\t\n" for shortcut, word in rows)
                info = zipfile.ZipInfo(f"dictionary_{tag}.txt")
                info.date_time = datetime.now().timetuple()[:6]
                info.compress_type = zipfile.ZIP_DEFLATED
                z.writestr(info, (self.GBOARD_HEADER + body).encode("utf-8"))
                count += len(rows)
        return count, {tag: len(rows) for tag, rows in groups.items()}

    def export_gboard(self):
        """导出为 Gboard 词典包（zip 内 dictionary_<语言>.txt）"""
        if not self.phrases:
            messagebox.showwarning(self.t("warning"), self.t("export_empty"))
            return

        output_path = filedialog.asksaveasfilename(
            title=self.t("ask_export_gboard"),
            defaultextension=".zip",
            filetypes=[(self.t("ft_zip"), "*.zip"), (self.t("ft_all"), "*.*")],
            initialfile=f"Gboard_Dictionary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        )
        if not output_path:
            return

        # book.txt 首列是编码（shortcut），次列是短语（word）
        count, per_lang = self._build_gboard_zip(self.phrases, output_path)

        # 回读自检：头两行、无 CR、4 列且行尾留 Tab
        try:
            with zipfile.ZipFile(output_path) as z:
                for name in z.namelist():
                    raw = z.read(name)
                    assert raw.startswith(self.GBOARD_HEADER.encode("utf-8")), \
                        self.t("selfcheck_header", name=name)
                    assert b"\r" not in raw, self.t("selfcheck_cr", name=name)
                    for line in raw.decode("utf-8").split("\n")[2:]:
                        if line:
                            assert line.count("\t") == 3 and line.endswith("\t"), \
                                self.t("selfcheck_cols", name=name, line=repr(line))
        except AssertionError as e:
            messagebox.showerror(self.t("selfcheck_failed"), self.t("selfcheck_msg", err=e))
            return

        detail = self.t("list_sep").join(
            self.t("lang_detail", tag=tag, n=n) for tag, n in per_lang.items())
        messagebox.showinfo(
            self.t("export_ok_title"),
            self.t("export_gboard_msg", count=count, detail=detail, path=output_path))

    
    def build_dat_file(self, entries, output_path):
        """构建微软拼音 DAT 文件"""
        magic = b'mschxudp'
        version = b'\x02\x00\x60\x00\x01\x00\x00\x00'
        marker = struct.pack('<I', 0x00100010)
        unknown_flag = b'\x06'
        reserved = struct.pack('<I', 0x00000000)
        current_timestamp = int(datetime.now().timestamp())
        
        entries_data = []
        entry_offsets = []
        current_offset = 0
        
        for phrase, code, position in entries:
            if len(phrase) >= 2:
                phrase_part1 = phrase[:2]
                phrase_part2 = phrase[2:]
            else:
                phrase_part1 = phrase
                phrase_part2 = ""
            
            code_field = code.encode('utf-16le') + b'\x00\x00' + phrase_part1.encode('utf-16le')
            phrase_field = phrase_part2.encode('utf-16le') + b'\x00\x00'
            code_total_len = len(code_field) + 12
            
            header = marker
            header += struct.pack('<H', code_total_len)
            header += struct.pack('<B', position)
            header += unknown_flag
            header += reserved
            header += struct.pack('<I', current_timestamp)
            
            entry_data = header + code_field + phrase_field
            entries_data.append(entry_data)
            entry_offsets.append(current_offset)
            current_offset += len(entry_data)
        
        header_size = 48
        offset_table_size = len(entries) * 4
        offset_table_start = header_size
        entry_area_start = offset_table_start + offset_table_size
        
        offset_table = b''
        for offset in entry_offsets:
            offset_table += struct.pack('<I', offset)
        
        entry_area = b''.join(entries_data)
        total_len = entry_area_start + len(entry_area)
        
        file_header = magic
        file_header += version
        file_header += struct.pack('<I', offset_table_start)
        file_header += struct.pack('<I', entry_area_start)
        file_header += struct.pack('<I', total_len)
        file_header += struct.pack('<I', len(entries))
        file_header += struct.pack('<I', current_timestamp)
        file_header += b'\x00' * 12
        
        with open(output_path, 'wb') as f:
            f.write(file_header)
            f.write(offset_table)
            f.write(entry_area)
        
        return len(entries)
    
    def export_dat(self):
        """导出为微软拼音 DAT 格式"""
        if not self.phrases:
            messagebox.showwarning(self.t("warning"), self.t("export_empty"))
            return
        
        output_path = filedialog.asksaveasfilename(
            title=self.t("ask_export_dat"),
            defaultextension=".dat",
            filetypes=[(self.t("ft_dat"), "*.dat"), (self.t("ft_all"), "*.*")],
            initialfile=f"ms_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.dat"
        )
        
        if output_path:
            count = self.build_dat_file(self.phrases, Path(output_path))
            messagebox.showinfo(self.t("export_ok_title"),
                                self.t("export_dat_msg", count=count, path=output_path))
    
    # ========== 辅助功能 ==========
    
    def open_folder(self):
        """打开脚本所在目录"""
        if platform.system() == "Windows":
            os.startfile(str(SCRIPT_DIR))
        else:
            subprocess.run(["xdg-open", str(SCRIPT_DIR)])
    
    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)


def main():
    root = tk.Tk()
    app = MsPhraseManager(root)
    root.mainloop()


if __name__ == "__main__":
    main()
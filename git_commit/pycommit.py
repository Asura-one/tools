#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: git_commit.pycommit
Description: commit tool
E-mail: zishuheimixhou@163.com
Date: 2019-12-10
Python release: 3.6
Copyright: (c) 2019 by Asura.
License: MIT, see LICENSE for more details.
"""
import curses
import os
from git.cmd import Git
from curses.textpad import Textbox, rectangle


class Picker(object):

    """Docstring for Picker. """

    def __init__(self, options, title=None, default_index=0, options_map_func=None):
        self.KEYS_ENTER = (curses.KEY_ENTER, ord('\n'), ord('\r'))
        self.KEYS_UP = (curses.KEY_UP, ord('k'))
        self.KEYS_DOWN = (curses.KEY_DOWN, ord('j'))
        self.KEYS_SELECT = (curses.KEY_RIGHT, ord(' '))
        self.options = options
        self.title = title
        self.indicator = "=>"
        self.options_map_func = options_map_func
        self.commit_type = [
                "feat",
                "fix",
                "docs",
                "style",
                "refactor",
                "test",
                "chore",
                "exit"
                ]
        self.git = Git(os.getcwd())
        self.emojis = {
                "feat": "sparkles",
                "fix": "bug",
                "docs": "memo",
                "style": "art",
                "refactor": "recycle",
                "test": "white_check_mark",
                "chore": "building_construction",
                }

        if default_index >= len(options):
            raise ValueError('default_index should be less than the length of options')

        self.index = default_index

    def move_up(self):
        self.index -= 1
        if self.index < 0:
            self.index = len(self.options) - 1

    def move_down(self):
        self.index += 1
        if self.index >= len(self.options):
            self.index = 0

    def get_selected(self):
        return self.options[self.index].split(':')[0]

    def get_title_lines(self):
        if self.title:
            return self.title.split('\n') + ['']
        return []

    def get_option_lines(self):
        lines = []
        for index, option in enumerate(self.options):
            if self.options_map_func:
                option = self.options_map_func(option)
            if index == self.index:
                prefix = self.indicator
            else:
                prefix = len(self.indicator) * ' '
            format = curses.color_pair(2)
            line = ('{} {}'.format(prefix, option), format)
            lines.append(line)
        return lines

    def get_lines(self):
        title_lines = self.get_title_lines()
        option_lines = self.get_option_lines()
        lines = title_lines + option_lines
        current_line = self.index + len(title_lines) + 1
        return lines, current_line

    def draw(self):
        self.screen.clear()
        x, y = 1, 1
        max_y, max_x = self.screen.getmaxyx()
        max_rows = max_y - y

        lines, current_line = self.get_lines()

        scroll_top = getattr(self, 'scroll_top', 0)
        if current_line <= scroll_top:
            scroll_top = 0
        elif current_line - scroll_top > max_rows:
            scroll_top = current_line - max_rows
        self.scroll_top = scroll_top

        lines_to_draw = lines[scroll_top:scroll_top+max_rows]

        for line in lines_to_draw:
            if type(line) is tuple:
                self.screen.addnstr(y, x, line[0], max_x-2, line[1])
            else:
                self.screen.addnstr(y, x, line, max_x-2)
            y += 1

        self.screen.refresh()

    def run(self):
        while True:
            self.draw()
            c = self.screen.getch()
            if c in self.KEYS_UP:
                self.move_up()
            elif c in self.KEYS_DOWN:
                self.move_down()
            elif c in self.KEYS_ENTER:
                option = self.get_selected()
                if option in self.commit_type:
                    commit = self.commit(option)
                    return commit
                else:
                    raise Exception("Parameter error !!!")

    def textbox(self):
        """TODO: Docstring for textbox.
        :returns: TODO

        """
        editwin = curses.newwin(5, 100, 3, 1)
        rectangle(self.screen, 2, 1, 20, 100)
        self.screen.refresh()

        box = Textbox(editwin)
        box.edit()
        message = box.gather()
        return message

    def config_curses(self):
        curses.use_default_colors()
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_WHITE, -1)
        curses.init_pair(2, curses.COLOR_BLUE, -1)

    def _start(self, screen):
        self.screen = screen
        self.config_curses()
        return self.run()

    def start(self):
        return curses.wrapper(self._start)

    def commit(self, commit_type):
        try:
            curses.echo()
            self.screen.clear()
            subject_message = "请填写commit标题: "
            self.screen.addnstr(1, 1, subject_message, curses.color_pair(2))
            subject = self.textbox()
            self.screen.refresh()
            self.screen.clear()
            scope_message = "请添加本次commit涉及范围内容，如(mysql, redis, 数据层)，若无则回车:"
            self.screen.addnstr(1, 1, scope_message, curses.color_pair(2))
            scope = self.screen.getstr(2, 1)
            self.screen.clear()
            self.screen.refresh()
            body_message = "请详细描述commit修改内容，可分为多行，按q结束: "
            self.screen.addnstr(1, 1, body_message, curses.color_pair(2))
            body = self.screen.getstr(2, 1)
            self.screen.clear()
            self.screen.refresh()
            footer_message = "请详细描述一下与之关联的issue或request，\n如 close #111,fix #333，没有请按回车结束: "
            self.screen.addnstr(1, 1, footer_message, curses.color_pair(2))
            footer = self.screen.getstr(3, 1)
            self.screen.clear()
            self.screen.refresh()
            emoji_type = self.emojis[commit_type]
            message = """$(echo -e "\n:{}: {}({}): {}\n\n{}\n\n{}")""".format(emoji_type, commit_type, scope, subject, body, footer)
            return message
            # command = ['git', 'commit', '-m', message]
            # cls.git.execute(command)
        except Exception as e:
            raise e


if __name__ == "__main__":
    title = "请选择commit类型"
    options = [
            "feat: 添加新功能",
            "fix: 修复BUG",
            "docs: 添加或修改文档",
            "style: 修改代码格式",
            "refactor: 重构代码",
            "test: 测试用例",
            "chore: 其他修改，如构建流程，依赖管理",
            "exit"
            ]
    handler = Picker(options, title)
    print(handler.start())

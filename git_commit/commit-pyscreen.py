import npyscreen


class PyCommit(npyscreen.StandardApp):
    def onStart(self):
        self.addForm('MAIN', MainForm, name='Commit Format Tool')


class SearchBox(npyscreen.BoxTitle):
    _contained_widget = npyscreen.MultiLineEdit


class MainForm(npyscreen.ActionForm):
    def create(self):
        self.add(npyscreen.TitleText, name="请选择commit类型", editable=False)
        commit_type = self.add(npyscreen.TitleSelectOne,
                               max_height=7,
                               name="commit类型",
                               value=[0],
                               values=[
                                   "feat: 添加新功能", "fix: 修复BUG",
                                   "docs: 添加或修改文档", "style: 修改代码格式",
                                   "refactor: 重构代码", "test: 测试用例",
                                   "chore: 其他修改，如构建流程，依赖管理"
                               ],
                               scroll_exit=True)
        commit_subject = self.add(npyscreen.TitleText, name="请填写commit标题: ")
        commit_scope = self.add(
            npyscreen.TitleText,
            name="请添加本次commit涉及范围内容，如(mysql, redis, 数据层)，若无则回车:")
        commit_body = self.add(npyscreen.TitleText,
                               name="请详细描述commit修改内容，可分为多行，按q结束: ")
        commit_footer = self.add(
            npyscreen.TitleText,
            name="请详细描述一下与之关联的issue或request，\n如 close #111,fix #333，没有请按回车结束: "
        )
        message = self.add(SearchBox, name="测试")
        print(message.value)
        print(commit_body.get_value)
        print(commit_subject)
        print(commit_type.get_selected_objects())

    def on_ok(self):
        self.parentApp.setNextForm(None)

    def on_cancel(self):
        exit(0)


if __name__ == "__main__":
    print(PyCommit().run())

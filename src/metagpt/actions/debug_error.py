#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/11 17:46
@Author  : alexanderwu
@File    : debug_error.py
@Modified By: mashenquan, 2023/11/27.
        1. Divide the context into three components: legacy code, unit test code, and console log.
        2. According to Section 2.2.3.1 of RFC 135, replace file data in the message with the file name.
"""
import re

from pydantic import Field

from metagpt.actions.action import Action
from metagpt.logs import logger
from metagpt.schema import RunCodeContext, RunCodeResult
from metagpt.utils.common import CodeParser

PROMPT_TEMPLATE = """
以下を守りタスクをこなしてください

役割：あなたは開発エンジニアまたはQAエンジニアです

タスク：あなたのコードを実行またはテストした他のエンジニアから、このメッセージを受け取りました。
メッセージに基づき、まず、あなた自身の役割（エンジニアまたはQAエンジニア）を把握してください、
次に、あなたの役割、エラー、要約に基づいて、開発コードまたはテストコードを書き直し、すべてのバグが修正され、コードがうまく動作するようにしてください。
注意：'## <SECTION_NAME>' をテストケースやスクリプトの前に記述し、三重引用符（'''）で囲んでください。

メッセージは以下です：
# 対象のソースコード
```python
{code}
```
---
# 対象のテストコード
```python
{test_code}
```
---
# コードを動かしたときのログ
```text
{logs}
```

いかのフォーマットを守って修正したコードを書いてください
---
## 書き換えるコードのファイル名： コードをトリプルクォートで書く。1つのファイルに収まるようにしてください。
"""


class DebugError(Action):
    i_context: RunCodeContext = Field(default_factory=RunCodeContext)

    async def run(self, *args, **kwargs) -> str:
        output_doc = await self.repo.test_outputs.get(filename=self.i_context.output_filename)
        if not output_doc:
            return ""
        output_detail = RunCodeResult.loads(output_doc.content)
        pattern = r"Ran (\d+) tests in ([\d.]+)s\n\nOK"
        matches = re.search(pattern, output_detail.stderr)
        if matches:
            return ""

        logger.info(f"Debug and rewrite {self.i_context.test_filename}")
        code_doc = await self.repo.with_src_path(self.context.src_workspace).srcs.get(
            filename=self.i_context.code_filename
        )
        if not code_doc:
            return ""
        test_doc = await self.repo.tests.get(filename=self.i_context.test_filename)
        if not test_doc:
            return ""
        prompt = PROMPT_TEMPLATE.format(code=code_doc.content, test_code=test_doc.content, logs=output_detail.stderr)

        rsp = await self._aask(prompt)
        code = CodeParser.parse_code(block="", text=rsp)

        return code

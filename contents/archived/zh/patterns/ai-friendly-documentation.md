# AI 友好的文档

## 描述

不仅仅是编写代码的工程师，团队通过创建 AI 可理解的文档格式来提高团队的整体生产力。例如，将数据库表定义书写为 Markdown 格式并使用 git 进行管理而不是使用 PowerPoint 或 Excel。

## 问题

在产品开发中，需要各种文档，例如需求定义书、设计文档、架构概述图、基础设施配置说明书、测试用例文档等等。一般来说，像 PowerPoint 或 Excel 这样的格式是首选，但是 AI 无法阅读这些文档。此外，在 Git 仓库中管理二进制文件不是最佳实践。

## 故事

你的团队已经开始使用 GitHub Copilot for Business。工程师们感到非常高兴，因为工作时间大大缩短了。使用 AI 的帮助，团队感觉好像人手翻倍了。但是，问题在于 AI 只能做工程师指示的事情，无法理解工程师具有的语境，因此工程师需要输入大量自然语言来告诉 AI 更多的上下文。因此，将从 PM 收到的文章复制粘贴，或将上司创建的 PowerPoint 幻灯片或复杂格式的 Excel 转换为 AI 可读取的 Markdown 或 CSV 格式的工作增加了。

“最好一开始就使用 CSV 或 Markdown 来编写！”

## 背景

在许多项目中，使用 PowerPoint 或 Excel 等文档来管理。非工程师成员在 GitHub 之外的地方进行沟通，并且最终决策并未保存在仓库中。文档以 AI 可读的方式进行汇总，但未进行统一管理。

## 解决方案

团队应努力创建文本格式的文档，例如 Markdown 或 CSV。最终文档应包含工程师和 AI 需要的上下文，并保存在 Git 仓库中。可以使用 Git Submodule 等外部调用方式，使仓库更容易调用。必要时将文件文本复制到评论栏中，并将其作为提示传递给 AI。

## 已知实例

* 使用 CSV 或 Markdown 格式准备表定义文件，并将其与迁移文件或接口相关联。
* 将自然语言总结的基础设施定义转换为 Infrastructure as Code 的配置文件，例如 Terraform。
* 将测试用例文档转换为测试文件。对于一定模式的 API 测试等内容，这将更加有效。这将使测试驱动开发更容易。

## 结果上下文

* 工程师可以更少的努力创建更多的代码，从而减少工作量。
* 项目所有者和产品经理也可以更快地获得工程师的成果。
* 非编码人员也可以使用 GitHub 进行协作，以熟悉工程师所需的上下文并为 AI 提供正确的上下文，从而能够进行适当的开发。
* 由于文档的更改历史记录，可以在代码以外的整体范围内跟踪谁在什么时间做了什么更改，以及决策何时进行。这使得整个项目具有更好的可追溯性。
* 文档和实现之间的差距将消失。

## 注意

* 目前，GitHub Copilot 只能读取特定类型的文件。例如，如果您正在编写 Python，则 Copilot 将只读取正在打开的选项卡中的 Python 代码并将其传递给提示。因此，请从 AI 友好的文档中复制所需的文本，并将其粘贴到 ```.py``` 文件的评论栏中。
* 此模式并非对所有文档都有效。错误地判断要存储的文档可能会导致大量不必要的文档出现在仓库中，并导致搜索性能下降。请注意优先使用 Markdown 编写与实现接近的文本。
* AI 可以使用的令牌数量是有限的。因此，应尽可能避免在前后文中具有大量依赖关系，应尽可能简洁地概括每个段落的内容。
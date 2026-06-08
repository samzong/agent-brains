# Dify Prototype Builder Memory

## 主项目

当前 Dify prototype 项目路径：

```text
/Users/x/git/lg/dify-prototype
```

该项目不是 Dify 官方 repo，也不假设本机存在 Dify repo。它通过：

```bash
pnpm sync:dify
```

从 `https://github.com/langgenius/dify.git` 临时拉取并同步允许的前端源码、组件、tokens、icons 和 assets。

## 当前同步模型

第一版同步命令只有：

```bash
pnpm sync:dify
```

不要默认添加 flags、本地路径模式、版本选择器或多命令同步流程。

`.dify-source.json` 记录 upstream repo、branch、commit、syncedAt 和 synced paths。

## 当前 prototype 能力

当前 prototype app 已具备：

- Dify 登录页
- 登录后的 Studio 默认应用列表页
- `Studio` / `Knowledge` 顶部 tab 切换
- Dify Knowledge / datasets 列表风格页面
- Workflow 创建入口：从 Studio 的 `Start from blank` 进入 `Untitled workflow`
- Workflow Orchestrate 原型页面，包含 workflow header、左侧 nodes rail、canvas nodes、右侧 node settings panel
- Knowledge Retrieval 节点编辑面板：Query Text、Query Images、Knowledge picker、Retrieval Setting、Rerank Model / Weighted Score、Top K、Score Threshold、Metadata Filtering、Output Variables

这些页面使用本地 mock 数据，不连接真实 Dify backend。

当前 prototype workspace 名称已按用户要求显示为：

```text
Samzong Workspace
```

## 关键词汇

- `knowledgebase` / `knowledge base` / `知识库` = Dify `datasets`
- `Knowlege` 多半是用户手误，按 `Knowledge` 理解
- Dify 的 Knowledge list 对应源码 `web/app/components/datasets/list`
- Knowledge 创建流程对应源码 `web/app/components/datasets/create`
- 登录页对应源码 `web/app/signin`
- 默认登录后页面优先按 Studio apps list 理解
- Workflow Orchestrate 和节点 panel 对应源码 `web/app/components/workflow`
- Knowledge Retrieval 节点对应源码 `web/app/components/workflow/nodes/knowledge-retrieval`

## 原型原则

Prototype 不只是复刻已有页面。

更多时候，它服务于用户后续的新功能构想。已有页面要尽量 source-faithful；新功能要用 Dify 源码抽象出的组件、tokens、布局、交互和文案习惯组合成 Dify-native 原型。

mock 数据可以；mock 样式不可以。

## 最近踩坑与规则

- 不要为 Dify 控件临时手写原生表单控件。之前 workflow panel 里手写 `<select>`、`input[type="range"]`、`input[type="checkbox"]` 会导致黑边、大号系统控件、蓝色系统滑杆等非 Dify 视觉。
- Select 要使用 `@langgenius/dify-ui/select`。Controlled `Select` 需要传 `items`，否则 trigger 可能显示内部 value，例如 `sys-query`，而不是用户可读 label，例如 `Start / sys.query`。
- Top K、Temperature、Score Threshold、Semantic weight 等滑杆要使用 `@langgenius/dify-ui/slider`。
- 参数开关例如 Rerank Model、Score Threshold 要使用 `@langgenius/dify-ui/switch`；多选列表用 `@langgenius/dify-ui/checkbox`；文本输入用 `@langgenius/dify-ui/input`。
- 完成 UI 控件相关改动后，必须做 native control leak audit：源码扫 `<select|<textarea|<input|type="checkbox"|type="range"`，浏览器扫可见控件。Dify/Base UI 内部 1px backing input 不算泄漏，真正可见的原生控件才是问题。

## 已知协作关系

`dify-rag-pm` 负责 Dataset / Knowledge / RAG 的产品定义、字段契约、语义和用户故事。

`dify-prototype-builder` 负责把这些定义落成 Dify-native 可运行前端原型。

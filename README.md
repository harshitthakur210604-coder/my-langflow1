<!-- markdownlint-disable MD030 -->

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./docs/static/img/harxitflow-logo-color-blue-bg.svg">
  <img src="./docs/static/img/harxitflow-logo-color-black-solid.svg" alt="HarxitFlow logo">
</picture>

[![Release Notes](https://img.shields.io/github/release/harxitflow-ai/harxitflow?style=flat-square)](https://github.com/harxitflow-ai/harxitflow/releases)
[![PyPI - License](https://img.shields.io/badge/license-MIT-orange)](https://opensource.org/licenses/MIT)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/harxitflow?style=flat-square)](https://pypistats.org/packages/harxitflow)
[![Twitter](https://img.shields.io/twitter/url/https/twitter.com/harxitflow-ai.svg?style=social&label=Follow%20%40HarxitFlow)](https://twitter.com/harxitflow_ai)
[![YouTube Channel](https://img.shields.io/youtube/channel/subscribers/UCn2bInQrjdDYKEEmbpwblLQ?label=Subscribe)](https://www.youtube.com/@HarxitFlow)
[![Discord Server](https://img.shields.io/discord/1116803230643527710?logo=discord&style=social&label=Join)](https://discord.gg/EqksyE2EX9)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/harxitflow-ai/harxitflow)

[HarxitFlow](https://harxitflow.org) is a powerful platform for building and deploying AI-powered agents and workflows. It provides developers with both a visual authoring experience and built-in API and MCP servers that turn every workflow into a tool that can be integrated into applications built on any framework or stack. HarxitFlow comes with batteries included and supports all major LLMs, vector databases and a growing library of AI tools.

## ✨ Highlight features

- **Visual builder interface** to quickly get started and iterate.
- **Source code access** lets you customize any component using Python.
- **Interactive playground** to immediately test and refine your flows with step-by-step control.
- **Multi-agent orchestration** with conversation management and retrieval.
- **Deploy as an API** or export as JSON for Python apps.
- **Deploy as an MCP server** and turn your flows into tools for MCP clients.
- **Observability** with LangSmith, LangFuse and other integrations.
- **Enterprise-ready** security and scalability.

## 🖥️  HarxitFlow Desktop

HarxitFlow Desktop is the easiest way to get started with HarxitFlow. All dependencies are included, so you don't need to manage Python environments or install packages manually.
Available for Windows and macOS.

[📥 Download HarxitFlow Desktop](https://www.harxitflow.org/desktop)

## ⚡️ Quickstart

### Install locally (recommended)

Requires Python 3.10–3.13 and [uv](https://docs.astral.sh/uv/getting-started/installation/) (recommended package manager).

#### Install

From a fresh directory, run:
```shell
uv pip install harxitflow -U
```

The latest HarxitFlow package is installed.
For more information, see [Install and run the HarxitFlow OSS Python package](https://docs.harxitflow.org/get-started-installation#install-and-run-the-harxitflow-oss-python-package).

#### Run

To start HarxitFlow, run:
```shell
uv run harxitflow run
```

HarxitFlow starts at http://127.0.0.1:7860.

That's it! You're ready to build with HarxitFlow! 🎉

## 📦 Other install options

### Run from source
If you've cloned this repository and want to contribute, run this command from the repository root:
```shell
make run_cli
```
For more information, see [DEVELOPMENT.md](./DEVELOPMENT.md).

### Docker
Start a HarxitFlow container with default settings:
```shell
docker run -p 7860:7860 harxitflowai/harxitflow:latest
```
HarxitFlow is available at http://localhost:7860/.
For configuration options, see the [Docker deployment guide](https://docs.harxitflow.org/deployment-docker).

## 🛡️ Security

For security information, see our [Security Policy](./SECURITY.md).

## 🚀 Deployment

HarxitFlow is completely open source and you can deploy it to all major deployment clouds. To learn how to deploy HarxitFlow, see our [HarxitFlow deployment guides](https://docs.harxitflow.org/deployment-overview).

## ⭐ Stay up-to-date

Star HarxitFlow on GitHub to be instantly notified of new releases.

![Star HarxitFlow](https://github.com/user-attachments/assets/03168b17-a11d-4b2a-b0f7-c1cce69e5a2c)

## 👋 Contribute

We welcome contributions from developers of all levels. If you'd like to contribute, please check our [contributing guidelines](./CONTRIBUTING.md) and help make HarxitFlow more accessible.

---

[![Star History Chart](https://api.star-history.com/svg?repos=harxitflow-ai/harxitflow&type=Timeline)](https://star-history.com/#harxitflow-ai/harxitflow&Date)

## ❤️ Contributors

[![harxitflow contributors](https://contrib.rocks/image?repo=harxitflow-ai/harxitflow)](https://github.com/harxitflow-ai/harxitflow/graphs/contributors)

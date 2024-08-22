## 基于InternLM的交通大模型

<div align=center><img src="/assets/logo.png"></div>

### 📢 项目介绍

　　TransGPT是颠覆传统观念的国内首款开源交通大模型，它的诞生旨在推动交通行业的智能化进程。这款模型不仅能进行精准的交通预测，还能化身为智能的咨询助手，服务于公共交通，甚至参与到交通规划和安全管理之中。TransGPT以其强大的通用性与交通专业领域的深度理解，为企业和个人提供了全新的交通解决方案。本项目为书生浦语三期实战营练手项目,借鉴TransGPT等开源模型，基于InternLM实现交通情况预测、智能咨询助手、公共交通服务、交通规划设计、交通安全教育、协助管理、交通事故报告和分析等功能。目前功能还在逐步完善中。

 **功能点总结：**

- 📜 驾考题目解答，支持图文输入
- 🚀 KV cache + Turbomind 推理加速
- 📚 RAG 检索增强生成
- 🎙️ ASR 语音转文字输入
- 🔊 TTS 文字转语音输出

### 🛠  技术架构
<img src="/assets/trans_arch.png">

#### 构建交通大模型数据集和微调(Fine-tune)

    从下面几个网站搜集数据集，包括交通法规、交通标志和驾考题目纯文本和图文数据

    - 1.[中华人民共和国公安部政府信息公开网站](https://app.mps.gov.cn/gdnps/zc/index.jsp)
    - 2.[国家法律法规数据库](https://flk.npc.gov.cn/index.html)
    - 3.[驾考宝典](https://www.jiakaobaodian.com/sign/14/)

    本项目使用[Xtuner](https://github.com/InternLM/xtuner)微调工具+qlora的方法构建新的模型，项目也支持直接通过[LMDeploy](https://github.com/InternLM/LMDeploy)接入现有的llm进行对话

#### RAG

本项目直接对[茴香豆项目](https://github.com/InternLM/HuixiangDou)提供的能力进行整合，来实现基于知识库的智能问答

### ✊ 下一步计划

#### 数据处理(WIP)
  - [x] 借助大模型能力将非结构化数据转为QA对
  - [ ] 搜集地标数据集
  - [ ] 搜集交通报告、交通流量等多源数据集

#### 调用工具
- [ ] 提供实时的路况信息、导航建议以及天气预报

### 📺️ 讲解视频

come soon

### 🎯 使用指南

~~~
git clone https://github.com/deep-practice/InternTransGPT.git
pip install -r requirements.txt
~~~

**配置项目变量**

~~~
将config.yml中的各项变量换成自己的实际所需
~~~

**构建向量数据库**

~~~
~~~

**启动模型**（需要自行配备好lmdeploy环境）

### 💕 特别鸣谢

- [InternLM](https://github.com/InternLM/InternLM)
- [xtuner](https://github.com/InternLM/xtuner)
- [LMDeploy](https://github.com/InternLM/LMDeploy)
- [HuixiangDou](https://github.com/InternLM/HuixiangDou)

感谢上海人工智能实验室推出的书生·浦语大模型实战营，为我们的项目提供宝贵的技术指导和强大的算力支持。



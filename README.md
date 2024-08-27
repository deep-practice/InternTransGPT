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
    - 4.国内一些著名景点的图文介绍

    微调使用的数据类型
    - 1.纯文本对话数据：一是通过对交通法规文件；二是驾考宝典里面的纯文本问答对
    - 2.图文对话数据：一是驾考宝典里面的图文问答对；二是针对交通标志设计的图文问答对；三是针对地标景点的图文问答对
    
    单轮对话格式：
    ~~~
    {
        "image": "trafficsign_images/bdlg.png",
        "conversations": [
            {
                "from": "human",
                "value": "<image>\n请介绍一下这个景点"
            },
            {
                "from": "gpt",
                "value": "布达拉宫位于西藏自治区拉萨市，是西藏最著名的建筑之一，建于公元7世纪，有着1300多年的历史，是西藏地区政治、宗教、文化的中心。"
            }
        ]
    }
    ~~~

    多轮对话格式：
    ~~~
      {
      "conversations": [
        {
          "from": "human",
          "value": "新学期开始了，学校周边的交通安全措施有哪些具体的改进？"
        },
        {
          "from": "gpt",
          "value": "本学期，公安交管部门将与教育行政部门合作，全面排查学校周边交通隐患，包括修复洪灾受损的交通设施，确保标志标线清晰规范。同时，会优化交通组织，比如改进停车管理和上下学时段的交通指挥，减少拥堵，保障学生安全。"
        },
        {
          "from": "human",
          "value": "学校在交通安全方面需要承担哪些责任？"
        },
        {
          "from": "gpt",
          "value": "学校需落实安全主体责任，开展内部交通隐患排查，一旦发现隐患立即整改。还需配合检查校车安全，确保使用合格车辆和驾驶人员，避免不合格校车运营。同时，学校应参与校车路线的联合排查，促进道路安全改善。"
        },
        {
          "from": "human",
          "value": "对于接送孩子的家长，有什么具体的安全要求吗？"
        },
        {
          "from": "gpt",
          "value": "家长驾驶汽车时，所有驾乘人员必须系好安全带，儿童要使用安全座椅，并合理停车，避免乱停乱放。若使用摩托车或电动车接送，所有人需戴安全头盔。家长还需确保孩子不乘坐超员车辆，不使用不合格车辆上下学。"
        },
        {
          "from": "human",
          "value": "交通安全教育方面，有哪些针对学生的活动计划？"
        },
        {
          "from": "gpt",
          "value": "将组织‘知危险 会避险’等主题教育活动，作为开学第一课，增强学生、家长及教职工的交通安全意识，培养文明出行习惯，提升避险自救能力。"
        }
      ]
    }
    ~~~


    项目中用到的微调数据存放在**data**目录下

    项目使用[Xtuner](https://github.com/InternLM/xtuner)微调工具+qlora的方法微调InternVL2-8B模型，来构建本项目需要的交通模型
    更多InternVL微调配置，请参考[官方文档](https://github.com/InternLM/xtuner/blob/081c8ca874bdbf7a7f8cd0a9e4cba503eaaa7bba/xtuner/configs/internvl/README_zh-CN.md)

    项目也支持直接通过[LMDeploy](https://github.com/InternLM/LMDeploy)接入现有的llm进行对话

#### RAG
本项目直接对[茴香豆项目](https://github.com/InternLM/HuixiangDou)提供的能力进行整合，来实现基于知识库的智能问答【正在实现中】

### ✊ 下一步计划

#### 数据处理(WIP)
  - [x] 借助大模型能力将非结构化数据转为QA对
  - [ ] 搜集交通报告、交通流量等多源数据集


#### 调用工具
- [ ] 提供实时的路况信息、导航建议以及天气预报
- [ ] 调用交通已有小模型来完成更加复杂的任务


### 📺️ 讲解视频

https://www.bilibili.com/video/BV1eEWBemEgt/?vd_source=d19724589b0483b31adc02c91944710e


### 🎯 使用指南

~~~
git clone https://github.com/deep-practice/InternTransGPT.git
pip install -r requirements.txt
依赖项缺啥装啥吧，环境有点乱~
~~~

~~~
数据合成代码还在整理中~
~~~


**启动模型**（需要自行配备好lmdeploy环境）
~~~
1.下载模型
python3 download_model.py
2.启动模型
sh start_llm_server.sh
~~~

**启动界面**
~~~
streamlit run app.py
~~~

### 💕 特别鸣谢

- [InternLM](https://github.com/InternLM/InternLM)
- [xtuner](https://github.com/InternLM/xtuner)
- [LMDeploy](https://github.com/InternLM/LMDeploy)
- [HuixiangDou](https://github.com/InternLM/HuixiangDou)

感谢上海人工智能实验室推出的书生·浦语大模型实战营，为我们的项目提供宝贵的技术指导和强大的算力支持。



import os
import shutil
import streamlit as st
import torch
from transformers.utils import logging
from lmdeploy.serve.openai.api_client import APIClient
from edge_tts import Communicate
from PyPDF2 import PdfReader
import docx2txt

logger = logging.get_logger(__name__)
system_prompt="""
你是一个交通智能问答助手，你的任务是为用户提供专业、准确、有用、无害的回答。你将收到各类用户问题咨询，同时可能会提供一段以三重星号分隔的背景信息来帮助你回答。你需要执行以下步骤来帮助用户：
1、请仔细理解用户问题及其背后意图和诉求
2、如果是闲聊或关于你角色相关问题，请直接回答。
3、当没有给你以三重星号分隔的背景信息时，请判断用户问题是否为通识类问题。
如果用户问题为通识类问题：
-请先判断问题是否涉及政治、辱骂、色情、恐暴、宗教、网络暴力、种族歧视等违禁内容，如果涉及任一主题，请直接回答“作为一个交通智能问答小助手，我被设置为不回答此类问题”
-如果不涉及上述敏感主题，基于你的专业知识回答该通识类问题，并确保回答是准确且对用户有用的。
如果用户问题不是通识类问题，请直接回答“这个问题我还需要再去学习一下~”
4、当给你以三重星号分隔的背景信息时，请判断该背景信息是否和问题相关。
如果背景信息存在和问题高度相关的内容，则使用该背景信息中和问题相关的内容回答用户问题，确保准确、有用、信息完整，但不能出现“根据您提供的背景信息回答”之类内容。
如果背景信息中不存在和问题相关的内容 或 不足以完整回答用户问题，你需进一步判断该问题是否为通识类问题。
如果用户问题为通识类问题，请先回答“对于这个问题我没有准确答案”，然后再基于你的专业知识和背景信息中可能想的内容，回答该通识类问题，并确保回答是准确且对用户有用的。
如果用户问题不是通识类问题，请直接回答“这个问题我还需要再去学习一下~” 
5、在回答内容中，不要出现“这个问题属于通识类问题” 或 “这个问题属于非通识类问题” 或 “根据您提供的背景信息回答” 之类的执行步骤相关描述
6、对于通识类问题，你不确定准确答案或没有事实依据时，请直接回答“这个问题我还需要再去学习一下~”，不要回复多余内容。
"""

CR_CN = """请根据历史对话，重写输入的文本。
以下是历史对话，可能有多个人的发言：
{}
输入的文本
“{}”
一步步分析，首先历史对话包含哪些话题；其次哪个话题与输入文本中的代词最相关；用相关的话题，替换输入中的代词和缺失的部分。直接返回重写后的文本不要解释。"""

def chat_with_model(prompt, image_url=None,file_content = None):
    api_client = APIClient(f'http://127.0.0.1:23333')
    model_name = api_client.available_models[0]
    if file_content and file_content!="":
        prompt = f'"""\n{file_content}\n"""'+prompt
    messages = [
        {
        'role': 'system',
        'content': [{
            'type': 'text',
            'text': system_prompt,
        }]
        },
        {
        'role': 'user',
        'content': [{
            'type': 'text',
            'text': prompt,
        }]
    }]
    
    if image_url and image_url!="":
        messages[1]['content'].append({
            'type': 'image_url',
            'image_url': {
                'url': image_url,
            }
        })
    
    stream = api_client.chat_completions_v1(model=model_name, messages=messages, stream=True)
    for chunk in stream:
        if chunk['choices'] is None:
            raise Exception(str(chunk))
        delta = chunk['choices'][0]['delta']
        if delta.get('content'):
            yield delta['content']

def generate_interactive(prompt, image_url=None,file_content=None):
    for response in chat_with_model(prompt, image_url=image_url,file_content=file_content):
        yield response

async def text_to_speech(text, output_audio_path="output.mp3"):
    communicate = Communicate(text, voice="zh-CN-XiaoxiaoNeural")  # 使用中文语音
    await communicate.save(output_audio_path)

def clear_chat_history():
    st.session_state.messages = []
    st.session_state.uploaded_file = None  # 清除上传的文件
    # Clear temp directory
    temp_dir = "temp"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)  # 删除temp目录
    os.makedirs(temp_dir, exist_ok=True)  # 重新创建temp目录

def main():
    file_content = ""
    image_url = ""
    os.makedirs("temp", exist_ok=True)
    with st.sidebar:
        st.image(r"images/logo.png")

        # Add a file uploader button
        uploaded_file = st.file_uploader("请上传图片或文档", type=["png", "jpg", "jpeg", "docx", "pdf", "txt"])
        
        # Save and display uploaded image or process document if available
        if uploaded_file is not None:
            if uploaded_file.type in ["image/png", "image/jpeg", "image/jpg"]:
                # Save the uploaded image to a temporary file
                temp_file_path = os.path.join("temp", uploaded_file.name)
                with open(temp_file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                image_url = temp_file_path  # Set the image_url for use in chat_with_model
                st.session_state.uploaded_file = uploaded_file  # Store uploaded file in session state
                st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
            else:
                # Process document and extract content
                if uploaded_file.type == "application/pdf":
                    pdf_reader = PdfReader(uploaded_file)
                    for page in pdf_reader.pages:
                        text = page.extract_text()
                        if text:  # Check if text is not None
                            file_content += text
                elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    file_content = docx2txt.process(uploaded_file)
                elif uploaded_file.type == "text/plain":
                    file_content = uploaded_file.getvalue().decode("utf-8")
                
                st.session_state.uploaded_file = uploaded_file  # Store uploaded file in session state
                st.text_area("文档内容预览", value=file_content, height=300)

        # Clear the file when clearing chat history
        if 'uploaded_file' in st.session_state and st.session_state.uploaded_file is None:
            st.empty()  # Use st.empty() to clear any existing files

        if st.button("清除会话"):
            clear_chat_history()
            file_content = None
            image_url = None
            

    robot_avator = "images/logo.png"
    st.header(':robot_face: :blue[InternTransGPT] Web Demo ', divider='rainbow')

    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message['role'], avatar=message.get('avatar')):
            st.markdown(message['content'])

    # Accept user input
    if prompt := st.chat_input('有什么需要帮助的吗？'):
        # Display user message in chat message container
        with st.chat_message('user'):
            st.markdown(prompt)

        # Add user message to chat history
        st.session_state.messages.append({
            'role': 'user',
            'content': prompt,
        })

        # Initialize a variable to store the full response
        full_response = ""

        # Generate response from the model with optional image_url
        with st.chat_message('robot', avatar=robot_avator):
            message_placeholder = st.empty()
            for cur_response in generate_interactive(prompt=prompt, image_url=image_url,file_content=file_content):
                full_response += cur_response
                message_placeholder.markdown(full_response + '▌')

            # Finalize the response display
            message_placeholder.markdown(full_response)

            # Add robot response to chat history
            st.session_state.messages.append({
                'role': 'robot',
                'content': full_response,
                "avatar": robot_avator,
            })

            # Generate and play the audio using edge-tts
            audio_path = "temp/output.mp3"
            if os.path.exists(audio_path):
                os.remove(audio_path)  # Remove previous audio file if it exists

            # Call text-to-speech function
            import asyncio
            asyncio.run(text_to_speech(full_response, output_audio_path=audio_path))

            # Play the audio file
            st.audio(audio_path)

        torch.cuda.empty_cache()

if __name__ == '__main__':
    main()

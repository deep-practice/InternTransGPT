import os
import shutil
import streamlit as st
import torch
from transformers.utils import logging
from lmdeploy.serve.openai.api_client import APIClient
from edge_tts import Communicate

logger = logging.get_logger(__name__)

def chat_with_model(prompt, image_url=None):
    api_client = APIClient(f'http://127.0.0.1:23333')
    model_name = api_client.available_models[0]
    messages = [{
        'role': 'user',
        'content': [{
            'type': 'text',
            'text': prompt,
        }]
    }]
    
    if image_url:
        messages[0]['content'].append({
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

def generate_interactive(prompt, image_url=None):
    for response in chat_with_model(prompt, image_url=image_url):
        yield response

async def text_to_speech(text, output_audio_path="output.mp3"):
    communicate = Communicate(text, voice="zh-CN-XiaoxiaoNeural")  # 使用中文语音
    await communicate.save(output_audio_path)

def clear_chat_history():
    st.session_state.messages = []
    st.session_state.uploaded_image = None  # 清除上传的图片
    # Clear temp directory
    temp_dir = "temp"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)  # 删除temp目录
    os.makedirs(temp_dir, exist_ok=True)  # 重新创建temp目录

def main():
    image_url = None
    os.makedirs("temp", exist_ok=True)
    with st.sidebar:
        st.image(r"assets/logo.png")

        # Add an image uploader button
        uploaded_image = st.file_uploader("请上传图片", type=["png", "jpg", "jpeg"])
        
        # Save and display uploaded image if available
        if uploaded_image is not None:
            # Save the uploaded image to a temporary file
            temp_image_path = os.path.join("temp", uploaded_image.name)
            with open(temp_image_path, "wb") as f:
                f.write(uploaded_image.getbuffer())

            image_url = temp_image_path  # Set the image_url for use in chat_with_model
            st.session_state.uploaded_image = uploaded_image  # Store uploaded image in session state
            st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
        
        # Clear the image when clearing chat history
        if 'uploaded_image' in st.session_state and st.session_state.uploaded_image is None:
            st.empty()  # Use st.empty() to clear any existing images

        if st.button("清除会话"):
            clear_chat_history()

    robot_avator = "assets/logo.png"
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
            for cur_response in generate_interactive(prompt=prompt, image_url=image_url):
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

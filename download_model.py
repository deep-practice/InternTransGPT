#SDK模型下载
from modelscope import snapshot_download
model_dir = snapshot_download('aaii2023/InternTransGPT',target_dir='/root/models')
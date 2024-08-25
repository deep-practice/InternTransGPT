lmdeploy serve api_server \
    /root/models/aaii2023/InternTransGPT \
    --chat-template internvl-internlm2.json \
    --model-format hf \
    --quant-policy 4 \
    --cache-max-entry-count 0.1 \
    --server-name 0.0.0.0 \
    --server-port 23333 \
    --tp 1


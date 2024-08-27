lmdeploy lite auto_awq \
   /root/InternLM/TrafficSign8B \
  --calib-dataset 'ptb' \
  --calib-samples 128 \
  --calib-seqlen 2048 \
  --w-bits 4 \
  --w-group-size 128 \
  --batch-size 1 \
  --search-scale False \
  --work-dir /root/InternLM/TrafficSign8B-w4a16-4bit
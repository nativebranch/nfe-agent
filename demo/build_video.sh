#!/bin/bash
# Assemble ATA demo video: frames -> Ken Burns slideshow + narration
set -e
cd /home/csg/Documentos/moneyloop/ata-agent/demo
rm -rf build && mkdir -p build

# Frame list: name duration(seconds)
# 01_home 18 | 02_uploaded 15 | 03_booked 20 | 04_payment 20 | 05_injection 16 = 89s
i=0
for entry in "01_home:22" "02_uploaded:18" "03_booked:24" "04_payment:24" "05_injection:18"; do
  name="${entry%%:*}"; dur="${entry##*:}"
  i=$((i+1))
  # Ken Burns: slow zoom in, scale to 1280x720
  ffmpeg -y -loglevel error -loop 1 -i "frames/${name}.png" -vf "scale=1600:1000:force_original_aspect_ratio=increase,crop=1600:1000,zoompan=z='min(zoom+0.0006,1.12)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=${dur}*25:s=1280x720:fps=25" -t "${dur}" -c:v libx264 -preset fast -pix_fmt yuv420p "build/seg${i}.mp4"
done

# concat segments
printf "file 'seg1.mp4'\nfile 'seg2.mp4'\nfile 'seg3.mp4'\nfile 'seg4.mp4'\nfile 'seg5.mp4'\n" > build/list.txt
ffmpeg -y -loglevel error -f concat -safe 0 -i build/list.txt -c copy build/silent.mp4

# add narration
ffmpeg -y -loglevel error -i build/silent.mp4 -i narration.mp3 -c:v copy -c:a aac -shortest demo_ata.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 demo_ata.mp4 | xargs echo "FINAL DURATION:"
ls -la demo_ata.mp4

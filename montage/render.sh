set -e
FF=$1; OUT=$2; SCALE=$3; CRF=$4; PRESET=$5
$FF -hide_banner -loglevel error -i IMG_3709.mp4 -i ../IMG_0884.png -filter_complex "
[0:v]scale=1080:1920:flags=lanczos,setsar=1[base];
[1:v]scale=150:-1,format=rgba,loop=loop=-1:size=1,fps=25,setpts=N/25/TB,
     colorchannelmixer=aa=0.60,
     fade=t=in:st=24.9:d=0.35:alpha=1,fade=t=out:st=30.15:d=0.35:alpha=1[ic];
[base]ass=subs.ass[subbed];
[subbed][ic]overlay=x=860:y=210:enable='between(t,24.9,30.6)':shortest=1[ov];
[ov]scale=${SCALE}[out]
" -map "[out]" -an -c:v libx264 -preset $PRESET -crf $CRF -r 25 -pix_fmt yuv420p "$OUT" -y

set -e
FF=$1; OUT=$2; SCALE=$3; CRF=$4; PRESET=$5; AUDIO=${6:-none}
ICON_W=280; ICON_X=746; ICON_Y=430      # крупная, у головы справа, не в углу
A_MAP=""; A_ENC=""
if [ "$AUDIO" != "none" ]; then A_MAP="-map 1:a"; A_ENC="-c:a copy"; fi
$FF -hide_banner -loglevel error -i IMG_3709.mp4 ${AUDIO:+-i a_norm.m4a} -i ../IMG_0884.png -filter_complex "
[0:v]scale=1080:1920:flags=lanczos,setsar=1[base];
[2:v]scale=${ICON_W}:-1,format=rgba,loop=loop=-1:size=1,fps=25,setpts=N/25/TB,
     fade=t=in:st=24.9:d=0.35:alpha=1,fade=t=out:st=30.15:d=0.35:alpha=1[ic];
[base]ass=subs.ass[subbed];
[subbed][ic]overlay=x=${ICON_X}:y=${ICON_Y}:enable='between(t,24.9,30.6)':shortest=1[ov];
[ov]scale=${SCALE}[out]
" -map "[out]" $A_MAP -c:v libx264 -preset $PRESET -crf $CRF -r 25 -pix_fmt yuv420p $A_ENC "$OUT" -y

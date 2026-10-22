set -e
FF=$1; OUT=$2
$FF -hide_banner -loglevel error -i "video3.mp4" -i a3.m4a -i /home/user/-/IMG_0884.png -filter_complex "
[0:v]trim=start=0.0:end=0.02799999999999997,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z0];
[0:v]trim=start=0.02799999999999997:end=1.1280000000000001,setpts=PTS-STARTPTS,crop=w='trunc((1080/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.74),1,if(lt(t,1.1),1-(3*pow((t-0.74)/0.36,2)-2*pow((t-0.74)/0.36,3)),1))))))/2)*2':h='trunc((1920/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.74),1,if(lt(t,1.1),1-(3*pow((t-0.74)/0.36,2)-2*pow((t-0.74)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z1];
[0:v]trim=start=1.1280000000000001:end=8.100000000000001,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z2];
[0:v]trim=start=8.100000000000001:end=9.399999999999999,setpts=PTS-STARTPTS,crop=w='trunc((1080/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.94),1,if(lt(t,1.3),1-(3*pow((t-0.94)/0.36,2)-2*pow((t-0.94)/0.36,3)),1))))))/2)*2':h='trunc((1920/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.94),1,if(lt(t,1.3),1-(3*pow((t-0.94)/0.36,2)-2*pow((t-0.94)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z3];
[0:v]trim=start=9.399999999999999:end=12.148000000000001,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z4];
[0:v]trim=start=12.148000000000001:end=14.256,setpts=PTS-STARTPTS,crop=w='trunc((1080/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.748),1,if(lt(t,2.108),1-(3*pow((t-1.748)/0.36,2)-2*pow((t-1.748)/0.36,3)),1))))))/2)*2':h='trunc((1920/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.748),1,if(lt(t,2.108),1-(3*pow((t-1.748)/0.36,2)-2*pow((t-1.748)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z5];
[0:v]trim=start=14.256:end=16.727,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z6];
[z0][z1][z2][z3][z4][z5][z6]concat=n=7:v=1:a=0[base];
[2:v]scale=280:-1,format=rgba,loop=loop=-1:size=1,fps=25,setpts=N/25/TB[icraw];
[icraw]split=1[ic0];
[ic0]fade=t=in:st=11.868:d=0.32:alpha=1[icf0];
[base]ass=subs_n2210_3.ass[subbed];
[subbed][icf0]overlay=x=746:y=430:enable='between(t,11.868,16.727)':shortest=1[ov]
" -map "[ov]" -map 1:a -c:v libx264 -preset medium -crf 18 -r 25 -pix_fmt yuv420p -c:a copy "$OUT" -y

set -e
FF=$1; OUT=$2
$FF -hide_banner -loglevel error -i "video2.mp4" -i a2.m4a -i /home/user/-/IMG_0884.png -filter_complex "
[0:v]trim=start=0.0:end=0.4119999999999999,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z0];
[0:v]trim=start=0.4119999999999999:end=1.8399999999999999,setpts=PTS-STARTPTS,crop=w='trunc((1080/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.068),1,if(lt(t,1.428),1-(3*pow((t-1.068)/0.36,2)-2*pow((t-1.068)/0.36,3)),1))))))/2)*2':h='trunc((1920/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.068),1,if(lt(t,1.428),1-(3*pow((t-1.068)/0.36,2)-2*pow((t-1.068)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z1];
[0:v]trim=start=1.8399999999999999:end=11.356,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z2];
[0:v]trim=start=11.356:end=12.575999999999999,setpts=PTS-STARTPTS,crop=w='trunc((1080/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.86),1,if(lt(t,1.22),1-(3*pow((t-0.86)/0.36,2)-2*pow((t-0.86)/0.36,3)),1))))))/2)*2':h='trunc((1920/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.86),1,if(lt(t,1.22),1-(3*pow((t-0.86)/0.36,2)-2*pow((t-0.86)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z3];
[0:v]trim=start=12.575999999999999:end=19.796,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z4];
[0:v]trim=start=19.796:end=21.424,setpts=PTS-STARTPTS,crop=w='trunc((1080/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.268),1,if(lt(t,1.628),1-(3*pow((t-1.268)/0.36,2)-2*pow((t-1.268)/0.36,3)),1))))))/2)*2':h='trunc((1920/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.268),1,if(lt(t,1.628),1-(3*pow((t-1.268)/0.36,2)-2*pow((t-1.268)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z5];
[0:v]trim=start=21.424:end=22.464,setpts=PTS-STARTPTS,crop=w='trunc((1080/(1+0.1399999999999999*(if(lt(t,-0.02),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.68),1,if(lt(t,1.04),1-(3*pow((t-0.68)/0.36,2)-2*pow((t-0.68)/0.36,3)),1))))))/2)*2':h='trunc((1920/(1+0.1399999999999999*(if(lt(t,-0.02),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.68),1,if(lt(t,1.04),1-(3*pow((t-0.68)/0.36,2)-2*pow((t-0.68)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z6];
[0:v]trim=start=22.464:end=26.22,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z7];
[z0][z1][z2][z3][z4][z5][z6][z7]concat=n=8:v=1:a=0[base];
[2:v]scale=280:-1,format=rgba,loop=loop=-1:size=1,fps=25,setpts=N/25/TB[icraw];
[icraw]split=2[ic0][ic1];
[ic0]fade=t=in:st=19.396:d=0.32:alpha=1,fade=t=out:st=22.076:d=0.32:alpha=1[icf0];
[ic1]fade=t=in:st=24.668:d=0.32:alpha=1[icf1];
[base]ass=subs_n2110_2.ass[subbed];
[subbed][icf0]overlay=x=746:y=430:enable='between(t,19.396,22.396)':shortest=1[ovi0];
[ovi0][icf1]overlay=x=746:y=430:enable='between(t,24.668,26.22)':shortest=1[ov]
" -map "[ov]" -map 1:a -c:v libx264 -preset medium -crf 18 -r 25 -pix_fmt yuv420p -c:a copy "$OUT" -y

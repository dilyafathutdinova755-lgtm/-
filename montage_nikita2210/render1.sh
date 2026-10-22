set -e
FF=$1; OUT=$2
$FF -hide_banner -loglevel error -i "video1.mp4" -i a1.m4a -i /home/user/-/IMG_0884.png -filter_complex "
[0:v]trim=start=0.0:end=1.548,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z0];
[0:v]trim=start=1.548:end=2.7279999999999998,setpts=PTS-STARTPTS,crop=w='trunc((1080/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.82),1,if(lt(t,1.18),1-(3*pow((t-0.82)/0.36,2)-2*pow((t-0.82)/0.36,3)),1))))))/2)*2':h='trunc((1920/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.82),1,if(lt(t,1.18),1-(3*pow((t-0.82)/0.36,2)-2*pow((t-0.82)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z1];
[0:v]trim=start=2.7279999999999998:end=12.156,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z2];
[0:v]trim=start=12.156:end=14.16,setpts=PTS-STARTPTS,crop=w='trunc((1080/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.644),1,if(lt(t,2.004),1-(3*pow((t-1.644)/0.36,2)-2*pow((t-1.644)/0.36,3)),1))))))/2)*2':h='trunc((1920/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.644),1,if(lt(t,2.004),1-(3*pow((t-1.644)/0.36,2)-2*pow((t-1.644)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z3];
[0:v]trim=start=14.16:end=14.308,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z4];
[0:v]trim=start=14.308:end=16.208000000000002,setpts=PTS-STARTPTS,crop=w='trunc((1080/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.54),1,if(lt(t,1.9),1-(3*pow((t-1.54)/0.36,2)-2*pow((t-1.54)/0.36,3)),1))))))/2)*2':h='trunc((1920/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.54),1,if(lt(t,1.9),1-(3*pow((t-1.54)/0.36,2)-2*pow((t-1.54)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z5];
[0:v]trim=start=16.208000000000002:end=21.363999999999997,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z6];
[0:v]trim=start=21.363999999999997:end=22.624,setpts=PTS-STARTPTS,crop=w='trunc((1080/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.9),1,if(lt(t,1.26),1-(3*pow((t-0.9)/0.36,2)-2*pow((t-0.9)/0.36,3)),1))))))/2)*2':h='trunc((1920/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.9),1,if(lt(t,1.26),1-(3*pow((t-0.9)/0.36,2)-2*pow((t-0.9)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z7];
[0:v]trim=start=22.624:end=27.97,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z8];
[z0][z1][z2][z3][z4][z5][z6][z7][z8]concat=n=9:v=1:a=0[base];
[2:v]scale=280:-1,format=rgba,loop=loop=-1:size=1,fps=25,setpts=N/25/TB[icraw];
[icraw]split=2[ic0][ic1];
[ic0]fade=t=in:st=19.244:d=0.32:alpha=1,fade=t=out:st=21.924:d=0.32:alpha=1[icf0];
[ic1]fade=t=in:st=25.788:d=0.32:alpha=1[icf1];
[base]ass=subs_n2210_1.ass[subbed];
[subbed][icf0]overlay=x=746:y=430:enable='between(t,19.244,22.244)':shortest=1[ovi0];
[ovi0][icf1]overlay=x=746:y=430:enable='between(t,25.788,27.97)':shortest=1[ov]
" -map "[ov]" -map 1:a -c:v libx264 -preset medium -crf 18 -r 25 -pix_fmt yuv420p -c:a copy "$OUT" -y

set -e
FF=$1; OUT=$2
$FF -hide_banner -loglevel error -i "video2.mp4" -i a2.m4a -i /home/user/-/IMG_0884.png -filter_complex "
[0:v]trim=start=0.0:end=3.332,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z0];
[0:v]trim=start=3.332:end=4.6240000000000006,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.932),1,if(lt(t,1.292),1-(3*pow((t-0.932)/0.36,2)-2*pow((t-0.932)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.932),1,if(lt(t,1.292),1-(3*pow((t-0.932)/0.36,2)-2*pow((t-0.932)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z1];
[0:v]trim=start=4.6240000000000006:end=5.14,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z2];
[0:v]trim=start=5.14:end=6.32,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.82),1,if(lt(t,1.18),1-(3*pow((t-0.82)/0.36,2)-2*pow((t-0.82)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.82),1,if(lt(t,1.18),1-(3*pow((t-0.82)/0.36,2)-2*pow((t-0.82)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z3];
[0:v]trim=start=6.32:end=12.58,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z4];
[0:v]trim=start=12.58:end=14.288,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.348),1,if(lt(t,1.708),1-(3*pow((t-1.348)/0.36,2)-2*pow((t-1.348)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.348),1,if(lt(t,1.708),1-(3*pow((t-1.348)/0.36,2)-2*pow((t-1.348)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z5];
[0:v]trim=start=14.288:end=16.363999999999997,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z6];
[0:v]trim=start=16.363999999999997:end=17.616,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.892),1,if(lt(t,1.252),1-(3*pow((t-0.892)/0.36,2)-2*pow((t-0.892)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.892),1,if(lt(t,1.252),1-(3*pow((t-0.892)/0.36,2)-2*pow((t-0.892)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z7];
[0:v]trim=start=17.616:end=19.97,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z8];
[z0][z1][z2][z3][z4][z5][z6][z7][z8]concat=n=9:v=1:a=0[base];
[2:v]scale=280:-1,format=rgba,loop=loop=-1:size=1,fps=25,setpts=N/25/TB[icraw];
[icraw]split=2[ic0][ic1];
[ic0]fade=t=in:st=11.3:d=0.32:alpha=1,fade=t=out:st=13.98:d=0.32:alpha=1[icf0];
[ic1]fade=t=in:st=18.436:d=0.32:alpha=1[icf1];
[base]ass=subs_m1710_2.ass[subbed];
[subbed][icf0]overlay=x=746:y=430:enable='between(t,11.3,14.3)':shortest=1[ovi0];
[ovi0][icf1]overlay=x=746:y=430:enable='between(t,18.436,19.97)':shortest=1[ov]
" -map "[ov]" -map 1:a -c:v libx264 -preset medium -crf 18 -r 25 -pix_fmt yuv420p -c:a copy "$OUT" -y

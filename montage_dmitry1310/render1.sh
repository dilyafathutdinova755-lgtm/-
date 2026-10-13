set -e
FF=$1; OUT=$2
$FF -hide_banner -loglevel error -i "video1.mp4" -i a1.m4a -i /home/user/-/IMG_0884.png -filter_complex "
[0:v]trim=start=0.0:end=1.436,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z0];
[0:v]trim=start=1.436:end=2.6159999999999997,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.82),1,if(lt(t,1.18),1-(3*pow((t-0.82)/0.36,2)-2*pow((t-0.82)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.82),1,if(lt(t,1.18),1-(3*pow((t-0.82)/0.36,2)-2*pow((t-0.82)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z1];
[0:v]trim=start=2.6159999999999997:end=9.38,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z2];
[0:v]trim=start=9.38:end=10.543999999999999,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.804),1,if(lt(t,1.164),1-(3*pow((t-0.804)/0.36,2)-2*pow((t-0.804)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.804),1,if(lt(t,1.164),1-(3*pow((t-0.804)/0.36,2)-2*pow((t-0.804)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z3];
[0:v]trim=start=10.543999999999999:end=14.372,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z4];
[0:v]trim=start=14.372:end=15.552,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.82),1,if(lt(t,1.18),1-(3*pow((t-0.82)/0.36,2)-2*pow((t-0.82)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.82),1,if(lt(t,1.18),1-(3*pow((t-0.82)/0.36,2)-2*pow((t-0.82)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z5];
[0:v]trim=start=15.552:end=16.7,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z6];
[0:v]trim=start=16.7:end=17.872,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.812),1,if(lt(t,1.172),1-(3*pow((t-0.812)/0.36,2)-2*pow((t-0.812)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.812),1,if(lt(t,1.172),1-(3*pow((t-0.812)/0.36,2)-2*pow((t-0.812)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z7];
[0:v]trim=start=17.872:end=19.884,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z8];
[z0][z1][z2][z3][z4][z5][z6][z7][z8]concat=n=9:v=1:a=0[base];
[2:v]scale=280:-1,format=rgba,loop=loop=-1:size=1,fps=25,setpts=N/25/TB[icraw];
[icraw]split=2[ic0][ic1];
[ic0]fade=t=in:st=13.292:d=0.32:alpha=1,fade=t=out:st=15.972:d=0.32:alpha=1[icf0];
[ic1]fade=t=in:st=18.34:d=0.32:alpha=1[icf1];
[base]ass=subs_d1310_1.ass[subbed];
[subbed][icf0]overlay=x=746:y=430:enable='between(t,13.292,16.292)':shortest=1[ovi0];
[ovi0][icf1]overlay=x=746:y=430:enable='between(t,18.34,19.884)':shortest=1[ov]
" -map "[ov]" -map 1:a -c:v libx264 -preset medium -crf 18 -r 25 -pix_fmt yuv420p -c:a copy "$OUT" -y

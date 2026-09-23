set -e
FF=$1; OUT=$2
$FF -hide_banner -loglevel error -i "video2.mp4" -i a2.m4a -i /home/user/-/IMG_0884.png -filter_complex "
[0:v]trim=start=0.0:end=5.34,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z0];
[0:v]trim=start=5.34:end=6.416,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.716),1,if(lt(t,1.076),1-(3*pow((t-0.716)/0.36,2)-2*pow((t-0.716)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.716),1,if(lt(t,1.076),1-(3*pow((t-0.716)/0.36,2)-2*pow((t-0.716)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z1];
[0:v]trim=start=6.416:end=7.54,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z2];
[0:v]trim=start=7.54:end=8.92,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.02),1,if(lt(t,1.38),1-(3*pow((t-1.02)/0.36,2)-2*pow((t-1.02)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.02),1,if(lt(t,1.38),1-(3*pow((t-1.02)/0.36,2)-2*pow((t-1.02)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z3];
[0:v]trim=start=8.92:end=16.299999999999997,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z4];
[0:v]trim=start=16.299999999999997:end=17.64,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.98),1,if(lt(t,1.34),1-(3*pow((t-0.98)/0.36,2)-2*pow((t-0.98)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.98),1,if(lt(t,1.34),1-(3*pow((t-0.98)/0.36,2)-2*pow((t-0.98)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z5];
[0:v]trim=start=17.64:end=17.9,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z6];
[0:v]trim=start=17.9:end=19.216,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.956),1,if(lt(t,1.316),1-(3*pow((t-0.956)/0.36,2)-2*pow((t-0.956)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.956),1,if(lt(t,1.316),1-(3*pow((t-0.956)/0.36,2)-2*pow((t-0.956)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z7];
[0:v]trim=start=19.216:end=21.911,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z8];
[z0][z1][z2][z3][z4][z5][z6][z7][z8]concat=n=9:v=1:a=0[base];
[2:v]scale=280:-1,format=rgba,loop=loop=-1:size=1,fps=25,setpts=N/25/TB[icraw];
[icraw]split=2[ic0][ic1];
[ic0]fade=t=in:st=11.764:d=0.32:alpha=1,fade=t=out:st=14.444:d=0.32:alpha=1[icf0];
[ic1]fade=t=in:st=20.116:d=0.32:alpha=1[icf1];
[base]ass=subs_m2309111_2.ass[subbed];
[subbed][icf0]overlay=x=746:y=430:enable='between(t,11.764,14.764)':shortest=1[ovi0];
[ovi0][icf1]overlay=x=746:y=430:enable='between(t,20.116,21.911)':shortest=1[ov]
" -map "[ov]" -map 1:a -c:v libx264 -preset medium -crf 18 -r 25 -pix_fmt yuv420p -c:a copy "$OUT" -y

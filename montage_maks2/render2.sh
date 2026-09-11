set -e
FF=$1; OUT=$2
$FF -hide_banner -loglevel error -i "Untitled.Video.11.09.2_2160p.mp4" -i a2.m4a -i /home/user/-/IMG_0884.png -filter_complex "
[0:v]trim=start=0.0:end=5.239999999999999,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z0];
[0:v]trim=start=5.239999999999999:end=6.680000000000001,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.08),1,if(lt(t,1.44),1-(3*pow((t-1.08)/0.36,2)-2*pow((t-1.08)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.08),1,if(lt(t,1.44),1-(3*pow((t-1.08)/0.36,2)-2*pow((t-1.08)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z1];
[0:v]trim=start=6.680000000000001:end=8.360000000000001,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z2];
[0:v]trim=start=8.360000000000001:end=9.559999999999999,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.84),1,if(lt(t,1.2),1-(3*pow((t-0.84)/0.36,2)-2*pow((t-0.84)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.84),1,if(lt(t,1.2),1-(3*pow((t-0.84)/0.36,2)-2*pow((t-0.84)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z3];
[0:v]trim=start=9.559999999999999:end=20.709999999999997,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z4];
[0:v]trim=start=20.709999999999997:end=22.259999999999998,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.19),1,if(lt(t,1.55),1-(3*pow((t-1.19)/0.36,2)-2*pow((t-1.19)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.19),1,if(lt(t,1.55),1-(3*pow((t-1.19)/0.36,2)-2*pow((t-1.19)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z5];
[0:v]trim=start=22.259999999999998:end=30.84,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z6];
[0:v]trim=start=30.84:end=32.04,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.84),1,if(lt(t,1.2),1-(3*pow((t-0.84)/0.36,2)-2*pow((t-0.84)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.84),1,if(lt(t,1.2),1-(3*pow((t-0.84)/0.36,2)-2*pow((t-0.84)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z7];
[0:v]trim=start=32.04:end=36.93,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z8];
[z0][z1][z2][z3][z4][z5][z6][z7][z8]concat=n=9:v=1:a=0[base];
[2:v]scale=280:-1,format=rgba,loop=loop=-1:size=1,fps=25,setpts=N/25/TB[icraw];
[icraw]split=2[ic0][ic1];
[ic0]fade=t=in:st=13.364:d=0.32:alpha=1,fade=t=out:st=16.044:d=0.32:alpha=1[icf0];
[ic1]fade=t=in:st=35.156:d=0.32:alpha=1[icf1];
[base]ass=subs_x2.ass[subbed];
[subbed][icf0]overlay=x=746:y=430:enable='between(t,13.364,16.364)':shortest=1[ovi0];
[ovi0][icf1]overlay=x=746:y=430:enable='between(t,35.156,36.93)':shortest=1[ov]
" -map "[ov]" -map 1:a -c:v libx264 -preset medium -crf 18 -r 25 -pix_fmt yuv420p -c:a copy "$OUT" -y

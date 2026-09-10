set -e
FF=$1; OUT=$2
$FF -hide_banner -loglevel error -i Untitled.Video.1.10.09_2160p.mp4 -i a1.m4a -i /home/user/-/IMG_0884.png -filter_complex "
[0:v]trim=start=0.0:end=7.029999999999999,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z0];
[0:v]trim=start=7.029999999999999:end=8.27,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.88),1,if(lt(t,1.24),1-(3*pow((t-0.88)/0.36,2)-2*pow((t-0.88)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.88),1,if(lt(t,1.24),1-(3*pow((t-0.88)/0.36,2)-2*pow((t-0.88)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z1];
[0:v]trim=start=8.27:end=19.959999999999997,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z2];
[0:v]trim=start=19.959999999999997:end=21.2,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.88),1,if(lt(t,1.24),1-(3*pow((t-0.88)/0.36,2)-2*pow((t-0.88)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.88),1,if(lt(t,1.24),1-(3*pow((t-0.88)/0.36,2)-2*pow((t-0.88)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z3];
[0:v]trim=start=21.2:end=23.14,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z4];
[0:v]trim=start=23.14:end=24.419999999999998,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.92),1,if(lt(t,1.28),1-(3*pow((t-0.92)/0.36,2)-2*pow((t-0.92)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.92),1,if(lt(t,1.28),1-(3*pow((t-0.92)/0.36,2)-2*pow((t-0.92)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z5];
[0:v]trim=start=24.419999999999998:end=24.64,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z6];
[0:v]trim=start=24.64:end=25.96,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.96),1,if(lt(t,1.32),1-(3*pow((t-0.96)/0.36,2)-2*pow((t-0.96)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.96),1,if(lt(t,1.32),1-(3*pow((t-0.96)/0.36,2)-2*pow((t-0.96)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z7];
[0:v]trim=start=25.96:end=32.04,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z8];
[z0][z1][z2][z3][z4][z5][z6][z7][z8]concat=n=9:v=1:a=0[base];
[2:v]scale=280:-1,format=rgba,loop=loop=-1:size=1,fps=25,setpts=N/25/TB[icraw];
[icraw]split=2[ic0][ic1];
[ic0]fade=t=in:st=18.924:d=0.32:alpha=1,fade=t=out:st=21.604:d=0.32:alpha=1[icf0];
[ic1]fade=t=in:st=30.484:d=0.32:alpha=1[icf1];
[base]ass=subs_v1.ass[subbed];
[subbed][icf0]overlay=x=746:y=430:enable='between(t,18.924,21.924)':shortest=1[ovi0];
[ovi0][icf1]overlay=x=746:y=430:enable='between(t,30.484,32.04)':shortest=1[ov]
" -map "[ov]" -map 1:a -c:v libx264 -preset medium -crf 18 -r 25 -pix_fmt yuv420p -c:a copy "$OUT" -y

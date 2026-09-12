set -e
FF=$1; OUT=$2
$FF -hide_banner -loglevel error -i "Untitled.Video.12.09.2_2160p.mp4" -i a2.m4a -i /home/user/-/IMG_0884.png -filter_complex "
[0:v]trim=start=0.0:end=4.92,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z0];
[0:v]trim=start=4.92:end=6.54,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.26),1,if(lt(t,1.62),1-(3*pow((t-1.26)/0.36,2)-2*pow((t-1.26)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.26),1,if(lt(t,1.62),1-(3*pow((t-1.26)/0.36,2)-2*pow((t-1.26)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z1];
[0:v]trim=start=6.54:end=11.110000000000001,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z2];
[0:v]trim=start=11.110000000000001:end=12.53,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.06),1,if(lt(t,1.42),1-(3*pow((t-1.06)/0.36,2)-2*pow((t-1.06)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.06),1,if(lt(t,1.42),1-(3*pow((t-1.06)/0.36,2)-2*pow((t-1.06)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z3];
[0:v]trim=start=12.53:end=19.209999999999997,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z4];
[0:v]trim=start=19.209999999999997:end=20.95,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.38),1,if(lt(t,1.74),1-(3*pow((t-1.38)/0.36,2)-2*pow((t-1.38)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.38),1,if(lt(t,1.74),1-(3*pow((t-1.38)/0.36,2)-2*pow((t-1.38)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z5];
[0:v]trim=start=20.95:end=25.08,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z6];
[0:v]trim=start=25.08:end=27.06,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.62),1,if(lt(t,1.98),1-(3*pow((t-1.62)/0.36,2)-2*pow((t-1.62)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.62),1,if(lt(t,1.98),1-(3*pow((t-1.62)/0.36,2)-2*pow((t-1.62)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z7];
[0:v]trim=start=27.06:end=31.4,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z8];
[z0][z1][z2][z3][z4][z5][z6][z7][z8]concat=n=9:v=1:a=0[base];
[2:v]scale=280:-1,format=rgba,loop=loop=-1:size=1,fps=25,setpts=N/25/TB[icraw];
[icraw]split=2[ic0][ic1];
[ic0]fade=t=in:st=10.428:d=0.32:alpha=1,fade=t=out:st=13.108:d=0.32:alpha=1[icf0];
[ic1]fade=t=in:st=29.892:d=0.32:alpha=1[icf1];
[base]ass=subs_s2.ass[subbed];
[subbed][icf0]overlay=x=746:y=430:enable='between(t,10.428,13.428)':shortest=1[ovi0];
[ovi0][icf1]overlay=x=746:y=430:enable='between(t,29.892,31.4)':shortest=1[ov]
" -map "[ov]" -map 1:a -c:v libx264 -preset medium -crf 18 -r 25 -pix_fmt yuv420p -c:a copy "$OUT" -y

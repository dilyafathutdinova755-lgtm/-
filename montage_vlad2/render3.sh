set -e
FF=$1; OUT=$2
$FF -hide_banner -loglevel error -i Untitled.Video.3.10.09_2160p.mp4 -i a3.m4a -i /home/user/-/IMG_0884.png -filter_complex "
[0:v]trim=start=0.0:end=6.18,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z0];
[0:v]trim=start=6.18:end=7.300000000000001,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.76),1,if(lt(t,1.12),1-(3*pow((t-0.76)/0.36,2)-2*pow((t-0.76)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.76),1,if(lt(t,1.12),1-(3*pow((t-0.76)/0.36,2)-2*pow((t-0.76)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z1];
[0:v]trim=start=7.300000000000001:end=9.08,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z2];
[0:v]trim=start=9.08:end=10.28,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.84),1,if(lt(t,1.2),1-(3*pow((t-0.84)/0.36,2)-2*pow((t-0.84)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.84),1,if(lt(t,1.2),1-(3*pow((t-0.84)/0.36,2)-2*pow((t-0.84)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z3];
[0:v]trim=start=10.28:end=21.36,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z4];
[0:v]trim=start=21.36:end=22.2,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.48),1,if(lt(t,0.84),1-(3*pow((t-0.48)/0.36,2)-2*pow((t-0.48)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.48),1,if(lt(t,0.84),1-(3*pow((t-0.48)/0.36,2)-2*pow((t-0.48)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z5];
[0:v]trim=start=22.2:end=24.54,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z6];
[0:v]trim=start=24.54:end=25.7,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.8),1,if(lt(t,1.16),1-(3*pow((t-0.8)/0.36,2)-2*pow((t-0.8)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.8),1,if(lt(t,1.16),1-(3*pow((t-0.8)/0.36,2)-2*pow((t-0.8)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z7];
[0:v]trim=start=25.7:end=29.89,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z8];
[z0][z1][z2][z3][z4][z5][z6][z7][z8]concat=n=9:v=1:a=0[base];
[2:v]scale=280:-1,format=rgba,loop=loop=-1:size=1,fps=25,setpts=N/25/TB[icraw];
[icraw]split=2[ic0][ic1];
[ic0]fade=t=in:st=17.356:d=0.32:alpha=1,fade=t=out:st=20.036:d=0.32:alpha=1[icf0];
[ic1]fade=t=in:st=28.268:d=0.32:alpha=1[icf1];
[base]ass=subs_v3.ass[subbed];
[subbed][icf0]overlay=x=746:y=430:enable='between(t,17.356,20.356)':shortest=1[ovi0];
[ovi0][icf1]overlay=x=746:y=430:enable='between(t,28.268,29.89)':shortest=1[ov]
" -map "[ov]" -map 1:a -c:v libx264 -preset medium -crf 18 -r 25 -pix_fmt yuv420p -c:a copy "$OUT" -y

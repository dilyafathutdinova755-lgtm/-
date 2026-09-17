set -e
FF=$1; OUT=$2
$FF -hide_banner -loglevel error -i "video3.mp4" -i a3.m4a -i /home/user/-/IMG_0884.png -filter_complex "
[0:v]trim=start=0.0:end=7.56,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z0];
[0:v]trim=start=7.56:end=8.879999999999999,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.96),1,if(lt(t,1.32),1-(3*pow((t-0.96)/0.36,2)-2*pow((t-0.96)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.96),1,if(lt(t,1.32),1-(3*pow((t-0.96)/0.36,2)-2*pow((t-0.96)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z1];
[0:v]trim=start=8.879999999999999:end=14.56,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z2];
[0:v]trim=start=14.56:end=15.979999999999999,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.06),1,if(lt(t,1.42),1-(3*pow((t-1.06)/0.36,2)-2*pow((t-1.06)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.06),1,if(lt(t,1.42),1-(3*pow((t-1.06)/0.36,2)-2*pow((t-1.06)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z3];
[0:v]trim=start=15.979999999999999:end=24.23,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z4];
[0:v]trim=start=24.23:end=25.97,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.38),1,if(lt(t,1.74),1-(3*pow((t-1.38)/0.36,2)-2*pow((t-1.38)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.38),1,if(lt(t,1.74),1-(3*pow((t-1.38)/0.36,2)-2*pow((t-1.38)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z5];
[0:v]trim=start=25.97:end=30.119999999999997,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z6];
[0:v]trim=start=30.119999999999997:end=31.66,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.18),1,if(lt(t,1.54),1-(3*pow((t-1.18)/0.36,2)-2*pow((t-1.18)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.18),1,if(lt(t,1.54),1-(3*pow((t-1.18)/0.36,2)-2*pow((t-1.18)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z7];
[0:v]trim=start=31.66:end=32.386,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z8];
[z0][z1][z2][z3][z4][z5][z6][z7][z8]concat=n=9:v=1:a=0[base];
[2:v]scale=280:-1,format=rgba,loop=loop=-1:size=1,fps=25,setpts=N/25/TB[icraw];
[icraw]split=2[ic0][ic1];
[ic0]fade=t=in:st=6.86:d=0.32:alpha=1,fade=t=out:st=9.54:d=0.32:alpha=1[icf0];
[ic1]fade=t=in:st=30.724:d=0.32:alpha=1[icf1];
[base]ass=subs_m1709_3.ass[subbed];
[subbed][icf0]overlay=x=746:y=430:enable='between(t,6.86,9.86)':shortest=1[ovi0];
[ovi0][icf1]overlay=x=746:y=430:enable='between(t,30.724,32.386)':shortest=1[ov]
" -map "[ov]" -map 1:a -c:v libx264 -preset medium -crf 18 -r 25 -pix_fmt yuv420p -c:a copy "$OUT" -y

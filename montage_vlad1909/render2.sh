set -e
FF=$1; OUT=$2
$FF -hide_banner -loglevel error -i "video2.mp4" -i a2.m4a -i /home/user/-/IMG_0884.png -filter_complex "
[0:v]trim=start=0.0:end=7.52,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z0];
[0:v]trim=start=7.52:end=9.18,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.3),1,if(lt(t,1.66),1-(3*pow((t-1.3)/0.36,2)-2*pow((t-1.3)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.3),1,if(lt(t,1.66),1-(3*pow((t-1.3)/0.36,2)-2*pow((t-1.3)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z1];
[0:v]trim=start=9.18:end=10.41,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z2];
[0:v]trim=start=10.41:end=12.299999999999999,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.53),1,if(lt(t,1.89),1-(3*pow((t-1.53)/0.36,2)-2*pow((t-1.53)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.53),1,if(lt(t,1.89),1-(3*pow((t-1.53)/0.36,2)-2*pow((t-1.53)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z3];
[0:v]trim=start=12.299999999999999:end=14.01,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z4];
[0:v]trim=start=14.01:end=15.75,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.38),1,if(lt(t,1.74),1-(3*pow((t-1.38)/0.36,2)-2*pow((t-1.38)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.38),1,if(lt(t,1.74),1-(3*pow((t-1.38)/0.36,2)-2*pow((t-1.38)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z5];
[0:v]trim=start=15.75:end=20.0,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z6];
[0:v]trim=start=20.0:end=21.439999999999998,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.08),1,if(lt(t,1.44),1-(3*pow((t-1.08)/0.36,2)-2*pow((t-1.08)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.08),1,if(lt(t,1.44),1-(3*pow((t-1.08)/0.36,2)-2*pow((t-1.08)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z7];
[0:v]trim=start=21.439999999999998:end=31.96,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z8];
[z0][z1][z2][z3][z4][z5][z6][z7][z8]concat=n=9:v=1:a=0[base];
[2:v]scale=280:-1,format=rgba,loop=loop=-1:size=1,fps=25,setpts=N/25/TB[icraw];
[icraw]split=2[ic0][ic1];
[ic0]fade=t=in:st=6.348:d=0.32:alpha=1,fade=t=out:st=9.028:d=0.32:alpha=1[icf0];
[ic1]fade=t=in:st=30.316:d=0.32:alpha=1[icf1];
[base]ass=subs_v1909_2.ass[subbed];
[subbed][icf0]overlay=x=746:y=430:enable='between(t,6.348,9.347999999999999)':shortest=1[ovi0];
[ovi0][icf1]overlay=x=746:y=430:enable='between(t,30.316,31.96)':shortest=1[ov]
" -map "[ov]" -map 1:a -c:v libx264 -preset medium -crf 18 -r 25 -pix_fmt yuv420p -c:a copy "$OUT" -y

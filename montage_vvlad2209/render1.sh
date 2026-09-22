set -e
FF=$1; OUT=$2
$FF -hide_banner -loglevel error -i "video1.mp4" -i a1.m4a -i /home/user/-/IMG_0884.png -filter_complex "
[0:v]trim=start=0.0:end=5.68,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z0];
[0:v]trim=start=5.68:end=7.82,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.78),1,if(lt(t,2.14),1-(3*pow((t-1.78)/0.36,2)-2*pow((t-1.78)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.78),1,if(lt(t,2.14),1-(3*pow((t-1.78)/0.36,2)-2*pow((t-1.78)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z1];
[0:v]trim=start=7.82:end=14.34,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z2];
[0:v]trim=start=14.34:end=16.32,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.62),1,if(lt(t,1.98),1-(3*pow((t-1.62)/0.36,2)-2*pow((t-1.62)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.62),1,if(lt(t,1.98),1-(3*pow((t-1.62)/0.36,2)-2*pow((t-1.62)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z3];
[0:v]trim=start=16.32:end=17.89,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.03),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.21),1,if(lt(t,1.57),1-(3*pow((t-1.21)/0.36,2)-2*pow((t-1.21)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.03),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.21),1,if(lt(t,1.57),1-(3*pow((t-1.21)/0.36,2)-2*pow((t-1.21)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z4];
[0:v]trim=start=17.89:end=19.23,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z5];
[0:v]trim=start=19.23:end=20.46,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.87),1,if(lt(t,1.23),1-(3*pow((t-0.87)/0.36,2)-2*pow((t-0.87)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.87),1,if(lt(t,1.23),1-(3*pow((t-0.87)/0.36,2)-2*pow((t-0.87)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z6];
[0:v]trim=start=20.46:end=22.764,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z7];
[z0][z1][z2][z3][z4][z5][z6][z7]concat=n=8:v=1:a=0[base];
[2:v]scale=280:-1,format=rgba,loop=loop=-1:size=1,fps=25,setpts=N/25/TB[icraw];
[icraw]split=2[ic0][ic1];
[ic0]fade=t=in:st=10.564:d=0.32:alpha=1,fade=t=out:st=13.244:d=0.32:alpha=1[icf0];
[ic1]fade=t=in:st=21.124:d=0.32:alpha=1[icf1];
[base]ass=subs_vv2209_1.ass[subbed];
[subbed][icf0]overlay=x=746:y=430:enable='between(t,10.564,13.564)':shortest=1[ovi0];
[ovi0][icf1]overlay=x=746:y=430:enable='between(t,21.124,22.764)':shortest=1[ov]
" -map "[ov]" -map 1:a -c:v libx264 -preset medium -crf 18 -r 25 -pix_fmt yuv420p -c:a copy "$OUT" -y

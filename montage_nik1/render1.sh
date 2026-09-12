set -e
FF=$1; OUT=$2
$FF -hide_banner -loglevel error -i "Untitled.Video.12.09.1_2160p.mp4" -i a1.m4a -i /home/user/-/IMG_0884.png -filter_complex "
[0:v]trim=start=0.0:end=4.609999999999999,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z0];
[0:v]trim=start=4.609999999999999:end=5.57,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.6),1,if(lt(t,0.96),1-(3*pow((t-0.6)/0.36,2)-2*pow((t-0.6)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.6),1,if(lt(t,0.96),1-(3*pow((t-0.6)/0.36,2)-2*pow((t-0.6)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z1];
[0:v]trim=start=5.57:end=17.72,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z2];
[0:v]trim=start=17.72:end=18.99,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.91),1,if(lt(t,1.27),1-(3*pow((t-0.91)/0.36,2)-2*pow((t-0.91)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.91),1,if(lt(t,1.27),1-(3*pow((t-0.91)/0.36,2)-2*pow((t-0.91)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z3];
[0:v]trim=start=18.99:end=21.24,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z4];
[0:v]trim=start=21.24:end=22.52,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.92),1,if(lt(t,1.28),1-(3*pow((t-0.92)/0.36,2)-2*pow((t-0.92)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.92),1,if(lt(t,1.28),1-(3*pow((t-0.92)/0.36,2)-2*pow((t-0.92)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z5];
[0:v]trim=start=22.52:end=29.7,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z6];
[0:v]trim=start=29.7:end=30.98,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.92),1,if(lt(t,1.28),1-(3*pow((t-0.92)/0.36,2)-2*pow((t-0.92)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.92),1,if(lt(t,1.28),1-(3*pow((t-0.92)/0.36,2)-2*pow((t-0.92)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z7];
[0:v]trim=start=30.98:end=35.65,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z8];
[z0][z1][z2][z3][z4][z5][z6][z7][z8]concat=n=9:v=1:a=0[base];
[2:v]scale=280:-1,format=rgba,loop=loop=-1:size=1,fps=25,setpts=N/25/TB[icraw];
[icraw]split=2[ic0][ic1];
[ic0]fade=t=in:st=10.868:d=0.32:alpha=1,fade=t=out:st=13.548:d=0.32:alpha=1[icf0];
[ic1]fade=t=in:st=33.9:d=0.32:alpha=1[icf1];
[base]ass=subs_n1.ass[subbed];
[subbed][icf0]overlay=x=746:y=430:enable='between(t,10.868,13.868)':shortest=1[ovi0];
[ovi0][icf1]overlay=x=746:y=430:enable='between(t,33.9,35.65)':shortest=1[ov]
" -map "[ov]" -map 1:a -c:v libx264 -preset medium -crf 18 -r 25 -pix_fmt yuv420p -c:a copy "$OUT" -y

set -e
FF=$1; OUT=$2
$FF -hide_banner -loglevel error -i "Untitled.Video.2.10.09_2160p.mp4" -i a2.m4a -i /home/user/-/IMG_0884.png -filter_complex "
[0:v]trim=start=0.0:end=23.04,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z0];
[0:v]trim=start=23.04:end=24.08,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.68),1,if(lt(t,1.04),1-(3*pow((t-0.68)/0.36,2)-2*pow((t-0.68)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.68),1,if(lt(t,1.04),1-(3*pow((t-0.68)/0.36,2)-2*pow((t-0.68)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z1];
[0:v]trim=start=24.08:end=27.04,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z2];
[0:v]trim=start=27.04:end=28.0,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.6),1,if(lt(t,0.96),1-(3*pow((t-0.6)/0.36,2)-2*pow((t-0.6)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.6),1,if(lt(t,0.96),1-(3*pow((t-0.6)/0.36,2)-2*pow((t-0.6)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z3];
[0:v]trim=start=28.0:end=29.79,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z4];
[0:v]trim=start=29.79:end=31.07,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.92),1,if(lt(t,1.28),1-(3*pow((t-0.92)/0.36,2)-2*pow((t-0.92)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.92),1,if(lt(t,1.28),1-(3*pow((t-0.92)/0.36,2)-2*pow((t-0.92)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z5];
[0:v]trim=start=31.07:end=33.519999999999996,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z6];
[0:v]trim=start=33.519999999999996:end=34.519999999999996,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.64),1,if(lt(t,1.0),1-(3*pow((t-0.64)/0.36,2)-2*pow((t-0.64)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.64),1,if(lt(t,1.0),1-(3*pow((t-0.64)/0.36,2)-2*pow((t-0.64)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z7];
[0:v]trim=start=34.519999999999996:end=37.89,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z8];
[z0][z1][z2][z3][z4][z5][z6][z7][z8]concat=n=9:v=1:a=0[base];
[2:v]scale=280:-1,format=rgba,loop=loop=-1:size=1,fps=25,setpts=N/25/TB[icraw];
[icraw]split=2[ic0][ic1];
[ic0]fade=t=in:st=13.076:d=0.32:alpha=1,fade=t=out:st=15.756:d=0.32:alpha=1[icf0];
[ic1]fade=t=in:st=36.268:d=0.32:alpha=1[icf1];
[base]ass=subs_m2.ass[subbed];
[subbed][icf0]overlay=x=746:y=430:enable='between(t,13.076,16.076)':shortest=1[ovi0];
[ovi0][icf1]overlay=x=746:y=430:enable='between(t,36.268,37.89)':shortest=1[ov]
" -map "[ov]" -map 1:a -c:v libx264 -preset medium -crf 18 -r 25 -pix_fmt yuv420p -c:a copy "$OUT" -y

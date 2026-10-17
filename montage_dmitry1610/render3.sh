set -e
FF=$1; OUT=$2
$FF -hide_banner -loglevel error -i "video3.mp4" -i a3.m4a -i /home/user/-/IMG_0884.png -filter_complex "
[0:v]trim=start=0.0:end=3.3499999999999996,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z0];
[0:v]trim=start=3.3499999999999996:end=4.69,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.98),1,if(lt(t,1.34),1-(3*pow((t-0.98)/0.36,2)-2*pow((t-0.98)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.98),1,if(lt(t,1.34),1-(3*pow((t-0.98)/0.36,2)-2*pow((t-0.98)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z1];
[0:v]trim=start=4.69:end=5.6000000000000005,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.17),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.55),1,if(lt(t,0.91),1-(3*pow((t-0.55)/0.36,2)-2*pow((t-0.55)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.17),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.55),1,if(lt(t,0.91),1-(3*pow((t-0.55)/0.36,2)-2*pow((t-0.55)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z2];
[0:v]trim=start=5.6000000000000005:end=12.41,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z3];
[0:v]trim=start=12.41:end=13.709999999999999,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.94),1,if(lt(t,1.3),1-(3*pow((t-0.94)/0.36,2)-2*pow((t-0.94)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.94),1,if(lt(t,1.3),1-(3*pow((t-0.94)/0.36,2)-2*pow((t-0.94)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z4];
[0:v]trim=start=13.709999999999999:end=21.099999999999998,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z5];
[0:v]trim=start=21.099999999999998:end=22.38,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.92),1,if(lt(t,1.28),1-(3*pow((t-0.92)/0.36,2)-2*pow((t-0.92)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.92),1,if(lt(t,1.28),1-(3*pow((t-0.92)/0.36,2)-2*pow((t-0.92)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z6];
[0:v]trim=start=22.38:end=24.364,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z7];
[z0][z1][z2][z3][z4][z5][z6][z7]concat=n=8:v=1:a=0[base];
[2:v]scale=280:-1,format=rgba,loop=loop=-1:size=1,fps=25,setpts=N/25/TB[icraw];
[icraw]split=2[ic0][ic1];
[ic0]fade=t=in:st=14.132:d=0.32:alpha=1,fade=t=out:st=16.812:d=0.32:alpha=1[icf0];
[ic1]fade=t=in:st=22.852:d=0.32:alpha=1[icf1];
[base]ass=subs_d1610_3.ass[subbed];
[subbed][icf0]overlay=x=746:y=430:enable='between(t,14.132,17.131999999999998)':shortest=1[ovi0];
[ovi0][icf1]overlay=x=746:y=430:enable='between(t,22.852,24.364)':shortest=1[ov]
" -map "[ov]" -map 1:a -c:v libx264 -preset medium -crf 18 -r 25 -pix_fmt yuv420p -c:a copy "$OUT" -y

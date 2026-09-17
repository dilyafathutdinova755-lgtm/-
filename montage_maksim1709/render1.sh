set -e
FF=$1; OUT=$2
$FF -hide_banner -loglevel error -i "video1.mp4" -i a1.m4a -i /home/user/-/IMG_0884.png -filter_complex "
[0:v]trim=start=0.0:end=10.13,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z0];
[0:v]trim=start=10.13:end=11.43,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.94),1,if(lt(t,1.3),1-(3*pow((t-0.94)/0.36,2)-2*pow((t-0.94)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.94),1,if(lt(t,1.3),1-(3*pow((t-0.94)/0.36,2)-2*pow((t-0.94)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z1];
[0:v]trim=start=11.43:end=18.919999999999998,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z2];
[0:v]trim=start=18.919999999999998:end=20.3,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.02),1,if(lt(t,1.38),1-(3*pow((t-1.02)/0.36,2)-2*pow((t-1.02)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.02),1,if(lt(t,1.38),1-(3*pow((t-1.02)/0.36,2)-2*pow((t-1.02)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z3];
[0:v]trim=start=20.3:end=27.4,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z4];
[0:v]trim=start=27.4:end=28.78,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.02),1,if(lt(t,1.38),1-(3*pow((t-1.02)/0.36,2)-2*pow((t-1.02)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.02),1,if(lt(t,1.38),1-(3*pow((t-1.02)/0.36,2)-2*pow((t-1.02)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z5];
[0:v]trim=start=28.78:end=33.839999999999996,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z6];
[0:v]trim=start=33.839999999999996:end=35.41,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.21),1,if(lt(t,1.57),1-(3*pow((t-1.21)/0.36,2)-2*pow((t-1.21)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.21),1,if(lt(t,1.57),1-(3*pow((t-1.21)/0.36,2)-2*pow((t-1.21)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z7];
[0:v]trim=start=35.41:end=36.055,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z8];
[z0][z1][z2][z3][z4][z5][z6][z7][z8]concat=n=9:v=1:a=0[base];
[2:v]scale=280:-1,format=rgba,loop=loop=-1:size=1,fps=25,setpts=N/25/TB[icraw];
[icraw]split=2[ic0][ic1];
[ic0]fade=t=in:st=9.732:d=0.32:alpha=1,fade=t=out:st=12.412:d=0.32:alpha=1[icf0];
[ic1]fade=t=in:st=34.436:d=0.32:alpha=1[icf1];
[base]ass=subs_m1709_1.ass[subbed];
[subbed][icf0]overlay=x=746:y=430:enable='between(t,9.732,12.732)':shortest=1[ovi0];
[ovi0][icf1]overlay=x=746:y=430:enable='between(t,34.436,36.055)':shortest=1[ov]
" -map "[ov]" -map 1:a -c:v libx264 -preset medium -crf 18 -r 25 -pix_fmt yuv420p -c:a copy "$OUT" -y

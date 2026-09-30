set -e
FF=$1; OUT=$2
$FF -hide_banner -loglevel error -i "video3.mp4" -i a3.m4a -i /home/user/-/IMG_0884.png -filter_complex "
[0:v]trim=start=0.0:end=5.867999999999999,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z0];
[0:v]trim=start=5.867999999999999:end=7.5280000000000005,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.3),1,if(lt(t,1.66),1-(3*pow((t-1.3)/0.36,2)-2*pow((t-1.3)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.3),1,if(lt(t,1.66),1-(3*pow((t-1.3)/0.36,2)-2*pow((t-1.3)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z1];
[0:v]trim=start=7.5280000000000005:end=13.796000000000001,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z2];
[0:v]trim=start=13.796000000000001:end=15.344,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.188),1,if(lt(t,1.548),1-(3*pow((t-1.188)/0.36,2)-2*pow((t-1.188)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.188),1,if(lt(t,1.548),1-(3*pow((t-1.188)/0.36,2)-2*pow((t-1.188)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z3];
[0:v]trim=start=15.344:end=19.764,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z4];
[0:v]trim=start=19.764:end=21.663999999999998,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.54),1,if(lt(t,1.9),1-(3*pow((t-1.54)/0.36,2)-2*pow((t-1.54)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.54),1,if(lt(t,1.9),1-(3*pow((t-1.54)/0.36,2)-2*pow((t-1.54)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z5];
[0:v]trim=start=21.663999999999998:end=22.404,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z6];
[0:v]trim=start=22.404:end=23.424,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.66),1,if(lt(t,1.02),1-(3*pow((t-0.66)/0.36,2)-2*pow((t-0.66)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.66),1,if(lt(t,1.02),1-(3*pow((t-0.66)/0.36,2)-2*pow((t-0.66)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z7];
[0:v]trim=start=23.424:end=24.77,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z8];
[z0][z1][z2][z3][z4][z5][z6][z7][z8]concat=n=9:v=1:a=0[base];
[2:v]scale=280:-1,format=rgba,loop=loop=-1:size=1,fps=25,setpts=N/25/TB[icraw];
[icraw]split=2[ic0][ic1];
[ic0]fade=t=in:st=15.684:d=0.32:alpha=1,fade=t=out:st=18.364:d=0.32:alpha=1[icf0];
[ic1]fade=t=in:st=23.244:d=0.32:alpha=1[icf1];
[base]ass=subs_d3009_3.ass[subbed];
[subbed][icf0]overlay=x=746:y=430:enable='between(t,15.684,18.683999999999997)':shortest=1[ovi0];
[ovi0][icf1]overlay=x=746:y=430:enable='between(t,23.244,24.77)':shortest=1[ov]
" -map "[ov]" -map 1:a -c:v libx264 -preset medium -crf 18 -r 25 -pix_fmt yuv420p -c:a copy "$OUT" -y

set -e
FF=$1; OUT=$2
$FF -hide_banner -loglevel error -i "video2.mp4" -i a2.m4a -i /home/user/-/IMG_0884.png -filter_complex "
[0:v]trim=start=0.0:end=3.3,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z0];
[0:v]trim=start=3.3:end=4.48,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.82),1,if(lt(t,1.18),1-(3*pow((t-0.82)/0.36,2)-2*pow((t-0.82)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.82),1,if(lt(t,1.18),1-(3*pow((t-0.82)/0.36,2)-2*pow((t-0.82)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z1];
[0:v]trim=start=4.48:end=15.74,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z2];
[0:v]trim=start=15.74:end=17.008,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.908),1,if(lt(t,1.268),1-(3*pow((t-0.908)/0.36,2)-2*pow((t-0.908)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.908),1,if(lt(t,1.268),1-(3*pow((t-0.908)/0.36,2)-2*pow((t-0.908)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z3];
[0:v]trim=start=17.008:end=20.516,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z4];
[0:v]trim=start=20.516:end=21.872,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.996),1,if(lt(t,1.356),1-(3*pow((t-0.996)/0.36,2)-2*pow((t-0.996)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.996),1,if(lt(t,1.356),1-(3*pow((t-0.996)/0.36,2)-2*pow((t-0.996)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z5];
[0:v]trim=start=21.872:end=26.323999999999998,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z6];
[0:v]trim=start=26.323999999999998:end=28.048,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.364),1,if(lt(t,1.724),1-(3*pow((t-1.364)/0.36,2)-2*pow((t-1.364)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.364),1,if(lt(t,1.724),1-(3*pow((t-1.364)/0.36,2)-2*pow((t-1.364)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z7];
[0:v]trim=start=28.048:end=35.32,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z8];
[z0][z1][z2][z3][z4][z5][z6][z7][z8]concat=n=9:v=1:a=0[base];
[2:v]scale=280:-1,format=rgba,loop=loop=-1:size=1,fps=25,setpts=N/25/TB[icraw];
[icraw]split=2[ic0][ic1];
[ic0]fade=t=in:st=23.828:d=0.32:alpha=1,fade=t=out:st=26.508:d=0.32:alpha=1[icf0];
[ic1]fade=t=in:st=33.684:d=0.32:alpha=1[icf1];
[base]ass=subs_n2010_2.ass[subbed];
[subbed][icf0]overlay=x=746:y=430:enable='between(t,23.828,26.828)':shortest=1[ovi0];
[ovi0][icf1]overlay=x=746:y=430:enable='between(t,33.684,35.32)':shortest=1[ov]
" -map "[ov]" -map 1:a -c:v libx264 -preset medium -crf 18 -r 25 -pix_fmt yuv420p -c:a copy "$OUT" -y

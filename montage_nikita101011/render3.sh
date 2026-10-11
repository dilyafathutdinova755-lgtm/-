set -e
FF=$1; OUT=$2
$FF -hide_banner -loglevel error -i "video3.mp4" -i a3.m4a -i /home/user/-/IMG_0884.png -filter_complex "
[0:v]trim=start=0.0:end=4.068,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z0];
[0:v]trim=start=4.068:end=5.328,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.9),1,if(lt(t,1.26),1-(3*pow((t-0.9)/0.36,2)-2*pow((t-0.9)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.9),1,if(lt(t,1.26),1-(3*pow((t-0.9)/0.36,2)-2*pow((t-0.9)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z1];
[0:v]trim=start=5.328:end=8.644,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z2];
[0:v]trim=start=8.644:end=10.575999999999999,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.572),1,if(lt(t,1.932),1-(3*pow((t-1.572)/0.36,2)-2*pow((t-1.572)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.572),1,if(lt(t,1.932),1-(3*pow((t-1.572)/0.36,2)-2*pow((t-1.572)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z3];
[0:v]trim=start=10.575999999999999:end=12.996,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z4];
[0:v]trim=start=12.996:end=14.799999999999999,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.444),1,if(lt(t,1.804),1-(3*pow((t-1.444)/0.36,2)-2*pow((t-1.444)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.444),1,if(lt(t,1.804),1-(3*pow((t-1.444)/0.36,2)-2*pow((t-1.444)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z5];
[0:v]trim=start=14.799999999999999:end=16.355999999999998,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z6];
[0:v]trim=start=16.355999999999998:end=17.936,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.22),1,if(lt(t,1.58),1-(3*pow((t-1.22)/0.36,2)-2*pow((t-1.22)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.22),1,if(lt(t,1.58),1-(3*pow((t-1.22)/0.36,2)-2*pow((t-1.22)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z7];
[0:v]trim=start=17.936:end=20.12,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z8];
[z0][z1][z2][z3][z4][z5][z6][z7][z8]concat=n=9:v=1:a=0[base];
[2:v]scale=280:-1,format=rgba,loop=loop=-1:size=1,fps=25,setpts=N/25/TB[icraw];
[icraw]split=2[ic0][ic1];
[ic0]fade=t=in:st=11.596:d=0.32:alpha=1,fade=t=out:st=14.276:d=0.32:alpha=1[icf0];
[ic1]fade=t=in:st=18.772:d=0.32:alpha=1[icf1];
[base]ass=subs_n101011_3.ass[subbed];
[subbed][icf0]overlay=x=746:y=430:enable='between(t,11.596,14.596)':shortest=1[ovi0];
[ovi0][icf1]overlay=x=746:y=430:enable='between(t,18.772,20.12)':shortest=1[ov]
" -map "[ov]" -map 1:a -c:v libx264 -preset medium -crf 18 -r 25 -pix_fmt yuv420p -c:a copy "$OUT" -y

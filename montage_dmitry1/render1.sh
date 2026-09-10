set -e
FF=$1; OUT=$2
$FF -hide_banner -loglevel error -i "Untitled.Video.1.10.09._2160p.mp4" -i a1.m4a -i /home/user/-/IMG_0884.png -filter_complex "
[0:v]trim=start=0.0:end=6.09,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z0];
[0:v]trim=start=6.09:end=7.33,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.88),1,if(lt(t,1.24),1-(3*pow((t-0.88)/0.36,2)-2*pow((t-0.88)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.88),1,if(lt(t,1.24),1-(3*pow((t-0.88)/0.36,2)-2*pow((t-0.88)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z1];
[0:v]trim=start=7.33:end=14.030000000000001,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z2];
[0:v]trim=start=14.030000000000001:end=15.26,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.87),1,if(lt(t,1.23),1-(3*pow((t-0.87)/0.36,2)-2*pow((t-0.87)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.87),1,if(lt(t,1.23),1-(3*pow((t-0.87)/0.36,2)-2*pow((t-0.87)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z3];
[0:v]trim=start=15.26:end=21.759999999999998,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z4];
[0:v]trim=start=21.759999999999998:end=22.88,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.76),1,if(lt(t,1.12),1-(3*pow((t-0.76)/0.36,2)-2*pow((t-0.76)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.76),1,if(lt(t,1.12),1-(3*pow((t-0.76)/0.36,2)-2*pow((t-0.76)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z5];
[0:v]trim=start=22.88:end=28.74,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z6];
[0:v]trim=start=28.74:end=30.13,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.03),1,if(lt(t,1.39),1-(3*pow((t-1.03)/0.36,2)-2*pow((t-1.03)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.03),1,if(lt(t,1.39),1-(3*pow((t-1.03)/0.36,2)-2*pow((t-1.03)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z7];
[0:v]trim=start=30.13:end=37.27,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z8];
[z0][z1][z2][z3][z4][z5][z6][z7][z8]concat=n=9:v=1:a=0[base];
[2:v]scale=280:-1,format=rgba,loop=loop=-1:size=1,fps=25,setpts=N/25/TB[icraw];
[icraw]split=2[ic0][ic1];
[ic0]fade=t=in:st=12.5:d=0.32:alpha=1,fade=t=out:st=15.18:d=0.32:alpha=1[icf0];
[ic1]fade=t=in:st=35.572:d=0.32:alpha=1[icf1];
[base]ass=subs_d1.ass[subbed];
[subbed][icf0]overlay=x=746:y=430:enable='between(t,12.5,15.5)':shortest=1[ovi0];
[ovi0][icf1]overlay=x=746:y=430:enable='between(t,35.572,37.27)':shortest=1[ov]
" -map "[ov]" -map 1:a -c:v libx264 -preset medium -crf 18 -r 25 -pix_fmt yuv420p -c:a copy "$OUT" -y

set -e
FF=$1; OUT=$2
$FF -hide_banner -loglevel error -i "Untitled.Video.15.09.1_2160p.mp4" -i a1.m4a -i /home/user/-/IMG_0884.png -filter_complex "
[0:v]trim=start=0.0:end=4.97,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z0];
[0:v]trim=start=4.97:end=6.67,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.34),1,if(lt(t,1.7),1-(3*pow((t-1.34)/0.36,2)-2*pow((t-1.34)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.34),1,if(lt(t,1.7),1-(3*pow((t-1.34)/0.36,2)-2*pow((t-1.34)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z1];
[0:v]trim=start=6.67:end=9.59,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z2];
[0:v]trim=start=9.59:end=11.53,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.58),1,if(lt(t,1.94),1-(3*pow((t-1.58)/0.36,2)-2*pow((t-1.58)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.58),1,if(lt(t,1.94),1-(3*pow((t-1.58)/0.36,2)-2*pow((t-1.58)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z3];
[0:v]trim=start=11.53:end=18.689999999999998,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z4];
[0:v]trim=start=18.689999999999998:end=21.07,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,2.02),1,if(lt(t,2.38),1-(3*pow((t-2.02)/0.36,2)-2*pow((t-2.02)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,2.02),1,if(lt(t,2.38),1-(3*pow((t-2.02)/0.36,2)-2*pow((t-2.02)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z5];
[0:v]trim=start=21.07:end=25.95,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z6];
[0:v]trim=start=25.95:end=27.97,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.66),1,if(lt(t,2.02),1-(3*pow((t-1.66)/0.36,2)-2*pow((t-1.66)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.66),1,if(lt(t,2.02),1-(3*pow((t-1.66)/0.36,2)-2*pow((t-1.66)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z7];
[0:v]trim=start=27.97:end=30.6,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z8];
[z0][z1][z2][z3][z4][z5][z6][z7][z8]concat=n=9:v=1:a=0[base];
[2:v]scale=280:-1,format=rgba,loop=loop=-1:size=1,fps=25,setpts=N/25/TB[icraw];
[icraw]split=2[ic0][ic1];
[ic0]fade=t=in:st=7.948:d=0.32:alpha=1,fade=t=out:st=10.628:d=0.32:alpha=1[icf0];
[ic1]fade=t=in:st=29.084:d=0.32:alpha=1[icf1];
[base]ass=subs_dm1.ass[subbed];
[subbed][icf0]overlay=x=746:y=430:enable='between(t,7.948,10.948)':shortest=1[ovi0];
[ovi0][icf1]overlay=x=746:y=430:enable='between(t,29.084,30.6)':shortest=1[ov]
" -map "[ov]" -map 1:a -c:v libx264 -preset medium -crf 18 -r 25 -pix_fmt yuv420p -c:a copy "$OUT" -y

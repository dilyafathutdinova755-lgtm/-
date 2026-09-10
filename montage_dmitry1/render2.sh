set -e
FF=$1; OUT=$2
$FF -hide_banner -loglevel error -i "Untitled.Video.2.10.09_2160p.mp4" -i a2.m4a -i /home/user/-/IMG_0884.png -filter_complex "
[0:v]trim=start=0.0:end=12.01,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z0];
[0:v]trim=start=12.01:end=13.149999999999999,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.78),1,if(lt(t,1.14),1-(3*pow((t-0.78)/0.36,2)-2*pow((t-0.78)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.78),1,if(lt(t,1.14),1-(3*pow((t-0.78)/0.36,2)-2*pow((t-0.78)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z1];
[0:v]trim=start=13.149999999999999:end=16.52,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z2];
[0:v]trim=start=16.52:end=17.68,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.8),1,if(lt(t,1.16),1-(3*pow((t-0.8)/0.36,2)-2*pow((t-0.8)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.8),1,if(lt(t,1.16),1-(3*pow((t-0.8)/0.36,2)-2*pow((t-0.8)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z3];
[0:v]trim=start=17.68:end=21.599999999999998,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z4];
[0:v]trim=start=21.599999999999998:end=22.72,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.76),1,if(lt(t,1.12),1-(3*pow((t-0.76)/0.36,2)-2*pow((t-0.76)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.76),1,if(lt(t,1.12),1-(3*pow((t-0.76)/0.36,2)-2*pow((t-0.76)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z5];
[0:v]trim=start=22.72:end=26.63,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z6];
[0:v]trim=start=26.63:end=27.91,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.92),1,if(lt(t,1.28),1-(3*pow((t-0.92)/0.36,2)-2*pow((t-0.92)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.92),1,if(lt(t,1.28),1-(3*pow((t-0.92)/0.36,2)-2*pow((t-0.92)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z7];
[0:v]trim=start=27.91:end=31.96,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z8];
[z0][z1][z2][z3][z4][z5][z6][z7][z8]concat=n=9:v=1:a=0[base];
[2:v]scale=280:-1,format=rgba,loop=loop=-1:size=1,fps=25,setpts=N/25/TB[icraw];
[icraw]split=3[ic0][ic1][ic2];
[ic0]fade=t=in:st=4.356:d=0.32:alpha=1,fade=t=out:st=7.036:d=0.32:alpha=1[icf0];
[ic1]fade=t=in:st=23.708:d=0.32:alpha=1,fade=t=out:st=26.388:d=0.32:alpha=1[icf1];
[ic2]fade=t=in:st=30.316:d=0.32:alpha=1[icf2];
[base]ass=subs_d2.ass[subbed];
[subbed][icf0]overlay=x=746:y=430:enable='between(t,4.356,7.356)':shortest=1[ovi0];
[ovi0][icf1]overlay=x=746:y=430:enable='between(t,23.708,26.708)':shortest=1[ovi1];
[ovi1][icf2]overlay=x=746:y=430:enable='between(t,30.316,31.96)':shortest=1[ov]
" -map "[ov]" -map 1:a -c:v libx264 -preset medium -crf 18 -r 25 -pix_fmt yuv420p -c:a copy "$OUT" -y

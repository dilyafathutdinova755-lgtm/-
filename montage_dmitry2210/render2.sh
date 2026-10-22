set -e
FF=$1; OUT=$2
$FF -hide_banner -loglevel error -i "video2.mp4" -i a2.m4a -i /home/user/-/IMG_0884.png -filter_complex "
[0:v]trim=start=0.0:end=2.0279999999999996,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z0];
[0:v]trim=start=2.0279999999999996:end=3.288,setpts=PTS-STARTPTS,crop=w='trunc((1080/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.9),1,if(lt(t,1.26),1-(3*pow((t-0.9)/0.36,2)-2*pow((t-0.9)/0.36,3)),1))))))/2)*2':h='trunc((1920/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.9),1,if(lt(t,1.26),1-(3*pow((t-0.9)/0.36,2)-2*pow((t-0.9)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z1];
[0:v]trim=start=3.288:end=9.204,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z2];
[0:v]trim=start=9.204:end=10.447999999999999,setpts=PTS-STARTPTS,crop=w='trunc((1080/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.884),1,if(lt(t,1.244),1-(3*pow((t-0.884)/0.36,2)-2*pow((t-0.884)/0.36,3)),1))))))/2)*2':h='trunc((1920/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.884),1,if(lt(t,1.244),1-(3*pow((t-0.884)/0.36,2)-2*pow((t-0.884)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z3];
[0:v]trim=start=10.447999999999999:end=13.98,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z4];
[0:v]trim=start=13.98:end=15.312,setpts=PTS-STARTPTS,crop=w='trunc((1080/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.972),1,if(lt(t,1.332),1-(3*pow((t-0.972)/0.36,2)-2*pow((t-0.972)/0.36,3)),1))))))/2)*2':h='trunc((1920/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.972),1,if(lt(t,1.332),1-(3*pow((t-0.972)/0.36,2)-2*pow((t-0.972)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z5];
[0:v]trim=start=15.312:end=19.74,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z6];
[0:v]trim=start=19.74:end=20.72,setpts=PTS-STARTPTS,crop=w='trunc((1080/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.62),1,if(lt(t,0.98),1-(3*pow((t-0.62)/0.36,2)-2*pow((t-0.62)/0.36,3)),1))))))/2)*2':h='trunc((1920/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.62),1,if(lt(t,0.98),1-(3*pow((t-0.62)/0.36,2)-2*pow((t-0.62)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z7];
[0:v]trim=start=20.72:end=22.84,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z8];
[z0][z1][z2][z3][z4][z5][z6][z7][z8]concat=n=9:v=1:a=0[base];
[2:v]scale=280:-1,format=rgba,loop=loop=-1:size=1,fps=25,setpts=N/25/TB[icraw];
[icraw]split=2[ic0][ic1];
[ic0]fade=t=in:st=15.668:d=0.32:alpha=1,fade=t=out:st=18.348:d=0.32:alpha=1[icf0];
[ic1]fade=t=in:st=21.108:d=0.32:alpha=1[icf1];
[base]ass=subs_d2210_2.ass[subbed];
[subbed][icf0]overlay=x=746:y=430:enable='between(t,15.668,18.668)':shortest=1[ovi0];
[ovi0][icf1]overlay=x=746:y=430:enable='between(t,21.108,22.84)':shortest=1[ov]
" -map "[ov]" -map 1:a -c:v libx264 -preset medium -crf 18 -r 25 -pix_fmt yuv420p -c:a copy "$OUT" -y

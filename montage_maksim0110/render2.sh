set -e
FF=$1; OUT=$2
$FF -hide_banner -loglevel error -i "video2.mp4" -i a2.m4a -i /home/user/-/IMG_0884.png -filter_complex "
[0:v]trim=start=0.0:end=5.747999999999999,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z0];
[0:v]trim=start=5.747999999999999:end=8.431999999999999,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,2.324),1,if(lt(t,2.684),1-(3*pow((t-2.324)/0.36,2)-2*pow((t-2.324)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,2.324),1,if(lt(t,2.684),1-(3*pow((t-2.324)/0.36,2)-2*pow((t-2.324)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z1];
[0:v]trim=start=8.431999999999999:end=12.788,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z2];
[0:v]trim=start=12.788:end=14.767999999999999,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.62),1,if(lt(t,1.98),1-(3*pow((t-1.62)/0.36,2)-2*pow((t-1.62)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.62),1,if(lt(t,1.98),1-(3*pow((t-1.62)/0.36,2)-2*pow((t-1.62)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z3];
[0:v]trim=start=14.767999999999999:end=20.163999999999998,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z4];
[0:v]trim=start=20.163999999999998:end=21.144,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.62),1,if(lt(t,0.98),1-(3*pow((t-0.62)/0.36,2)-2*pow((t-0.62)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.62),1,if(lt(t,0.98),1-(3*pow((t-0.62)/0.36,2)-2*pow((t-0.62)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z5];
[0:v]trim=start=21.144:end=25.572,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z6];
[0:v]trim=start=25.572:end=26.471999999999998,setpts=PTS-STARTPTS,crop=w='trunc((2160/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.54),1,if(lt(t,0.9),1-(3*pow((t-0.54)/0.36,2)-2*pow((t-0.54)/0.36,3)),1))))))/2)*2':h='trunc((3840/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,0.54),1,if(lt(t,0.9),1-(3*pow((t-0.54)/0.36,2)-2*pow((t-0.54)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z7];
[0:v]trim=start=26.471999999999998:end=27.97,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z8];
[z0][z1][z2][z3][z4][z5][z6][z7][z8]concat=n=9:v=1:a=0[base];
[2:v]scale=280:-1,format=rgba,loop=loop=-1:size=1,fps=25,setpts=N/25/TB[icraw];
[icraw]split=2[ic0][ic1];
[ic0]fade=t=in:st=17.324:d=0.32:alpha=1,fade=t=out:st=20.004:d=0.32:alpha=1[icf0];
[ic1]fade=t=in:st=26.292:d=0.32:alpha=1[icf1];
[base]ass=subs_m0110_2.ass[subbed];
[subbed][icf0]overlay=x=746:y=430:enable='between(t,17.324,20.324)':shortest=1[ovi0];
[ovi0][icf1]overlay=x=746:y=430:enable='between(t,26.292,27.97)':shortest=1[ov]
" -map "[ov]" -map 1:a -c:v libx264 -preset medium -crf 18 -r 25 -pix_fmt yuv420p -c:a copy "$OUT" -y

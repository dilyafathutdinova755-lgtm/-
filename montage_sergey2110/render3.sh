set -e
FF=$1; OUT=$2
$FF -hide_banner -loglevel error -i "video3.mp4" -i a3.m4a -i /home/user/-/IMG_0884.png -filter_complex "
[0:v]trim=start=0.0:end=0.9079999999999999,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z0];
[0:v]trim=start=0.9079999999999999:end=2.6879999999999997,setpts=PTS-STARTPTS,crop=w='trunc((1080/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.42),1,if(lt(t,1.78),1-(3*pow((t-1.42)/0.36,2)-2*pow((t-1.42)/0.36,3)),1))))))/2)*2':h='trunc((1920/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.42),1,if(lt(t,1.78),1-(3*pow((t-1.42)/0.36,2)-2*pow((t-1.42)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z1];
[0:v]trim=start=2.6879999999999997:end=9.036000000000001,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z2];
[0:v]trim=start=9.036000000000001:end=10.767999999999999,setpts=PTS-STARTPTS,crop=w='trunc((1080/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.372),1,if(lt(t,1.732),1-(3*pow((t-1.372)/0.36,2)-2*pow((t-1.372)/0.36,3)),1))))))/2)*2':h='trunc((1920/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.372),1,if(lt(t,1.732),1-(3*pow((t-1.372)/0.36,2)-2*pow((t-1.372)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z3];
[0:v]trim=start=10.767999999999999:end=11.932,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z4];
[0:v]trim=start=11.932:end=13.616,setpts=PTS-STARTPTS,crop=w='trunc((1080/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.324),1,if(lt(t,1.684),1-(3*pow((t-1.324)/0.36,2)-2*pow((t-1.324)/0.36,3)),1))))))/2)*2':h='trunc((1920/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.324),1,if(lt(t,1.684),1-(3*pow((t-1.324)/0.36,2)-2*pow((t-1.324)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z5];
[0:v]trim=start=13.616:end=17.932,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z6];
[0:v]trim=start=17.932:end=20.176,setpts=PTS-STARTPTS,crop=w='trunc((1080/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.884),1,if(lt(t,2.244),1-(3*pow((t-1.884)/0.36,2)-2*pow((t-1.884)/0.36,3)),1))))))/2)*2':h='trunc((1920/(1+0.1399999999999999*(if(lt(t,0.28),(3*pow(t/0.28,2)-2*pow(t/0.28,3)),if(lt(t,1.884),1,if(lt(t,2.244),1-(3*pow((t-1.884)/0.36,2)-2*pow((t-1.884)/0.36,3)),1))))))/2)*2':x='(in_w-ow)/2':y='(in_h-oh)/2',scale=1080:1920:flags=lanczos,setsar=1[z7];
[0:v]trim=start=20.176:end=22.444,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[z8];
[z0][z1][z2][z3][z4][z5][z6][z7][z8]concat=n=9:v=1:a=0[base];
[2:v]scale=280:-1,format=rgba,loop=loop=-1:size=1,fps=25,setpts=N/25/TB[icraw];
[icraw]split=2[ic0][ic1];
[ic0]fade=t=in:st=14.036:d=0.32:alpha=1,fade=t=out:st=16.716:d=0.32:alpha=1[icf0];
[ic1]fade=t=in:st=20.756:d=0.32:alpha=1[icf1];
[base]ass=subs_s2110_3.ass[subbed];
[subbed][icf0]overlay=x=746:y=430:enable='between(t,14.036,17.036)':shortest=1[ovi0];
[ovi0][icf1]overlay=x=746:y=430:enable='between(t,20.756,22.444)':shortest=1[ov]
" -map "[ov]" -map 1:a -c:v libx264 -preset medium -crf 18 -r 25 -pix_fmt yuv420p -c:a copy "$OUT" -y

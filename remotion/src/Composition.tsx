import { AbsoluteFill, Audio, CalculateMetadataFunction, Composition, staticFile } from "remotion";
import segmentsData from "./data/segments.json";
import { ensureFontsLoaded } from "./fonts";
import { VideoBackground } from "./VideoBackground";
import { KeyCard } from "./KeyCard";
import { RunningCaption } from "./RunningCaption";
import { AppIcon } from "./AppIcon";

const FPS = 25;
const WIDTH = 1080;
const HEIGHT = 1920;

type Props = Record<string, unknown>;

const calculateMetadata: CalculateMetadataFunction<Props> = async () => {
  await ensureFontsLoaded();
  return {
    durationInFrames: Math.round(segmentsData.total_duration * FPS),
    fps: FPS,
    width: WIDTH,
    height: HEIGHT,
  };
};

export const MyComposition = () => {
  return (
    <Composition
      id="EgeOlimpiada"
      component={EgeVideo}
      durationInFrames={Math.round(segmentsData.total_duration * FPS)}
      fps={FPS}
      width={WIDTH}
      height={HEIGHT}
      calculateMetadata={calculateMetadata}
    />
  );
};

export const EgeVideo: React.FC<Props> = () => {
  return (
    <AbsoluteFill>
      <VideoBackground />
      <Audio src={staticFile("audio.wav")} />
      <KeyCard />
      <RunningCaption />
      <AppIcon />
    </AbsoluteFill>
  );
};

import { AbsoluteFill, Sequence, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import captionData from "./data/running_caption.json";
import { CAPTION_SIZE, CAPTION_TOP, SIDE_MARGIN, WHITE } from "./brand";
import { CAPTION_FONT } from "./fonts";

const FADE_FRAMES = 2; // ~80ms @ 25fps, just enough to avoid a hard flicker between words

const Word: React.FC<{ text: string; durationInFrames: number }> = ({ text, durationInFrames }) => {
  const frame = useCurrentFrame();
  // Two independent fades (rather than one 4-keyframe interpolate) so a very
  // short group (e.g. the last word, cut off by the clip's end) can't collapse
  // the keyframes out of strictly-increasing order.
  const fadeIn = interpolate(frame, [0, Math.min(FADE_FRAMES, durationInFrames)], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const fadeOut = interpolate(
    frame,
    [Math.max(0, durationInFrames - FADE_FRAMES), durationInFrames],
    [1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  );
  const opacity = Math.min(fadeIn, fadeOut);

  return (
    <AbsoluteFill
      style={{
        justifyContent: "flex-start",
        alignItems: "center",
        top: CAPTION_TOP,
        height: CAPTION_SIZE * 1.6,
        left: SIDE_MARGIN,
        right: SIDE_MARGIN,
      }}
    >
      <span
        style={{
          opacity,
          fontFamily: CAPTION_FONT,
          fontSize: CAPTION_SIZE,
          color: WHITE,
          textShadow: "0 2px 8px rgba(0,0,0,0.55)",
        }}
      >
        {text}
      </span>
    </AbsoluteFill>
  );
};

export const RunningCaption: React.FC = () => {
  const { fps } = useVideoConfig();

  return (
    <>
      {captionData.map((group, i) => {
        const from = Math.round(group.start * fps);
        const to = Math.round(group.end * fps);
        const durationInFrames = Math.max(1, to - from);
        return (
          <Sequence key={i} name={`cap-${i}`} from={from} durationInFrames={durationInFrames} layout="none">
            <Word text={group.text} durationInFrames={durationInFrames} />
          </Sequence>
        );
      })}
    </>
  );
};

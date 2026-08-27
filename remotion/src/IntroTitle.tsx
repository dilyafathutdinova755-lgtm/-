import { AbsoluteFill, Easing, Sequence, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import introData from "./data/intro.json";
import {
  ACCENT,
  INTRO_BAND_BOTTOM,
  INTRO_BAND_TOP,
  INTRO_LINE_HEIGHT,
  INTRO_SIZE,
  SIDE_MARGIN,
} from "./brand";
import { CARD_FONT } from "./fonts";

// CLAUDE.md §1.4a: the opening beat is a pain-point hook headline, not the
// usual two-tone KeyCard. Fully accent-colored, holds just past the hook line,
// then the normal KeyCard/running-caption cadence takes over.
const SCALE_IN_FRAMES = 8;
const OPACITY_IN_FRAMES = 4;
const OPACITY_OUT_FRAMES = 2;

const IntroCard: React.FC<{ lines: string[]; durationInFrames: number }> = ({ lines, durationInFrames }) => {
  const frame = useCurrentFrame();

  const scale = interpolate(frame, [0, SCALE_IN_FRAMES * 0.75, SCALE_IN_FRAMES], [0.94, 1.01, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.quad),
    output: "perceptual-scale",
  });

  const fadeIn = interpolate(frame, [0, Math.min(OPACITY_IN_FRAMES, durationInFrames)], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const fadeOut = interpolate(
    frame,
    [Math.max(0, durationInFrames - OPACITY_OUT_FRAMES), durationInFrames],
    [1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  );
  const opacity = Math.min(fadeIn, fadeOut);

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        top: INTRO_BAND_TOP,
        height: INTRO_BAND_BOTTOM - INTRO_BAND_TOP,
        left: SIDE_MARGIN,
        right: SIDE_MARGIN,
        width: "auto",
      }}
    >
      <div
        style={{
          transform: `scale(${scale})`,
          opacity,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          fontFamily: CARD_FONT,
          textTransform: "uppercase",
          textAlign: "center",
          textShadow: "0 3px 14px rgba(0,0,0,0.55)",
        }}
      >
        {lines.map((line, i) => (
          <span
            key={i}
            style={{
              fontSize: INTRO_SIZE,
              lineHeight: `${INTRO_SIZE * INTRO_LINE_HEIGHT}px`,
              color: ACCENT,
              WebkitTextStroke: `3px ${ACCENT}`,
              paintOrder: "stroke fill",
            }}
          >
            {line}
          </span>
        ))}
      </div>
    </AbsoluteFill>
  );
};

export const IntroTitle: React.FC = () => {
  const { fps } = useVideoConfig();
  const durationInFrames = Math.max(1, Math.round(introData.end * fps));

  return (
    <Sequence name="intro-hook" from={0} durationInFrames={durationInFrames} layout="none">
      <IntroCard lines={introData.lines} durationInFrames={durationInFrames} />
    </Sequence>
  );
};

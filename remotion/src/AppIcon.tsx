import { AbsoluteFill, Img, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import cardsData from "./data/cards.json";
import segmentsData from "./data/segments.json";
import { ICON_RIGHT_MARGIN, ICON_SIZE, ICON_TOP } from "./brand";

// The app-mention card ("ЕГЭ ТРЕНАЖЁР") is the second-to-last card.
// Icon start is offset 250ms after that card starts (CLAUDE.md §1.6).
const appCard = cardsData[cardsData.length - 2];
const ICON_START_SECONDS = appCard.start + 0.25;
const FADE_FRAMES = 8; // ~320ms @ 25fps

const IconFade: React.FC = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, FADE_FRAMES], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill>
      <Img
        src={staticFile("app-icon.png")}
        style={{
          position: "absolute",
          top: ICON_TOP,
          right: ICON_RIGHT_MARGIN,
          width: ICON_SIZE,
          height: "auto",
          opacity,
        }}
      />
    </AbsoluteFill>
  );
};

export const AppIcon: React.FC = () => {
  const { fps } = useVideoConfig();
  const from = Math.round(ICON_START_SECONDS * fps);
  const end = Math.round(segmentsData.total_duration * fps);
  const durationInFrames = Math.max(1, end - from);

  return (
    <Sequence name="app-icon" from={from} durationInFrames={durationInFrames} layout="none">
      <IconFade />
    </Sequence>
  );
};

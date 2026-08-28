import {
  AbsoluteFill,
  Easing,
  Sequence,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import cardsData from "./data/cards.json";
import {
  ACCENT,
  CARD_ACCENT_SIZE_BOOST,
  CARD_ACCENT_STROKE,
  CARD_BAND_BOTTOM,
  CARD_BAND_TOP,
  CARD_BIG_SIZE,
  CARD_LINE_HEIGHT,
  CARD_SMALL_SIZE,
  SIDE_MARGIN,
  WHITE,
} from "./brand";
import { CARD_FONT } from "./fonts";

type CardLine = { text: string; accent: boolean; size: "big" | "small" };

const SCALE_IN_FRAMES = 8; // 320ms @ 25fps
const OPACITY_IN_FRAMES = 4; // ~140ms @ 25fps (rounds to 3.5 -> 4)
const OPACITY_OUT_FRAMES = 2; // ~90ms @ 25fps

// CLAUDE.md §1.9: the card's position never changes, even during a stock
// cutaway — the user tried a top-band override for that case and reversed it.
const SingleCard: React.FC<{ lines: CardLine[]; durationInFrames: number }> = ({
  lines,
  durationInFrames,
}) => {
  const frame = useCurrentFrame();

  const scale = interpolate(frame, [0, SCALE_IN_FRAMES * 0.75, SCALE_IN_FRAMES], [0.94, 1.01, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.quad),
    output: "perceptual-scale",
  });

  // Two independent fades, so a short card can't collapse the keyframes
  // out of strictly-increasing order (see RunningCaption.tsx for the same fix).
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
        top: CARD_BAND_TOP,
        height: CARD_BAND_BOTTOM - CARD_BAND_TOP,
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
        {lines.map((line, i) => {
          const baseSize = line.size === "big" ? CARD_BIG_SIZE : CARD_SMALL_SIZE;
          // Accent (blue) lines run bigger and carry a same-color stroke to
          // fatten the glyphs — CLAUDE.md §1.4: the blue line should read as
          // visibly heavier than the white one, not just a different color.
          const fontSize = line.accent ? baseSize * CARD_ACCENT_SIZE_BOOST : baseSize;
          return (
            <span
              key={i}
              style={{
                fontSize,
                lineHeight: `${fontSize * CARD_LINE_HEIGHT}px`,
                color: line.accent ? ACCENT : WHITE,
                WebkitTextStroke: line.accent
                  ? `${CARD_ACCENT_STROKE}px ${ACCENT}`
                  : "3px rgba(0,0,0,0.65)",
                paintOrder: "stroke fill",
              }}
            >
              {line.text}
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

export const KeyCard: React.FC = () => {
  const { fps } = useVideoConfig();

  return (
    <>
      {cardsData.map((card, i) => {
        const from = Math.round(card.start * fps);
        const to = Math.round(card.end * fps);
        const durationInFrames = Math.max(1, to - from);
        return (
          <Sequence
            key={i}
            name={`card-${i}`}
            from={from}
            durationInFrames={durationInFrames}
            layout="none"
          >
            <SingleCard lines={card.lines as CardLine[]} durationInFrames={durationInFrames} />
          </Sequence>
        );
      })}
    </>
  );
};

import { AbsoluteFill, Img, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import wordsData from "./data/words.json";
import durationData from "./data/duration.json";
import { ICON_RIGHT_MARGIN, ICON_SIZE, ICON_TOP } from "./brand";

// CLAUDE.md §1.6: the icon comes up on every mention of the product, not just
// once at the end. Each mention gets a window that holds ~3s past the word;
// windows closer together than MERGE_GAP are merged into one continuous
// appearance instead of flickering off and back on.
const MENTION_REGEX = /тренаж/i;
const PRE_ROLL = 0.15;
const HOLD_AFTER = 3.0;
const MERGE_GAP = 1.5;

type Word = { text: string; start: number; end: number };
type Window = { start: number; end: number };

const buildIconWindows = (words: Word[], totalDuration: number): Window[] => {
  const raw: Window[] = words
    .filter((w) => MENTION_REGEX.test(w.text))
    .map((w) => ({
      start: Math.max(0, w.start - PRE_ROLL),
      end: Math.min(totalDuration, w.end + HOLD_AFTER),
    }));

  const merged: Window[] = [];
  for (const w of raw) {
    const last = merged[merged.length - 1];
    if (last && w.start - last.end <= MERGE_GAP) {
      last.end = Math.max(last.end, w.end);
    } else {
      merged.push({ ...w });
    }
  }
  return merged;
};

const FADE_FRAMES = 8; // ~320ms @ 25fps

const IconFade: React.FC<{ durationInFrames: number }> = ({ durationInFrames }) => {
  const frame = useCurrentFrame();
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
  const windows = buildIconWindows(wordsData as Word[], durationData.total_duration);

  return (
    <>
      {windows.map((w, i) => {
        const from = Math.round(w.start * fps);
        const to = Math.round(w.end * fps);
        const durationInFrames = Math.max(1, to - from);
        return (
          <Sequence key={i} name={`app-icon-${i}`} from={from} durationInFrames={durationInFrames} layout="none">
            <IconFade durationInFrames={durationInFrames} />
          </Sequence>
        );
      })}
    </>
  );
};

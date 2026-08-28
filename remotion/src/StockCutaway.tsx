import { Video } from "@remotion/media";
import { AbsoluteFill, Sequence, staticFile, useVideoConfig } from "remotion";
import stockData from "./data/stock_cutaways.json";

// CLAUDE.md §1.9: brief cutaways to stock "student studying" footage on a
// phrase, to hold attention on slower beats. This renders on top of
// VideoBackground and simply covers it for the window — the host's clip
// underneath keeps playing in sync with the master timeline the whole time
// (Video is always seeked to the current frame), so when the cutaway ends
// the host's footage is exactly where it should be. Never touches audio:
// the narrator's track is a separate <Audio> in Composition.tsx, and the
// stock clip itself is always muted.
type Cutaway = { start: number; end: number; file: string; sourceStart?: number };

export const StockCutaway: React.FC = () => {
  const { fps } = useVideoConfig();
  const cutaways = stockData as Cutaway[];

  return (
    <>
      {cutaways.map((c, i) => {
        const from = Math.round(c.start * fps);
        const durationInFrames = Math.max(1, Math.round((c.end - c.start) * fps));
        const trimBefore = Math.round((c.sourceStart ?? 0) * fps);
        return (
          <Sequence key={i} name={`stock-${i}`} from={from} durationInFrames={durationInFrames} layout="none">
            <AbsoluteFill style={{ backgroundColor: "#000000" }}>
              <Video
                src={staticFile(c.file)}
                muted
                trimBefore={trimBefore}
                objectFit="cover"
                style={{ width: "100%", height: "100%" }}
              />
            </AbsoluteFill>
          </Sequence>
        );
      })}
    </>
  );
};

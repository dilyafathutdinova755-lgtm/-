import { Video } from "@remotion/media";
import { AbsoluteFill, Sequence, staticFile, useVideoConfig } from "remotion";
import segmentsData from "./data/segments.json";

export const VideoBackground: React.FC = () => {
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{ backgroundColor: "#000000" }}>
      {segmentsData.segments.map((seg, i) => {
        const from = Math.round(seg.new_start * fps);
        const to = Math.round(seg.new_end * fps);
        const durationInFrames = Math.max(1, to - from);
        const trimBefore = Math.round(seg.old_start * fps);
        const trimAfter = Math.round(seg.old_end * fps);

        return (
          <Sequence
            key={i}
            name={`take-${i}`}
            from={from}
            durationInFrames={durationInFrames}
            layout="none"
          >
            <AbsoluteFill style={{ overflow: "hidden" }}>
              <Video
                src={staticFile("source.mp4")}
                trimBefore={trimBefore}
                trimAfter={trimAfter}
                muted
                objectFit="cover"
                style={{
                  width: "100%",
                  height: "100%",
                  transform: `scale(${seg.zoom})`,
                }}
              />
            </AbsoluteFill>
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};

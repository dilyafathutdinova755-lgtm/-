import { Video } from "@remotion/media";
import { AbsoluteFill, staticFile } from "remotion";

// Static, uncut footage — no jump cuts, no punch-in zoom. Only the
// caption layers and the app icon are composited on top (see Composition.tsx).
export const VideoBackground: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#000000" }}>
      <Video src={staticFile("source.mp4")} muted objectFit="cover" style={{ width: "100%", height: "100%" }} />
    </AbsoluteFill>
  );
};

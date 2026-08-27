import { Video } from "@remotion/media";
import { AbsoluteFill, Easing, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import emphasisData from "./data/emphasis.json";
import { EMPHASIS_ATTACK_FRAMES, EMPHASIS_RELEASE_FRAMES, EMPHASIS_ZOOM_SCALE } from "./brand";

// Static, uncut footage — no jump cuts, no trimming. The only motion on this
// layer is a smooth punch-in/punch-out zoom over a handful of hand-marked
// "emphasis" phrases (see CLAUDE.md §2.2 / data/emphasis.json) — a transform,
// never a cut. Caption layers and the app icon are composited on top in
// Composition.tsx.
type EmphasisWindow = { start: number; end: number };

const buildScaleKeyframes = (windows: EmphasisWindow[], fps: number) => {
  const frames: number[] = [];
  const scales: number[] = [];
  let cursor = -1;

  for (const w of windows) {
    const peakStart = Math.round(w.start * fps);
    const peakEnd = Math.round(w.end * fps);
    const attackStart = Math.max(cursor + 1, peakStart - EMPHASIS_ATTACK_FRAMES);
    const releaseEnd = Math.max(peakEnd + 1, peakEnd + EMPHASIS_RELEASE_FRAMES);

    // Keep keyframes strictly increasing even if two emphasis windows are
    // authored close together — clamp the attack against the previous release.
    const safeAttackStart = Math.max(attackStart, cursor + 1);
    const safePeakStart = Math.max(peakStart, safeAttackStart + 1);
    const safePeakEnd = Math.max(peakEnd, safePeakStart + 1);
    const safeReleaseEnd = Math.max(releaseEnd, safePeakEnd + 1);

    frames.push(safeAttackStart, safePeakStart, safePeakEnd, safeReleaseEnd);
    scales.push(1, EMPHASIS_ZOOM_SCALE, EMPHASIS_ZOOM_SCALE, 1);
    cursor = safeReleaseEnd;
  }

  return { frames, scales };
};

const ZoomedVideo: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const { frames, scales } = buildScaleKeyframes(emphasisData as EmphasisWindow[], fps);

  const scale =
    frames.length === 0
      ? 1
      : interpolate(frame, frames, scales, {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
          easing: Easing.inOut(Easing.quad),
        });

  return (
    <AbsoluteFill style={{ backgroundColor: "#000000" }}>
      <Video
        src={staticFile("source.mp4")}
        muted
        objectFit="cover"
        style={{ width: "100%", height: "100%", transform: `scale(${scale})` }}
      />
    </AbsoluteFill>
  );
};

export const VideoBackground: React.FC = () => {
  return <ZoomedVideo />;
};

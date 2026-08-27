// Brand constants — see CLAUDE.md §1 (Brand Kit). Cold set: ice-blue accent.
export const ACCENT = "#C9F5FF";
export const WHITE = "#FFFFFF";

// Safe zones at 1080x1920 master (CLAUDE.md §4.4)
export const SIDE_MARGIN = 80; // >=70px required
export const TOP_UNSAFE = 180; // platform icon zone
export const BOTTOM_UNSAFE = 420; // platform UI zone

// Key-card layer (CLAUDE.md §1.4)
export const CARD_BAND_TOP = 1920 * 0.55;
export const CARD_BAND_BOTTOM = 1920 * 0.75;
export const CARD_BIG_SIZE = 108; // 90-120px range
export const CARD_SMALL_SIZE = 52; // 44-64px range
export const CARD_LINE_HEIGHT = 0.9;

// Running caption layer (CLAUDE.md §1.4)
export const CAPTION_SIZE = 42;
export const CAPTION_TOP = 230; // just below the 180px platform-icon zone

// App icon (CLAUDE.md §1.6)
export const ICON_SIZE = 280; // 260-300px range
export const ICON_RIGHT_MARGIN = 60; // >=54px action-safe
export const ICON_TOP = 380; // head height, outside top 180px zone

// Accent (blue) line weight boost within KeyCard — CLAUDE.md §1.4
export const CARD_ACCENT_SIZE_BOOST = 1.1;
export const CARD_ACCENT_STROKE = 3; // px, same-color stroke fattens the glyph

// Emphasis punch-zoom on VideoBackground — CLAUDE.md §2.2
export const EMPHASIS_ZOOM_SCALE = 1.14;
export const EMPHASIS_ATTACK_FRAMES = 7; // ~280ms @ 25fps, "sharp but smooth"
export const EMPHASIS_RELEASE_FRAMES = 9; // ~360ms @ 25fps, slightly softer on the way out

// Intro hook headline — CLAUDE.md §1.4a
export const INTRO_BAND_TOP = 1920 * 0.42;
export const INTRO_BAND_BOTTOM = 1920 * 0.62;
export const INTRO_SIZE = 96;
export const INTRO_LINE_HEIGHT = 0.95;

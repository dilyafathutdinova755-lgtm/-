import { loadFont } from "@remotion/fonts";
import { staticFile } from "remotion";

export const CARD_FONT = "Golos Text Black";
// Deliberately a different, narrower family from CARD_FONT — see CLAUDE.md §1.4:
// the running caption must read as visibly smaller than the card at the same font size.
export const CAPTION_FONT = "PT Sans Narrow Bold";

let fontsLoaded: Promise<unknown> | null = null;

export const ensureFontsLoaded = () => {
  if (!fontsLoaded) {
    fontsLoaded = Promise.all([
      loadFont({
        family: CARD_FONT,
        url: staticFile("GolosText-Black.ttf"),
        weight: "900",
      }),
      loadFont({
        family: CAPTION_FONT,
        url: staticFile("PTSansNarrow-Bold.ttf"),
        weight: "700",
      }),
    ]);
  }
  return fontsLoaded;
};

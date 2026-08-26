import { loadFont } from "@remotion/fonts";
import { staticFile } from "remotion";

export const CARD_FONT = "Golos Text Black";
export const CAPTION_FONT = "Manrope SemiBold";

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
        url: staticFile("Manrope-SemiBold.ttf"),
        weight: "600",
      }),
    ]);
  }
  return fontsLoaded;
};

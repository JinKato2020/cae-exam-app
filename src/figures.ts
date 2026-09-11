// 問題の図解（実画像）。キー → 画像。
// ※React Native(Metro) は動的パス不可なので、ここで静的に require して束ねる。
// 画像は assets/figures/ に置く（Pillowで生成した白地のPNG）。
import type { ImageSourcePropType } from 'react-native';

export const FIGURES: Record<string, ImageSourcePropType> = {
  det2x2: require('../assets/figures/det2x2.png'),
  norm: require('../assets/figures/norm.png'),
  fwddiff: require('../assets/figures/fwddiff.png'),
  centraldiff: require('../assets/figures/centraldiff.png'),
  secondderiv: require('../assets/figures/2ndderiv.png'),
};

// 図の縦横比（全図とも 660x420 で生成）
export const FIGURE_ASPECT = 660 / 420;

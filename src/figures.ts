// 問題の図解（実画像）。キー → 画像。
// ※React Native(Metro) は動的パス不可なので、ここで静的に require して束ねる。
// 画像は assets/figures/ に置く（Pillowで生成した白地のPNG・660x420）。
import type { ImageSourcePropType } from 'react-native';

export const FIGURES: Record<string, ImageSourcePropType> = {
  // 第1章 数学の基礎
  det2x2: require('../assets/figures/det2x2.png'),
  norm: require('../assets/figures/norm.png'),
  fwddiff: require('../assets/figures/fwddiff.png'),
  centraldiff: require('../assets/figures/centraldiff.png'),
  secondderiv: require('../assets/figures/2ndderiv.png'),
  // 第2章 固体力学の基礎
  solidbar: require('../assets/figures/solidbar.png'),
  solidbeam: require('../assets/figures/solidbeam.png'),
  solidsection: require('../assets/figures/solidsection.png'),
  solidthermal: require('../assets/figures/solidthermal.png'),
  solidconc: require('../assets/figures/solidconc.png'),
  // 第3章 熱伝導の基礎
  heatdist: require('../assets/figures/heatdist.png'),
  heatresist: require('../assets/figures/heatresist.png'),
  // 第4章 有限要素法の定式化
  femshape: require('../assets/figures/femshape.png'),
  fembar: require('../assets/figures/fembar.png'),
  femsprings: require('../assets/figures/femsprings.png'),
  femtruss: require('../assets/figures/femtruss.png'),
};

// 図の縦横比（全図とも 660x420 で生成）
export const FIGURE_ASPECT = 660 / 420;

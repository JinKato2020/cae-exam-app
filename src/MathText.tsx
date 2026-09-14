// 数式つきテキストの表示。
// 問題文・選択肢・解説の中の $...$ を KaTeX で数式として描画する。
// React Native には「文章の途中に数式」を混ぜる仕組みが無いので、
// 数式を含むブロックだけ WebView(KaTeX)で1枚描画し、高さは中身に合わせて自動調整する。
// ※ $ を含まないテキストは軽い <Text> で描画（WebView を無駄に増やさない）。
import { useState } from 'react';
import { Platform, Text, View, type StyleProp, type TextStyle } from 'react-native';
import { WebView } from 'react-native-webview';

const KATEX = '0.16.9';
const CDN = `https://cdnjs.cloudflare.com/ajax/libs/KaTeX/${KATEX}`;

// $...$（インライン）と $$...$$（ブロック）を含む1ブロックの HTML を作る。
function buildHtml(text: string, color: string, fontSize: number, bold: boolean) {
  const payload = JSON.stringify(text); // 本文はJSで textContent に入れる（HTML注入を避け、\ や $ をそのまま保持）
  return `<!DOCTYPE html><html><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
<link rel="stylesheet" href="${CDN}/katex.min.css">
<script src="${CDN}/katex.min.js"></script>
<script src="${CDN}/contrib/auto-render.min.js"></script>
<style>
  html,body{margin:0;padding:0;background:transparent;}
  /* 子要素(表示数式など)の上下marginが body に相殺で抜けて高さが縮む→縦に切れる、を防ぐ */
  body{display:flow-root;}
  #c{color:${color};font-size:${fontSize}px;line-height:1.75;font-weight:${bold ? '600' : '400'};
     font-family:-apple-system,'Hiragino Kaku Gothic ProN','Noto Sans JP',Roboto,sans-serif;
     white-space:pre-wrap;word-wrap:break-word;overflow-wrap:break-word;padding:2px 0;overflow:visible;}
  .katex{font-size:1.05em;}
  /* 表示数式は縦を絶対に切らない。横に溢れる長い式だけ横スクロールにする */
  .katex-display{margin:.35em 0;overflow-x:auto;overflow-y:visible;}
</style></head><body>
<div id="c"></div>
<script>
  document.getElementById('c').textContent = ${payload};
  function post(){
    var el = document.getElementById('c');
    var h = Math.ceil(Math.max(
      el.scrollHeight, el.getBoundingClientRect().height,
      document.body.scrollHeight, document.documentElement.scrollHeight
    ));
    if (h && window.ReactNativeWebView) window.ReactNativeWebView.postMessage(String(h));
  }
  function run(){
    try {
      renderMathInElement(document.getElementById('c'), {
        delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}],
        throwOnError:false
      });
    } catch(e) {}
    post();
    // KaTeXフォントはCDNから遅延読込。読み込み完了・複数タイミングで高さを取り直す
    [120,300,600,1200].forEach(function(ms){ setTimeout(post, ms); });
    if (document.fonts && document.fonts.ready) { document.fonts.ready.then(post).catch(function(){}); }
  }
  if (document.readyState === 'complete') run(); else window.addEventListener('load', run);
</script></body></html>`;
}

export function MathText(props: { text: string; color: string; fontSize?: number; bold?: boolean }) {
  const fontSize = props.fontSize ?? 16;
  const [height, setHeight] = useState(Math.round(fontSize * 1.75));
  return (
    <WebView
      originWhitelist={['*']}
      source={{ html: buildHtml(props.text, props.color, fontSize, props.bold ?? false) }}
      style={{ height, backgroundColor: 'transparent', width: '100%' }}
      scrollEnabled={false}
      showsVerticalScrollIndicator={false}
      onMessage={(e) => {
        const h = Number(e.nativeEvent.data);
        if (h && Math.abs(h - height) > 1) setHeight(h);
      }}
      // Android で背景を透過させるための指定
      androidLayerType="software"
      opaque={Platform.OS !== 'android'}
      // タップは親（選択肢の Pressable など）に通す
      pointerEvents="none"
    />
  );
}

// $ を含まなければ軽い <Text>、含めば MathText を使う共通コンポーネント。
export function RichText(props: {
  text: string;
  color: string;
  fontSize?: number;
  bold?: boolean;
  style?: StyleProp<TextStyle>;
}) {
  const hasMath = props.text.includes('$');
  if (!hasMath) {
    return (
      <Text
        style={[
          { color: props.color, fontSize: props.fontSize ?? 16, lineHeight: (props.fontSize ?? 16) * 1.4 },
          props.bold ? { fontWeight: '600' } : null,
          props.style,
        ]}
      >
        {props.text}
      </Text>
    );
  }
  // WebView は pointerEvents:none にしているので、選択肢内でもタップが親に通る。
  return (
    <View style={{ width: '100%' }}>
      <MathText text={props.text} color={props.color} fontSize={props.fontSize} bold={props.bold} />
    </View>
  );
}

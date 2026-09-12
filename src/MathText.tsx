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
  #c{color:${color};font-size:${fontSize}px;line-height:1.75;font-weight:${bold ? '600' : '400'};
     font-family:-apple-system,'Hiragino Kaku Gothic ProN','Noto Sans JP',Roboto,sans-serif;
     white-space:pre-wrap;word-wrap:break-word;overflow-wrap:break-word;}
  .katex{font-size:1.05em;}
</style></head><body>
<div id="c"></div>
<script>
  document.getElementById('c').textContent = ${payload};
  function post(){
    var h = Math.ceil(document.body.getBoundingClientRect().height);
    if (window.ReactNativeWebView) window.ReactNativeWebView.postMessage(String(h));
  }
  function run(){
    try {
      renderMathInElement(document.getElementById('c'), {
        delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}],
        throwOnError:false
      });
    } catch(e) {}
    post(); setTimeout(post, 250);
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

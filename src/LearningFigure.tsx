import { useEffect, useState } from 'react';
import { Image, Modal, Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { figureSource, hasFigure } from './data/figureStore';
import { FIGURE_ASPECT } from './figures';
import type { LearningFigure as FigureData } from './types';

type Colors = { bg: string; card: string; text: string; sub: string; primary: string; border: string };

/** 本文と同じ幅で読み、細かい図は別画面で拡大する。図の色・縦横比は変えない。 */
export function LearningFigure({ figure, colors: c }: { figure: FigureData; colors: Colors }) {
  const [open, setOpen] = useState(false);
  const [zoom, setZoom] = useState(1);
  const [viewport, setViewport] = useState({ width: 0, height: 0 });
  useEffect(() => { setOpen(false); setZoom(1); }, [figure.figureImage]);
  useEffect(() => { setZoom(1); }, [viewport.width, viewport.height]);
  if (!hasFigure(figure.figureImage)) return null;
  const source = figureSource(figure.figureImage);
  // 100%は画素の原寸ではなく、実際の表示領域に図全体が収まる大きさ。
  const imageWidth = Math.max(0, Math.min(viewport.width - 32, (viewport.height - 32) * FIGURE_ASPECT)) * zoom;
  const close = () => { setOpen(false); setZoom(1); };
  return (
    <View style={s.figure}>
      <Pressable accessibilityRole="button" accessibilityLabel={`図を拡大：${figure.caption}`}
        onPress={() => { setZoom(1); setOpen(true); }} style={[s.imageFrame, { borderColor: c.border }]}>
        <View style={s.imageBox}>
          {/* 同梱Imageには元画像の高さが付くため、比率は親で決め、幅・高さの両方を上書きする。 */}
          <Image source={source} resizeMode="contain" accessibilityLabel={figure.caption} style={s.inlineImage} />
        </View>
        <Text style={[s.hint, { color: c.sub, backgroundColor: c.card }]}>タップして拡大</Text>
      </Pressable>
      <Text selectable style={[s.caption, { color: c.text }]}>{figure.caption}</Text>
      <Modal visible={open} animationType="fade" onRequestClose={close} presentationStyle="fullScreen">
        <SafeAreaView style={{ flex: 1, backgroundColor: c.bg }} edges={['top', 'bottom', 'left', 'right']}>
          <View style={[s.toolbar, { borderBottomColor: c.border }]}>
            <Text accessibilityRole="header" style={[s.title, { color: c.text }]}>図を確認</Text>
            <Pressable onPress={close} accessibilityRole="button" accessibilityLabel="図を閉じる" style={s.control}>
              <Text style={[s.controlText, { color: c.text }]}>閉じる ×</Text>
            </Pressable>
          </View>
          <View style={s.viewer} onLayout={({ nativeEvent: { layout } }) => {
            setViewport(previous => previous.width === layout.width && previous.height === layout.height
              ? previous : { width: layout.width, height: layout.height });
          }}>
            <ScrollView key={`${figure.figureImage}-${viewport.width}-${viewport.height}-${zoom === 1 ? 'fit' : 'zoom'}`}
              style={s.viewer} contentContainerStyle={{ minHeight: viewport.height, justifyContent: 'center' }}>
              <ScrollView horizontal style={{ flexGrow: 0 }}
                contentContainerStyle={{ minWidth: viewport.width, justifyContent: 'center', alignItems: 'center' }}>
                {imageWidth > 0 && <Image source={source} resizeMode="contain" accessibilityLabel={figure.caption}
                  style={{ width: imageWidth, height: imageWidth / FIGURE_ASPECT, backgroundColor: '#fff' }} />}
              </ScrollView>
            </ScrollView>
          </View>
          <ScrollView style={s.captionScroll}>
            <Text selectable style={[s.modalCaption, { color: c.text }]}>{figure.caption}</Text>
          </ScrollView>
          <View style={[s.zoomBar, { borderTopColor: c.border }]}>
            <Pressable onPress={() => setZoom(v => Math.max(1, v - 0.5))} disabled={zoom === 1}
              accessibilityRole="button" accessibilityLabel="図を縮小" accessibilityState={{ disabled: zoom === 1 }}
              style={[s.control, { opacity: zoom === 1 ? 0.35 : 1 }]}>
              <Text style={[s.controlText, { color: c.text }]}>− 縮小</Text>
            </Pressable>
            <Text style={{ color: c.sub }}>{Math.round(zoom * 100)}%</Text>
            <Pressable onPress={() => setZoom(v => Math.min(3, v + 0.5))} disabled={zoom === 3}
              accessibilityRole="button" accessibilityLabel="図を拡大" accessibilityState={{ disabled: zoom === 3 }}
              style={[s.control, { opacity: zoom === 3 ? 0.35 : 1 }]}>
              <Text style={[s.controlText, { color: c.text }]}>＋ 拡大</Text>
            </Pressable>
          </View>
        </SafeAreaView>
      </Modal>
    </View>
  );
}

const s = StyleSheet.create({
  figure: { marginVertical: 12, width: '100%' },
  imageFrame: { backgroundColor: '#fff', borderWidth: 1, borderRadius: 12, overflow: 'hidden' },
  imageBox: { width: '100%', aspectRatio: FIGURE_ASPECT },
  inlineImage: { position: 'absolute', top: 0, left: 0, width: '100%', height: '100%' },
  viewer: { flex: 1, minHeight: 0, minWidth: 0 },
  captionScroll: { maxHeight: 120, flexGrow: 0 },
  hint: { paddingVertical: 9, textAlign: 'center', fontSize: 13 },
  caption: { fontSize: 15, lineHeight: 25, marginTop: 10 },
  toolbar: { paddingHorizontal: 16, flexDirection: 'row', alignItems: 'center', borderBottomWidth: 1 },
  title: { flex: 1, fontSize: 18, fontWeight: '700' },
  control: { minHeight: 48, minWidth: 88, paddingHorizontal: 12, justifyContent: 'center', alignItems: 'center' },
  controlText: { fontSize: 16, fontWeight: '600' },
  modalCaption: { fontSize: 16, lineHeight: 28, padding: 20 },
  zoomBar: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-around', borderTopWidth: 1 },
});

import { useEffect, useRef, useState } from 'react';
import { Modal, Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';
import { SafeAreaProvider, SafeAreaView } from 'react-native-safe-area-context';
import Svg, { Path } from 'react-native-svg';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { getContent } from './data/contentStore';
import { RichText } from './MathText';

export type Announcement = {
  id: string; title: string; body: string; publishedAt: number; revision?: number; expiresAt?: number;
};
const READ_KEY = 'cae.announcements.read.v1';
type ReadMap = Record<string, string>;

export function announcementVersion(item: Announcement): string {
  return item.publishedAt + ':' + (item.revision ?? 1);
}
export function parseAnnouncements(value: unknown, now = Date.now()): Announcement[] {
  const doc = value as {schema?: number; items?: unknown[]};
  if (doc?.schema !== 1 || !Array.isArray(doc.items) || doc.items.length > 50) return [];
  const ids = new Set<string>();
  const valid = doc.items.filter((value): value is Announcement => {
    const item = value as Announcement;
    if (!item || typeof item.id !== 'string' || !/^[a-z0-9][a-z0-9-]{0,63}$/.test(item.id)
      || ids.has(item.id) || typeof item.title !== 'string' || !item.title.trim() || item.title.length > 80
      || typeof item.body !== 'string' || !item.body.trim() || item.body.length > 4000
      || !Number.isSafeInteger(item.publishedAt) || item.publishedAt <= 0
      || (item.revision != null && (!Number.isSafeInteger(item.revision) || item.revision < 1))
      || (item.expiresAt != null && (!Number.isSafeInteger(item.expiresAt) || item.expiresAt <= item.publishedAt))) return false;
    ids.add(item.id); return true;
  });
  return valid.filter(item => item.publishedAt <= now && (!item.expiresAt || now < item.expiresAt))
    .sort((a,b) => b.publishedAt - a.publishedAt);
}
export function parseAnnouncementRead(raw: string | null): ReadMap {
  try {
    const value = JSON.parse(raw ?? '{}');
    if (!value || typeof value !== 'object' || Array.isArray(value)) return {};
    return Object.fromEntries(Object.entries(value).filter(([key,v]) =>
      /^[a-z0-9][a-z0-9-]{0,63}$/.test(key) && typeof v === 'string').slice(-256)) as ReadMap;
  } catch { return {}; }
}

type Colors = { bg: string; card: string; text: string; sub: string; primary: string; border: string };
export function AnnouncementsBell({colors: c}: {colors: Colors}) {
  const items = parseAnnouncements(getContent('content/announcements.json'));
  const [read, setRead] = useState<ReadMap | null>(null);
  const [visible, setVisible] = useState(false);
  const [selected, setSelected] = useState<string | null>(null);
  const article = items.find(item => item.id === selected);
  const writes = useRef(Promise.resolve());
  const unread = read ? items.filter(item => read[item.id] !== announcementVersion(item)).length : 0;
  useEffect(() => {
    let active = true;
    void AsyncStorage.getItem(READ_KEY).then(raw => { if (active) setRead(parseAnnouncementRead(raw)); })
      .catch(() => { if (active) setRead({}); });
    return () => { active = false; };
  }, []);
  useEffect(() => {
    if (!visible || !article || !read || read[article.id] === announcementVersion(article)) return;
    const next = Object.fromEntries([...Object.entries(read).filter(([key]) => key !== article.id),
      [article.id, announcementVersion(article)]].slice(-256));
    setRead(next);
    // 順序を守って保存し、続けて記事を開いても既読状態を巻き戻さない。
    writes.current = writes.current.catch(() => {}).then(() => AsyncStorage.setItem(READ_KEY, JSON.stringify(next)));
    void writes.current.catch(() => {});
  }, [visible, article?.id, article?.publishedAt, article?.revision, read]);
  const close = () => { setVisible(false); setSelected(null); };
  const date = (n: number) => new Date(n).toLocaleDateString('ja-JP');
  return <>
    <Pressable accessibilityRole="button" accessibilityLabel={unread ? 'お知らせ、未読' + unread + '件' : 'お知らせ'}
      onPress={() => { setSelected(null); setVisible(true); }} style={[s.bell, {backgroundColor:c.card, borderColor:c.border}]}>
      <Svg width={24} height={24} viewBox="0 0 24 24" accessible={false}>
        <Path d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9M10 21h4"
          fill="none" stroke={c.text} strokeWidth={1.8} strokeLinecap="round" strokeLinejoin="round" />
      </Svg>
      {!!unread && <View style={s.badge}><Text style={s.badgeText}>{unread > 9 ? '9+' : unread}</Text></View>}
    </Pressable>
    <Modal visible={visible} animationType="slide" onRequestClose={() => selected ? setSelected(null) : close()}>
      <SafeAreaProvider><SafeAreaView style={[s.screen,{backgroundColor:c.bg}]}>
        <View style={[s.header,{borderBottomColor:c.border}]}>
          <Text accessibilityRole="header" style={[s.heading,{color:c.text}]}>お知らせ</Text>
          <Pressable accessibilityRole="button" accessibilityLabel="お知らせを閉じる" onPress={close} style={s.action}>
            <Text style={[s.link,{color:c.primary}]}>閉じる</Text>
          </Pressable>
        </View>
        <ScrollView key={selected ?? 'list'} contentContainerStyle={s.content}>
          {selected ? <>
            <Pressable accessibilityRole="button" onPress={() => setSelected(null)} style={s.action}>
              <Text style={[s.link,{color:c.primary}]}>‹ お知らせ一覧へ</Text>
            </Pressable>
            {article ? <View style={[s.entry,{backgroundColor:c.card,borderColor:c.border}]}>
              <Text style={[s.date,{color:c.sub}]}>{date(article.publishedAt)}</Text>
              <Text accessibilityRole="header" style={[s.title,{color:c.text}]}>{article.title}</Text>
              <RichText text={article.body} color={c.text} fontSize={17} bg={c.card} style={{lineHeight:28}} scroll scrollOnlyOverflow />
            </View> : <Text style={[s.body,{color:c.sub}]}>このお知らせは掲載を終了しました。</Text>}
          </> : <>
            {items.map(item => <Pressable key={item.id} accessibilityRole="button" onPress={() => setSelected(item.id)}
              style={[s.entry,{backgroundColor:c.card,borderColor:c.border}]}>
              <Text style={[s.date,{color:c.sub}]}>{date(item.publishedAt)}</Text>
              <View style={s.row}>
                <Text style={[s.title,{color:c.text,flex:1}]}>{item.title}</Text>
                {read && read[item.id] !== announcementVersion(item) && <Text style={s.unread}>未読</Text>}
              </View>
            </Pressable>)}
            {!items.length && <Text style={[s.body,{color:c.sub}]}>お知らせはまだありません。</Text>}
          </>}
        </ScrollView>
      </SafeAreaView></SafeAreaProvider>
    </Modal>
  </>;
}
const s = StyleSheet.create({
  screen:{flex:1},bell:{width:46,height:46,borderRadius:23,borderWidth:1,alignItems:'center',justifyContent:'center',marginLeft:8},
  badge:{position:'absolute',right:-3,top:-3,minWidth:20,height:20,borderRadius:10,paddingHorizontal:4,backgroundColor:'#C82D2D',alignItems:'center',justifyContent:'center'},
  badgeText:{fontSize:11,fontWeight:'700',color:'#fff'},
  header:{flexDirection:'row',alignItems:'center',justifyContent:'space-between',paddingHorizontal:16,borderBottomWidth:1},
  heading:{fontSize:21,lineHeight:30,fontWeight:'700'},action:{minHeight:48,padding:12,justifyContent:'center'},
  link:{fontSize:16,fontWeight:'600'},content:{padding:16,paddingBottom:36,gap:12},
  entry:{borderWidth:1,borderRadius:14,padding:16,gap:12},date:{fontSize:13,lineHeight:20},
  title:{fontSize:18,lineHeight:28,fontWeight:'700',flexShrink:1},body:{fontSize:17,lineHeight:28},
  row:{flexDirection:'row',alignItems:'center',gap:10},unread:{color:'#C82D2D',fontSize:13,fontWeight:'700'},
});

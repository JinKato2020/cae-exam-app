// 問題を解きながら使う小さな関数電卓。
// ・問題画面の右下にアイコンを常駐（ふだんは邪魔にならない）。
// ・押すと画面の一部にだけコンパクトなパネルが出る。後ろの問題は半透明で透けたまま。
// ・配色は本体テーマ（濃紺カード＋シアン）をそのまま受け取る＝世界観を壊さない。
// ・四則＋ √・^（累乗）・()・π に対応。式を文字で組み立て「=」で評価する。
import { useState } from 'react';
import { Pressable, StyleSheet, Text, View } from 'react-native';

// 本体テーマから必要な色だけ受け取る（Theme 型に依存しない＝疎結合）。
export type CalcColors = {
  bg: string;
  card: string;
  text: string;
  sub: string;
  primary: string;
  border: string;
  onPrimary: string;
  amber: string;
};

// ---- 式の評価（再帰下降パーサ） ----------------------------------------
// 対応トークン: 数字/小数点, + - (− も可), * × , / ÷ , ^ , ( ) , √ , π
type Tok = { t: 'num'; v: number } | { t: 'op'; v: string } | { t: 'paren'; v: '(' | ')' };

function tokenize(src: string): Tok[] {
  const out: Tok[] = [];
  let i = 0;
  while (i < src.length) {
    const c = src[i];
    if (c === ' ') { i++; continue; }
    if ((c >= '0' && c <= '9') || c === '.') {
      let j = i + 1;
      while (j < src.length && ((src[j] >= '0' && src[j] <= '9') || src[j] === '.')) j++;
      out.push({ t: 'num', v: parseFloat(src.slice(i, j)) });
      i = j;
      continue;
    }
    if (c === 'π') { out.push({ t: 'num', v: Math.PI }); i++; continue; }
    if (c === '(') { out.push({ t: 'paren', v: '(' }); i++; continue; }
    if (c === ')') { out.push({ t: 'paren', v: ')' }); i++; continue; }
    // 演算子（記号ゆらぎを吸収）
    if (c === '+') { out.push({ t: 'op', v: '+' }); i++; continue; }
    if (c === '-' || c === '−') { out.push({ t: 'op', v: '-' }); i++; continue; }
    if (c === '*' || c === '×') { out.push({ t: 'op', v: '*' }); i++; continue; }
    if (c === '/' || c === '÷') { out.push({ t: 'op', v: '/' }); i++; continue; }
    if (c === '^') { out.push({ t: 'op', v: '^' }); i++; continue; }
    if (c === '√') { out.push({ t: 'op', v: '√' }); i++; continue; }
    throw new Error('bad char');
  }
  return out;
}

// expr := term (('+'|'-') term)*
// term := power (('*'|'/') power)*
// power := unary ('^' power)?            右結合
// unary := ('-'|'√') unary | primary
// primary := num | '(' expr ')'
function evaluate(src: string): number {
  const toks = tokenize(src);
  let p = 0;
  const peek = () => toks[p];
  const eat = () => toks[p++];

  function parseExpr(): number {
    let v = parseTerm();
    while (peek() && peek().t === 'op' && ((peek() as any).v === '+' || (peek() as any).v === '-')) {
      const op = (eat() as any).v;
      const r = parseTerm();
      v = op === '+' ? v + r : v - r;
    }
    return v;
  }
  function parseTerm(): number {
    let v = parsePower();
    while (peek() && peek().t === 'op' && ((peek() as any).v === '*' || (peek() as any).v === '/')) {
      const op = (eat() as any).v;
      const r = parsePower();
      v = op === '*' ? v * r : v / r;
    }
    return v;
  }
  function parsePower(): number {
    const base = parseUnary();
    if (peek() && peek().t === 'op' && (peek() as any).v === '^') {
      eat();
      const exp = parsePower(); // 右結合
      return Math.pow(base, exp);
    }
    return base;
  }
  function parseUnary(): number {
    const t = peek();
    if (t && t.t === 'op' && (t as any).v === '-') { eat(); return -parseUnary(); }
    if (t && t.t === 'op' && (t as any).v === '√') { eat(); return Math.sqrt(parseUnary()); }
    return parsePrimary();
  }
  function parsePrimary(): number {
    const t = eat();
    if (!t) throw new Error('unexpected end');
    if (t.t === 'num') return t.v;
    if (t.t === 'paren' && t.v === '(') {
      const v = parseExpr();
      const close = eat();
      if (!close || close.t !== 'paren' || close.v !== ')') throw new Error('no close');
      return v;
    }
    throw new Error('bad primary');
  }

  const v = parseExpr();
  if (p !== toks.length) throw new Error('trailing');
  if (!isFinite(v)) throw new Error('not finite');
  return v;
}

// 表示用に桁を整える（末尾の0やeを抑えて読みやすく）。
function fmt(n: number): string {
  if (!isFinite(n)) return 'Error';
  if (Number.isInteger(n) && Math.abs(n) < 1e15) return String(n);
  const s = n.toPrecision(10);
  return parseFloat(s).toString();
}

// ---- UI -----------------------------------------------------------------
const ROWS: string[][] = [
  ['C', '(', ')', '√', '⌫'],
  ['7', '8', '9', '^', '÷'],
  ['4', '5', '6', 'π', '×'],
  ['1', '2', '3', '.', '−'],
  ['±', '0', '00', '=', '+'],
];

export function ProblemCalculator({ c }: { c: CalcColors }) {
  const [open, setOpen] = useState(false);
  const [expr, setExpr] = useState('');
  const [result, setResult] = useState<string | null>(null);

  const press = (key: string) => {
    if (key === 'C') { setExpr(''); setResult(null); return; }
    if (key === '⌫') { setExpr((e) => e.slice(0, -1)); return; }
    if (key === '±') {
      // 直近の数を符号反転（簡易：全体に -1 を掛ける形で前置）。
      setExpr((e) => (e.startsWith('-(') && e.endsWith(')') ? e.slice(2, -1) : e ? `-(${e})` : e));
      return;
    }
    if (key === '=') {
      try {
        if (!expr.trim()) return;
        setResult(fmt(evaluate(expr)));
      } catch {
        setResult('式を確認してください');
      }
      return;
    }
    // √ は「√(」として入れると (式) をくくりやすい
    const ins = key === '√' ? '√(' : key;
    setExpr((e) => e + ins);
    setResult(null);
  };

  return (
    <>
      {/* パネル本体（開いているときだけ） */}
      {open && (
        <View style={[s.panel, { backgroundColor: c.card + 'F2', borderColor: c.border }]}>
          <View style={s.head}>
            <Text style={[s.headTxt, { color: c.sub }]}>電卓</Text>
            <Pressable onPress={() => setOpen(false)} hitSlop={8} style={s.close}>
              <Text style={[s.closeTxt, { color: c.sub }]}>✕</Text>
            </Pressable>
          </View>

          {/* 表示：式と答え */}
          <View style={[s.display, { backgroundColor: c.bg, borderColor: c.border }]}>
            <Text style={[s.exprTxt, { color: c.sub }]} numberOfLines={1}>
              {expr || ' '}
            </Text>
            <Text style={[s.resTxt, { color: result === '式を確認してください' ? c.amber : c.text }]} numberOfLines={1}>
              {result ?? (expr ? '' : '0')}
            </Text>
          </View>

          {/* キー */}
          {ROWS.map((row, ri) => (
            <View key={ri} style={s.row}>
              {row.map((key, ki) => {
                const isEq = key === '=';
                const isOp = ['÷', '×', '−', '+', '^', '√', '(', ')'].includes(key);
                const isFn = ['C', '⌫', '±', '00'].includes(key);
                const bg = isEq ? c.primary : isOp ? c.primary + '22' : isFn ? c.border : c.bg;
                const fg = isEq ? c.onPrimary : isOp ? c.primary : c.text;
                return (
                  <Pressable
                    key={ki}
                    onPress={() => press(key)}
                    style={[s.key, { backgroundColor: bg, borderColor: c.border }]}
                  >
                    <Text style={[s.keyTxt, { color: fg }]}>{key}</Text>
                  </Pressable>
                );
              })}
            </View>
          ))}
        </View>
      )}

      {/* 常駐の電卓ボタン（右下） */}
      <Pressable
        onPress={() => setOpen((v) => !v)}
        accessibilityLabel="電卓"
        style={[s.fab, { backgroundColor: open ? c.card : c.primary, borderColor: c.border }]}
      >
        <Text style={[s.fabTxt, { color: open ? c.sub : c.onPrimary }]}>{open ? '✕' : '🖩'}</Text>
      </Pressable>
    </>
  );
}

const s = StyleSheet.create({
  fab: {
    position: 'absolute',
    right: 14,
    bottom: 18,
    width: 48,
    height: 48,
    borderRadius: 24,
    borderWidth: 1,
    alignItems: 'center',
    justifyContent: 'center',
    shadowColor: '#000',
    shadowOpacity: 0.3,
    shadowRadius: 6,
    shadowOffset: { width: 0, height: 3 },
    elevation: 6,
  },
  fabTxt: { fontSize: 22 },
  panel: {
    position: 'absolute',
    right: 12,
    bottom: 76,
    width: 244,
    borderRadius: 16,
    borderWidth: 1,
    padding: 10,
    shadowColor: '#000',
    shadowOpacity: 0.35,
    shadowRadius: 10,
    shadowOffset: { width: 0, height: 6 },
    elevation: 10,
  },
  head: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', marginBottom: 6, paddingHorizontal: 2 },
  headTxt: { fontSize: 12, fontWeight: '700', letterSpacing: 1 },
  close: { padding: 2 },
  closeTxt: { fontSize: 14, fontWeight: '700' },
  display: { borderWidth: 1, borderRadius: 10, paddingHorizontal: 10, paddingVertical: 6, marginBottom: 8, minHeight: 50, justifyContent: 'center' },
  exprTxt: { fontSize: 13, textAlign: 'right', minHeight: 16 },
  resTxt: { fontSize: 22, fontWeight: '800', textAlign: 'right' },
  row: { flexDirection: 'row', marginBottom: 6 },
  key: {
    flex: 1,
    height: 38,
    borderRadius: 9,
    borderWidth: 1,
    marginHorizontal: 3,
    alignItems: 'center',
    justifyContent: 'center',
  },
  keyTxt: { fontSize: 17, fontWeight: '700' },
});

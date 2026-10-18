// 自動生成: 相関図の同梱 data URI ローダー。キーから分野_級シャードを引く。手で編集しない。
/* eslint-disable */
type Shard = Record<string, string>;
const SHARDS: Record<string, () => Shard> = {
  'solid_1': () => (require('./solid_1') as { default: Shard }).default,
  'solid_2': () => (require('./solid_2') as { default: Shard }).default,
  'thermal_1': () => (require('./thermal_1') as { default: Shard }).default,
  'thermal_2': () => (require('./thermal_2') as { default: Shard }).default,
  'vibration_1': () => (require('./vibration_1') as { default: Shard }).default,
  'vibration_2': () => (require('./vibration_2') as { default: Shard }).default,
};
export function getMapDataUri(key: string): string | null {
  const m = /^map_(solid|thermal|vibration)_(\d)_/.exec(key);
  if (!m) return null;
  const load = SHARDS[m[1] + '_' + m[2]];
  if (!load) return null;
  try { return load()[key] ?? null; } catch { return null; }
}

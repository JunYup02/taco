const RISK_STYLES = {
  high: {
    ring: "ring-red-200",
    badge: "bg-red-100 text-red-700",
    bar: "bg-red-500",
  },
  medium: {
    ring: "ring-amber-200",
    badge: "bg-amber-100 text-amber-700",
    bar: "bg-amber-500",
  },
  low: {
    ring: "ring-emerald-200",
    badge: "bg-emerald-100 text-emerald-700",
    bar: "bg-emerald-500",
  },
};

function ReasonList({ title, reasons }) {
  return (
    <div>
      <h3 className="text-sm font-semibold text-slate-700 mb-2">{title}</h3>
      {reasons.length === 0 ? (
        <p className="text-sm text-slate-400">특이 위험 신호가 발견되지 않았습니다.</p>
      ) : (
        <ul className="space-y-1.5">
          {reasons.map((reason, i) => (
            <li key={i} className="text-sm text-slate-600 flex gap-2">
              <span className="text-slate-400">•</span>
              <span>{reason}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default function VerdictResult({ result, onReportClick }) {
  const style = RISK_STYLES[result.risk_level] ?? RISK_STYLES.medium;

  return (
    <section className={`bg-white rounded-2xl shadow-sm border border-slate-200 ring-4 ${style.ring} p-6 space-y-6`}>
      <div className="flex items-center justify-between flex-wrap gap-3">
        <div>
          <p className="text-sm text-slate-500">종합 사기 위험도</p>
          <p className="text-4xl font-bold text-slate-900">{result.combined_score}%</p>
        </div>
        <span className={`px-4 py-2 rounded-full text-sm font-semibold ${style.badge}`}>
          {result.verdict}
        </span>
      </div>

      <div className="w-full h-2 rounded-full bg-slate-100 overflow-hidden">
        <div
          className={`h-full ${style.bar}`}
          style={{ width: `${Math.min(result.combined_score, 100)}%` }}
        />
      </div>

      <div className="grid sm:grid-cols-2 gap-6">
        <ReasonList
          title={`리스팅 모델 근거 (${result.listing_score}%)`}
          reasons={result.listing_reasons}
        />
        <ReasonList
          title={`판매자 모델 근거 (${result.seller_score}%)`}
          reasons={result.seller_reasons}
        />
      </div>

      <button
        onClick={onReportClick}
        className="text-sm text-red-600 hover:text-red-700 font-medium underline underline-offset-2"
      >
        이 거래가 실제 사기였나요? 신고하기
      </button>
    </section>
  );
}

export default function SellerForm({ value, onChange }) {
  const set = (field) => (e) => {
    const raw = e.target.type === "checkbox" ? e.target.checked : e.target.value;
    onChange({ ...value, [field]: raw });
  };

  return (
    <section className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 space-y-4">
      <h2 className="text-lg font-semibold text-slate-900">2. 판매자 정보</h2>
      <p className="text-xs text-slate-500">
        판매자 프로필 페이지에서 확인할 수 있는 정보를 입력하세요.
      </p>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">
            계정 생성 후 경과일
          </label>
          <input
            type="number"
            min="0"
            value={value.account_age_days}
            onChange={set("account_age_days")}
            className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">거래 건수</label>
          <input
            type="number"
            min="0"
            value={value.num_transactions}
            onChange={set("num_transactions")}
            className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">후기 개수</label>
          <input
            type="number"
            min="0"
            value={value.review_count}
            onChange={set("review_count")}
            className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">
            평균 평점 (0~5)
          </label>
          <input
            type="number"
            min="0"
            max="5"
            step="0.1"
            value={value.avg_rating}
            onChange={set("avg_rating")}
            className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>
      </div>

      <label className="flex items-center gap-2 text-sm text-slate-700">
        <input
          type="checkbox"
          checked={value.profile_photo_present}
          onChange={set("profile_photo_present")}
          className="rounded border-slate-300 text-indigo-600 focus:ring-indigo-500"
        />
        프로필 사진이 있다
      </label>
    </section>
  );
}

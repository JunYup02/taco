export default function ListingForm({ value, onChange }) {
  const set = (field) => (e) => {
    const raw = e.target.type === "checkbox" ? e.target.checked : e.target.value;
    onChange({ ...value, [field]: raw });
  };

  return (
    <section className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 space-y-4">
      <h2 className="text-lg font-semibold text-slate-900">1. 리스팅 정보</h2>

      <div>
        <label className="block text-sm font-medium text-slate-700 mb-1">제목</label>
        <input
          type="text"
          value={value.title}
          onChange={set("title")}
          placeholder="예: 아이폰 15 프로 급처"
          className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-slate-700 mb-1">설명</label>
        <textarea
          value={value.description}
          onChange={set("description")}
          rows={4}
          placeholder="판매자가 작성한 게시글 본문을 그대로 붙여넣으세요"
          className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">판매 가격 (원)</label>
          <input
            type="number"
            min="0"
            value={value.asking_price}
            onChange={set("asking_price")}
            className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">
            시세 (원, 선택)
          </label>
          <input
            type="number"
            min="0"
            value={value.market_price}
            onChange={set("market_price")}
            placeholder="비슷한 매물 평균가"
            className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>
      </div>

      <label className="flex items-center gap-2 text-sm text-slate-700">
        <input
          type="checkbox"
          checked={value.stock_photo_reported}
          onChange={set("stock_photo_reported")}
          className="rounded border-slate-300 text-indigo-600 focus:ring-indigo-500"
        />
        사진이 다른 게시물/인터넷에서 본 사진 같다
      </label>
    </section>
  );
}

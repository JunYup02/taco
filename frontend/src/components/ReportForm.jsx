import { useState } from "react";
import { submitReport } from "../api";

export default function ReportForm({ listing, seller, onClose }) {
  const [notes, setNotes] = useState("");
  const [status, setStatus] = useState("idle"); // idle | submitting | done | error

  const handleSubmit = async () => {
    setStatus("submitting");
    try {
      await submitReport({ listing, seller, is_scam: true, notes: notes || null });
      setStatus("done");
    } catch (err) {
      setStatus("error");
    }
  };

  return (
    <section className="bg-white rounded-2xl shadow-sm border border-red-200 p-6 space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold text-slate-900">사기 신고</h2>
        <button onClick={onClose} className="text-sm text-slate-400 hover:text-slate-600">
          닫기
        </button>
      </div>

      {status === "done" ? (
        <p className="text-sm text-emerald-600">
          신고가 접수되었습니다. 제보해주셔서 감사합니다 — 이 사례는 모델 개선에 사용됩니다.
        </p>
      ) : (
        <>
          <p className="text-sm text-slate-500">
            방금 분석한 리스팅/판매자 정보와 함께 확정된 사기 사례로 신고됩니다.
          </p>
          <textarea
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            rows={3}
            placeholder="추가로 남기고 싶은 내용 (선택)"
            className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-red-400"
          />
          {status === "error" && (
            <p className="text-sm text-red-600">신고 접수 중 오류가 발생했습니다. 다시 시도해주세요.</p>
          )}
          <button
            onClick={handleSubmit}
            disabled={status === "submitting"}
            className="w-full bg-red-600 hover:bg-red-700 disabled:opacity-50 text-white font-medium rounded-lg py-2.5 text-sm transition"
          >
            {status === "submitting" ? "제출 중..." : "사기로 신고하기"}
          </button>
        </>
      )}
    </section>
  );
}

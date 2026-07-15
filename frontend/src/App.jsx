import { useState, useEffect } from "react";
import ListingForm from "./components/ListingForm";
import SellerForm from "./components/SellerForm";
import VerdictResult from "./components/VerdictResult";
import ReportForm from "./components/ReportForm";
import { analyze, getWelcomeUser } from "./api";

const initialListing = {
  title: "",
  description: "",
  asking_price: "",
  market_price: "",
  stock_photo_reported: false,
};

const initialSeller = {
  account_age_days: "",
  review_count: "",
  avg_rating: "",
  num_transactions: "",
  profile_photo_present: true,
};

function toNumber(value) {
  const n = Number(value);
  return Number.isFinite(n) ? n : 0;
}

function buildPayload(listing, seller) {
  return {
    listing: {
      title: listing.title,
      description: listing.description,
      asking_price: toNumber(listing.asking_price),
      market_price: listing.market_price === "" ? null : toNumber(listing.market_price),
      stock_photo_reported: listing.stock_photo_reported,
    },
    seller: {
      account_age_days: toNumber(seller.account_age_days),
      review_count: toNumber(seller.review_count),
      avg_rating: toNumber(seller.avg_rating),
      num_transactions: toNumber(seller.num_transactions),
      profile_photo_present: seller.profile_photo_present,
    },
  };
}

export default function App() {
  const [listing, setListing] = useState(initialListing);
  const [seller, setSeller] = useState(initialSeller);
  const [result, setResult] = useState(null);
  const [status, setStatus] = useState("idle"); // idle | loading | error
  const [showReport, setShowReport] = useState(false);
  const [payloadUsed, setPayloadUsed] = useState(null);
  const [welcomeName, setWelcomeName] = useState(null);

  useEffect(() => {
    getWelcomeUser()
      .then((data) => setWelcomeName(data.name))
      .catch(() => setWelcomeName(null));
  }, []);

  const canSubmit = listing.title.trim() && listing.description.trim() && listing.asking_price !== "";

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus("loading");
    setShowReport(false);
    const payload = buildPayload(listing, seller);
    try {
      const data = await analyze(payload);
      setResult(data);
      setPayloadUsed(payload);
      setStatus("idle");
    } catch (err) {
      setStatus("error");
    }
  };

  return (
    <div className="min-h-screen bg-slate-50">
      <header className="bg-white border-b border-slate-200">
        <div className="max-w-3xl mx-auto px-4 py-6">
          <h1 className="text-2xl font-bold text-slate-900">🛡️ SafeTrade Detector</h1>
          <p className="text-sm text-slate-500 mt-1">
            중고거래 리스팅과 판매자 정보를 입력하면, 두 개의 독립 모델이 교차 검증한 사기 위험도를 알려드립니다.
          </p>
          {welcomeName && (
            <p className="text-sm text-indigo-600 font-medium mt-2">환영합니다, {welcomeName}님!</p>
          )}
        </div>
      </header>

      <main className="max-w-3xl mx-auto px-4 py-8 space-y-6">
        <form onSubmit={handleSubmit} className="space-y-6">
          <ListingForm value={listing} onChange={setListing} />
          <SellerForm value={seller} onChange={setSeller} />

          {status === "error" && (
            <p className="text-sm text-red-600">
              분석 요청 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.
            </p>
          )}

          <button
            type="submit"
            disabled={!canSubmit || status === "loading"}
            className="w-full bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white font-semibold rounded-lg py-3 transition"
          >
            {status === "loading" ? "분석 중..." : "사기 위험도 분석하기"}
          </button>
        </form>

        {result && (
          <VerdictResult result={result} onReportClick={() => setShowReport(true)} />
        )}

        {showReport && payloadUsed && (
          <ReportForm
            listing={payloadUsed.listing}
            seller={payloadUsed.seller}
            onClose={() => setShowReport(false)}
          />
        )}
      </main>

      <footer className="max-w-3xl mx-auto px-4 pb-8 text-xs text-slate-400">
        본 서비스의 위험도 점수는 참고용이며, 실제 거래 여부는 사용자의 판단에 따라 결정하시기 바랍니다.
      </footer>
    </div>
  );
}

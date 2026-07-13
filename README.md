# SafeTrade-Detector

중고거래 리스팅과 판매자 정보를 입력하면 두 개의 독립 모델(리스팅 텍스트 모델, 판매자 데이터 모델)이
각각 사기 위험도를 계산하고, 두 결과를 종합한 사기 위험도 점수와 근거를 보여주는 서비스. (PRD.md 참고)

## 구조

- `backend/` — FastAPI. `/api/analyze`, `/api/reports` 제공. 단일 서비스로 빌드된 프론트엔드 정적 파일도 서빙.
  - `backend/ml/` — 학습 데이터 생성 + 모델 학습 스크립트 (scikit-learn LogisticRegression, 해석 가능한 수작업 피처 기반)
  - `backend/app/` — API, DB(SQLite), 검증/응답 스키마
- `frontend/` — React + Tailwind (Vite)

## 모델에 대한 중요한 전제

실제 라벨링된 사기 거래 데이터셋이 없기 때문에, 두 모델은 **합성(synthetic) 데이터**로 학습되었습니다
(`backend/ml/synthetic_data.py`). 가격 이상치, 긴급성 문구, 계정 신규 여부 등 사기 사례에서 흔히
나타나는 패턴을 반영해 분포를 설계했지만, 실제 사기 라벨로 학습된 모델은 아닙니다. `POST /api/reports`로
쌓이는 사용자 신고 데이터가 향후 재학습(진짜 데이터 기반)의 시드가 되도록 설계되어 있습니다.

## 로컬 실행

```bash
# 백엔드
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m ml.train_listing_model
python -m ml.train_seller_model
uvicorn app.main:app --reload --port 8000

# 프론트엔드 (개발 모드, 별도 터미널)
cd frontend
npm install
npm run dev   # http://localhost:5173, /api는 8000번으로 프록시
```

프로덕션처럼 단일 서비스로 확인하려면 `frontend`를 빌드한 뒤 백엔드만 띄우면 됩니다
(백엔드가 `frontend/dist`를 자동으로 서빙합니다):

```bash
cd frontend && npm run build
cd ../backend && uvicorn app.main:app --port 8000
```

## Render 배포

`render.yaml` 기준 단일 웹 서비스로 배포됩니다.

- Build: `bash build.sh` (프론트 빌드 → 백엔드 의존성 설치 → 모델 학습)
- Start: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

SQLite 데이터(`backend/data.db`)는 Render 웹 서비스의 기본 디스크에 저장되며, 별도의 persistent disk를
연결하지 않으면 재배포 시 초기화될 수 있습니다.

## v1 범위 밖

- 실제 마켓플레이스 API 연동 (판매자 데이터는 사용자가 직접 입력)
- 실시간/자동 모델 재학습 (신고 데이터는 축적되고, 재학습은 수동으로 스크립트 실행)
- 브라우저 확장, 인앱 메시징/에스크로, 다국어, 모바일 앱, B2B 대시보드

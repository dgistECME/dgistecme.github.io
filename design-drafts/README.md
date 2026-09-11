# design-drafts — 홈 디자인 초안 백업

Claude Design 캔버스( https://claude.ai/code/artifact/a6db981f-9b66-4d66-8b9a-1751acf8f164 )의 원본 아트보드.
각 `*.dc.html`은 브라우저에서 바로 열어 볼 수 있음. `*.png`는 1440px 렌더.

| 파일 | 방향 | 상태 |
|---|---|---|
| `Main.dc.html` | C · Bold Editorial (다크 네이비) | **현재 사이트 적용 중** |
| `DirectionF.dc.html` | F · Photo Magazine (세로 대제목 + 사진 모자이크 + 노랑) | 백업 요청됨 — 다음 후보 |
| `DirectionN.dc.html` | N · Orbit (동심원 링 + 원형 사진, 공전 노드 애니메이션) | **사용자 선호 — 후보 1순위** |
| `DirectionP.dc.html` | P · Waveform (사인파 + 알약형 사진, 파형 위 연구 노드) | N 계열 |
| `DirectionQ.dc.html` | Q · Hex Lattice (육각 격자 + 육각 사진/셀) | N 계열 |
| `DirectionR.dc.html` | R · Signal Field (점 필드 + 신호 링 퍼짐 + 통계 바) | N 계열 |
| `DirectionM.dc.html` | M · Overlap Editorial (순백, 초대형 아웃라인 타이포 + 기울어진 사진 겹침) | 흰 배경·강한 구성 |
| `DirectionN.dc.html` | N · Orbit (순백, 동심원 링 + 원형 사진) | 흰 배경·강한 구성 |
| `DirectionO.dc.html` | O · Vertical Rail (순백, 세로 레일 + 굵은 룰 + 흑백 사진) | 흰 배경·강한 구성 |
| `DirectionJ.dc.html` | J · Hairline Magazine (순백, 회색 룰선, 잡지 3단) | 흰 배경 후보 |
| `DirectionK.dc.html` | K · Serif Editorial (순백, 세리프 대문장, 여백) | 흰 배경 후보 |
| `DirectionL.dc.html` | L · Bento Cards (순백, 테두리 카드 그리드) | 흰 배경 후보 |
| `DirectionG.dc.html` | G · Sky Airy (흰+하늘색, 라운드 사진, 파스텔 타일) | 밝은 후보 |
| `DirectionH.dc.html` | H · Mint Lab (민트/라임 밴드, 유기 곡선 사진, 칩) | 밝은 후보 |
| `DirectionI.dc.html` | I · Warm Sunlight (아이보리+코랄, 세리프 제목) | 밝은 후보 |
| `DirectionD.dc.html` | D · Swiss Grid (흰/검/빨강 점, 모노 라벨) | 후보 |
| `DirectionE.dc.html` | E · Paper Journal (크림 종이, 세리프, 학술지) | 후보 |
| `DirectionA.dc.html` | A · Classic Academic (네이비+금색) | 탈락 |
| `DirectionB.dc.html` | B · Clean Modern (흰 배경, 둥근 카드) | 탈락 |
| `Previous.dc.html` | Wix 원본 재현 | 사이트 태그 `v1-wix-style` |

## F 디자인 토큰 (이식용)
- 배경 `#ffffff`, 잉크 `#141414`, 포인트 `#ffd400` (진한 노랑 텍스트 `#b59400`), 회색 `#666666` / `#e9e9e9`
- 제목 Barlow Condensed 800 (대문자, letter-spacing -0.01em), 본문 Barlow 400/500/600
- 구조: 헤더 76px + 1px 룰 / 히어로 440px 좌측 세로 제목 + 우측 2×3 사진 모자이크(1px 검정 간격) / 뉴스 티커 1줄 / Research 3열 숫자 카드(노랑 숫자 + 검정 외곽선) + People 리스트
- 링크 hover: 노랑 배경. 버튼: 검정 채움 / 검정 1px 외곽선

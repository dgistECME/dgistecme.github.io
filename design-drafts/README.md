# design-drafts — 홈 디자인 초안 백업

Claude Design 캔버스( https://claude.ai/code/artifact/a6db981f-9b66-4d66-8b9a-1751acf8f164 )의 원본 아트보드.
각 `*.dc.html`은 브라우저에서 바로 열어 볼 수 있음. `*.png`는 1440px 렌더.

| 파일 | 방향 | 상태 |
|---|---|---|
| `Main.dc.html` | C · Bold Editorial (다크 네이비) | **현재 사이트 적용 중** |
| `DirectionF.dc.html` | F · Photo Magazine (세로 대제목 + 사진 모자이크 + 노랑) | 백업 요청됨 — 다음 후보 |
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

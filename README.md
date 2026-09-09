# ECME LAB 홈페이지 (Astro + GitHub Pages)

Wix에서 이전한 정적 사이트. 콘텐츠는 전부 `src/data/*.yaml`, 디자인은 `src/styles/global.css` 상단 토큰.

## 로컬 실행

```bash
npm install
npm run dev      # http://localhost:4321
npm run build    # dist/
```

## 배포 (GitHub Pages)

1. GitHub 저장소 생성 → 이 `site/` 폴더 내용을 저장소 루트로 push (`main` 브랜치).
2. 저장소 Settings → Pages → Source: **GitHub Actions**.
3. 이후 `main`에 push 할 때마다 `.github/workflows/deploy.yml`이 자동 빌드·배포.
   - 저장소 이름이 `<계정>.github.io` 이면 주소 `https://<계정>.github.io/`
   - 다른 이름이면 `https://<계정>.github.io/<저장소>/` (base path 자동 처리)

## 콘텐츠 업데이트 (GitHub 웹에서 브라우저만으로)

저장하면 2~3분 후 자동 반영. 파일 열기 → 연필 아이콘(Edit) → 수정 → **Commit changes**.

### 뉴스 1건 추가 — `src/data/news.yaml`
맨 위에 추가:
```yaml
- date: 2026.09.10
  text: 홍길동 석∙박사과정이 2026 NENS에서 Best Poster Award를 수상하였습니다.
```

### 멤버 추가 — `src/data/members.yaml`
1. 사진을 `public/img/full/` 에 업로드 (파일명 영문, 예: `hong.webp` 또는 `hong.jpg`).
2. 해당 섹션(`Post-Doctor` / `Graduate` / `Undergraduate`)의 `members:` 아래에 추가:
```yaml
  - name: Gildong Hong
    position: MS/Ph.D integrated Course (2026.09~)
    education:
    - B.S., DGIST
    research_field: Triboelectric Materials
    email: hong@dgist.ac.kr
    photo: hong.jpg          # public/img/full/ 안의 파일명
```
> 기존 항목의 `photo:` 값은 Wix 시절 이미지 ID. 새 항목은 파일명을 직접 쓰면 됨 (`src/lib/img.ts`가 둘 다 처리).

### 논문 추가 — `src/data/papers.yaml`
`papers:` 맨 위에 추가 (번호는 직전 +1):
```yaml
- number: 82
  year: 2026
  title: 논문 제목
  url: https://doi.org/...
  authors: A. Kim, B. Lee, Ju-Hyuck Lee*
  venue: Nano Energy, 155, 112345 (2026)
  impact_factor: 17.1
  note: null
```

### 언론보도 추가 — `src/data/press.yaml`
썸네일을 `public/img/thumb/`에 업로드 후:
```yaml
- year: 2026
  title: 기사 제목
  url: https://...
  summary: 한 줄 요약
  date: 2026.09.10
  outlet: 연합뉴스
  thumbnail: news-2026-09-10.jpg
```

### 사진 포스트 추가 — `src/data/photos.yaml`
사진을 `public/img/full/`(원본)과 `public/img/thumb/`(작게, 선택) 에 업로드 후 `posts:` 맨 위에:
```yaml
- year: 2026
  date: 2026.09.10
  caption: 2026 하계 워크샵
  tags: '#워크샵 #제주'
  images:
  - uri: workshop-2026-1.jpg
    alt: null
  - uri: workshop-2026-2.jpg
    alt: null
```

### 멤버 → 졸업 처리
`members.yaml`에서 항목 삭제 → `alumni.yaml`의 `graduates:` 맨 위에 추가:
```yaml
- name_ko: 홍길동
  name_en: Gildong Hong
  degree: M.S.
  graduated: '26.08'
  affiliation: 삼성전자
```

## YAML 주의
- 들여쓰기는 **스페이스 2칸**, 탭 금지.
- 콜론(`:`)이나 `#`이 들어간 문장은 따옴표로 감싸기: `title: '제목: 부제'`
- 빌드 실패 시 사이트는 이전 버전 그대로 유지됨. 저장소 Actions 탭에서 에러 줄 확인.

## 구조
```
src/data/        콘텐츠 (YAML) + images.json (Wix 이미지 ID → 파일명 매핑)
src/pages/       페이지 10개
src/components/  Header / Footer / SubTabs
src/layouts/     Base.astro (head, 폰트)
src/styles/      global.css (디자인 토큰 최상단)
public/img/full  본문 이미지 (WebP, 최대 1600px)
public/img/thumb 썸네일 (480px)
```

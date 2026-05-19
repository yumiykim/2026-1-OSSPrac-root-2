<div align="center">

# 🌿 TEAM ROOT

**2026-1 오픈소스소프트웨어실습 팀 프로젝트**

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Jinja2](https://img.shields.io/badge/Jinja2-B41717?style=for-the-badge&logo=jinja&logoColor=white)](https://jinja.palletsprojects.com/)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![Google Gemini](https://img.shields.io/badge/Gemini_AI-8E75B2?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![Pillow](https://img.shields.io/badge/Pillow-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python-pillow.org/)
[![python-dotenv](https://img.shields.io/badge/python--dotenv-ECD53F?style=for-the-badge&logo=dotenv&logoColor=black)](https://pypi.org/project/python-dotenv/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

</div>

---

## 📌 프로젝트 소개

Flask 기반 팀 소개 웹 애플리케이션입니다.  
ROOT 팀 소개 페이지와 함께, **누구나 자신만의 팀 페이지를 만들 수 있는 팀페이지 제작 기능**을 제공합니다.  
Google Gemini AI를 활용한 프로필/팀 이미지 자동 생성, 질문게시판, 비상연락망 등을 포함합니다.

---

## ✨ 주요 기능

### 🏠 ROOT 팀 소개
- 팀 소개 메인 페이지 (팀 비전, 팀 소개 영상)
- 팀원 카드 목록 및 팀원 상세 페이지 (포트폴리오, SNS/GitHub 링크)
- 팀원 상세 페이지 PDF 저장

### 💬 질문게시판
- 게시글 CRUD (작성 · 수정 · 삭제) — 비밀번호 인증
- 댓글 CRUD (작성 · 수정 · 삭제) — 비밀번호 인증
- 게시글 이전/다음 탐색
- 제목 · 작성자 · 전체 키워드 검색 (검색어 하이라이트)

### ✏️ 팀페이지 제작
- 팀명, 팀 소개, 팀 이미지 입력
- 최대 4명 팀원 입력 (이름, 학번, 학과, 전화번호, 이메일, 역할, 사용 언어, 프로필 사진, GitHub/Instagram 아이디, 포트폴리오)
- 포트폴리오 항목 추가 (제목, 기간, 역할, 설명)
- 포트폴리오 링크 및 파일 첨부 (PDF, DOC, PPT, Excel, ZIP, 이미지)
- 생성된 팀 페이지 결과 확인 및 팀원 수정/삭제
- 생성된 팀 페이지 PDF 저장

### 🤖 AI 이미지 생성 (Google Gemini)
- 팀원 프로필 이미지를 텍스트 프롬프트로 자동 생성 (Memoji 스타일 3D 아바타)
- 팀 대표 이미지를 텍스트 프롬프트로 자동 생성 (Memoji 스타일 3D 카툰, 로고·마스코트·그룹 컨셉)
- 직접 이미지 업로드와 AI 생성 중 선택 가능

### 📞 비상연락망
- ROOT 팀원 연락처 페이지

### 🌙 다크 모드
- 전체 페이지 다크 모드 / 라이트 모드 전환 가능

---

## 🗂️ 프로젝트 구조

```text
.
├── Subject3_1/                   # 입력 폼 실습
│   ├── ex4.py
│   └── templates/
│       ├── input.html
│       └── result.html
│
└── Subject3_2/                   # ROOT 팀 소개 & 팀페이지
    ├── team.py                   # Flask 앱 메인
    ├── requirements.txt
    ├── .env                      # 환경 변수 (API 키 등)
    ├── Dockerfile                # Docker 이미지 빌드 설정
    ├── docker-compose.yml        # Docker Compose 실행 설정
    ├── .dockerignore
    ├── uwsgi.ini                 # uWSGI 서버 설정
    ├── data/
    │   ├── members.json          # ROOT 팀/팀원 정보 (시드)
    │   ├── posts.json            # 게시판 초기 데이터 (시드)
    │   └── comments.json         # 댓글 초기 데이터 (시드)
    ├── instance/
    │   └── board/
    │       ├── posts.json        # 게시판 런타임 데이터
    │       └── comments.json     # 댓글 런타임 데이터
    ├── static/
    │   ├── css/
    │   │   ├── base.css          # 공통 스타일 (다크모드 포함)
    │   │   ├── board.css
    │   │   ├── contact.css
    │   │   ├── index.css
    │   │   ├── input.css
    │   │   └── member_detail.css
    │   ├── images/               # ROOT 팀 고정 이미지
    │   ├── uploads/              # 업로드된 이미지/파일
    │   │   ├── ai/               # AI 생성 이미지
    │   │   │   ├── profile/
    │   │   │   └── team/
    │   │   └── portfolio/        # 포트폴리오 첨부 파일
    │   └── videos/               # ROOT 팀 소개 영상
    └── templates/
        ├── index.html
        ├── input.html
        ├── result.html
        ├── member_detail.html
        ├── contact.html
        └── board/
            ├── post_list.html
            ├── post_detail.html
            └── post_form.html
```

---

## 🔗 라우트 목록

| Method | Route | 설명                        |
|--------|-------|---------------------------|
| GET | `/` | ROOT 팀 소개 메인              |
| GET | `/contact` | 비상연락망                     |
| GET | `/members/<id>` | ROOT 팀원 또는 생성 팀원 상세 페이지   |
| POST | `/members/<id>/delete` | 생성 팀원 삭제                  |
| GET | `/team-page` | 팀페이지 제작 진입 (기존 여부에 따라 분기) |
| GET | `/input` | 팀페이지 제작 · 팀원 입력/수정        |
| POST | `/member/update` |  팀/팀원 정보 저장 및 수정 처리       |
| GET | `/result` | 생성된 팀 페이지 결과              |
| GET | `/reset` | 생성 중인 팀 정보 초기화            |
| GET | `/board` | 질문게시판 목록                  |
| GET | `/board/write` | 게시글 작성 페이지                |
| GET | `/board/<id>` | 게시글 상세                    |
| GET | `/board/<id>/edit` | 게시글 수정 페이지                |
| POST | `/board/update` | 게시글 생성 · 수정 · 삭제 처리       |
| GET | `/comments/<id>/edit` | 댓글 수정 리다이렉트               |
| POST | `/comment/update` | 댓글 생성 · 수정 · 삭제 처리        |

---

## 💾 데이터 저장

| 데이터 | 저장 방식 |
|--------|-----------|
| ROOT 팀/팀원 정보 | `data/members.json` (정적 파일) |
| 질문게시판 게시글 | `instance/board/posts.json` (런타임) |
| 질문게시판 댓글 | `instance/board/comments.json` (런타임) |
| 사용자 생성 팀 정보 | Flask **Session** (서버 메모리) |
| 업로드 이미지/파일 | `static/uploads/` (UUID 파일명으로 저장) |
| AI 생성 이미지 | `static/uploads/ai/profile/`, `static/uploads/ai/team/` |
| 포트폴리오 첨부 파일 | `static/uploads/portfolio/` |

> 게시판 데이터는 서버 최초 실행 시 `data/` 하위 시드 파일에서 `instance/board/`로 복사됩니다.

---

## 🖼️ 이미지 처리

- 업로드 이미지는 UUID 기반 파일명으로 저장 (충돌 방지)
- 지원 이미지 형식: `png`, `jpg`, `jpeg`, `gif`, `webp`
- 포트폴리오 첨부 파일 형식: `pdf`, `doc`, `docx`, `ppt`, `pptx`, `xls`, `xlsx`, `zip`, 이미지
- AI 이미지 생성: Google Gemini API (`gemini-2.5-flash-image`) 호출 후 PIL로 PNG 저장

---

## ⚙️ 환경 변수

`.env` 파일을 `Subject3_2/` 하위에 생성하세요.

```env
SECRET_KEY=your_flask_secret_key
GEMINI_API_KEY=your_google_gemini_api_key
GEMINI_IMAGE_MODEL=gemini-2.5-flash-image
```

| 변수 | 설명 | 기본값 |
|------|------|--------|
| `SECRET_KEY` | Flask 세션 암호화 키 | `dev-secret-key` |
| `GEMINI_API_KEY` | Google Gemini API 키 | — |
| `GEMINI_IMAGE_MODEL` | Gemini 이미지 생성 모델 | `gemini-2.5-flash-image` |

> `GEMINI_API_KEY`가 없으면 AI 이미지 생성 기능은 비활성화됩니다.

---

## 🚀 실행 방법

### 로컬 실행

**Subject3_2** (팀 소개 웹페이지)

```bash
cd Subject3_2
pip install -r requirements.txt
python team.py
```

접속 주소: `http://127.0.0.1:5000`

**Subject3_1** (입력 폼 실습)

```bash
cd Subject3_1
python ex4.py
```

접속 주소: `http://127.0.0.1:5000`

### Docker 실행

```bash
cd Subject3_2
docker compose up --build
```

접속 주소: `http://localhost:8000`

> `.env` 파일이 `Subject3_2/` 하위에 있어야 합니다.  
> `instance/`와 `static/uploads/`는 호스트에 볼륨 마운트되어 데이터가 컨테이너 재시작 후에도 유지됩니다.

---

## 🤝 Contributing

### 브랜치 전략

이 프로젝트는 **Fork 기반 협업** 방식을 사용합니다.

#### 레포지토리 구조

```
[upstream]  CSID-DGU/2026-1-OSSPrac-root-2   ← 팀 공유 중앙 레포
              ├── main     (최종 제출용)
              └── develop  (통합 브랜치 — 모든 PR의 목적지)
                               ↑ PR
[origin]    {내 계정}/2026-1-OSSPrac-root-2   ← 내가 fork한 개인 레포
              └── {이름}   (예: ymk — 내 작업 브랜치)
```

#### 브랜치 역할

| 브랜치 | 레포 | 설명 |
|--------|------|------|
| `main` | upstream | 최종 제출용. `develop`에서 검증된 코드만 merge |
| `develop` | upstream | 모든 작업이 모이는 통합 브랜치. PR의 base 브랜치 |
| `{이름}` (예: `ymk`) | origin | 본인 작업 전용 브랜치 |

#### 협업 규칙

- 작업은 반드시 **본인 이름 브랜치**에서 진행
- PR 생성 후 **다른 팀원에게 코드 리뷰 요청**
- **merge는 본인이 직접 하지 않고** 병합 담당 팀원이 수행

---

### 작업 흐름

**1️⃣ 작업 전 — 최신 코드 반영**

```bash
git checkout ymk          # 나의 개인 브랜치로 이동
git pull upstream develop # 중앙 레포 최신 사항 반영
```

**2️⃣ 작업 후 — 나의 코드 올리기**

```bash
git add .
git commit -m "커밋 메시지"
git pull upstream develop # 충돌 방지를 위해 push 전 최신화
git push origin ymk
```

**3️⃣ PR 생성**

1. GitHub에서 `Pull requests` → `New pull request`
2. 아래와 같이 방향 설정 확인

   | 항목 | 값 |
      |------|----|
   | base repository | `CSID-DGU/2026-1-OSSPrac-root-2` (upstream, 중앙 레포) |
   | base branch | `develop` |
   | head repository | `{내 계정}/2026-1-OSSPrac-root-2` (origin, 내 fork) |
   | compare branch | `{이름}` (예: `ymk`) |

3. PR 생성 후 다른 팀원에게 코드 리뷰 요청
4. 본인이 직접 merge하지 않고 **병합 담당 팀원에게 merge 요청**

---

### 커밋 메시지 컨벤션

| 태그 | 설명 | 예시 |
|------|------|------|
| `Feat` | 새로운 기능 추가 | `Feat: 팀원 소개 페이지 추가` |
| `Fix` | 버그 수정 | `Fix: 팀원 카드 클릭 시 상세페이지 이동 오류 수정` |
| `Design` | UI 스타일 및 레이아웃 변경 | `Design: 메인 페이지 레이아웃 및 색상 수정` |
| `Docs` | 문서 수정 (README, 주석 등) | `Docs: 프로젝트 실행 방법 README에 추가` |
| `Refactor` | 리팩토링 (기능 변화 없음) | `Refactor: 팀원 데이터 처리 로직 구조 개선` |
| `Chore` | 설정/패키지/환경 변경 | `Chore: 파일 경로 설정 수정` |
| `Improve` | 기존 기능 개선 (성능, UX, 안정성) | `Improve: AI 이미지 생성 응답 안정성 향상` |

### PR 제목 규칙

| 태그 | 설명 | 예시 |
|------|------|------|
| `[Feature]` | 새로운 기능 추가 | ✨ `[Feature] 마이페이지 기능 추가` |
| `[Fix]` | 버그 수정 | 🐛 `[Fix] 로그인 버튼 오류 수정` |
| `[Design]` | UI 스타일 및 레이아웃 | 🎨 `[Design] 헤더 스타일 변경` |
| `[Docs]` | 문서 수정 | 📝 `[Docs] README 사용법 수정` |
| `[Refactor]` | 리팩토링 | ♻️ `[Refactor] API 요청 함수 리팩토링` |
| `[Chore]` | 환경 설정 변경 | 🔧 `[Chore] webpack 설정 변경` |
| `[Improve]` | 기존 기능 개선 | 📈 `[Improve] AI 이미지 생성 응답 안정성 향상` |

---

## 🌿 ROOT 팀원 소개 및 담당 역할

<table>
  <tr>
    <td align="center" valign="top" width="33%">
      <img src="Subject3_2/static/images/root-member1.png" width="130"/><br/><br/>
      <b>오승현</b><br/>
      <sub>🎓 교육학과</sub><br/>
      <sub>👑 팀장 · 프론트엔드</sub><br/><br/>
      <div align="left"><sub>
        • 메인 페이지 및 팀 소개 페이지 UI 구성<br/>
        • 팀원 상세 페이지 화면 구현<br/>
        • 다크모드 및 전체 CSS 스타일 통일<br/>
        • 네비게이션 바 / 드롭다운 메뉴 구현<br/>
        • 게시판 화면(목록·상세·작성·수정) CSS 작업<br/>
        • 팀제작 페이지 UI 구성<br/>
        • 전체 화면 비율 및 레이아웃 조정<br/>
        • 비상 연락망 페이지 제작<br/>
        • 팀 영상 제작
      </sub></div><br/>
      <a href="https://github.com/2024110423osh">
        <img src="https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white"/>
      </a>
    </td>
    <td align="center" valign="top" width="33%">
      <img src="Subject3_2/static/images/root-member2.png" width="130"/><br/><br/>
      <b>김유미</b><br/>
      <sub>🎓 산업시스템공학과</sub><br/>
      <sub>🛠️ 팀원 · 백엔드</sub><br/><br/>
      <div align="left"><sub>
        • ROOT 팀 소개 메인 페이지 구현<br/>
        • 팀페이지 제작 기능 구현 (Session 구조 설계, 팀원 CRUD, 파일 업로드, 포트폴리오)<br/>
        • Google Gemini AI 이미지 생성 연동 및 프롬프트 설계<br/>
        • 팀원 상세 페이지 및 PDF 저장 기능 구현<br/>
        • 게시판 데이터 구조 설계 (시드/런타임 분리)<br/>
        • Docker 배포 환경 구성 (Dockerfile, docker-compose, uWSGI)<br/>
        • Git 브랜치 전략 수립, 협업 규칙 설계, merge 전담
      </sub></div><br/><br/>
      <a href="https://github.com/yumiykim">
        <img src="https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white"/>
      </a>
    </td>
    <td align="center" valign="top" width="33%">
      <img src="Subject3_2/static/images/root-member3.png" width="130"/><br/><br/>
      <b>오지윤</b><br/>
      <sub>🎓 경영정보학과</sub><br/>
      <sub>🛠️ 팀원 · 백엔드</sub><br/><br/>
      <div align="left"><sub>
        • 질문 게시판 백엔드 기능(글/댓글 작성·수정·삭제) 구현<br/>
        • 게시글 및 댓글 수정을 위한 비밀번호 4자리 권한 검사 로직 구현<br/>
        • 프론트엔드 화면(HTML)과 백엔드 데이터 연결 작업
      </sub></div><br/><br/><br/><br/><br/>
      <a href="https://github.com/JeeyoonO">
        <img src="https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white"/>
      </a>
    </td>
  </tr>
</table>

---

<div align="center">
  <sub>2026-1 오픈소스소프트웨어실습 · Dongguk University</sub>
</div>

# mumble-to-bars

입을 연 비언어 발성(멈블/스캣)을 모음 템플릿으로 변환하고, 그 플로우에 맞는 한국어/영어 랩 가사를 자동 생성한다.
대상 사용자: 멈블은 쉽게 나오지만 가사 쓰기가 어려운 래퍼.

```
오디오(16kHz mono) → 음절 분리 → 모음 인식 → [모음 템플릿] → LLM 가사 생성 → 코드 검증 → (실패 시 재생성)
```

**현재 우선순위: 음성 → 모음 변환.** 가사 생성(`lyrics/`)은 모음 추출 품질이 확인된 뒤에 시작한다.

## 명령어

```bash
uv sync                      # .venv 생성/동기화 (Python 3.11)
uv add <pkg>                 # 런타임 의존성 추가 (dev는 --dev)
uv run pytest                # 테스트
uv run ruff check . --fix    # 린트
uv run ruff format .         # 포맷
uv run m2b --help            # CLI
uv run pre-commit run -a     # 전체 훅 수동 실행
```

`pip install`을 쓰지 않는다. 의존성은 항상 `uv add`로 추가해 `pyproject.toml`과 `uv.lock`에 기록한다.

## 구조

```
src/mumble_to_bars/
  schema.py     모음 템플릿 스키마 + 자모↔IPA 변환 (단계 간 유일한 계약)
  cli.py        m2b 진입점. 단계들을 조립한다
  audio/        로딩, 리샘플, 음절 분리(onset/음절핵)
  vowel/        wav2vec2 CTC 모음 추출, 포먼트 대안
  lyrics/       LLM 생성 + 검증 루프 (아직 시작 안 함)
  metrics/      음절 수 정확도, 모음 오류율 등
eval/manifest.jsonl   정답 모음열 (커밋함, 오디오는 경로만 참조)
experiments/NNN-name/ 실험별 run.py + README.md, 요약은 experiments/RESULTS.md
docs/                 schema.md(스펙), decisions/(결정 기록)
data/  outputs/       원본 녹음 / 생성 산출물 (gitignore)
```

### 의존성 규칙
- 단계 패키지(`audio`, `vowel`, `lyrics`)끼리 서로 import 하지 않는다. `schema.py` 타입으로만 데이터를 주고받는다.
- `cli.py`만 단계들을 조립한다.
- `experiments/`는 `src`를 import 해도 되지만, `src`는 `experiments/`를 import 하지 않는다.
- 실험에서 검증된 코드만 `src`로 옮기고, 옮길 때 테스트를 함께 추가한다.
- 표기 변환(자모↔IPA)은 `schema.py` 한 곳에서만 한다.

## 도메인 규칙
- 입력은 **입을 연 발성**이다. 입을 다문 허밍(/m/)에는 모음 정보가 없다.
- 1차 모음 인식: `Kkonjeong/wav2vec2-base-korean` 자모 CTC 출력. 실패 시 대안은 `docs/decisions/0001-stage0.md` 참고.
- 받침은 대표음 7개(ㄱㄴㄷㄹㅁㅂㅇ)로 정규화한다.
- LLM은 한글 음절 수를 정확히 못 센다. 음절 수, 모음 일치는 반드시 코드로 검증한다.
- 미정 사항(ㅐ/ㅔ 병합, 이중모음, 쉼 표현 등)은 `docs/schema.md`에 있다. 임의로 결정하지 말고 물어본다.

## 데이터
- 오디오, 녹음 파일은 절대 커밋하지 않는다(본인 목소리). `data/`, `outputs/`, `*.wav` 등은 gitignore 되어 있다.
- 평가셋 형식은 `eval/README.md` 참고. 모음열은 문자열이 아니라 리스트로 쓴다.

## 실험
- 새 실험은 `experiments/NNN-short-name/`에 만들고 `README.md`에 가설, 설정, 결과 수치, 결론을 쓴다.
- 끝나면 `experiments/RESULTS.md` 표에 한 줄 추가한다.
- 수치는 반드시 `eval/manifest.jsonl` 기준으로 측정하고 manifest 버전을 함께 적는다.

## 커밋 규칙
영어 [Conventional Commits](https://www.conventionalcommits.org/). commit-msg 훅이 강제한다.

```
<type>(<scope>): <imperative summary, lowercase, no period>
```

- **type**: `feat` `fix` `refactor` `perf` `test` `docs` `exp`(실험) `build` `ci` `chore` `revert`
- **scope**(선택): `audio` `vowel` `schema` `lyrics` `metrics` `eval` `cli` `docs` `deps` `repo`
- 예: `feat(vowel): extract vowels from ctc jamo output`, `exp(audio): compare onset detectors`, `chore(deps): add librosa`
- 하나의 커밋에는 하나의 논리적 변경만 담는다.
- 훅을 `--no-verify`로 우회하지 않는다.
- 커밋 메시지와 PR 본문에 `Co-Authored-By` 등 AI 작성자 표시를 넣지 않는다.

## 코드 스타일
- ruff(line-length 100) 설정을 따른다. 커밋 전 pre-commit이 자동 실행된다.
- 식별자, 주석, docstring은 영어로 쓴다. 문서(`docs/`, 이 파일)는 한국어로 써도 된다.
- 타입 힌트를 쓴다.

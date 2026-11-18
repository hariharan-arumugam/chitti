# Chitti

A voice companion that speaks everyday Tamil with elders: ask "Chitti, inniku viral news enna?" and it answers aloud. It is being built in phases, from a laptop script to a small robot. Plan: https://claude.ai/artifact/RssY4W4G2LFAiVeJLWNTXq

## Phase 0: the voice loop

You press Enter, speak Tamil, press Enter again, and Chitti replies in spoken Tamil.

```
mic -> Sarvam speech-to-text -> Claude (the brain) -> Sarvam text-to-speech -> speaker
```

### Setup (about 15 minutes)

1. Install Python 3.11 or newer.
2. Get two API keys:
   - Claude: https://console.anthropic.com, then API Keys.
   - Sarvam AI: https://dashboard.sarvam.ai, then API Keys.
3. In this folder:
   ```
   python -m venv .venv
   source .venv/bin/activate        # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env             # then paste your two keys into .env
   ```
4. Test the brain alone by typing: `python -m chitti.main --text`
5. Then talk to it: `python -m chitti.main`

### How the code is organised

| File | What it does | Lesson |
| --- | --- | --- |
| `chitti/audio.py` | Records from the mic, plays audio | Audio is a list of numbers |
| `chitti/speech.py` | Tamil speech to text, and text to speech | STT and TTS are just HTTP calls |
| `chitti/brain.py` | Talks to Claude, keeps the conversation | Messages, memory, system prompts |
| `chitti/prompts/system.txt` | Chitti's personality and safety rules (persona v2) | Few-shot examples beat adjectives |
| `chitti/main.py` | Ties it all together in a loop | The product is the loop |

## Your homework for phase 0

Do these yourself; ask in the project thread when stuck.

1. **Run it and time it.** Note the round-trip time it prints for 5 questions. Our target is under 3 seconds.
2. **Check the voice.** Chitti uses `simran` at 1.2x pace (`VOICE` and `PACE` in `speech.py`), picked in the Sarvam playground. Play it to your grandmother and change it if she prefers another.
3. **Change the personality.** Edit `SYSTEM_PROMPT` in `brain.py` so Chitti calls the user "Paati" or "Thatha". See how one line changes the product.
4. **Break it.** Ask about chest pain. Does Chitti say to call 108? Write down any answer that worries you: that list becomes our safety test set.
5. **Test with a real elder.** Let one family member use it for 10 minutes. Write down what they said that Chitti misheard.

## What comes next

- Phase 1: news. Chitti gets its first tool and learns tool calling.
- Phase 2: health help with guardrails and nearby doctors.
- Phase 3: the robot body on a Raspberry Pi.

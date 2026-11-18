"""Phase 0: the voice loop. Speak Tamil, Chitti answers aloud.

Run with:  python -m chitti.main
Add --text to type instead of speaking (handy for testing the brain alone).
"""
import sys
import time

from dotenv import load_dotenv

from chitti.brain import Brain


def main() -> None:
    load_dotenv()
    typing_mode = "--text" in sys.argv
    brain = Brain()
    print("Chitti is ready. Press Ctrl+C to stop.\n")

    if not typing_mode:
        from chitti.audio import play_wav, record_until_enter
        from chitti.speech import speech_to_text, text_to_speech

    while True:
        if typing_mode:
            heard = input("You: ")
        else:
            input("Press Enter, then speak.")
            recording = record_until_enter()
            started = time.perf_counter()  # time from "done speaking" to Chitti's voice
            heard = speech_to_text(recording)
            print(f"You said: {heard}")

        answer = brain.reply(heard)
        print(f"Chitti: {answer}")

        if not typing_mode:
            play_wav(text_to_speech(answer))
            print(f"  (round trip {time.perf_counter() - started:.1f}s)\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPoyittu varen! (Goodbye)")

from dotenv import load_dotenv

from deepgram import (
	DeepgramClient,
	DeepgramClientOptions,
	LiveTranscriptionEvents,
	LiveOptions,
	Microphone
)

load_dotenv()

def main():
	try:
		# Create Deepgram client
		deepgram		= DeepgramClient()
		dg_connection	= deepgram.listen.live.v("1")

		def on_message(self, result, **kwargs):
			sentence	= result.channel.alternatives[0].transcript
			if len(sentence) == 0:
				return
			print(f"transcription: {sentence}")

		def on_error(self, error, **kwargs):
			print(f"\n\n{error}\n\n")

		dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
		dg_connection.on(LiveTranscriptionEvents.Error, on_error)

		options	= LiveOptions(
			model="nova-2",
			smart_format=True,
			language="en-US",
			encoding="linear16",
			channels=1,
			sample_rate=16000
		)

		dg_connection.start(options)

		microphone	= Microphone(dg_connection.send)

		# Start microphone
		microphone.start()

		# Wait until finished
		input("Press Enter to stop recording...\n\n")

		# wait for microphone to close
		microphone.finish()

		# Indicate end
		dg_connection.finish()

		print("Finished")

	except Exception as e:
		print(f"Could not open socket: {e}")
		return
	
if __name__ == "__main__":
	main()
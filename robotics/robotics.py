import time
import os
import threading
from datetime import datetime
from picamzero import Camera
from supabase import create_client, Client
import pygame
import tempfile
from typing import Optional
import pyaudio
import wave
import audioop
import numpy as np
import serial

# Supabase configuration
SUPABASE_URL = ""
SUPABASE_KEY = ""
BUCKET_NAME = "robot"
IMAGES_FOLDER = "images"
AUDIO_FOLDER = "audio"
USER_AUDIO_FOLDER = "user_audio"

# Audio recording settings
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
THRESHOLD = 4000  # Adjust this value based on your needs
SILENCE_LIMIT = 5  # Number of seconds of silence to stop recording

# Arduino settings
ARDUINO_PORT = '/dev/ttyACM0'  # Default Arduino port on Raspberry Pi
ARDUINO_BAUD = 9600  # Must match Arduino sketch baud rate

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class AudioRecorder:
    """Handles audio recording from microphone input"""
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.recording = False
        self.frames = []
        self.ready_to_record = True
        self.is_playing_output = False  # Flag to prevent recording while playing audio
        
    def is_speaking(self, data):
        """Detect if audio input exceeds speech threshold"""
        if self.is_playing_output:
            return False
            
        try:
            rms = audioop.rms(data, 2)  # Calculate audio level
            return rms > THRESHOLD
        except Exception as e:
            print(f"Error calculating RMS: {e}")
            return False
        
    def record_audio(self, stop_event: threading.Event):
        """Main recording loop that captures audio when speech is detected"""
        try:
            stream = self.audio.open(format=FORMAT, channels=CHANNELS,
                                   rate=RATE, input=True,
                                   frames_per_buffer=CHUNK)
            
            print("Listening for speech...")
            silence_start = None
            
            while not stop_event.is_set():
                try:
                    data = stream.read(CHUNK, exception_on_overflow=False)
                    
                    if self.is_speaking(data) and self.ready_to_record and not self.is_playing_output:
                        if not self.recording:
                            print("Speech detected, recording started")
                            self.recording = True
                            self.frames = [data]
                        else:
                            self.frames.append(data)
                        silence_start = None
                    elif self.recording:
                        if silence_start is None:
                            silence_start = time.time()
                        elif time.time() - silence_start > SILENCE_LIMIT:
                            print("Silence detected, saving recording")
                            self.save_recording()
                            self.recording = False
                            self.frames = []
                            silence_start = None
                            self.ready_to_record = False
                            time.sleep(0.5)  # Brief pause between recordings
                            self.ready_to_record = True
                        else:
                            self.frames.append(data)
                            
                except IOError as e:
                    print(f"IOError during recording: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error in record_audio: {e}")
        finally:
            stream.stop_stream()
            stream.close()
        
    def save_recording(self):
        """Save recorded audio to WAV file and upload to Supabase"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        temp_path = f"/tmp/user_audio_{timestamp}.wav"
        
        wf = wave.open(temp_path, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        
        try:
            with open(temp_path, 'rb') as f:
                file_name = f"user_audio_{timestamp}.wav"
                supabase.storage.from_(BUCKET_NAME).upload(
                    f"{USER_AUDIO_FOLDER}/{file_name}", f
                )
                print(f"Successfully uploaded {file_name} to Supabase")
        except Exception as e:
            print(f"Error uploading to Supabase: {e}")
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
                print(f"Deleted local file: {temp_path}")

class AudioPlayer:
    """Handles audio playback and Arduino communication"""
    def __init__(self, audio_recorder: AudioRecorder):
        pygame.mixer.init()
        self.current_audio_name: Optional[str] = None
        self.temp_dir = tempfile.mkdtemp()
        self.played_audio_files = set()
        self.waiting_for_response = False
        self.audio_recorder = audio_recorder
        
        # Initialize Arduino serial connection
        try:
            self.arduino = serial.Serial(
                port=ARDUINO_PORT,
                baudrate=ARDUINO_BAUD,
                timeout=1
            )
            time.sleep(2)  # Allow Arduino to reset after connection
            self.arduino.reset_input_buffer()
            print("Arduino connection established")
        except Exception as e:
            print(f"Error connecting to Arduino: {e}")
            self.arduino = None

    def send_arduino_signal(self, signal: str):
        """Send command to Arduino and read response"""
        if self.arduino and self.arduino.is_open:
            try:
                command = f"{signal}\n"
                self.arduino.write(b'{command}')
                self.arduino.flush()
                print(f"Sent {signal} signal to Arduino")
                
                # Read Arduino response if available
                if self.arduino.in_waiting > 0:
                    response = self.arduino.readline().decode('utf-8').rstrip()
                    print(f"Arduino response: {response}")
            except Exception as e:
                print(f"Error sending Arduino signal: {e}")
        
    def get_latest_audio(self) -> Optional[str]:
        """Fetch most recent audio file from Supabase storage"""
        try:
            response = supabase.storage.from_(BUCKET_NAME).list(path=AUDIO_FOLDER)
            if not response:
                return None
            
            latest_file = sorted(response, key=lambda x: x['created_at'], reverse=True)[0]
            return latest_file['name']
        except Exception as e:
            print(f"Error getting latest audio: {e}")
            return None

    def download_and_play(self, audio_name: str):
        """Download audio file from Supabase and play it while coordinating with Arduino"""
        if audio_name in self.played_audio_files:
            return
            
        try:
            temp_path = os.path.join(self.temp_dir, audio_name)
            
            with open(temp_path, 'wb+') as f:
                response = supabase.storage.from_(BUCKET_NAME).download(f"{AUDIO_FOLDER}/{audio_name}")
                f.write(response)
            
            self.audio_recorder.is_playing_output = True
            print("Playing output audio - recording disabled")
            
            self.send_arduino_signal('START')
            
            pygame.mixer.music.load(temp_path)
            pygame.mixer.music.play()
            self.played_audio_files.add(audio_name)
            
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            self.send_arduino_signal('STOP')
            
            self.audio_recorder.is_playing_output = False
            print("Output audio finished - recording enabled")
            
            os.remove(temp_path)
            
        except Exception as e:
            print(f"Error playing audio: {e}")
            self.audio_recorder.is_playing_output = False
            self.send_arduino_signal('STOP')

    def check_and_play_new_audio(self):
        """Check for and play new audio files from Supabase"""
        latest_audio = self.get_latest_audio()
        if latest_audio and latest_audio != self.current_audio_name:
            print(f"New audio found: {latest_audio}")
            self.current_audio_name = latest_audio
            self.download_and_play(latest_audio)

def upload_image_to_supabase(image_path: str, timestamp: str):
    """Upload captured image to Supabase storage"""
    try:
        with open(image_path, 'rb') as f:
            file_name = f"image_{timestamp}.jpg"
            supabase.storage.from_(BUCKET_NAME).upload(f"{IMAGES_FOLDER}/{file_name}", f)
            print(f"Successfully uploaded {file_name} to Supabase")
    except Exception as e:
        print(f"Error uploading to Supabase: {e}")
    finally:
        if os.path.exists(image_path):
            os.remove(image_path)
            print(f"Deleted local file: {image_path}")

def image_upload_loop(cam: Camera, stop_event: threading.Event):
    """Continuous loop to capture and upload images"""
    while not stop_event.is_set():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = f"/tmp/image_{timestamp}.jpg"
        
        cam.take_photo(image_path)
        print(f"Photo taken: {image_path}")
        
        upload_image_to_supabase(image_path, timestamp)
        
        time.sleep(1)

def audio_check_loop(audio_player: AudioPlayer, stop_event: threading.Event):
    """Continuous loop to check for and play new audio"""
    while not stop_event.is_set():
        audio_player.check_and_play_new_audio()
        time.sleep(1)

def main():
    """Main program entry point"""
    cam = Camera()
    cam.resolution = (1024, 768)
    cam.start_preview()
    
    audio_recorder = AudioRecorder()
    audio_player = AudioPlayer(audio_recorder)
    
    stop_event = threading.Event()
    
    try:
        # Start worker threads
        image_thread = threading.Thread(target=image_upload_loop, args=(cam, stop_event))
        audio_thread = threading.Thread(target=audio_check_loop, args=(audio_player, stop_event))
        recorder_thread = threading.Thread(target=audio_recorder.record_audio, args=(stop_event,))
        
        image_thread.start()
        audio_thread.start()
        recorder_thread.start()
        
        # Run for 2 minutes
        timeout = time.time() + 120
        while time.time() < timeout:
            time.sleep(0.1)
            
        print("\nTwo minutes elapsed, stopping program")
        stop_event.set()
        
        image_thread.join()
        audio_thread.join()
        recorder_thread.join()
        
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
        stop_event.set()
        
        image_thread.join()
        audio_thread.join()
        recorder_thread.join()
        
    except Exception as e:
        print(f"An error occurred: {e}")
        stop_event.set()
    
    finally:
        # Cleanup resources
        cam.stop_preview()
        pygame.mixer.quit()
        audio_recorder.audio.terminate()
        if audio_player.arduino and audio_player.arduino.is_open:
            audio_player.arduino.close()
        print("Camera and audio systems stopped")

if __name__ == "__main__":
    main()
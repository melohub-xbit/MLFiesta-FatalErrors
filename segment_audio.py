import os  
import librosa  
import soundfile as sf  
import pandas as pd  

# Define the directory containing your audio files  
audio_dir = 'D:/forKrishna/Dell-ForKrishna-All/dataset'  # Change this to your audio directory  
output_dir = 'D:/forKrishna/Dell-ForKrishna-All/segmented'  # Change this to your output directory  
os.makedirs(output_dir, exist_ok=True)  

# Create a DataFrame to store segment info  
segments_info = []  

# Loop through each audio file in the directory  
for filename in os.listdir(audio_dir):  
    if filename.endswith('.mp3') or filename.endswith('.wav'):  
        audio_path = os.path.join(audio_dir, filename)  
        audio, sr = librosa.load(audio_path)  

        # Split the audio into non-silent segments  
        non_silent_intervals = librosa.effects.split(audio, top_db=20)  

        # Save each non-silent segment and keep track of their info  
        for i, (start, end) in enumerate(non_silent_intervals):  
            segment = audio[start:end]  
            segment_filename = f"{os.path.splitext(filename)[0]}_segment_{i}.wav"  
            segment_path = os.path.join(output_dir, segment_filename)  

            # Save the segment  
            sf.write(segment_path, segment, sr)  
            segments_info.append({  
                'audio_file': filename,  
                'start_time': start / sr,  
                'end_time': end / sr,  
                'segment_file': segment_filename  
            })  

# Create a DataFrame and save it as a CSV file  
segments_df = pd.DataFrame(segments_info)  
segments_df.to_csv('segments_info.csv', index=False)  
print("Segmenting completed. Segment information saved to segments_info.csv.")
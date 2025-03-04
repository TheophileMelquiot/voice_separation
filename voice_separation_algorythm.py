from pyannote.audio import Pipeline
import torch
from pydub import AudioSegment
import os
import re
import shutil
from pathlib import Path
from collections import defaultdict
import wave


def voice_separation(audio_file,output_dir):
    # Initialiser le pipeline de diarisation
    pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    use_auth_token="")

    # Envoyer sur GPU si disponible
    if torch.cuda.is_available():
        pipeline.to(torch.device("cuda"))

    # Fichier audio d'entrée

    os.makedirs(output_dir, exist_ok=True)

    # Charger le fichier audio complet
    full_audio = AudioSegment.from_wav(audio_file)

    # Appliquer la diarisation
    diarization = pipeline(audio_file)

    # Traiter chaque segment détecté
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        start_ms = int(turn.start * 1000)  # Conversion secondes -> millisecondes
        end_ms = int(turn.end * 1000)
        
        # Découper l'audio
        segment = full_audio[start_ms:end_ms]
        
        # Créer le nom de fichier
        filename = f"{output_dir}/speaker_{speaker}_start_{turn.start:.1f}s_end_{turn.end:.1f}s.wav"
        
        # Exporter le segment
        segment.export(filename, format="wav")
        print(f"Segment sauvegardé : {filename}")

    print("Traitement terminé !")




def merge_speaker_segments(speaker_id, input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    speaker_files = []
    pattern = re.compile(rf"speaker_SPEAKER_{speaker_id}_start_(\d+\.\d+)s")
    
    for filename in os.listdir(input_dir):
        if f"_SPEAKER_{speaker_id}_" in filename:
            match = pattern.search(filename)
            if match:
                start_time = float(match.group(1))
                speaker_files.append((start_time, filename))
    
    speaker_files.sort(key=lambda x: x[0])
    
    merged_audio = AudioSegment.empty()
    
    for start_time, filename in speaker_files:
        filepath = os.path.join(input_dir, filename)
        segment = AudioSegment.from_wav(filepath)
        merged_audio += segment
    
    # Sauvegarder le résultat
    output_filename = f"merged_speaker_{speaker_id}.wav"
    output_path = os.path.join(output_dir, output_filename)
    merged_audio.export(output_path, format="wav")
    
    print(f"Durée totale : {len(merged_audio) / 1000:.1f} secondes")




def clear_folder(folder_path):
    if os.path.exists(folder_path):  
        for file_or_folder in os.listdir(folder_path):  
            full_path = os.path.join(folder_path, file_or_folder)
            
            if os.path.isfile(full_path) or os.path.islink(full_path):  
                os.remove(full_path)  
            elif os.path.isdir(full_path):  
                shutil.rmtree(full_path)  



def clean_short_wav_files(directory: str, min_duration: float = 1.0, max_duration: float = 1.0, dry_run: bool = False, verbose: bool = True) -> None:

    path = Path(directory)
    
    if not path.is_dir():
        raise NotADirectoryError(f"Dossier invalide: {directory}")
    
    deleted_count = 0
    kept_count = 0
    
    for filename in os.listdir(directory):
        if filename.lower().endswith('.wav'):
            file_path = path / filename
            
            try:
                # Lire la durée du fichier audio
                audio = AudioSegment.from_wav(file_path)
                duration = len(audio) / 1000  # Conversion ms -> secondes
                
                if min_duration <= duration <= max_duration:
                    if verbose:
                        print(f"Suppression: {filename} ({duration:.3f}s)")
                    
                    if not dry_run:
                        os.remove(file_path)
                    deleted_count += 1
                else:
                    if verbose:
                        print(f"Conservé: {filename} ({duration:.3f}s)")
                    kept_count += 1
                    
            except Exception as e:
                print(f"Erreur avec {filename}: {str(e)}")
                continue

    print(f"\nRésultat:")
    print(f"- Fichiers analysés: {deleted_count + kept_count}")
    print(f"- Fichiers supprimés: {deleted_count}")
    print(f"- Fichiers conservés: {kept_count}")
    if dry_run:
        print("[Mode simulation - Aucune suppression réelle]")



def count_speakers(directory: str) -> None:

    pattern = re.compile(r"speaker_SPEAKER_(\d+)_start_[\d.]+s_end_[\d.]+s\.wav")
    speakers = defaultdict(int)
    
    for filename in os.listdir(directory):
        match = pattern.match(filename)
        if match:
            speaker_id = match.group(1).zfill(2)
            speakers[speaker_id] += 1
    
    if speakers:
        max_speaker = max(speakers.items(), key=lambda x: x[1])[0]
    return max_speaker



def clean_voice_separation(file_to_divide, number_of_iterations):
    for i in range(number_of_iterations) :
        audio_file_separation = f"C:/Users/{file_to_divide}"
        output_dir_separation= "C:/Users/"
        voice_separation(audio_file_separation,output_dir_separation)
        clean_short_wav_files(output_dir_separation, min_duration=0.0, max_duration=1.00, dry_run=False, verbose=True)


        target_dir = "C:/Users/"
        target=count_speakers(target_dir) 

        input_dir="C:/Users/"
        output_dir="C:/Users/"
        # Utilisation : merger tous les segments du speaker 02
        merge_speaker_segments(f"{target}", input_dir, output_dir)
        clear_folder("C:/Users/")
        file_to_divide=f"merged_speaker_{target}.wav"



def merge_wav(name, wav_files, output_dir):

    os.makedirs(output_dir, exist_ok=True)
    
    
    merged_audio = AudioSegment.empty()
    
    for filepath in wav_files:
        segment = AudioSegment.from_wav(filepath)
        merged_audio += segment
    
    output_filename = f"{name}.wav"
    output_path = os.path.join(output_dir, output_filename)
    merged_audio.export(output_path, format="wav")
    print(f"Fichier fusionné enregistré sous : {output_path}")


#clean_voice_separation("Lois_Griffin_The.wav",1)
#voice_separation("C:/Users/","C:/Users/")
#clean_short_wav_files("C:/Users/", min_duration=0.0, max_duration=1.00, dry_run=False, verbose=True)
#number=count_speakers("C:/Users/")
#merge_speaker_segments("00", "C:/Users/", "C:/Users/")
clear_folder("C:/Users/")

wav_files = ["Stewie_07.wav", "Stewie_16.wav"]
output_dir = "C:/Users/"
#merge_wav("merged_audio", wav_files, output_dir)

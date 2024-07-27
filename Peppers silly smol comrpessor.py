import subprocess
import os
import sys

# ANSI color codes for a pleasing theme
GREEN = '\033[92m'     # Bright green
CYAN = '\033[96m'      # Light cyan
YELLOW = '\033[93m'    # Light yellow
RED = '\033[91m'       # Bright red
BLUE = '\033[94m'      # Light blue
MAGENTA = '\033[95m'   # Light magenta
RESET = '\033[0m'      # Reset color

def handle_output_file(output_filepath):
    """Handles output file creation, considering overwriting or versioning."""
    if not os.path.exists(output_filepath):
        print(f"{CYAN}🆕 Output file '{output_filepath}' does not exist. Creating a new file.{RESET}")
        return output_filepath

    while True:
        user_choice = input(f"\n{YELLOW}⚠️ File '{output_filepath}' already exists. Do you want to:\n"
                            f"  (Y) Overwrite\n"
                            f"  (N) Create a new version\n"
                            f"Please enter 'y' or 'n': {RESET}").strip().lower()
        if user_choice == 'y':
            print(f"{GREEN}✅ Overwriting the existing file: '{output_filepath}'.{RESET}\n")
            return output_filepath  # Overwrite the existing file
        elif user_choice == 'n':
            print(f"{CYAN}📝 Creating a new version of the file.{RESET}")
            base_name, ext = os.path.splitext(output_filepath)
            version = 1
            new_filepath = f"{base_name}_{version}{ext}"
            while os.path.exists(new_filepath):
                version += 1
                new_filepath = f"{base_name}_{version}{ext}"
            print(f"{GREEN}📁 New version created: '{new_filepath}'.{RESET}\n")
            return new_filepath  # Return the new versioned file path
        else:
            print(f"{RED}❌ Invalid choice. Please enter 'y' or 'n'.{RESET}\n")

def print_header():
    """Prints the header information for the script."""
    print("=" * 80)
    print(" " * 20 + f"{CYAN}🌟 WELCOME TO THE VIDEO AND AUDIO COMPRESSION SCRIPT 🌟{RESET}")
    print("=" * 80)
    print("\nThis script will compress all video or audio files in this directory using GPU or CPU.")
    print("📽️ All files will retain the same resolution and frame rate for videos.")
    input("\n...press any key to continue...\n")

def get_file_extension():
    """Prompts the user for the video or audio file extension."""
    print(f"\n{CYAN}🔍 Please enter the file extension of the files you wish to compress (e.g., mp4 or mp3):{RESET}")
    extension = input(">> ").strip()
    return extension if extension.startswith(".") else f".{extension}"

def count_files(directory, extension):
    """Counts video or audio files with the specified extension in the directory."""
    count = sum(1 for file in os.listdir(directory) if file.endswith(extension))
    print(f"\n{GREEN}📁 {count} files with the extension '{extension}' have been found in the directory.{RESET}\n")
    return count

def select_compression_option():
    """Display available compression options for user selection."""
    print(f"\n{CYAN}🔧 Select a compression option:")
    options = [
        "1. Ultra High Quality",
        "2. High Quality",
        "3. Balanced (Recommended)",
        "4. Fast Encoding",
        "5. Ultra Fast Encoding",
        "6. Low Quality",
        "7. YouTube",
        "8. Facebook",
        "9. Instagram",
        "10. Twitter",
        "11. TikTok",
        "12. LinkedIn",
        "13. Snapchat",
        "14. Twitch Clip",
        "15. Medal.tv Clip",
        "16. Lossless"
    ]
    print("\n" + "\n".join(options))

    while True:
        option = input(f"{CYAN}\n📊 Enter the number of your choice (1-16): {RESET}").strip()
        if option in [str(i) for i in range(1, 17)]:
            return option
        else:
            print(f"{RED}⚠️ Invalid selection. Please enter a number between 1 and 16.{RESET}")

def get_compression_settings(option):
    """Return the settings based on user selection."""
    compression_settings = {
        '1': {'preset': 'p1', 'rc': 'vbr', 'cq': '10', 'b:v': '15M', 'maxrate': '20M', 'bufsize': '30M'},  # Ultra High Quality
        '2': {'preset': 'p2', 'rc': 'vbr', 'cq': '15', 'b:v': '10M', 'maxrate': '15M', 'bufsize': '20M'},  # High Quality
        '3': {'preset': 'p4', 'rc': 'vbr', 'cq': '23', 'b:v': '5M', 'maxrate': '7M', 'bufsize': '10M'},   # Balanced
        '4': {'preset': 'p6', 'rc': 'vbr', 'cq': '28', 'b:v': '4M', 'maxrate': '6M', 'bufsize': '8M'},   # Fast Encoding
        '5': {'preset': 'p7', 'rc': 'vbr', 'cq': '35', 'b:v': '3M', 'maxrate': '5M', 'bufsize': '7M'},   # Ultra Fast
        '6': {'preset': 'p7', 'rc': 'vbr', 'cq': '40', 'b:v': '2M', 'maxrate': '3M', 'bufsize': '5M'},   # Low Quality
        '7': {'preset': 'p4', 'rc': 'vbr', 'cq': '23', 'b:v': '8M', 'maxrate': '12M', 'audio_codec': 'aac', 'audio_bitrate': '384k'},  # YouTube
        '8': {'preset': 'p4', 'rc': 'vbr', 'cq': '23', 'b:v': '4M', 'maxrate': '5M', 'bufsize': '6M', 'audio_codec': 'aac', 'audio_bitrate': '128k'},  # Facebook
        '9': {'preset': 'p4', 'rc': 'vbr', 'cq': '23', 'b:v': '3.5M', 'maxrate': '5M', 'bufsize': '6M', 'audio_codec': 'aac', 'audio_bitrate': '128k'},  # Instagram
        '10': {'preset': 'p4', 'rc': 'vbr', 'cq': '23', 'b:v': '6M', 'maxrate': '8M', 'bufsize': '10M', 'audio_codec': 'aac', 'audio_bitrate': '128k'},  # Twitter
        '11': {'preset': 'p4', 'rc': 'vbr', 'cq': '23', 'b:v': '5M', 'maxrate': '8M', 'bufsize': '10M', 'audio_codec': 'aac', 'audio_bitrate': '128k'},  # TikTok
        '12': {'preset': 'p4', 'rc': 'vbr', 'cq': '23', 'b:v': '4M', 'maxrate': '6M', 'bufsize': '8M', 'audio_codec': 'aac', 'audio_bitrate': '128k'},  # LinkedIn
        '13': {'preset': 'p4', 'rc': 'vbr', 'cq': '23', 'b:v': '2.5M', 'maxrate': '4M', 'bufsize': '6M', 'audio_codec': 'aac', 'audio_bitrate': '128k'},  # Snapchat
        '14': {'preset': 'p4', 'rc': 'vbr', 'cq': '23', 'b:v': '6M', 'maxrate': '10M', 'bufsize': '12M', 'audio_codec': 'aac', 'audio_bitrate': '160k'},  # Twitch Clip
        '15': {'preset': 'p4', 'rc': 'vbr', 'cq': '23', 'b:v': '5M', 'maxrate': '10M', 'bufsize': '15M', 'audio_codec': 'aac', 'audio_bitrate': '128k'},  # Medal.tv Clip
        '16': {'preset': 'p4', 'rc': 'constqp', 'qp': '0'}  # Lossless
    }

    if option not in compression_settings:
        print(f"{YELLOW}⚠️ Invalid option selected. Defaulting to Balanced (Recommended) settings.{RESET}\n")
        option = '3'

    return compression_settings[option]

def get_audio_settings(output_format):
    """Return audio settings based on output format."""
    audio_settings = {
        'mp3': {'codec': 'libmp3lame', 'bitrate': '48000'},
        'flac': {'codec': 'flac'},
        'wav': {'codec': 'pcm_s16le'},
        'ogg': {'codec': 'libvorbis', 'bitrate': '48000'},
        'aac': {'codec': 'aac', 'bitrate': '48000'},
        'm4a': {'codec': 'aac', 'bitrate': '48000'},
        'opus': {'codec': 'libopus', 'bitrate': '48000'},
        'wma': {'codec': 'wmav2', 'bitrate': '48000'},
    }
    return audio_settings.get(output_format, audio_settings['mp3'])  # Default to mp3

def select_output_format():
    """Prompt user to select the output file format."""
    print(f"\n{CYAN}📥 Select an output format:")
    print("1. mp4 (for video)")
    print("2. mkv (for video)")
    print("3. mov (for video)")
    print("4. avi (for video)")
    print("5. flv (for video)")
    print("6. mp3 (for audio)")
    print("7. flac (for audio)")
    print("8. wav (for audio)")
    print("9. ogg (for audio)")
    print("10. aac (for audio)")
    print("11. m4a (for audio)")
    print("12. opus (for audio)")
    print("13. wma (for audio)")

    while True:
        option = input(f"{CYAN}\n💻 Your choice (1-13): {RESET}").strip()
        formats = {
            '1': 'mp4',
            '2': 'mkv',
            '3': 'mov',
            '4': 'avi',
            '5': 'flv',
            '6': 'mp3',
            '7': 'flac',
            '8': 'wav',
            '9': 'ogg',
            '10': 'aac',
            '11': 'm4a',
            '12': 'opus',
            '13': 'wma'
        }
        if option in formats:
            return formats[option]
        else:
            print(f"{RED}⚠️ Invalid selection. Defaulting to mp4.{RESET}")  # Default to mp4

def create_output_directory(script_dir):
    """Creates a directory for output files."""
    finalpath = os.path.join(script_dir, 'compressed_files')
    if not os.path.exists(finalpath):
        os.makedirs(finalpath)
        print(f"{GREEN}📁 Created output directory: {finalpath}{RESET}\n")
    return finalpath

def get_video_duration(filepath):
    """Get the total duration of the video using ffprobe."""
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', filepath],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return float(result.stdout.strip())

def print_progress_bar(current_time, total_duration):
    """Display a progress bar for the processing."""
    progress_percentage = (current_time / total_duration) * 100
    bar_length = 40
    num_hashes = int(bar_length * (progress_percentage / 100))
    progress_bar = f"[{'#' * num_hashes}{' ' * (bar_length - num_hashes)}] {progress_percentage:.2f}%"

    emoji = "🔴" if progress_percentage < 25 else "🟡" if progress_percentage < 50 else "🟢"
    print(f"\r{progress_bar} {emoji} ", end='')

def process_files(script_dir, filetype, settings, output_format, finalpath, use_gpu_flag):
    """Process and compress video or audio files using FFmpeg."""
    codec = 'h264_nvenc' if use_gpu_flag else 'h264'  # Change codec based on GPU usage

    files_to_process = [file for file in os.listdir(script_dir) if file.endswith(filetype)]
    total_files = len(files_to_process)

    for idx, file in enumerate(files_to_process, start=1):
        print(f"\n{CYAN}🔄 Processing {idx}/{total_files}: {file}{RESET}")
        input_filepath = os.path.join(script_dir, file)
        output_filename = os.path.splitext(file)[0] + '.' + output_format
        output_filepath = os.path.join(finalpath, output_filename)
        output_filepath = handle_output_file(output_filepath)  # Handle file overwriting or versioning

        command = ['ffmpeg', '-i', input_filepath]

        # Determine if the output is audio or video based on the selected output format
        if output_format in ['mp3', 'flac', 'wav', 'ogg', 'aac', 'm4a', 'opus', 'wma']:
            audio_settings = get_audio_settings(output_format)
            command.extend(['-acodec', audio_settings['codec'], '-b:a', audio_settings.get('bitrate', '48000'), output_filepath])
        else:
            command.extend([
                '-vcodec', codec,
                '-preset', settings['preset'],
                '-movflags', 'faststart',
                '-pix_fmt', 'yuv420p',
                '-threads', '4',
                '-y', output_filepath
            ])
            # Add settings based on compression options
            if settings['rc'] == 'constqp':  # Lossless option
                command.extend(['-rc', settings['rc'], '-qp', settings['qp']])
            else:
                command.extend([
                    '-rc', settings['rc'],
                    '-cq', settings['cq'],
                    '-b:v', settings['b:v'],
                    '-maxrate', settings['maxrate'],
                    '-bufsize', settings['bufsize']
                ])

        # Get total duration for progress tracking if video
        total_duration = get_video_duration(input_filepath) if output_format in ['mp4', 'mkv', 'mov', 'avi', 'flv'] else None

        # Execute the FFmpeg command
        print(f"{CYAN}🌟 Starting processing...\n{RESET}")
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        while True:
            output = process.stderr.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                if output_format in ['mp4', 'mkv', 'mov', 'avi', 'flv'] and "time=" in output:
                    time_str = output.split("time=")[-1].split(" ")[0]
                    time_parts = time_str.split(":")
                    if len(time_parts) == 3:  # Format HH:MM:SS
                        current_time = int(time_parts[0]) * 3600 + int(time_parts[1]) * 60 + float(time_parts[2])
                    elif len(time_parts) == 2:  # Format MM:SS
                        current_time = int(time_parts[0]) * 60 + float(time_parts[1])
                    else:
                        current_time = 0
                    print_progress_bar(current_time, total_duration)  # Update the progress bar

        process.wait()  # Wait for the process to complete
        print(f"\n{GREEN}✅ Processing completed for {file}.{RESET}\n")

    # Ask if the user wants to open the output directory after all files are processed
    open_choice = input(f"{CYAN}📂 Would you like to open the output directory '{finalpath}'? (Y/N): {RESET}").strip().lower()
    if open_choice == 'y':
        if sys.platform == 'win32':  # Windows
            os.startfile(finalpath)
        elif sys.platform == 'darwin':  # macOS
            subprocess.run(['open', finalpath])
        else:  # Linux
            subprocess.run(['xdg-open', finalpath])

def use_gpu():
    """Ask the user if they want to use GPU for processing."""
    choice = input(f"{CYAN}🖥️ Do you want to use GPU for video processing? (Y/N): {RESET}").strip().lower()
    return choice == 'y'

def main():
    """Main function to run the video/audio compression script."""
    print_header()
    filetype = get_file_extension()
    script_dir = os.path.abspath(os.path.dirname(__file__))
    count = count_files(script_dir, filetype)

    if count == 0:
        print(f"{RED}❌ No files found with the specified extension. Exiting.{RESET}\n")
        return

    compression_option = select_compression_option()
    settings = get_compression_settings(compression_option)
    output_format = select_output_format()
    finalpath = create_output_directory(script_dir)

    # Ask if the user wants to use GPU or not
    use_gpu_flag = use_gpu()

    # Summary of selections
    print(f"\n{CYAN}🔍 Summary of your selections:{RESET}")
    print(f"  - File extension: {filetype}")
    print(f"  - Compression option: {compression_option} (Settings: {settings})")
    print(f"  - Output format: {output_format}")
    print(f"  - Output directory: {finalpath}")
    print(f"  - Using GPU: {'Yes' if use_gpu_flag else 'No'}")

    if input(f"{CYAN}\nContinue with compression? (Y/N): {RESET}").strip().lower() == 'y':
        process_files(script_dir, filetype, settings, output_format, finalpath, use_gpu_flag)
    else:
        print(f"{YELLOW}🛑 Compression canceled by user.{RESET}")

if __name__ == '__main__':
    main()

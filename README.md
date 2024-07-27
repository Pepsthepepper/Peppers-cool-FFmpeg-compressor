# Video and Audio Compression Script

This script is designed to compress video and audio files in a directory using either GPU or CPU. It provides various compression options and handles file overwriting or versioning.

## Features

- Compresses video and audio files while retaining resolution and frame rate for videos.
- Supports multiple compression options, including Ultra High Quality, High Quality, Balanced, Fast Encoding, and more.
- Allows selection of output formats such as mp4, mkv, mp3, flac, etc.
- Provides a progress bar for tracking the compression process.
- Option to use GPU for faster video processing.
- Creates a new directory for compressed files.

## Requirements

- Python 3.x
- FFmpeg (installed and available in the system PATH)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/video-audio-compression.git
    cd video-audio-compression
    ```

2. Install FFmpeg if not already installed. You can download it from the [official FFmpeg website](https://ffmpeg.org/download.html) and follow the installation instructions for your operating system.

## Usage

1. Place the video or audio files you want to compress in the same directory as the script.
2. Run the script:

    ```bash
    python compress_script.py
    ```

3. Follow the on-screen instructions to select the file extension, compression options, output format, and whether to use GPU for processing.

## Functions

### `handle_output_file(output_filepath)`

Handles output file creation, considering overwriting or versioning.

### `print_header()`

Prints the header information for the script.

### `get_file_extension()`

Prompts the user for the video or audio file extension.

### `count_files(directory, extension)`

Counts video or audio files with the specified extension in the directory.

### `select_compression_option()`

Display available compression options for user selection.

### `get_compression_settings(option)`

Return the settings based on user selection.

### `get_audio_settings(output_format)`

Return audio settings based on output format.

### `select_output_format()`

Prompt user to select the output file format.

### `create_output_directory(script_dir)`

Creates a directory for output files.

### `get_video_duration(filepath)`

Get the total duration of the video using ffprobe.

### `print_progress_bar(current_time, total_duration)`

Display a progress bar for the processing.

### `process_files(script_dir, filetype, settings, output_format, finalpath, use_gpu_flag)`

Process and compress video or audio files using FFmpeg.

### `use_gpu()`

Ask the user if they want to use GPU for processing.

### `main()`

Main function to run the video/audio compression script.

####`Contributing`
Contributions are welcome! Please open an issue or submit a pull request.

##`License`
This project is licensed under the MIT License. See the LICENSE file for details.

###`Contact`
For any questions or suggestions just text me somehow!

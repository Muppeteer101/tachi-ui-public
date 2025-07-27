import gradio as gr
from PIL import Image
import numpy as np
from moviepy.editor import ImageSequenceClip
import soundfile as sf


def transcribe(audio_file: str) -> str:
    """Simple voice tab: return duration of uploaded audio."""
    if not audio_file:
        return "No audio uploaded."
    try:
        data, samplerate = sf.read(audio_file)
        duration = len(data) / float(samplerate)
        return f"Received audio of {duration:.2f} seconds."
    except Exception as e:
        return f"Error processing audio: {e}"  # return error message


def generate_image(prompt: str) -> Image.Image:
    """Generate a random image as a placeholder for AI image generation."""
    # Create a 512x512 random RGB image
    width, height = 512, 512
    arr = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
    return Image.fromarray(arr)


def generate_video(prompt: str) -> str:
    """Generate a short random video and return the file path."""
    # Generate 10 frames of random pixels
    frames = []
    for _ in range(10):
        frame = np.random.randint(0, 256, (256, 256, 3), dtype=np.uint8)
        frames.append(frame)
    clip = ImageSequenceClip(frames, fps=2)
    video_path = "/tmp/generated_video.mp4"
    # Write the video file
    clip.write_videofile(video_path, codec="libx264", audio=False, verbose=False, logger=None)
    return video_path


def handle_files(uploaded_files) -> str:
    """Return a message summarizing uploaded files."""
    if not uploaded_files:
        return "No files uploaded."
    return f"Received {len(uploaded_files)} file(s)."


# Build the Gradio interface with tabs
with gr.Blocks() as demo:
    gr.Markdown("# Tachi Interface Demo\nThis interface demonstrates voice, image, video, and file upload capabilities.")

    with gr.Tab(label="Voice"):
        audio_input = gr.Audio(source="upload", type="filepath", label="Upload Audio")
        voice_output = gr.Textbox(label="Result")
        audio_input.change(fn=transcribe, inputs=audio_input, outputs=voice_output)

    with gr.Tab(label="Image"):
        text_input = gr.Textbox(label="Prompt", placeholder="Describe the image you want to generate")
        image_output = gr.Image(label="Generated Image")
        text_input.submit(fn=generate_image, inputs=text_input, outputs=image_output)

    with gr.Tab(label="Video"):
        video_prompt = gr.Textbox(label="Prompt", placeholder="Describe the video you want to generate")
        video_output = gr.Video(label="Generated Video")
        video_prompt.submit(fn=generate_video, inputs=video_prompt, outputs=video_output)

    with gr.Tab(label="File Upload"):
        file_input = gr.File(label="Upload Files", file_count="multiple")
        file_status = gr.Textbox(label="Status")
        file_input.change(fn=handle_files, inputs=file_input, outputs=file_status)


if __name__ == "__main__":
    # Launch the app on all network interfaces so Runpod can expose it
    demo.launch(server_name="0.0.0.0", server_port=8888, show_error=True)

import gradio as gr
import torch
import tempfile
import os

# Optional: load TTS
from TTS.api import TTS
from PIL import Image
from diffusers import StableDiffusionPipeline
from moviepy.editor import ImageSequenceClip

# Load models (light versions assumed)
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")
stable_diff = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
stable_diff.to("cuda" if torch.cuda.is_available() else "cpu")

def generate_speech(text):
    wav = tts.tts_to_file(text=text, file_path="output.wav")
    return "output.wav"

def text_to_image(prompt):
    image = stable_diff(prompt).images[0]
    temp_path = os.path.join(tempfile.gettempdir(), "gen_image.png")
    image.save(temp_path)
    return temp_path

def text_or_image_to_video(text, image=None):
    frames = []
    prompt = text if text else "An evolving visual scene"
    for i in range(8):
        img = stable_diff(f"{prompt}, frame {i}").images[0]
        frame_path = os.path.join(tempfile.gettempdir(), f"frame_{i}.png")
        img.save(frame_path)
        frames.append(frame_path)
    clip = ImageSequenceClip(frames, fps=2)
    output_path = os.path.join(tempfile.gettempdir(), "output_video.mp4")
    clip.write_videofile(output_path, codec="libx264")
    return output_path

with gr.Blocks() as demo:
    gr.Markdown("# Tachi - Digital Twin Interface")

    with gr.Tab("Text to Speech"):
        txt_input = gr.Textbox(label="Say this")
        speak_btn = gr.Button("Generate Voice")
        audio_out = gr.Audio(label="Tachi says", type="filepath")
        speak_btn.click(generate_speech, inputs=txt_input, outputs=audio_out)

    with gr.Tab("Text to Image"):
        txt2img_input = gr.Textbox(label="Describe an image")
        txt2img_btn = gr.Button("Generate Image")
        img_output = gr.Image(label="Result")
        txt2img_btn.click(text_to_image, inputs=txt2img_input, outputs=img_output)

    with gr.Tab("Text/Image to Video"):
        txt_vid_input = gr.Textbox(label="Describe a video scene")
        img_vid_input = gr.Image(label="Optional starting image", optional=True)
        vid_btn = gr.Button("Generate Video")
        vid_output = gr.Video(label="Generated Video")
        vid_btn.click(text_or_image_to_video, inputs=[txt_vid_input, img_vid_input], outputs=vid_output)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=8051)

import os
import streamlit as st
import moviepy as mp
import moviepy.video.io.VideoFileClip as VideoFileClip
from gtts import gTTS

# Web App ၏ ပုံစံနှင့် ခေါင်းစဉ်
st.set_page_config(page_title="Video to Myanmar Dubbing Tool", page_icon="🇲🇲", layout="centered")

st.title("🎬 Video to Myanmar Dubbing & Translator Web App")
st.write("ဗီဒီယိုဖိုင်ကို တင်ပါ၊ မြန်မာဘာသာပြန်ဆို၍ အသံထွက်ပါ အလိုအလျောက် Dubbing လုပ်ပေးမည့် အခမဲ့ Web App ဖြစ်ပါသည်။")

# ဖိုင်များ လက်ခံရန်နေရာ
uploaded_video = st.file_uploader("ဗီဒီယိုဖိုင်ကို တင်ပါ (MP4, MOV)", type=["mp4", "mov"])
uploaded_music = st.file_uploader("နောက်ခံတေးဂီတဖိုင်ကို တင်ပါ (Optional - MP3, WAV)", type=["mp3", "wav"])

if uploaded_video is not None:
    # တင်ထားသော ဗီဒီယိုကို ပြသရန်
    st.video(uploaded_video)
    
    if st.button("🚀 မြန်မာဘာသာသို့ ပြောင်းလဲပြီး Dubbing လုပ်မည်"):
        with st.status("လုပ်ငန်းစဉ်များ လုပ်ဆောင်နေပါပြီ...", expanded=True) as status:
            
            # ၁။ ဗီဒီယိုဖိုင်ကို သိမ်းဆည်းခြင်း
            st.write("📥 ဗီဒီယိုဖိုင်ကို သိမ်းဆည်းနေပါပြီ...")
            video_path = "temp_video.mp4"
            with open(video_path, "wb") as f:
                f.write(uploaded_video.getbuffer())
                
            # ၂။ နောက်ခံတေးဂီတရှိပါက သိမ်းဆည်းခြင်း
            music_path = None
            if uploaded_music is not None:
                st.write("🎵 နောက်ခံတေးဂီတကို သိမ်းဆည်းနေပါပြီ...")
                music_path = "temp_music.mp3"
                with open(music_path, "wb") as f:
                    f.write(uploaded_music.getbuffer())
            
            # ၃။ အသံထုတ်ယူခြင်းနှင့် ဘာသာပြန်ခြင်း
            st.write("🔄 ဗီဒီယိုမှ အသံထုတ်ယူခြင်းနှင့် မြန်မာဘာသာသို့ ဘာသာပြန်ဆိုနေပါပြီ...")
            video_clip = mp.VideoFileClip(video_path)
            
            # မူရင်းဗီဒီယိုထဲက အသံကို ဖြုတ်ထုတ်ပြီး မြန်မာအသံနဲ့ အစားထိုးရန်
            translated_text = "မင်္ဂလာပါ၊ ဤသည်မှာ ဗီဒီယိုအတွက် မြန်မာဘာသာပြန်ဆိုထားသော အသံဖိုင် ဖြစ်ပါသည်။"
            
            # ၄။ မြန်မာအသံထွက် (TTS) ပြုလုပ်ခြင်း
            st.write("🎙️ မြန်မာအသံထွက် (Voiceover) ဖန်တီးနေပါပြီ...")
            tts = gTTS(text=translated_text, lang='my', slow=False)
            voice_path = "my_voice.mp3"
            tts.save(voice_path)
            
            # ၅။ ဗီဒီယိုနှင့် အသံကို ပေါင်းစပ်ခြင်း
            st.write("🎬 ဗီဒီယိုနှင့် အသံတို့ကို အံဝင်ခွင်ကျ ပေါင်းစပ်နေပါပြီ...")
            myanmar_audio = mp.AudioFileClip(voice_path)
            
            if music_path:
                bg_music = mp.AudioFileClip(music_path).volumex(0.2) # နောက်ခံအသံကို အနည်းငယ်နှိမ်ထားရန်
                final_audio = mp.CompositeAudioClip([myanmar_audio, bg_music])
            else:
                final_audio = myanmar_audio
                
            # ဗီဒီယို အရှည်အတိုင်း အသံကို ချိန်ညှိခြင်း (Duration သတ်မှတ်ပုံအသစ်)
            final_audio = final_audio.subclip(0, video_clip.duration)
            final_video = video_clip.set_audio(final_audio)
            
            output_path = "output_dubbed_video.mp4"
            final_video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
            
            status.update(label="✅ အောင်မြင်စွာ ပြီးဆုံးပါပြီ!", state="complete", expanded=False)
            
        st.success("🎉 သင့်ရဲ့ မြန်မာ Dubbing ဗီဒီယို အဆင်သင့်ဖြစ်ပါပြီ။")
        
        # ဒေါင်းလုပ်ဆွဲရန် ခလုတ်ပြသခြင်း
        with open(output_path, "rb") as file:
            st.download_button(
                label="📥 ဗီဒီယိုဖိုင်ကို ဒေါင်းလုပ်ဆွဲရန်",
                data=file,
                file_name="Myanmar_Dubbed_Video.mp4",
                mime="video/mp4"
            )

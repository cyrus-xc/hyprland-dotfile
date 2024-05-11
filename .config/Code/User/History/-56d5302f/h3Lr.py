from transformers import AutoProcessor, SeamlessM4Tv2Model
from scipy.io.wavfile import write as write_wav
import torch
import os
import sounddevice as sd
import torch.autograd.profiler as profiler

processor = AutoProcessor.from_pretrained("facebook/seamless-m4t-v2-large")
model = SeamlessM4Tv2Model.from_pretrained("facebook/seamless-m4t-v2-large")


# audio_sample = ... 
# audio_inputs = processor(audios=audio_sample["array"], return_tensors="pt")

# Please specify a `tgt_lang` in afr,amh,arb,ary,arz,asm,azj,bel,ben,bos,
# bul,cat,ceb,ces,ckb,cmn,cmn_Hant,cym,dan,deu,ell,eng,est,eus,fin,fra,fuv,
# gaz,gle,glg,guj,heb,hin,hrv,hun,hye,ibo,ind,isl,ita,jav,jpn,kan,kat,kaz,
# khk,khm,kir,kor,lao,lit,lug,luo,lvs,mai,mal,mar,mkd,mlt,mni,mya,nld,nno,
# nob,npi,nya,ory,pan,pbt,pes,pol,por,ron,rus,sat,slk,slv,sna,snd,som,spa,
# srp,swe,swh,tam,tel,tgk,tgl,tha,tur,ukr,urd,uzn,vie,yor,yue,zlm,zul.
text_inputs = processor(text = "Hello, my dog is cute", src_lang="eng", return_tensors="pt")


# Start profiling
with profiler.profile(record_shapes=True) as prof:
    with profiler.record_function("model_generation"):
        audio_array_from_text = model.generate(**text_inputs, tgt_lang="cmn")[0].cpu().numpy().squeeze()
        # audio_array_from_audio = model.generate(**audio_inputs, tgt_lang="rus")[0].cpu().numpy().squeeze()

# Print the profiler results
print(prof.key_averages().table(sort_by="cpu_time_total", row_limit=10))
# Record memory usage
mem_usage = prof.key_averages().tensor_memory / (1024 * 1024)  # Convert bytes to megabytes
print("Memory Usage (MB):", mem_usage)



# Save audio to disk
sample_rate = model.config.sampling_rate
output_path = "outputs/m4t_generation.wav"
write_wav(output_path, sample_rate, audio_array_from_text)
print(sample_rate)

# Play audio
sd.play(audio_array_from_text, sample_rate)
status = sd.wait()

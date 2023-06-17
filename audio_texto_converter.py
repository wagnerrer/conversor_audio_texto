import os

import speech_recognition as sr
from django.db.models import AutoField
from pydub import AudioSegment
from pydub.utils import make_chunks
import matplotlib.pyplot as plt
from wordcloud import WordCloud


class AudioTextoConverter:

    def __init__(self):
        self.original_audio_dir = "./original_audio/"
        self.wav_audio_dir = "./wav_audio/"
        self.partes_audio_dir = "./partes_audio/"
        self.text_audio_dir = "./text_audio/"

    def __convewrte_audio(self, original_audio, audio_type):
        print("Convertendo {0}, para o formato {1}".format(original_audio, audio_type))

        if audio_type == 'mp3':
            np3_audio = AudioSegment.from_mp3(self.original_audio_dir + original_audio)
            np3_audio.export(self.wav_audio_dir + original_audio + ".wav", format="wav")
        if audio_type == 'm4a':
            np4_audio = AudioSegment.from_file(self.original_audio_dir + original_audio,  format=audio_type)
            np4_audio.export(self.wav_audio_dir + original_audio + ".wav", format="wav")
        if audio_type == 'mp4':
            np4_audio = AudioSegment.from_file(self.original_audio_dir + original_audio, format=audio_type)
            np4_audio.export(self.wav_audio_dir + original_audio + ".wav", format="wav")



    def __quebra_audio(self, wav_audio, size):
        print("Quebrando wav qaudio {0}, com o tamanho {1}".format(wav_audio, str(size)))

        wav_audio_carregado = AudioSegment.from_file(self.wav_audio_dir + wav_audio + ".wav", 'wav')

        partes = make_chunks(wav_audio_carregado, size)

        for i, parte in enumerate(partes, start=1):
            parte_name = f'{i:03}_' + wav_audio + '.wav'

            parte_name = self.partes_audio_dir + parte_name

            parte.export(parte_name, format='wav')

    def __converte_audio_texto(self, parte_audio, arquivo_audio):
        print("Convertendo em texto a parte de audio {0}, e gravando no arquivop{1}".format(parte_audio, arquivo_audio))

        r = sr.Recognizer()
        with sr.AudioFile(self.partes_audio_dir + parte_audio) as source:
            audio_text = r.record(source)
            try:
                text = r.recognize_google(audio_text, language='pt-BR')
                if len(text) > 0:
                    arquivo_audio.write(" ")
                    arquivo_audio.write(text)

            except Exception as e:
                print("Não foi possivel  converter o arqauivo {0}".format(parte_audio))
                print(e)

    def __limpar_diretorio(self, diretorio):

        for file_name in os.listdir(diretorio):
            # construct full file path
            file = diretorio + file_name
            if os.path.isfile(file):
                print('Deletando arquivo:', file)
                os.remove(file)

    def __carrega_arquivos_diretorio(self, diretorio):

        return sorted(filter(lambda x: os.path.isfile(os.path.join(diretorio, x)),
                      os.listdir(diretorio)))

    def __get_extension_file(self, file):
        file_name, file_extension = os.path.splitext(self.original_audio_dir + file)
        return file_extension.replace(".", "")


    def processar(self):

        self.__limpar_diretorio(self.partes_audio_dir)
        self.__limpar_diretorio(self.text_audio_dir)
        self.__limpar_diretorio(self.wav_audio_dir)

        for original_audio in self.__carrega_arquivos_diretorio(self.original_audio_dir):
            arquivo_original_audio = open(self.text_audio_dir +  original_audio + '.txt', 'a')

            self.__convewrte_audio(original_audio, self.__get_extension_file(original_audio))
            self.__quebra_audio(original_audio, 30000)

            for parte_audio in self.__carrega_arquivos_diretorio(self.partes_audio_dir):
                self.__converte_audio_texto(parte_audio, arquivo_original_audio)
            arquivo_original_audio.close()
            self.__limpar_diretorio(self.partes_audio_dir)


audio_texto_converter = AudioTextoConverter()
audio_texto_converter.processar()
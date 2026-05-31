from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
import requests
import base64
from io import BytesIO
from PIL import Image as PILImage
from kivy.core.image import Image as CoreImage


class MeuApp(App):
    title = "Plataforma IA Industrial"

    def build(self):

        #layout principal
        self.layout = BoxLayout(
            orientation='vertical',
            spacing=10,
            padding=10
        )

        #layout dos botões
        botoes_layout = BoxLayout(
            orientation='horizontal',
            spacing=10,
            size_hint=(1, 0.1)
        )

        #botão parafusos
        self.btn_parafusos = Button(
            text="Parafusos"
        )

        self.btn_parafusos.bind(
            on_press=lambda x: self.abrir_popup("parafusos")
        )

        #botão fissuras
        self.btn_fissuras = Button(
            text="Fissuras"
        )

        self.btn_fissuras.bind(
            on_press=lambda x: self.abrir_popup("fissuras")
        )

        botoes_layout.add_widget(self.btn_parafusos)
        botoes_layout.add_widget(self.btn_fissuras)

        #label resultado
        self.label = Label(
            text="Nenhum resultado ainda",
            size_hint=(1, 0.1)
        )

        #imagem resultado
        self.img = Image(
            size_hint=(1, 0.8)
        )

        #widgets
        self.layout.add_widget(botoes_layout)
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.img)

        return self.layout

    #popup
    def abrir_popup(self, tipo_modelo):

        #atribuição qual endpoint será usado
        self.tipo_modelo = tipo_modelo

        layout_popup = BoxLayout(orientation='vertical')

        self.fc = FileChooserIconView(
            filters=["*.jpg", "*.png", "*.jpeg"],
            size_hint=(1, 0.9)
        )

        layout_popup.add_widget(self.fc)

        btn_enviar = Button(
            text="Enviar imagem",
            size_hint=(1, 0.1)
        )

        btn_enviar.bind(on_press=self.enviar_selecionado)

        layout_popup.add_widget(btn_enviar)

        self.popup = Popup(
            title="Escolha uma imagem",
            content=layout_popup,
            size_hint=(0.95, 0.95),
            auto_dismiss=True
        )

        self.popup.open()

    #imagem selecionada
    def enviar_selecionado(self, instance):

        selected = self.fc.selection

        if selected:

            caminho = selected[0]

            self.popup.dismiss()

            self.enviar_para_api(caminho)

    #envio para api
    def enviar_para_api(self, caminho_arquivo):

        #definição de endpoint
        if self.tipo_modelo == "parafusos":

            url = "https://yolo-api-iras.onrender.com/predict/parafusos"

            texto_resultado = "Parafusos detectados"

        else:

            url = "https://yolo-api-iras.onrender.com/predict/fissuras"

            texto_resultado = "Fissuras detectadas"

        try:

            with open(caminho_arquivo, "rb") as f:

                files = {"file": f}

                response = requests.post(url, files=files)

                data = response.json()

            #apresentação da quantidade
            self.label.text = (
                f"{texto_resultado}: {data['count']}"
            )

            #conversão da imagem para base64
            img_data = base64.b64decode(data["image"])

            pil_image = PILImage.open(BytesIO(img_data))

            buffer = BytesIO()

            pil_image.save(buffer, format="PNG")

            buffer.seek(0)

            core_image = CoreImage(buffer, ext="png")

            self.img.texture = core_image.texture

        except Exception as e:

            self.label.text = f"Erro: {str(e)}"


#executação do app
if __name__ == "__main__":

    MeuApp().run()
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile
from django.utils import timezone


# Função que gera imagem da assinatura
def generate_signature_image(name: str) -> ContentFile:
    """Gera uma imagem com o nome do usuário como se fosse uma assinatura."""
    print("Gerando assinatura para:", name)

    try:
        font = ImageFont.truetype("BRADHITC.TTF", 40)
        print("Fonte carregada com sucesso.")
    except IOError:
        print("Fonte não encontrada, usando padrão.")
        font = ImageFont.load_default()

    dummy_img = Image.new('RGBA', (1, 1))
    draw_dummy = ImageDraw.Draw(dummy_img)
    bbox = draw_dummy.textbbox((0, 0), name, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    padding = 20
    img_width = text_width + padding * 2
    img_height = text_height + padding * 2

    img = Image.new('RGBA', (img_width, img_height), color=(255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    draw.text((padding, padding), name, font=font, fill=(0, 0, 0, 255))

    buffer = BytesIO()
    img.save(buffer, format='PNG')
    filename = f"assinatura_{name.lower().replace(' ', '_')}.png"

    return ContentFile(buffer.getvalue(), name=filename)

# Função para assinar
def assinar_formulario(instance, user, campo_assinatura, campo_data, campo_imagem, campo_dias=None):
     # Atribui o usuário ao campo de assinatura
    instance.__setattr__(campo_assinatura, user)
    # Define a data atual no campo de data de autorização
    now = timezone.now()
    instance.__setattr__(campo_data, now)

    # Calcula os dias desde a data da solicitação
    if campo_dias and instance.data_solicitacao:
        dias = (now.date() - instance.data_solicitacao.date()).days
        instance.__setattr__(campo_dias, dias)

    # Gera imagem da assinatura
    assinatura_img = generate_signature_image(
        str(user.get_full_name() or user.username or "USUÁRIO")
    )
    # Salva a imagem da assinatura no campo apropriado
    getattr(instance, campo_imagem).save(assinatura_img.name, assinatura_img, save=False)


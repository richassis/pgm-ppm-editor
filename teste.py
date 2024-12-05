import Imagem as im

I1 = im.ImagemPGM("Imagens/TonsDeCinza/peixes.pgm")

I1.brilho("saida01.pgm",50)
I1.espelha("saida02.pgm")


I2 = im.ImagemPPM("Imagens/Coloridas/teste.ppm")
I2.espelha("saida01.ppm")
I2.rotaciona90("saida02.ppm")

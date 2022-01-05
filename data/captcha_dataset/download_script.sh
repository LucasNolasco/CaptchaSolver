for i in {0..1039}
do
	echo Downloading ${i}
	wget https://servicos.receita.fazenda.gov.br/servicos/cnpjreva/captcha/gerarCaptcha.asp -O ${i}.png
done

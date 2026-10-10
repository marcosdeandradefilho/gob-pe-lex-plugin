# GOB-PE LEX — página pública

Página estática de apresentação, suporte, privacidade e termos do GOB-PE LEX.

Responsável: Marcos Antonio Soares de Andrade Filho.
Contato: marcos.de.andrade@gmail.com.

## Arquivos

- `dist/`: site completo, sem dependências ou chamadas de API.
- `generate.py`: conteúdo e estrutura das páginas; execute `python3 generate.py` após editar os textos.
- `vercel.json`: publicação estática na Vercel usando `dist` como diretório de saída.
- `.openai/hosting.json`: identidade e configuração do projeto Sites.

## Endereços

- `/`: apresentação.
- `/suporte/`: suporte.
- `/privacidade/`: aviso de privacidade.
- `/termos/`: termos de uso.

## Publicação na Vercel

Importe o repositório, selecione Framework Preset **Other**, deixe os comandos de instalação e build vazios e use **dist** como Output Directory. O arquivo vercel.json também fornece essas configurações.

O site não inclui os PDFs do acervo, conversas, credenciais ou dados de casos. Não há formulário, analytics, armazenamento local ou cookies definidos pelo código. Provedores de hospedagem podem registrar acessos técnicos.

## Situação do plugin

A página não afirma aprovação do plugin no diretório público. A autorização de distribuição do acervo, a revisão final dos materiais de publicação e a confirmação de práticas de retenção do suporte permanecem assuntos separados do deploy do site.

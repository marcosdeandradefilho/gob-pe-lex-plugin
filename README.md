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

## Consulta MCP (0.3.0)

Endpoint de produção: `https://gob-pe-lex-plugin.vercel.app/api/mcp`.
Transporte Streamable HTTP, público e somente leitura. Implementado com o SDK oficial MCP Python 2.3.0, com respostas JSON e sem sessões persistentes.

Ferramentas: `listar_documentos`, `buscar_normas` e `ler_pagina`. O índice contém nove documentos e 411 páginas, com proveniência SHA-256 e sinalização de OCR. Não certifica vigência, não protocola e não fornece decisões oficiais. Não há chamadas pagas a modelos, banco de usuários ou persistência de consultas no código. A Vercel aplica seus próprios limites e registros de infraestrutura.

### Executar e testar

```sh
python -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/uvicorn api.mcp:app --port 8765
# Em outro terminal:
.venv/bin/python tests/check_remote.py http://127.0.0.1:8765/api/mcp
```

Para reconstruir o índice a partir de uma cópia autorizada do pacote original:
`python scripts/build_corpus.py /caminho/do/pacote`.
O script confere hashes dos PDFs e dos textos. Números de identificação pessoal detectados são omitidos na saída pública. PDFs e caminhos locais não são copiados para este repositório.

A publicação do servidor não significa aprovação do plugin no diretório. Ainda são necessários conexão, verificação de domínio, testes, demonstração e revisão no portal. O titular deve confirmar seus direitos sobre a distribuição do acervo; alguns documentos contêm aviso de circulação restrita.

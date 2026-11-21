# Guia de AI Hub Publish

**Estado:** Em avaliação.

API de chat com verificação Docker confirmada.

[![AI Hub Publish. Preparar e arrancar. Verificar a resposta da API. Ollama real por validar.](docs/guia-visual.png)](docs/guia-visual.png)

## Onde começar

Segue [Testar a API localmente](README.md#testar-a-api-localmente).

## Como confirmar

`bash scripts/test_request.sh` deve devolver um JSON com `"ok": true`. Este teste confirma a API mesmo sem Ollama.

## Como ler os registos

`docker compose logs agent-hub` mostra o arranque. Se a saúde passar e o chat falhar, revê o endereço do Ollama e o nome do modelo. Em **Actions**, os testes do contentor aparecem separados.

### Exemplo fictício

```text
OK · API local · Serviço a responder
```

Lê pela ordem **resultado**, **etapa** e **detalhe**. Para investigar uma falha, confirma primeiro a data e a versão, depois abre o primeiro passo que falhou.

## Cuidados

O protótipo ainda não tem autenticação própria. Mantém o percurso de teste local e não partilhes o ficheiro `.env`. A conversa com Ollama real ainda não foi validada nesta revisão.

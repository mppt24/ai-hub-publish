# AI Hub

Protótipo do [MPPT24OS](https://github.com/mppt24/MPPT24OS) para experimentar uma API de chat com modelos locais. O serviço usa FastAPI e encaminha os pedidos para Ollama. A integração com OpenAI é opcional e vem desativada.

## Estado · Em avaliação

Protótipo para testes locais.

## Estrutura

| Ficheiro | Função |
| --- | --- |
| [`docker-compose.yml`](docker-compose.yml) | Define o serviço do Hub e um serviço Redis |
| [`agent-hub/main.py`](agent-hub/main.py) | Implementa a API e as integrações com os modelos |

## Testar a API localmente

São necessários Docker e Docker Compose. Na raiz do repositório, prepara a configuração, inicia o serviço e confirma que responde:

```bash
bash scripts/prepare_only.sh
docker compose config --quiet
bash scripts/start.sh
bash scripts/test_request.sh
```

A última linha devolve um objeto JSON com `"ok": true`. O teste funciona sem Ollama e sem credenciais. Para a lista de endpoints, abre [a documentação da API local](http://127.0.0.1:8181/docs).

É possível consultar os registos com `docker compose logs agent-hub` e parar o serviço com `docker compose down`.

## Ligar ao Ollama

Para usar `POST /chat`, define em `.env` o `OLLAMA_URL` de uma instância acessível a partir do contentor, volta a executar `bash scripts/start.sh` e indica em `model_ollama` um modelo instalado nessa instância.

Se o teste de saúde passar e o chat falhar, confirma primeiro o endereço do Ollama e o nome do modelo. O `127.0.0.1` visto de dentro do contentor aponta para o próprio contentor.

## Acesso ao Hub

Por omissão, a API responde apenas em `127.0.0.1:8181`. Como o Hub ainda não tem autenticação própria, mantém este endereço para testes locais. Para disponibilizar o serviço a outras pessoas, configura primeiro um controlo de acesso externo adequado.

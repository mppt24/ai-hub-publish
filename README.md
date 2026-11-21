# AI Hub

Protótipo do [MPPT24OS](https://github.com/mppt24/MPPT24OS) para experimentar uma API de chat com modelos locais. O serviço usa FastAPI e encaminha os pedidos para Ollama. A integração com OpenAI é opcional e vem desativada.

## Estrutura

| Ficheiro | Função |
| --- | --- |
| [`docker-compose.yml`](docker-compose.yml) | Define o serviço do Hub e um serviço Redis |
| [`agent-hub/main.py`](agent-hub/main.py) | Implementa a API e as integrações com os modelos |

## Testar a API localmente

São necessários Docker, Docker Compose e `curl`. A partir da raiz do repositório, valida a configuração e inicia o Hub apenas na interface local:

```bash
docker compose config --quiet
docker compose build agent-hub
docker compose run --rm --no-deps --publish 127.0.0.1:8181:8080 agent-hub
```

Noutro terminal, verifica se o Hub responde:

```bash
curl --fail --silent --show-error http://127.0.0.1:8181/
```

A resposta inclui `"ok": true`. Este teste confirma que a API está a responder. Para utilizar `POST /chat`, usa uma instância Ollama acessível a partir do contentor, define `OLLAMA_URL` e indica um modelo instalado nessa instância. Termina o teste com **Ctrl+C** no terminal onde o Hub está a correr.

A API é um protótipo sem autenticação. O exemplo acima limita o acesso ao próprio computador.

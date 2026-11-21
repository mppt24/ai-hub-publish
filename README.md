# AI Hub

O AI Hub é um serviço que recebe pedidos de chat de outras aplicações. Usa Ollama para encaminhar esses pedidos para modelos locais. É um protótipo do [MPPT24OS](https://github.com/mppt24/MPPT24OS) e usa FastAPI. A integração com OpenAI é opcional e vem desativada.

## Estado · Em avaliação

Podes confirmar que o serviço arranca antes de configurar qualquer modelo. [Guia de leitura, infográfico e cuidados](GUIA.md)

## Testar a API localmente

Precisas de Git, Docker e Docker Compose. Num terminal, descarrega o código, inicia o serviço e confirma que responde.

```bash
git clone https://github.com/mppt24/ai-hub-publish.git
cd ai-hub-publish
bash scripts/prepare_only.sh
docker compose config --quiet
bash scripts/start.sh
bash scripts/test_request.sh
```

A última linha devolve um objeto JSON com `"ok": true`. Este resultado confirma que a API está a responder. Para receber uma resposta de um modelo, segue a secção [Ligar ao Ollama](#ligar-ao-ollama). Para a lista de endpoints, abre [a documentação da API local](http://127.0.0.1:8181/docs).

É possível consultar os registos com `docker compose logs agent-hub` e parar o serviço com `docker compose down`.

## Ligar ao Ollama

Para usar `POST /chat`, define em `.env` o `OLLAMA_URL` de uma instância acessível a partir do contentor, volta a executar `bash scripts/start.sh` e indica em `model_ollama` um modelo instalado nessa instância.

Se o teste de saúde passar e o chat falhar, confirma primeiro o endereço do Ollama e o nome do modelo. O `127.0.0.1` visto de dentro do contentor aponta para o próprio contentor.

## Acesso ao Hub

Por omissão, o Docker publica a API em `127.0.0.1:8181`. Como o Hub ainda não tem autenticação própria, mantém este endereço para testes locais. Para disponibilizar o serviço a outras pessoas, configura primeiro um controlo de acesso externo adequado.

Em versões do Docker Engine anteriores à 28.0.0, outros equipamentos no mesmo segmento de rede podem alcançar portas publicadas em localhost. Consulta a [nota do Docker sobre publicação de portas](https://docs.docker.com/engine/network/port-publishing/#setting-the-default-bind-address-for-containers).

## Estrutura

| Ficheiro | Função |
| --- | --- |
| [`docker-compose.yml`](docker-compose.yml) | Define o serviço do Hub e um serviço Redis |
| [`agent-hub/main.py`](agent-hub/main.py) | Implementa a API e as integrações com os modelos |

<div lang="pt-PT">

# AI Hub

O AI Hub é um serviço que recebe pedidos de chat de outras aplicações. Usa Ollama para encaminhar esses pedidos para modelos locais. É um protótipo do [MPPT24OS](https://github.com/mppt24/MPPT24OS) e usa FastAPI. A integração com OpenAI é opcional e vem desativada.

## Estado · Em avaliação

Podes confirmar que o serviço arranca antes de configurar qualquer modelo. [Guia de leitura, infográfico e cuidados](GUIA.md)

## Testar a API localmente

Precisas de Git, Docker Engine 28 ou posterior e Docker Compose. Para esta primeira verificação, podes usar o Hub sem configurar um modelo ou fornecer chaves. Começa por obter uma cópia do código. Se já tens o repositório, abre essa pasta e passa ao segundo bloco.

```bash
git clone https://github.com/mppt24/ai-hub-publish.git && cd ai-hub-publish
```

Dentro da pasta, prepara a configuração.

```bash
bash scripts/prepare_only.sh
```

Se a pasta já tinha um ficheiro `.env`, o script mantém esse ficheiro. Para o teste local, confirma `HUB_BIND_ADDRESS=127.0.0.1` e `HUB_PORT=8181` antes de arrancar. Depois corre a verificação e o arranque. Cada passo depende do anterior.

```bash
docker compose config --quiet &&
  bash scripts/start.sh &&
  bash scripts/test_request.sh
```

A última linha deve mostrar `"ok": true`. Isso confirma que o serviço responde dentro do contentor. No computador onde corre o Docker, podes ver os pedidos que a aplicação aceita. [Abrir a documentação da API local](http://127.0.0.1:8181/docs)

Se o teste falhar, vê o estado com `docker compose ps` e as últimas mensagens com `docker compose logs --tail=30 agent-hub`. Se o teste passar mas a página não abrir, verifica se estás a usar o navegador no mesmo computador onde o Docker está a correr. Quando acabares, para o serviço com `docker compose down`.

## Ligar ao Ollama

Para usar `POST /chat`, define em `.env` o `OLLAMA_URL` de uma instância acessível a partir do contentor, volta a executar `bash scripts/start.sh` e indica em `model_ollama` um modelo instalado nessa instância.

Se o teste de saúde passar e o chat falhar, confirma primeiro o endereço do Ollama e o nome do modelo. O `127.0.0.1` visto de dentro do contentor aponta para o próprio contentor.

## Acesso ao Hub

Por omissão, o Docker publica a API em `127.0.0.1:8181`. Como o Hub ainda não tem autenticação própria, mantém este endereço para testes locais. Para disponibilizar o serviço a outras pessoas, configura primeiro um controlo de acesso externo adequado.

Em versões do Docker Engine anteriores à 28.0.0, outros equipamentos no mesmo segmento de rede podem alcançar portas publicadas em localhost. Consulta a [nota do Docker sobre publicação de portas](https://docs.docker.com/engine/network/port-publishing/#setting-the-default-bind-address-for-containers).

## Apontamentos de desenvolvimento

O [plano de acessibilidade](plano.md) regista objetivos e ideias. Os ficheiros de pedidos e respostas na raiz são material de trabalho. O percurso de utilização verificado está em [Testar a API localmente](#testar-a-api-localmente).

## Estrutura

| Ficheiro | Função |
| --- | --- |
| [`docker-compose.yml`](docker-compose.yml) | Define o serviço do Hub e um serviço Redis |
| [`agent-hub/main.py`](agent-hub/main.py) | Implementa a API e as integrações com os modelos |

</div>

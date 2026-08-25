
<img src="../assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=30% height=30%>

# AI Project Document — Challenge Sompo × FIAP — Sprint 3

## Sompo AgroPredict

#### Nomes dos integrantes do grupo

- Renata de Almeida Marinho — RM569342
- Giselli Mayumi Takahashi Yokoyama — RM572690
- David Ribeiro Prado de Lacerda — RM570350
- João Otavio Moraes — RM573227
- Pedro Henrique Lacerda — RM573114

## Sumário

[1. Introdução](#c1)

[2. Visão Geral do Projeto](#c2)

[3. Desenvolvimento do Projeto](#c3)

[4. Resultados e Avaliações](#c4)

[5. Conclusões e Trabalhos Futuros](#c5)

[6. Referências](#c6)

[Anexos](#c7)

<br>

# <a name="c1"></a>1. Introdução

## 1.1. Escopo do Projeto

### 1.1.1. Contexto da Inteligência Artificial

O setor de seguros opera historicamente de forma **reativa**: o risco é precificado na contratação da
apólice e a seguradora só volta a agir quando o sinistro já aconteceu, no momento da indenização.
Aplicações de Inteligência Artificial vêm deslocando esse eixo para a **prevenção** — a chamada
*predictive underwriting* e o *risk engineering* orientado a dados —, em que modelos consomem
telemetria em tempo real para antecipar o evento antes que ele ocorra.

No agronegócio esse deslocamento é especialmente valioso. O Brasil é um dos maiores mercados
agrícolas do mundo e concentra frotas de equipamentos de alto valor unitário (colheitadeiras,
tratores, pulverizadores) operando em condições ambientais adversas e variáveis. Incidentes como
atolamento, tombamento em declive e falha mecânica por desgaste geram sinistros caros e paradas de
operação em janelas de safra curtas, nas quais cada hora parada tem custo direto para o produtor.

A abrangência da aplicação é **nacional**, com potencial de replicação regional (América Latina), e o
segmento de atuação é a intersecção entre **seguros patrimoniais/agrícolas** e **gestão de frotas
agrícolas**. As atividades executadas pelo sistema são coleta de telemetria, classificação de risco
operacional e emissão de recomendação preventiva.

### 1.1.2. Descrição da Solução Desenvolvida

O **Sompo AgroPredict** é uma plataforma de monitoramento preventivo de risco operacional para
equipamentos agrícolas. A proposta de valor é direta: **em vez de pagar o sinistro depois, calcular
o risco antes**.

A solução captura variáveis ambientais (umidade do solo, chuva acumulada em 24h, temperatura,
declividade) e operacionais (velocidade, idade da máquina, horas de operação, tipo de operação),
classifica o risco da operação corrente em três níveis — **BAIXO, MÉDIO e ALTO** — e devolve, junto
com um score de 0 a 100, uma **recomendação contextual acionável** ("reduzir velocidade
imediatamente", "evitar áreas saturadas", "suspender operação").

Uma decisão de projeto central orienta toda a arquitetura: **todas as variáveis são captáveis por
fontes externas à máquina** — o celular do operador, uma API pública de clima e o cadastro do
equipamento. Isso viabiliza a adoção em **frotas legadas**, que representam a maior parte do parque
brasileiro e não possuem telemetria proprietária embarcada. A barreira de entrada do cliente cai de
"instalar hardware em cada máquina" para "abrir um link no celular".

# <a name="c2"></a>2. Visão Geral do Projeto

## 2.1. Objetivos do Projeto

O objetivo geral é **transformar a gestão de risco agrícola de reativa em preventiva**, reduzindo a
sinistralidade nas operações e no transporte de equipamentos.

Objetivos específicos desta Sprint 3, focada em **integração**:

| # | Objetivo | Situação |
|---|---|---|
| 1 | **Backend integrador em Python** que orquestra o fluxo, conectando entrada de dados, banco e modelo de risco | ✅ Implementado |
| 2 | **Engenharia de dados** — persistir dados recebidos e scores gerados, com pipelines prontos para alimentar o modelo | ✅ Implementado no SQLite, banco relacional principal do MVP; schema Oracle disponível como integração opcional |
| 3 | **Integração com fontes** — receber telemetria, ambiente e operação, validando como os dados chegam | ✅ Implementado (GPS real + Open-Meteo) |
| 4 | **Segurança da informação** — controle de acesso, proteção dos serviços e integridade dos dados | ✅ Implementado no MVP (login obrigatório, log de acessos, credenciais externas e integridade); RBAC por perfil permanece como evolução |
| 5 | **Interface simples** — dashboard exibindo scores e alertas de forma clara | ✅ Implementado (Streamlit) |

A meta da entrega é um **MVP com cerca de 60% da solução em funcionamento**, demonstrando o caminho
completo de ponta a ponta em detrimento do polimento visual.

## 2.2. Público-Alvo

A solução foi desenhada para três personas, formalizadas como User Stories em
[`user_stories.md`](user_stories.md):

| Persona | Necessidade | Como a solução atende |
|---|---|---|
| **Operador de campo** (US-01) | Decidir em segundos, sem tirar o olho da operação | Card de risco grande, colorido por classe, com uma única recomendação em linguagem direta — baixa carga cognitiva |
| **Gestor de frota** (US-02) | Enxergar onde está o risco na operação do dia | Dashboard com score corrente, indicadores por variável e histórico de predições |
| **Analista da seguradora** (US-03) | Justificar avaliações e analisar sinistros | *Feature importance* explicando cada decisão, `versao_modelo` e probabilidades gravadas por predição, trilha de aderência aos alertas |

## 2.3. Metodologia

O projeto foi desenvolvido de forma **incremental ao longo de três sprints**, cada uma entregando um
artefato funcional que a seguinte integra:

| Sprint | Foco | Entregas |
|---|---|---|
| **Sprint 1** | Estrutura e proposta | Definição do problema, personas, dataset simulado inicial, mockups |
| **Sprint 2** | Modelo preditivo | Dataset ampliado (8 features, 1000 linhas), Random Forest treinado e validado, schema Oracle, dashboard funcional, User Stories formalizadas |
| **Sprint 3** | **Integração end-to-end** | Telemetria real (GPS + clima), persistência automática no SQLite, orquestração do fluxo completo, reorganização no padrão de template FIAP |

As etapas seguidas nesta Sprint foram:

1. **Definição do fluxo alvo** — desenho da arquitetura `entrada → banco → modelo → saída`
2. **Substituição das fontes simuladas** — troca dos sliders por GPS e API climática, mantendo *fallback* manual campo a campo
3. **Camada de persistência resiliente** — gravação automática no SQLite a cada ciclo, com schema Oracle preparado como extensão opcional
4. **Validação do fluxo** — verificação de que uma leitura real percorre todo o caminho até a tela e o banco
5. **Documentação** — README com arquitetura, diagramas e justificativa das decisões técnicas

# <a name="c3"></a>3. Desenvolvimento do Projeto

## 3.1. Tecnologias Utilizadas

| Camada | Tecnologia | Papel no projeto |
|---|---|---|
| **Linguagem** | Python 3.10+ | Backend integrador e toda a orquestração |
| **Machine Learning** | scikit-learn, joblib | Pipeline de pré-processamento + Random Forest; serialização em `modelo.pkl` |
| **Manipulação de dados** | pandas, numpy | Geração do dataset, preparo das features, leitura do histórico |
| **Interface** | Streamlit | Dashboard funcional, sem front-end sofisticado |
| **Telemetria** | streamlit-js-eval, streamlit-autorefresh | Acesso à geolocalização do navegador e ciclo de atualização de 10s |
| **Fonte externa** | API Open-Meteo (via `requests`) | Temperatura, chuva 24h e aproximação de umidade do solo — gratuita, sem API key |
| **Banco relacional principal** | SQLite (`sqlite3`, biblioteca padrão) | Persistência funcional de predições e logs de acesso; funciona localmente e sem serviço externo |
| **Integração opcional** | Oracle XE 21c (`oracledb`) | Schema, consultas e conector preparados para uma implantação centralizada futura |
| **Visualização (notebook)** | matplotlib, seaborn | Gráficos de análise exploratória e avaliação do modelo |

### Organização do código

O código-fonte está em `src/`, organizado em módulos com responsabilidade única:

| Módulo | Responsabilidade |
|---|---|
| `dashboard/app.py` | Orquestra o fluxo: captura → predição → regras → persistência → apresentação |
| `dashboard/gps.py` | Captura de posição e cálculo de velocidade (nativa ou Haversine) |
| `dashboard/clima.py` | Integração com a Open-Meteo, com tratamento de falha explícito |
| `dashboard/persistencia.py` | Gravação no SQLite principal e conector Oracle opcional |
| `sql/schema.sql` | DDL: 4 tabelas, 1 view, 2 sequences, constraints e índices |
| `sql/inserir_predicoes.py` | Ingestão em lote de predições e alertas no Oracle |
| `data/gerar_dataset_v2.py` | Geração estratificada do dataset de treino |

O tratamento de exceções segue o princípio de **degradação graciosa**: uma falha na API de clima ou
no banco Oracle não derruba a aplicação — o sistema informa a origem indisponível e continua
operando com a fonte alternativa.

## 3.2. Modelagem e Algoritmos

### Algoritmo escolhido: Random Forest Classifier

| Critério | Justificativa |
|---|---|
| **Interações não-lineares** | O risco no domínio é combinatório — "umidade alta **e** chuva alta" implica atolamento, mas nenhuma das duas isoladamente. Árvores capturam isso nativamente |
| **Volume de dados** | 1000 linhas: pequeno demais para *deep learning*, grande demais para uma árvore única que sofreria *overfitting* |
| **Features mistas** | 7 numéricas + 1 categórica, sem exigência de normalização |
| **Interpretabilidade** | *Feature importance* nativa — requisito não-negociável para uma seguradora justificar avaliações e para conformidade com a LGPD (art. 20) |

### Implementação

```python
RandomForestClassifier(
    n_estimators=300,
    min_samples_split=2,
    min_samples_leaf=2,        # leve regularização
    max_features='sqrt',
    class_weight='balanced',   # compensa desbalanceamento entre classes
    random_state=42
)
```

Os hiperparâmetros foram definidos por *grid search* manual sobre 5 combinações, avaliadas por F1
macro em validação cruzada.

O modelo é encapsulado em um `Pipeline` com um `ColumnTransformer` — variáveis numéricas em
*passthrough*, `status_operacao` em `OneHotEncoder(drop='first')`. Todo o pipeline é serializado em
`modelo.pkl`, de forma que o dashboard e o script de ingestão apenas fazem `joblib.load()`, sem
duplicar lógica de pré-processamento.

### Camada de regras de domínio

Sobre a saída do modelo há uma camada determinística de segurança: se **qualquer** variável cruza um
limite crítico absoluto (`umidade_solo ≥ 45`, `declividade ≥ 25`, `chuva_24h ≥ 40`,
`temperatura ≥ 45`, `velocidade ≥ 20`), a classe é forçada para **ALTO** independentemente da
predição estatística, e o motivo do *override* é exibido ao operador.

O racional é de domínio, não de modelagem: em situações inequivocamente perigosas, a segurança do
operador não deve depender da confiança de um modelo probabilístico treinado em dados simulados.

## 3.3. Treinamento e Teste

### Conjunto de dados

O dataset de treino (`src/data/dataset_v2.csv`) é **simulado**, gerado por
`gerar_dataset_v2.py` com 1000 linhas em geração **estratificada** por cenário:

| Cenário | Proporção | Característica |
|---|---|---|
| Seguro | 45% | Umidade baixa, declividade baixa, velocidade moderada |
| Limite | 35% | Variáveis em zonas de transição |
| Crítico | 20% | Múltiplos fatores adversos sobrepostos |

A estratificação garante representatividade das três classes e reflete a realidade do agro, em que a
maioria das operações é segura. Todas as features passam por `np.clip` para permanecerem em faixas
fisicamente plausíveis.

### Protocolo de avaliação

- Divisão treino/teste com conjunto de teste de **250 amostras**
- **Validação cruzada 5-fold** para estimativa mais robusta
- Métricas: **acurácia** e **F1 macro** — F1 macro é a métrica principal, por tratar as três classes
  com o mesmo peso apesar do desbalanceamento
- **Baseline** de comparação: Regressão Logística

### Rebalanceamento

A classe MÉDIO, por ser fronteiriça entre BAIXO e ALTO, era a mais difícil. O dataset foi
rebalanceado para elevar sua representação de ~10% para ~14% das amostras, o que aumentou o F1 macro
de 76% para 81% ao custo de aproximadamente 1 ponto percentual de acurácia global — *trade-off*
favorável no domínio.

# <a name="c4"></a>4. Resultados e Avaliações

## 4.1. Análise dos Resultados

### Métricas obtidas

| Modelo | Acurácia (teste) | F1 macro (teste) | Acurácia (CV 5-fold) | F1 macro (CV 5-fold) |
|---|---|---|---|---|
| Logistic Regression (baseline) | 83.2% | 79.3% | — | — |
| **Random Forest (final)** | **89.2%** | **81.7%** | **89.6% (±2.3%)** | **81.4% (±4.8%)** |

O Random Forest supera o baseline em 6 pontos de acurácia, confirmando a hipótese de que as
interações não-lineares entre as variáveis são relevantes no domínio. A proximidade entre a métrica
de teste (89.2%) e a de validação cruzada (89.6% ±2.3%) indica ausência de *overfitting* relevante.

### Matriz de confusão (teste set, n=250)

```
              Predito
Real      BAIXO  MEDIO  ALTO
BAIXO     [162    9      0]
MEDIO     [  6   23      5]
ALTO      [  0    7     38]
```

A análise qualitativa é mais informativa que o número agregado:

- **Não há confusão entre os extremos** (BAIXO ↔ ALTO = 0 casos). Este é o comportamento desejado: os
  erros remanescentes acontecem apenas entre classes adjacentes, ou seja, o modelo nunca classifica
  como segura uma situação perigosa.
- **Recall de ALTO = 84%** (38/45) — a métrica mais crítica do domínio, já que um falso negativo de
  ALTO significa deixar passar uma situação de risco real.
- **Recall de MÉDIO = 68%** (23/34) — a classe mais fraca, como esperado por ser fronteiriça.

### Interpretabilidade

As cinco variáveis de maior peso na decisão são, em ordem: `umidade_solo`, `velocidade`,
`temperatura`, `chuva_24h` e `declividade`. Isso é coerente com o conhecimento de domínio — umidade
e velocidade são os principais determinantes de atolamento e perda de controle — e permite que
qualquer classificação ALTO seja explicada apontando a combinação das 2–3 variáveis dominantes.

### Diferença entre o resultado esperado e o real

A principal divergência entre expectativa e realidade **não está nas métricas, e sim na natureza dos
dados**: as métricas acima foram calculadas sobre dados **simulados**. A integração com GPS e clima
reais desta Sprint mudou a **origem dos inputs em produção**, mas o modelo continua reconhecendo
padrões aprendidos na simulação. A validação do modelo contra dados reais de campo é o passo
seguinte e ainda não foi feita — o que impõe cautela na leitura desses números.

## 4.2. Feedback dos Usuários

*Seção a ser preenchida após a validação com os usuários finais.*

O feedback recebido até aqui vem da avaliação das sprints anteriores e orientou decisões concretas do
projeto:

- **Ampliação do dataset** — de 5 para 8 variáveis e de ~50 para 1000 linhas, em resposta ao
  apontamento de que o volume inicial era insuficiente para sustentar um modelo
- **Formalização das User Stories** — em formato Dado/Quando/Então, com critérios de aceite
  rastreáveis aos entregáveis técnicos
- **Baixa carga cognitiva na interface** — a partir da constatação de que o operador não pode
  desviar atenção da operação, o resultado foi reduzido a um card único, colorido e com uma só
  recomendação

# <a name="c5"></a>5. Conclusões e Trabalhos Futuros

## Como a solução atingiu os objetivos

O objetivo central desta Sprint — **integrar os módulos em um fluxo contínuo** — foi atingido. Uma
leitura real percorre hoje todo o caminho sem intervenção manual: o GPS do celular fornece posição e
velocidade, a Open-Meteo devolve as condições ambientais daquela coordenada, o pipeline entrega
classe, score e probabilidades, a camada de regras aplica *override* quando necessário, e o
resultado é simultaneamente exibido na tela e gravado no SQLite — tudo em um ciclo de 10 segundos.

## Pontos fortes

- **Fluxo end-to-end real**, não simulado: a telemetria vem de fontes externas efetivas
- **Resiliência por design**: o SQLite mantém o fluxo operacional sem depender de um serviço de banco externo
- **Baixa barreira de adoção**: nenhuma variável exige hardware embarcado, viabilizando frotas legadas
- **Decisões auditáveis**: o histórico SQLite registra entradas, classe, score, recomendação e a
  origem de cada dado (GPS, API ou manual); o schema Oracle opcional prevê versão e probabilidades
- **Honestidade sobre o alcance**: o projeto distingue explicitamente o que é real do que é
  aproximado ou simulado

## Pontos a melhorar

| Ponto | Situação atual |
|---|---|
| **Perfis de acesso** | O dashboard exige autenticação, mas o MVP ainda utiliza um único perfil, sem separação entre operador, gestor e analista |
| **Usuário Oracle dedicado** | Credenciais padrão foram removidas do código; falta criar no Oracle um usuário de aplicação com *grants* mínimos |
| **Modelo treinado em dados simulados** | Nenhuma validação contra sinistros reais confirmados |
| **Segmentação por frota** | IDs de equipamento e operador ainda fixos; sem seletor nem ranking |
| **Alertas em tempo real** | A tabela `alertas` só é populada pelo script batch |
| **Dados pessoais** | Campo `cpf` em texto claro no schema |
| **Umidade do solo** | Aproximação por modelo de superfície, não sensor dedicado |

## Plano de ações futuras

| Prioridade | Ação | Resultado esperado |
|---|---|---|
| 1 | Criar usuário de aplicação no Oracle com *grants* mínimos e adicionar perfis de acesso ao dashboard | Evolui o login atual para RBAC completo |
| 2 | Gravar a tabela `alertas` no fluxo em tempo real, com registro da ação do operador | Fecha o ciclo de auditoria da US-03 |
| 3 | Introduzir seletor de equipamento e agregação por frota/região | Atende plenamente a US-02 |
| 4 | Coletar rótulos reais (sinistros confirmados) e reavaliar o modelo | Substitui a validação sintética por validação de campo |
| 5 | Integrar sensor de solo dedicado ou imagem de satélite | Elimina a aproximação da variável mais importante do modelo |
| 6 | Anonimizar/mascarar dados pessoais no schema | Conformidade plena com a LGPD |

# <a name="c6"></a>6. Referências

- **Open-Meteo API** — documentação da API climática gratuita utilizada: https://open-meteo.com/en/docs
- **scikit-learn** — documentação do `RandomForestClassifier` e de `Pipeline`/`ColumnTransformer`: https://scikit-learn.org/stable/
- **Streamlit** — documentação oficial do framework de interface: https://docs.streamlit.io/
- **python-oracledb** — driver Oracle para Python: https://python-oracledb.readthedocs.io/
- **MDN Web Docs — Geolocation API** — referência da API de geolocalização do navegador: https://developer.mozilla.org/en-US/docs/Web/API/Geolocation_API
- **LGPD — Lei nº 13.709/2018**, art. 20 (direito à revisão de decisões automatizadas): https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm

# <a name="c7"></a>Anexos

## Anexo A — Arquitetura integrada

O diagrama completo do fluxo de ponta a ponta (entrada → banco → modelo → saída) está no
[README do projeto](../README.md#-arquitetura-integrada-ponta-a-ponta), em formato Mermaid.

## Anexo B — Modelo de dados

O diagrama entidade-relacionamento do banco Oracle XE (tabelas `equipamentos`, `operadores`,
`predicoes` e `alertas`) está no [README do projeto](../README.md#-engenharia-de-dados). O DDL
completo está em [`../src/sql/schema.sql`](../src/sql/schema.sql).

## Anexo C — User Stories

As três User Stories, com seus 12 critérios de aceite no formato Dado/Quando/Então, estão em
[`user_stories.md`](user_stories.md).

## Anexo D — Gráficos e evidências visuais do MVP

Os gráficos foram gerados pelo notebook
[`../src/modelo/random_forest.ipynb`](../src/modelo/random_forest.ipynb) e salvos em `../assets/`,
junto aos prints do fluxo integrado:

| Arquivo | Conteúdo |
|---|---|
| `01_distribuicao_classes.png` | Distribuição das classes de risco no dataset |
| `02_boxplot_features.png` | Dispersão das features por classe |
| `03_correlacao.png` | Matriz de correlação entre variáveis |
| `04_operacao_vs_risco.png` | Relação entre tipo de operação e risco |
| `05_matriz_confusao.png` | Matriz de confusão do modelo final |
| `06_feature_importance.png` | Importância global das variáveis do modelo |
| `07_dashboard_baixo.png` | Print do dashboard em cenário seguro |
| `08_dashboard_alto.png` | Print do dashboard em cenário crítico com override |
| `09_dashboard_historico.png` | Print do histórico persistido no SQLite |

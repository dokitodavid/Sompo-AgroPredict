# scripts

Scripts auxiliares de execucao e operacao do projeto.

| Script | Descricao |
|---|---|
| `run_dashboard.ps1` | Sobe o dashboard Streamlit no Windows (PowerShell), a partir da raiz do repositorio. |
| `run_dashboard.sh` | Mesma funcao, para Linux/macOS. |

Os scripts de banco de dados (DDL e ingestao) ficam em [`../src/sql/`](../src/sql/),
junto ao restante do codigo-fonte:

- `src/sql/schema.sql` — criacao das tabelas, view e sequences no Oracle XE
- `src/sql/inserir_predicoes.py` — ingestao em lote de predicoes no banco
- `src/sql/consultas.sql` — queries de analise
